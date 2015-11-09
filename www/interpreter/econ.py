

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
