"""Testes automáticos das regras comerciais. Execute com:  python -m unittest -v"""

import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from rentsmart import Apartamento, Casa, Cliente, Estudio, ExportadorCSV, Orcamento, TaxaContratual

D = Decimal


class TestApartamento(unittest.TestCase):
    def test_base_com_criancas(self):
        self.assertEqual(Apartamento(1, False, True).calcular_aluguel_mensal(), D("700.00"))

    def test_desconto_sem_criancas_sobre_base(self):
        self.assertEqual(Apartamento(1, False, False).calcular_aluguel_mensal(), D("665.00"))

    def test_dois_quartos_garagem_sem_criancas(self):
        # (700 + 200 + 300) = 1200 ; 5% = 60 ; 1200 - 60 = 1140
        self.assertEqual(Apartamento(2, True, False).calcular_aluguel_mensal(), D("1140.00"))

    def test_dois_quartos_garagem_com_criancas(self):
        self.assertEqual(Apartamento(2, True, True).calcular_aluguel_mensal(), D("1200.00"))

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Apartamento(3, False, True)


class TestCasa(unittest.TestCase):
    def test_base(self):
        self.assertEqual(Casa(1, False).calcular_aluguel_mensal(), D("900.00"))

    def test_dois_quartos_garagem(self):
        self.assertEqual(Casa(2, True).calcular_aluguel_mensal(), D("1450.00"))

    def test_casa_nao_tem_desconto(self):
        nomes = [i.descricao for i in Casa(2, True).composicao_aluguel()]
        self.assertFalse(any("Desconto" in n for n in nomes))


class TestEstudio(unittest.TestCase):
    def test_sem_estacionamento(self):
        self.assertEqual(Estudio(False).calcular_aluguel_mensal(), D("1200.00"))

    def test_pacote_duas_vagas(self):
        self.assertEqual(Estudio(True).calcular_aluguel_mensal(), D("1450.00"))

    def test_vagas_adicionais(self):
        # 1200 + 250 + 3 x 60 = 1630
        self.assertEqual(Estudio(True, 3).calcular_aluguel_mensal(), D("1630.00"))
        self.assertEqual(Estudio(True, 3).total_vagas, 5)

    def test_adicional_sem_pacote_invalido(self):
        with self.assertRaises(ValueError):
            Estudio(False, 2)


class TestTaxaContratual(unittest.TestCase):
    def test_parcelas_somam_2000(self):
        for n in range(1, 6):
            self.assertEqual(sum(TaxaContratual(n).valores_das_parcelas()), D("2000.00"))

    def test_tres_parcelas_ajuste_de_centavos(self):
        self.assertEqual(TaxaContratual(3).valores_das_parcelas(), [D("666.67"), D("666.67"), D("666.66")])

    def test_limite_de_parcelas(self):
        for invalido in (0, 6):
            with self.assertRaises(ValueError):
                TaxaContratual(invalido)

    def test_parcela_fora_do_prazo_e_zero(self):
        self.assertEqual(TaxaContratual(4).parcela_do_mes(5), D("0.00"))


class TestOrcamentoECSV(unittest.TestCase):
    def setUp(self):
        self.orcamento = Orcamento(Cliente("Ana Souza"), Apartamento(2, True, False), TaxaContratual(4))

    def test_projecao_12_meses(self):
        projecao = self.orcamento.gerar_projecao()
        self.assertEqual(len(projecao), 12)
        self.assertEqual(projecao[0].total_mes, D("1640.00"))   # 1140 + 500
        self.assertEqual(projecao[4].total_mes, D("1140.00"))   # mês 5: sem taxa
        self.assertEqual(self.orcamento.total_primeiro_ano(), D("15680.00"))  # 12 x 1140 + 2000

    def test_csv_gerado(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = ExportadorCSV(pasta).exportar(self.orcamento)
            with open(caminho, encoding="utf-8-sig") as f:
                linhas = list(csv.reader(f, delimiter=";"))
            self.assertTrue(Path(caminho).exists())
            self.assertEqual(len(linhas), 14)  # cabeçalho + 12 meses + total
            self.assertEqual(linhas[1], ["1", "1140,00", "500,00", "1640,00", "1640,00"])
            self.assertEqual(linhas[-1][0], "TOTAL")


if __name__ == "__main__":
    unittest.main()
