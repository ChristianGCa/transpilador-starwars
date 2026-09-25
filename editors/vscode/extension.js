'use strict';

const vscode = require('vscode');
const language = require('./language');
const entries = require('./phrases.json');

function provideHover(document, position) {
  const lines = document.getText().split(/\r?\n/);
  const found = language.hoverAt(lines, position.line, position.character, entries);
  if (!found) return null;
  const range = new vscode.Range(position.line, found.start, position.line, found.end);
  return new vscode.Hover(new vscode.MarkdownString(found.markdown), range);
}

function provideCompletionItems(document, position) {
  const prefix = document.lineAt(position.line).text.slice(0, position.character);
  if (language.insideStringOrComment(prefix)) return [];
  return language.completions(prefix, entries).map(completion => {
    const item = new vscode.CompletionItem(
      { label: completion.label, description: completion.description },
      vscode.CompletionItemKind.Keyword,
    );
    item.range = new vscode.Range(position.line, completion.start, position.line, position.character);
    item.filterText = completion.filterText;
    item.documentation = new vscode.MarkdownString(completion.markdown);
    return item;
  });
}

function activate(context) {
  context.subscriptions.push(
    vscode.languages.registerHoverProvider('starwars', { provideHover }),
    vscode.languages.registerCompletionItemProvider('starwars', { provideCompletionItems }),
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
