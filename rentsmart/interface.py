"""Interface de terminal: conversa com o atendente, valida as respostas e monta os objetos."""

from .contrato import TaxaContratual
from .exportador import ExportadorCSV
from .imoveis import Apartamento, Casa, Estudio, Imovel
from .orcamento import Cliente, Orcamento


class Entrada:
    """Leitura de dados do teclado com validação. Repete a pergunta até a resposta ser válida."""

    @staticmethod
    def texto(pergunta: str) -> str:
        while True:
            resposta = input(pergunta).strip()
            if resposta:
                return resposta
            print("  ⚠ Este campo é obrigatório.")

    @staticmethod
    def inteiro(pergunta: str, minimo: int, maximo: int) -> int:
        while True:
            resposta = input(pergunta).strip()
            if resposta.isdigit() and minimo <= int(resposta) <= maximo:
                return int(resposta)
            print(f"  ⚠ Digite um número inteiro entre {minimo} e {maximo}.")

    @staticmethod
    def sim_ou_nao(pergunta: str) -> bool:
        while True:
            resposta = input(f"{pergunta} (s/n): ").strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("  ⚠ Responda com 's' para sim ou 'n' para não.")


class AtendimentoConsole:
    """Conduz o atendimento: coleta dados, cria o orçamento, exibe e exporta."""

    MAX_VAGAS_ADICIONAIS = 10

    def __init__(self, exportador: ExportadorCSV | None = None):
        self.exportador = exportador or ExportadorCSV()
        # Cada opção do menu aponta para o método que coleta os dados daquele tipo de imóvel.
        self.opcoes_imovel = {
            1: ("Apartamento (a partir de R$ 700,00)", self._coletar_apartamento),
            2: ("Casa (a partir de R$ 900,00)", self._coletar_casa),
            3: ("Estúdio (a partir de R$ 1.200,00)", self._coletar_estudio),
        }

    # ---------- coleta por tipo de imóvel ----------
    def _coletar_apartamento(self) -> Imovel:
        quartos = Entrada.inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = Entrada.sim_ou_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        criancas = Entrada.sim_ou_nao("O cliente possui crianças?")
        return Apartamento(quartos, garagem, criancas)

    def _coletar_casa(self) -> Imovel:
        quartos = Entrada.inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = Entrada.sim_ou_nao("Deseja vaga de garagem (+ R$ 300,00)?")
        return Casa(quartos, garagem)

    def _coletar_estudio(self) -> Imovel:
        pacote = Entrada.sim_ou_nao("Deseja o pacote de estacionamento com 2 vagas (+ R$ 250,00)?")
        adicionais = 0
        if pacote:
            adicionais = Entrada.inteiro(
                f"Vagas adicionais além das 2 do pacote (R$ 60,00 cada, 0 a {self.MAX_VAGAS_ADICIONAIS}): ",
                0, self.MAX_VAGAS_ADICIONAIS,
            )
        return Estudio(pacote, adicionais)

    # ---------- fluxo principal ----------
    def _escolher_imovel(self) -> Imovel:
        print("\nTipos de imóvel:")
        for numero, (texto, _) in self.opcoes_imovel.items():
            print(f"  {numero} - {texto}")
        opcao = Entrada.inteiro("Escolha o tipo de imóvel: ", 1, len(self.opcoes_imovel))
        _, coletar = self.opcoes_imovel[opcao]
        return coletar()

    def _escolher_parcelas(self) -> TaxaContratual:
        print(f"\nTaxa contratual: R$ 2.000,00 (pode ser parcelada em até {TaxaContratual.MAXIMO_PARCELAS}x).")
        parcelas = Entrada.inteiro(f"Em quantas parcelas (1 a {TaxaContratual.MAXIMO_PARCELAS})? ",
                                   1, TaxaContratual.MAXIMO_PARCELAS)
        return TaxaContratual(parcelas)

    def novo_orcamento(self) -> Orcamento:
        cliente = Cliente(Entrada.texto("\nNome do cliente: "))
        imovel = self._escolher_imovel()
        taxa = self._escolher_parcelas()
        return Orcamento(cliente, imovel, taxa)

    def executar(self) -> None:
        print("=" * 58)
        print("   Bem-vindo(a) ao RentSmart – Orçamentos R.M Imóveis")
        print("=" * 58)
        while True:
            orcamento = self.novo_orcamento()
            print("\n" + orcamento.resumo())
            caminho = self.exportador.exportar(orcamento)
            print(f"\n✔ Projeção de 12 meses salva em: {caminho}")
            if not Entrada.sim_ou_nao("\nDeseja fazer outro orçamento?"):
                print("\nObrigado por usar o RentSmart!")
                break
