# Especificação técnica — Linguagem Star Wars

Disciplina: Linguagens Formais e Compiladores — UNIJUÍ.

**Identificação do grupo:** preencher os nomes dos integrantes antes da entrega.

## 1. Tema, objetivo e linguagem destino

O projeto utiliza frases do universo Star Wars para representar construções de uma
linguagem imperativa pequena. O objetivo é demonstrar análise léxica, análise
sintática, construção de AST, verificação semântica e geração de código equivalente.

A implementação está em Python e o destino é C99, a linguagem de referência do
enunciado. O ambiente de demonstração utiliza GCC, `int` de 32 bits e `float`
IEEE-754 de precisão simples. C torna explícitos os tipos, blocos, operações,
`printf`, `scanf`, `if/else` e `while` estudados na disciplina.

## 2. Três decisões próprias de projeto da sintaxe

As extensões abaixo alteram a estrutura da linguagem em relação ao modelo BIRL-Lite;
não consistem apenas na troca de nomes das palavras-chave.

1. **Declaração com nome antes do tipo:** `energia: Você era o escolhido = 10;`.
   O `:` separa o nome escolhido pelo programador da anotação de tipo. Isso torna
   possível localizar rapidamente as variáveis à esquerda das declarações. O parser
   diferencia declaração de atribuição verificando o token seguinte ao identificador.
2. **Leitura com mensagem integrada e destino explícito:**
   `Ajude-me Obi-Wan Kenobi ("Energia: " -> energia);`.
   O texto é exibido antes da leitura e a seta indica a variável que recebe o valor.
   A AST representa essa operação por um nó `Leitura` contendo mensagem opcional e
   destino. Evita exigir um comando separado para a pergunta ao usuário.
3. **Saída de uma lista heterogênea de itens:**
   `Hello There ("Energia: ", energia, " / limite: ", 100);`.
   Um mesmo comando aceita vários textos e expressões numéricas. A AST guarda uma
   lista de itens, permitindo apresentar rótulos e valores na mesma linha sem uma
   linguagem adicional de formatação.

A declaração prefixada `tipo nome = expressão;`, a saída com um item e as frases
originais de operadores foram preservadas como formas alternativas. Assim, o arquivo
original `teste.starwars` continua válido. Os exemplos novos exercitam as extensões.
Os símbolos aritméticos e relacionais usuais são aliases das frases temáticas.

## 3. Especificação léxica

### 3.1 Alfabeto e palavras

O arquivo é decodificado em UTF-8. Seja Σ o conjunto dos valores escalares Unicode
(U+0000 a U+D7FF e U+E000 a U+10FFFF). O arquivo fonte é uma palavra de Σ*.
Nem toda palavra de Σ* é um programa válido: os tokens restringem as sequências
permitidas e o parser impõe sua organização.

Os identificadores usam letras ASCII, `_` e letras latinas acentuadas nos intervalos
`À-Ö`, `Ø-ö`, `ø-ÿ`; a partir do segundo caractere também podem conter dígitos ASCII.
Texto e comentários podem conter outros caracteres Unicode. Um caractere como `@`
é permitido dentro de texto/comentário, mas causa erro léxico fora deles.

Cada categoria de token define uma linguagem regular: palavras-chave são palavras
fixas, identificadores/números são descritos por expressões regulares, e alternativas
e repetições usam união e fechamento. A linguagem de programas também precisa da
GLC e das regras contextuais das próximas seções.

### 3.2 Palavras reservadas

São sensíveis a maiúsculas, acentos e espaços. Os espaços internos das frases
reservadas são exatamente os apresentados na tabela.

