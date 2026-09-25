# Transpilador Star Wars

Transpilador de uma linguagem de programação temática, com palavras-chave tiradas de falas
de Star Wars, para C99. A linguagem tem dois tipos numéricos, variáveis, aritmética,
comparações, condicionais, repetição (`while` e `for`), funções e entrada/saída.
O transpilador percorre as etapas:

**fonte → léxico → tokens → parser → AST → análise semântica → código C**

## Pré-requisitos

- Python 3.8 ou superior, sem bibliotecas externas.
- GCC com suporte a C99, para compilar os programas gerados e executar os testes.
- Arquivos fonte em UTF-8, com extensão `.starwars`.

Os comandos abaixo são para Linux e partem da raiz do projeto.

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
./sw vscode                    # instala a extensão do VS Code
./sw                           # ajuda
```

Sem o redirecionamento `<`, os valores de entrada são digitados no terminal. O compilador
C padrão é `gcc`; outro pode ser escolhido com a variável `CC` (`CC=clang ./sw run ...`).

## Executar passo a passo

Os comandos abaixo mostram as etapas que o `./sw run` executa:

```bash
mkdir -p build
PYTHONPATH=src python3 -m starwars examples/valid/02_complete.starwars -o build/02_complete.c
gcc -std=c99 -Wall -Wextra build/02_complete.c -o build/02_complete
./build/02_complete < examples/valid/02_complete.input.txt
```

O transpilador gera C; a execução do programa é uma etapa posterior, feita com GCC.

- Sem `-o`, o código C é impresso na saída padrão.
- Sem o arquivo de entrada, o transpilador procura exatamente um `.starwars` na pasta
  atual; se houver zero ou vários, é preciso informar o caminho.
- A pasta de saída precisa existir.
- Em caso de erro, o código de saída é 1 e o arquivo C não é criado nem sobrescrito.

## A linguagem

```text
Há muito tempo, em uma galáxia muito, muito distante
energia: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe a energia: " -> energia);
energia Eu alterei o acordo energia Que a força esteja com você 3 Eu sou todos os jedi 4;
Hello There ("Energia final: ", energia);
Chewie, estamos em casa
```

| Construção | Sintaxe |
| --- | --- |
| Início e fim do programa | `Há muito tempo, em uma galáxia muito, muito distante` ... `Chewie, estamos em casa` (ou `INICIA_SISTEMA` ... `LOGOUT`) |
| Tipos | `Você era o escolhido` (`int`) e `Eu sou C3PO, ciborgue de relações humanas` (`float`) |
| Declaração | `nome: Tipo;` ou `nome: Tipo Eu alterei o acordo valor;` (também `Tipo nome ...;`) |
| Decisão | `Faça, ou não faça (condição)` ... `Tentativa não há` ... `Chewie, estamos em casa` |
| Repetição por condição | `Eu sinto uma perturbação na força (condição)` ... `Chewie, estamos em casa` |
| Repetição por intervalo | `This is the way (i de 1 até n)` ... `Chewie, estamos em casa` |
| Função | `Execute a ordem 66 nome(a: Tipo, ...): Tipo` ... `Chewie, estamos em casa` |
| Retorno | `Palpatine retornou valor;` |
| Leitura | `Ajude-me Obi-Wan Kenobi (variável);` ou `Ajude-me Obi-Wan Kenobi ("mensagem" -> variável);` |
| Escrita | `Hello There (item, item, ...);` |
| Comentário | `#` até o fim da linha |

Cada operador tem uma frase temática, usada nos exemplos, e um símbolo equivalente:

| Frase | Símbolo |
| --- | --- |
| `Eu alterei o acordo` | `=` |
| `Que a força esteja com você` / `Acabou anakin` | `+` / `-` |
| `Eu sou todos os jedi` / `Eu sou todos os sith` | `*` / `/` |
| `Como deve ser` / `Estes não são os droides que você procura` | `==` / `!=` |
| `I have the high ground` / `A força é forte nele` | `>` / `>=` |
| `Você subestima meu poder` / `Não, eu sou seu pai` | `<` / `<=` |

Regras principais:

- `Chewie, estamos em casa` fecha o programa e cada bloco. No condicional, um único fim
  fecha a decisão inteira, inclusive a alternativa.
- As funções são definidas logo após o início do programa. Sem `: Tipo`, a função é um
  procedimento, chamado como comando (`nome(argumentos);`).
- No `for`, o intervalo é inclusivo e a variável de controle é criada pelo laço, é inteira
  e não pode ser alterada no corpo.
- Não há sinal negativo: escreva `0 Acabou anakin valor`. A entrada de dados aceita
  valores negativos.
- Textos usam aspas duplas e aceitam `\n`, `\r`, `\t`, `\"` e `\\`. Só aparecem na saída
  e na mensagem de leitura.
- Na saída, os itens são concatenados sem separador. Se houver alguma expressão numérica,
  uma quebra de linha é adicionada ao final; saída só com textos imprime exatamente o texto.

