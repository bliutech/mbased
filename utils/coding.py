import string
from dataclasses import dataclass
import re
import unittest
import itertools



# NameGenerator class
class NameGenerator:
    def __init__(self) -> None:
        self.generated_list : dict[str, str] = {
            "conditional": "key"
        }
        self.last_state = []
    def is_same_except_not_equal(self, cond : str) -> bool | str:
        for i in range(1, len(self.generated_list)):
            compare : list[str] = list(self.generated_list.keys())[i]
            parts1 : list[str] = cond.split()
            parts2 : list[str] = compare.split()
            if len(parts1) != len(parts2):
                return False

            differences : int = 0
            for p1, p2 in zip(parts1, parts2):
                if p1 != p2:
                    if (p1 == '==' and p2 == '!=') or (p1 == '!=' and p2 == '=='):
                        differences += 1 
                    else:
                        differences += 2
                
            if differences == 1:
                return compare
        return False

    def generate_name(self, conditional : str) -> str:
            reused_test : bool | str = self.is_same_except_not_equal(conditional)
            if (self.generated_list.get(conditional) == None) and type(reused_test) == bool:
                gen_key : str = next(self.generate_unique_uppercase_string())
                new_code : dict[str, str] = {conditional : gen_key}
                self.generated_list.update(new_code)
                return gen_key
            else:
                if type(reused_test) != bool:
                    return "! " + self.generated_list.get(reused_test)
                else:
                    return self.generated_list.get(conditional)
            
            

    def generate_unique_uppercase_string(self) -> any:
        for length in itertools.count(1):
            for s in itertools.product(string.ascii_uppercase, repeat=length):
                if ''.join(s) not in self.last_state:
                    self.last_state.append(''.join(s))
                    yield ''.join(s)


@dataclass
class Boolean:
    raw: str
    encoded: str

class DictionaryEncoder:
    def __init__(self) -> None:
        self.name_generator = NameGenerator()

    def encode(self, mlil_if_string) -> str:
        first_index : int = -1
        last_index : int = -1
        first_times : int = -1
        for i in range(len(mlil_if_string)):
            if mlil_if_string[i] == '(' and first_times < 0:
                first_index = i
                first_times += 1
            elif mlil_if_string[i] == ')':
                last_index = i + 1

        condition : str = mlil_if_string[first_index: last_index]

        logical_operators = r'(\|\||&&|!(?!\=)|\(|\))'
        split_conditions : list[str] = re.split(logical_operators, condition)
        split_conditions = [cond.strip() for cond in split_conditions if cond.strip()]


        encoded_parts : list[str] = []

        for cond in split_conditions:
            if cond in {'||', '&&', '!','(', ')'}:
                if cond == '||':
                    encoded_parts.append('|')
                elif cond == '&&':
                    encoded_parts.append('&')
                else:
                    encoded_parts.append(cond)
            else:
                code : str = self.name_generator.generate_name(cond)
                #print(code)
                encoded_parts.append(code)
        
        return ' '.join(encoded_parts)

# Unit tests
class TestNameGenerator(unittest.TestCase):
    def test_generate_name(self) -> None:
        name_gen : NameGenerator = NameGenerator()

class TestDictionaryEncoder(unittest.TestCase):
    def test_encode(self) -> None:
        encoder : DictionaryEncoder = DictionaryEncoder()
        encoded_str : str = encoder.encode("if (([ebp_1 + 0x14].b == 0 || [ebp_1 + 0x14].b != 0 && [ebp_1 + 0x14].c != 0) || ![ebp_1 + 0x14] == 0) then 387 @ 0x8040da8 else 388 @ 0x8040d8b")
        print(encoded_str)


if __name__ == '__main__':
    unittest.main()
