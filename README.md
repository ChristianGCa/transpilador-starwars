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
python3 transpilador_hacker.py testes/02_valido_completo.starwars -o gerados/02_valido_completo.c
gcc -std=c99 -Wall -Wextra gerados/02_valido_completo.c -o gerados/completo.bin
./gerados/completo.bin < testes/02_valido_completo.entrada.txt
```

A entrada de demonstração contém `3` e `1.5`. A saída esperada está em
[`testes/02_valido_completo.esperado.txt`](testes/02_valido_completo.esperado.txt).
Para digitar os valores interativamente, execute `./gerados/completo.bin` sem o redirecionamento.

O transpilador gera C; a execução do programa é uma etapa posterior, feita com GCC.
Sem `-o`, o código C é impresso na saída padrão. Sem o argumento do arquivo,
o transpilador procura exatamente um `.starwars` na pasta atual, preservando o uso
original de `python3 transpilador_hacker.py` com `teste.starwars`.
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
python3 -B -m unittest discover -s testes -v
```

A suíte testa o lexer, a AST, erros semânticos, escopos, entrada/saída, argumentos
da interface e a compilação/execução real dos programas C em uma pasta temporária.
Ela também confere que os arquivos em `gerados/` correspondem às fontes atuais.

| Arquivo | Objetivo |
| --- | --- |
| `testes/01_valido_basico.starwars` | Declaração, atribuição e saída |
| `testes/02_valido_completo.starwars` | Dois tipos, entrada, saída, if/else, while, precedência e parênteses |
| `testes/03_erro_lexico.starwars` | Caractere inválido |
| `testes/04_erro_sintatico.starwars` | Expressão ausente na declaração |
| `testes/05_erro_semantico.starwars` | Variável não declarada |
| `testes/06_erro_redeclaracao.starwars` | Declaração duplicada no mesmo escopo |
| `testes/07_erro_tipo.starwars` | Real atribuído a inteiro na declaração |
| `testes/08_erro_escopo.starwars` | Uso de variável fora do bloco |

Para demonstrar uma mensagem de erro produzida pelo próprio transpilador:

```bash
python3 transpilador_hacker.py testes/03_erro_lexico.starwars
python3 transpilador_hacker.py testes/04_erro_sintatico.starwars
python3 transpilador_hacker.py testes/05_erro_semantico.starwars
```

## Inspecionar as etapas

```bash
python3 transpilador_hacker.py testes/01_valido_basico.starwars --tokens --ast -o gerados/01_valido_basico.c
```

`--tokens` mostra categoria, lexema e linha. `--ast` mostra a árvore em JSON,
anotada pela análise semântica com tipos e nomes de destino. Essas informações vão
para a saída de diagnóstico (`stderr`), separadas do código C.

## Organização

- `transpilador_hacker.py`: implementação, mantido o nome original do arquivo.
- `RELATORIO.md`: especificação formal e explicação da implementação.
- `testes/`: fontes válidas/inválidas, entrada, saídas esperadas e suíte automatizada.
- `gerados/`: C dos dois exemplos obrigatórios e do exemplo original.
- `teste.starwars`: exemplo original preservado.
- `ROTEIRO_APRESENTACAO.md`: sequência de demonstração e tópicos para a defesa técnica.
- O arquivo com `Trabalho_Pratico_1_Linguagem_Tematica_v6` no nome é o enunciado.

## Autoria e apresentação

A revisão e complementação tiveram apoio do OpenAI Codex, conforme declarado no
relatório. Antes da entrega, o grupo deve identificar seus integrantes no relatório,
revisar e compreender as decisões implementadas e preparar a apresentação conjunta.
