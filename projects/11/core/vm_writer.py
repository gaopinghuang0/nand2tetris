
class VMWriter(object):
    """Write vm code"""
    def __init__(self, outfile):
        self.fp = outfile

    def write_push(self, segment, index):
        """
        Write a VM push command
        @param segment: constant | argument | static | this ...
        @param index: int
        """
        self.fp.write('push {} {}\n'.format(segment, index))

    def write_pop(self, segment, index):
        """
        Write a VM pop command
        @param segment: constant | argument | static | this ...
        @param index: int
        """
        self.fp.write('pop {} {}\n'.format(segment, index))

    def write_arithmetic(self, command):
        """
        Write a VM arithmetic-logical command
        @param command: add, sub, neg, eq, gt, lt, and, or, not
        """
        self.fp.write('{}\n'.format(command))

    def write_label(self, label):
        self.fp.write('label {}\n'.format(label))

    def write_goto(self, label):
        """
        Write a VM goto command
        """
        self.fp.write('goto {}\n'.format(label))

    def write_if(self, label):
        """
        Write a VM if-goto command
        """
        self.fp.write('if-goto {}\n'.format(label))

    def write_call(self, name, n_args):
        self.fp.write('call {} {}\n'.format(name, n_args))

    def write_function(self, name, n_locals):
        """
        Define a function
        @param n_locals: # of local variables, not # of params
        """
        self.fp.write('function {} {}\n'.format(name, n_locals))

    def write_return(self):
        self.fp.write('return\n')
