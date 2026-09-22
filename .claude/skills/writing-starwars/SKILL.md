---
name: writing-starwars
description: Use when writing, editing, reviewing or debugging programs in the Star Wars themed language (.starwars files), when asked to create an example program for this transpiler, or when a .starwars file fails with ERRO LÉXICO, ERRO SINTÁTICO or ERRO SEMÂNTICO.
---

# Escrevendo programas `.starwars`

Linguagem mínima transpilada para C99 por `python3 -m starwars`: dois tipos numéricos,
aritmética, `if/else`, `while`, leitura e escrita. **O que não está aqui ou em
`reference.md` não existe.** Não traga sintaxe de C ou Python.

## Frases reservadas: copie exatamente

Maiúsculas, acentos, vírgulas e espaços simples fazem parte da frase. Prefira os símbolos.

| Função | Frase | Símbolo |
| --- | --- | --- |
| Início / fim | `INICIA_SISTEMA` / `LOGOUT` | |
| Tipo `int` | `Você era o escolhido` | |
| Tipo `float` | `Eu sou C3PO, ciborgue de relações humanas` | |
| Se / senão | `Faça, ou não faça` / `Tentativa não há` | |
| Enquanto | `Eu sinto uma perturbação na força` | |
| Escrever / ler | `Hello There` / `Ajude-me Obi-Wan Kenobi` | |
| Atribuir | `Eu alterei o acordo` | `=` |
| `+ - * /` | `Que a força esteja com você`, `Acabou anakin`, `Eu sou todos os jedi`, `Eu sou todos os sith` | `+ - * /` |
| `== > >= < <=` | `Como deve ser`, `I have the high ground`, `A força é forte nele`, `Você subestima meu poder`, `Não, eu sou seu pai` | `== > >= < <=` |
| Diferente | *(sem frase)* | `!=` |

## Exemplo que mostra quase tudo

```starwars
INICIA_SISTEMA
# comentário até o fim da linha
n: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe n: " -> n);
soma: Você era o escolhido = 0;
i: Você era o escolhido = 1;
Eu sinto uma perturbação na força (i <= n)
    soma = soma + i;
    i = i + 1;
LOGOUT
Faça, ou não faça (soma > 10)
    media: Eu sou C3PO, ciborgue de relações humanas = soma / (n * 1.0);
    Hello There ("Soma: ", soma, " / média: ", media);
Tentativa não há
    Hello There ("Soma pequena\n");
LOGOUT
LOGOUT
```

## Regras que mais causam erro

- Declaração: `nome: Tipo;` ou `nome: Tipo = expressão;`. Sem valor, vale `0`. Declare antes de usar.
- Todo comando simples termina com `;`. `LOGOUT` **nunca** leva `;`.
- Cada `if` e cada laço fecham com **um** `LOGOUT`, e o programa tem o seu. No `if/senão`,
  o `LOGOUT` vem só depois do senão.
- Condição: `(a OP b)`, com exatamente um operador relacional. Não há `&&`, `||`, `!`,
  encadeamento, `else if`, `for`, `break`, `%` nem booleanos.
- Sem sinal unário: `0 - 1`, não `-1`. Reais: `0.5` e `5.0`, nunca `.5` ou `5.`.
- `int / int` trunca; use um operando real (`x / 2.0`). Real **nunca** vai para `int`.
- Textos: aspas duplas, uma linha, só em `Hello There` ou na mensagem de leitura.
- `Hello There` junta os itens sem espaço e pula linha sozinho só se houver algum número.
- A leitura recebe uma variável: `(x)` ou `("mensagem" -> x)`.
- Variável declarada dentro de um bloco some no `LOGOUT` desse bloco.

## Arquivos de apoio

- `reference.md`: detalhes de tipos, saída, escopo e receitas para `%`, `||`, `else if` e `for`.
- `errors.md`: mensagem de erro → causa → correção, e o checklist antes de entregar.

## Validar

Na raiz do projeto do transpilador:

```bash
./sw check programa.starwars           # só verifica; erro sai com linha e coluna
./sw run programa.starwars             # transpila, compila e executa
./sw run programa.starwars < entrada.txt
```

Sempre transpile antes de entregar. Sem acesso a comandos, use o checklist de `errors.md`.
