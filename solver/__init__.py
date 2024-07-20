"""
    MBA solver module applying strategies to simplify the AST.

The Solver takes on the approach of applying passes to the AST in a
pipeline fashion. A pass is a transformation that simplifies the AST
in some way. The passes are defined in the passes directory.
"""

import sys
from importlib import import_module

from parser.ast import Expr


class Solver:
    def __init__(self, passes: list[str]):
        self.passes: list[str] = passes

    def get_module(self, name: str):
        print(f"Importing {name}")
        return import_module(f"solver.passes.{name}")

    # TODO: Add type annotation for AST once classes are finished.
    def run(self, ast: Expr) -> Expr:
        for m in map(self.get_module, self.passes):
            try:
                ast = m.run_pass(ast)
            except Exception as e:
                print(f"Error in {m.__name__}: {e}", file=sys.stderr)
                raise e
        return ast
