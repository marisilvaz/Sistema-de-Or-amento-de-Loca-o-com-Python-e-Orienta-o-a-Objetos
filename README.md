# RentSmart – Sistema de Orçamento de Locação

Aplicação em Python, orientada a objetos, que automatiza os orçamentos de locação da **R.M Imóveis**. O sistema recebe as características da locação, aplica as regras comerciais da imobiliária, exibe um orçamento detalhado e gera um arquivo **CSV com a projeção dos 12 primeiros meses**.

> Trabalho da disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming** – UniFECAF
> Aluna: **Mariana Evangelista da Silva**

---

## Funcionalidades

- Orçamento para **apartamento**, **casa** e **estúdio**
- Adicionais de quarto, vaga de garagem e estacionamento do estúdio
- Desconto de 5% para apartamento quando o cliente não possui crianças
- Taxa contratual de R$ 2.000,00 apresentada **separada do aluguel**, parcelável em até 5x
- Validação de todas as entradas (o sistema repete a pergunta até receber uma resposta válida)
- Resumo mostrando linha a linha como o valor final foi formado
- Exportação da projeção de 12 meses em CSV (abre direto no Excel / Google Planilhas)
- Testes automáticos das regras de negócio

## Regras comerciais implementadas

| Imóvel | Aluguel-base | Adicionais | Desconto |
|---|---|---|---|
| Apartamento | R$ 700,00 | 2 quartos: + R$ 200,00 · Garagem: + R$ 300,00 | 5% sem crianças (após os adicionais) |
| Casa | R$ 900,00 | 2 quartos: + R$ 250,00 · Garagem: + R$ 300,00 | — |
| Estúdio | R$ 1.200,00 | Pacote 2 vagas: + R$ 250,00 · Vaga extra: + R$ 60,00 cada | — |

**Taxa contratual:** R$ 2.000,00, em 1 a 5 parcelas, cobradas nos primeiros meses do contrato. Quando a divisão não é exata, a diferença de centavos fica na última parcela (ex.: 3x = R$ 666,67 + R$ 666,67 + R$ 666,66).

## Requisitos

- Python **3.10 ou superior** (usa apenas a biblioteca padrão, não precisa instalar pacotes)

Para conferir a versão instalada:

```bash
python --version
```

## Como executar

```bash
# 1. Baixe o projeto
git clone https://github.com/SEU-USUARIO/RentSmart.git
cd RentSmart

# 2. Execute
python main.py
```

> No Linux/macOS, se `python` não funcionar, use `python3`.

O programa pergunta o nome do cliente, o tipo de imóvel, as opções de cada tipo e o número de parcelas da taxa contratual. Ao final, mostra o orçamento e salva o CSV na pasta `saida/`.

## Exemplo de execução

```
==========================================================
        RentSmart – R.M Imóveis | ORÇAMENTO DE LOCAÇÃO
==========================================================
Cliente: Ana Souza
Imóvel:  Apartamento – 2 quartos, com vaga de garagem, cliente não possui crianças
----------------------------------------------------------
ALUGUEL MENSAL
  Aluguel-base (Apartamento)                   R$ 700,00
  Adicional por 2 quartos                      R$ 200,00
  Vaga de garagem                              R$ 300,00
  Desconto de 5% (sem crianças)               - R$ 60,00
----------------------------------------------------------
  VALOR MENSAL DO ALUGUEL                    R$ 1.140,00
----------------------------------------------------------
TAXA CONTRATUAL (cobrada à parte, não faz parte do aluguel)
  Valor total da taxa                        R$ 2.000,00
  Parcelamento escolhido: 4x de R$ 500,00
----------------------------------------------------------
  Total previsto nos primeiros 12 meses     R$ 15.680,00
==========================================================
```

Um exemplo do CSV gerado está em [`exemplos/projecao_12_meses_ana_souza.csv`](exemplos/projecao_12_meses_ana_souza.csv).

## Testes

```bash
python -m unittest -v
```

São 18 testes que conferem os cálculos de cada tipo de imóvel, o desconto, o parcelamento da taxa, a projeção e o CSV.

## Estrutura do projeto

```
RentSmart/
├── main.py                 # ponto de entrada
├── rentsmart/
│   ├── imoveis.py          # Imovel, ImovelResidencial, Apartamento, Casa, Estudio, ItemOrcamento
│   ├── contrato.py         # TaxaContratual
│   ├── orcamento.py        # Cliente, Orcamento, ParcelaProjecao
│   ├── exportador.py       # ExportadorCSV
│   ├── interface.py        # Entrada (validação) e AtendimentoConsole (fluxo)
│   └── utils.py            # arredondamento e formatação de moeda
├── tests/
│   └── test_regras.py      # testes automáticos
├── exemplos/               # CSV de exemplo
└── README.md
```

## Organização orientada a objetos

- **Herança:** `Apartamento` e `Casa` herdam de `ImovelResidencial` (quartos e garagem), que herda de `Imovel`; `Estudio` herda direto de `Imovel`.
- **Polimorfismo:** o `Orcamento` chama `calcular_aluguel_mensal()` sem saber qual é o tipo de imóvel; cada classe responde com suas próprias regras.
- **Encapsulamento:** valores das regras ficam em constantes de cada classe (ex.: `Casa.ADICIONAL_SEGUNDO_QUARTO`), e as validações ficam nos construtores.
- **Separação de responsabilidades:** regras de preço (`imoveis`, `contrato`), montagem do orçamento (`orcamento`), arquivo (`exportador`) e conversa com o usuário (`interface`) ficam em módulos diferentes.

## Links

- Vídeo pitch: _inserir link do YouTube_
