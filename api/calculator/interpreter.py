# This will now point to the actual interpreter package
from interpreter.imp_lexer import imp_lex
from interpreter.interpreter import Interpreter

def calc_result(expr):
    tokens = imp_lex(expr)
    interpreter = Interpreter(tokens)
    return interpreter.expr()