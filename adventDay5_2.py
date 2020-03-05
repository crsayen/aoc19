import sys
from instructions5_1 import mem

ID = 5

i = e = o = m = p = d = 0

modeselect = lambda m: {
    0: lambda param: mem[param],
    1: lambda param: param
}.get(m)

nparams = [3,3,3,1,1,2,2,3,3] + [0] * 99

def jump_true(a):
    if a != 0:
        i = modeselect(m[0])(p[0]) - 1

def jump_false(a):
    if a == 0:
        i = modeselect(m[0])(p[0]) - 1

opselect = lambda op: {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: lambda: 5,
    4: "print",
    5: jump_true,
    6: jump_false,
    7: lambda a, b: 1 if a < b else 0,
    8: lambda a, b: 1 if a == b else 0,
    99: "halt"
}.get(op)

def do(ptr):
    e = str(mem[ptr])
    o, m = int(''.join(e[-2:])), [ int(c) for c in e[-3::-1] ]
    m = ((m + [0] * (nparams[o] - len(m))))
    p,d = mem[ptr + 1: ptr + nparams[o]],  mem[ptr + nparams[o]]
    print(f"\n{i=}\n{e=}\n{o=}\n{m=}\n{p=}\n{d=}\n")
    if (f := opselect(o)) is not None:
        if f == "print":
            print(mem[mem[i + 1]])
        elif f == "halt":
            print(mem[0])
            sys.exit()
        else:
            mem[d] = f(*[ modeselect(m)(p) for (m,p) in zip(m, p) ])
    return nparams[o] + 1
   
while True:
    i+= do(i)


