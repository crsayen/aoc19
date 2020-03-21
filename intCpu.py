from copy import deepcopy
import re
import json
from itertools import permutations
from mem3 import program
from instructions5_1 import mem as testmem4


class IntCodeCPU:
  def __init__(self, program):
    self.ROM = program
    self.RAM = program.copy()
    self.instructionPtr = 0
    self.inputModes = ["position","immediate"]
    self.inputQueue = []
    self.halt = False
    self.routeOutputToInput = False
    self.output = None
    self.opTable = {
      1: self.add,
      2: self.multiply,
      3: self.input_,
      4: self.setOutput,
      5: self.jumpTrue,
      6: self.jumpFalse,
      7: self.lessThan,
      8: self.equality,
      99: self.setHalt
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

  def printState(self):
    print()
    print(f"instruction pointer: {self.instructionPtr}")
    print(f"inputQueue: {self.inputQueue}")
    print(f"output: {self.output}")
    print()

  def clearRAM(self):
    self.RAM = self.ROM.copy()
    self.instructionPtr = 0

  def clearOutput(self):
    self.output = None

  def reset(self):
    self.clearInputQueue()
    self.clearOutput()
    self.clearRAM()

  def clearInputQueue(self):
    self.inputQueue = []

  def parseInstruction(self, instruction: str):
    instruction = str(instruction).strip()
    # check if the instruction len > 2 and if so,
    # whether extra chars are "input modes"
    # if  len > 2 and !modes, then !instruction
    opcode = int(instruction[-2:])
    nparams = self.opcodeParamCounts.get(opcode)
    if nparams is None:
      return False
    preamble = ['0'] * nparams
    if len(instruction) > 2:
      preamble = instruction[:-2]
      l = len(preamble)
      if any([True for c in preamble if c not in ['0','1']]):
        # this is not a valid instruction
        return False
      # preamble needs to be reversed
      preamble = preamble[::-1]
    if len(preamble) < nparams:
      suffix = '0' * (nparams - len(preamble))
      preamble += suffix
    return {
      "opcode": opcode,
      "params": [
        {
          "address": None,
          "value" : None,
          "mode": self.inputModes[int(mode)]
        }
        for mode in preamble
      ],
      "nparams": nparams
    }

  def add(self, a, b, c):
    self.RAM[c["address"]] = a["value"] + b["value"]

  def multiply(self, a, b, c):
    self.RAM[c["address"]] = a["value"] * b["value"]

  def input_(self, a):
    value = self.inputQueue.pop(0)
    self.RAM[a["address"]] = value

  def setOutput(self, a):
    self.output = self.RAM[a["address"]]
    if self.routeOutputToInput:
      self.inputQueue.append(self.output)

  def jumpTrue(self, a, b):
    if a["value"] != 0:
      self.instructionPtr = b["value"]

  def jumpFalse(self, a, b):
    if a["value"] == 0:
      self.instructionPtr = b["value"]

  def lessThan(self, a, b, c):
    self.RAM[c["address"]] = 1 if a["value"] < b["value"] else 0

  def equality(self, a, b, c):
    self.RAM[c["address"]] = 1 if a["value"] == b["value"] else 0

  def setHalt(self):
    self.halt = True

  def processParameters(self, parameters, instruction):
    loadedInstruction = deepcopy(instruction)
    for i, (parameter, iParameter) in enumerate(zip(parameters, instruction["params"])):
      loadedInstruction["params"][i]["address"] = parameter
      if iParameter["mode"] == "position":
        loadedInstruction["params"][i]["value"] = self.RAM[parameter]
      else:
        loadedInstruction["params"][i]["value"] = parameter
    return loadedInstruction

  def enqueueInput(self, value):
    if not isinstance(value, list):
      value = [value]
    self.inputQueue.extend(value)

  def doOperation(self, debug=False):
    instruction = self.parseInstruction(self.RAM[self.instructionPtr])
    if debug:
      print(self.RAM[self.instructionPtr:self.instructionPtr + 10])
    self.instructionPtr += 1
    if not instruction:
      return
    func = self.opTable.get(instruction["opcode"])
    if func is None:
      return
    parameters = [
      parameter
      for parameter in
      self.RAM[self.instructionPtr: self.instructionPtr + instruction["nparams"]]
    ]
    self.instructionPtr += instruction["nparams"]
    loadedInstruction = self.processParameters(parameters, instruction)
    args = [param for param in loadedInstruction["params"]]
    func(*args)
    if debug:
      print(json.dumps(loadedInstruction))
      self.printState()


def tryPhases(computer, phases):
  signal = 0
  for phase in phases:
    computer.reset()
    computer.enqueueInput([phase, signal])
    while computer.output is None and not computer.halt:
      computer.doOperation(debug=False)
    signal = computer.output
  return signal

def simpleIO(program, input_):
  computer = IntCodeCPU(program)
  computer.enqueueInput(input_)
  while not computer.halt:
    computer.doOperation(debug=False)
  return computer.output

# TESTS ======================================================
assert(simpleIO(testmem4,1) == 13787043)
print("INPUT MODE TEST PASSED")
assert(simpleIO([3,9,8,9,10,9,4,9,99,-1,8],8) == 1)
assert(simpleIO([3,9,8,9,10,9,4,9,99,-1,8],7) == 0)
print("POSITION MODE EQUALITY TESTS PASSED")
assert(simpleIO([3,9,7,9,10,9,4,9,99,-1,8],7) == 1)
assert(simpleIO([3,9,7,9,10,9,4,9,99,-1,8],8) == 0)
print("POSITION MODE LESSTHAN TESTS PASSED")
assert(simpleIO([3,3,1108,-1,8,3,4,3,99],8) == 1)
assert(simpleIO([3,3,1108,-1,8,3,4,3,99],7) == 0)
print("IMMEDIATE MODE EQUALITY TESTS PASSED")
assert(simpleIO([3,3,1107,-1,8,3,4,3,99],7) == 1)
assert(simpleIO([3,3,1107,-1,8,3,4,3,99],8) == 0)
print("IMMEDIATE MODE LESSTHAN TESTS PASSED")
assert(simpleIO([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],1) == 1)
assert(simpleIO([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],0) == 0)
print("POSITION MODE JUMP TESTS PASSED")
assert(simpleIO([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],0) == 0)
assert(simpleIO([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],1) == 1)
print("IMMEDIATE MODE JUMP TESTS PASSED")
assert(simpleIO(testmem4,5) == 3892695)
print("5.1 5.2 PASSED")
assert(tryPhases(IntCodeCPU(
  [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]), [4,3,2,1,0]) == 43210)
assert(tryPhases(IntCodeCPU([3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0]), [0,1,2,3,4]) == 54321)
assert(tryPhases(IntCodeCPU([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]), [1,0,4,3,2]) == 65210)
print("7.1 SAMPLE TESTS PASSED")
outputs = set()
for phases in permutations([1,2,3,4,0]):
  output = tryPhases(IntCodeCPU(program), phases)
  outputs.add(output)
assert(max(outputs) == 46248)
print("7.1 PASSED")
#============================================================
print("***ALL TESTS PASSED***\n\n")


