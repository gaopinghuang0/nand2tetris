'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

class CommandType(object):
  C_ARITHMETIC = 0
  C_PUSH = 1
  C_POP = 2
  C_LABEL = 3
  C_GOTO = 4
  C_IF = 5
  C_FUNCTION = 6
  C_RETURN = 7
  C_CALL = 8
  def __init__(self, cmd_type, arg1, arg2=None, source=None):
    self.cmd_type = cmd_type
    self.arg1 = arg1
    self.arg2 = arg2
    self.source = source

  def __repr__(self):
    return 'CommandType(type={}, arg1={}, arg2={})'.format(self.cmd_type, self.arg1, self.arg2)
