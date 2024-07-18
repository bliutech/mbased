from typing import override
from unittest import TestCase

from parser.parse import Parser
from utils.metrics import OpCounter


class TestCount(TestCase):
    def test_counter(self) -> None:
        p: Parser = Parser()
        tree = p.parse(["!", "(", "A", "&", "!", "B", "|", "C", ")", "<EOF>"])
        counter = OpCounter()

        self.assertEqual(counter.getCount(), 0)

        tree.accept(counter)

        self.assertEqual(counter.getCount(), 4)
