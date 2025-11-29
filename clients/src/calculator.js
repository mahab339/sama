// Token types
const NUMBER = 'NUMBER';
const MINUS = 'MINUS';
const PLUS = 'PLUS';
const MUL = 'MUL';
const DIV = 'DIV';
const PERCENT = 'PERCENT';
const COMMA = 'COMMA';
const RPAREN = 'RPAREN';
const LPAREN = 'LPAREN';
const PgF = 'PgivenF';
const FgP = 'FgivenP';
const AgF = 'AgivenF';
const FgA = 'FgivenA';
const PgA = 'PgivenA';
const AgP = 'AgivenP';
const PgG = 'PgivenG';
const AgG = 'AgivenG';
const PgA1 = 'PgivenA1';

class Token {
    constructor(value, type) {
        this.type = type;
        // Convert value to number if type is NUMBER
        this.value = type === NUMBER ? parseFloat(value) : value;
    }
}

class LexerError extends Error {
    constructor(message) {
        super(message);
        this.name = 'LexerError';
    }
}

class ParserError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ParserError';
    }
}

function lex(characters) {
    const token_exprs = [
        [/^\s+/, null],
        [/^#[^\n]*/, null],
        [/^\+/, PLUS],
        [/^-/, MINUS],
        [/^\*/, MUL],
        [/^\//, DIV],
        [/^\(\s*P\s*[|/\\]\s*F\s*,/i, PgF],
        [/^\(\s*F\s*[|/\\]\s*P\s*,/i, FgP],
        [/^\(\s*F\s*[|/\\]\s*A\s*,/i, FgA],
        [/^\(\s*A\s*[|/\\]\s*F\s*,/i, AgF],
        [/^\(\s*P\s*[|/\\]\s*A\s*,/i, PgA],
        [/^\(\s*A\s*[|/\\]\s*P\s*,/i, AgP],
        [/^\(\s*P\s*[|/\\]\s*G\s*,/i, PgG],
        [/^\(\s*A\s*[|/\\]\s*G\s*,/i, AgG],
        [/^\(\s*P\s*[|/\\]\s*A1\s*,/i, PgA1],
        [/^\(/, LPAREN],
        [/^\)/, RPAREN],
        [/^%/, PERCENT],
        [/^,/, COMMA],
        [/^(\d*\.\d+|\d+)/, NUMBER]
    ];

    let pos = 0;
    const tokens = [];

    while (pos < characters.length) {
        let match = null;
        for (const [pattern, tag] of token_exprs) {
            match = pattern.exec(characters.slice(pos));
            if (match) {
                const text = match[0];
                if (tag) {
                    tokens.push(new Token(text, tag));
                }
                pos += text.length;
                break;
            }
        }
        if (!match) {
            throw new LexerError(`Illegal character: ${characters[pos]}`);
        }
    }

    return tokens;
}

// Financial calculation functions
function f_given_p(p, i, n) {
    return p * Math.pow(1 + i, n);
}

function p_given_f(f, i, n) {
    return f * Math.pow(1 + i, -n);
}

function f_given_a(a, i, n) {
    return a * ((Math.pow(1 + i, n) - 1) / i);
}

function a_given_f(f, i, n) {
    return f * (i / (Math.pow(1 + i, n) - 1));
}

function p_given_a(a, i, n) {
    return a * ((Math.pow(1 + i, n) - 1) / (i * Math.pow(1 + i, n)));
}

function a_given_p(p, i, n) {
    return p * ((i * Math.pow(1 + i, n)) / (Math.pow(1 + i, n) - 1));
}

function p_given_g(g, i, N) {
    return g * ((Math.pow(1 + i, N) - i * N - 1) / (i * i * Math.pow(1 + i, N)));
}

function a_given_g(g, i, N) {
    return g * ((Math.pow(1 + i, N) - i * N - 1) / (i * (Math.pow(1 + i, N) - 1)));
}

function p_given_a1(a1, g, i, N) {
    if (g !== i) {
        return a1 * (1 - Math.pow(1 + g, N) * Math.pow(1 + i, -N)) / (i - g);
    } else {
        return a1 * (N / (1 + i));
    }
}

class Interpreter {
    constructor(tokens) {
        this.tokens = tokens;
        this.pos = 0;
        this.current_token = this.tokens[this.pos];
    }

    get_next_token() {
        this.pos += 1;
        if (this.pos >= this.tokens.length) {
            return new Token('EOF', null);
        }
        return this.tokens[this.pos];
    }

    error() {
        throw new ParserError('Invalid syntax');
    }

    eat(token_type) {
        if (this.current_token.type === token_type) {
            this.current_token = this.get_next_token();
        } else {
            this.error();
        }
    }

    _calc_i() {
        const i_lex = [];
        if (this.current_token.type === MINUS) {
            i_lex.push(new Token(0, NUMBER));
        }
        while (this.current_token.type !== COMMA) {
            i_lex.push(this.current_token);
            this.eat(this.current_token.type);
        }
        this.eat(COMMA);
        return new Interpreter(i_lex).expr();
    }

    _calc_n() {
        const n_lex = [];
        while (this.current_token.type !== RPAREN) {
            n_lex.push(this.current_token);
            this.eat(this.current_token.type);
        }
        this.eat(RPAREN);
        return new Interpreter(n_lex).expr();
    }

    factor() {
        const token = this.current_token;
        if (token.type === NUMBER) {
            this.eat(NUMBER);
            if (this.current_token.type === PERCENT) {
                this.eat(PERCENT);
                return token.value / 100;
            }
            return token.value;
        } else if (token.type === LPAREN) {
            this.eat(LPAREN);
            const result = this.expr();
            this.eat(RPAREN);
            return result;
        } else if (token.type === PLUS) {
            this.eat(PLUS);
            return this.factor();
        } else if (token.type === MINUS) {
            this.eat(MINUS);
            return -this.factor();
        }
        this.error();
    }

    term() {
        let result = this.factor();

        while ([MUL, DIV, FgP, PgF, AgF, FgA, AgP, PgA, PgG, AgG, PgA1].includes(this.current_token.type)) {
            const token = this.current_token;
            
            switch (token.type) {
                case MUL:
                    this.eat(MUL);
                    if ([FgP, PgF, AgF, FgA, AgP, PgA, PgG, AgG, PgA1].includes(this.current_token.type)) {
                        continue;
                    }
                    result *= this.factor();
                    break;
                    
                case DIV:
                    this.eat(DIV);
                    result /= this.factor();
                    break;

                case FgP:
                    this.eat(FgP);
                    const i_fgp = this._calc_i();
                    const n_fgp = this._calc_n();
                    result = f_given_p(result, i_fgp, n_fgp);
                    break;

                case PgF:
                    this.eat(PgF);
                    const i_pgf = this._calc_i();
                    const n_pgf = this._calc_n();
                    result = p_given_f(result, i_pgf, n_pgf);
                    break;

                case AgF:
                    this.eat(AgF);
                    const i_agf = this._calc_i();
                    const n_agf = this._calc_n();
                    result = a_given_f(result, i_agf, n_agf);
                    break;

                case FgA:
                    this.eat(FgA);
                    const i_fga = this._calc_i();
                    const n_fga = this._calc_n();
                    result = f_given_a(result, i_fga, n_fga);
                    break;

                case AgP:
                    this.eat(AgP);
                    const i_agp = this._calc_i();
                    const n_agp = this._calc_n();
                    result = a_given_p(result, i_agp, n_agp);
                    break;

                case PgA:
                    this.eat(PgA);
                    const i_pga = this._calc_i();
                    const n_pga = this._calc_n();
                    result = p_given_a(result, i_pga, n_pga);
                    break;

                case AgG:
                    this.eat(AgG);
                    const i_agg = this._calc_i();
                    const n_agg = this._calc_n();
                    result = a_given_g(result, i_agg, n_agg);
                    break;

                case PgG:
                    this.eat(PgG);
                    const i_pgg = this._calc_i();
                    const n_pgg = this._calc_n();
                    result = p_given_g(result, i_pgg, n_pgg);
                    break;

                case PgA1:
                    this.eat(PgA1);
                    const g_pga1 = this._calc_i();
                    const i_pga1 = this._calc_i();
                    const n_pga1 = this._calc_n();
                    result = p_given_a1(result, g_pga1, i_pga1, n_pga1);
                    break;

                default:
                    this.error();
            }
        }
        return result;
    }

    expr() {
        let result = this.term();

        while ([PLUS, MINUS].includes(this.current_token.type)) {
            const token = this.current_token;

            if (token.type === PLUS) {
                this.eat(PLUS);
                result += this.term();
            } else if (token.type === MINUS) {
                this.eat(MINUS);
                result -= this.term();
            }
        }

        return result;
    }
}

export function calcexpression(expr) {
    const tokens = lex(expr);
    const interpreter = new Interpreter(tokens);
    return interpreter.expr();
}

// Example usage:
// console.log(calcexpression("100000(P|A, 5.25%, 5) + 50000(P|A, 4.75%, 3) + 30000(P|A1, .09, 5.25%, 5)"));
