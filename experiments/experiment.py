import sys

from mbased.experiments.generator import BooleanGenerator
from mbased.experiments.obfuscator import MBAObfuscator

from mbased.parser.lex import Lexer
from mbased.parser.parse import Parser
from mbased.parser.ast import Expr

from mbased.solver import Solver

from mbased.utils.metrics import OpCounter, VarCounter


def count_ops(ast: Expr) -> int:
    oc: OpCounter = OpCounter()
    ast.accept(oc)
    return oc.getCount()


def count_vars(ast: Expr) -> int:
    vc: VarCounter = VarCounter()
    ast.accept(vc)
    return vc.getCount()


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

    for i in range(2, n + 1):
        print("========================================", file=sys.stderr)
        print(f"Running experiment with n={i}", file=sys.stderr)

        expr: str = bg.generate_expr(i)

        l: Lexer = Lexer()
        l.lex(expr)

        p: Parser = Parser()
        orig_ast: Expr = p.parse(l.tokens)
        print(f"Original expression: {orig_ast}", file=sys.stderr)

        orig_op_count = count_ops(orig_ast)
        print(f"Original Operation count: {orig_op_count}", file=sys.stderr)
        orig_var_count = count_vars(orig_ast)
        print(f"Original Variable count: {orig_var_count}", file=sys.stderr)

        obf_ast = MBAObfuscator().obfuscate(orig_ast)
        print(f"Obfuscated expression: {obf_ast}", file=sys.stderr)
        obf_op_count = count_ops(obf_ast)
        print(f"Obfuscated Operation count: {obf_op_count}", file=sys.stderr)
        obf_var_count = count_vars(obf_ast)
        print(f"Obfuscated Variable count: {obf_var_count}", file=sys.stderr)

        simplified_ast = s.run(obf_ast)
        print(f"Simplified expression: {simplified_ast}", file=sys.stderr)
        simplified_op_count = count_ops(simplified_ast)
        print(f"Simplified Operation count: {simplified_op_count}", file=sys.stderr)
        simplified_var_count = count_vars(simplified_ast)
        print(f"Simplified Variable count: {simplified_var_count}", file=sys.stderr)

        res.append(
            (
                i,
                orig_ast,
                orig_op_count,
                orig_var_count,
                obf_ast,
                obf_op_count,
                obf_var_count,
                simplified_ast,
                simplified_op_count,
                simplified_var_count,
            )
        )

    return res
