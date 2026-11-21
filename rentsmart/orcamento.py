"""Cliente e orçamento: reúnem imóvel e taxa contratual e geram resumo e projeção."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .contrato import TaxaContratual
from .imoveis import Imovel
from .utils import arredondar, formatar_moeda


class Cliente:
    def __init__(self, nome: str):
        nome = nome.strip()
        if not nome:
            raise ValueError("O nome do cliente não pode ficar em branco.")
        self.nome = nome


@dataclass
class ParcelaProjecao:
    """Uma linha da projeção mensal."""
    mes: int
    aluguel: Decimal
    parcela_taxa: Decimal
    total_mes: Decimal
    total_acumulado: Decimal


class Orcamento:
    MESES_PROJECAO = 12

    def __init__(self, cliente: Cliente, imovel: Imovel, taxa: TaxaContratual):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa
        self.data = date.today()

    def aluguel_mensal(self) -> Decimal:
        return self.imovel.calcular_aluguel_mensal()

    def gerar_projecao(self) -> list[ParcelaProjecao]:
        """Projeção dos 12 primeiros meses: aluguel + parcela da taxa (quando houver)."""
        projecao = []
        acumulado = Decimal("0.00")
        aluguel = self.aluguel_mensal()
        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            total = arredondar(aluguel + parcela)
            acumulado += total
            projecao.append(ParcelaProjecao(mes, aluguel, parcela, total, acumulado))
        return projecao

    def total_primeiro_ano(self) -> Decimal:
        return self.gerar_projecao()[-1].total_acumulado

    def resumo(self) -> str:
        """Texto do orçamento, mostrando como o valor final foi formado."""
        linha = "-" * 58
        partes = [
            "=" * 58,
            "        RentSmart – R.M Imóveis | ORÇAMENTO DE LOCAÇÃO",
            "=" * 58,
            f"Cliente: {self.cliente.nome}",
            f"Data:    {self.data.strftime('%d/%m/%Y')}",
            f"Imóvel:  {self.imovel.descricao()}",
            linha,
            "ALUGUEL MENSAL",
        ]
        for item in self.imovel.composicao_aluguel():
            partes.append(f"  {item.descricao:<40}{formatar_moeda(item.valor):>14}")
        partes += [
            linha,
            f"  {'VALOR MENSAL DO ALUGUEL':<40}{formatar_moeda(self.aluguel_mensal()):>14}",
            linha,
            "TAXA CONTRATUAL (cobrada à parte, não faz parte do aluguel)",
            f"  {'Valor total da taxa':<40}{formatar_moeda(self.taxa.VALOR_TOTAL):>14}",
            f"  Parcelamento escolhido: {self.taxa.descricao()}",
            linha,
            f"  {'Total previsto nos primeiros 12 meses':<40}{formatar_moeda(self.total_primeiro_ano()):>14}",
            "=" * 58,
        ]
        return "\n".join(partes)
