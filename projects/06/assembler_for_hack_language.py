'''
Assembler for Hack language
Translate *.asm file into Hack language *.hack
Part of project 6 of www.nand2tetris.org
and the book "The Elements of Computing Systems"

Author: Gaoping Huang
Since: 20170826
'''

import re
import os

DEBUG_PARSER = False
DEBUG_SYMBOL_TABLE = True
DEBUG_RESULT = False

class Label(object):
  def __init__(self, name):
    self.name = name


class AInstruction(object):
  def __init__(self, value):
    self.value = value

  def toCode(self, value=None):
    value = value if value is not None else self.value
    return bin(int(value))[2:].zfill(16)

class CInstruction(object):
  COMP_A1 = {
    'M': '110000',
    '!M': '110001',
    '-M': '110011',
    'M+1': '110111',
    'M-1': '110010',
    'D+M': '000010',
    'D-M': '010011',
    'M-D': '000111',
    'D&M': '000000',
    'D|M': '010101'
  }
  COMP_A0 = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101'
  }
  DEST = [None, 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
  JUMP = [None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

  def __init__(self, comp, dest=None, jump=None):
    self.comp = comp
    self.dest = dest
    self.jump = jump

  def toCode(self):
    code = '111'
    if self.comp in self.COMP_A1:
      code += '1' + self.COMP_A1[self.comp]
    elif self.comp in self.COMP_A0:
      code += '0' + self.COMP_A0[self.comp]
    else:
      print(self.comp)
      raise ValueError('Unknown comp')
    code += bin(self.DEST.index(self.dest))[2:].zfill(3)
    code += bin(self.JUMP.index(self.jump))[2:].zfill(3)
    return code


class Parser(object):
  """Parser"""
  def __init__(self):
    self.statements = []
    
  def parse(self, filename):
    with open(filename, 'r') as f:
      for line in f:
        statement = line.strip()
        if not statement or statement.startswith('//'):
          # empty line or comment
          continue
        DEBUG_PARSER and print(statement)
        if '//' in statement:  # remove inline comment
          statement = statement[:statement.index('//')].strip()
        if statement.startswith('@'):
          # A-instruction
          res = re.search('@(.+)', statement)
          self.statements.append(AInstruction(res.group(1)))
        elif statement.startswith('('):
          # label
          res = re.search('\((.+)\)', statement)
          self.statements.append(Label(res.group(1)))
        else:
          # C-instruction
          res = re.search('(\w+)?=?([^;]+);?(\w+)?\s*.*$', statement)
          self.statements.append(CInstruction(res.group(2), res.group(1), res.group(3)))
    return self.statements


class Assembler(object):
  def __init__(self):
    self.symbol_table = {}
    self.parser = Parser()
    self.init_predefined_symbol()

  def init_predefined_symbol(self):
    for i in range(16):
      self.symbol_table['R'+str(i)] = i
    self.symbol_table.update({
      'SCREEN': 16384,
      'KBD': 24576,
      'SP': 0,
      'LCL': 1,
      'ARG': 2,
      'THIS': 3,
      'THAT': 4
      })

  def update_symbol_table(self, statements):
    # label symbol
    i = 0
    for stmt in statements:
      if isinstance(stmt, Label):
        if stmt.name in self.symbol_table:
          raise ValueError('Duplicate label declaration')
        else:
          self.symbol_table[stmt.name] = i
      else:
        i += 1
    # variable symbol
    i = 16
    for stmt in statements:
      if isinstance(stmt, AInstruction):
        if not stmt.value.isnumeric() and stmt.value not in self.symbol_table:
          self.symbol_table[stmt.value] = i
          i += 1

  def translate(self, infile, outfile=None):
    '''
    Translate *.asm file into Hack language *.hack
    '''
    contents = []
    statements = self.parser.parse(infile)
    self.update_symbol_table(statements)

    DEBUG_SYMBOL_TABLE and print(self.symbol_table)
    for stmt in statements:
      if isinstance(stmt, AInstruction):
        if not stmt.value.isnumeric():
          contents.append(stmt.toCode(self.symbol_table[stmt.value]))
        else:
          contents.append(stmt.toCode())
      elif isinstance(stmt, CInstruction):
        contents.append(stmt.toCode())
    DEBUG_RESULT and print('\n'.join(contents))

    if not outfile:
      outfile = infile[:-4]+'.hack'
    print(outfile)

    with open(outfile, 'w') as outf:
      for code in contents:
        outf.write(code+'\n')




def main():
  asm = Assembler()
  asm.translate('./rect/Rect.asm')

if __name__ == '__main__':
  main()
    