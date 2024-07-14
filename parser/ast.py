from typing import Union


class Variable:
    """
    Represents a single variable term in a binary expression

    ...

    Attributes
    ----------
    name : str
        the encoded name of the variable term
    """

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            the encoded name of the variable term
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


class Expression:
    """
    Represents a full boolean expression

    ...

    Attributes
    ----------
    left : Variable/Expression
        The operand left of the expression's operator. Can be a Variable or another Expression.

    right : Variable/Expression
        The operand right of the expression's operator. Can be a Variable or another Expression.

    operator : And/Or/Not
        The operator of the boolean expression.
    """

    def __init__(
        self,
        left: Union["Expression", "Variable"],
        right: Union["Expression", "Variable"],
        operator: Union["And", "Or", "Not"],
    ) -> None:
        """
        Parameters
        ----------
        left : Variable/Expression
            The operand left of the expression's operator. Can be a Variable or another Expression.

        right : Variable/Expression
            The operand right of the expression's operator. Can be a Variable or another Expression.

        operator : And/Or/Not
            The operator of the boolean expression.
        """

        self.left = left  # left operand
        self.right = right  # right operand
        self.operator = operator  # operator

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"
