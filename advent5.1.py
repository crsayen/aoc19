import sys
from instructions5_1 import mem

i = e = o = m = p = d = 0

modeselect = lambda m: {
    0: lambda param: mem[param],
    1: lambda param: param
}.get(m)

nparams = [3,3,3,1,1] + [0] * 99

opselect = lambda op: {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: lambda: 1,
    4: "print",
    99: "halt"
}.get(op)

def do(ptr):
    e = str(mem[ptr])
    o, m = int(''.join(e[-2:])), [ int(c) for c in e[-3::-1] ]
    m = ((m + [0] * (nparams[o] - len(m))))
    p,d = mem[ptr + 1: ptr + nparams[o]],  mem[ptr + nparams[o]]
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


