from typing import Union


class Term:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value


class And:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "&"


class Or:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "|"


class Not:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "!"


class Expr:
    def __init__(
        self,
        left: Union["Expr", "Term"],
        right: Union["Expr", "Term"],
        operator: Union["And", "Or", "Not"],
    ) -> None:

        self.left = left  # left operand
        self.right = right  # right operand
        self.operator = operator  # operator

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"
