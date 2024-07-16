import re
import sys


def error(msg: str, pos: int):
    print(f"Parse error: {msg} at position {pos}", file=sys.stderr)
    exit(1)


class Parser:
    """Parser object for analyzing tokens for errors"""

    def __init__(self):
        """Initializes the parser with attributes to be used"""
        self.pos: int = -1
        print("Initializing the parser")

    def parse(self, tokens: list[str]):
        """Parses given tokens"""

        self.tokens: str = tokens
        self.len: int = len(tokens) - 1
        self.advance()  # Initializes the first token
        rv = self.expr()
        self.assert_end()
        print("Successfully completed parsing")
        return rv

    def assert_end(self):
        if self.pos < self.len:
            error(f"Expected end ({self.len})", self.pos)

    def next_token(self):
        next: str = self.tokens[self.pos + 1]
        return next

    def eat(self, expected: str):
        """Skips a token"""
        if self.next_token == expected:
            # print("eating " + (self.next_token))
            self.advance()
        else:
            error(f"Expected '{expected}' but found '{self.next_token}'", self.pos)

    def advance(self):
        """Moves to the next token"""
        if self.pos < self.len:
            self.pos += 1
            self.next_token: str = self.tokens[self.pos]

    def expr(self):
        """Parses an expression"""
        # print("expr: " + str(self.next_token))
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

    def expr_prime(self):
        """Parses an expression prime (explain what this is later)"""
        # print("prime: " + self.next_token)
        if self.pos < self.len:
            if self.next_token == "&":
                self.eat("&")
                self.expr()
            elif self.next_token == "|":
                self.eat("|")
                self.expr()
            else:
                self.advance()

    def var(self):
        """Parses a variable that represents a boolean expression"""
        # print("var: " + str(self.next_token))
        if re.match("[A-Z]+", self.next_token):
            return True


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
    ["!", "(", "A", "&", "!", "B", "|", "C", ")"]
)  # tree does not tree, only parses
print(tree)
