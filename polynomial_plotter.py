#!/usr/bin/env python3
"""Ask for a polynomial's coefficients and save its graph with Matplotlib."""

import argparse
import math
from pathlib import Path


def ask_degree():
    while True:
        try:
            degree = int(input("Polynomial degree (highest power of x): "))
            if degree >= 0:
                return degree
        except ValueError:
            pass
        print("Please enter a whole number greater than or equal to 0.")


def ask_coefficients(degree):
    coefficients = []
    print("Enter coefficients from the highest power to the constant term.")
    print("Use 0 for any missing term.")

    for power in range(degree, -1, -1):
        prompt = f"Coefficient of x^{power}: "
        if power == 0:
            prompt = "Constant term (x^0): "

        while True:
            try:
                coefficient = float(input(prompt))
                if not math.isfinite(coefficient):
                    print("Please enter a finite number.")
                elif power == degree and degree > 0 and coefficient == 0:
                    print("The highest-degree coefficient must be nonzero.")
                else:
                    coefficients.append(coefficient)
                    break
            except ValueError:
                print("Please enter a number, for example 3, -4 or 0.5.")

    return coefficients


def evaluate_polynomial(x, coefficients):
    """Coefficients are ordered from the highest power to the constant."""
    result = 0
    power = len(coefficients) - 1
    for coefficient in coefficients:
        result += coefficient * x**power
        power -= 1
    return result


def approximate_integral(coefficients, a, b, steps):
    h = (b - a) / steps

    total = (
        evaluate_polynomial(a, coefficients)
        + evaluate_polynomial(b, coefficients)
    ) / 2

    for i in range(1, steps):
        x = a + i * h
        total += evaluate_polynomial(x, coefficients)

    return h * total


def polynomial_text(coefficients, math_text=False):
    """Make a readable formula, omitting zero terms and unnecessary 1s."""
    terms = []
    degree = len(coefficients) - 1
    for index, coefficient in enumerate(coefficients):
        if coefficient == 0:
            continue

        power = degree - index
        magnitude = abs(coefficient)
        factor = f"{magnitude:.15g}"
        if math_text and "e" in factor:
            mantissa, exponent = factor.split("e")
            factor = rf"{mantissa}\times 10^{{{int(exponent)}}}"
        if power > 0 and magnitude == 1:
            factor = ""

        if power == 0:
            term = factor
        elif power == 1:
            term = factor + "x"
        else:
            exponent = f"x^{{{power}}}" if math_text else f"x^{power}"
            term = factor + exponent

        if terms:
            sign = " - " if coefficient < 0 else " + "
        else:
            sign = "-" if coefficient < 0 else ""
        terms.append(sign + term)

    return "".join(terms) or "0"


def save_graph(coefficients, xmin, xmax, points, output):
    try:
        import matplotlib
        matplotlib.use("Agg")  # Save a file without needing a desktop window.
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ValueError(
            "Matplotlib is required. Install it with: "
            "python -m pip install matplotlib"
        ) from error

    step = (xmax - xmin) / (points - 1)
    xs = [xmin + i * step for i in range(points)]
    ys = [evaluate_polynomial(x, coefficients) for x in xs]
    if not all(math.isfinite(y) for y in ys):
        raise ValueError("Values are too large. Try a smaller x-axis range.")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, color="#254f91", linewidth=2)
    ax.axhline(0, color="#666666", linewidth=0.8)
    if xmin <= 0 <= xmax:
        ax.axvline(0, color="#666666", linewidth=0.8)
    ax.set_xlim(xmin, xmax)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("$f(x) = " + polynomial_text(coefficients, math_text=True) + "$")
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description="Ask for a polynomial's degree and coefficients, then save its graph.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: degree 3, then coefficients 3, -4, 1, -12 "
               "gives f(x) = 3x^3 - 4x^2 + x - 12.",
    )
    parser.add_argument("--output", "-o", type=Path, default=Path("polynomial.png"),
                        help="output graph filename (.png or .svg)")
    parser.add_argument("--xmin", type=float, default=-5,
                        help="left end of the x-axis range")
    parser.add_argument("--xmax", type=float, default=5,
                        help="right end of the x-axis range")
    parser.add_argument("--points", type=int, default=500,
                        help="number of points used to draw the curve")


    parser.add_argument(
    "--integrate",
    action="store_true",
    help="approximate the definite integral"
    )
    parser.add_argument(
    "--a",
    type=float,
    help="left endpoint of the integration interval"
    )
    parser.add_argument(
    "--b",
    type=float,
    help="right endpoint of the integration interval"
    )
    parser.add_argument(
    "--steps",
    type=int,
    default=1000,
    help="number of subintervals used for numerical integration"
    )


    args = parser.parse_args()

    if not (math.isfinite(args.xmin) and math.isfinite(args.xmax)
            and math.isfinite(args.xmax - args.xmin) and args.xmin < args.xmax):
        parser.error("the x-axis limits must be finite, with xmin < xmax")
    if args.points < 2:
        parser.error("--points must be at least 2")
    if (args.xmax - args.xmin) / (args.points - 1) == 0:
        parser.error("the chosen range and number of points give a zero step width")
    if args.output.suffix.lower() not in (".png", ".svg"):
        parser.error("--output must have a .png or .svg extension")


    if args.integrate:
        if args.a is None or args.b is None:
            parser.error("--integrate requires both --a and --b")
        if not (math.isfinite(args.a) and math.isfinite(args.b)):
            parser.error("--a and --b must be finite numbers")
        if args.a >= args.b:
            parser.error("--a must be less than --b")
        if args.steps <= 0:
            parser.error("--steps must be a positive integer")
    

    try:
        degree = ask_degree()
        coefficients = ask_coefficients(degree)
        print("\nf(x) = " + polynomial_text(coefficients))
        save_graph(coefficients, args.xmin, args.xmax, args.points, args.output)
        print("Graph saved to:", args.output.resolve())


        if args.integrate:
            integral = approximate_integral(
                coefficients, args.a, args.b, args.steps
            )
            
            print("\nNumerical integration")
            print("Polynomial:", polynomial_text(coefficients))
            print(f"Interval: [{args.a}, {args.b}]")
            print("Method: Composite trapezoidal rule")
            print("Subintervals:", args.steps)
            print("Approximate integral:", integral)


    except EOFError:
        parser.exit(2, "\nInput ended before all coefficients were entered.\n")
    except KeyboardInterrupt:
        parser.exit(130, "\nCancelled.\n")
    except (ValueError, OverflowError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
