# Abarico, Michelle - 220017
# Caryl Chan - 221503
# Muli, Lamberlain -

import os

# Single-character tokens
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

# Keywords
KEYWORDS = {
    'PRINT': 'Print',
    'IF': 'If',
    'ELSE': 'Else',
    'ENDIF': 'Endif',
    'SQRT': 'Sqrt',
    'AND': 'And',
    'OR': 'Or',
    'NOT': 'Not'
}

class Scanner:
    def __init__(self, text):
        self.text = text
        self.i = 0
        self.length = len(text)
        self.line = 1

    def getlinenum(self):
        return self.line

    def gettoken(self):
        text = self.text
        length = self.length
        i = self.i

        # Skip whitespace and count newlines
        while i < length and text[i].isspace():
            if text[i] == '\n':
                self.line += 1
            i += 1
        if i >= length:
            self.i = i
            return ('EndofFile', '')

        c = text[i]

        # Comments //
        if c == '/' and i + 1 < length and text[i+1] == '/':
            i += 2
            while i < length and text[i] != '\n':
                i += 1
            self.i = i
            return self.gettoken()

        # Strings
        if c == '"':
            i += 1
            start = i
            while i < length and text[i] != '"':
                if text[i] == '\n':
                    self.i = i
                    return ('LexicalError', 'Unterminated string')
                i += 1
            if i >= length:
                self.i = i
                return ('LexicalError', 'Unterminated string')
            lex = text[start-1:i+1]
            i += 1
            self.i = i
            return ('String', lex)

        # Identifiers / Keywords
        if c.isalpha() or c == '_':
            start = i
            i += 1
            while i < length and (text[i].isalnum() or text[i] == '_'):
                i += 1
            lex = text[start:i]
            self.i = i
            if lex in KEYWORDS:
                return (KEYWORDS[lex], lex)
            return ('Identifier', lex)

        # FSM for NUMBERS
        if c.isdigit():
            start = i
            state = "INT"     # INT → FLOAT → EXP → EXPDIG
            i += 1

            while True:
                if state == "INT":
                    if i < length and text[i].isdigit():
                        i += 1
                    elif i < length and text[i] == '.':
                        # dot must be followed by digit
                        if i + 1 < length and text[i+1].isdigit():
                            i += 2
                            state = "FLOAT"
                        else:
                            # dot without digits → ERROR, skip only dot
                            self.i = i + 1
                            return ('LexicalError', 'Invalid number format')
                    elif i < length and text[i] in 'eE':
                        state = "EXP"
                        i += 1
                    else:
                        break  # number ends cleanly

                elif state == "FLOAT":
                    if i < length and text[i].isdigit():
                        i += 1
                    elif i < length and text[i] in 'eE':
                        state = "EXP"
                        i += 1
                    else:
                        break

                elif state == "EXP":
                    # optional sign
                    if i < length and text[i] in '+-':
                        # next must be digit
                        if i + 1 < length and text[i+1].isdigit():
                            i += 2
                            state = "EXPDIG"
                        else:
                            self.i = i + 2
                            return ('LexicalError', 'Invalid number format')
                    elif i < length and text[i].isdigit():
                        i += 1
                        state = "EXPDIG"
                    else:
                        self.i = i + 1
                        return ('LexicalError', 'Invalid number format')

                elif state == "EXPDIG":
                    if i < length and text[i].isdigit():
                        i += 1
                    else:
                        break

            end = i

            # If a letter immediately follows → NUMBER then IDENTIFIER
            if i < length and (text[i].isalpha() or text[i] == '_'):
                lex = text[start:end]
                self.i = end
                return ('Number', lex)

            # Valid FINAL number
            lex = text[start:end]
            self.i = end
            return ('Number', lex)


        # Two-character tokens
        two = text[i:i+2]
        if two == ':=':
            self.i = i + 2
            return ('Assign', ':=')
        if two == '<=':
            self.i = i + 2
            return ('LTEqual', '<=')
        if two == '>=':
            self.i = i + 2
            return ('GTEqual', '>=')
        if two == '!=':
            self.i = i + 2
            return ('NotEqual', '!=')
        if two == '**':
            self.i = i + 2
            return ('Raise', '**')

        # Single-character tokens
        if c in TOKEN_SINGLE:
            self.i = i + 1
            return (TOKEN_SINGLE[c], c)

        # Unknown character
        self.i = i + 1
        return ('LexicalError', 'Illegal character/character sequence')


# File handling
def tokenize_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return Scanner(text)

def write_scan_output(scanner, outpath):
    with open(outpath, 'w', encoding='utf-8') as f:
        while True:
            ttype, lex = scanner.gettoken()
            if ttype == 'EndofFile':
                f.write('EndofFile\n')
                break
            elif ttype == 'LexicalError':
                f.write(f'Lexical Error: {lex}\n')
                f.write('Error\n')
            else:
                f.write(f'{ttype}\t{lex}\n')


def find_input_files(root='samples'):
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
        scanner = tokenize_file(infile)
        dirname, fname = os.path.split(infile)
        outname = fname.replace('input', 'output_scan')
        outpath = os.path.join(dirname, outname)
        write_scan_output(scanner, outpath)

if __name__ == '__main__':
    main()
