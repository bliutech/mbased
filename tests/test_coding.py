from unittest import TestCase
from utils.coding import DictionaryEncoder


class TestDictionaryEncoder(TestCase):
    """
    A class to test the DictionaryEncoder class.

    Methods
    -------
    test_encode() -> None:
        Tests the encode method.
    """

    test_cases: dict[str, str] = {
        "if (([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || ![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( ( A | ! A & B ) | ! C )",
        "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A )",
        "while (x == 3 && y >= 2):": "( A & B )",
        "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || (![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A & B ) | ( ! C )",
    }

    def test_encode(self) -> None:
        """
        Tests the encode method.
        """
        for expected, actual in self.test_cases.items():
            with self.subTest(expected=expected, actual=actual):
                encoder: DictionaryEncoder = DictionaryEncoder()
                encoded_str: str = encoder.encode(expected)
                self.assertEqual(
                    encoded_str, actual, "Two values are not equal to each other..."
                )
