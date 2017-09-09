'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

from command_type import CommandType

class CodeWriter(object):
  def __init__(self, outfile):
    self.f = open(outfile, 'w')

  def write_arithmetic(self, cmd):
    """
    add, sub, neg, eq, gt, lt, and, or, not
    """
    stmts = ['// '+cmd.source]
    if cmd.arg1 == 'add':
      # pop, pop, add, SP--
      stmts += ['@SP', 'A=M-1', 'D=M', 'A=A-1', 'M=D+M', '@SP', 'M=M-1']
    else:
      raise ValueError('unknown arithmetic command')

    self.write(stmts)

  def write_push_pop(self, cmd):
    stmts = ['// '+cmd.source]
    if cmd.cmd_type == CommandType.C_PUSH:
      if cmd.arg1 == 'constant':
        # push, SP++
        stmts += ['@'+cmd.arg2, 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    else:
      pass

    self.write(stmts)

  def write(self, statements):
    for stmt in statements:
      self.f.write(stmt+'\n')

  def close(self):
    self.f.close()
    print('file closed:', self.f.closed)