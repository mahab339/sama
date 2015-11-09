import lexer

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
    return lexer.lex(characters, token_exprs)
