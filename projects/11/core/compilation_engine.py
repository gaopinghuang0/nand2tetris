
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
            token=self.tokenizer.escape(self.tokenizer.curr_token),
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

    def _consume_symbol(self, token=None):
        self._consume('symbol', token)

    def _consume_keyword(self, token=None):
        self._consume('keyword', token)

    def _compile_type(self):
        token = self.tokenizer.peek_next()
        if token in ['int', 'char', 'boolean']:
            self._consume_keyword()
        else:
            self._consume('identifier')  # className

    def _compile_class_name(self):
        self._consume('identifier')

    def _compile_var_name(self):
        self._consume('identifier')

    def _compile_subroutine_name(self):
        self._consume('identifier')

    def _compile_subroutine_body(self):
        self._start_block('subroutineBody')
        self._consume_symbol('{')
        while self.compile_var_dec():
            pass
        self.compile_statements()
        self._consume_symbol('}')
        self._end_block('subroutineBody')

    def _compile_statement(self):
        token = self.tokenizer.peek_next()
        if token == 'let':
            self.compile_let()
        elif token == 'if':
            self.compile_if()
        elif token == 'while':
            self.compile_while()
        elif token == 'do':
            self.compile_do()
        elif token == 'return':
            self.compile_return()
        else:
            return False
        return True

    def _compile_subroutine_call(self):
        self._compile_subroutine_name()  # also could be className, varName
        token = self.tokenizer.peek_next()
        if token == '(':
            self._consume_symbol('(')
            self.compile_expression_list()
            self._consume_symbol(')')
        elif token == '.':
            self._consume_symbol('.')
            self._compile_subroutine_name()
            self._consume_symbol('(')
            self.compile_expression_list()
            self._consume_symbol(')')
        else:
            raise ValueError('Unknown symbol')

    def _is_op(self, token):
        # check if token is operator
        return token in '+-*/&|<>='


    #### Below are public APIs ####

    def compile_class(self):
        self._start_block('class')
        self._consume_keyword('class')
        self._compile_class_name()
        self._consume_symbol('{')
        # 0 or more classVarDec
        while self.compile_class_var_dec():
            pass
        # 0 or more subroutineDec
        while self.compile_subroutine():
            pass
        self._consume_symbol('}')
        self._end_block('class')

    def compile_class_var_dec(self):
        token = self.tokenizer.peek_next()
        if token not in ['static', 'field']:
            # no classVarDec, just skip
            return False
        self._start_block('classVarDec')
        self._consume_keyword()  # 'static' or 'field'
        self._compile_type()
        self._compile_var_name()  # varName
        # 0 or more varName
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self._compile_var_name()
            else:
                break
        self._consume_symbol(';')
        self._end_block('classVarDec')
        return True

    def compile_subroutine(self):
        token = self.tokenizer.peek_next()
        if token not in ['constructor', 'function', 'method']:
            # no subroutineDec, just skip
            return False
        self._start_block('subroutineDec')
        self._consume_keyword()  # 'constructor', 'function', 'method'
        # (void | type)
        token = self.tokenizer.peek_next()
        if token == 'void':
            self._consume_keyword('void')
        else:
            self._compile_type()

        self._compile_subroutine_name()
        self._consume_symbol('(')
        self.compile_parameter_list()
        self._consume_symbol(')')
        self._compile_subroutine_body()
        self._end_block('subroutineDec')
        return True

    def compile_parameter_list(self):
        self._start_block('parameterList')
        token = self.tokenizer.peek_next()
        if token == ')':   # no param list, skip
            self._end_block('parameterList')
            return
        self._compile_type()
        self._compile_var_name()
        # 0 or more (type, varName)
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self._compile_type()
                self._compile_var_name()
            else:
                break
        self._end_block('parameterList')

    def compile_var_dec(self):
        token = self.tokenizer.peek_next()
        if token != 'var':   # no var dec, skip
            return False
        self._start_block('varDec')
        self._consume_keyword('var')
        self._compile_type()
        self._compile_var_name()
        # 0 or more varName
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self._compile_var_name()
            else:
                break
        self._consume_symbol(';')
        self._end_block('varDec')
        return True

    def compile_statements(self):
        self._start_block('statements')
        while self._compile_statement():
            pass
        self._end_block('statements')

    def compile_do(self):
        self._start_block('doStatement')
        self._consume_keyword('do')
        self._compile_subroutine_call()
        self._consume_symbol(';')
        self._end_block('doStatement')
        
    def compile_let(self):
        self._start_block('letStatement')
        self._consume_keyword('let')
        self._compile_var_name()
        # ('[' expression ']')?
        token = self.tokenizer.peek_next()
        if token == '[':  # array left bracket
            self._consume_symbol('[')
            self.compile_expression()
            self._consume_symbol(']')
        self._consume_symbol('=')
        self.compile_expression()
        self._consume_symbol(';')
        self._end_block('letStatement')

    def compile_while(self):
        self._start_block('whileStatement')
        self._consume_keyword('while')
        self._consume_symbol('(')
        self.compile_expression()
        self._consume_symbol(')')
        self._consume_symbol('{')
        self.compile_statements()
        self._consume_symbol('}')
        self._end_block('whileStatement')

    def compile_return(self):
        self._start_block('returnStatement')
        self._consume_keyword('return')
        token = self.tokenizer.peek_next()
        if token != ';':  # has return expression
            self.compile_expression()
        self._consume_symbol(';')
        self._end_block('returnStatement')
        
    def compile_if(self):
        self._start_block('ifStatement')
        self._consume_keyword('if')
        self._consume_symbol('(')
        self.compile_expression()
        self._consume_symbol(')')
        self._consume_symbol('{')
        self.compile_statements()
        self._consume_symbol('}')
        token = self.tokenizer.peek_next()
        if token == 'else':
            self._consume_keyword('else')
            self._consume_symbol('{')
            self.compile_statements()
            self._consume_symbol('}')
        self._end_block('ifStatement')
        
    def compile_expression(self):
        self._start_block('expression')
        self.compile_term()
        # 0 or more (op term)
        while True:
            token = self.tokenizer.peek_next()
            if self._is_op(token):
                self._consume_symbol(token)
                self.compile_term()
            else:
                break
        self._end_block('expression')
        
    def compile_term(self):
        self._start_block('term')
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token = self.tokenizer.curr_token
            token_type = self.tokenizer.token_type()
            if token_type in ['integerConstant', 'stringConstant']:
                self._write_curr_token()
            elif token in ['true', 'false', 'null', 'this']:  # keywordConstant
                self._write_curr_token()
            elif token == '(':  # '(' expression ')'
                self.tokenizer.move_back()
                self._consume_symbol('(')
                self.compile_expression()
                self._consume_symbol(')')
            elif token in '-~':  # unary op
                self.tokenizer.move_back()
                self._consume_symbol(token)
                self.compile_term()
            else:
                assert token_type == 'identifier'  # the curr token type must be identifier to meet the remaining rules
                next_token = self.tokenizer.peek_next()
                if next_token == '[':  # varName '[' expression ']'
                    self.tokenizer.move_back()
                    self._compile_var_name()
                    self._consume_symbol('[')
                    self.compile_expression()
                    self._consume_symbol(']')
                elif next_token in '(.':  # subroutineCall
                    self.tokenizer.move_back()
                    self._compile_subroutine_call()
                else:  # varName
                    self.tokenizer.move_back()
                    self._compile_var_name()
        self._end_block('term')

    def compile_expression_list(self):
        self._start_block('expressionList')
        token = self.tokenizer.peek_next()
        if token == ')':   # no expression list, skip
            self._end_block('expressionList')
            return
        self.compile_expression()
        # 0 or more (',' expression)
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self.compile_expression()
            else:
                break
        self._end_block('expressionList')

