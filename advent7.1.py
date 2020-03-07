import sys
from itertools import permutations
#from mem3 import mem
from instructions5_1 import mem
HALT = False
IPTR = 0
INPUTS = [5,0]
MAXTHRUST = 0
i = e = o = m = p = d = OUT = 0

modeselect = lambda m: {
    0: lambda param: imem[param],
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
    global imem, IPTR
    loc = imem[i + 1]
    inp = INPUTS[IPTR]
    imem[loc] = inp
    IPTR = int(not IPTR)
    return None

# def inp():
#     global imem
#     imem[225] = 5
#     return None

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
    global i,m,d,OUT,HALT,INPUTS
    print(f"\n{imem[ptr: ptr + 10]}")
    m=d=0
    e = str(imem[ptr])
    o, m = int(''.join(e[-2:])), [ int(c) for c in e[-3::-1] ]
    m = ((m + [0] * (nparams[o] - len(m))))
    p,d = imem[ptr + 1: ptr + nparams[o]],  imem[ptr + nparams[o]]
    print(f"\n{i=}\n{e=}\n{o=}\n{m=}\n{p=}\n{d=}\n{OUT=}\n{IPTR=}")
    if (f := opselect(o)) is not None:
        if f == "output":
            OUT = modeselect(m[-1])(d)
        elif f == "halt":
            HALT = True
        else:
            if (r := f(*[ modeselect(_m)(p) for (_m,p) in zip(m, p) ])) == "jump":
                return i
            if r is not None:
                imem[d] = r
    return nparams[o] + 1

imem = mem.copy()

while not HALT:
    i+= do(i)
print(OUT)

# for PERMUTATION in list(permutations([4,2,1,0,3])):
#     imem = mem.copy()
#     for PHASE in PERMUTATION:
#         #print(f"{PERMUTATION=}\n{PHASE=}")
#         i = 0
#         INPUTS[0] = PHASE
#         INPUTS[1] = OUT
#         #print(f"{INPUTS=}")
#         while not HALT:
#             i+= do(i)
#         HALT = False
#     MAXTHRUST = OUT if OUT > MAXTHRUST else MAXTHRUST
# print(MAXTHRUST)