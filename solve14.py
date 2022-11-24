from aocd import submit, get_data


def main():
    day = 14
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "9": "5158916779",
        "5": "0124515891",
        "18": "9251071085",
        "2018": "5941429882",
    }
    test_data_b = {
        "51589": 9,
        "01245": 5,
        "92510": 18,
        "59414": 2018,
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
    recs = [3, 7]
    elves = [0, 1]
    steps = int(data)

    while True:
        new = sum(recs[e] for e in elves)
        recs += [int(c) for c in str(new)]
        for i in range(len(elves)):
            elves[i] = (elves[i] + recs[elves[i]] + 1) % len(recs)
        if len(recs) == steps + 10:
            break
        elif len(recs) > steps + 10:
            recs.pop(-1)
            break
    return "".join(str(i) for i in recs[-10:])


def solve_b(data):
    recs = [3, 7]
    elves = [0, 1]
    target = list(int(c) for c in data)

    while True:
        new = sum(recs[e] for e in elves)
        recs += [int(c) for c in str(new)]
        for i in range(len(elves)):
            elves[i] = (elves[i] + recs[elves[i]] + 1) % len(recs)
        if recs[-len(target):] == target:
            return len(recs) - len(target)
        elif recs[-len(target)-1:-1] == target:
            return len(recs) - len(target) - 1


if __name__ == "__main__":
    main()
