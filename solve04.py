from collections import defaultdict
from aocd import submit, get_data


def main():
    day = 4
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""": 10*24,
    }
    test_data_b = {
        """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""": 99*45,
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
    rawevents = []
    events = {}
    guard = -1
    guards = defaultdict(lambda: defaultdict(int))
    for line in data.splitlines():
        sline = line.split()
        if "begins shift" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                int(sline[3][1:]),
                "guard",
            ))
        elif "falls asleep" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                "sleep",
            ))
        elif "wakes up" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                "wake",
            ))

    for event in sorted(rawevents):
        if event[-1] == "guard":
            guard = event[2]
            if guard not in events:
                events[guard] = []
        elif event[-1] == "sleep":
            events[guard].append((event[0], event[1], event[2]))
        elif event[-1] == "wake":
            events[guard].append((event[0], event[1], event[2]))

    for guard, gevents in events.items():
        f, t = 0, 0
        for event in gevents:
            if event[2] == "sleep":
                f = event[1][1]
            elif event[2] == "wake":
                t = event[1][1]
                for i in range(f, t):
                    guards[guard][i] += 1

    gm = -1
    for guard, times in guards.items():
        if gm == -1:
            gm = guard
            continue
        if sum(times.values()) > sum(guards[gm].values()):
            gm = guard
    mt = sorted(guards[gm].items(), reverse=True, key=lambda x: x[1])[0]
    return gm * mt[0]


def solve_b(data):
    rawevents = []
    events = {}
    guard = -1
    guards = defaultdict(lambda: defaultdict(int))
    for line in data.splitlines():
        sline = line.split()
        if "begins shift" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                int(sline[3][1:]),
                "guard",
            ))
        elif "falls asleep" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                "sleep",
            ))
        elif "wakes up" in line:
            rawevents.append((
                sline[0][1:],
                tuple([int(s) for s in sline[1][:-1].split(":")]),
                "wake",
            ))

    for event in sorted(rawevents):
        if event[-1] == "guard":
            guard = event[2]
            if guard not in events:
                events[guard] = []
        elif event[-1] == "sleep":
            events[guard].append((event[0], event[1], event[2]))
        elif event[-1] == "wake":
            events[guard].append((event[0], event[1], event[2]))

    for guard, gevents in events.items():
        f, t = 0, 0
        for event in gevents:
            if event[2] == "sleep":
                f = event[1][1]
            elif event[2] == "wake":
                t = event[1][1]
                for i in range(f, t):
                    guards[guard][i] += 1

    gm = (-1, 0)
    for guard, times in guards.items():
        mt = sorted(times.items(), reverse=True, key=lambda x: x[1])[0]
        if gm[0] == -1:
            gm = (guard, mt)
            continue
        if mt[1] > gm[1][1]:
            gm = (guard, mt)
    return gm[0] * gm[1][0]


if __name__ == "__main__":
    main()
