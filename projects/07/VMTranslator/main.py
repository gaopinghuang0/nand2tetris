'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

import sys
from VM_translator import VMTranslator

def main():
  argv = sys.argv
  size = len(argv)

  default = ['../StackArithmetic/SimpleAdd/SimpleAdd.vm',
    '../StackArithmetic/StackTest/StackTest.vm',
    '../MemoryAccess/BasicTest/BasicTest.vm',
    '../MemoryAccess/StaticTest/StaticTest.vm',
    '../MemoryAccess/PointerTest/PointerTest.vm',
    ][1]

  if size < 2:
    print('Usage: python main.py somefile.vm')
    print('using default file: %s...'%default)
    infile = default
  else:
    infile = argv[1]

  vm = VMTranslator()
  vm.translate(infile)


if __name__ == '__main__':
    main()
