#!/usr/bin/env python3
import sys
import os
import subprocess
import platform


def main():
    if len(sys.argv) < 4:
        print('Compile *.jack into *.vm')
        print('Usage: ./jack_compiler.py infile_or_dir [outdir]')
        print('infile_or_dir   either a single file or src dir')
        print('outdir          use the input dir as outdir if not specified')
        sys.exit(1)
    # compare_xml(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)

if __name__ == '__main__':
    main()