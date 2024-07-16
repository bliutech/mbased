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


class Var:
    """
    A class to represent the terminal value labeled by the encoder.

    ...

    Attributes
    ----------
    name : str
        the name given to the boolean variable by the encoder. name ::= [A-Z]+

    """

    def __init__(self, name: str):
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

    second: Expr | ExprPrime | None
        the second term of the expression. Can be an Expr, ExprPrime, or None. Can only be None when ExprPrime is nullable.
    """

    def __init__(
        self, first: Var | Operator, second: Expr | ExprPrime, third: Operator = None
    ):
        """
        Constructs all the necessary attributes for the Expr object.

        Parameters
        ----------
        first : Var | Operator
            the first term of the expression. Can be a Var or Operator.

        second: Expr | ExprPrime
            the second term of the expression. Can be an Expr or ExprPrime.
        """
        self.first = first
        self.second = second

    def __str__(self) -> str:
        """
        The string format of the Expr class.

        Returns  in the format matching the number of terms of an expression.

        Returns
        -------
        str
        """

        if self.second is None:
            return str(self.first)  # when ExprPrime is nullable

        if self.first == Operator.Not:
            return str(self.first) + str(self.second)

        return f"{self.first} {self.second}"


class ExprPrime:
    """
    An intermediary class for Expr to maintain LL(1) grammar

    Both attributes support None to allow for node to empty as per the LL(1) grammar.

    ...

    Attributes
    ----------
    first : Operator
        the operator for the expression'.

    second: Expr
        the expression that will have the operator applied to it.
    """

    def __init__(self, first: Operator, second: Expr):
        """
        Parameters
        ----------
        first : Operator
            the operator for the expression'.

        second: Expr
            the expression that will have the operator applied to it.
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


class ParenExpr:
    """
    A class to represent a parenthesized expression.
    Attributes
    ----------
    first : Expr
        The inner expression within the parentheses
    """

    def __init__(self, first: Expr):
        """
        Parameters
        ----------
        first : Expr
            The inner expression within the parentheses
        """
        self.first = first

    def __str__(self) -> str:
        return f"({self.first})"
