total = 0
with open('orbits', 'r') as f:
    orbits = {tuple(o.strip('\n').split(')')) for o in f}


leaves = {
    l for l in {
        orbiter[1] for orbiter in orbits
    } if l not in {
        orbited[0] for orbited in orbits
    }
}


def maptree(oed, l):
    global total
    total += l
    if oed in leaves:
        return {oed: None}
    oedoers = [o[1] for o in orbits if o[0] == oed]
    oedd = {
        oer: maptree(oer, l + 1)
        for oer in oedoers
    }
    return oedd


maptree('COM', 0)

print(total)
