import re
import sys


def error(msg: str, pos: int):
    print(f"Parse error: {msg} at position {pos}", file=sys.stderr)
    exit(1)


class Parser:
    """Parser object for analyzing tokens for errors"""

    def __init__(self) -> None:
        """Initializes the parser with attributes to be used"""
        self.pos: int = -1
        print("Initializing the parser")

    def parse(self, tokens: list[str]) -> None:
        """Parses given tokens"""

        self.tokens: list[str] = tokens
        self.len: int = len(tokens) - 1
        self.advance()  # Initializes the first token
        rv = self.expr()
        self.assert_end()
        print("Successfully completed parsing")
        return rv

    def assert_end(self) -> None:
        if self.next_token != "<EOF>":
            error(f"Expected end '<EOF>' but found {self.next_token}", self.pos)

    def next_token(self) -> None:
        next: str = self.tokens[self.pos + 1]
        return next

    def eat(self, expected: str) -> None:
        """Skips a token"""
        if self.next_token == expected:
            # print("eating " + (self.next_token))
            self.advance()
        else:
            error(f"Expected '{expected}' but found '{self.next_token}'", self.pos)

    def advance(self) -> None:
        """Moves to the next token"""
        if self.pos < self.len:
            self.pos += 1
            self.next_token: str = self.tokens[self.pos]
            print(self.next_token)

    def expr(self) -> None:
        """Parses an expression"""
        print("expr: " + str(self.next_token))
        if self.var():
            self.eat(self.next_token)
            self.expr_prime()
        elif self.next_token == "!":
            self.eat("!")
            self.expr()
        elif self.next_token == "(":
            self.eat("(")
            self.expr()
            if self.next_token == ")":
                self.eat(")")
            else:
                error(f"Expected ')' but found '{self.next_token}'", self.pos)
        else:
            error(f"Expected [var, !, (] but found '{self.next_token}'", self.pos)

    def expr_prime(self) -> None:
        """Parses an expression prime (explain what this is later)"""
        print("prime: " + self.next_token)
        if self.pos < self.len:
            if self.next_token == "&":
                self.eat("&")
                self.expr()
            elif self.next_token == "|":
                self.eat("|")
                self.expr()

    def var(self) -> None:
        """Parses a variable that represents a boolean expression"""
        print("var: " + str(self.next_token))
        if re.match("[A-Z]+", self.next_token):
            return True
        else:
            print("not var: " + self.next_token)


"""
Expr ::= var Expr'
       | NOT Expr
       | ( Expr )
		
Expr' ::= AND Expr
        | OR Expr
        | ε

var ::= [A-Z]+
"""

# test
p: Parser = Parser()
tree = p.parse(
    ["!", "A", "&", "!", "B", "|", "C", "<EOF>"]
)  # tree does not tree, only parses
print(tree)
