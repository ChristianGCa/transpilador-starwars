# Erros do transpilador e checklist

O primeiro erro interrompe a transpilação e informa a linha e a coluna.

| Mensagem (trecho) | Causa | Correção |
| --- | --- | --- |
| `ERRO LÉXICO` com `'%'`, `'&'`, `'\|'` ou `'!'` | operador inexistente | receitas em `reference.md` |
| `ERRO LÉXICO` com `'.'` | `.5` ou `5.` | `0.5`, `5.0` |
| `ERRO LÉXICO` com `'"'` | texto quebrado em linhas ou com escape inválido | `\n`; só `\n \r \t \" \\` |
| `ERRO LÉXICO` com `'''` | aspas simples | aspas duplas |
| `esperado '=', encontrado 'There'` (ou outra palavra) | frase reservada digitada errada e lida como variável | copiar a frase da tabela |
| `esperado tipo inteiro ou real` | tipo errado (`Voce`, `int`) | copiar a frase do tipo |
| `encontrado '-'` ou `'+'` no início de expressão | sinal unário | `0 - x` |
| `comando inválido começando com ';'` | `;` depois de `LOGOUT` | remover |
| `esperado ';'` | falta `;`, ou comparação usada como valor | adicionar `;`; usar `if` |
| `esperado ')', encontrado '>'` | condição com parênteses extras ou encadeada | `(a > b)` |
| `esperado '('` | condição sem parênteses | `(x > 0)` |
| `esperado '->'` | vírgula na leitura | `("Texto: " -> x)` |
| `esperado 'LOGOUT', encontrado fim do arquivo` | falta `LOGOUT` | um por `if`/laço, mais o do programa |
| `esperado fim do arquivo` | `LOGOUT` a mais, geralmente antes de `Tentativa não há` | remover |
| `encontrado "texto"` | texto em expressão, comparação ou atribuição | textos só em saída/leitura |
| `não declarada neste escopo` | uso antes da declaração ou fora do bloco onde foi declarada | declarar antes, fora do bloco |
| `já declarada neste escopo` | declaração repetida no mesmo bloco | declarar uma vez e depois atribuir |
| `não é possível atribuir float à variável int` | real em variável `int` | declarar como real |
| `literal fora do intervalo de int` | inteiro > 2147483647 | usar um valor menor ou um real |

## Checklist final

- [ ] `INICIA_SISTEMA` no início e `LOGOUT` no fim, e nada depois dele.
- [ ] Frases copiadas da tabela, com acentos, vírgulas e espaços simples.
- [ ] Um `LOGOUT` por `if`/laço, nenhum antes de `Tentativa não há` e nenhum seguido de `;`.
- [ ] `;` em todo comando simples.
- [ ] Variáveis declaradas antes do uso e visíveis no ponto de uso.
- [ ] Nenhum `-x`, `%`, `&&`, `||`, `.5`, aspas simples ou texto fora de saída/leitura.
- [ ] Resultados com casas decimais guardados em variáveis reais.
- [ ] Espaços e `\n` da saída escritos dentro dos textos.
- [ ] `./sw check` sem erros e `./sw run` com a saída esperada.
