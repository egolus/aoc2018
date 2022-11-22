from aocd import submit, get_data


def main():
    day = 6
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""": 17,
    }
    test_data_b = {
        ("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""", 32): 16,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(*test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    submit(result_b, part="b", day=day, year=year)


def manhatten(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


def solve_a(data):
    grid = {}
    coords = []
    for line in data.splitlines():
        x, y = line.split(", ")
        coords.append((int(x), int(y)))

    minx = min(p[0] for p in coords)
    maxx = max(p[0] for p in coords)
    miny = min(p[1] for p in coords)
    maxy = max(p[1] for p in coords)
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            dists = [(p[0], manhatten((x, y), p[1])) for p in enumerate(coords)]
            dists = sorted(dists, key=lambda p: p[1])
            if dists[0][1] == dists[1][1]:
                grid[(x, y)] = -1
            else:
                grid[(x, y)] = dists[0][0]
    sizes = {}
    for c in range(len(coords)):
        parea = [k for k, v in grid.items() if v == c]
        for p in parea:
            if p[0] == minx or p[0] == maxx or p[1] == miny or p[1] == maxy:
                break
        else:
            sizes[c] = len(parea)
    print(sizes)
    return max(sizes.values())


def solve_b(data, targetDistance=10000):
    target = []
    coords = []
    for line in data.splitlines():
        x, y = line.split(", ")
        coords.append((int(x), int(y)))

    minx = min(p[0] for p in coords)
    maxx = max(p[0] for p in coords)
    miny = min(p[1] for p in coords)
    maxy = max(p[1] for p in coords)
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            if sum(manhatten((x, y), p) for p in coords) < targetDistance:
                target.append((x, y))

    return len(target)


if __name__ == "__main__":
    main()
