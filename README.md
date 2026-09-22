# Transpilador Star Wars

Linguagem temática com dois tipos numéricos, variáveis, aritmética, comparações,
condicionais, repetição e entrada/saída. O transpilador percorre as etapas:

**fonte → tokens → parser → AST → análise semântica → código C**

## Pré-requisitos

- Python 3.8 ou superior, sem bibliotecas externas.
- GCC com suporte a C99 para compilar os programas gerados e executar os testes.
- Arquivos fonte em UTF-8. Os comandos abaixo são para Linux, executados nesta pasta.

## Uso rápido: `./sw`

O script `./sw` reúne as etapas em comandos curtos e pode ser chamado de qualquer pasta.
Os arquivos gerados ficam em `build/`.

```bash
./sw run examples/valid/02_complete.starwars      # transpila, compila e executa
./sw run examples/valid/02_complete.starwars < examples/valid/02_complete.input.txt
./sw build arquivo.starwars    # gera build/arquivo.c e build/arquivo sem executar
./sw c arquivo.starwars        # mostra o C gerado (aceita --tokens e --ast)
./sw check arquivo.starwars    # só verifica erros léxicos, sintáticos e semânticos
./sw test                      # roda a suíte de testes
./sw regen                     # regenera examples/generated a partir das fontes
./sw demo                      # executa os exemplos válidos e mostra cada tipo de erro
./sw clean                     # apaga build/
./sw                           # ajuda
```

A entrada de demonstração contém `3` e `1.5`. A saída esperada está em
[`examples/valid/02_complete.expected.txt`](examples/valid/02_complete.expected.txt).
Sem o redirecionamento `<`, os valores são digitados no terminal. O compilador C
padrão é `gcc`; outro pode ser escolhido com a variável `CC`.

## Executar passo a passo

Os comandos abaixo mostram as etapas que o `./sw run` executa:

```bash
mkdir -p build
python3 -m starwars examples/valid/02_complete.starwars -o build/02_complete.c
gcc -std=c99 -Wall -Wextra build/02_complete.c -o build/02_complete
./build/02_complete < examples/valid/02_complete.input.txt
```

O transpilador gera C; a execução do programa é uma etapa posterior, feita com GCC.
Sem `-o`, o código C é impresso na saída padrão. Sem o argumento do arquivo,
o transpilador procura exatamente um `.starwars` na pasta atual.
Se houver zero ou vários arquivos, é necessário informar o caminho explicitamente.
A pasta de saída deve existir. Erros retornam código de saída 1 e não geram nem
sobrescrevem o arquivo C solicitado; um arquivo antigo, se existir, permanece antigo.

## Exemplo da linguagem

```text
Há muito tempo, em uma galáxia muito, muito distante
energia: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe a energia: " -> energia);
energia Eu alterei o acordo energia Que a força esteja com você 3 Eu sou todos os jedi 4;
Hello There ("Energia final: ", energia);
Chewie, estamos em casa
```

- `Você era o escolhido`: inteiro (`int`).
- `Eu sou C3PO, ciborgue de relações humanas`: real (`float`).
- `Há muito tempo, em uma galáxia muito, muito distante` ... `Chewie, estamos em casa`:
  início e fim do programa (ou `INICIA_SISTEMA` ... `LOGOUT`). A frase de fim também fecha blocos.
- `Faça, ou não faça (...) ... Tentativa não há ... Chewie, estamos em casa`: decisão.
- `Eu sinto uma perturbação na força (...) ... Chewie, estamos em casa`: repetição enquanto a condição for verdadeira.
- `Ajude-me Obi-Wan Kenobi (variavel);`: leitura sem mensagem.
- `Hello There (...)`: saída de um ou vários textos/expressões separados por vírgulas.
- `#`: comentário até o fim da linha.

Cada operador tem uma frase temática, usada nos exemplos, e um símbolo equivalente:

| Frase | Símbolo |
| --- | --- |
| `Eu alterei o acordo` | `=` |
| `Que a força esteja com você` / `Acabou anakin` | `+` / `-` |
| `Eu sou todos os jedi` / `Eu sou todos os sith` | `*` / `/` |
| `Como deve ser` / `Estes não são os droides que você procura` | `==` / `!=` |
| `I have the high ground` / `A força é forte nele` | `>` / `>=` |
| `Você subestima meu poder` / `Não, eu sou seu pai` | `<` / `<=` |

A declaração `tipo nome = valor;` também é aceita.
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
./sw test                                     # ou: python3 -B -m unittest discover -s tests -v
```

A suíte tem um arquivo por fase do transpilador (`tests/test_lexer.py`,
`tests/test_parser.py`, `tests/test_semantic.py`, `tests/test_codegen.py`, ...), além de
`tests/test_examples.py`, que confere que os arquivos em `examples/generated/`
correspondem às fontes atuais e compila/executa os programas C em uma pasta temporária,
`tests/test_cli.py`, para os argumentos da interface, e `tests/test_script.py`, para o `./sw`.

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
./sw check examples/invalid/03_lexical_error.starwars
./sw check examples/invalid/04_syntax_error.starwars
./sw check examples/invalid/05_semantic_error.starwars
```

`./sw demo` executa todos os exemplos válidos e mostra o erro de cada exemplo inválido.

## Inspecionar as etapas

```bash
./sw c examples/valid/01_basic.starwars --tokens --ast
```

`--tokens` mostra categoria, lexema, linha e coluna, e é impresso mesmo quando a análise
sintática falha. `--ast` mostra a árvore em JSON, anotada pela análise semântica com
tipos e nomes de destino. Essas informações vão para a saída de diagnóstico (`stderr`),
separadas do código C.

## Organização

- `sw`: script com os comandos de uso rápido.
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
