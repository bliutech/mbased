"""
Generate random boolean expressions for testing purposes.
"""

import random

from mbased.utils.coding import NameGenerator


class BooleanGenerator:
    def __init__(self, seed: int = 1337):
        self.seed = seed
        self.random = random.Random(seed)
        self.ops = ["|", "&", "^"]

    def generate_expr(self, n: int = 2) -> str:
        """
        Generates a random boolean expression with n variables.
        """
        if n < 2:
            raise ValueError("n must be greater than 1")

        ng: NameGenerator = NameGenerator()

        res: list[str] = []
        paren_count: int = 0

        if self.random.randint(0, 1):
            res.append("(")
            paren_count += 1
        if self.random.randint(0, 1):
            res.append("!")
        res.append(next(ng.generate_unique_uppercase_string()))

        for _ in range(1, n):
            res.append(self.random.choice(self.ops))
            closing_paren = False

            if self.random.randint(0, 1):
                if paren_count > 0 and self.random.randint(0, 1):
                    closing_paren = True
                else:
                    res.append("(")
                    paren_count += 1

            if self.random.randint(0, 1):
                res.append("!")

            res.append(next(ng.generate_unique_uppercase_string()))

            if closing_paren:
                res.append(")")
                paren_count -= 1

        while paren_count > 0:
            res.append(")")
            paren_count -= 1

        return " ".join(res)


if __name__ == "__main__":
    generator = BooleanGenerator(None)
    for i in range(2, 101):
        print(f"N={i}: {generator.generate_expr(i)}", end="\n\n")
