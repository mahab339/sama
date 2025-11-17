import sys
import re

class Token(object):
    def __init__(self, value, type):
        self.type = type
        #convert vlue to float if type is number
        if type == 'NUMBER':
            value = float(value)
        self.value = value


def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = Token(text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens

NUMBER = 'NUMBER'
MINUS, PLUS, MUL, DIV = 'MINUS', 'PLUS', 'MUL', 'DIV'
PERCENT = 'PERCENT'
COMMA = 'COMMA'
RPAREN, LPAREN = 'RPAREN', 'LPAREN'
PgF, FgP = 'PgivenF', 'FgivenP'
AgF, FgA = 'AgivenF', 'FgivenA'
PgA, AgP = 'PgivenA', 'AgivenP'
PgG, AgG = 'PgivenG', 'AgivenG'
PgA1 = 'PgivenA1'

token_exprs = [
    (r'[ \n\t]+',   None),
    (r'#[^\n]*',    None),

    (r'\+',         PLUS),
    (r'-',          MINUS),
    (r'\*',         MUL),
    (r'/',          DIV),

    (r'(?i)\(\s*P\s*(\||\/|\\)\s*F,', PgF),
    (r'(?i)\(\s*F\s*(\||\/|\\)\s*P,', FgP),

    (r'(?i)\(\s*F\s*(\||\/|\\)\s*A,', FgA),
    (r'(?i)\(\s*A\s*(\||\/|\\)\s*F,', AgF),

    (r'(?i)\(\s*P\s*(\||\/|\\)\s*A,', PgA),
    (r'(?i)\(\s*A\s*(\||\/|\\)\s*P,', AgP),

    (r'(?i)\(\s*P\s*(\||\/|\\)\s*G,', PgG),
    (r'(?i)\(\s*A\s*(\||\/|\\)\s*G,', AgG),

    (r'(?i)\(\s*P\s*(\||\/|\\)\s*A1,',PgA1),

    (r'\(',         LPAREN),
    (r'\)',         RPAREN),
    (r'\%',         PERCENT),
    (r'\,',         COMMA),

    (r'([0-9]*\.[0-9]+|[0-9]+)', NUMBER)
    ]


def imp_lex(characters):
    return lex(characters, token_exprs)

def f_given_p(p, i, n):
    return p * (1+i)**n

def p_given_f(f, i, n):
    return f * (1+i)**-n

def f_given_a(a, i, n):
    return a * (((1+i)**n-1)/i)

def a_given_f(f, i, n):
    return f * (i/((1+i)**n-1))

def p_given_a(a, i, n):
    return a * (((1+i)**n-1)/(i*(1+i)**n))

def a_given_p(p, i, n):
    return p * (i*(1+i)**n/((1+i)**n-1))

def p_given_g(g, i, N):
    return g * (((1+i)**N-i*N-1)/(i*i*(1+i)**N))

def a_given_g(g, i, N):
    return g * (((1+i)**N-i*N-1)/(i*((1+i)**N-1)))

def p_given_a1(a1, g, i, N):
    if g != i:
        return a1 * (1-(1+g)**N*(1+i)**-N) / (i-g)
    else:
        return a1*(N/(1+i))


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
        elif token.type in (PLUS, MINUS):
            if token.type == PLUS:
                self.eat(PLUS)
                return self.factor()
            else:
                self.eat(MINUS)
                return 0 - self.factor()


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
                result = f_given_p(result, i, n)
            elif token.type == PgF:
                self.eat(PgF)
                i = self._calc_i()
                n = self._calc_n()
                result = p_given_f(result, i, n)

            elif token.type == AgF:
                self.eat(AgF)
                i = self._calc_i()
                n = self._calc_n()
                result = a_given_f(result, i, n)
            elif token.type == FgA:
                self.eat(FgA)
                i = self._calc_i()
                n = self._calc_n()
                result = f_given_a(result, i, n)

            elif token.type == AgP:
                self.eat(AgP)
                i = self._calc_i()
                n = self._calc_n()
                result = a_given_p(result, i, n)
            elif token.type == PgA:
                self.eat(PgA)
                i = self._calc_i()
                n = self._calc_n()
                result = p_given_a(result, i, n)

            elif token.type == AgG:
                self.eat(AgG)
                i = self._calc_i()
                n = self._calc_n()
                result = a_given_g(result, i, n)
            elif token.type == PgG:
                self.eat(PgG)
                i = self._calc_i()
                n = self._calc_n()
                result = p_given_g(result, i, n)

            elif token.type == PgA1:
                self.eat(PgA1)
                g = self._calc_i()
                i = self._calc_i()
                n = self._calc_n()
                result = p_given_a1(result,g, i, n)
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


def calc_result(expr):
    tokens = imp_lex(expr)
    interpreter = Interpreter(tokens)
    return interpreter.expr()


if __name__ == "__main__":
    print(calc_result("100000(P|A, 5.25%, 5) + 50000(P|A, 4.75%, 3)+ 30000(P|A1, .09, 5.25%, 5)"))
