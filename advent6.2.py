total = 0
# with open('orbits2', 'r') as f:
#     orbits = {tuple(o.strip('\n').split(')')) for o in f}
orbits = [ 
    ('COM','B'),
    ('B','C'),
    ('C','D'),
    ('D','E'),
    ('E','F'),
    ('B','G'),
    ('G','H'),
    ('D','I'),
    ('E','J'),
    ('J','K'),
    ('K','L'),
    ('K','YOU'),
    ('I','SAN')
]


leaves = {
    l for l in {
        orbiter[1] for orbiter in orbits
    } if l not in {
        orbited[0] for orbited in orbits
    }
}

paths_to_com = {}

def maptree(oed, l, steps):
    global total
    total += l
    paths_to_com[oed] = set(steps)
    if oed in leaves:
        return {oed: None}
    oedoers = [o[1] for o in orbits if o[0] == oed]
    oedd = {
        oer: maptree(oer, l + 1, steps + [oed])
        for oer in oedoers
    }
    return oedd


maptree('COM', 0, ['COM'])

print(f"total orbits: {total}")
print(f"transfers: {len(paths_to_com['SAN'] & paths_to_com['YOU'])}")



