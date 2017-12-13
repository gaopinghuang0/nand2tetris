'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

from command_type import CommandType

R_R3 = R_THIS = 3
R_R4 = R_THAT = 4
R_R5 = R_TEMP = 5
R_R15 = R_COPY  = 15

class CodeWriter(object):
  def __init__(self, outfile):
    self.f = open(outfile, 'w')
    self.label_num = 0

  def write_cmd(self, cmd):
    if isinstance(cmd, list):
      for c in cmd:
        self.f.write(c+'\n')
    elif isinstance(cmd, str):
      self.f.write(cmd+'\n')

  def write_arithmetic(self, cmd):
    """
    add, sub, neg, eq, gt, lt, and, or, not
    """
    def pop_stack_twice():
      # more efficient way
      # since *SP is not updated except the end
      # D is the SP-1, M is the SP-2
      self.write_cmd(['@SP', 'A=M-1', 'D=M', 'A=A-1'])
    def pop_stack_once():
      # note that *SP is not updated
      # D is the SP-1
      self.write_cmd(['@SP', 'A=M-1', 'D=M'])

    self.write_comment(cmd)
    if cmd.arg1 == 'add':
      # pop, pop, add, SP--
      pop_stack_twice()
      self.write_cmd('M=D+M')
    elif cmd.arg1 == 'sub':
      pop_stack_twice()
      self.write_cmd('M=M-D')
    elif cmd.arg1 == 'and':
      pop_stack_twice()
      self.write_cmd('M=M&D')
    elif cmd.arg1 == 'or':
      pop_stack_twice()
      self.write_cmd('M=M|D')
    elif cmd.arg1 == 'not':
      pop_stack_once()
      self.write_cmd('M=!D')
      return  # no need to dec_sp later
    elif cmd.arg1 == 'neg':
      pop_stack_once()
      self.write_cmd('M=-D')
      return  # no need to dec_sp later
    elif cmd.arg1 == 'eq':
      # pop, pop, eq, SP--
      pop_stack_twice()
      self._compare('JNE')
    elif cmd.arg1 == 'lt':
      pop_stack_twice()
      self._compare('JLE')
    elif cmd.arg1 == 'gt':
      pop_stack_twice()
      self._compare('JGE')
    else:
      # raise ValueError('unknown arithmetic command')
      pass

    # update *SP only once
    self._dec_sp()

  def write_push_pop(self, cmd):
    def access_mem(name, offset):
      if name == 'static':
        self._a_command('FooStatic.'+offset)
      else:
        base_reg = {"temp": R_TEMP, "pointer": R_THIS}[name]
        self._access_reg(base_reg + int(offset))

    self.write_comment(cmd)
    if cmd.cmd_type == CommandType.C_PUSH:
      if cmd.arg1 == 'constant':
        # push, SP++
        self.write_cmd(['@'+cmd.arg2, 'D=A'])
        self._D_to_stack()
      if cmd.arg1 in ['local', 'argument', 'this', 'that']:
        self._push_basic_seg(cmd)
      elif cmd.arg1 in ['temp', 'pointer', 'static']:
        # *SP = *(TEMP+i), SP++
        # *SP = *(THIS/THAT), SP++
        # *SP = *(FooStatic.i), SP++
        access_mem(cmd.arg1, cmd.arg2)
        self.write_cmd('D=M')
        self._D_to_stack()
    else:
      if cmd.arg1 in ['local', 'argument', 'this', 'that']:
        self._pop_basic_seg(cmd)
      elif cmd.arg1 in ['temp', 'pointer', 'static']:
        # SP--, *(TEMP+i) = *SP
        # SP--, *(THIS/THAT) = *SP
        # SP--, *(FooStatic.i) = *SP
        self._stack_to_D()
        access_mem(cmd.arg1, cmd.arg2)
        self.write_cmd('M=D')

  def _push_basic_seg(self, cmd):
    # addr = segmentPointer + i, *SP=*addr, SP++
    seg = self._get_seg(cmd)
    self.write_cmd(['@'+seg, 'D=M', '@'+cmd.arg2, 'A=D+A', 'D=M'])
    self._D_to_stack()

  def _pop_basic_seg(self, cmd):
    # addr = segmentPointer + i, SP--, *addr=*SP
    seg = self._get_seg(cmd)
    self.write_cmd(['@'+seg, 'D=M', '@'+cmd.arg2, 'D=D+A'])
    self._save_to_reg('D', R_COPY)
    self._stack_to_D()
    self._load_from_reg(R_COPY)
    self.write_cmd('M=D')

  def close(self):
    self.f.close()
    print('file closed:', self.f.closed)

  def write_comment(self, cmd):
    self.write_cmd('// '+cmd.source)

  def _dec_sp(self):
    self.write_cmd(['@SP', 'M=M-1'])

  def _inc_sp(self):
    self.write_cmd(['@SP', 'M=M+1'])

  def _load_sp(self):
    self.write_cmd(['@SP', 'A=M'])

  def _compare(self, comp):
    """
    pop_stack_twice()
    D=D-M
    @Label1
    D;comp  // (e.g., JNE, JLE, JGE)
    @-1
    D=A
    @SP
    A=M-2
    M=D
    @Label2
    0;JMP
    (Label1)
    @0
    D=A
    @SP
    A=M-2
    M=D
    (Label2)
    """
    def save_int(num):
      # save to *SP-2, but didn't update SP
      if num == -1:
        self.write_cmd(['@1', 'D=-A'])
      else:
        self.write_cmd(['@%d'%num, 'D=A'])
      self.write_cmd(['@SP', 'A=M-1', 'A=A-1', 'M=D'])

    self.write_cmd('D=D-M')
    label1 = self._new_label()
    self.write_cmd(['@'+label1, 'D;'+comp])
    save_int(-1)
    label2 = self._new_label()
    self.write_cmd(['@'+label2, '0;JMP'])
    self.write_cmd('(%s)'%label1)
    save_int(0)
    self.write_cmd('(%s)'%label2)

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
    self.write_cmd('@'+a)

  def _get_seg(self, cmd):
    if cmd.arg1 == 'local':
      seg = 'LCL'
    elif cmd.arg1 == 'argument':
      seg = 'ARG'
    else:
      seg = cmd.arg1.upper()
    return seg

  def _D_to_stack(self):
    self._load_sp()
    self.write_cmd('M=D')
    self._inc_sp()

  def _stack_to_D(self):
    self._dec_sp()
    self._load_sp()
    self.write_cmd('D=M')
