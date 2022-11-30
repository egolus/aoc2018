from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 17
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
"""x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""": 57,
"""x=496, y=5..7
x=500, y=5..7
x=492, y=3..9
x=508, y=3..9
y=9, x=492..508
y=7, x=496..500""": 113,
    }
    test_data_b = {
"""x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""": 29,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def debug(grid, miny, maxy, minx, maxx):
    for py in range(miny-1, maxy + 1):
        for px in range(minx-1, maxx + 1):
            if (py, px) in grid:
                print(grid[(py, px)], end="")
            else:
                print(" ", end="")
        print()
    print()


def genWater(grid, y, x, miny, maxy, minx, maxx):
    """ generate one layer of water """
    ty = y
    tx0 = x
    tx1 = x

    # filled up
    if (ty+1, x) in grid and grid[(ty+1, x)] != "|":
        return "filled"

    # down until we hit something
    while (ty+1, x) not in grid or grid[(ty+1, x)] == "|":
        if ty >= maxy:
            # we reached the imaginary bottom
            return "inf"
        ty += 1
        grid[(ty, x)] = "|"

    if (ty+1, x) in grid and grid[(ty+1, x)] == "+":
        return
    grid[(ty, x)] = "+"

    # left
    wallLeft = True
    breakLeft = False
    while ((ty, tx0-1) not in grid) or grid[(ty, tx0-1)] == "|":
        grid[(ty, tx0-1)] = "+"
        if (ty+1, tx0-1) not in grid:
            grid[(ty, tx0-1)] = "+"
            ret = True
            while ret:
                ret = genWater(grid, ty, tx0-1, miny, maxy, minx, maxx)
                if not ret:
                    wallLeft = False
                    breakLeft = True
                    break
                elif ret == "filled":
                    # debug(grid, miny, maxy, minx, maxx)
                    grid[(ty, tx0-1)] = "~"
                    break
                elif ret == "inf":
                    # debug(grid, miny, maxy, minx, maxx)
                    wallLeft = False
                    breakLeft = True
                    break
            if breakLeft:
                break
        tx0 -= 1

    # right
    wallRight = True
    breakRight = False
    while ((ty, tx1+1) not in grid) or grid[(ty, tx1+1)] == "|":
        grid[(ty, tx1+1)] = "+"
        if (ty+1, tx1+1) not in grid:
            grid[(ty, tx1+1)] = "+"
            ret = True
            while ret:
                ret = genWater(grid, ty, tx1+1, miny, maxy, minx, maxx)
                if not ret:
                    wallRight = False
                    breakRight = True
                    break
                elif ret == "filled":
                    # debug(grid, miny, maxy, minx, maxx)
                    grid[(ty, tx1+1)] = "~"
                    break
                elif ret == "inf":
                    # debug(grid, miny, maxy, minx, maxx)
                    return "inf"
            if breakRight:
                break
        tx1 += 1

    if wallLeft and wallRight:
        for x in range(tx0, tx1+1):
            grid[(ty, x)] = "~"
        return True


def solve_a(data):
    grid = {}

    for line in data.splitlines():
        a, b = line.split()
        f = a[0]
        a = int(a[2:-1])
        b = [int(bx) for bx in b[2:].split(".") if bx]
        if f == "x":
            for y in range(b[0], b[1]+1):
                grid[(y, a)] = "#"
        else:
            for x in range(b[0], b[1]+1):
                grid[(a, x)] = "#"

    minx, maxx = min(x for (y, x) in grid.keys()), max(x for (y, x) in grid.keys())
    miny, maxy = min(y for (y, x) in grid.keys()), max(y for (y, x) in grid.keys())

    grid[(0, 500)] = "+"
    again = True
    while again is True:
        again = False
        again = genWater(grid, 0, 500, miny, maxy, minx, maxx)
        # debug(grid, miny-1, maxy+1, minx-1, maxx+1)

    for y in range(miny):
        grid.pop((y, 500))
    pprint(sorted([(k, v) for k, v in grid.items() if k[0] < 10]))
    return len([v for v in grid.values() if v in ["~", "|", "+"]])


def solve_b(data):
    grid = {}

    for line in data.splitlines():
        a, b = line.split()
        f = a[0]
        a = int(a[2:-1])
        b = [int(bx) for bx in b[2:].split(".") if bx]
        if f == "x":
            for y in range(b[0], b[1]+1):
                grid[(y, a)] = "#"
        else:
            for x in range(b[0], b[1]+1):
                grid[(a, x)] = "#"

    minx, maxx = min(x for (y, x) in grid.keys()), max(x for (y, x) in grid.keys())
    miny, maxy = min(y for (y, x) in grid.keys()), max(y for (y, x) in grid.keys())

    grid[(0, 500)] = "+"
    again = True
    while again is True:
        again = False
        again = genWater(grid, 0, 500, miny, maxy, minx, maxx)
        # debug(grid, miny, maxy, minx, maxx)

    for py in range(miny-2, maxy + 3):
        for px in range(minx-2, maxx + 3):
            if (py, px) in grid:
                print(grid[(py, px)], end="")
            else:
                print(" ", end="")
        print()

    for y in range(miny):
        grid.pop((y, 500))
    pprint(sorted([(k, v) for k, v in grid.items() if k[0] < 10]))
    return len([v for v in grid.values() if v == "~"])


if __name__ == "__main__":
    main()
