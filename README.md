# Transpilador Star Wars

Linguagem temática com dois tipos numéricos, variáveis, aritmética, comparações,
condicionais, repetição e entrada/saída. O transpilador percorre as etapas:

**fonte → tokens → parser → AST → análise semântica → código C**

## Pré-requisitos

- Python 3.8 ou superior, sem bibliotecas externas.
- GCC com suporte a C99 para compilar os programas gerados e executar os testes.
- Arquivos fonte em UTF-8. Os comandos abaixo são para Linux, executados nesta pasta.

## Executar um programa

```bash
python3 -m starwars examples/valid/02_complete.starwars -o examples/generated/02_complete.c
gcc -std=c99 -Wall -Wextra examples/generated/02_complete.c -o examples/generated/complete.bin
./examples/generated/complete.bin < examples/valid/02_complete.input.txt
```

A entrada de demonstração contém `3` e `1.5`. A saída esperada está em
[`examples/valid/02_complete.expected.txt`](examples/valid/02_complete.expected.txt).
Para digitar os valores interativamente, execute `./examples/generated/complete.bin` sem o redirecionamento.

O transpilador gera C; a execução do programa é uma etapa posterior, feita com GCC.
Sem `-o`, o código C é impresso na saída padrão. Sem o argumento do arquivo,
o transpilador procura exatamente um `.starwars` na pasta atual.
Se houver zero ou vários arquivos, é necessário informar o caminho explicitamente.
A pasta de saída deve existir. Erros retornam código de saída 1 e não geram nem
sobrescrevem o arquivo C solicitado; um arquivo antigo, se existir, permanece antigo.

## Exemplo da linguagem

```text
INICIA_SISTEMA
energia: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe a energia: " -> energia);
energia = energia + 3 * 4;
Hello There ("Energia final: ", energia);
LOGOUT
```

- `Você era o escolhido`: inteiro (`int`).
- `Eu sou C3PO, ciborgue de relações humanas`: real (`float`).
- `Faça, ou não faça (...) ... Tentativa não há ... LOGOUT`: decisão.
- `Eu sinto uma perturbação na força (...) ... LOGOUT`: repetição enquanto a condição for verdadeira.
- `Ajude-me Obi-Wan Kenobi (variavel);`: leitura sem mensagem.
- `Hello There (...)`: saída de um ou vários textos/expressões separados por vírgulas.
- `#`: comentário até o fim da linha.

Os operadores `+ - * / = == != > >= < <=` são aceitos. As frases temáticas
originais também continuam válidas, assim como a declaração `tipo nome = valor;`.
`-` representa subtração binária; para escrever um valor negativo em uma expressão,
use `0 - valor`. A entrada de dados aceita valores negativos.

Textos usam aspas duplas e aceitam `\n`, `\r`, `\t`, `\"` e `\\`.
Na saída com vários itens, eles são concatenados sem separador automático. Se houver
alguma expressão numérica, uma quebra de linha é adicionada ao final do comando;
saída composta apenas por textos imprime exatamente o conteúdo informado.

A especificação completa, as três decisões próprias de sintaxe, as regras de tipos
e a gramática estão no [`RELATORIO.md`](RELATORIO.md).

## Testar

```bash
python3 -B -m unittest discover -s tests -v
```

A suíte tem um arquivo por fase do transpilador (`tests/test_lexer.py`,
`tests/test_parser.py`, `tests/test_semantic.py`, `tests/test_codegen.py`, ...), além de
`tests/test_examples.py`, que confere que os arquivos em `examples/generated/`
correspondem às fontes atuais e compila/executa os programas C em uma pasta temporária,
e `tests/test_cli.py`, para os argumentos da interface.

| Arquivo | Objetivo |
| --- | --- |
| `examples/valid/01_basic.starwars` | Declaração, atribuição e saída |
| `examples/valid/02_complete.starwars` | Dois tipos, entrada, saída, if/else, while, precedência e parênteses |
| `examples/invalid/03_lexical_error.starwars` | Caractere inválido |
| `examples/invalid/04_syntax_error.starwars` | Expressão ausente na declaração |
| `examples/invalid/05_semantic_error.starwars` | Variável não declarada |
| `examples/invalid/06_redeclaration_error.starwars` | Declaração duplicada no mesmo escopo |
| `examples/invalid/07_type_error.starwars` | Real atribuído a inteiro na declaração |
| `examples/invalid/08_scope_error.starwars` | Uso de variável fora do bloco |

Para demonstrar uma mensagem de erro produzida pelo próprio transpilador:

```bash
python3 -m starwars examples/invalid/03_lexical_error.starwars
python3 -m starwars examples/invalid/04_syntax_error.starwars
python3 -m starwars examples/invalid/05_semantic_error.starwars
```

## Inspecionar as etapas

```bash
python3 -m starwars examples/valid/01_basic.starwars --tokens --ast -o examples/generated/01_basic.c
```

`--tokens` mostra categoria, lexema, linha e coluna, e é impresso mesmo quando a análise
sintática falha. `--ast` mostra a árvore em JSON, anotada pela análise semântica com
tipos e nomes de destino. Essas informações vão para a saída de diagnóstico (`stderr`),
separadas do código C.

## Organização

- `starwars/`: pacote do transpilador, um módulo por fase (`lexer`, `parser`, `semantic`,
  `codegen`, `cli`, entre outros).
- `RELATORIO.md`: especificação formal e explicação da implementação.
- `tests/`: suíte automatizada, um arquivo por módulo/fase.
- `examples/`: `valid/` e `invalid/` com fontes de exemplo, `generated/` com o C gerado
  e `demo.starwars` com o exemplo de demonstração.
- `docs/presentation.md`: sequência de demonstração e tópicos para a defesa técnica.
- `docs/assignment.md`: enunciado do trabalho.

## Autoria e apresentação

A revisão e complementação tiveram apoio do OpenAI Codex, conforme declarado no
relatório. Antes da entrega, o grupo deve identificar seus integrantes no relatório,
revisar e compreender as decisões implementadas e preparar a apresentação conjunta.
