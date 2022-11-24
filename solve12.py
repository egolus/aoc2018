from aocd import submit, get_data
from pprint import pprint


def main():
    day = 12
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""": 325,
    }
    test_data_b = {
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


def solve_a(data, generations=20):
    pods = set()
    rules = {}
    lines = data.splitlines()
    for i, c in enumerate(lines[0].split()[2]):
        if c == "#":
            pods.add(i)

    for line in lines[2:]:
        sline = line.split()
        rules[sline[0]] = sline[2]
    for generation in range(generations):
        new = set()
        for pod in range(min(pods)-2, max(pods)+3):
            try:
                old = f"""{
                    '#' if pod-2 in pods else '.'}{
                    '#' if pod-1 in pods else '.'}{
                    '#' if pod in pods else '.'}{
                    '#' if pod+1 in pods else '.'}{
                    '#' if pod+2 in pods else '.'}"""
                if rules.get(old, ".") == "#":
                    new.add(pod)
            except KeyError:
                pass
        pods = new
    return sum(pods)


def solve_b(data, generations=50_000_000_000):
    split = 100
    pods = set()
    rules = {}
    lines = data.splitlines()
    for i, c in enumerate(lines[0].split()[2]):
        if c == "#":
            pods.add(i)

    for line in lines[2:]:
        sline = line.split()
        rules[sline[0]] = sline[2]
    for generation in range(min(split, generations)):
        new = set()
        print(generation, min(pods))
        for pod in range(min(pods)-2, max(pods)+3):
            try:
                old = f"""{
                    '#' if pod-2 in pods else '.'}{
                    '#' if pod-1 in pods else '.'}{
                    '#' if pod in pods else '.'}{
                    '#' if pod+1 in pods else '.'}{
                    '#' if pod+2 in pods else '.'}"""
                if rules.get(old, ".") == "#":
                    new.add(pod)
            except KeyError:
                pass
            print("#" if pod in new else ".", end="")
        print()
        pods = new
    if generations > split:
        new = set()
        for pod in pods:
            new.add(pod + (generations - split))
        pods = new
    return sum(pods)


if __name__ == "__main__":
    main()
