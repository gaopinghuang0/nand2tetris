# Modified from project 10: compilation_engine.py
# Since 7/21/2018

from .symbol_table import SymbolTable

# a recursive top-down parser for Jack
class CompilationEngine(object):
    def __init__(self, tokenizer, vm_writer):
        self.tokenizer = tokenizer
        self.vm_writer = vm_writer
        self.indent = 0  # indent spaces
        self.symtable = SymbolTable()
        self.class_name = None
        self.label_indice = {'while': 0, 'if': 0}


    #### Below are some internal helper functions ####

    def _start_block(self, block_name):
        # self.fp.write('{indent}<{name}>\n'.format(
        #     indent=self.indent*' ',
        #     name=block_name))
        # self.indent += 2
        pass

    def _end_block(self, block_name):
        # self.indent -= 2
        # self.fp.write('{indent}</{name}>\n'.format(
        #     indent=self.indent*' ',
        #     name=block_name))
        pass

    def _write_curr_token(self):
        # self.fp.write('{indent}<{type}> {token} </{type}>\n'.format(
        #     indent=self.indent*' ',
        #     token=self.tokenizer.escape(self.tokenizer.curr_token),
        #     type=self.tokenizer.token_type()
        # ))
        pass

    def _write_curr_identifier(self, usage):
        "use special format to represent identifier"
        name = self.tokenizer.curr_token
        # I intentionly use this xml format although it is invalid,
        # because it will be highlighted automatically by the text editor
        # self.fp.write('{indent}<{usage},{type},{kind},{index}> {token} </>\n'.format(
        #     indent=self.indent*' ',
        #     token=name,
        #     type=self.symtable.get_type(name),
        #     kind=self.symtable.get_kind(name),
        #     index=self.symtable.get_index(name),
        #     usage=usage
        # ))
        pass

    # check the next token with the given type and token_text
    # if matches, consume it and write to output
    def _consume(self, _type, token=None):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if _type == self.tokenizer.token_type():
                if token is None or token == self.tokenizer.curr_token:
                    self._write_curr_token()
                    return self.tokenizer.curr_token
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
            return token
        else:
            return self._consume('identifier')  # className

    def _compile_class_name(self):
        return self._consume('identifier')

    def _compile_var_name(self, _type=None, kind=None):
        "if _type and kind are given, define new var, or else use defined var."
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            name = self.tokenizer.curr_token
            if _type is not None:   # define new var
                self.symtable.define(name, _type, kind)
                self._write_curr_identifier('define')
            else:
                self._write_curr_identifier('use')
            return name
        else:
            raise ValueError('should have more tokens')

    def _compile_subroutine_name(self):
        return self._consume('identifier')

    def _compile_subroutine_body(self, func_kind):
        self._start_block('subroutineBody')
        self._consume_symbol('{')
        total_locals = 0
        while True:
            n_locals = self.compile_var_dec()
            total_locals += n_locals
            if not n_locals:
                break

        self.vm_writer.write_function(self.func_name, total_locals)
        if func_kind == 'method':
            # anchor `this` first
            self._write_push_by_name('this')
            self.vm_writer.write_pop('pointer', 0)
        elif func_kind == 'constructor':
            # alloc memory for `field vars`
            n_field_vars = self.symtable.get_var_count('field')
            self.vm_writer.write_push('constant', n_field_vars)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)  # again, `this` is not `argument 0` within constructor

        self.compile_statements()
        self._consume_symbol('}')
        self._end_block('subroutineBody')
        return total_locals

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
        # the first token could be subroutineName, className, or varName
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            name = self.tokenizer.curr_token
            next_token = self.tokenizer.peek_next()
            self.tokenizer.move_back()
            n_args = 0
            if next_token == '(':
                # method call without obj or class name, we need to prepend class name
                # and also push this onto stack. However, some method call is within constructor
                # which has no argument this, thus we push pointer 0 onto stack
                n_args = 1
                func_name = self._compile_subroutine_name()
                self.vm_writer.write_push('pointer', 0)
                func_name = '{}.{}'.format(self.class_name, func_name)
            elif next_token == '.':
                if self.symtable.is_var(name):
                    # obj.method call, need to replace obj with class name, 
                    # and push obj as the first argument, increment the n_args
                    n_args = 1
                    obj_name = self._compile_var_name()
                    class_name = self.symtable.get_type(obj_name)
                    self._write_push_by_name(obj_name)
                else:
                    # class.function
                    class_name = self._compile_class_name()
                self._consume_symbol('.')
                func_name = self._compile_subroutine_name()
                func_name = '{}.{}'.format(class_name, func_name)
            else:
                raise ValueError('Unknown symbol')

            self._consume_symbol('(')
            n_args += self.compile_expression_list()
            self._consume_symbol(')')
            self.vm_writer.write_call(func_name, n_args)

    def _is_op(self, token):
        # check if token is operator
        return token in '+-*/&|<>='

    def _translate_op(self, op):
        # does not include '*' and '/'
        lookup = {'+': 'add', '-': 'sub', '=': 'eq', '>': 'gt', '<': 'lt', '&': 'and', '|': 'or'}
        return lookup[op]

    def _gen_while_label(self):
        curr_idx = self.label_indice['while']
        self.label_indice['while'] += 1
        return 'WHILE_EXP{}'.format(curr_idx), 'WHILE_END{}'.format(curr_idx)

    def _gen_if_label(self):
        curr_idx = self.label_indice['if']
        self.label_indice['if'] += 1
        return 'IF_FALSE{}'.format(curr_idx), 'IF_END{}'.format(curr_idx)

    def _write_push_by_name(self, name):
        kind = self.symtable.get_kind(name)
        if kind == 'field':
            kind = 'this'  # use `this` instead
        self.vm_writer.write_push(kind, self.symtable.get_index(name))

    def _write_pop_by_name(self, name):
        kind = self.symtable.get_kind(name)
        if kind == 'field':
            kind = 'this'  # use `this` instead
        self.vm_writer.write_pop(kind, self.symtable.get_index(name))

    def _compile_string(self, token):
        # call String.new and appendChar for each char
        n = len(token)
        self.vm_writer.write_push('constant', n)
        self.vm_writer.write_call('String.new', 1)
        for c in token:
            self.vm_writer.write_push('constant', ord(c))
            self.vm_writer.write_call('String.appendChar', 2)

    def _compile_array_on_the_right(self):
        "compile arr[i] as right-value; arr[i] as left-value is compiled in compile_let()"
        name = self._compile_var_name()
        # push the base addr of arr onto the stack
        self._write_push_by_name(name)
        self._consume_symbol('[')
        self.compile_expression()
        self._consume_symbol(']')
        # add the base addr with expression value to get the addr of the array element
        self.vm_writer.write_arithmetic('add')
        # anchor the addr to THAT
        self.vm_writer.write_pop('pointer', 1)
        # push the value of addr (i.e., the array element) onto the stack
        self.vm_writer.write_push('that', 0)


    #### Below are public APIs ####

    def compile_class(self):
        self._start_block('class')
        self._consume_keyword('class')
        self.class_name = self._compile_class_name()
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
        kind = self.tokenizer.peek_next()
        if kind not in ['static', 'field']:
            # no classVarDec, just skip
            return False
        self._start_block('classVarDec')
        self._consume_keyword()  # 'static' or 'field'
        _type = self._compile_type()
        self._compile_var_name(_type, kind)  # varName
        # 0 or more varName
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self._compile_var_name(_type, kind)
            else:
                break
        self._consume_symbol(';')
        self._end_block('classVarDec')
        return True

    def compile_subroutine(self):
        func_kind = self.tokenizer.peek_next()
        if func_kind not in ['constructor', 'function', 'method']:
            # no subroutineDec, just skip
            return False
        is_method = (func_kind == 'method')
        self.symtable.reset_subroutine_table(is_method, self.class_name)

        self._start_block('subroutineDec')
        self._consume_keyword()  # 'constructor', 'function', 'method'
        # (void | type)
        token = self.tokenizer.peek_next()
        if token == 'void':
            self._consume_keyword('void')
        else:
            self._compile_type()

        func_name = self._compile_subroutine_name()
        self.func_name = '{}.{}'.format(self.class_name, func_name)
        self._consume_symbol('(')
        self.compile_parameter_list()
        self._consume_symbol(')')
        self._compile_subroutine_body(func_kind)
        self._end_block('subroutineDec')
        return True

    def compile_parameter_list(self):
        self._start_block('parameterList')
        token = self.tokenizer.peek_next()
        if token == ')':   # no param list, skip
            self._end_block('parameterList')
            return 0
        _type = self._compile_type()
        self._compile_var_name(_type, 'argument')
        n_args = 1
        # 0 or more (type, varName)
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                _type = self._compile_type()
                self._compile_var_name(_type, 'argument')
                n_args += 1
            else:
                break
        self._end_block('parameterList')
        return n_args

    def compile_var_dec(self):
        token = self.tokenizer.peek_next()
        if token != 'var':   # no var dec, skip
            return 0
        self._start_block('varDec')
        self._consume_keyword('var')
        _type = self._compile_type()
        self._compile_var_name(_type, 'local')
        n_locals = 1
        # 0 or more varName
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self._compile_var_name(_type, 'local')
                n_locals += 1
            else:
                break
        self._consume_symbol(';')
        self._end_block('varDec')
        return n_locals

    def compile_statements(self):
        self._start_block('statements')
        while self._compile_statement():
            pass
        self._end_block('statements')

    def compile_do(self):
        self._start_block('doStatement')
        self._consume_keyword('do')
        self._compile_subroutine_call()
        # for do statement, we need to pop out the return value from the stack
        # since its value is not used
        self.vm_writer.write_pop('temp', 0)
        self._consume_symbol(';')
        self._end_block('doStatement')
        
    def compile_let(self):
        self._start_block('letStatement')
        self._consume_keyword('let')
        name = self._compile_var_name()
        # ('[' expression ']')?
        token = self.tokenizer.peek_next()
        is_array = False
        if token == '[':  # array left bracket
            is_array = True
            # push the base addr of arr onto the stack
            self._write_push_by_name(name)
            self._consume_symbol('[')
            self.compile_expression()
            self._consume_symbol(']')
            # add the base addr with expression value to get the addr of the array element
            self.vm_writer.write_arithmetic('add')

        self._consume_symbol('=')
        self.compile_expression()
        if is_array:
            # save the value of expression to temp 0
            self.vm_writer.write_pop('temp', 0)
            # save the addr of array element into pointer 1 
            self.vm_writer.write_pop('pointer', 1)
            # push the value of expression from temp 0 onto the stack
            self.vm_writer.write_push('temp', 0)
            # save value to array element
            self.vm_writer.write_pop('that', 0)
        else:
            # save value to var
            self._write_pop_by_name(name)
        self._consume_symbol(';')
        self._end_block('letStatement')

    def compile_while(self):
        self._start_block('whileStatement')
        self._consume_keyword('while')
        label_start, label_end = self._gen_while_label()
        self.vm_writer.write_label(label_start)
        self._consume_symbol('(')
        self.compile_expression()
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(label_end)
        self._consume_symbol(')')
        self._consume_symbol('{')
        self.compile_statements()
        self.vm_writer.write_goto(label_start)
        self.vm_writer.write_label(label_end)
        self._consume_symbol('}')
        self._end_block('whileStatement')

    def compile_return(self):
        self._start_block('returnStatement')
        self._consume_keyword('return')
        token = self.tokenizer.peek_next()
        if token != ';':  # has return expression
            self.compile_expression()
        else:  # no return value, still push arbitrary value onto the stack
            self.vm_writer.write_push('constant', 0)
        self.vm_writer.write_return()
        self._consume_symbol(';')
        self._end_block('returnStatement')
        
    def compile_if(self):
        # based on `images/compile-if-statement.png`
        self._start_block('ifStatement')
        label_1, label_2 = self._gen_if_label()
        self._consume_keyword('if')
        self._consume_symbol('(')
        self.compile_expression()
        self._consume_symbol(')')
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(label_1)
        self._consume_symbol('{')
        self.compile_statements()
        self._consume_symbol('}')
        self.vm_writer.write_goto(label_2)
        token = self.tokenizer.peek_next()
        self.vm_writer.write_label(label_1)
        if token == 'else':
            self._consume_keyword('else')
            self._consume_symbol('{')
            self.compile_statements()
            self._consume_symbol('}')
        self.vm_writer.write_label(label_2)
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
                if token == '*':
                    self.vm_writer.write_call('Math.multiply', 2)
                elif token == '/':
                    self.vm_writer.write_call('Math.divide', 2)
                else:
                    self.vm_writer.write_arithmetic(self._translate_op(token))
            else:
                break
        self._end_block('expression')

    def compile_term(self):
        self._start_block('term')
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token = self.tokenizer.curr_token
            token_type = self.tokenizer.token_type()
            if token_type == 'integerConstant':
                self.vm_writer.write_push('constant', token)
            elif token_type == 'stringConstant':
                self._compile_string(token)
            elif token in ['true', 'false', 'null', 'this']:  # keywordConstant
                if token == 'this':
                    self._write_curr_identifier('use')
                    # `this` may appear in constructor, which means we have to use pointer 0
                    # instead of argument 0
                    self.vm_writer.write_push('pointer', 0)
                elif token == 'true':
                    # use -1 as true, could obtain by 0 followed by not, or 1 followed by neg
                    self.vm_writer.write_push('constant', 0)
                    self.vm_writer.write_arithmetic('not')
                elif token in ['false', 'null']:
                    self.vm_writer.write_push('constant', 0)
                else:
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
                self.vm_writer.write_arithmetic('neg' if token == '-' else 'not')
            else:
                assert token_type == 'identifier'  # the curr token type must be identifier to meet the remaining rules
                next_token = self.tokenizer.peek_next()
                self.tokenizer.move_back()
                if next_token == '[':  # varName '[' expression ']', array
                    self._compile_array_on_the_right()
                elif next_token in '(.':  # subroutineCall
                    self._compile_subroutine_call()
                else:  # varName
                    name = self._compile_var_name()
                    self._write_push_by_name(name)

        self._end_block('term')

    def compile_expression_list(self):
        self._start_block('expressionList')
        token = self.tokenizer.peek_next()
        if token == ')':   # no expression list, skip
            self._end_block('expressionList')
            return 0
        self.compile_expression()
        n_args = 1
        # 0 or more (',' expression)
        while True:
            token = self.tokenizer.peek_next()
            if token == ',':
                self._consume_symbol(',')
                self.compile_expression()
                n_args += 1
            else:
                break
        self._end_block('expressionList')
        return n_args