| Categoria | Padrão e exemplo de lexema | Descrição |
| --- | --- | --- |
| INICIA | `INICIA_SISTEMA` | Início do programa |
| LOGOUT | `LOGOUT` | Final do programa ou de um bloco de controle |
| NUM_TYPE | `Você era o escolhido` | Tipo inteiro |
| REAL_TYPE | `Eu sou C3PO, ciborgue de relações humanas` | Tipo real |
| ASSIGN | `Eu alterei o acordo` ou `=` | Atribuição/inicialização |
| PLUS | `Que a força esteja com você` ou `+` | Adição |
| MINUS | `Acabou anakin` ou `-` | Subtração |
| STAR | `Eu sou todos os jedi` ou `*` | Multiplicação |
| SLASH | `Eu sou todos os sith` ou `/` | Divisão |
| EQ | `Como deve ser` ou `==` | Igualdade |
| NEQ | `!=` | Diferença |
| GT | `I have the high ground` ou `>` | Maior |
| GE | `A força é forte nele` ou `>=` | Maior ou igual |
| LT | `Você subestima meu poder` ou `<` | Menor |
| LE | `Não, eu sou seu pai` ou `<=` | Menor ou igual |
| IF | `Faça, ou não faça` | Condicional |
| ELSE | `Tentativa não há` | Alternativa do condicional |
| PRINT | `Hello There` | Saída de dados |
| INPUT | `Ajude-me Obi-Wan Kenobi` | Entrada de dados |
| WHILE | `Eu sinto uma perturbação na força` | Repetição |

### 3.3 Demais categorias

As expressões regulares abaixo usam a notação do módulo `re` do Python.

| Categoria | Expressão regular ou padrão literal | Exemplo | Descrição |
| --- | --- | --- | --- |
| ID | `[A-Za-z_À-ÖØ-öø-ÿ][A-Za-z0-9_À-ÖØ-öø-ÿ]*` | `energia2` | Identificador |
| NUM | `[0-9]+(\.[0-9]+)?` | `12`, `1.5`, `08` | Literal decimal inteiro ou real |
| STRING | Expressão STRING apresentada abaixo | `"Energia:\n"` | Texto |
| LPAREN | `(` | `(` | Início de agrupamento/argumentos |
| RPAREN | `)` | `)` | Fim de agrupamento/argumentos |
| SEMI | `;` | `;` | Fim de comando simples |
| COLON | `:` | `:` | Separa nome e tipo |
| COMMA | `,` | `,` | Separa itens de saída |
| ARROW | `->` | `->` | Separa mensagem e destino da leitura |
| SKIP | `[ \t]+` | espaços | Descartado |
| NEWLINE | Expressão NEWLINE apresentada abaixo | quebra de linha | Descartado; incrementa a linha |
| COMMENT | `#[^\r\n]*` | `# comentario` | Descartado até a quebra de linha |
| EOF | fim da entrada, sem lexema | — | Marcador técnico do lexer |

Expressões exatas que contêm união, apresentadas fora da tabela para evitar
interferência do separador de colunas do Markdown:

```text
STRING  = "(?:[^"\\\x00-\x1f\x7f]|\\["\\nrt])*"
NEWLINE = \r\n|\r|\n
```

STRING não contém quebras de linha nem controles ASCII crus. Reconhece as sequências
`\n`, `\r`, `\t`, `\"` e `\\`; escapes desconhecidos são erros léxicos. Texto não é
um terceiro tipo de variável: é um literal permitido em saída e mensagem de leitura.
Os números não têm sinal ou expoente na sintaxe; para valores negativos nas
expressões, utiliza-se subtração, como `0 - 3`.

### 3.4 Reconhecimento, maior casamento e erros

O lexer percorre a entrada da esquerda para a direita. Tenta primeiro frases
reservadas, da mais longa para a mais curta, exigindo que o caractere seguinte não
seja continuação de identificador. Assim, `LOGOUTx` é ID e não `LOGOUT` seguido de ID.
Depois reconhece as categorias simples. Operadores compostos (`==`, `!=`, `>=`,
`<=`, `->`) vêm antes dos operadores de um caractere; as repetições dos padrões são
gulosas. CRLF é reconhecido antes das quebras isoladas.

