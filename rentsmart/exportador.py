"""Geração do arquivo CSV com a projeção de 12 meses."""

import csv
from pathlib import Path

from .orcamento import Orcamento
from .utils import formatar_numero


class ExportadorCSV:
    """Grava a projeção em CSV no padrão brasileiro (separador ';' e vírgula decimal),
    para abrir corretamente no Excel e no Google Planilhas."""

    CABECALHO = ["Mês", "Aluguel (R$)", "Parcela da taxa contratual (R$)", "Total do mês (R$)", "Total acumulado (R$)"]

    def __init__(self, pasta_saida: str = "saida"):
        self.pasta_saida = Path(pasta_saida)

    def nome_arquivo(self, orcamento: Orcamento) -> Path:
        nome = "".join(c if c.isalnum() else "_" for c in orcamento.cliente.nome.lower()).strip("_")
        return self.pasta_saida / f"projecao_12_meses_{nome}.csv"

    def exportar(self, orcamento: Orcamento) -> Path:
        self.pasta_saida.mkdir(parents=True, exist_ok=True)
        caminho = self.nome_arquivo(orcamento)
        projecao = orcamento.gerar_projecao()
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(self.CABECALHO)
            for linha in projecao:
                escritor.writerow([
                    linha.mes,
                    formatar_numero(linha.aluguel),
                    formatar_numero(linha.parcela_taxa),
                    formatar_numero(linha.total_mes),
                    formatar_numero(linha.total_acumulado),
                ])
            total_aluguel = sum(l.aluguel for l in projecao)
            total_taxa = sum(l.parcela_taxa for l in projecao)
            escritor.writerow([
                "TOTAL",
                formatar_numero(total_aluguel),
                formatar_numero(total_taxa),
                formatar_numero(total_aluguel + total_taxa),
                "",
            ])
        return caminho
