from typing import Array
from copy import deepcopy
import re

class IntCodeCPU:
  def __init__(self, program: Array):
    self.ROM = program
    self.RAM = program
    self.instructionPtr = 0
    self.inputModes = ["position","immediate"]
    self.inputQueue = []
    self.opTable = {
      1: self.add,
      2: self.multiply,
      3: self.input_,
      4: self.output,
      5: self.jumpTrue,
      6: self.jumpFalse,
      7: self.lessThan,
      8: self.equality,
      99: self.halt
    }
    self.opcodeParamCounts = {
      1: 3, # add
      2: 3, # multiply
      3: 1, # input
      4: 1, # output
      5: 2, # jumpTrue
      6: 2, # jumpFalse
      7: 3, # lessThan
      8: 3, # equality
      99: 0 # halt
    }

  def clearRAM(self):
    self.RAM = self.ROM

  def parseInstruction(self, instruction: str):
    instruction = instruction.strip()
    # check if the instruction len > 2 and if so,
    # whether extra chars are "input modes"
    # if  len > 2 and !modes, then !instruction
    if len(instruction) > 2:
      preamble = instruction[:-2]
      l = len(preamble)
      if re.search("01{l}", preamble) is None:
        # this is not a valid instruction
        return False
      # preamble needs to be reversed
      preamble = preamble[::-1]
      opcode = int(instruction[-2:])
      instruction = {
        "opcode": opcode,
        "params": [
          {
            "value": None,
            "mode": self.inputModes[int(mode)]
          }
          for mode in preamble
        ],
        "nparams": self.opcodeParamCounts[opcode]
      }

  def add(self, a, b, address):
    self.RAM[address] = a + b

  def multiply(self, a, b, address):
    self.RAM[address] = a * b

  def input_(self, address):
    value = self.inputQueue.pop(0)
    self.RAM[address] = value

  def output(self, address):
    return RAM[address]

  def jumpTrue(self, value, address):
    if value != 0:
      self.instructionPtr = self.RAM[address]

  def jumpFalse(self, value, address):
    if value == 0:
      self.instructionPtr = self.RAM[address]

  def lessThan(self, a, b, address):
    self.RAM[address] = 1 if a < b else 0

  def equality(self, a, b, address):
    self.RAM[address] = 1 if a == b else 0

  def processParameters(self, parameters, instruction):
    loadedInstruction = deepcopy(instruction)
    for parameter, i, iParameter in parameters, enumerate(instruction["params"]):
      loadedInstruction["params"][i]["value"] = self.RAM[parameter] \
        if iParameter["mode"] == "position" else parameter
    return loadedInstruction

  def enqueueInput(self, value):
    self.inputQueue.append(value)

  def doOperation(self):
    instruction = self.parseInstruction(self.instructionPtr)
    self.instructionPtr += 1
    parameters = [
      parameter
      for parameter in
      self.RAM[self.instructionPtr: self.instructionPtr + instruction["nparams"]]
    ]
    loadedInstruction = self.processParameters(parameters, instruction)
    func = self.opTable[loadedInstruction["opcode"]]
    args = [param["value"] for param in loadedInstruction["params"]]
    func(args)