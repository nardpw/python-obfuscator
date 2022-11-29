import argparse
import ast
from ast import *
from pathlib import Path
from random import choice, choices
from typing import Optional

import astor

import _helper as helper


class ObfuscatorVisitor:

    random_string = 'lI'
    random_string1 = 'lI1'
    no_args = arguments([], [], None, [], [], None, [])

    @property
    def random(self):
        return choice(self.random_string) + ''.join(choices(self.random_string1, k=16))

    def __init__(self) -> None:
        self._break = Call(Name(self.random), [], [])
        self.str_pool = []
        self.str_pool_name = Name(self.random)
        self.initialized = False

    def visit_list(self, body):
        if body is None:
            return None
        return list(helper.flatten_list(map(self.visit, body)))


    def obf_module(self, code: Module):
        'Module(stmt* body, type_ignore* type_ignores)'
        l = []
        'FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment)'
        'arguments(arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults, arg? kwarg, expr* defaults)'
        if not self.initialized:
            l.append(NamedExpr(self.str_pool_name, Tuple(self.str_pool)))
            l.append(FunctionDef(self._break.func.id, self.no_args, [Raise(Name('StopIteration'))], [], None, None))
            self.initialized = True
        l.extend(self.visit_list(code.body))

        return Module(l)


    def obf_assign(self, code: Assign):
        'Assign(expr* targets, expr value, string? type_comment)'
        return code

    def obf_augassign(self, code: AugAssign):
        'NamedExpr(expr target, expr value)'
        'BinOp(expr left, operator op, expr right)'
        return code

    'Call(expr func, expr* args, keyword* keywords)'
    _for = Name('_for')
    def obf_for(self, code: For):
        'For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)'
        'ListComp(expr elt, comprehension* generators)'
        'comprehension(expr target, expr iter, expr* ifs, int is_async)'
        return For(code.target, code.iter, self.visit_list(code.body), code.orelse, 0)

    _ = Name('_')
    'Call(expr func, expr* args, keyword* keywords)'
    _while = Name('_while_cond')
    def obf_while(self, code: While):
        'While(expr test, stmt* body, stmt* orelse)'
        'Call(expr func, expr* args, keyword* keywords)'
        'Lambda(arguments args, expr body)'
        'arguments(arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults, arg? kwarg, expr* defaults)'
        return While(self.visit(code.test), self.visit_list(code.body), code.orelse)

    def obf_with(self, code: With):
        'With(withitem* items, stmt* body, string? type_comment)'
        return With(self.visit_list(code.items), self.visit_list(code.body))

    def obf_withitem(self, item: withitem):
        'withitem(expr context_expr, expr? optional_vars)'
        return withitem(self.visit(item.context_expr), self.visit(item.optional_vars))

    def obf_if(self, code: If):
        'If(expr test, stmt* body, stmt* orelse)'
        'IfExp(expr test, expr body, expr orelse)'
        return If(self.visit(code.test), self.visit_list(code.body), code.orelse)

    def obf_boolop(self, code: BoolOp):
        'BoolOp(boolop op, expr* values)'
        'UnaryOp(unaryop op, expr operand)'
        if (t := type(code.op)) not in (And, Or):
            return BoolOp(code.op, self.visit_list(code.values))
        
        if t is And:
            return UnaryOp(Not(), BoolOp(Or(), [UnaryOp(Not(), x) for x in code.values]))
        else:
            return UnaryOp(Not(), BoolOp(And(), [UnaryOp(Not(), x) for x in code.values]))

    def obf_compare(self, code: Compare):
        'Compare(expr left, cmpop* ops, expr* comparators)'
        # if len(code.ops) != 1: return code
        # if len(code.comparators) != 1: return code

        # op = code.ops[0]
        # if isinstance(op, And):
        #     return Compare()

        return Compare(self.visit(code.left), code.ops, self.visit_list(code.comparators))

    def obf_functiondef(self, code: FunctionDef):
        'FunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment)'
        
        'ClassDef(identifier name, expr* bases, keyword* keywords, stmt* body, expr* decorator_list)'
        'Assign(expr* targets, expr value, string? type_comment)'
        'Name(identifier id, expr_context ctx)'
        name = code.name
        l = [FunctionDef(name, self.visit(code.args), self.visit_list(code.body), [], self.visit(code.returns), self.visit(code.type_comment))]
        
        for decorator in reversed(code.decorator_list):
            l.append(Assign([Name(name)], Call(decorator, [Name(name)], [])))

        return l

    def obf_asyncfunctiondef(self, code: AsyncFunctionDef):
        'AsyncFunctionDef(identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment)'
        
        'ClassDef(identifier name, expr* bases, keyword* keywords, stmt* body, expr* decorator_list)'
        'Assign(expr* targets, expr value, string? type_comment)'
        'Name(identifier id, expr_context ctx)'
        name = code.name
        l = [AsyncFunctionDef(name, self.visit(code.args), self.visit_list(code.body), [], self.visit(code.returns), self.visit(code.type_comment))]
        
        for decorator in reversed(code.decorator_list):
            l.append(Assign([Name(name)], Call(decorator, [Name(name)], [])))

        return l

    def obf_arguments(self, arg: arguments):
        'arguments(arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults, arg? kwarg, expr* defaults)'
        return arguments(self.visit_list(arg.posonlyargs), self.visit_list(arg.args), self.visit(arg.vararg), self.visit_list(arg.kwonlyargs), self.visit_list(arg.kw_defaults), self.visit(arg.kwarg), self.visit_list(arg.defaults))

    def obf_arg(self, code: arg):
        'arg(identifier arg, expr? annotation, string? type_comment)'
        return arg(code.arg, None, None)

    def obf_classdef(self, code: ClassDef):
        'ClassDef(identifier name, expr* bases, keyword* keywords, stmt* body, expr* decorator_list)'
        'Assign(expr* targets, expr value, string? type_comment)'
        'Name(identifier id, expr_context ctx)'
        name = code.name
        l = [ClassDef(name, code.bases, code.keywords, self.visit_list(code.body), [])]
        
        for decorator in reversed(code.decorator_list):
            l.append(Assign([Name(name)], Call(decorator, [Name(name)], [])))

        return l

    def obf_break(self, code: Break):
        return code

    _import = Name('__import__')
    def obf_import(self, code: Import):
        l = []
        'Assign(expr* targets, expr value, string? type_comment)'
        for x in code.names:
            l.append(NamedExpr(Name(x.asname or x.name), Call(self._import, [self.add_str(x.name)], [])))
        return Expr(Tuple(l))
    
    def obf_expr(self, code: Expr):
        'Expr(expr value)'
        return Expr(self.visit(code.value))
    
    def obf_name(self, name: Name):
        return name
    
    def obf_call(self, call: Call):
        'Call(expr func, expr* args, keyword* keywords)'
        'keyword(identifier? arg, expr value)'
        'Dict(expr* keys, expr* values)'
        kwargs = {self.add_str(kw.arg): self.visit(kw.value) for kw in call.keywords if kw.arg is not None}
        k = map(lambda kw: keyword(kw.arg, self.visit(kw.value)), filter(lambda kw: kw.arg is None, call.keywords))
        return Call(self.visit(call.func), [Starred(Tuple(self.visit_list(call.args)))], [keyword(None, self.visit(Dict(list(kwargs.keys()), list(kwargs.values())))), *k] if call.keywords else [])

    def add_str(self, text) -> int:
        'Constant(constant value, string? kind)'
        'Name(identifier id, expr_context ctx)'
        'Call(expr func, expr* args, keyword* keywords)'
        'Attribute(expr value, identifier attr, expr_context ctx)'
        'Subscript(expr value, expr slice, expr_context ctx)'
        self.str_pool.append(Call(Attribute(Call(Name('bytes'), [Tuple(list(map(Constant, map(int, text.encode()))))], []), Name('decode')), [], []))
        return self.visit(Subscript(self.str_pool_name, Constant(len(self.str_pool) - 1)))
    
    def obf_subscript(self, s: Subscript):
        'Subscript(expr value, expr slice, expr_context ctx)'
        return Subscript(self.visit(s.value), self.visit(s.slice)) # Call(Attribute(self.visit(s.value), Name('__getitem__')), [self.visit(s.slice)], [])
    
    def obf_slice(self, s: Slice):
        return s # Call(Name('slice'), list(filter(lambda x: x is not None, [s.lower, s.upper, s.step])), [])
    
    def obf_attribute(self, attr: Attribute):
        'Attribute(expr value, identifier attr, expr_context ctx)'
        return Attribute(self.visit(attr.value), attr.attr)

    def obf_constant(self, const: Constant):
        if isinstance(const.value, str):
            return self.add_str(const.value)
        else:
            return const
    
    def obf_dict(self, code: Dict):
        'Dict(expr* keys, expr* values)'
        return Dict(self.visit_list(code.keys), self.visit_list(code.values))
        
    def obf_await(self, code: Await):
        'Await(expr value)'
        return Await(self.visit(code.value))

    def obf_return(self, code: Return):
        'Return(expr? value)'
        return Return(self.visit(code.value))

    def visit(self, code: ast.AST) -> ast.AST:
        if code is None: return code
        if hasattr(self, name := 'obf_' + code.__class__.__name__.lower()):
            return getattr(self, name)(code)
        return code


def main(code):
    obfuscated = ObfuscatorVisitor()
    parsed = ast.parse(code)

    parsed = obfuscated.visit(parsed)
    
    return astor.to_source(parsed).encode()

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