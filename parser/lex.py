import re
import sys


class Lexer:
    terminals: str = r"\&|\||\^|\!|\(|\)|[A-Z]+|t|f"
    ws: str = r"\s|\t|\n|\r"
    eof: str = r"\Z"

    def __init__(self) -> None:
        self.tokens: list[str] = []

    @staticmethod
    def error(msg: str) -> None:
        raise Exception(msg)

    def getTokens(self) -> list[str]:
        return self.tokens

    def lex(self, prog: str) -> None:
        p: re.Pattern[str] = re.compile(f"{Lexer.terminals}|{Lexer.ws}|{Lexer.eof}")
        last: int = 0
        for m in p.finditer(prog):
            token: str = m.group()

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
