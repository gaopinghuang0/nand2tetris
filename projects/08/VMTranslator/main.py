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

    if len(argv) < 2:
        print('Usage: python main.py [filename.vm|dir]')
    else:
        infile = get_files(argv[1])
        vm = VMTranslator()
        vm.translate(infile)

def get_files(file_or_dir):
    if file_or_dir.endswith('.vm'):
        return file_or_dir
    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()
