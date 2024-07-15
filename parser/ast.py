type ExprType = (
    "AndExpr" | "OrExpr" | "NotExpr" | "ParenExpr" | "Expr" | "ExprPrime"
)  # Union of the different expression types for type hinting

type VarType = "Var"


class Var:
    """
    A class to represent a variable in an expression.

    Attributes
    ----------
    value : str
        The name of the variable.
    """

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the variable.
        """
        self.value = name

    def __str__(self) -> str:
        return self.value


class Expr:
    """
    A class to represent a generic expression.

    Attributes
    ----------
    first : VarType or ExprType
        The first part of the expression.
    second : ExprType, optional
        The second part of the expression (default is None).
    """

    def __init__(self, first: VarType | ExprType, second: ExprType = None) -> None:
        """
        Parameters
        ----------
        first : VarType or ExprType
            The first part of the expression.
        second : ExprType, optional
            The second part of the expression (default is None).
        """
        self.first = first
        self.second = second

    def __str__(self) -> str:
        return (
            str(self.first) + " " + str(self.second)
            if self.second is not None
            else str(self.first)
        )


class ExprPrime:
    """
    A class to represent expression' (needed for valid LL(1) grammar).

    Attributes
    ----------
    first : ExprType or None
        The first part of the expression.
    """

    def __init__(self, first: ExprType | None) -> None:
        """
        Parameters
        ----------
        first : ExprType or None
            The first part of the expression.
        """
        self.first = first

    def __str__(self) -> str:
        return str(self.first)


class AndExpr:
    """
    A class to represent an 'and' expression.

    Attributes
    ----------
    first : VarType or ExprType
        The first part of the expression.
    """

    def __init__(self, first: VarType | ExprType) -> None:
        """
        Parameters
        ----------
        first : VarType or ExprType
            The first part of the expression.
        """
        self.first = first

    def __str__(self) -> str:
        return f"& {self.first}"


class OrExpr:
    """
    A class to represent an 'or' expression.

    Attributes
    ----------
    first : VarType or ExprType
        The first part of the expression.
    """

    def __init__(self, first: VarType | ExprType) -> None:
        """
        Parameters
        ----------
        first : VarType or ExprType
            The first part of the expression.
        """
        self.first = first

    def __str__(self) -> str:
        return f"| {self.first}"


class NotExpr:
    """
    A class to represent a 'not' expression.

    Attributes
    ----------
    first : VarType or ExprType
        The first part of the expression.
    """

    def __init__(self, first: VarType | ExprType) -> None:
        """
        Parameters
        ----------
        first : VarType or ExprType
            The first part of the expression.
        """
        self.first = first

    def __str__(self) -> str:
        return f"!{self.first}"


class ParenExpr:
    """
    A class to represent a parenthesized expression.

    Attributes
    ----------
    first : VarType or ExprType
        The first part of the expression.
    """

    def __init__(self, first: VarType | ExprType) -> None:
        """
        Parameters
        ----------
        first : VarType or ExprType
            The first part of the expression.
        """
        self.first = first

    def __str__(self) -> str:
        return f"({self.first})"
