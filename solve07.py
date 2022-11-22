from aocd import submit, get_data


def main():
    day = 7
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""": "CABDFE",
    }
    test_data_b = {
        ("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""", 2, 0): 15,
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


def solve_a(data):
    res = []
    steps = {}
    for line in data.splitlines():
        sline = line.split()
        x, y = sline[1], sline[7]
        if x not in steps:
            steps[x] = []
        if y in steps:
            steps[y].append(x)
        else:
            steps[y] = [x]
    while steps:
        step = sorted([k for k, v in steps.items() if not v])[0]
        res.append(step)
        steps.pop(step)
        for v in steps.values():
            if step in v:
                v.remove(step)
    return "".join(res)


def solve_b(data, numElves=5, timeNeeded=60):
    alphabeth = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    second = 0
    steps = {}
    workers = {x: [] for x in range(numElves)}
    for line in data.splitlines():
        sline = line.split()
        x, y = sline[1], sline[7]
        if x not in steps:
            steps[x] = []
        if y in steps:
            steps[y].append(x)
        else:
            steps[y] = [x]
    while steps or any(v for v in workers.values()):
        for w, v in workers.items():
            if not v:
                continue
            v[1] -= 1
            if v[1] == 0:
                workers[w] = []
                for x in steps.values():
                    if v[0] in x:
                        x.remove(v[0])
        for w in workers:
            if not workers[w]:
                try:
                    step = sorted([k for k, v in steps.items() if not v])[0]
                except IndexError:
                    break
                steps.pop(step)
                workers[w] = [step, timeNeeded + alphabeth.index(step) + 1]
        second += 1
    return second-1


if __name__ == "__main__":
    main()
