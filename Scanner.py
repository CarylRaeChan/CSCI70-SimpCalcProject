# Abarico, Michelle -
# Caryl Chan - 221503
# Muli, Lamberlain - 


import os
import re

# Token types
TOKEN_SINGLE = {
    ';': 'Semicolon',
    ':': 'Colon',
    ',': 'Comma',
    '(': 'LeftParen',
    ')': 'RightParen',
    '+': 'Plus',
    '-': 'Minus',
    '*': 'Multiply',
    '/': 'Divide',
    '<': 'LessThan',
    '=': 'Equal',
    '>': 'GreaterThan'
}

KEYWORDS = {'PRINT', 'IF', 'ELSE', 'ENDIF', 'SQRT', 'AND', 'OR', 'NOT'}


def tokenize_text(text):
    tokens = []
    i = 0
    length = len(text)

    def add(ttype, lexeme):
        tokens.append((ttype, lexeme))

    while i < length:
        c = text[i]

        # Whitespace
        if c.isspace():
            i += 1
            continue

        # Comments start with // to end of line
        if c == '/' and i + 1 < length and text[i+1] == '/':
            i += 2
            while i < length and text[i] != '\n':
                i += 1
            continue

        # Strings: double-quoted, cannot span lines
        if c == '"':
            i += 1
            start = i
            while i < length and text[i] != '"':
                if text[i] == '\n': 
                    return [('LexicalError', 'Unterminated string literal')]
                i += 1
            if i >= length: 
                return [('LexicalError', 'Unterminated string literal')]
            lex = text[start:i] # exclude quotes
            add('String', lex) 
            i += 1
            continue

        # Identifier or keyword: letter or underscore then letters/digits/underscores
        if (c.isalpha() or c == '_'):
            start = i
            i += 1
            while i < length and (text[i].isalnum() or text[i] == '_'):
                i += 1
            lex = text[start:i]
            if lex.upper() in KEYWORDS:
                add(lex.upper(), lex)
            else:
                add('Identifier', lex)
            continue

        # Number: integer, float, exponent
        if c.isdigit() or (c == '.' and i+1 < length and text[i+1].isdigit()):
            start = i
            # integer/decimal part
            while i < length and text[i].isdigit():
                i += 1
            if i < length and text[i] == '.':
                i += 1
                while i < length and text[i].isdigit():
                    i += 1
            # exponent
            if i < length and text[i] in 'eE':
                i += 1
                if i < length and text[i] in '+-':
                    i += 1
                if i >= length or not text[i].isdigit():
                    return [('LexicalError', 'Malformed number exponent')]
                while i < length and text[i].isdigit():
                    i += 1
            lex = text[start:i]
            add('Number', lex)
            continue

        # Two-character tokens: :=, <=, >=, !=, **
        two = text[i:i+2]
        if two == ':=':
            add('Assign', ':=')
            i += 2
            continue
        if two == '<=':
            add('LTEqual', '<=')
            i += 2
            continue
        if two == '>=':
            add('GTEqual', '>=')
            i += 2
            continue
        if two == '!=':
            add('NotEqual', '!=')
            i += 2
            continue
        if two == '**':
            add('Raise', '**')
            i += 2
            continue

        # Single character tokens
        if c in TOKEN_SINGLE:
            add(TOKEN_SINGLE[c], c)
            i += 1
            continue

        # Unknown character
        return [('LexicalError', f'Lexical Error reading character "{c}"')]

    add('EndofFile', '')
    return tokens


def tokenize_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return tokenize_text(text)


def write_scan_output(tokens, outpath):
    with open(outpath, 'w', encoding='utf-8') as f:
        for ttype, lex in tokens:
            if ttype == 'EndofFile':
                f.write('EndofFile\n')
            elif ttype == 'LexicalError':
                f.write(lex + '\n')
            else:
                f.write(f"{ttype}\t{lex}\n")


def find_input_files(root='samples'):
    """Return list of input files in `root` directory that contain 'input' and end with .txt."""
    files = []
    if not os.path.isdir(root):
        return files
    for fname in os.listdir(root):
        if 'input' in fname and fname.endswith('.txt'):
            files.append(os.path.join(root, fname))
    return sorted(files)


def main():
    inputs = find_input_files('samples')
    if not inputs:
        print('No input files found in samples/.')
        return

    for infile in inputs:
        tokens = tokenize_file(infile)
        # construct scan output filename: replace 'input' with 'output_scan'
        dirname, fname = os.path.split(infile)
        outname = fname.replace('input', 'output_scan')
        outpath = os.path.join(dirname, outname)
        write_scan_output(tokens, outpath)


if __name__ == '__main__':
    main()