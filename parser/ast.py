from typing import Union


class Term:
    """
    Represents a single term in a binary expression

    ...

    Attributes
    ----------
    name : str
        the encoded name of the term
    """

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            the encoded name of the term
        """
        self.value = name

    def __str__(self) -> str:
        return self.value


class And:
    """
    Represents the AND (&) operator in a boolean expression
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "&"


class Or:
    """
    Represents the OR (|) operator in a boolean expression
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "|"


class Not:
    """
    Represents the NOT (!) operator in a boolean expression
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "!"


class Expr:
    """
    Represents a full binary expression

    ...

    Attributes
    ----------
    left : Expr/Term
        The operand left of the expression's operator. Can be a Term or another Expr.

    right : Expr/Term
        The operand right of the expression's operator. Can be a Term or another Expr.

    operator : And/Or/Not
        The operator of the boolean expression.
    """

    def __init__(
        self,
        left: Union["Expr", "Term"],
        right: Union["Expr", "Term"],
        operator: Union["And", "Or", "Not"],
    ) -> None:
        """
        Parameters
        ----------
        left : Expr/Term
            The operand left of the expression's operator. Can be a Term or another Expr.

        right : Expr/Term
            The operand right of the expression's operator. Can be a Term or another Expr.

        operator : And/Or/Not
            The operator of the boolean expression.
        """

        self.left = left  # left operand
        self.right = right  # right operand
        self.operator = operator  # operator

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"
