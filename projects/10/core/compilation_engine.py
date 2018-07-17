import re


DEBUG = False
def dbg_print(*kw):
    if DEBUG:
        print(*kw)


# a recursive top-down parser for Jack
class CompilationEngine(object):
    def __init__(self, tokenizer, outfile):
        self.tokenizer = tokenizer
        self.fp = outfile
        self.indent = 0  # indent spaces

    #### Below are some internal helper functions ####

    def _start_block(self, block_name):
        self.fp.write('{indent}<{name}>\n'.format(
            indent=self.indent*' ',
            name=block_name))
        self.indent += 2

    def _end_block(self, block_name):
        self.indent -= 2
        self.fp.write('{indent}</{name}>\n'.format(
            indent=self.indent*' ',
            name=block_name))

    def _write_curr_token(self):
        self.fp.write('{indent}<{type}> {token} </{type}>\n'.format(
            indent=self.indent*' ',
            token=self.tokenizer.curr_token,
            type=self.tokenizer.token_type()
        ))

    # check the next token with the given type and token_text
    # if matches, consume it and write to output
    def _consume(self, _type, token=None):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if _type == self.tokenizer.token_type():
                if token is None or token == self.tokenizer.curr_token:
                    self._write_curr_token()
                else:
                    raise ValueError('token text does not match, expect {}, got {}'.format(
                                    token, self.tokenizer.curr_token))
            else:
                raise ValueError('token type does not match, expect {}, got {}'.format(
                                 _type, self.tokenizer.token_type()))
        else:
            raise ValueError('should have more tokens')

    def _compile_type(self):
        token = self.tokenizer.peek_next()
        if token in ['int', 'char', 'boolean']:
            self._consume('keyword')
        else:
            self._consume('identifier')  # className

    def _compile_class_name(self):
        self._consume('identifier')

    def _compile_var_name(self):
        self._consume('identifier')

    def _compile_subroutine_name(self):
        self._consume('identifier')

    def _compile_subroutine_body(self):
        pass

    #### Below are public APIs ####

    def compile_class(self):
        self._start_block('class')
        self._consume('keyword', 'class')
        self._compile_class_name()
        self._consume('symbol', '{')
        # 0 or more classVarDec
        while self.compile_class_var_dec():
            pass
        # 0 or more subroutineDec
        while self.compile_subroutine():
            pass
        # self._consume('symbol', '}')  # TODO: uncomment it
        self._end_block('class')

    def compile_class_var_dec(self):
        token = self.tokenizer.peek_next()
        if token not in ['static', 'field']:
            # no classVarDec, just skip
            return False
        self._start_block('classVarDec')
        self._consume('keyword')  # 'static' or 'field'
        self._compile_type()
        self._compile_var_name()  # varName
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume('symbol', ',')
                self._compile_var_name()
            else:
                break
        self._consume('symbol', ';')
        self._end_block('classVarDec')
        return True

    def compile_subroutine(self):
        token = self.tokenizer.peek_next()
        if token not in ['constructor', 'function', 'method']:
            # no subroutineDec, just skip
            return False
        self._start_block('subroutineDec')
        self._consume('keyword')  # 'constructor', 'function', 'method'
        # (void | type)
        token = self.tokenizer.peek_next()
        if token == 'void':
            self._consume('keyword', 'void')
        else:
            self._compile_type()

        self._compile_subroutine_name()
        self._consume('symbol', '(')
        self.compile_parameter_list()
        # self._consume('symbol', ')')

        self._end_block('subroutineDec')
        return True

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

