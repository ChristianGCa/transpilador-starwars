**LINGUAGENS FORMAIS E COMPILADORES**

**TRABALHO PRÁTICO 1**  
*Projeto e Implementação de uma Linguagem de Programação Temática*

Professor: Marcos Ronaldo Melo Cavalheiro

*Disciplina: Linguagens Formais e Compiladores — UNIJUÍ | Tópicos: ER, GLC, análise léxica, análise sintática, AST, análise semântica e geração de código*

**Forma de realização:** trabalho em grupo. Será realizada uma única entrega por grupo. Todos os integrantes deverão participar do planejamento, especificação, implementação, testes, documentação e apresentação do projeto.

**Objetivo Geral**

Projetar e implementar uma pequena linguagem de programação temática, formalizando seu léxico e sua sintaxe e construindo um transpilador (compilador fonte-a-fonte) capaz de reconhecer programas escritos nessa linguagem, produzir uma representação estrutural por meio de uma Árvore Sintática Abstrata (AST), realizar verificações semânticas mínimas e gerar código equivalente em uma linguagem destino executável.

**CÓDIGO-FONTE  →  LÉXICO  →  TOKENS  →  PARSER  →  AST  →  SEMÂNTICA  →  CÓDIGO DESTINO**

**O Modelo de Inspiração: BIRL**

