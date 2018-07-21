#!/usr/bin/env python3

"""
test SymbolTable
Just modify project 10 code, output special/customized tag
(e.g., not just `identifier` but `field 0 | static 1 | ...`) for each variable
into xml code, and then check the output xml code manually. 
The test cases include `ExpressoinlessSquare` (copied from project 10) and 
`TestMethodType` (I made up to solely test `method-type subroutine` 
with parameterList. It's not runnable.)
"""

# Author: Gaoping Huang
# Since: 07/21/2018

import sys
import os

from core.jack_tokenizer import JackTokenizer
from core.compilation_engine import CompilationEngine

SUFFIX = '.my.xml'
class TestSymbolTable(object):
    def __init__(self, infile_or_dir, output_dir=None):
        self.infile_or_dir = infile_or_dir
        self.isdir = os.path.isdir(infile_or_dir)
        self.set_output_dir(output_dir)

    def set_output_dir(self, output_dir):
        if output_dir:
            self.output_dir = output_dir
        else: # guess output dir
            if self.isdir:
                self.output_dir = infile_or_dir
            else:
                # use the same dir as input file
                self.output_dir = os.path.dirname(infile_or_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def parse(self, infile):
        basename = os.path.basename(infile)
        base = os.path.splitext(basename)[0]
        outfile = os.path.join(self.output_dir, base+SUFFIX)
        print(outfile)
        with open(infile) as inpt, open(outfile, 'w') as outpt:
            tokenizer = JackTokenizer(inpt)
            compiler = CompilationEngine(tokenizer, outpt)
            compiler.compile_class()

    def run(self):
        if self.isdir:
            for infile in os.listdir(self.infile_or_dir):
                if infile.endswith('.jack'):
                    self.parse(os.path.join(self.infile_or_dir, infile))
        else:
            self.parse(self.infile_or_dir)


def main():
    if len(sys.argv) < 2:
        print('Usage: ./test_symbol_table.py infile_or_dir [outdir]')
        print('infile_or_dir   either a single file or src dir')
        print('outdir          use the input dir if not specified')
        sys.exit(1)
    obj = TestSymbolTable(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)
    obj.run()

if __name__ == '__main__':
    main()