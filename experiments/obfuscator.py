"""
Apply mixed-boolean arithmetic (MBA) obfuscation to a given boolean expression.

MBAObfucator takes an approach of apply transformation to the given boolean expression
based on the abstract syntax tree (AST) of the expression. The transformation is applied
based on a few rules which are taken from the Obfuscator LLVM project. The rules are shown
at https://github.com/obfuscator-llvm/obfuscator/wiki/Instructions-Substitution
"""

from parser.visitor import RetVisitor


class MBAObfuscator(RetVisitor):
    def obfuscate(self, ast, n: int = 1):
        """
        Obfuscates the given AST.

        :param ast: The AST to obfuscate.
        :return: The obfuscated AST.
        """
        for _ in range(n):
            ast = ast.acceptRet(self)

        return ast

    # TODO: Override the visit methods to apply the obfuscation rules
