---
name: writing-starwars
description: Use when writing, editing, reviewing or debugging programs in the Star Wars themed language (.starwars files), when asked to create an example program for this transpiler, or when a .starwars file fails with ERRO LÉXICO, ERRO SINTÁTICO or ERRO SEMÂNTICO.
---

# Escrevendo programas `.starwars`

Linguagem mínima transpilada para C99: dois tipos numéricos, aritmética, `if/else`,
`while`, `for` por intervalo, leitura e escrita. **O que não está aqui ou em `reference.md` não existe.**
Não traga sintaxe de C ou Python.

## Frases reservadas: copie exatamente

Maiúsculas, acentos, vírgulas e espaços simples fazem parte da frase. **Escreva sempre
com as frases**, que são o padrão do projeto. Os símbolos da última coluna são aceitos,
mas só servem para ler código antigo.

| Função | Frase | Símbolo |
| --- | --- | --- |
| Início do programa | `Há muito tempo, em uma galáxia muito, muito distante` | `INICIA_SISTEMA` |
| Fim do programa **e** de cada bloco | `Chewie, estamos em casa` | `LOGOUT` |
| Tipo `int` / tipo `float` | `Você era o escolhido` / `Eu sou C3PO, ciborgue de relações humanas` | |
| Se / senão | `Faça, ou não faça` / `Tentativa não há` | |
| Enquanto | `Eu sinto uma perturbação na força` | |
| Para (intervalo) | `This is the way (i de início até fim)` | |
| Escrever / ler | `Hello There` / `Ajude-me Obi-Wan Kenobi` | |
| Atribuir | `Eu alterei o acordo` | `=` |
| Somar / subtrair | `Que a força esteja com você` / `Acabou anakin` | `+` / `-` |
| Multiplicar / dividir | `Eu sou todos os jedi` / `Eu sou todos os sith` | `*` / `/` |
| Igual / diferente | `Como deve ser` / `Estes não são os droides que você procura` | `==` / `!=` |
| Maior / maior ou igual | `I have the high ground` / `A força é forte nele` | `>` / `>=` |
| Menor / menor ou igual | `Você subestima meu poder` / `Não, eu sou seu pai` | `<` / `<=` |

## Exemplo que mostra quase tudo

```starwars
Há muito tempo, em uma galáxia muito, muito distante
# comentário até o fim da linha
n: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe n: " -> n);
soma: Você era o escolhido Eu alterei o acordo 0;
This is the way (i de 1 até n)
    soma Eu alterei o acordo soma Que a força esteja com você i;
Chewie, estamos em casa
Faça, ou não faça (soma I have the high ground 10)
    media: Eu sou C3PO, ciborgue de relações humanas Eu alterei o acordo soma Eu sou todos os sith (n Eu sou todos os jedi 1.0);
    Hello There ("Soma: ", soma, " / média: ", media);
Tentativa não há
    Hello There ("Soma pequena\n");
Chewie, estamos em casa
Chewie, estamos em casa
```

## Regras que mais causam erro

- Declaração: `nome: Tipo;` ou `nome: Tipo Eu alterei o acordo expressão;`. Sem valor, vale `0`.
  Declare antes de usar.
- Todo comando simples termina com `;`. `Chewie, estamos em casa` **nunca** leva `;`.
- Cada `if` e cada laço (`while` ou `for`) fecham com **um** `Chewie, estamos em casa`,
  e o programa tem o seu.
  No `if/senão`, o fim vem só depois do senão.
- Condição: `(a OP b)`, com exatamente um operador relacional. Não há `&&`, `||`, `!`,
  encadeamento, `else if`, `break`, resto nem booleanos.
- Separe as frases dos nomes com espaço: `x Eu alterei o acordo 1;`.
- Sem sinal unário: `0 Acabou anakin 1`, não `-1`. Reais: `0.5` e `5.0`, nunca `.5` ou `5.`.
- Divisão entre `int` trunca; use um operando real (`x Eu sou todos os sith 2.0`).
  Real **nunca** vai para `int`.
- Textos: aspas duplas, uma linha, só em `Hello There` ou na mensagem de leitura.
- `Hello There` junta os itens sem espaço e pula linha sozinho só se houver algum número.
- A leitura recebe uma variável: `(x)` ou `("mensagem" -> x)`. A seta `->` não tem frase.
- `for`: `This is the way (i de a até b)` conta de `a` até `b` **inclusive**, de 1 em 1.
  `a` e `b` são inteiros; `i` é criado pelo laço, só existe nele e **não pode ser alterado**.
  Para contar de trás para frente ou de 2 em 2, use `while`.
- `de` e `até` são reservadas: não use como nome de variável.
- Variável declarada dentro de um bloco some no fim desse bloco.
- Em `esperado ...`, os erros usam a forma curta (`'LOGOUT'`, `'='`): tradução em `errors.md`.

## Arquivos de apoio

- `reference.md`: detalhes de tipos, saída, escopo, laços e receitas para resto, `||` e `else if`.
- `errors.md`: mensagem de erro → causa → correção, e o checklist antes de entregar.

## Validar

Na raiz do projeto do transpilador:

```bash
./sw check programa.starwars           # só verifica; erro sai com linha e coluna
./sw run programa.starwars             # transpila, compila e executa
./sw run programa.starwars < entrada.txt
```

Sempre transpile antes de entregar. Sem acesso a comandos, use o checklist de `errors.md`.
