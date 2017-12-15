'''
VM translator to Hack assembly
Translate *.vm file into assembly file *.asm
Part of project 7 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 2017-09-09
'''

from command import Command


class Parser(object):
  def __init__(self, infile):
    self.infile = infile

  def parse(self):
    with open(self.infile, 'r') as f:
      for line in f:
        statement = line.strip()
        if not statement or statement.startswith('//'):
          # skip empty line or comment
          continue
        # remove inline comment
        _statement = statement.split('//')[0].strip()
        args = _statement.split(' ')
        if len(args) == 1:
          yield Command(Command.C_ARITHMETIC, args[0], source=statement)
        else:
          if args[0] == 'push':
            assert len(args) == 3
            yield Command(Command.C_PUSH, args[1], args[2], source=statement)
          elif args[0] == 'pop':
            assert len(args) == 3
            yield Command(Command.C_POP, args[1], args[2], source=statement)
          elif args[0] == 'label':
            assert len(args) == 2
            yield Command(Command.C_LABEL, args[1], source=statement)
          elif args[0] == 'goto':
            assert len(args) == 2
            yield Command(Command.C_GOTO, args[1], source=statement)
          elif args[0] == 'if-goto':
            assert len(args) == 2
            yield Command(Command.C_IF, args[1], source=statement)
          else:
            # TODO: in the future
            pass
