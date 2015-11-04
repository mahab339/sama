import unittest
from imp_lexer import *
from interpreter import Interpreter

def calc_result(expr):
    tokens = imp_lex(expr)
    interpreter = Interpreter(tokens)
    result = interpreter.expr()
    return result


class TestLexerImp(unittest.TestCase):

    def test_basics1(self):
        expr = '33/3'
        self.assertEqual(calc_result(expr), 11)


    def test_basics2(self):
        expr = '5+3'
        self.assertEqual(calc_result(expr), 8)


    def test_basics3(self):
        expr = '2222-(2)'
        self.assertEqual(calc_result(expr), 2220)


    def test_basics4(self):
        expr = '55+5*2'
        self.assertEqual(calc_result(expr), 65)


    def test_basics5(self):
        expr = '2 + 7 * 4'
        self.assertEqual(calc_result(expr), 30)


    def test_basics6(self):
        expr = '7 - 8 / 4'
        self.assertEqual(calc_result(expr), 5)


    def test_basics7(self):
        expr = '14 + 2 * 3 - 6 / 2'
        self.assertEqual(calc_result(expr), 17)


    def test_basics8(self):
        expr = '7 + 3 * (10 / (12 / (3 + 1) - 1))'
        self.assertEqual(calc_result(expr), 22)


    def test_basics7(self):
        expr = '7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)'
        self.assertEqual(calc_result(expr), 10)


    def test_basics7(self):
        expr = '7 + (((3 + 2)))'
        self.assertEqual(calc_result(expr), 12)


    def test_percent1(self):
        expr = '33%'
        self.assertEqual(calc_result(expr), 0.33)


    def test_percent2(self):
        expr = '40%+5'
        self.assertEqual(calc_result(expr), 5.4)


    def test_percent3(self):
        expr = '50% - .5'
        self.assertEqual(calc_result(expr), 0)


    def error_less_001(self, n1, n2):
        error = abs(n1 - n2)
        if error < .001:
            return True
        else:
            return False

    def test_FgP1(self):
        expr = '5000(F|P, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 5624.32))


    def test_FgP2(self):
        expr = '32000*(F|P, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 28311.552))


    def test_FgP3(self):
        expr = '14141(F|P, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 3776.240231))


    def test_FgP4(self):
        expr = '14141(F|P, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 47255.36189))


    def test_PgF1(self):
        expr = '5000(P|F, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 4444.981793))


    def test_PgF2(self):
        expr = '32000*(P|F, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 36168.98148))


    def test_PgF3(self):
        expr = '14141(P|F, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 52954.22663))


    def test_PgF4(self):
        expr = '14141(P|F, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 4231.644262))

    def test_AgF1(self):
        expr = '5000(A|F, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 1601.742696))


    def test_AgF2(self):
        expr = '32000*(A|F, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 11104.9417))


    def test_AgF3(self):
        expr = '14141(A|F, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 1736.374956))


    def test_AgF4(self):
        expr = '14141(A|F, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 543.4834997))


    def test_FgA1(self):
        expr = '5000(F|A, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 15608))


    def test_FgA2(self):
        expr = '32000*(F|A, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 92211.2))


    def test_FgA3(self):
        expr = '14141(F|A, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 115163.9974))


    def test_FgA4(self):
        expr = '14141(F|A, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 367937.3544))


    def test_PgA1(self):
        expr = '5000(P|A, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 13875.45517))

    def test_PgA2(self):
        expr = '32000*(P|A, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 104224.537))


    def test_PgA3(self):
        expr = '14141(P|A, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 431258.0737))


    def test_PgA4(self):
        expr = '14141(P|A, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 110103.9526))


    def test_AgP1(self):
        expr = '5000(A|P, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 1801.742696))

    def test_AgP2(self):
        expr = '32000*(A|P, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 9824.941699))


    def test_AgP3(self):
        expr = '14141(A|P, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 463.6849562))


    def test_AgP4(self):
        expr = '14141(A|P, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 1816.1735))


    def test_PgG1(self):
        expr = '5000(P|G, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 13512.74465))

    def test_PgG2(self):
        expr = '32000*(P|G, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 107060.1852))


    def test_PgG3(self):
        expr = '14141(P|G, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 3445567.768))


    def test_PgG4(self):
        expr = '14141(P|G, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 565121.4775))


    def test_AgG1(self):
        expr = '5000(A|G, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 4869.297796))

    def test_AgG2(self):
        expr = '32000*(A|G, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 32870.62743))


    def test_AgG3(self):
        expr = '14141(A|G, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 112980.5487))


    def test_AgG4(self):
        expr = '14141(A|G, 9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 72580.3445))


    def test_PgA11(self):
        expr = '5000(P|A1, 0.06, 0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 14702.22178))

    def test_PgA12(self):
        expr = '32000*(P|A1, 4%, -0.04, 3)'
        self.assertTrue(self.error_less_001(calc_result(expr), 108564.8148))


    def test_PgA13(self):
        expr = '14141(P|A1, -0.05, -9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 292086.2842))


    def test_PgA14(self):
        expr = '14141(P|A1, 9% ,9%, 14)'
        self.assertTrue(self.error_less_001(calc_result(expr), 181627.5229))
