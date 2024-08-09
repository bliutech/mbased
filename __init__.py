from binaryninja.log import log_info, log_error
from binaryninja.binaryview import BinaryViewType
from binaryninja.plugin import PluginCommand
from binaryninja.plugin import BackgroundTaskThread
from binaryninja.enums import MediumLevelILOperation

from mbased.parser.lex import Lexer
from mbased.parser.parse import Parser
from mbased.parser.ast import Expr

from mbased.solver import Solver
from mbased.utils.coding import DictionaryEncoder, DictionaryDecoder


class MBADeobfuscationInBackground(BackgroundTaskThread):
    """Assigns a thread to MBA deobfuscation"""

    def __init__(self, bv: BinaryViewType, msg: str):
        """Initiates the MBADeobfuscationInBackground object and defines bv attribute"""
        BackgroundTaskThread.__init__(self, msg, True)
        self.bv = bv

    def run(self):
        """Logs all program if statements to BinaryNinja log"""
        for instr in self.bv.mlil_instructions:
            if instr.operation == MediumLevelILOperation.MLIL_IF:
                try:
                    encoder: DictionaryEncoder = DictionaryEncoder()
                    encoded_instr: str = encoder.encode(str(instr))

                    l: Lexer = Lexer()
                    l.lex(encoded_instr)

                    p: Parser = Parser()
                    ast: Expr = p.parse(l.getTokens())

                    passes: list[str] = ["sympy_pass"]
                    s: Solver = Solver(passes)
                    simplified_ast: Expr = s.run(ast)

                    decoded_instr: str = DictionaryDecoder(
                        encoder.get_encoded_dictionary()
                    ).decode(str(simplified_ast))

                    log_info(f"{hex(instr.address)}: {decoded_instr}", "MBASED")
                except Exception as e:
                    log_error(f"{hex(instr.address)}: {e}", "MBASED")


def mba_deobfuscation_in_background(bv: BinaryViewType):
    """Creates a background task and starts MBA deobfuscation"""
    background_task: MBADeobfuscationInBackground = MBADeobfuscationInBackground(
        bv, "Starting MBASED..."
    )
    background_task.start()


PluginCommand.register(
    "MBASED: Simplify all MBA expressions.",
    "Simplifying booleans...",
    mba_deobfuscation_in_background,
)
