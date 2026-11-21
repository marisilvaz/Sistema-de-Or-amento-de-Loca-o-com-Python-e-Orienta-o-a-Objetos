"""Taxa contratual: custo único, separado do aluguel mensal, parcelável em até 5 vezes."""

from decimal import Decimal

from .utils import arredondar


class TaxaContratual:
    VALOR_TOTAL = Decimal("2000.00")
    MAXIMO_PARCELAS = 5

    def __init__(self, parcelas: int):
        if not 1 <= parcelas <= self.MAXIMO_PARCELAS:
            raise ValueError(f"A taxa contratual pode ser paga em 1 a {self.MAXIMO_PARCELAS} parcelas.")
        self.parcelas = parcelas

    def valores_das_parcelas(self) -> list[Decimal]:
        """Divide a taxa em parcelas. Diferenças de centavos ficam na última parcela,
        garantindo que a soma seja exatamente R$ 2.000,00 (ex.: 3x = 666,67 + 666,67 + 666,66)."""
        parcela = arredondar(self.VALOR_TOTAL / self.parcelas)
        valores = [parcela] * (self.parcelas - 1)
        valores.append(self.VALOR_TOTAL - parcela * (self.parcelas - 1))
        return valores

    def parcela_do_mes(self, mes: int) -> Decimal:
        """Valor da taxa cobrado no mês informado (1 a 12). Zero depois da última parcela."""
        if 1 <= mes <= self.parcelas:
            return self.valores_das_parcelas()[mes - 1]
        return Decimal("0.00")

    def descricao(self) -> str:
        if self.parcelas == 1:
            return "à vista (1x)"
        valores = self.valores_das_parcelas()
        if len(set(valores)) == 1:
            return f"{self.parcelas}x de R$ {valores[0]:.2f}".replace(".", ",")
        return (f"{self.parcelas}x (de R$ {valores[0]:.2f}, última de R$ {valores[-1]:.2f})"
                .replace(".", ","))
