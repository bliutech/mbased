import re
import sys


class Lexer:
    terminals: str = "\\&|\\||\\!|\\(|\\)|[A-Z]+"
    ws: str = "\\s|\\t|\\n|\\r"
    eof: str = "\\Z"

    def __init__(self):
        self.tokens: list[str] = []

    def error(msg: str):
        print(f"Lex error: {msg}", file=sys.stderr)
        exit(1)

    def getTokens(self) -> list[str]:
        return self.tokens

    def lex(self, prog: str):
        p = re.compile(f"{Lexer.terminals}|{Lexer.ws}|{Lexer.eof}")
        last = 0
        for m in p.finditer(prog):
            token = m.group()

            if m.start() != last:
                Lexer.error(
                    f"Invalid character, {prog[last]}, at {m.start()}:{m.end()}"
                )

            if not re.match(Lexer.ws, token):
                if re.match(Lexer.eof, token):
                    self.tokens.append("<EOF>")
                else:
                    self.tokens.append(token)

            last = m.end()


prog = sys.stdin.read()
l = Lexer()
l.lex(prog)
tokens = l.getTokens()
print(tokens)


"""p = Parser(tokens)
p.parse()"""
