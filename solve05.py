from aocd import submit, get_data


def main():
    day = 5
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "dabAcCaCBAcCcaDA": 10,
    }
    test_data_b = {
        "dabAcCaCBAcCcaDA": 4,
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
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"

    new = []
    again = True
    while again:
        again = False
        gen = iter(range(len(data)-1))
        for i in gen:
            if (not (data[i].islower() and data[i+1] == upper[lower.index(data[i])])
                and not (data[i].isupper() and data[i+1] == lower[upper.index(data[i])])):
                new.append(data[i])
            else:
                try:
                    next(gen)
                except StopIteration:
                    break
                again = True
        else:
            new.append(data[-1])
        data = new
        new = []
    return len(data)


def solve_b(data):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"

    pols = {}
    for c in set(data.lower()):
        old = data
        new = []
        again = True
        old = old.replace(c, "")
        old = old.replace(c.upper(), "")
        while again:
            again = False
            gen = iter(range(len(old)-1))
            for i in gen:
                if (not (old[i].islower() and old[i+1] == upper[lower.index(old[i])])
                    and not (old[i].isupper() and old[i+1] == lower[upper.index(old[i])])):
                    new.append(old[i])
                else:
                    try:
                        next(gen)
                    except StopIteration:
                        break
                    again = True
            else:
                new.append(old[-1])
            old = new
            new = []
        print(c, len(old))
        pols[c] = len(old)
    print(pols)
    return min(pols.values())


if __name__ == "__main__":
    main()
