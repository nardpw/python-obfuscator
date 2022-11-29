import argparse
import ast
from ast import *
from pathlib import Path
from typing import Optional

import astor


def obf_body(body):
    return tuple(map(obf, body))


def obf_module(code: Module):
    'Module(stmt* body, type_ignore* type_ignores)'
    return Module(obf_body(code.body))

def obf_annassign(code: AnnAssign):
    'AnnAssign(expr target, expr annotation, expr? value, int simple)'
    'NamedExpr(expr target, expr value)'
    
    return NamedExpr(code.target, code.value)

def obf_assign(code: Assign):
    'Assign(expr* targets, expr value, string? type_comment)'
    'NamedExpr(expr target, expr value)'
    l = []

    for x in code.targets:
        if isinstance(x, Tuple):
            for i, a in enumerate(x.elts):
                n = NamedExpr(a, code.value.elts[i])
                l.append(n)
        else:
            n = NamedExpr(x, code.value)
            l.append(n)
    if len(l) > 1:
        e = Expr(List(l, Load()))
    else:
        e = Expr(l.pop())
    return e

def obf_augassign(code: AugAssign):
    'NamedExpr(expr target, expr value)'
    'BinOp(expr left, operator op, expr right)'
    return Expr(NamedExpr(code.target, BinOp(code.target, code.op, code.value)))

'Call(expr func, expr* args, keyword* keywords)'
_for = Name('_for', Load())
def obf_for(code: For):
    'For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)'
    'ListComp(expr elt, comprehension* generators)'
    'comprehension(expr target, expr iter, expr* ifs, int is_async)'
    args = [GeneratorExp(
                    Tuple(obf_body(code.body), Load()),
                    [
                        comprehension(
                            code.target,
                            code.iter,
                            []
                        )
                    ]
    )]

    if code.orelse:
        args.append(code.orelse)
    
    return Expr(
        Call(
            _for,
            args,
            []
        )
    )

_ = Name('_', Load())
'Call(expr func, expr* args, keyword* keywords)'
_while = Name('_while_cond', Load())
def obf_while(code: While):
    'While(expr test, stmt* body, stmt* orelse)'

    'Call(expr func, expr* args, keyword* keywords)'
    
    'Lambda(arguments args, expr body)'
    
    'arguments(arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults, arg? kwarg, expr* defaults)'
    return obf_for(For(_, Call(_while, [Lambda(arguments([], [], None, [], [], None, []), code.test)], []), obf_body(code.body), code.orelse))
    # return While(code.test, obf_body(code.body), code.orelse)


def obf_if(code: If):
    'If(expr test, stmt* body, stmt* orelse)'
    'IfExp(expr test, expr body, expr orelse)'
    return Tuple([
        IfExp(code.test, Expr(List(obf_body(code.body))), Tuple(obf_body(code.orelse) if code.orelse else [], Load()))
    ], Load())
    # return If(code.test, obf_body(code.body), code.orelse)

_break = Call(Name('_break', Load()), [], [])
def obf_break(code: Break):
    return _break

_import = Name('__import__', Load())
def obf_import(code: Import):
    l = []
    'Assign(expr* targets, expr value, string? type_comment)'
    for x in code.names:
        l.append(Assign([Name(x.asname or x.name, Load())], Call(_import, [Constant(x.name)], [])))
    return Expr(Tuple(obf_body(l), Load()))

# def obf_from(code: ImportFrom):
#     l = []
#     'Assign(expr* targets, expr value, string? type_comment)'
#     for x in code.names:
#         l.append(Assign([Name(x.asname or x.name, Load())], Call(_import, [Constant(x.name)], [])))
#     return Expr(Tuple(obf_body(l), Load()))


OBF = {
    Module: obf_module,
    Assign: obf_assign,
    AnnAssign: obf_annassign,
    For: obf_for,
    While: obf_while,
    If: obf_if,
    AugAssign: obf_augassign,
    Break: obf_break,
    Import: obf_import,
    # ImportFrom: obf_from
}


def obf(code: ast.AST) -> ast.AST:
    if (t := type(code)) in OBF:
        return OBF[t](code)
    return code


def main(code):
    b = obf(ast.parse(code))
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
 raise StopIteration()\n\n''' + astor.to_source(b).encode()

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