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
      codeWriter.write_comment(cmd.source)
      if cmd.cmd_type == cmd.C_ARITHMETIC:
        codeWriter.write_arithmetic(cmd.arg1)
      elif cmd.cmd_type == cmd.C_PUSH or cmd.cmd_type == cmd.C_POP:
        codeWriter.write_push_pop(cmd.cmd_type, cmd.arg1, cmd.arg2)
      elif cmd.cmd_type == cmd.C_LABEL:
        codeWriter.write_label(cmd.arg1)
      elif cmd.cmd_type == cmd.C_GOTO:
        codeWriter.write_goto(cmd.arg1)
      elif cmd.cmd_type == cmd.C_IF:
        codeWriter.write_if(cmd.arg1)
      elif cmd.cmd_type == cmd.C_FUNCTION:
        codeWriter.write_function(cmd.arg1, cmd.arg2)
      elif cmd.cmd_type == cmd.C_RETURN:
        codeWriter.write_return()
      elif cmd.cmd_type == cmd.C_CALL:
        codeWriter.write_call(cmd.arg1, cmd.arg2)
      else:
        raise ValueError('Unknown command type')
    codeWriter.close()
