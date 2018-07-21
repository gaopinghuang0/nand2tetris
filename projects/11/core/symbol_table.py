
class SymbolTable(object):
    """Maintain a class-scope and subroutine-scope symbol table"""
    def __init__(self):
        self.class_table = {}       
        self.class_indice = {'field': 0, 'static': 0}
        # subroutine-scope table should be reset every time
        self.subroutine_table = {}

    def define(self, name, _type, kind):
        """Define class-scope or subroutine-scope symbol table.
        @param _type: int | char | boolean | className
        @param kind: static | field | argument | local
        """
        if kind in ['static', 'field']:
            table, indice = self.class_table, self.class_indice
        else:
            table, indice = self.subroutine_table, self.subroutine_indice

        if name in table:
            raise KeyError('{} is already defined'.format(name))
        table[name] = (_type, kind, indice[kind])
        indice[kind] += 1

    def reset_subroutine_table(self, is_method, class_name):
        """reset subroutine-scope table.
        Note that for method-type subroutine, the first argument must be `this`
        """
        self.subroutine_table = {}
        self.subroutine_indice = {'argument': 0, 'local': 0}
        if is_method:
            self.define('this', class_name, 'argument') 

    def is_var(self, name):
        return name in self.subroutine_table or name in self.class_table

    def _get_var(self, name):
        "get variable by name, starting from subroutine-scope to class-scope"
        if name in self.subroutine_table:
            return self.subroutine_table[name]
        if name in self.class_table:
            return self.class_table[name]
        raise KeyError('{} is undefined'.format(name))

    def get_type(self, name):
        return self._get_var(name)[0]

    def get_kind(self, name):
        return self._get_var(name)[1]

    def get_index(self, name):
        return self._get_var(name)[2]
