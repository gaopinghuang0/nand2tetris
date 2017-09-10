'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

import os
import re
import sys

from parser import Parser
from code_writer import CodeWriter
from command_type import CommandType


class VMTranslator(object):
  def __init__(self):
    pass

  def translate(self, infile, outfile=None):
    """
    Translate *.vm file into assembly  *.asm
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


def main():
  argv = sys.argv
  size = len(argv)

  default = ['./StackArithmetic/SimpleAdd/SimpleAdd.vm',
    './StackArithmetic/StackTest/StackTest.vm',
    './MemoryAccess/BasicTest/BasicTest.vm',
    './MemoryAccess/StaticTest/StaticTest.vm',
    './MemoryAccess/PointerTest/PointerTest.vm',
    ][1]

  if size < 2:
    print('Usage: python VM_translator.py somefile.vm')
    print('using default file: %s...'%default)
    infile = default
  else:
    infile = argv[1]

  vm = VMTranslator()
  vm.translate(infile)



if __name__ == '__main__':
  main()
