# Roteiro de apresentação e defesa técnica

## Antes da apresentação

Preencher a identificação do grupo no relatório e dividir a apresentação entre os
integrantes. Todos devem conseguir explicar cada etapa, mesmo que apresentem partes
diferentes. Executar a suíte do README e abrir o programa completo, o relatório e
o C gerado.

## Sequência de demonstração

1. Apresentar o tema Star Wars, os tipos inteiro/real e as três decisões próprias:
   declaração `nome: tipo`, leitura com mensagem e seta, e saída com vários itens.
2. Mostrar as expressões regulares de identificadores e números, a distinção entre
   `=` e `==` e por que `LOGOUTx` continua sendo um identificador.
3. Exibir as produções de expressão, termo e fator no relatório. Comparar as ASTs
   de `2 + 3 * 4` e `(2 + 3) * 4` usando a opção `--ast`.
4. Transpilar `examples/valid/02_complete.starwars`, mostrar o C e executá-lo com a
   entrada fornecida. Explicar por que são usados `%d`, `%f`, `%g` e `%s`.
5. Executar novamente com `0` repetições e nível `1` para demonstrar o ramo alternativo.
6. Rodar os arquivos de erro léxico, sintático e semântico separadamente. Mostrar
   que o erro vem do transpilador e interrompe o processamento antes da geração.
7. Demonstrar o erro de escopo e a rejeição de real em variável inteira. Explicar
   a pilha de tabelas de símbolos e o nome único de cada variável no C.
8. Mostrar a execução dos testes e concluir a demonstração. Informar o apoio de IA
   descrito no relatório e as responsabilidades do grupo.

## Perguntas para treinar em conjunto

- Qual a diferença entre lexema, token e categoria de token?
- Quais são V, T, P e S nesta gramática?
- Como o parser diferencia `x: tipo` de `x = expressão`?
- Por que a precedência pertence ao parser e à AST?
- Por que usar uma variável não declarada é erro semântico, embora a frase tenha forma válida?
- Como é permitido repetir um nome em blocos distintos sem aceitar duplicata no mesmo bloco?
- Por que `int x = 1.5` deve ser rejeitado segundo as regras escolhidas?
- Por que imprimir o texto diretamente como formato de printf causava problema com `%`?
- Como a declaração `return: Você era o escolhido = 8;` vira C válido?
- Quais recursos e verificações estão fora do escopo documentado da linguagem?
