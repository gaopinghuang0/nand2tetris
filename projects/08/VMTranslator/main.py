'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''
import os
import sys
import glob
from VM_translator import VMTranslator

def main():
    argv = sys.argv

    if len(argv) < 2:
        print('Usage: python main.py [filename.vm|dir]')
    else:
        infiles, outfile = get_files(argv[1])
        print(infiles)
        print(outfile)
        vm = VMTranslator()
        vm.translate_all(infiles, outfile)

def get_files(file_or_dir):
    if file_or_dir.endswith('.vm'):
        return [file_or_dir], file_or_dir.replace('.vm', '.asm')
    else:
        _, name = os.path.split(file_or_dir.rstrip('/'))
        return glob.glob(file_or_dir+'/*.vm'), os.path.join(file_or_dir, name+'.asm')


if __name__ == '__main__':
    main()
