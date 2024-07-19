from unittest import TestCase
from utils.coding import DictionaryEncoder


class TestDictionaryEncoder(unittest.TestCase):
    """
    A class to test the DictionaryEncoder class.

    Methods
    -------
    test_encode() -> None:
        Tests the encode method.
    """

    def test_encode(self) -> None:
        """
        Tests the encode method.
        """
        test_cases_encoded: dict[str, str] = {
            "if (([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || ![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( ( A | ! A & ! B ) | ! C )",
            "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A )",
            "while (x == 3 && y >= 2):": "( A & B )",
            "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || (![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A & ! B ) | ( ! C )",
        }
        for encoded_test in test_cases_encoded:
            encoder: DictionaryEncoder = DictionaryEncoder()
            encoded_str: str = encoder.encode(encoded_test)
            answer: str = test_cases_encoded.get(encoded_test)
            self.assertEqual(
                encoded_str, answer, "Two values are not equal to each other..."
            )


class TestDictionaryDecoder(unittest.TestCase):
    """
    A class to test the DictionaryDecoder class.

    Methods
    -------
    test_decode() -> None:
        Tests the decode method.
    """

    def test_decode(self) -> None:
        """
        Tests the encode method.
        """
        test_cases_encoded: dict[str, str] = {
            "if (([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || ![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( ( A | ! A & ! B ) | ! C )",
            "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A )",
            "while (x == 3 && y >= 2):": "( A & B )",
            "if ([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || (![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b": "( A | ! A & ! B ) | ( ! C )",
        }

        test_cases_decoded: dict[str, str] = {
            "( ( A | ! A & ! B ) | ! C )": "( ( [ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0 ) || [ebp_1 + 0x14] != 0 )",
            "( A | ! A )": "( [ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 )",
            "( A & B )": "( x == 3 && y >= 2 )",
            "( A | ! A & ! B ) | ( ! C )": "( [ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0 ) || ( [ebp_1 + 0x14] != 0 )",
        }

        for encoded_test in test_cases_encoded:
            encoder: DictionaryEncoder = DictionaryEncoder()
            encoded_str: str = encoder.encode(encoded_test)
            answer: str = test_cases_encoded.get(encoded_test)

            decoder: DictionaryDecoder = DictionaryDecoder(
                encoder.get_encoded_dictionary()
            )
            decoded_str: str = decoder.decode(answer)
            # print(decoded_str)
            answer: str = test_cases_decoded.get(answer)
            # print(answer)
            self.assertEqual(
                decoded_str, answer, "Two values are not equal to each other..."
            )
