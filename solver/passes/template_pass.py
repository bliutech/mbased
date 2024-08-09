from mbased.parser.ast import Expr
from mbased.parser.visitor import Visitor


def run_pass(ast: Expr) -> Expr:
    # Sample visitor
    v: TemplateVisitor = TemplateVisitor()
    ast.accept(v)

    return ast


class TemplateVisitor(Visitor):
    pass
