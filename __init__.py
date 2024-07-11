from binaryninja.log import log_info
from binaryninja.binaryview import BinaryViewType
from binaryninja.plugin import PluginCommand
from binaryninja.plugin import BackgroundTaskThread
from binaryninja.enums import MediumLevelILOperation


class MBADeobfuscationInBackground(BackgroundTaskThread):
    '''Assigns a thread to MBA deobfuscation'''
    
    def __init__(self, bv : BinaryViewType, msg : str):
        '''Initiates the MBADeobfuscationInBackground object and defines bv attribute'''
        BackgroundTaskThread.__init__(self, msg, True)
        self.bv = bv

    def run(self):
        '''Logs all program if statements to BinaryNinja log'''
        for instr in self.bv.mlil_instructions:
            if instr.operation == MediumLevelILOperation.MLIL_IF:
                log_info(instr)


def mba_deobfuscation_in_background(bv : BinaryViewType):
    '''Creates a background task and starts MBA deobfuscation'''
    background_task : MBADeobfuscationInBackground = MBADeobfuscationInBackground(bv, "Starting MBA Deobfuscation")
    background_task.start()


PluginCommand.register(
    "MBA Deobfuscation", "Simplifying booleans", mba_deobfuscation_in_background
)
