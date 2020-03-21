import sys
from itertools import permutations
#from mem3 import mem
mem = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#from instructions5_1 import mem
HALT, FEEDBACK = False, False
INPUTS = []
MAXTHRUST = 0
IMEMS = [mem.copy()] * 5
AMP = 0
INIT = True
i = e = o = m = p = d = OUT = 0

modeselect = lambda m: {
    0: lambda param: IMEMS[AMP][param],
    1: lambda param: param
}.get(m)

nparams = [3,3,3,1,1,2,2,3,3] + [0] * 99

def jump_true(a):
    global i
    if a != 0:
        i = modeselect(m[-1])(d) - i
    else:
        i = 3
    return "jump"

def jump_false(a):
    global i
    if a == 0:
        i = modeselect(m[-1])(d) - i
    else:
        i = 3
    return "jump"

def inp():
    global IMEMS, INPUTS, INIT
    if INIT:
        INIT = False
        return None
    loc = IMEMS[AMP][i + 1]
    inp = INPUTS.pop(0)
    IMEMS[AMP][loc] = inp
    return None

opselect = lambda op: {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: inp,
    4: "output",
    5: jump_true,
    6: jump_false,
    7: lambda a, b: 1 if a < b else 0,
    8: lambda a, b: 1 if a == b else 0,
    99: "halt"
}.get(op)

def do(ptr):
    global i,m,d,OUT,HALT,INPUTS, INIT
    print(f"\n{IMEMS[AMP][ptr: ptr + 10]}")
    m=d=0
    e = str(IMEMS[AMP][ptr])
    o, m = int(''.join(e[-2:])), [ int(c) for c in e[-3::-1] ]
    m = ((m + [0] * (nparams[o] - len(m))))
    if any(map(lambda x: x > 1, m)): o = 0
    p,d = IMEMS[AMP][ptr + 1: ptr + nparams[o]],  IMEMS[AMP][ptr + nparams[o]]
    print(f"\n{i=}\n{e=}\n{o=}\n{m=}\n{p=}\n{d=}\n{OUT=}\n{INPUTS=}\n")
    if (f := opselect(o)) is not None:
        if f == "output":
            OUT = modeselect(m[-1])(d)
            #print(f"\n\n{OUT}\n\n")
            if FEEDBACK:
                INPUTS.append(OUT)
        elif f == "halt":
            HALT = True
            return 1
        else:
            if (r := f(*[ modeselect(_m)(p) for (_m,p) in zip(m, p) ])) == "jump":
                return i
            if r is not None:
                IMEMS[AMP][d] = r
    return nparams[o] + 1


def incrAmp():
    global AMP, INIT
    AMP = AMP + 1 if AMP < 4 else 0

def initAmp(phase):
    if len(PHASES):
        INPUTS = [phase]
        i = 0
        while INIT:
            i += do(i)
        return True
    return False


for nperm, PERMUTATION in enumerate(list(permutations([5,6,7,8,9]))):
    print(nperm)
    i = 0

    INPUTS = []
    PHASES = list(PERMUTATION)
    INPUTS.extend(PHASES)
    while len(INPUTS):
        i+= do(i)
    FEEDBACK = True

    print("done with some \n\n\n\n\n")
    INPUTS.append(0)
    while 1:
        i = 0
        while not HALT:
            #print(f"{OUT=}")
            i+= do(i)
        HALT = False
        #INPUTS.append(0)
    MAXTHRUST = OUT if OUT > MAXTHRUST else MAXTHRUST
print(MAXTHRUST)