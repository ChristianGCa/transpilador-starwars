# Linguagem Star Wars

Suporte do VS Code para a linguagem Star Wars (`.starwars`), uma linguagem de programação
temática com palavras-chave tiradas de falas de Star Wars, transpilada para C99.

```text
Há muito tempo, em uma galáxia muito, muito distante
energia: Você era o escolhido;
Ajude-me Obi-Wan Kenobi ("Informe a energia: " -> energia);
energia Eu alterei o acordo energia Que a força esteja com você 3 Eu sou todos os jedi 4;
Hello There ("Energia final: ", energia);
Chewie, estamos em casa
```

## Recursos

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

## Transpilador

A extensão cuida da edição. Para transpilar, compilar e executar os programas, use o
transpilador do [repositório do projeto](https://github.com/ChristianGCa/transpilador-starwars),
que também documenta a linguagem completa:

```bash
./sw run programa.starwars
```

## Autoria

Christian Gabriel Candeloni, Christian Mathias Michelson e Leonardo Daniel Becker.
Trabalho Prático 1 de Linguagens Formais e Compiladores (Unijuí).
