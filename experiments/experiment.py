import sys

from experiments.generator import BooleanGenerator
from experiments.obfuscator import MBAObfuscator

from parser.lex import Lexer
from parser.parse import Parser
from parser.ast import Expr

from solver import Solver

from utils.metrics import OpCounter


def run_experiment(
    passes: list[str], n: int = 100
) -> list[tuple[int, str, int, str, int, str, int]]:
    """
    Runs an experiment with the given passes and up to n variables.

    :param passes: The passes to run.
    :param n: The maximum number of variables.

    :return:

    (n, original, original_count, obfuscated, obfuscated_count, simplified, simplified_count)
    """
    if n < 2:
        n = 2

    res: list[tuple[int, str, int, str, int, str, int]] = (
        []
    )  # (n, original, original_count, obfuscated, obfuscated_count, simplified, simplified_count)

    bg: BooleanGenerator = BooleanGenerator()
    s: Solver = Solver(passes)
    oc: OpCounter = OpCounter()

    for i in range(2, n + 1):
        print(f"Running experiment with n={i}", file=sys.stderr)

        expr: str = bg.generate_expr(i)
        print(f"Original expression: {expr}", file=sys.stderr)

        l: Lexer = Lexer(expr)
        l.lex()

        p: Parser = Parser(l.tokens)
        orig_ast: Expr = p.parse()

        orig_count = orig_ast.acceptRet(oc)
        print(f"Original count: {orig_count}", file=sys.stderr)

        obf_ast = MBAObfuscator().obfuscate(orig_ast)
        print(f"Obfuscated expression: {obf_ast}", file=sys.stderr)
        obf_count = obf_ast.acceptRet(oc)
        print(f"Obfuscated count: {obf_count}", file=sys.stderr)

        simplified_ast = s.run(obf_ast)
        print(f"Simplified expression: {simplified_ast}", file=sys.stderr)
        simplified_count = simplified_ast.acceptRet(oc)
        print(f"Simplified count: {simplified_count}", file=sys.stderr)

        res.append(
            (
                i,
                orig_ast,
                orig_count,
                obf_ast,
                obf_count,
                simplified_ast,
                simplified_count,
            )
        )

    return res
