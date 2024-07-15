from __future__ import annotations
from enum import Enum


class Operator(Enum):
    """
    An enumeration class to represent each operation in a boolean expression.

    Attributes
    ----------
    value: str
        the string value of each operator. The characters "&", "|", "!", "(", and ")" are allowed.
    """

    def __str__(self) -> str:
        return str(self.value)

    And = "&"
    Or = "|"
    Not = "!"
    ParenOpen = "("
    ParenClose = ")"


class Var:
    """
    A class to represent the terminal value labeled by the encoder.

    ...

    Attributes
    ----------
    name : str
        the name given to the boolean variable by the encoder. name ::= [A-Z]+

    """

    def __init__(self, name: str) -> None:
        """
        Constructs all the necessary attributes for the Var object.

        Parameters
        ----------
        name : str
            the name given to the boolean variable by the encoder. name ::= [A-Z]+
        """

        self.name = name

    def __str__(self) -> str:
        return self.name


class Expr:
    """
    A class to represent a boolean expression. Can contain up to 3 terminals or non-terminals.

    ...

    Attributes
    ----------
    first : Var | Operator
        the first term of the expression. Can be a Var or Operator.

    second: Expr | ExprPrime
        the second term of the expression. Can be an Expr or ExprPrime.

    third: Operator
        the third term of the expression. Can only be the ParenClose Operator (default is None)
    """

    def __init__(
        self, first: Var | Operator, second: Expr | ExprPrime, third: Operator = None
    ) -> None:
        """
        Constructs all the necessary attributes for the Expr object.

        Parameters
        ----------
        first : Var | Operator
            the first term of the expression. Can be a Var or Operator.

        second: Expr | ExprPrime
            the second term of the expression. Can be an Expr or ExprPrime.

        third: Operator
            the third term of the expression. Can only be the ParenClose Operator (default is None).
        """
        self.first = first
        self.second = second
        self.third = third

    def __str__(self) -> str:
        """
        The string format of the Expr class.

        Returns  in the format matching the number of terms of an expression.

        Returns
        -------
        str
        """

        if self.first == Operator.Not:
            return f"{self.first}{self.second}"

        if self.first == Operator.ParenOpen:
            return f"{self.first}{self.second}{self.third}"

        return f"{self.first} {self.second}"


class ExprPrime:
    """
    An intermediary class for Expr to maintain LL(1) grammar

    Both attributes support None to allow for node to empty as per the LL(1) grammar.

    ...

    Attributes
    ----------
    first : Operator | None
        the first term of the expression. Can be Operator or None (default is None).

    second: Expr | None
        the second term of the expression. Can be an Expr or None (default is None).
    """

    def __init__(self, first: Operator | None, second: Expr | None = None) -> None:
        """
        Parameters
        ----------
        first : Operator | None
            the first term of the expression. Can be Operator or None (default is None).

        second: Expr | None
            the second term of the expression. Can be an Expr or None (default is None).
        """
        self.first = first
        self.second = second

    def __str__(self) -> str:
        """
        The string format of the Expr class.

        Returns in the format matching the number of terms of an expression'.

        Returns an empty string when both attributes are equal to None (ε/"").

        Returns
        -------
        str
        """
        if self.first is None:
            return ""

        return f"{self.first} {self.second}"
