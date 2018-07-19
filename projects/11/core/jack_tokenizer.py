import re

DEBUG = False
def dbg_print(*kw):
    if DEBUG:
        print(*kw)

KEYWORDS = set(['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this',
            'let', 'do', 'if', 'else', 'while', 'return'])

class Lexer(object):
    def __init__(self, inpt):
        self.chars = [ch for line in inpt for ch in line]
        self.size = len(self.chars)
        self.tokens = []
        self.idx = 0
        self.run()

    def run(self):
        dbg_print(self.size)
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if self.is_whitespace(ch):
                self.idx += 1
            elif ch == '"':
                self.idx += 1
                self.read_string()
            elif self.is_digit(ch):
                self.read_int()
            elif re.match('[a-zA-Z_]', ch):  # do not start with digit
                self.read_identifier()
            elif ch == '/':
                _next_ch = self.peek_next()
                if _next_ch == '*':
                    self.idx += 2
                    self.read_block_comment()
                elif _next_ch == '/':
                    self.idx += 2
                    self.read_line_comment()
                else:
                    self.tokens.append({'text': '/', 'type': 'symbol'})
                    self.idx += 1
            elif ch in '()[]{}.,;+-*&|<>=~':
                self.tokens.append({'text': ch, 'type': 'symbol'})
                self.idx += 1

    def is_digit(self, ch):
        return re.match('[0-9]', ch)

    def is_whitespace(self, ch):
        return re.match('\s', ch)

    def get_curr_ch(self):
        return self.chars[self.idx]

    def peek_next(self):
        if self.idx + 1 < self.size:
            return self.chars[self.idx+1]
        return False

    def get_tokens(self):
        # return tokens after completely tokenizing
        return self.tokens

    def read_int(self):
        dbg_print('read_int')
        text = ''
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if self.is_digit(ch):
                text += ch
                self.idx += 1
            elif self.is_whitespace(ch):
                self.idx += 1
                break
            elif ch in '})],;+-*/&|<>=':
                break
            else:
                raise ValueError('digit should follow a whitespace or other valid symbol, but got '+text+ch)
        self.tokens.append({'text': text, 'type': 'integerConstant'})

    def read_string(self):
        dbg_print('read_string')
        text = ''
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if ch != '"':
                text += ch
                self.idx += 1
            else:
                self.idx += 1
                break
        self.tokens.append({'text': text, 'type': 'stringConstant'})

    def read_identifier(self):
        dbg_print('read_identifier')
        text = ''
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if re.match('\w', ch):
                text += ch
                self.idx += 1
            else:
                break
        if text in KEYWORDS:
            self.tokens.append({'text': text, 'type': 'keyword'})
        else:
            self.tokens.append({'text': text, 'type': 'identifier'})

    def read_block_comment(self):
        dbg_print('read_block_comment')
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if ch == '*':
                if self.peek_next() == '/':
                    self.idx += 2
                    break
            self.idx += 1

    def read_line_comment(self):
        dbg_print('read_line_comment')
        while self.idx < self.size:
            ch = self.get_curr_ch()
            if ch == '\n':
                self.idx += 1
                break
            self.idx += 1

# tokenize a single file stream
class JackTokenizer(object):
    def __init__(self, inpt):
        lexer = Lexer(inpt)
        self.tokens = lexer.get_tokens()
        self.index = -1
        self.size = len(self.tokens)
        self.curr_token = None
        self.escape_dict = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

    def has_more_tokens(self):
        return self.index + 1 < self.size

    def advance(self, step=1):
        # advance to the next token from the input and make it the current token
        self.index += step
        self._token = self.tokens[self.index]
        self.curr_token = self._token['text']

    def move_back(self):
        # the reverse of advance
        self.advance(-1)

    def peek_next(self):
        # peek the text of next token
        return self.tokens[self.index+1]['text'] if self.has_more_tokens() else None

    def token_type(self):
        # return the type of the current token
        # KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        return self._token['type']

    def escape(self, token):
        return self.escape_dict[token] if token in self.escape_dict else token