from parser.ast import Expr
from parser.visitor import Visitor

def run_pass(ast: Expr) -> Expr:
    # Sample visitor
    v: TemplateVisitor = TemplateVisitor()
    ast.accept(v)

    return ast


class TemplateVisitor(Visitor):
    pass
