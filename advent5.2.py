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
    global i
    print("jumped!")
    if a != 0:
        i = modeselect(m[-1])(d) - i
        return "jump"

def jump_false(a):
    global i
    print("jumped!")
    if a == 0:
        i = modeselect(m[-1])(d) - i
        return "jump"

def inp():
    global mem
    mem[255] = 1114
    return None

opselect = lambda op: {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: inp,
    4: "print",
    5: jump_true,
    6: jump_false,
    7: lambda a, b: 1 if a < b else 0,
    8: lambda a, b: 1 if a == b else 0,
    99: "halt"
}.get(op)

def do(ptr):
    global i,m,d
    m=d=0
    #print(mem[ptr: ptr + 10])
    e = str(mem[ptr])
    o, m = int(''.join(e[-2:])), [ int(c) for c in e[-3::-1] ]
    m = ((m + [0] * (nparams[o] - len(m))))
    p,d = mem[ptr + 1: ptr + nparams[o]],  mem[ptr + nparams[o]]
    #print(f"\n{i=}\n{e=}\n{o=}\n{m=}\n{p=}\n{d=}\n")
    if (f := opselect(o)) is not None:
        if f == "print":
            print(modeselect(m[-1])(d))
        elif f == "halt":
            #print(mem[0])
            sys.exit()
        else:
            if (r := f(*[ modeselect(_m)(p) for (_m,p) in zip(m, p) ])) == "jump":
                return i
            mem[d] = r
    return nparams[o] + 1
   
while True:
    i+= do(i)


