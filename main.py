"""Ponto de entrada do RentSmart. Execute com:  python main.py"""

from rentsmart.interface import AtendimentoConsole


def main() -> None:
    try:
        AtendimentoConsole().executar()
    except (KeyboardInterrupt, EOFError):
        print("\n\nAtendimento encerrado pelo usuário.")


if __name__ == "__main__":
    main()
