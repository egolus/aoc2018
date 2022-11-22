from aocd import submit, get_data


def main():
    day = 2
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "abcdef": 0,
        "bababc": 1,
        "abbcde": 0,
        "abcccd": 0,
        "aabcdd": 0,
        "abcdee": 0,
        "ababab": 0,
    }
    test_data_b = {
        """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""": "fgij",
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
    twos = 0
    threes = 0
    for line in data.splitlines():
        twoFound, threeFound = False, False
        for c in set(line):
            count = len([x for x in line if x == c])
            if count == 2 and not twoFound:
                twoFound = True
                twos += 1
            if count == 3 and not threeFound:
                threeFound = True
                threes += 1

    print(f"twos: {twos}, threes: {threes}")
    return twos * threes


def solve_b(data):
    boxes = data.splitlines()
    for i, box in enumerate(boxes):
        for other in boxes[i:]:
            diff = len([c for j, c in enumerate(box) if c != other[j]])
            if diff == 1:
                return "".join([c for j, c in enumerate(box) if c == other[j]])


if __name__ == "__main__":
    main()
