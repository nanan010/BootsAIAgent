#!/usr/bin/env python3

from pkg.calculator import Calculator
from pkg.render import format_json_output

def main():
    calculator = Calculator()
    
    # Test some expressions
    expressions = [
        "3 + 5",
        "10 * 2",
        "15 / 3",
        "2 + 3 * 4",
        "100 - 25 / 5"
    ]
    
    for expr in expressions:
        result = calculator.evaluate(expr)
        if result is not None:
            output = format_json_output(
                expression=expr,
                result=result,
                indent=4,
                sort_keys=True
            )
            print(f"Expression: {expr}")
            print(f"Result: {output}")
            print("-" * 40)

if __name__ == "__main__":
    main()