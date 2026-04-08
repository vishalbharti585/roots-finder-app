from sympy import symbols, sympify, diff

x = symbols('x')

def get_function(expr):
    try:
        f = sympify(expr)
        return lambda val: float(f.subs(x, val))
    except:
        return None

def get_derivative(expr):
    try:
        f = sympify(expr)
        df = diff(f, x)
        return lambda val: float(df.subs(x, val))
    except:
        return None