# Polynomial Plotter and Numerical Integration Tool

This Python command-line tool asks the user for a polynomial and saves its graph using Matplotlib.

The program has also been extended to approximate a definite integral using the composite trapezoidal rule.

## Requirements

- Python 3
- Matplotlib

Install Matplotlib with:

```bash
python3 -m pip install matplotlib
```

The command was tested on my computer and Matplotlib was already installed.

## Running the Program

To see the help menu:

```bash
python3 polynomial_plotter.py --help
```

To run the program with the default graph settings:

```bash
python3 polynomial_plotter.py
```

Example with a custom graph range and output file:

```bash
python3 polynomial_plotter.py --xmin -2 --xmax 3 --output polynomial.png
```

The program then asks for the polynomial degree and coefficients.

For example:

```text
Polynomial degree: 3
Coefficient of x^3: 3
Coefficient of x^2: -4
Coefficient of x^1: 1
Constant term: -12
```

This represents:

```text
f(x) = 3x^3 - 4x^2 + x - 12
```

The coefficients are stored from the highest power to the constant term:

```text
[3, -4, 1, -12]
```

Use `0` for a missing term. For example:

```text
3x^3 + x - 12
```

is represented by:

```text
[3, 0, 1, -12]
```

## Graph Options

- `--xmin`: left end of the x-axis range
- `--xmax`: right end of the x-axis range
- `--points`: number of sampled points used to draw the curve
- `--output`, `-o`: output graph filename (`.png` or `.svg`)
- `--help`, `-h`: display the help menu

The default graph uses 500 sampled points.

The program evaluates `f(x)` at the sampled x values and uses these points to draw the curve.

For the example polynomial:

```text
f(0) = -12
```

so the graph passes through `(0, -12)`.

## Numerical Integration

The program can approximate a definite integral using the composite trapezoidal rule.

Example:

```bash
python3 polynomial_plotter.py --integrate --a 0 --b 2 --steps 1000
```

Integration options:

- `--integrate`: enable numerical integration
- `--a`: left endpoint of the integration interval
- `--b`: right endpoint of the integration interval
- `--steps`: number of subintervals

The program checks that the endpoints are finite, that `a < b`, and that the number of steps is positive.

The trapezoidal rule uses:

```text
h = (b - a) / N
```

and approximates the integral using the two endpoints and the interior points.

The implementation reuses `evaluate_polynomial()` to calculate the polynomial values.

`--points` and `--steps` have different purposes:

- `--points` controls the number of points used to draw the graph.
- `--steps` controls the number of subintervals used for numerical integration.

For `N` subintervals, the trapezoidal rule uses `N + 1` evaluation points.

## Numerical Checks

### Test 1: f(x) = x^2 on [0, 1]

Exact value:

```text
1/3 = 0.333333333...
```

With 1000 subintervals, the program produced:

```text
0.33333349999999995
```

### Test 2: f(x) = x on [-1, 1]

Exact value:

```text
0
```

With 1000 subintervals, the program produced:

```text
2.398081733190338e-17
```

This is extremely close to zero; the very small difference is caused by floating-point numerical calculation.

### Test 3: f(x) = 3x^3 - 4x^2 + x - 12 on [0, 2]

Exact value:

```text
-62/3 ≈ -20.666666667
```

Results:

| Subintervals (N) | Approximate integral |
|---:|---:|
| 10 | -20.600000000000005 |
| 100 | -20.666000000000004 |
| 1000 | -20.666659999999972 |

As the number of subintervals increases, the approximation gets closer to the exact value.

A definite integral represents signed accumulation. Areas below the x-axis contribute negative values, while areas above the x-axis contribute positive values.

## Program Structure

- `ask_degree()` asks for the polynomial degree.
- `ask_coefficients()` asks for the coefficients and validates them.
- `evaluate_polynomial()` calculates `f(x)` for a given x value.
- `approximate_integral()` approximates the definite integral using the composite trapezoidal rule.
- `polynomial_text()` creates a readable polynomial expression.
- `save_graph()` calculates sampled points and saves the graph with Matplotlib.
- `main()` handles command-line arguments, validation, and the overall program flow.

The entry point:

```python
if __name__ == "__main__":
    main()
```

runs `main()` when the file is executed directly, but not when it is imported as a module.

## Comparison with the Previous CLI Tool

The previous `permute.py` program and this program both use `argparse`, functions, `main()`, input validation, and the standard Python entry-point structure.

The previous tool mainly receives a string from a command-line argument and prints permutations to the terminal.

The polynomial tool is more flexible and complex. It combines command-line options with interactive input, stores numerical coefficients in a list, evaluates mathematical functions, creates graph files, and performs numerical integration.

`argparse`, `math`, and `pathlib` are part of the Python standard library. Matplotlib is an external dependency and must be installed separately.

## Example Graph

The repository includes an example polynomial graph generated with Matplotlib.