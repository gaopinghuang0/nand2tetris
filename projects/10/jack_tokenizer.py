#!/usr/bin/env python3
import sys
import os

from core.tokenizer import Lexer, Tokenizer


# tokenize a single file or directory
# output *T.xml if necessary
class JackTokenizer(object):
    def __init__(self, infile_or_dir, output_dir=None):
        self.infile_or_dir = infile_or_dir
        self.isdir = os.path.isdir(infile_or_dir)

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

        self.escape_dict = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

    def save2xml(self, tokens, outfile):
        with open(outfile, 'w') as fp:
            fp.write('<tokens>\n')
            for token in tokens:
                if token['text'] in self.escape_dict:  # escape
                    token['text'] = self.escape_dict[token['text']]
                fp.write('<{type}> {text} </{type}>\n'.format(**token))
            fp.write('</tokens>\n')

    def run_one(self, infile):
        basename = os.path.basename(infile)
        base = os.path.splitext(basename)[0]
        outfile = os.path.join(self.output_dir, base+'T.my.xml')
        print(outfile)
        with open(infile) as inpt:
            lexer = Lexer(inpt)
            tokens = lexer.get_tokens()
            # save to outfile xml
            self.save2xml(tokens, outfile)

    def run_all(self):
        if self.isdir:
            for infile in os.listdir(self.infile_or_dir):
                if infile.endswith('.jack'):
                    self.run_one(os.path.join(self.infile_or_dir, infile))
        else:
            self.run_one(self.infile_or_dir)


def main():
    if len(sys.argv) < 2:
        print('Usage: ./jack_tokenizer.py infile_or_dir [outdir]')
        sys.exit(1)
    jt = JackTokenizer(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else None)
    jt.run_all()

if __name__ == '__main__':
    main()