from aocd import submit, get_data


def main():
    day = 18
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""": 1147,
    }
    test_data_b = {
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f" result a: {result_a}")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f" result b: {result_b}")
    submit(result_b, part="b", day=day, year=year)


def debug(grid, maxy, maxx):
    for y in range(maxy):
        for x in range(maxx):
            if (y, x) in grid:
                print(grid[(y, x)], end="")
            else:
                print(" ", end="")
        print()
    print()


def getAround(grid, y, x):
    return [
        grid[(y-1, x-1)] if (y-1, x-1) in grid else " ",
        grid[(y-1, x)] if (y-1, x) in grid else " ",
        grid[(y-1, x+1)] if (y-1, x+1) in grid else " ",
        grid[(y, x-1)] if (y, x-1) in grid else " ",
        grid[(y, x+1)] if (y, x+1) in grid else " ",
        grid[(y+1, x-1)] if (y+1, x-1) in grid else " ",
        grid[(y+1, x)] if (y+1, x) in grid else " ",
        grid[(y+1, x+1)] if (y+1, x+1) in grid else " ",
    ]


def update(grid, maxy, maxx):
    new = {}
    for y in range(maxy):
        for x in range(maxx):
            if (y, x) in grid:
                if grid[(y, x)] == "|":
                    # tree
                    if getAround(grid, y, x).count("#") >= 3:
                        new[(y, x)] = "#"
                    else:
                        new[(y, x)] = "|"
                elif grid[(y, x)] == "#":
                    # lumberyard
                    around = getAround(grid, y, x)
                    if around.count("#") >= 1 and around.count("|") >= 1:
                        new[(y, x)] = "#"
            else:
                # open field
                if getAround(grid, y, x).count("|") >= 3:
                    new[(y, x)] = "|"

    return new


def solve_a(data):
    grid = {}

    for y, line in enumerate(lines := data.splitlines()):
        for x, c in enumerate(line):
            if c in ["|", "#"]:
                grid[(y, x)] = c

    maxy = len(lines)
    maxx = len(lines[0])

    for m in range(10):
        grid = update(grid, maxy, maxx)
        # debug(grid, maxy, maxx)

    lumber = len([v for v in grid.values() if v == "#"])
    trees = len([v for v in grid.values() if v == "|"])
    return lumber * trees


def solve_b(data, minutes=1_000_000_000):
    grids = []
    grid = {}
    rest = 0

    for y, line in enumerate(lines := data.splitlines()):
        for x, c in enumerate(line):
            if c in ["|", "#"]:
                grid[(y, x)] = c
    grids.append(grid)

    maxy = len(lines)
    maxx = len(lines[0])

    for m in range(1, minutes + 1):
        grid = update(grid, maxy, maxx)
        if grid not in grids:
            grids.append(grid)
        else:
            target = grid
            rest = minutes - m
            break
    for m in range(rest):
        grid = update(grid, maxy, maxx)
        if grid == target:
            break
    for m in range((rest % (m+1))):
        grid = update(grid, maxy, maxx)
        lumber = len([v for v in grid.values() if v == "#"])
        trees = len([v for v in grid.values() if v == "|"])

    lumber = len([v for v in grid.values() if v == "#"])
    trees = len([v for v in grid.values() if v == "|"])
    return lumber * trees


if __name__ == "__main__":
    main()
