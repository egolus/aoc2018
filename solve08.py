from aocd import submit, get_data


def main():
    day = 8
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2": 1+1+2+10+11+12+2+99,
    }
    test_data_b = {
        "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2": 33+33+0,
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


def getPacket(data):
    metadata = []
    numpackets = int(data.pop(0))
    numMeta = int(data.pop(0))
    for packet in range(numpackets):
        metadata += getPacket(data)
    for meta in range(numMeta):
        metadata.append(int(data.pop(0)))
    return metadata


def solve_a(data):
    return sum(getPacket(data.split()))


def getPacket_b(data):
    value = 0
    numpackets = int(data.pop(0))
    numMeta = int(data.pop(0))
    metadata = []
    packets = [getPacket_b(data) for _ in range(numpackets)]
    for _ in range(numMeta):
        meta = int(data.pop(0))
        metadata.append(meta)
        if len(packets) > meta-1:
            value += packets[meta-1]
    if numpackets:
        return value
    return sum(metadata)


def solve_b(data):
    return getPacket_b(data.split())


if __name__ == "__main__":
    main()
