from aocd import submit, get_data


def main():
    day = 11
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "18": "33,45",
    }
    test_data_b = {
        # "18": "90,269,16",
        "42": "232,251,12",
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


def solve_a(data):
    res = ((0, 0), 0)
    cells = {}
    for y in range(1, 301):
        for x in range(1, 301):
            rack = x + 10
            cells[(x, y)] = int(f"{((rack * y) + int(data)) * rack:0>3}"[-3]) - 5
    for y in range(1, 298):
        for x in range(1, 298):
            fuel = sum((
                cells[(x, y)], cells[(x+1, y)], cells[(x+2, y)],
                cells[(x, y+1)], cells[(x+1, y+1)], cells[(x+2, y+1)],
                cells[(x, y+2)], cells[(x+1, y+2)], cells[(x+2, y+2)],
            ))
            if fuel > res[1]:
                res = ((x, y), fuel)
    return ",".join([str(x) for x in res[0]])


def solve_b(data):
    res = ((0, 0, 0), 0)
    cells = [[]]
    for y in range(1, 301):
        line = []
        for x in range(1, 301):
            rack = x + 10
            line.append(int(f"{((rack * y) + int(data)) * rack:0>3}"[-3]) - 5)
        cells[0].append(line)

    for s in range(1, 300):
        for y in range(0, 300-s):
            for x in range(0, 300-s):
                fuel = sum((
                    cells[s-1][y][x],
                    sum(cells[0][y+s][x:x+s+1]),
                    sum(line[x+s] for line in cells[0][y:y+s+1])
                ))
                if len(cells) <= s:
                    cells.append([[fuel]])
                if len(cells[s]) <= y:
                    cells[s].append([fuel])
                if len(cells[s][y]) <= x:
                    cells[s][y].append(fuel)
                if fuel > res[1]:
                    res = ((x, y, s), fuel)
    return ",".join(str(x+1) for x in res[0])


if __name__ == "__main__":
    main()
