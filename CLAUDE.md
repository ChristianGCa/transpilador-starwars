# CLAUDE.md

Transpilador de uma linguagem temática de Star Wars para C99, feito para o Trabalho
Prático 1 de Linguagens Formais e Compiladores (Unijuí). Pipeline:
fonte → lexer → tokens → parser → AST → análise semântica → código C.

## Comandos

```bash
python3 -B -m unittest discover -s tests -v              # testes (exige GCC)
python3 -m starwars arquivo.starwars -o saida.c
python3 -m starwars arquivo.starwars --tokens --ast
gcc -std=c99 -Wall -Wextra saida.c -o saida.bin
```

- Somente a biblioteca padrão do Python (3.8+). Não adicione dependências externas.
- Os arquivos em `examples/generated/` são verificados pelos testes: ao mudar a geração
  de C, regenere-os a partir das fontes em `examples/`.
- Estrutura: `starwars/` (um módulo por fase), `tests/` (um arquivo por fase), `examples/`, `docs/`.

## Idioma

- Código em inglês: nomes de arquivos, módulos, classes, funções, variáveis e testes.
- Textos voltados ao usuário em português: mensagens de erro, ajuda da CLI, documentação.
- Comentários e docstrings, quando existirem, em português.
- Palavras-chave da linguagem Star Wars e mensagens de erro (`ERRO LÉXICO`, `ERRO SINTÁTICO`,
  `ERRO SEMÂNTICO`, `ERRO DE ENTRADA`) fazem parte da especificação: não traduza.

## Estilo de código

- Evite comentários. Escreva apenas quando o motivo não puder ser expresso pelo código
  (uma regra da especificação, uma armadilha do C como trigraphs). Nunca comente o óbvio.
- Nomes descritivos no lugar de comentários explicativos.
- Siga a PEP 8, use type hints em funções públicas e prefira `dataclasses` para nós da AST.
- Módulos pequenos e com uma responsabilidade; um arquivo não deve misturar fases do compilador.
- Sem código morto, sem prints de depuração, sem imports não usados.
- Erros de compilação usam `CompilerError` com a categoria e a linha na mensagem.

## Testes

- Toda mudança de comportamento vem com teste. Correções de bug começam com um teste que falha.
- Rode a suíte completa antes de cada commit; ela deve passar sem falhas.
- Refatorações não podem mudar a saída: o C gerado e as mensagens de erro devem ser idênticos.

## Commits

- Conventional Commits (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`),
  com escopo quando ajudar: `refactor(parser): extrai parsing de expressões`.
- Mensagens em português do Brasil, no imperativo, descritivas porém curtas
  (assunto com até ~72 caracteres; corpo opcional explicando o porquê).
- Sem trailers de coautoria (`Co-Authored-By`) nem menções a ferramentas de IA.
- Commits granulares e pequenos: um por mudança lógica, cada um com a suíte passando.
  Não misture refatoração com mudança de comportamento.
- Não faça commit de arquivos do superpowers (`docs/superpowers/`), binários ou `__pycache__`.
