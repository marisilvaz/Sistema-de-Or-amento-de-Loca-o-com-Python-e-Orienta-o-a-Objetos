"""Funções auxiliares de formatação de valores monetários."""

from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def arredondar(valor: Decimal) -> Decimal:
    """Arredonda um valor para duas casas decimais (centavos)."""
    return Decimal(valor).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def formatar_moeda(valor: Decimal) -> str:
    """Formata um valor no padrão brasileiro. Ex.: 1234.5 -> 'R$ 1.234,50'."""
    valor = arredondar(valor)
    texto = f"{abs(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    sinal = "- " if valor < 0 else ""
    return f"{sinal}R$ {texto}"


def formatar_numero(valor: Decimal) -> str:
    """Formata um valor sem o símbolo de moeda, com vírgula decimal (usado no CSV)."""
    return f"{arredondar(valor):.2f}".replace(".", ",")
