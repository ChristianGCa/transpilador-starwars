# Erros do transpilador e checklist

O primeiro erro interrompe a transpilação e informa a linha e a coluna.

Na parte `esperado ...`, as mensagens mostram a **forma curta** da frase. A parte
`encontrado ...` mostra o que está escrito no arquivo.

| Na mensagem | Frase correspondente |
| --- | --- |
| `'INICIA_SISTEMA'` | `Há muito tempo, em uma galáxia muito, muito distante` |
| `'LOGOUT'` | `Chewie, estamos em casa` |
| `'='` | `Eu alterei o acordo` |
| `'+'`, `'-'`, `'*'`, `'/'` | as frases de soma, subtração, multiplicação e divisão |
| `'=='`, `'!='`, `'>'`, `'>='`, `'<'`, `'<='` | as frases de comparação |

As listagens de `--tokens` também mostram a frase reconhecida.

| Mensagem (trecho) | Causa | Correção |
| --- | --- | --- |
| `ERRO LÉXICO` com `'%'`, `'&'`, `'\|'` ou `'!'` | operador inexistente | receitas em `reference.md` |
| `ERRO LÉXICO` com `'.'` | `.5` ou `5.` | `0.5`, `5.0` |
| `ERRO LÉXICO` com `'"'` | texto quebrado em linhas ou com escape inválido | `\n`; só `\n \r \t \" \\` |
| `ERRO LÉXICO` com `'''` | aspas simples | aspas duplas |
| `esperado 'INICIA_SISTEMA'` | frase de início ausente ou digitada errada | copiar a frase da tabela |
| `esperado '=', encontrado 'There'` (ou outra palavra) | frase reservada digitada errada e lida como variável | copiar a frase da tabela |
| `esperado tipo inteiro ou real` | tipo errado (`Voce`, `int`) | copiar a frase do tipo |
| `encontrado '-'` ou `'+'` no início de expressão | sinal unário | `0 Acabou anakin x` |
| `comando inválido começando com ';'` | `;` depois do fim de bloco | remover |
| `esperado ';'` | falta `;`, ou comparação usada como valor | adicionar `;`; usar `if` |
| `esperado ')', encontrado 'I have the high ground'` (ou outro comparador) | condição com parênteses extras ou encadeada | `(a I have the high ground b)` |
| `esperado '('` | condição sem parênteses | `(x I have the high ground 0)` |
| `esperado '->'` | vírgula na leitura | `("Texto: " -> x)` |
| `esperado 'de'` ou `esperado 'até'` | cabeçalho do `for` incompleto ou `ate` sem acento | `This is the way (i de 1 até n)` |
| `esperado identificador, encontrado ...` logo após `This is the way (` | faltou o nome da variável de controle | `(i de ...)` |
| `os limites do laço 'This is the way' devem ser inteiros` | início ou fim real | usar expressões inteiras |
| `variável de controle 'i' não pode ser alterada dentro do laço` | atribuição ou leitura na variável do `for` | usar outra variável ou um `while` |
| `funções devem ser definidas logo após o início do programa` | função depois de um comando ou declaração | mover todas as funções para o topo |
| `esperado ':'` dentro do cabeçalho da função | parâmetro sem tipo | `nome(x: Você era o escolhido)` |
| `função 'f' não declarada` | nome errado ou função inexistente | conferir o nome |
| `a função 'f' espera N argumento(s), mas recebeu M` | quantidade errada de argumentos | um argumento por parâmetro |
| `o argumento N de 'f' deve ser int` | real passado a parâmetro inteiro | declarar o parâmetro como real |
| `não retorna valor e não pode ser usada em expressões` | procedimento usado como valor | dar tipo à função ou chamá-la como comando |
| `'Palpatine retornou' só pode ser usado dentro de uma função` | retorno no programa principal | remover |
| `a função 'f' não retorna valor` | retorno com valor em procedimento | `Palpatine retornou;` ou dar tipo à função |
| `a função 'f' deve retornar um valor do tipo ...` | `Palpatine retornou;` sem valor em função com tipo | informar o valor |
| `a função 'f' deve retornar int` | retorno real em função inteira | mudar o tipo da função para real |
| `a função 'f' pode terminar sem 'Palpatine retornou'` | algum caminho sem retorno | retorno no fim do corpo |
| `'x' já é o nome de uma função` | variável ou parâmetro com nome de função | escolher outro nome |
| `não declarada` dentro de uma função | uso de variável do programa principal | receber o valor por parâmetro |
| `esperado 'LOGOUT', encontrado fim do arquivo` | falta `Chewie, estamos em casa` | um por `if`/laço, mais o do programa |
| `esperado fim do arquivo` | fim a mais, geralmente antes de `Tentativa não há` | remover |
| `encontrado "texto"` | texto em expressão, comparação ou atribuição | textos só em saída/leitura |
| `não declarada neste escopo` | uso antes da declaração ou fora do bloco onde foi declarada | declarar antes, fora do bloco |
| `já declarada neste escopo` | declaração repetida no mesmo bloco | declarar uma vez e depois atribuir |
| `não é possível atribuir float à variável int` | real em variável `int` | declarar como real |
| `literal fora do intervalo de int` | inteiro > 2147483647 | usar um valor menor ou um real |

## Checklist final

- [ ] Começa com `Há muito tempo, em uma galáxia muito, muito distante` e termina com
      `Chewie, estamos em casa`, sem nada depois.
- [ ] Todas as frases copiadas da tabela, com acentos, vírgulas e espaços simples,
      inclusive as dos operadores.
- [ ] Um `Chewie, estamos em casa` por `if`/laço, nenhum antes de `Tentativa não há`
      e nenhum seguido de `;`.
- [ ] `;` em todo comando simples.
- [ ] Variáveis declaradas antes do uso e visíveis no ponto de uso.
- [ ] Funções no topo; as com tipo retornam em todo caminho; chamadas com os argumentos certos.
- [ ] Nenhum `-x`, `%`, `&&`, `||`, `.5`, aspas simples ou texto fora de saída/leitura.
- [ ] Resultados com casas decimais guardados em variáveis reais.
- [ ] Espaços e `\n` da saída escritos dentro dos textos.
- [ ] `./sw check` sem erros e `./sw run` com a saída esperada.
