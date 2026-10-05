# Polynomial Plotter

An interactive Python command-line tool that asks for a polynomial's degree
and coefficients, then saves its graph with **Matplotlib**.

## Install and run

Extract this ZIP and open a terminal in the extracted folder.
Install the plotting package with the same Python interpreter you will use:

```bash
python -m pip install matplotlib
python polynomial_plotter.py --help
python polynomial_plotter.py
```

If your system uses `python3`, replace `python` with `python3` in these commands.

## Enter the example

For **3x^3 - 4x^2 + x - 12**, enter the degree and coefficients when prompted:

```text
Polynomial degree (highest power of x): 3
Enter coefficients from the highest power to the constant term.
Use 0 for any missing term.
Coefficient of x^3: 3
Coefficient of x^2: -4
Coefficient of x^1: 1
Constant term (x^0): -12

f(x) = 3x^3 - 4x^2 + x - 12
Graph saved to: .../polynomial.png
```

The graph is saved in the current working directory as `polynomial.png`.
An existing file with the same name will be overwritten. The program saves
the graph directly; no desktop graph window is needed.

## Options

```bash
python polynomial_plotter.py --output my_graph.png --xmin -2 --xmax 3
python polynomial_plotter.py --output my_graph.svg --points 1000
```

| Option | Purpose | Default |
| --- | --- | --- |
| `-h`, `--help` | Show the help menu and exit | - |
| `-o`, `--output` | Graph filename, PNG or SVG | `polynomial.png` |
| `--xmin` | Left end of the x-axis range | `-5` |
| `--xmax` | Right end of the x-axis range | `5` |
| `--points` | Number of sampled points | `500` |

The degree is the highest power of x. Enter coefficients in descending order,
including the constant term. For **2x^3 + 5**, enter degree **3** and coefficients
**2, 0, 0, 5**. For a constant function, enter degree **0** and one coefficient.
All coefficients must be finite numbers; a degree above 0 requires a nonzero
leading coefficient. Decimal coefficients use a dot, for example `0.5`.

The included `example_polynomial.png` plots the supplied example on [-2, 3].
The graph joins sampled points; its resolution is controlled by `--points`.

## Read the program

- `ask_degree()` reads a nonnegative integer.
- `ask_coefficients()` asks for each coefficient and checks the input.
- `evaluate_polynomial()` calculates the function value using a loop.
- `polynomial_text()` creates a readable formula.
- `save_graph()` samples the polynomial, plots it and saves the image.
- `main()` handles command-line options and connects these steps.
