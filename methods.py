#Bisection method
def bisection(f, a, b, tol=1e-6, max_iter=100):
    steps = []

    if f(a) * f(b) >= 0:
        return "Invalid interval", steps

    for i in range(max_iter):
        c = (a + b) / 2
        steps.append((i+1, c, f(c)))

        if abs(f(c)) < tol:
            return c, steps

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    return c, steps


#Secant Method
def secant(f, x0, x1, tol=1e-6, max_iter=100):
    steps = []

    for i in range(max_iter):
        if f(x1) - f(x0) == 0:
            return "Division error", steps

        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
        steps.append((i+1, x2, f(x2)))

        if abs(x2 - x1) < tol:
            return x2, steps

        x0, x1 = x1, x2

    return x2, steps

#Newton Method
def newton(f, df, x0, tol=1e-6, max_iter=100):
    steps = []

    x = x0
    for i in range(max_iter):
        if df(x) == 0:
            return "Derivative zero", steps

        x_new = x - f(x)/df(x)
        steps.append((i+1, x_new, f(x_new)))

        if abs(x_new - x) < tol:
            return x_new, steps

        x = x_new

    return x, steps

#Regular Falsi Method
def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    steps = []

    if f(a) * f(b) >= 0:
        return "Invalid interval", steps

    for i in range(max_iter):
        # False position formula
        c = (a*f(b) - b*f(a)) / (f(b) - f(a))
        steps.append((i+1, c, f(c)))

        if abs(f(c)) < tol:
            return c, steps

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    return c, steps