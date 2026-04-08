from flask import Flask, render_template, request
from methods import bisection, secant, newton, regula_falsi
from utils import get_function, get_derivative
import numpy as np
import plotly.graph_objs as go

app = Flask(__name__)

# ----------- PLOTLY GRAPH -----------
def generate_plot(f, root=None):
    x_vals = np.linspace(-10, 10, 400)
    y_vals = []

    for x in x_vals:
        try:
            y_vals.append(f(x))
        except:
            y_vals.append(None)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name='f(x)'
    ))

    if isinstance(root, (int, float)):
        fig.add_trace(go.Scatter(
            x=[root],
            y=[f(root)],
            mode='markers',
            name='Root'
        ))

    fig.update_layout(
        title="Function Graph",
        template="plotly_dark"
    )

    return fig.to_html(full_html=False)


# ----------- MAIN ROUTE -----------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    steps = []
    comparison = None
    plot_html = None

    if request.method == "POST":
        expr = request.form.get("function")
        method = request.form.get("method")
        action = request.form.get("action")

        f = get_function(expr)

        if f is None:
            return render_template("index.html", result="Invalid function")

        try:
            a = float(request.form.get("a", 0))
            b = float(request.form.get("b", 0))

            # -------- SOLVE --------
            if action == "solve":

                if method == "Bisection":
                    result, steps = bisection(f, a, b)

                elif method == "Secant":
                    result, steps = secant(f, a, b)

                elif method == "Newton":
                    df = get_derivative(expr)
                    result, steps = newton(f, df, a)

                elif method == "Regula Falsi":
                    result, steps = regula_falsi(f, a, b)

                if isinstance(result, (int, float)):
                    plot_html = generate_plot(f, result)

            # -------- COMPARE --------
            elif action == "compare":
                df = get_derivative(expr)

                root_b, steps_b = bisection(f, a, b)
                root_s, steps_s = secant(f, a, b)
                root_n, steps_n = newton(f, df, a)
                root_r, steps_r = regula_falsi(f, a, b)

                comparison = [
                    ("Bisection", root_b, len(steps_b)),
                    ("Secant", root_s, len(steps_s)),
                    ("Newton", root_n, len(steps_n)),
                    ("Regula Falsi", root_r, len(steps_r)),
                ]

        except:
            result = "Invalid input"

    return render_template(
        "index.html",
        result=result,
        steps=steps,
        comparison=comparison,
        plot_html=plot_html
    )


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))