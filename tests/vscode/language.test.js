'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const test = require('node:test');

const EXTENSION = path.join(__dirname, '..', '..', 'editors', 'vscode');
const language = require(path.join(EXTENSION, 'language.js'));
const entries = require(path.join(EXTENSION, 'phrases.json'));

const PROGRAM = [
  'Há muito tempo, em uma galáxia muito, muito distante',
  'Execute a ordem 66 mdc(a: Você era o escolhido, b: Você era o escolhido): Você era o escolhido',
  '    Palpatine retornou a;',
  'Chewie, estamos em casa',
  'Execute a ordem 66 aviso(codigo: Você era o escolhido)',
  '    Hello There ("codigo # nao e comentario", codigo);',
  'Chewie, estamos em casa',
  'soma: Eu sou C3PO, ciborgue de relações humanas Eu alterei o acordo 0.0;',
  'Você era o escolhido total;',
  'This is the way (i de 1 até 3)',
  '    soma Eu alterei o acordo soma Que a força esteja com você mdc(i, 2); # soma == 1',
  '    Ajude-me Obi-Wan Kenobi ("Valor: " -> total);',
  'Chewie, estamos em casa',
  'Chewie, estamos em casa',
];

function hover(lineIndex, text, offset = 0) {
  const character = PROGRAM[lineIndex].indexOf(text) + offset;
  assert.ok(character >= offset, `"${text}" não está na linha ${lineIndex}`);
  return language.hoverAt(PROGRAM, lineIndex, character, entries);
}

test('hover em uma frase mostra categoria, símbolo e equivalente em C', () => {
  const found = hover(10, 'Eu alterei o acordo', 5);
  assert.match(found.markdown, /\*\*Eu alterei o acordo\*\*/);
  assert.match(found.markdown, /`=`/);
  assert.equal(PROGRAM[10].slice(found.start, found.end), 'Eu alterei o acordo');
});

test('a frase mais longa vence: "de" dentro do tipo real mostra o tipo', () => {
  const found = hover(7, 'de relações');
  assert.match(found.markdown, /\*\*Eu sou C3PO, ciborgue de relações humanas\*\*/);
});

test('"de" no cabeçalho do for mostra a parte do laço', () => {
  assert.match(hover(9, ' de ', 1).markdown, /\*\*de\*\*/);
});

test('forma alternativa aponta para a frase principal', () => {
  const found = language.hoverAt(['LOGOUT'], 0, 2, entries);
  assert.match(found.markdown, /Chewie, estamos em casa/);
});

test('texto e comentário não têm hover', () => {
  assert.equal(hover(5, 'nao e comentario'), null);
  assert.equal(hover(10, '# soma == 1', 3), null);
});

test('símbolos mostram a frase equivalente', () => {
  assert.match(language.hoverAt(['x == 1;'], 0, 3, entries).markdown, /Como deve ser/);
  assert.match(language.hoverAt(['x = 1;'], 0, 2, entries).markdown, /Eu alterei o acordo/);
  assert.match(hover(11, '->').markdown, /leitura/);
});

test('variável mostra o tipo e a linha da declaração', () => {
  const found = hover(10, 'soma', 1);
  assert.match(found.markdown, /\*\*soma\*\*/);
  assert.match(found.markdown, /real/);
  assert.match(found.markdown, /linha 8/);
});

test('declaração prefixada também é encontrada', () => {
  assert.match(hover(11, 'total').markdown, /variável inteira[\s\S]*linha 9/);
});

test('variável de controle do for', () => {
  assert.match(hover(10, 'mdc(i', 4).markdown, /controle/);
});

test('parâmetro mostra a função a que pertence', () => {
  const found = hover(2, 'a;');
  assert.match(found.markdown, /parâmetro inteiro/);
  assert.match(found.markdown, /mdc/);
});

test('chamada de função mostra a assinatura', () => {
  const found = hover(10, 'mdc(i');
  assert.match(found.markdown, /mdc\(a: inteiro, b: inteiro\): inteiro/);
  assert.match(found.markdown, /linha 2/);
});

test('procedimento é identificado', () => {
  assert.match(hover(4, 'aviso').markdown, /procedimento/);
});

test('nome desconhecido não tem hover', () => {
  assert.equal(language.hoverAt(['x Eu alterei o acordo y;'], 0, 0, entries), null);
});

test('autocompletar cobre frases de várias palavras já digitadas', () => {
  const prefix = 'x Eu al';
  const item = language.completions(prefix, entries).find(c => c.label === 'Eu alterei o acordo');
  assert.equal(item.start, 2);
});

test('autocompletar aceita digitação sem acento', () => {
  const item = language.completions('Faca', entries).find(c => c.label === 'Faça, ou não faça');
  assert.equal(item.start, 0);
  assert.match(item.filterText, /Faca, ou nao faca/);
});

test('autocompletar por palavra em inglês usa só a palavra atual', () => {
  const item = language.completions('    whi', entries).find(c => c.label === 'Eu sinto uma perturbação na força');
  assert.equal(item.start, 4);
  assert.match(item.filterText, /while/);
});

test('autocompletar não oferece símbolos nem formas alternativas', () => {
  const labels = language.completions('', entries).map(c => c.label);
  assert.ok(!labels.includes('->'));
  assert.ok(!labels.includes('LOGOUT'));
});

test('detecta texto e comentário antes do cursor', () => {
  assert.equal(language.insideStringOrComment('Hello There ("Ol'), true);
  assert.equal(language.insideStringOrComment('x = 1; # nota'), true);
  assert.equal(language.insideStringOrComment('Hello There ("a\\"b") '), false);
});
