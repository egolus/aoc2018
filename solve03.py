from aocd import submit, get_data


def main():
    day = 3
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""": 4
    }
    test_data_b = {
        """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""": 3
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
    res = 0
    fabric = set()
    counted = set()
    for line in data.splitlines():
        sline = line.split()
        x = int(sline[2].split(",")[0])
        y = int(sline[2].split(",")[1][:-1])
        dx = int(sline[3].split("x")[0])
        dy = int(sline[3].split("x")[1])

        for tx in range(x, x+dx):
            for ty in range(y, y+dy):
                if (tx, ty) in fabric:
                    if not (tx, ty) in counted:
                        counted.add((tx, ty))
                        res += 1
                else:
                    fabric.add((tx, ty))
    return res


def solve_b(data):
    claims = set(range(1, len(data.splitlines())+1))
    fabric = {}
    for i, line in enumerate(data.splitlines(), start=1):
        sline = line.split()
        x = int(sline[2].split(",")[0])
        y = int(sline[2].split(",")[1][:-1])
        dx = int(sline[3].split("x")[0])
        dy = int(sline[3].split("x")[1])

        for tx in range(x, x+dx):
            for ty in range(y, y+dy):
                if (tx, ty) in fabric:
                    if i in claims:
                        claims.remove(i)
                    if fabric[(tx, ty)] in claims:
                        claims.remove(fabric[(tx, ty)])
                else:
                    fabric[(tx, ty)] = i
    return claims.pop()


if __name__ == "__main__":
    main()
