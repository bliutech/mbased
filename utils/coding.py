import string
from dataclasses import dataclass
import re
from typing import Generator
import itertools


@dataclass
class Boolean:
    """
    A class to represent a boolean expression with raw and encoded forms.

    Attributes
    ----------
    raw : str
        The raw boolean expression.
    encoded : str
        The encoded boolean expression.
    """

    raw: str
    encoded: str


class NameGenerator:
    """
    A class to generate unique names for boolean conditions.

    Attributes
    ----------
    generated_dictionary_keys : dict
        A dictionary to store generated names for conditions.
    last_state : list
        A list to store the last state of generated names.

    Methods
    -------
    generate_name(conditional: str) -> str:
        Generates a unique name for a given condition.
    generate_unique_uppercase_string() -> any:
        Generates a unique uppercase string.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the NameGenerator object.
        """
        self.generated_dictionary_keys: dict[str, str] = {}
        self.prev_state = []

    def generate_name(self, conditional: str) -> str:
        """
        Generates a unique name for a given condition.

        Parameters
        ----------
        conditional : str
            The condition to generate a name for.

        Returns
        -------
        str
            The generated name.
        """
        replaced_conditional = re.sub("!=", "==", conditional)
        if self.generated_dictionary_keys.get(replaced_conditional) == None:
            gen_key: str = next(self.generate_unique_uppercase_string())
            self.generated_dictionary_keys[replaced_conditional] = gen_key
            return gen_key
        else:
            if conditional != replaced_conditional:
                return "! " + self.generated_dictionary_keys.get(replaced_conditional)
            else:
                return self.generated_dictionary_keys.get(replaced_conditional)

    def generate_unique_uppercase_string(self) -> Generator[str, None, None]:
        """
        Generates a unique uppercase string.
        }

        Yields
        ------
        str
            A unique uppercase string.
        """
        for length in itertools.count(1):
            for s in itertools.product(string.ascii_uppercase, repeat=length):
                if "".join(s) not in self.prev_state:
                    self.prev_state.append("".join(s))
                    yield "".join(s)


class DictionaryEncoder:
    """
    A class to encode boolean expressions using generated names.

    Attributes
    ----------
    name_generator : NameGenerator
        An instance of the NameGenerator class.

    Methods
    -------
    encode(mlil_if_string: str) -> str:
        Encodes a given MLIL if-string.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the DictionaryEncoder object.
        """
        self.name_generator = NameGenerator()

    def encode(self, mlil_if_string: str) -> str:
        """
        Encodes a given MLIL if-string.

        Parameters
        ----------
        mlil_if_string : str
            The MLIL if-string to encode.

        Returns
        -------
        str
            The encoded string.
        """
        first_index: int = -1
        last_index: int = -1
        first_times: int = -1
        for i in range(len(mlil_if_string)):
            if mlil_if_string[i] == "(" and first_times < 0:
                first_index = i
                first_times += 1
            elif mlil_if_string[i] == ")":
                last_index = i + 1

        condition: str = mlil_if_string[first_index:last_index]

        LOGICAL_OPERATORS: re.Pattern = r"(\|\||&&|!(?!\=)|\(|\))"
        split_conditions: list[str] = re.split(LOGICAL_OPERATORS, condition)
        split_conditions = [cond.strip() for cond in split_conditions if cond.strip()]

        encoded_parts: list[str] = []

        for cond in split_conditions:
            if cond in {"||", "&&", "!", "(", ")"}:
                if cond == "||":
                    encoded_parts.append("|")
                elif cond == "&&":
                    encoded_parts.append("&")
                else:
                    encoded_parts.append(cond)
            else:
                code: str = self.name_generator.generate_name(cond)
                encoded_parts.append(code)

        return " ".join(encoded_parts)
