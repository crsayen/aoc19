from intCpu import IntCodeCPU
from itertools import permutations
from mem3 import mem

computer = IntCodeCPU(mem)

outputs = set()
for phases in permutations([0,1,2,3,4]):
  signal = 0
  for phase in phases:
    computer.clearRAM()
    computer.clearInputQueue()
    computer.enqueueInput([phase, signal])
    while computer.output is None and not computer.halt:
      print(computer.doOperation(debug=True))
      computer.printState()
    signal = computer.output
  outputs.add(signal)

print(max(outputs))