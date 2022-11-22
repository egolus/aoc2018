from aocd import submit, get_data


def main():
    day = 1
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """+1
-2
+3
+1""": 3,
        """+1
+1
+1""": 3,
        """+1
+1
-2""": 0,
        """-1
-2
-3""": -6,
    }
    test_data_b = {
        """+1
-2
+3
+1""": 2,
        """+1
-1""": 0,
        """+3
+3
+4
-2
-4""": 10,
        """-6
+3
+8
+5
-6""": 5,
        """+7
+7
-2
-7
-4""": 14,
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
    for line in data.splitlines():
        res += int(line)
    return res


def solve_b(data):
    res = {0}
    freq = 0
    while True:
        for line in data.splitlines():
            freq += int(line)
            if freq in res:
                return freq
            res.add(freq)



if __name__ == "__main__":
    main()
