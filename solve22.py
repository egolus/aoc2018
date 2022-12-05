import sys
from aocd import submit, get_data


def main():
    day = 22
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """depth: 510
target: 10,10""": 114,
    }
    test_data_b = {
        """depth: 510
target: 10,10""": 45,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    submit(result_b, part="b", day=day, year=year)


def geoIndex(grid, y, x, depth, target=None):
    if (y, x) == (0, 0):
        return 0
    elif target and (y, x) == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erosionLevel(grid[(y-1, x)], depth) * erosionLevel(grid[(y, x-1)], depth)


def erosionLevel(gi, depth):
    return (gi + depth) % 20183


def regionType(el):
    if el % 3 == 0:
        return "."  # rocky
    elif el % 3 == 1:
        return "="  # wet
    elif el % 3 == 2:
        return "|"  # narrow


def astar(grid, position, target):
    """
    a* from position to target

    third dimension is the currently used gear:
        0 = torch
        1 = climbing gear
        2 = neither

    gear available in regions:
        . (rocky)  - torch, climbing gear
        = (wet)    - climbing gear, neither
        | (narrow) - neither, torch

    returns the shortest path if available
    """
    gearAvailable = {
        0: ["c", "t"],
        1: ["c", "n"],
        2: ["t", "n"],
    }
    start = position
    goal = target
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        if current == goal:
            break
        openSet.remove(current)
        neighbors = {x: 1 for x in [
                (current[0]-1, current[1], current[2]),
                (current[0], current[1]-1, current[2]),
                (current[0], current[1]+1, current[2]),
                (current[0]+1, current[1], current[2]),
            ] if current[2] in gearAvailable[grid[(current[0], current[1])]]}

        neighbors[(current[0], current[1], [
            x for x in gearAvailable[grid[(current[0], current[1])]]
            if x != current[2]][0]
        )] = 7
        for neighbor, cost in neighbors.items():
            if neighbor[:2] not in grid:
                continue
            tentativeGScore = gScore[current] + cost
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)

    if current == goal:
        path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            path = [current] + path
        path.pop(0)
        return (path, fScore[goal])


def solve_a(data):
    # grid for geoIndex
    grid = {}

    lines = data.splitlines()
    depth = int(lines[0].split()[1])
    target = tuple(reversed([int(x) for x in lines[1].split()[1].split(",")]))

    for y in range(target[0] + 6):
        for x in range(target[1] + 6):
            grid[(y, x)] = geoIndex(grid, y, x, depth, target)

    return sum(sum(erosionLevel(grid[(y, x)], depth) % 3 for x in
                   range(target[1]+1)) for y in range(target[0]+1))


def solve_b(data):
    geoGrid = {}
    typeGrid = {}

    lines = data.splitlines()
    depth = int(lines[0].split()[1])
    target = tuple(reversed([int(x) for x in lines[1].split()[1].split(",")]))

    for y in range(target[0] + 20):
        for x in range(target[1] + 20):
            geoGrid[(y, x)] = geoIndex(geoGrid, y, x, depth, target)
            typeGrid[(y, x)] = erosionLevel(geoGrid[(y, x)], depth) % 3

    return astar(typeGrid, (0, 0, "t"), (*target, "t"))[1]


if __name__ == "__main__":
    main()
