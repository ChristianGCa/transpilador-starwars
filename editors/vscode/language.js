'use strict';

const IDENT_CHAR = /[A-Za-z0-9_À-ÖØ-öø-ÿ]/;
const IDENT = '[A-Za-z_À-ÖØ-öø-ÿ][A-Za-z0-9_À-ÖØ-öø-ÿ]*';
const TYPE_NAMES = {
  'Você era o escolhido': { masculine: 'inteiro', feminine: 'inteira', c: 'int' },
  'Eu sou C3PO, ciborgue de relações humanas': { masculine: 'real', feminine: 'real', c: 'float' },
};
const TYPE = Object.keys(TYPE_NAMES).map(escapeRegex).join('|');
const SYMBOLS = ['->', '==', '!=', '>=', '<=', '=', '+', '-', '*', '/', '>', '<'];

function escapeRegex(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function isIdentChar(ch) {
  return ch !== undefined && IDENT_CHAR.test(ch);
}

function stripAccents(text) {
  return text.normalize('NFD').replace(/[̀-ͯ]/g, '');
}

function normalize(text) {
  return stripAccents(text).toLowerCase();
}

// Troca textos e comentários por espaços, mantendo as colunas, para que o conteúdo
// deles não seja confundido com frases, símbolos ou nomes.
function maskLine(line) {
  const chars = [...line];
  let inString = false;
  for (let i = 0; i < chars.length; i++) {
    const ch = chars[i];
    if (inString) {
      if (ch === '\\' && i + 1 < chars.length) {
        chars[i] = ' ';
        i++;
      } else if (ch === '"') {
        inString = false;
      }
      chars[i] = ' ';
    } else if (ch === '"') {
      inString = true;
      chars[i] = ' ';
    } else if (ch === '#') {
      chars.fill(' ', i);
      break;
    }
  }
  return chars.join('');
}

function insideStringOrComment(prefix) {
  let inString = false;
  for (let i = 0; i < prefix.length; i++) {
    const ch = prefix[i];
    if (inString) {
      if (ch === '\\') i++;
      else if (ch === '"') inString = false;
    } else if (ch === '"') {
      inString = true;
    } else if (ch === '#') {
      return true;
    }
  }
  return inString;
}

function occurrences(masked, text) {
  const found = [];
  let index = masked.indexOf(text);
  while (index !== -1) {
    if (!isIdentChar(masked[index - 1]) && !isIdentChar(masked[index + text.length])) {
      found.push(index);
    }
    index = masked.indexOf(text, index + 1);
  }
  return found;
}

function phraseEntries(entries) {
  return entries.filter(entry => entry.kind !== 'symbol');
}

function phraseAt(masked, character, entries) {
  const lexemes = phraseEntries(entries)
    .flatMap(entry => [entry.phrase, ...(entry.aliases || [])].map(lexeme => ({ entry, lexeme })))
    .sort((a, b) => b.lexeme.length - a.lexeme.length);
  for (const { entry, lexeme } of lexemes) {
    for (const start of occurrences(masked, lexeme)) {
      if (character >= start && character < start + lexeme.length) {
        return { entry, lexeme, start, end: start + lexeme.length };
      }
    }
  }
  return null;
}

function symbolAt(masked, character) {
  let i = 0;
  while (i < masked.length) {
    const symbol = SYMBOLS.find(candidate => masked.startsWith(candidate, i));
    if (symbol) {
      if (character >= i && character < i + symbol.length) return { symbol, start: i, end: i + symbol.length };
      i += symbol.length;
    } else {
      i++;
    }
  }
  return null;
}

function identifierAt(masked, character) {
  if (!isIdentChar(masked[character])) return null;
  let start = character;
  let end = character;
  while (isIdentChar(masked[start - 1])) start--;
  while (isIdentChar(masked[end])) end++;
  const name = masked.slice(start, end);
  return /^[0-9]/.test(name) ? null : { name, start, end };
}

function typeLabel(typePhrase, gender) {
  const type = TYPE_NAMES[typePhrase];
  return `${type[gender]} (\`${type.c}\`)`;
}

function declarations(lines) {
  const functions = new Map();
  const variables = [];
  const functionHeader = new RegExp(`(?<![A-Za-z0-9_À-ÖØ-öø-ÿ])Execute a ordem 66\\s+(${IDENT})\\s*\\(([^)]*)\\)(?:\\s*:\\s*(${TYPE}))?`);
  const parameter = new RegExp(`(${IDENT})\\s*:\\s*(${TYPE})`, 'g');
  const forHeader = new RegExp(`(?<![A-Za-z0-9_À-ÖØ-öø-ÿ])This is the way\\s*\\(\\s*(${IDENT})`, 'g');
  const postfix = new RegExp(`(?<![A-Za-z0-9_À-ÖØ-öø-ÿ])(${IDENT})\\s*:\\s*(${TYPE})`, 'g');
  const prefix = new RegExp(`(${TYPE})\\s+(?!Eu alterei o acordo(?![A-Za-z0-9_À-ÖØ-öø-ÿ]))(${IDENT})`, 'g');
  let owner = null;
  lines.forEach((line, index) => {
    let masked = maskLine(line);
    const header = functionHeader.exec(masked);
    if (header) {
      owner = header[1];
      const params = [...header[2].matchAll(parameter)].map(match => ({ name: match[1], type: match[2] }));
      functions.set(owner, { line: index, params, returnType: header[3] });
      params.forEach(param => variables.push({ ...param, line: index, kind: 'parameter', owner }));
      masked = masked.slice(0, header.index) + ' '.repeat(header[0].length) + masked.slice(header.index + header[0].length);
    }
    for (const match of masked.matchAll(forHeader)) {
      variables.push({ name: match[1], type: 'Você era o escolhido', line: index, kind: 'control' });
    }
    for (const match of masked.matchAll(postfix)) {
      variables.push({ name: match[1], type: match[2], line: index, kind: 'variable' });
    }
    for (const match of masked.matchAll(prefix)) {
      variables.push({ name: match[2], type: match[1], line: index, kind: 'variable' });
    }
  });
  return { functions, variables };
}

function describeEntry(entry, lexeme) {
  const title = entry.symbol ? `**${entry.phrase}** · ${entry.category} · símbolo \`${entry.symbol}\`` :
    `**${entry.phrase}** · ${entry.category}`;
  const parts = [title];
  if (lexeme && lexeme !== entry.phrase) parts.push(`\`${lexeme}\` é a forma alternativa de \`${entry.phrase}\`.`);
  parts.push(entry.description);
  parts.push('```starwars\n' + entry.example + '\n```');
  parts.push(`Em C: \`${entry.c}\``);
  if (entry.origin) parts.push(`*${entry.origin}*`);
  return parts.join('\n\n');
}

function describeSymbol(symbol, entries) {
  const entry = entries.find(candidate => candidate.symbol === symbol || candidate.phrase === symbol);
  if (!entry) return null;
  if (entry.kind === 'symbol') return describeEntry(entry);
  return `\`${symbol}\` é o símbolo equivalente a **${entry.phrase}**.\n\n` + describeEntry(entry);
}

function signature(name, fn) {
  const params = fn.params.map(param => `${param.name}: ${TYPE_NAMES[param.type].masculine}`).join(', ');
  const result = fn.returnType ? `: ${TYPE_NAMES[fn.returnType].masculine}` : '';
  return `${name}(${params})${result}`;
}

function describeFunction(name, fn) {
  const kind = fn.returnType ? 'função' : 'procedimento (não devolve valor)';
  return `\`\`\`starwars\n${signature(name, fn)}\n\`\`\`\n\n${kind}, definida na linha ${fn.line + 1}.`;
}

function describeVariable(name, declaration) {
  const where = `linha ${declaration.line + 1}`;
  if (declaration.kind === 'parameter') {
    return `**${name}** · parâmetro ${typeLabel(declaration.type, 'masculine')} de \`${declaration.owner}\`, ${where}.`;
  }
  if (declaration.kind === 'control') {
    return `**${name}** · variável de controle do \`This is the way\`, inteiro (\`int\`), ${where}. ` +
      'Não pode ser alterada dentro do laço.';
  }
  return `**${name}** · variável ${typeLabel(declaration.type, 'feminine')}, declarada na ${where}.`;
}

function closestDeclaration(candidates, lineIndex) {
  const before = candidates.filter(candidate => candidate.line <= lineIndex);
  return before.length ? before[before.length - 1] : candidates[0];
}

function hoverAt(lines, lineIndex, character, entries) {
  const masked = maskLine(lines[lineIndex]);
  const phrase = phraseAt(masked, character, entries);
  if (phrase) return { markdown: describeEntry(phrase.entry, phrase.lexeme), start: phrase.start, end: phrase.end };
  const symbol = symbolAt(masked, character);
  if (symbol) {
    const markdown = describeSymbol(symbol.symbol, entries);
    return markdown ? { markdown, start: symbol.start, end: symbol.end } : null;
  }
  const identifier = identifierAt(masked, character);
  if (!identifier) return null;
  const { functions, variables } = declarations(lines);
  if (functions.has(identifier.name)) {
    return { markdown: describeFunction(identifier.name, functions.get(identifier.name)),
      start: identifier.start, end: identifier.end };
  }
  const candidates = variables.filter(variable => variable.name === identifier.name);
  if (!candidates.length) return null;
  const declaration = closestDeclaration(candidates, lineIndex);
  return { markdown: describeVariable(identifier.name, declaration), start: identifier.start, end: identifier.end };
}

function typedPhraseStart(prefix, phrase) {
  const target = normalize(phrase);
  for (let length = Math.min(prefix.length, phrase.length); length > 0; length--) {
    const start = prefix.length - length;
    if (isIdentChar(prefix[start - 1])) continue;
    if (target.startsWith(normalize(prefix.slice(start)))) return start;
  }
  return null;
}

function currentWordStart(prefix) {
  let start = prefix.length;
  while (isIdentChar(prefix[start - 1])) start--;
  return start;
}

function completions(prefix, entries) {
  const wordStart = currentWordStart(prefix);
  return phraseEntries(entries).map(entry => {
    const phraseStart = typedPhraseStart(prefix, entry.phrase);
    return {
      label: entry.phrase,
      description: entry.symbol ? `${entry.category} (${entry.symbol})` : entry.category,
      markdown: describeEntry(entry),
      start: phraseStart === null ? wordStart : Math.min(phraseStart, wordStart),
      filterText: [entry.phrase, stripAccents(entry.phrase), ...(entry.keywords || [])].join(' '),
    };
  });
}

module.exports = { completions, hoverAt, insideStringOrComment, maskLine };