A referência completa da linguagem, com regras de tipos, escopo e mensagens de erro, está
em [`.claude/skills/writing-starwars/`](.claude/skills/writing-starwars/).

## Extensão do VS Code

```bash
./sw vscode
```

Instala a extensão de `editors/vscode/` para arquivos `.starwars`:

- **Cores:** cada tipo de elemento tem uma cor (início e fim de blocos, controle de fluxo,
  tipos, funções, entrada e saída, operadores, variáveis, números, textos e comentários),
  aplicada sobre o tema atual, com variações para temas escuros e claros. Uma frase
  reservada digitada errada, com espaço duplo ou sem acento, perde a cor de palavra
  reservada.
- **Explicação ao passar o mouse:** sobre uma frase, mostra o que ela faz, o símbolo
  equivalente, um exemplo, o código C correspondente e a origem da fala; sobre um símbolo
  (`=`, `==`, `->`...), a frase equivalente; sobre uma variável, o tipo e a linha da
  declaração; sobre uma função, a assinatura.
- **Autocompletar:** sugere as frases enquanto você digita, mesmo sem acento (`Faca`) ou
  por palavras como `if`, `while`, `print` e `int`.
- **Modelos de estruturas:** `se`, `senao`, `enquanto`, `para`, `funcao`, `procedimento`,
  `int`, `real`, `ler`, `escrever` e `programa` (ou `if`, `while`, `for`, `func`, `input`,
  `print`) inserem a estrutura completa, com o fim de bloco no lugar certo.

Depois de instalar, recarregue a janela (`Ctrl+Shift+P` > `Developer: Reload Window`).
Para só gerar o pacote, sem instalar: `./sw vscode starwars.vsix`.

## Exemplos e testes

```bash
./sw test          # ou: PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

A suíte tem um arquivo por fase do transpilador (`test_lexer.py`, `test_parser.py`,
`test_semantic.py`, `test_codegen.py`, ...), além de:

- `test_examples.py`: confere que os arquivos em `examples/generated/` correspondem às
  fontes atuais e compila e executa cada exemplo válido;
- `test_cli.py`: argumentos e erros da interface de linha de comando;
- `test_script.py`: comandos do `./sw`.

| Arquivo | Objetivo |
| --- | --- |
| `examples/valid/01_basic.starwars` | Declaração, atribuição e saída |
| `examples/valid/02_complete.starwars` | Dois tipos, entrada, saída, if/else, while, precedência e parênteses |
| `examples/invalid/01_lexical_error.starwars` | Caractere inválido |
| `examples/invalid/02_syntax_error.starwars` | Expressão ausente na declaração |
| `examples/invalid/03_semantic_error.starwars` | Variável não declarada |
| `examples/invalid/04_redeclaration_error.starwars` | Declaração duplicada no mesmo escopo |
| `examples/invalid/05_type_error.starwars` | Real atribuído a inteiro na declaração |
| `examples/invalid/06_scope_error.starwars` | Uso de variável fora do bloco |
| `examples/valid/09_for.starwars` | Laço por intervalo (`This is the way`) |
| `examples/invalid/07_loop_variable_error.starwars` | Alteração da variável de controle do laço |
| `examples/valid/11_functions.starwars` | Funções com retorno, recursão e procedimento |
| `examples/invalid/08_argument_error.starwars` | Chamada com quantidade errada de argumentos |
| `examples/valid/13_galaxy.starwars` | Programa completo: avaliação de tiro ao alvo com funções, recursão (MDC), `for`, validação com `while`, `if` aninhado, leitura e escrita |

Cada exemplo válido tem um `.expected.txt` com a saída exata do programa. Os que leem
dados também têm um `.input.txt`, usado como entrada pelos testes e pelo `./sw demo`.

Para ver uma mensagem de erro produzida pelo próprio transpilador:

```bash
./sw check examples/invalid/01_lexical_error.starwars
./sw check examples/invalid/02_syntax_error.starwars
./sw check examples/invalid/03_semantic_error.starwars
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

- `src/starwars/`: pacote do transpilador, um módulo por fase (`lexer`, `parser`,
  `semantic`, `codegen`, `cli`, entre outros).
- `tests/`: suíte automatizada, um arquivo por módulo ou fase.
- `examples/`: `valid/` e `invalid/` com os programas de exemplo e `generated/` com o C
  gerado a partir dos válidos.
- `sw`: script com os comandos de uso rápido.
- `editors/vscode/`: extensão do VS Code (cores, explicações, autocompletar e modelos).
- `.claude/skills/writing-starwars/`: referência da linguagem para escrever programas.

## Autoria

Christian Gabriel Candeloni, Christian Mathias Michelson e Leonardo Daniel Becker.

Trabalho Prático 1 de Linguagens Formais e Compiladores (Unijuí). O desenvolvimento teve
apoio das ferramentas de IA Claude Code e OpenAI Codex, conforme declarado no relatório.
