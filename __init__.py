import sys
from binaryninja.log import log_info
from binaryninja.binaryview import BinaryViewType
from binaryninja.plugin import PluginCommand
from binaryninja.plugin import BackgroundTaskThread
from binaryninja.enums import (MediumLevelILOperation, RegisterValueType)

class MBADeobfuscationInBackground(BackgroundTaskThread):
  def __init__(self, bv, msg):
    BackgroundTaskThread.__init__(self, msg, True)
    self.bv = bv

  def run(self):
    for instr in self.bv.mlil_instructions:
	    if instr.operation == MediumLevelILOperation.MLIL_IF:
		    log_info(instr)


def mba_deobfuscation_in_background(self):
  # step 3 - how?
  # instance = 
  print("what now")
