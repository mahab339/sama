import sys
import os

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import from the interpreter package
from interpreter import imp_lex
from interpreter.interpreter import Interpreter

def calc_result(expr):
    tokens = imp_lex(expr)
    interpreter = Interpreter(tokens)
    return interpreter.expr()