Espaços, tabulações, comentários e quebras de linha são ignorados entre tokens.
LF, CRLF e CR contam como uma linha cada. Um caractere sem correspondência causa
`ERRO LEXICO`, com linha e caractere, e interrompe o processamento.
Uma palavra-chave dentro de texto/comentário não é interpretada como comando.

## 4. Gramática livre de contexto G = (V, T, P, S)

A gramática está em EBNF. `{ X }` indica zero ou mais repetições, `[ X ]` indica
opcionalidade e `|` indica alternativa. Os nomes em maiúsculas são categorias de
token da seção 3; aliases de um mesmo operador produzem a mesma categoria.

```text
V = { Programa, Bloco, Tipo, Declaracao, Comando, Atribuicao,
      Leitura, Escrita, ItemSaida, Condicional, Repeticao,
      ExprLogica, OpRel, Expressao, Termo, Fator }

T = { INICIA, LOGOUT, NUM_TYPE, REAL_TYPE, ASSIGN,
      PLUS, MINUS, STAR, SLASH, EQ, NEQ, GT, GE, LT, LE,
      IF, ELSE, PRINT, INPUT, WHILE, ID, NUM, STRING,
      LPAREN, RPAREN, SEMI, COLON, COMMA, ARROW }

S = Programa
```

SKIP, COMMENT e NEWLINE são descartados antes do parser. EOF é um marcador externo
à gramática: depois de reconhecer Programa, o parser exige EOF para rejeitar sobras.

O conjunto P contém as seguintes produções:

```ebnf
Programa    ::= INICIA Bloco LOGOUT
Bloco       ::= { Declaracao | Comando }
Tipo        ::= NUM_TYPE | REAL_TYPE
Declaracao  ::= ( Tipo ID | ID COLON Tipo ) [ ASSIGN Expressao ] SEMI
Comando     ::= Atribuicao | Leitura | Escrita | Condicional | Repeticao
Atribuicao  ::= ID ASSIGN Expressao SEMI
Leitura     ::= INPUT LPAREN [ STRING ARROW ] ID RPAREN SEMI
Escrita     ::= PRINT LPAREN ItemSaida { COMMA ItemSaida } RPAREN SEMI
ItemSaida   ::= STRING | Expressao
Condicional ::= IF LPAREN ExprLogica RPAREN Bloco [ ELSE Bloco ] LOGOUT
Repeticao   ::= WHILE LPAREN ExprLogica RPAREN Bloco LOGOUT
ExprLogica  ::= Expressao OpRel Expressao
OpRel       ::= EQ | NEQ | GT | GE | LT | LE
Expressao   ::= Termo { ( PLUS | MINUS ) Termo }
Termo       ::= Fator { ( STAR | SLASH ) Fator }
Fator       ::= ID | NUM | LPAREN Expressao RPAREN
```

A gramática não usa recursão à esquerda. O parser é manual, por descida recursiva.
O caso `ID COLON Tipo` usa antecipação de dois tokens para diferenciar declaração
pós-fixada de atribuição. Multiplicação/divisão têm precedência sobre adição/subtração;
operadores no mesmo nível associam à esquerda. Parênteses mudam o agrupamento.
Comparações não são encadeadas; cada condição contém exatamente um operador relacional.

O `LOGOUT` encerra o bloco de controle mais interno ainda aberto. No condicional,
o mesmo `LOGOUT` encerra a estrutura inteira, inclusive a alternativa quando presente.
Um `LOGOUT` adicional encerra o programa. Blocos e alternativas podem ser vazios.

## 5. AST e separação das etapas

