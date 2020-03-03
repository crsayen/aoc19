dct = {
    "U": (0,1),
    "R": (1,0),
    "L": (-1,0),
    "D": (0,-1)
}

with open('wires', 'r') as f:
    wires = [
        list(map(lambda x: [dct.get(x[0]), int(x[1:])], 
        wire.split(',')
    )) for wire in f ]

points = [set(),set()]
intersections = set()

def addDist(point, dist, wire):
    if point in intersections:
        if visited.get(point) is None:
            visited[point] = {wire:dist}
        elif visited[point].get(wire) is None:
            visited[point][w] = dist
    return dist + 1

for p, wire in enumerate(wires):
    x, y = 0 , 0
    for line in wire:
        if line[0][0]:
            for xi in range(0, line[1]):
                x+= line[0][0]
                points[p].add((x, y))
        if line[0][1]:
            for yi in range(0, line[1]):
                y+= line[0][1]
                points[p].add((x,y))

mmd = 100000
for point in points[0]:
    if point in points[1]:
        intersections.add(point)
        md = abs(point[0] + point[1])
        if md < mmd:
            mmd = md
print(f"minimum manhattan distance: {mmd}")

visited = {(0,0):{0:1000000,1:1000000}}

for w, wire in enumerate(wires):
    dist = 0
    x, y = 0 , 0
    for line in wire:
        if line[0][0]:
            for xi in range(0, line[1]):
                dist = addDist((x,y), dist, w)
                x+= line[0][0]
        if line[0][1]:
            for yi in range(0, line[1]):
                dist = addDist((x,y), dist, w)
                y+= line[0][1]

mdti = {"point": (0,0), "dist":10000000}
for point, dist in visited.items():
    total = dist[0] + dist[1]
    if total < mdti["dist"]:
        mdti = {"point": point, "dist": total}

print(f"minimum distance to intersection: {mdti}")


