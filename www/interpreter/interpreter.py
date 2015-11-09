from .imp_lexer import *
from .lexer import Token
from . import econ

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.pos = 0
        # set current token to the first token taken from the input
        self.current_token = self.lexer[self.pos]

    def get_next_token(self):
        self.pos += 1
        if self.pos >= len(self.lexer):
            return Token('EOF', None)
        return self.lexer[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()


    def _calc_i(self):
        i_lex = []
        if self.current_token.type == MINUS: #if i is negative
            i_lex.append(Token(0, NUMBER))
        while self.current_token.type != COMMA:
            i_lex.append(self.current_token)
            self.eat(self.current_token.type)
        self.eat(COMMA)
        return Interpreter(i_lex).expr()

    def _calc_n(self):
        n_lex = []
        while self.current_token.type != RPAREN:
            n_lex.append(self.current_token)
            self.eat(self.current_token.type)
        self.eat(RPAREN)
        return Interpreter(n_lex).expr()


    def factor(self):
        """factor : NUMBER | LPAREN expr RPAREN | NUMBER PERCENT"""
        token = self.current_token
        if token.type == NUMBER:
            self.eat(NUMBER)
            if self.current_token.type == PERCENT:
                self.eat(PERCENT)
                return token.value / 100
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        """term : factor ((MUL | DIV | FgP) factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL, DIV, FgP, PgF, AgF, FgA, AgP, PgA, PgG, AgG, PgA1):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                if self.current_token.type in (FgP, PgF, AgF, FgA, AgP, PgA, PgG, AgG, PgA1):
                    continue
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

            elif token.type == FgP:
                self.eat(FgP)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.f_given_p(result, i, n)
            elif token.type == PgF:
                self.eat(PgF)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.p_given_f(result, i, n)

            elif token.type == AgF:
                self.eat(AgF)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.a_given_f(result, i, n)
            elif token.type == FgA:
                self.eat(FgA)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.f_given_a(result, i, n)

            elif token.type == AgP:
                self.eat(AgP)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.a_given_p(result, i, n)
            elif token.type == PgA:
                self.eat(PgA)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.p_given_a(result, i, n)

            elif token.type == AgG:
                self.eat(AgG)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.a_given_g(result, i, n)
            elif token.type == PgG:
                self.eat(PgG)
                i = self._calc_i()
                n = self._calc_n()
                result = econ.p_given_g(result, i, n)

            elif token.type == PgA1:
                self.eat(PgA1)
                g = self._calc_i()
                i = self._calc_i()
                n = self._calc_n()
                result = econ.p_given_a1(result,g, i, n)
        return result

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        term   : factor ((MUL | DIV) factor)*
        factor : NUMBER | LPAREN expr RPAREN
        expr   : term ((PLUS | MINUS) term)*

        """
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result
