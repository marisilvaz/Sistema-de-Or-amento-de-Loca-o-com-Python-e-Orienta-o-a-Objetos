"""Classes que representam os imóveis da R.M Imóveis e suas regras de preço.

Hierarquia:

    Imovel (abstrata)
    ├── ImovelResidencial (abstrata)  -> regras comuns a casa e apartamento
    │   ├── Apartamento
    │   └── Casa
    └── Estudio
"""

from abc import ABC, abstractmethod
from decimal import Decimal

from .utils import arredondar


class ItemOrcamento:
    """Uma linha do orçamento: descrição e valor (positivo = acréscimo, negativo = desconto)."""

    def __init__(self, descricao: str, valor: Decimal):
        self.descricao = descricao
        self.valor = arredondar(valor)

    def __repr__(self) -> str:
        return f"ItemOrcamento({self.descricao!r}, {self.valor})"


class Imovel(ABC):
    """Classe base de todos os imóveis.

    Define o algoritmo geral de cálculo do aluguel mensal:
        aluguel = aluguel-base + adicionais - descontos
    As subclasses informam apenas o que muda: o aluguel-base, os adicionais e os descontos.
    """

    ALUGUEL_BASE = Decimal("0.00")
    NOME = "Imóvel"

    def itens_adicionais(self) -> list[ItemOrcamento]:
        """Acréscimos ao aluguel-base. Cada subclasse define os seus."""
        return []

    def itens_desconto(self, subtotal: Decimal) -> list[ItemOrcamento]:
        """Descontos aplicados sobre o subtotal (base + adicionais). Padrão: nenhum."""
        return []

    def composicao_aluguel(self) -> list[ItemOrcamento]:
        """Monta, em ordem, todas as linhas que formam o aluguel mensal."""
        itens = [ItemOrcamento(f"Aluguel-base ({self.NOME})", self.ALUGUEL_BASE)]
        itens += self.itens_adicionais()
        subtotal = sum((item.valor for item in itens), Decimal("0"))
        itens += self.itens_desconto(subtotal)
        return itens

    def calcular_aluguel_mensal(self) -> Decimal:
        """Soma todas as linhas da composição do aluguel."""
        return arredondar(sum((item.valor for item in self.composicao_aluguel()), Decimal("0")))

    @abstractmethod
    def descricao(self) -> str:
        """Texto curto com as características escolhidas."""


class ImovelResidencial(Imovel, ABC):
    """Regras comuns a casas e apartamentos: 1 ou 2 quartos e vaga de garagem opcional."""

    ADICIONAL_SEGUNDO_QUARTO = Decimal("0.00")
    VALOR_GARAGEM = Decimal("300.00")
    QUARTOS_PERMITIDOS = (1, 2)

    def __init__(self, quartos: int, possui_garagem: bool):
        if quartos not in self.QUARTOS_PERMITIDOS:
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.possui_garagem = possui_garagem

    def itens_adicionais(self) -> list[ItemOrcamento]:
        itens = []
        if self.quartos == 2:
            itens.append(ItemOrcamento("Adicional por 2 quartos", self.ADICIONAL_SEGUNDO_QUARTO))
        if self.possui_garagem:
            itens.append(ItemOrcamento("Vaga de garagem", self.VALOR_GARAGEM))
        return itens

    def descricao(self) -> str:
        garagem = "com vaga de garagem" if self.possui_garagem else "sem vaga de garagem"
        quarto = "quarto" if self.quartos == 1 else "quartos"
        return f"{self.NOME} – {self.quartos} {quarto}, {garagem}"


class Apartamento(ImovelResidencial):
    ALUGUEL_BASE = Decimal("700.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("200.00")
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = Decimal("0.05")
    NOME = "Apartamento"

    def __init__(self, quartos: int, possui_garagem: bool, possui_criancas: bool):
        super().__init__(quartos, possui_garagem)
        self.possui_criancas = possui_criancas

    def itens_desconto(self, subtotal: Decimal) -> list[ItemOrcamento]:
        # Regra exclusiva de apartamento: 5% para quem não tem crianças,
        # calculado depois de somados os adicionais.
        if self.possui_criancas:
            return []
        desconto = arredondar(subtotal * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS)
        return [ItemOrcamento("Desconto de 5% (sem crianças)", -desconto)]

    def descricao(self) -> str:
        criancas = "possui crianças" if self.possui_criancas else "não possui crianças"
        return f"{super().descricao()}, cliente {criancas}"


class Casa(ImovelResidencial):
    ALUGUEL_BASE = Decimal("900.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("250.00")
    NOME = "Casa"


class Estudio(Imovel):
    """Estúdio: não tem opção de quartos; estacionamento vendido em pacote de 2 vagas."""

    ALUGUEL_BASE = Decimal("1200.00")
    VALOR_PACOTE_ESTACIONAMENTO = Decimal("250.00")
    VAGAS_NO_PACOTE = 2
    VALOR_VAGA_ADICIONAL = Decimal("60.00")
    NOME = "Estúdio"

    def __init__(self, quer_estacionamento: bool, vagas_adicionais: int = 0):
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        if not quer_estacionamento and vagas_adicionais > 0:
            raise ValueError("Vagas adicionais exigem a contratação do pacote de estacionamento.")
        self.quer_estacionamento = quer_estacionamento
        self.vagas_adicionais = vagas_adicionais

    @property
    def total_vagas(self) -> int:
        if not self.quer_estacionamento:
            return 0
        return self.VAGAS_NO_PACOTE + self.vagas_adicionais

    def itens_adicionais(self) -> list[ItemOrcamento]:
        itens = []
        if self.quer_estacionamento:
            itens.append(ItemOrcamento(
                f"Pacote de estacionamento ({self.VAGAS_NO_PACOTE} vagas)",
                self.VALOR_PACOTE_ESTACIONAMENTO,
            ))
        if self.vagas_adicionais > 0:
            itens.append(ItemOrcamento(
                f"{self.vagas_adicionais} vaga(s) adicional(is) x R$ 60,00",
                self.VALOR_VAGA_ADICIONAL * self.vagas_adicionais,
            ))
        return itens

    def descricao(self) -> str:
        if self.total_vagas == 0:
            return f"{self.NOME} – sem estacionamento"
        return f"{self.NOME} – {self.total_vagas} vagas de estacionamento"