| Nó | Informação principal |
| --- | --- |
| Programa | Lista de declarações/comandos |
| Declaracao | Tipo, nome, inicializador opcional e linha |
| Atribuicao | Nome, expressão e linha |
| Leitura | Nome de destino, mensagem opcional e linha |
| Escrita | Lista de textos/expressões e linha |
| Condicional | Condição, bloco verdadeiro e bloco alternativo opcional |
| Repeticao | Condição e corpo |
| ExprLogica | Operandos e operador relacional |
| BinOp | Operandos e operador aritmético |
| Num, Var, StringLit | Literal ou referência a uma variável |

Por exemplo, `2 + 3 * 4` produz `BinOp(2, +, BinOp(3, *, 4))`, enquanto
`(2 + 3) * 4` produz `BinOp(BinOp(2, +, 3), *, 4)`. A precedência já está na AST;
o gerador apenas conserva esse agrupamento com parênteses.

`Parser` reconhece a forma e constrói os nós. `AnalisadorSemantico` percorre a árvore,
valida contexto e a anota com tipos e nomes de destino. `gerar_codigo_c` percorre a
árvore anotada. `analisar` e `transpilar` coordenam as fases; uma exceção interrompe
as etapas seguintes. Não há substituição textual do programa fonte.

## 6. Regras semânticas

1. Existem os tipos `int` e `float`. O ponto decimal distingue literais reais.
   Literais inteiros não negativos devem caber entre 0 e 2147483647; reais devem
   ser finitos e não ultrapassar o maior float de 32 bits. A precisão/representação
   segue o C de destino. Zeros iniciais continuam decimais: `08` representa oito.
2. A tabela de símbolos é uma pilha de dicionários. Cada entrada contém nome fonte,
   tipo e nome único no C. O programa tem um escopo; cada corpo de `if`, `else` ou
   `while` abre seu próprio escopo. A busca ocorre do escopo interno para o externo.
3. Uso de variável exige declaração visível anterior, inclusive em inicializadores,
   condições, expressões e leitura. Duas declarações do mesmo nome no mesmo escopo
   são rejeitadas. Escopos distintos podem declarar o mesmo nome.
4. O nome novo fica visível depois de verificar o inicializador. Uma declaração
   interna `x: tipo = x + 1;` consulta o `x` externo; sem um `x` externo, é erro.
   Nomes C únicos preservam essa regra e o sombreamento.
5. Declarações sem inicializador recebem zero. Variáveis de um bloco deixam de ser
   visíveis ao sair dele. Uma declaração de um ramo não fica visível no outro ramo.
6. Inteiro pode ser atribuído a real. Real não pode ser atribuído a inteiro, tanto
   na declaração quanto em atribuições posteriores. Não há conversão explícita.
7. Operações aritméticas aceitam somente expressões numéricas. Se algum operando é
   real, o resultado é real; caso contrário é inteiro. Divisão de inteiros trunca
   em direção a zero, como em C. Comparações numéricas podem misturar inteiro e real.
   Strings não participam de operações/atribuições: a gramática restringe seus usos.
8. Leitura só recebe uma variável declarada; seu tipo escolhe `%d` ou `%f` no `scanf`.
   Uma falha de conversão ou fim de entrada encerra o programa gerado com mensagem
   e status 1. O consumo da entrada segue `scanf`, incluindo seus prefixos numéricos.
9. Erros semânticos informam linha e a regra violada; erros sobre variáveis também
   identificam seu nome. Os limites numéricos em operações em tempo de execução,
   divisão por zero e entrada numérica fora da faixa não têm verificação adicional:
   os programas devem respeitar o domínio dos tipos do C adotado.

## 7. Geração de C e comportamento de saída

- Declarações viram `int` ou `float`, com inicializador explícito.
- Cada declaração recebe um nome como `sw_v0`, independente do nome fonte. Isso
  evita colisões com `return`, `printf` e outros identificadores do C, e permite
  usar nomes acentuados sem depender das regras de identificadores do compilador C.
