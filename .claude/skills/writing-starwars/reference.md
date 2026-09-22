# Referência da linguagem `.starwars`

## Estrutura e léxico

- Arquivo UTF-8 com extensão `.starwars`: `INICIA_SISTEMA` ... `LOGOUT`. Depois do
  `LOGOUT` final, só espaços e comentários.
- `#` comenta até o fim da linha. Não há comentário de bloco.
- Espaços e quebras de linha são livres e a indentação não tem significado (use 4 espaços).
- Identificadores: começam com letra ou `_`, seguem com letras, dígitos ou `_`. Acentos
  latinos são aceitos (`nível`), e maiúsculas e minúsculas são diferentes.
- Frase reservada digitada errada (espaço duplo, minúscula, sem acento) vira
  identificador e gera erro sintático.

## Declarações

```starwars
INICIA_SISTEMA
energia: Você era o escolhido = 10;
nivel: Eu sou C3PO, ciborgue de relações humanas = 1.5;
Você era o escolhido vidas = 3;
LOGOUT
```

- A forma `Tipo nome [= expr];` também vale, mas prefira `nome: Tipo [= expr];`.
- Podem aparecer em qualquer ponto de um bloco. Não pode haver nome repetido no mesmo bloco.
- O nome só passa a existir depois do inicializador. Por isso `x: Você era o escolhido = x;`
  só funciona se houver um `x` em um bloco externo.

## Números e expressões

- Inteiro: `0` a `2147483647`. Real: `1.5`, `10.0`. Não há `1e3`, `.5`, `5.` nem sinal.
- Negativos: `0 - 5`, `0 - x`, `0 - (a + b)`. A leitura pelo teclado aceita negativos.
- `*` e `/` antes de `+` e `-`; no mesmo nível, da esquerda para a direita
  (`10 - 3 - 2` = `5`). Parênteses agrupam.
- Se houver um operando real, o resultado é real; senão, inteiro. `7 / 2` = `3`, `7 / 2.0` = `3.5`.
- `int` pode ser atribuído a real; o contrário é erro.

## Saída: `Hello There (item, item, ...);`

- Pelo menos um item. Cada item é um texto ou uma expressão numérica.
- Os itens saem colados. Coloque os espaços dentro dos textos.
- Se houver alguma expressão, uma quebra de linha é adicionada ao final. Se só houver
  textos, nada é adicionado.
- Reais usam `%g`: `3.0` → `3`, `2.5` → `2.5`, `1234567.0` → `1.23457e+06`.

## Textos

- Somente aspas duplas, em uma única linha. Escapes permitidos: `\n \r \t \" \\`.
  Qualquer outro é erro. Acentos podem ser escritos diretamente.
- Não são valores: não podem ser comparados, atribuídos ou somados.

## Entrada: `Ajude-me Obi-Wan Kenobi`

- `(x);` ou `("Mensagem: " -> x);`. Recebe uma variável já declarada, nunca uma expressão.
- Para ler duas variáveis, use dois comandos. O tipo da variável define o que é lido.
- Entrada não numérica encerra o programa com `ERRO DE ENTRADA`.

## Condições, `if` e `while`

- `(expr OP expr)` com um único operador. `((a > b))` e `1 < x < 10` são erros; `((a + b) * 2 > c)` é válido.
- Pode misturar `int` e real. Uma comparação não pode ser atribuída nem impressa.
- `Faça, ou não faça (c)` bloco `[Tentativa não há` bloco`]` `LOGOUT`.
- `Eu sinto uma perturbação na força (c)` bloco `LOGOUT`.
- Blocos podem ser vazios. Cada corpo (`if`, senão, laço) tem escopo próprio: enxerga e
  altera as variáveis de fora, mas o que é declarado dentro some no `LOGOUT` e não
  aparece no outro ramo. Para usar um resultado depois do bloco, declare fora e atribua dentro.
- Dentro de um laço, uma declaração reinicia o valor a cada volta.
- Um bloco interno pode reusar um nome externo (esconde o de fora). Evite.

## Receitas para o que não existe

| Quero | Escreva |
| --- | --- |
| `a % b` | `a - (a / b) * b` (inteiros) |
| `a && b` | um `if` dentro de outro |
| `a \|\| b` | `ok = 0`; um `if` por condição fazendo `ok = 1;`; depois `(ok == 1)` |
| `else if` | um `if` dentro do senão; cada `if` com seu `LOGOUT` |
| `for` | contador declarado antes, `while (i < n)` e `i = i + 1;` no fim do corpo |
| booleano | `int` com `0`/`1` |
| real → `int`, texto em variável, funções, vetores, `break` | não existem; reestruture |

```starwars
INICIA_SISTEMA
nota: Você era o escolhido = 5;
Faça, ou não faça (nota >= 9)
    Hello There ("A\n");
Tentativa não há
    Faça, ou não faça (nota >= 6)
        Hello There ("B\n");
    Tentativa não há
        Hello There ("C\n");
    LOGOUT
LOGOUT
LOGOUT
```
