import unittest

from lexer import *
from imp_lexer import *


def _get_the_first_token_type(list):
    if len(list) == 0 or list == None:
        return None
    return list[0].type

def _get_the_first_token_value(list):
    if len(list) == 0 or list == None:
        return None
    return list[0].value


class TestLexerImp(unittest.TestCase):
    def lexer_test(self, characters, expected):
        actual = _get_the_first_token_type(imp_lex(characters))
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', None)

    def test_space(self):
        self.lexer_test(' ', None)

    def test_PgF(self):
        self.lexer_test('(P|F,', PgF)

    def test_FgP(self):
        self.lexer_test('(F|P,', FgP)

    def test_LPAREN(self):
        self.lexer_test('( ', LPAREN)

    def test_RPAREN(self):
        self.lexer_test('  )', RPAREN)

    def test_PLUS(self):
        self.lexer_test(' +', PLUS)

    def test_MUL(self):
        self.lexer_test('* ', MUL)

    def test_lex_len(self):
        self.assertEquals(len(imp_lex('5*20+33 ')), 5)
