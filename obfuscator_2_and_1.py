import argparse
import ast
from ast import *
from pathlib import Path
from random import choice, choices
from typing import Optional

import astor

import _helper as helper
import obfuscator_1 as obfv1
import obfuscator_2 as obfv2


class ObfuscatorVisitor(obfv2.ObfuscatorVisitor):
    def visit(self, code: ast.AST) -> ast.AST:
        if code is None: return code
        code = obfv1.obf(code)
        if hasattr(self, name := 'obf_' + code.__class__.__name__.lower()):
            return getattr(self, name)(code)
        return code


def main(code):
    obfuscated = ObfuscatorVisitor()
    parsed = ast.parse(code)

    parsed = obfuscated.visit(parsed)
    
    return b'''class _while_cond():
 def __init__(self,cond)->None:self.cond=cond
 def __iter__(self):return self
 def __next__(self):
  if self.cond():
   return True
  raise StopIteration
def _for(iter,_else=0):
 try:
  for _ in iter:pass
  else:
   if _else:_else()
 except RuntimeError:
  if _else:_else()
def _break():
 raise StopIteration()\n\n''' + astor.to_source(parsed).encode()

class Args:
    file: str
    output: Optional[str]
    print: bool

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='input file')
    parser.add_argument('-o', '--output', help='output', default=None)
    parser.add_argument('--print', help='output', action='store_true')
    args: Args = parser.parse_args()

    output = Path(args.output or args.file + '-out.py')

    input = Path(args.file).read_bytes()

    result = main(input)

    if args.print:
        print(result.decode())
    else:
        output.write_bytes(result)