- Literais são normalizados para decimal; reais recebem sufixo `f`.
- Operadores temáticos são mapeados para os símbolos C; os nós BinOp geram parênteses.
- Condicional e repetição viram `if/else` e `while` com chaves, preservando os escopos.
- Textos são passados como argumento de `printf("%s", texto)`, portanto `%` e `%n`
  no texto são impressos literalmente. Interrogações são escapadas para evitar
  interpretação de trigraphs do C99. Os escapes de texto permitidos têm a mesma
  interpretação no C.
- Expressões inteiras usam `%d`; reais usam `%g` com promoção para `double`.
  Uma saída concatena os itens, sem espaços automáticos, e acrescenta uma quebra de
  linha ao final se contiver pelo menos uma expressão numérica. Textos sozinhos
  não recebem quebra automática. O programador pode usar `\n` em textos.
- A leitura com mensagem imprime o texto, descarrega stdout e chama `scanf` para
  a variável correta. O retorno da leitura é verificado.

A linguagem não inclui funções, `for`, booleanos armazenáveis, vetores ou variáveis
de texto. O `while` atende ao requisito de repetição e os dois tipos numéricos
atendem ao mínimo de tipos primitivos.

## 8. Erros e testes

| Categoria | Exemplo | Resultado |
| --- | --- | --- |
| Léxico | `@` fora de texto/comentário | Linha e caractere inválido |
| Sintático | `x: Você era o escolhido = ;` | Linha, elemento esperado e encontrado |
| Semântico | `x = 1;` sem declaração | Linha, nome e declaração ausente |
| Semântico | `x: Você era o escolhido = 1.5;` | Incompatibilidade de tipos |
| Semântico | Uso de nome local fora de seu bloco | Nome não declarado no escopo atual |

Os arquivos 01 a 05 em `testes/` cumprem os cinco casos mínimos do enunciado.
Os arquivos 06 a 08 demonstram mais erros semânticos. O programa completo contém
leitura de inteiro e real, decisão com alternativa, repetição, saída composta,
`2 + 3 * 4` e `(2 + 3) * 4`. Os arquivos de entrada e de saída esperada acompanham
os exemplos. `gerados/` contém o código destino dos programas válidos.

A suíte `testes/test_transpilador.py` usa unittest e GCC. Verifica também a forma
da AST, limites de palavras-chave, operadores com prefixos comuns, inicialização,
sombreamento, erros em expressões, texto com `%`, escapes, nomes reservados no C,
zeros iniciais, CR/LF e o comportamento da interface em falhas. Os testes compilam
e executam C temporário e comparam a saída observada com a esperada.

Reprodução:

```bash
python3 -B -m unittest discover -s testes -v
```

## 9. Autoria e uso de IA

Nesta revisão foi utilizado OpenAI Codex como apoio para comparar a implementação
com o enunciado, identificar e corrigir falhas, completar a entrada de dados,
propor e implementar as três extensões de sintaxe, produzir testes automatizados
e redigir a documentação. A implementação original foi preservada como base.

Esta declaração descreve o apoio realizado nesta revisão; não pressupõe quais
ferramentas foram usadas anteriormente pelo grupo. O grupo deve complementar a
identificação dos integrantes e o histórico de uso de ferramentas, se necessário,
e revisar, compreender e assumir a responsabilidade pela versão entregue.
A participação e a defesa técnica individual precisam ser realizadas pelos integrantes.

## 10. Relação com a bibliografia indicada no enunciado

A especificação utiliza os conceitos de alfabeto, palavras e linguagens regulares
indicados em MENEZES, Paulo Blauth. *Linguagens Formais e Autômatos*, 6ª ed., 2011.
A organização em lexer, parser, AST, semântica e geração de código corresponde aos
tópicos de compiladores indicados em AHO, Alfred V.; SETHI, Ravi; ULLMAN, Jeffrey D.
*Compiladores: Princípios, Técnicas e Ferramentas*, referência fornecida no enunciado.
Essas são referências bibliográficas propostas pelo trabalho; não são atribuídas
citações diretas nem páginas específicas às obras.
