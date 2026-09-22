# Referência da linguagem `.starwars`

Nesta página, "fim" é a frase `Chewie, estamos em casa`.

## Estrutura e léxico

- Arquivo UTF-8 com extensão `.starwars`: `Há muito tempo, em uma galáxia muito, muito distante`
  ... `Chewie, estamos em casa`. Depois do fim do programa, só espaços e comentários.
- `#` comenta até o fim da linha. Não há comentário de bloco.
- Espaços e quebras de linha são livres e a indentação não tem significado (use 4 espaços).
  Uma expressão longa pode continuar na linha seguinte.
- Identificadores: começam com letra ou `_`, seguem com letras, dígitos ou `_`. Acentos
  latinos são aceitos (`nível`), e maiúsculas e minúsculas são diferentes.
- Frase reservada digitada errada (espaço duplo, minúscula, sem acento, sem vírgula)
  vira identificador e gera erro sintático.
- Os símbolos (`= + - * / == != > >= < <=`, `INICIA_SISTEMA`, `LOGOUT`) funcionam, mas
  o projeto escreve com as frases.

## Declarações

```starwars
Há muito tempo, em uma galáxia muito, muito distante
energia: Você era o escolhido Eu alterei o acordo 10;
nivel: Eu sou C3PO, ciborgue de relações humanas Eu alterei o acordo 1.5;
Você era o escolhido vidas Eu alterei o acordo 3;
Chewie, estamos em casa
```

- A forma `Tipo nome [Eu alterei o acordo expr];` também vale, mas prefira `nome: Tipo ...`.
- Podem aparecer em qualquer ponto de um bloco. Não pode haver nome repetido no mesmo bloco.
- O nome só passa a existir depois do inicializador. Por isso
  `x: Você era o escolhido Eu alterei o acordo x;` só funciona se houver um `x` em um bloco externo.

## Números e expressões

- Inteiro: `0` a `2147483647`. Real: `1.5`, `10.0`. Não há `1e3`, `.5`, `5.` nem sinal.
- Negativos: `0 Acabou anakin 5`, `0 Acabou anakin (a Que a força esteja com você b)`.
  A leitura pelo teclado aceita negativos.
- Multiplicar e dividir vêm antes de somar e subtrair; no mesmo nível, da esquerda para
  a direita (`10 Acabou anakin 3 Acabou anakin 2` = `5`). Parênteses agrupam.
- Se houver um operando real, o resultado é real; senão, inteiro.
  `7 Eu sou todos os sith 2` = `3`; `7 Eu sou todos os sith 2.0` = `3.5`.
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

- `(expr OP expr)` com um único operador. `((a I have the high ground b))` e
  `1 Você subestima meu poder x Você subestima meu poder 10` são erros;
  `((a Que a força esteja com você b) Eu sou todos os jedi 2 I have the high ground c)` é válido.
- Pode misturar `int` e real. Uma comparação não pode ser atribuída nem impressa.
- `Faça, ou não faça (c)` bloco `[Tentativa não há` bloco`]` fim.
- `Eu sinto uma perturbação na força (c)` bloco fim.
- Blocos podem ser vazios. Cada corpo (`if`, senão, laço) tem escopo próprio: enxerga e
  altera as variáveis de fora, mas o que é declarado dentro some no fim do bloco e não
  aparece no outro ramo. Para usar um resultado depois do bloco, declare fora e atribua dentro.
- Dentro de um laço, uma declaração reinicia o valor a cada volta.
- Um bloco interno pode reusar um nome externo (esconde o de fora). Evite.

## Receitas para o que não existe

| Quero | Escreva |
| --- | --- |
| resto de `a` por `b` | `a Acabou anakin (a Eu sou todos os sith b) Eu sou todos os jedi b` (inteiros) |
| `a && b` | um `if` dentro de outro |
| `a \|\| b` | `ok` com `0`; um `if` por condição fazendo `ok Eu alterei o acordo 1;`; depois `(ok Como deve ser 1)` |
| `else if` | um `if` dentro do senão; cada `if` com seu próprio fim |
| `for` | contador declarado antes, laço com `(i Você subestima meu poder n)` e `i Eu alterei o acordo i Que a força esteja com você 1;` no fim do corpo |
| booleano | `int` com `0`/`1` |
| real → `int`, texto em variável, funções, vetores, `break` | não existem; reestruture |

```starwars
Há muito tempo, em uma galáxia muito, muito distante
nota: Você era o escolhido Eu alterei o acordo 5;
Faça, ou não faça (nota A força é forte nele 9)
    Hello There ("A\n");
Tentativa não há
    Faça, ou não faça (nota A força é forte nele 6)
        Hello There ("B\n");
    Tentativa não há
        Hello There ("C\n");
    Chewie, estamos em casa
Chewie, estamos em casa
Chewie, estamos em casa
```
