from typing import Optional

from parser.ast import (
    Expr,
    ExprPrime,
    Term,
    Var,
    TermExpr,
    OrExpr,
    AndExpr,
    XorExpr,
    ParenTerm,
    NotTerm,
    VarVar,
    TrueConst,
    FalseConst,
)


import re
import sys


class Parser:
    """
    Parser object for building a boolean expression AST.
    """

    def __init__(self) -> None:
        """
        Initializes the parser.
        """
        self.pos: int = -1

    @staticmethod
    def error(msg: str, pos: int):
        print(f"Parse error: {msg} at position {pos}", file=sys.stderr)
        exit(1)

    def parse(self, tokens: list[str]) -> Expr:
        """
        Parses given tokens.
        """
        self.tokens: list[str] = tokens

        # Initializes the first token
        self.advance()

        rv: Expr = self.expr()
        self.assert_end()
        return rv

    def assert_end(self) -> None:
        if self.next_token != "<EOF>":
            Parser.error(f"Expected end '<EOF>' but found {self.next_token}", self.pos)

    def eat(self, expected: str) -> None:
        if self.next_token == expected:
            self.advance()
        else:
            Parser.error(
                f"Expected '{expected}' but found '{self.next_token}'", self.pos
            )

    def advance(self) -> None:
        """
        Moves to the next token.
        """
        self.pos += 1
        self.next_token: str = self.tokens[self.pos]

    def expr(self) -> Expr:
        """
        Parses an expression.
        """
        if (
            self.next_token == "("
            or self.next_token == "!"
            or re.match("[A-Z]+|t|f", self.next_token)
        ):
            first: Term = self.term()
            second: Optional[ExprPrime] = self.expr_prime()

            if second is None:
                return TermExpr(first)
            else:
                return TermExpr(first, second)
        else:
            Parser.error(
                f"Expected (, !, [A-Z]+, t, or f but found '{self.next_token}'",
                self.pos,
            )

    def expr_prime(self) -> Optional[ExprPrime]:
        """
        Parses an expression prime.
        """
        if self.next_token == "|":
            self.eat("|")

            first: Term = self.term()
            second: Optional[ExprPrime] = self.expr_prime()

            if second is None:
                return OrExpr(first)
            else:
                return OrExpr(first, second)
        elif self.next_token == "&":
            self.eat("&")

            first: Term = self.term()
            second: Optional[ExprPrime] = self.expr_prime()

            if second is None:
                return AndExpr(first)
            else:
                return AndExpr(first, second)
        if self.next_token == "^":
            self.eat("^")

            first: Term = self.term()
            second: Optional[ExprPrime] = self.expr_prime()

            if second is None:
                return XorExpr(first)
            else:
                return XorExpr(first, second)
        elif self.next_token == ")" or self.next_token == "<EOF>":
            # Handles epsilon case
            return None
        else:
            Parser.error(
                f"Expected |, &, ^, ), or <EOF> but found '{self.next_token}'", self.pos
            )

    def term(self) -> Term:
        """
        Parses a term.
        """
        if self.next_token == "(":
            self.eat("(")
            first: Expr = self.expr()
            self.eat(")")
            return ParenTerm(first)
        elif self.next_token == "!":
            self.eat("!")
            first: Term = self.term()
            return NotTerm(first)
        elif re.match("[A-Z]+|t|f", self.next_token):
            return self.var()
        else:
            Parser.error(
                f"Expected (, !, [A-Z]+, t, or f but found '{self.next_token}'",
                self.pos,
            )

    def var(self) -> Var:
        """Parses a variable that represents a boolean expression"""
        if re.match("[A-Z]+", self.next_token):
            v: VarVar = VarVar(self.next_token)
            self.eat(self.next_token)
            return v
        elif self.next_token == "t":
            self.eat("t")
            return TrueConst()
        elif self.next_token == "f":
            self.eat("f")
            return FalseConst()
        else:
            Parser.error(
                f"Expected [A-Z]+, t, or f but found '{self.next_token}'", self.pos
            )
