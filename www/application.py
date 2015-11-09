# -*- coding: utf-8 -*-
"""
    Sama Calculator
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Mohab Hassan.
    :license: GPL.
"""
from interpreter.interpreter import Interpreter
from interpreter.imp_lexer import *

from flask import Flask, jsonify, render_template, request
application = Flask(__name__)

def _calc(characters):
    tokens = imp_lex(characters)
    interpreter = Interpreter(tokens)
    return interpreter.expr()


@application.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=str)
    return jsonify(result=_calc(a))


@application.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    application.run()