Como ponto de partida, será utilizada como referência a BIRL (Bambam's "It's Show Time" Recursive Language), uma linguagem esotérica que associa bordões e expressões temáticas a construções tradicionais de programação. O objetivo da referência é mostrar que uma linguagem pode possuir uma sintaxe superficial criativa e, ao mesmo tempo, obedecer a regras léxicas e sintáticas formais.

**Referência:** [https://birl-language.github.io/](https://birl-language.github.io/)

| Regra de originalidade A linguagem do grupo não poderá ser apenas uma cópia da BIRL-Lite com substituição direta de palavras-chave. O grupo deverá justificar, no relatório, pelo menos três decisões próprias de projeto da sintaxe, como forma de declaração, delimitadores de bloco, estrutura de entrada/saída, construção condicional ou forma de repetição. |
| :---- |

**Resultados de Aprendizagem Esperados**

* Relacionar Expressões Regulares ao reconhecimento de tokens.  
* Utilizar uma Gramática Livre de Contexto para especificar a sintaxe de uma linguagem.  
* Implementar análise léxica e análise sintática e compreender a função de cada fase.  
* Representar o programa por meio de AST e aplicar verificações semânticas simples.  
* Traduzir construções da linguagem fonte para uma linguagem destino preservando seu significado.

**1\. Escopo Mínimo da Linguagem**

Cada grupo deverá definir um tema e projetar uma linguagem pequena, coerente e executável. O foco do trabalho não é criar uma linguagem industrial, mas desenvolver um subconjunto suficientemente rico para demonstrar as etapas fundamentais de um compilador/transpilador.

* Pelo menos dois tipos primitivos, sendo ao menos um tipo numérico (ex.: inteiro e real; inteiro e texto; inteiro e lógico).  
* Declaração de variáveis e atribuição de valores.  
* Expressões aritméticas com \+, \-, \* e /, respeitando precedência e parênteses.  
* Operadores relacionais para construção de expressões lógicas.  
* Estrutura de decisão com alternativa (equivalente a if/else).  
* Uma estrutura de repetição controlada por expressão lógica (equivalente a while ou for).  
* Comandos de entrada e saída de dados.  
* Delimitação clara do programa e dos blocos de comandos.

| Linguagem destino C será a linguagem de referência para o trabalho, pois preserva explicitamente conceitos como tipos, expressões, printf/scanf, if/else e laços. Outra linguagem destino poderá ser utilizada desde que seja tecnicamente justificada e informada ao professor no primeiro marco do projeto. |
| :---- |

**2\. Especificação Léxica**

O grupo deverá especificar formalmente os elementos reconhecidos pelo analisador léxico, relacionando a implementação aos conceitos de alfabeto, palavras e linguagens regulares apresentados em MENEZES (2011).

* Definir o alfabeto Σ utilizado pela linguagem.  
* Criar uma tabela de tokens contendo: categoria, expressão regular ou padrão, exemplo de lexema e descrição.  
* Definir palavras reservadas, identificadores, literais numéricos, literais de texto quando aplicável, operadores e delimitadores.  
* Definir o tratamento de espaços em branco e quebras de linha; comentários são opcionais, mas devem ser formalizados se existirem.  
* Tratar corretamente operadores com prefixos comuns, como \= e \==, observando a estratégia de maior casamento (longest match).  
* O analisador léxico deverá informar erro quando encontrar símbolo ou lexema inválido, indicando ao menos a linha da ocorrência.

**3\. Especificação Sintática — GLC**

A sintaxe deverá ser especificada por uma Gramática Livre de Contexto G \= (V, T, P, S), apresentada em notação BNF ou EBNF. A gramática deverá corresponder efetivamente à linguagem implementada.

* Identificar explicitamente o conjunto de variáveis/não terminais V, o conjunto de terminais T, as produções P e o símbolo inicial S.  
* Incluir produções para todas as estruturas obrigatórias do escopo mínimo.  
* Representar expressões de forma não ambígua, preservando precedência entre operadores aditivos e multiplicativos.  
* Permitir agrupamento com parênteses.  
* Evitar recursão à esquerda quando o grupo optar por parser preditivo por descida recursiva.

**4\. Analisador Sintático e AST**

O transpilador deverá implementar um parser que consuma a sequência de tokens produzida pelo analisador léxico e valide a estrutura do programa de acordo com a gramática definida pelo grupo.

* O parser poderá ser implementado manualmente por descida recursiva ou com ferramentas como ANTLR, JFlex/CUP, Lex/Yacc ou equivalentes.  
* Independentemente da ferramenta, o grupo deverá saber explicar quais produções da gramática reconhecem cada estrutura da linguagem.  
* O resultado do parsing deverá ser representado por uma Árvore Sintática Abstrata (AST). Quando a ferramenta escolhida gerar uma árvore de derivação, o grupo deverá utilizá-la para construir ou obter a representação necessária à geração de código.  
* Erros sintáticos devem interromper o processamento e indicar, sempre que possível, linha, token encontrado e elemento esperado.

**5\. Análise Semântica Mínima**

Após a análise sintática, deverá existir uma etapa semântica simples. Não se espera um sistema completo de tipos, mas o transpilador deve demonstrar que nem todo programa sintaticamente correto é semanticamente válido.

* Manter uma tabela de símbolos contendo, no mínimo, nome e tipo das variáveis declaradas.  
* Impedir o uso de variável antes de sua declaração.  
* Impedir a declaração duplicada de uma variável no mesmo escopo.  
* Verificar compatibilidade básica de tipos em atribuições e operações.  
* Emitir mensagem de erro semântico clara quando uma dessas regras for violada.

| Importante A gramática valida a forma do programa; a análise semântica valida propriedades que dependem de contexto, como a existência e o tipo de uma variável. Essas duas responsabilidades devem aparecer separadas na implementação e na explicação do grupo. |
| :---- |

**6\. Geração de Código**

Somente após as etapas de análise léxica, sintática e semântica serem concluídas com sucesso, o gerador de código deverá percorrer a AST e produzir o programa equivalente na linguagem destino.

* A tradução deve preservar o comportamento do programa de entrada.  
* Declarações e tipos devem ser mapeados de forma consistente para a linguagem destino.  
* Condicionais, repetições, expressões, entrada e saída devem ser geradas a partir dos nós correspondentes da AST.  
* Não será considerada suficiente uma implementação baseada apenas em substituição textual de palavras-chave.

**7\. Tratamento de Erros**

| Categoria | Exemplo de situação | Resposta esperada |
| :---- | :---- | :---- |
| Léxico | caractere @ não pertence ao padrão de nenhum token | indicar linha e caractere/lexema inválido |
| Sintático | declaração termina sem expressão após \= | indicar token encontrado e estrutura esperada |
| Semântico | atribuição a variável não declarada | indicar nome da variável e regra violada |

**Modelo de Referência — BIRL-Lite Revisada**

A BIRL-Lite abaixo serve apenas como modelo do nível de formalização esperado. Ela foi ampliada para apresentar declaração, atribuição, entrada, saída, decisão, repetição e expressões com precedência. Não copie esta gramática; utilize-a para compreender como as partes da especificação se relacionam.

**Definição Formal de G \= (V, T, P, S)**

| V \= { Programa, Bloco, Tipo, Declaracao, Comando, Atribuicao,      Leitura, Escrita, Condicional, Repeticao, ExprLogica,      OpRel, Expressao, Termo, Fator }T \= { HORA\_DO\_SHOW, BIRL, MONSTRO, TRAPEZIO, CE\_QUER\_VER,      QUE\_QUE\_CE\_QUER, ELE\_QUER, NAO\_VAI\_DAR, NEGATIVA\_BAMBAM,      id, num, string, \+, \-, \*, /, \=, \==, \!=, \>, \>=, \<, \<=,      (, ), ,, ; }S \= Programa |
| :---- |

**Tabela de Tokens — Exemplo**

| Token | Padrão / lexema | Descrição |
| :---- | :---- | :---- |
| HORA\_DO\_SHOW | HORA\_DO\_SHOW | início do programa |
| BIRL | BIRL | fim de bloco ou do programa |
| MONSTRO | MONSTRO | tipo inteiro (int) |
| TRAPEZIO | TRAPEZIO | tipo real (float) |
| CE\_QUER\_VER | CE\_QUER\_VER | comando de saída |
| QUE\_QUE\_CE\_QUER | QUE\_QUE\_CE\_QUER | comando de entrada |
| ELE\_QUER | ELE\_QUER | início do condicional |
| NAO\_VAI\_DAR | NAO\_VAI\_DAR | alternativa do condicional |
| NEGATIVA\_BAMBAM | NEGATIVA\_BAMBAM | estrutura de repetição |
| id | \[a-zA-Z\_\]\[a-zA-Z0-9\_\]\* | identificador |
| num | \[0-9\]+(\\.\[0-9\]+)? | literal numérico |
| string | "\[^"\\n\]\*" | literal de texto simplificado |
| op. aritméticos | \+  \-  \*  / | operações aritméticas |
| op. relacionais | \==  \!=  \>  \>=  \<  \<= | comparações |
| delimitadores | (  )  ,  ; | agrupamento e separação |

**Regras de Produção em EBNF — BIRL-Lite Revisada**

| (\* Programa principal \*)\<Programa\> ::= "HORA\_DO\_SHOW" \<Bloco\> "BIRL"(\* Sequência de declarações e comandos \*)\<Bloco\> ::= { \<Declaracao\> | \<Comando\> }\<Tipo\> ::= "MONSTRO" | "TRAPEZIO"\<Declaracao\> ::= \<Tipo\> id \[ "=" \<Expressao\> \] ";"\<Comando\> ::= \<Atribuicao\> | \<Leitura\> | \<Escrita\>            | \<Condicional\> | \<Repeticao\>\<Atribuicao\> ::= id "=" \<Expressao\> ";"\<Leitura\> ::= "QUE\_QUE\_CE\_QUER" "(" id ")" ";"\<Escrita\> ::= "CE\_QUER\_VER" "(" ( string | \<Expressao\> ) ")" ";"\<Condicional\> ::= "ELE\_QUER" "(" \<ExprLogica\> ")" \<Bloco\>                  \[ "NAO\_VAI\_DAR" \<Bloco\> \] "BIRL"\<Repeticao\> ::= "NEGATIVA\_BAMBAM" "(" \<ExprLogica\> ")"                \<Bloco\> "BIRL"\<ExprLogica\> ::= \<Expressao\> \<OpRel\> \<Expressao\>\<OpRel\> ::= "==" | "\!=" | "\>" | "\>=" | "\<" | "\<="\<Expressao\> ::= \<Termo\> { ( "+" | "-" ) \<Termo\> }\<Termo\>     ::= \<Fator\> { ( "\*" | "/" ) \<Fator\> }\<Fator\>     ::= id | num | "(" \<Expressao\> ")" |
| :---- |

**Precedência Obrigatória**

A separação entre Expressao, Termo e Fator deve produzir a interpretação correta de expressões como as seguintes:

| Entrada | Interpretação esperada |
| :---- | :---- |
| resultado \= 2 \+ 3 \* 4; | 2 \+ (3 \* 4\) |
| resultado \= (2 \+ 3\) \* 4; | (2 \+ 3\) \* 4 |

| Por que isso importa? A precedência não deve ser corrigida posteriormente pelo gerador de código. Ela deve estar representada na própria estrutura sintática e, consequentemente, na AST produzida pelo parser. |
| :---- |

**Exemplo Prático de Execução**

**Código-fonte de entrada — teste.birl**

| HORA\_DO\_SHOW  MONSTRO repeticoes \= 3;  TRAPEZIO carga \= 10.5;  NEGATIVA\_BAMBAM (repeticoes \> 0\)    CE\_QUER\_VER (repeticoes);    carga \= carga \+ 2 \* 1.5;    repeticoes \= repeticoes \- 1;  BIRL  ELE\_QUER (carga \>= 15\)    CE\_QUER\_VER ("Treino concluido\!\\n");  NAO\_VAI\_DAR    CE\_QUER\_VER ("Ainda falta carga.\\n");  BIRLBIRL |
| :---- |

O lexer transforma o arquivo em tokens; o parser valida a sequência conforme a GLC e constrói a AST; a análise semântica verifica as declarações e os tipos; somente então o gerador produz o programa equivalente na linguagem destino.

**Estrutura conceitual simplificada da AST**

| Programa ├─ Declaracao(MONSTRO, repeticoes, 3\) ├─ Declaracao(TRAPEZIO, carga, 10.5) ├─ While( repeticoes \> 0 ) │   ├─ Print(repeticoes) │   ├─ Atrib(carga, carga \+ (2 \* 1.5)) │   └─ Atrib(repeticoes, repeticoes \- 1\) └─ If( carga \>= 15 )     ├─ Print("Treino concluido\!\\n")     └─ Else → Print("Ainda falta carga.\\n") |
| :---- |

**Código C possível — saida.c**

| \#include \<stdio.h\>int main(void) {    int repeticoes \= 3;    float carga \= 10.5f;    while (repeticoes \> 0\) {        printf("%d\\n", repeticoes);        carga \= carga \+ 2 \* 1.5f;        repeticoes \= repeticoes \- 1;    }    if (carga \>= 15\) {        printf("Treino concluido\!\\n");    } else {        printf("Ainda falta carga.\\n");    }    return 0;} |
| :---- |

**8\. Suíte de Testes Obrigatória**

A entrega não poderá conter apenas um programa de demonstração. O grupo deverá apresentar uma pequena suíte de testes que evidencie tanto o reconhecimento correto quanto a rejeição de entradas inválidas.

| Arquivo sugerido | Objetivo mínimo |
| :---- | :---- |
| 01\_valido\_basico | declaração, atribuição e saída |
| 02\_valido\_completo | condicional, repetição, entrada/saída e expressões com precedência |
| 03\_erro\_lexico | símbolo ou lexema não reconhecido |
| 04\_erro\_sintatico | estrutura que viola a GLC |
| 05\_erro\_semantico | uso sem declaração, redeclaração ou incompatibilidade de tipos |

O teste válido completo deverá conter ao menos uma expressão em que a precedência seja relevante, como 2 \+ 3 \* 4 ou (2 \+ 3\) \* 4\. Para os casos inválidos, a execução deverá exibir a mensagem de erro produzida pelo próprio transpilador.

**9\. Entregáveis do Projeto**

1. Relatório Técnico de Especificação: tema, objetivos, três decisões próprias de projeto, alfabeto Σ, tabela de tokens/ER, G \= (V,T,P,S), gramática BNF/EBNF e regras semânticas adotadas.  
2. Código-fonte completo do transpilador, organizado e executável.  
3. Suíte de testes com os cinco casos mínimos definidos neste documento.  
4. Arquivos de código gerados na linguagem destino para os programas válidos.  
5. README com pré-requisitos, instruções de compilação/execução e exemplo de uso.

* Demonstração e apresentação do projeto pelo grupo, com participação de todos os integrantes e arguição técnica individual.

**10\. Autoria e Uso de Ferramentas de IA**

Ferramentas de Inteligência Artificial podem ser utilizadas como apoio ao estudo, revisão, geração de ideias e depuração, conforme as orientações da disciplina. O grupo permanece responsável por toda a especificação e implementação entregues.

* O relatório deverá informar, de forma breve, quais ferramentas foram utilizadas e para quais finalidades.  
* Durante a apresentação, qualquer integrante poderá ser questionado sobre tokens, produções da gramática, AST, análise semântica e geração de código.  
* Trechos que o grupo não consiga explicar serão considerados não demonstrados para fins de avaliação do domínio técnico.

**11\. Apresentação e Demonstração**

Conforme o Plano de Ensino, a Aula 18 é destinada à entrega, apresentação e demonstração do Projeto Integrado de Compilador. A apresentação, demonstração e defesa técnica correspondem a 15 pontos do trabalho. Cada grupo deverá apresentar a linguagem criada, explicar as principais decisões formais e demonstrar o funcionamento do transpilador com casos válidos e inválidos. Todos os integrantes deverão participar da apresentação e da arguição técnica.

Durante a demonstração, o professor poderá direcionar perguntas a qualquer integrante e solicitar novos casos de teste, explicações de tokens e produções, análise da AST, correção de erros ou pequenas modificações no código. A pontuação individual poderá ser diferenciada quando forem identificadas diferenças relevantes de participação, contribuição ou domínio da solução.

**12\. Critérios de Avaliação — 30 pontos**

**12.1 Desenvolvimento e Qualidade Técnica — 15 pontos**

| Critério | Pontos |
| :---- | :---: |
| Especificação léxica: alfabeto, tokens, expressões regulares e tratamento de erros léxicos | 2,0 |
| Especificação sintática: GLC completa em BNF/EBNF, organização das produções e precedência de operadores | 2,5 |
| Implementação do analisador léxico e do analisador sintático (parser), incluindo construção da AST | 3,0 |
| Análise semântica mínima: tabela de símbolos, declarações, escopo e verificações de tipos | 2,0 |
| Geração correta do código na linguagem destino | 3,0 |
| Suíte de testes, entradas válidas e inválidas e tratamento adequado de erros | 2,5 |
| **Subtotal** | **15,0** |

**12.2 Apresentação, Demonstração e Defesa Técnica — 15 pontos**

| Critério | Pontos |
| :---- | :---: |
| Organização e clareza da apresentação da linguagem criada, sua proposta e características | 2,0 |
| Explicação da especificação léxica, da gramática e das principais decisões de projeto | 3,0 |
| Demonstração prática do transpilador, incluindo entrada, análise e código destino gerado | 3,0 |
| Demonstração de casos válidos, erros léxicos, sintáticos e semânticos | 2,0 |
| Domínio técnico durante a arguição e capacidade de responder aos questionamentos | 3,0 |
| Participação efetiva e domínio do trabalho por todos os integrantes do grupo | 2,0 |
| **Subtotal** | **15,0** |
| **TOTAL DO TRABALHO** | **30,0** |

Os 15 pontos referentes ao desenvolvimento e à qualidade técnica serão atribuídos ao produto apresentado pelo grupo. Os 15 pontos referentes à apresentação, demonstração e defesa técnica avaliarão a capacidade de explicar, demonstrar e defender a solução. Durante a arguição, o professor poderá direcionar perguntas a qualquer integrante, solicitar novos testes ou pequenas modificações no código. A pontuação da etapa de apresentação poderá ser diferenciada individualmente quando forem identificadas diferenças relevantes de participação, contribuição ou domínio técnico. Também serão considerados o cumprimento dos requisitos e prazos e a transparência no uso de Inteligência Artificial, quando autorizado.

**13\. Cronograma Sugerido — Desenvolvimento Incremental**

| Marco | Produto a apresentar |
| :---- | :---- |
| Marco 1 | tema da linguagem, exemplos preliminares, decisões de projeto e linguagem destino |
| Marco 2 | alfabeto, tabela de tokens, expressões regulares e GLC em BNF/EBNF |
| Marco 3 | analisador léxico funcionando e testes léxicos |
| Marco 4 | parser \+ AST \+ tratamento de erros sintáticos |
| Marco 5 | análise semântica, geração de código, suíte de testes e relatório final |

| Acompanhamento Os marcos intermediários servem para revisão e feedback. Alterações de sintaxe e gramática podem ser solicitadas antes da implementação das fases seguintes para evitar que erros de especificação se propaguem pelo projeto. |
| :---- |

**14\. Bibliografia**

MENEZES, Paulo Blauth. Linguagens Formais e Autômatos. 6ª edição. Porto Alegre: Bookman, 2011\.

AHO, Alfred V.; SETHI, Ravi; ULLMAN, Jeffrey D. Compiladores: Princípios, Técnicas e Ferramentas. 2ª edição. São Paulo: Pearson Addison-Wesley, 2007\.

Plano de Ensino — Linguagens Formais e Compiladores, UNIJUÍ, 2026\.

BIRL — Bambam's "It's Show Time" Recursive Language. Disponível em: [https://birl-language.github.io/](https://birl-language.github.io/)