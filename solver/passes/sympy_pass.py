from parser.ast import Expr
from parser.visitor import Visitor


def run_pass(ast: Expr) -> Expr:
    # Sample visitor
    v: SympyMappingVisitor = SympyMappingVisitor()
    ast.accept(v)

    return ast


class SympyMappingVisitor(Visitor):
    pass
