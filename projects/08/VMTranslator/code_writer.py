'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

from command import Command

R_R3 = R_THIS = 3
R_R4 = R_THAT = 4
R_R5 = R_TEMP = 5
R_R15 = R_COPY  = 15

class CodeWriter(object):
    def __init__(self, outfile):
        self.f = open(outfile, 'w')
        self.label_num = 0

    def write_cmd(self, *cmds):
        for cmd in cmds:
            self.f.write(cmd+'\n')

    def write_arithmetic(self, cmd):
        """
        cmd: add, sub, neg, eq, gt, lt, and, or, not
        """
        def pop_stack_twice():
            # more efficient way
            # since *SP is not updated except the end
            # D is the *(*SP-1), M is the *(*SP-2)
            self.write_cmd('@SP', 'A=M-1', 'D=M', 'A=A-1')
        def pop_stack_once():
            # note that *SP is not updated
            # D is the *(*SP-1)
            self.write_cmd('@SP', 'A=M-1', 'D=M')

        if cmd == 'add':
            # pop, pop, add, SP--
            pop_stack_twice()
            self.write_cmd('M=D+M')
        elif cmd == 'sub':
            pop_stack_twice()
            self.write_cmd('M=M-D')
        elif cmd == 'and':
            pop_stack_twice()
            self.write_cmd('M=M&D')
        elif cmd == 'or':
            pop_stack_twice()
            self.write_cmd('M=M|D')
        elif cmd == 'not':
            pop_stack_once()
            self.write_cmd('M=!D')
            return  # no need to dec_sp later
        elif cmd == 'neg':
            pop_stack_once()
            self.write_cmd('M=-D')
            return  # no need to dec_sp later
        elif cmd == 'eq':
            # pop, pop, eq, SP--
            pop_stack_twice()
            self._compare('JNE')
        elif cmd == 'lt':
            pop_stack_twice()
            self._compare('JLE')
        elif cmd == 'gt':
            pop_stack_twice()
            self._compare('JGE')
        else:
            raise ValueError('unknown arithmetic command')

        # update *SP only once
        self._dec_sp()

    def write_push_pop(self, cmd_type, segment, index):
        if cmd_type == Command.C_PUSH:
            self._do_push(segment, index)
        else:
            self._do_pop(segment, index)

    def write_comment(self, msg):
        self.write_cmd('// '+ msg)

    def close(self):
        self.f.close()
        print('file closed:', self.f.closed)

    def write_init(self):
        self.write_comment("bootstrap code")

    def write_label(self, label):
        self.write_cmd('(%s)'%label)

    def write_goto(self, label):
        self._a_command(label)
        self.write_cmd('0;JMP')

    def write_if(self, label):
        self._stack_to_D()
        self._a_command(label)
        self.write_cmd('D;JNE')  # jump if D != 0

    def write_call(self, func, n_args):
        pass

    def write_return(self):
        def _load_frame_to_D(index):
            self._access_mem('temp', 1)
            self.write_cmd('D=M')
            self._a_command(index)
            self.write_cmd('A=D-A', 'D=M')

        # frame = *LCL, frame is a temp var
        self._a_command('LCL')
        self.write_cmd('D=M')
        self._access_mem('temp', 1)
        self.write_cmd('M=D')
        # returnAddr = *(frame-5), returnAddr is a temp var
        _load_frame_to_D(5)
        self._access_mem('temp', 2)
        self.write_cmd('M=D')
        # *ARG = pop(), save return value for the caller
        self._do_pop('argument', 0)
        # SP = *ARG + 1, restore caller's SP
        self._a_command('ARG')
        self.write_cmd('D=M+1')
        self.write_cmd('@SP', 'M=D')
        # THAT = *(frame-1)
        _load_frame_to_D(1)
        self.write_cmd('@THAT', 'M=D')
        # THIS = *(frame-2)
        _load_frame_to_D(2)
        self.write_cmd('@THIS', 'M=D')
        # ARG = *(frame-3)
        _load_frame_to_D(3)
        self.write_cmd('@ARG', 'M=D')
        # LCL = *(frame-4)
        _load_frame_to_D(4)
        self.write_cmd('@LCL', 'M=D')
        # goto returnAddr, namely @returnAddr
        self._access_mem('temp', 2)
        self.write_cmd('A=M')
        self.write_cmd('0;JMP')

    def write_function(self, func, n_locals):
        self.write_cmd('(%s)'%func)
        self.write_cmd('@0', 'D=A')
        for i in range(n_locals):
            self._D_to_stack()   # push constant 0 to local var

    def _dec_sp(self):
        self.write_cmd('@SP', 'M=M-1')

    def _inc_sp(self):
        self.write_cmd('@SP', 'M=M+1')

    def _load_sp(self):
        self.write_cmd('@SP', 'A=M')

    def _new_label(self):
        self.label_num += 1
        return 'LABEL%d'%self.label_num

    def _save_to_reg(self, src, reg):
        self._access_reg(reg)
        self.write_cmd('M='+src)

    def _load_from_reg(self, reg):
        self._access_reg(reg)
        self.write_cmd('A=M')

    def _access_reg(self, reg):
        self._a_command('R%d'%reg)

    def _a_command(self, a):
        self.write_cmd('@%s'%a)

    def _get_seg(self, segment):
        if segment == 'local':
            seg = 'LCL'
        elif segment == 'argument':
            seg = 'ARG'
        else:
            seg = segment.upper()
        return seg

    def _D_to_stack(self):
        self._load_sp()
        self.write_cmd('M=D')
        self._inc_sp()

    def _stack_to_D(self):
        self._dec_sp()
        self._load_sp()
        self.write_cmd('D=M')

    def _access_mem(self, segment, index):
        if segment == 'static':
            self._a_command('FooStatic.'+index)
        else:
            base_reg = {"temp": R_TEMP, "pointer": R_THIS}[segment]
            self._access_reg(base_reg + int(index))

    def _do_push(self, segment, index):
        """Push the value from segment$index into stack."""
        if segment == 'constant':
            # push, SP++
            self.write_cmd('@'+index, 'D=A')
            self._D_to_stack()
        if segment in ['local', 'argument', 'this', 'that']:
            self._push_basic_seg(segment, index)
        elif segment in ['temp', 'pointer', 'static']:
            # *SP = *(TEMP+i), SP++
            # *SP = *(THIS/THAT), SP++
            # *SP = *(FooStatic.i), SP++
            self._access_mem(segment, index)
            self.write_cmd('D=M')
            self._D_to_stack()

    def _do_pop(self, segment, index):
        """Pop the stack topmost value and save as segment$index."""
        if segment in ['local', 'argument', 'this', 'that']:
            self._pop_basic_seg(segment, index)
        elif segment in ['temp', 'pointer', 'static']:
            # SP--, *(TEMP+i) = *SP
            # SP--, *(THIS/THAT) = *SP
            # SP--, *(FooStatic.i) = *SP
            self._stack_to_D()
            self._access_mem(segment, index)
            self.write_cmd('M=D')

    def _push_basic_seg(self, segment, index):
        # addr = segmentPointer + i, *SP=*addr, SP++
        seg = self._get_seg(segment)
        self.write_cmd('@'+seg, 'D=M', '@%s'%index, 'A=D+A', 'D=M')
        self._D_to_stack()

    def _pop_basic_seg(self, segment, index):
        # addr = segmentPointer + i, SP--, *addr=*SP
        seg = self._get_seg(segment)
        self.write_cmd('@'+seg, 'D=M', '@%s'%index, 'D=D+A')
        self._save_to_reg('D', R_COPY)
        self._stack_to_D()
        self._load_from_reg(R_COPY)
        self.write_cmd('M=D')

    def _compare(self, comp):
        """
        Write code for comparision, e.g., JNE, JLE, JGE..

        If the comparision result is true, return -1, else 0.
        Therefore, we need to use two labels to support this if-else control flow 
        (branch1 to assign -1 and branch2 to assign 0)

        pop_stack_twice()
        D=D-M   # now D is the diff between the last two values on the stack
        @Label1
        D;comp  // (e.g., JNE, JLE, JGE)
        @-1
        D=A   # save -1 to D
        @SP
        A=M-2
        M=D   # assign -1 to *SP-2 if it's true
        @Label2
        0;JMP
        (Label1)
        @0
        D=A   # save 0 to D
        @SP
        A=M-2
        M=D   # assign 0 to *SP-2 if it's false
        (Label2)
        """
        def save_int(num):
            # save to *SP-2, but didn't update SP
            if num == -1:
                self.write_cmd('@1', 'D=-A')
            else:
                self.write_cmd('@%d'%num, 'D=A')
            self.write_cmd('@SP', 'A=M-1', 'A=A-1', 'M=D')

        self.write_cmd('D=D-M')
        label1 = self._new_label()
        self.write_cmd('@'+label1, 'D;'+comp)
        save_int(-1)
        label2 = self._new_label()
        self.write_cmd('@'+label2, '0;JMP')
        self.write_cmd('(%s)'%label1)
        save_int(0)
        self.write_cmd('(%s)'%label2)

