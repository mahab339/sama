import sys
from imp_lexer import *
from interpreter import Interpreter

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    interpreter = Interpreter(tokens)
    result = interpreter.expr()
    print('----- =', result)
