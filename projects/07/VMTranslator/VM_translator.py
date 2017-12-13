'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

import os

from my_parser import Parser
from code_writer import CodeWriter
from command_type import CommandType


class VMTranslator(object):
  def __init__(self):
    pass

  def translate(self, infile, outfile=None):
    """
    Translate *.vm file into assembly *.asm file
    """
    if not outfile:
      path, name = os.path.split(infile)
      outfile = os.path.join(path, os.path.splitext(name)[0]+'.asm')
    print(outfile)
    codeWriter = CodeWriter(outfile)

    for cmd in Parser(infile).parse():
      if cmd.cmd_type == cmd.C_ARITHMETIC:
        codeWriter.write_arithmetic(cmd)
      elif cmd.cmd_type == cmd.C_PUSH or cmd.cmd_type == cmd.C_POP:
        codeWriter.write_push_pop(cmd)
      else:
        # TODO: in the future
        pass
    codeWriter.close()


if __name__ == '__main__':
  pass
