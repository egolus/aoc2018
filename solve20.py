from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 20
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "^WNE$": 3,
        "^ENWWW(NEEE|SSE(EE|N))$": 10,
        "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$": 18,
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
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    rooms = {}
    current = 0
    position = (0, 0)

    stack = [(0, 0)]
    for c in data:
        if c in ["^", "$"]:
            continue
        elif c == "W":
            target = (position[0], position[1] - 1)
        elif c == "E":
            target = (position[0], position[1] + 1)
        elif c == "N":
            target = (position[0] - 1, position[1])
        elif c == "S":
            target = (position[0] + 1, position[1])
        elif c == "(":
            # add to stack
            stack.append(position)
            continue
        elif c == ")":
            # pop from stack
            position = stack.pop(-1)
            current = rooms[position]["score"]
            continue
        elif c == "|":
            # move position to last stack position
            position = stack[-1]
            current = rooms[position]["score"]
            continue
        current += 1
        if target not in rooms or current < rooms[target]["score"]:
            rooms[target] = {"score": current, "from": position}
        position = target

    return max(v["score"] for v in rooms.values())


def solve_b(data):
    rooms = {(0, 0): set()}
    position = (0, 0)

    stack = [(0, 0)]
    for c in data:
        if c in ["^", "$"]:
            continue
        elif c == "W":
            target = (position[0], position[1] - 1)
        elif c == "E":
            target = (position[0], position[1] + 1)
        elif c == "N":
            target = (position[0] - 1, position[1])
        elif c == "S":
            target = (position[0] + 1, position[1])
        elif c == "(":
            # add to stack
            stack.append(position)
            continue
        elif c == ")":
            # pop from stack
            position = stack.pop(-1)
            continue
        elif c == "|":
            # move position to last stack position
            position = stack[-1]
            continue

        if target not in rooms:
            rooms[target] = {position}
        else:
            rooms[target].add(position)
        rooms[position].add(target)
        position = target

    new = updateRooms(rooms)
    big = sorted([r for r in new.values() if r >= 1000])
    return len(big)


def updateRooms(rooms, target=(0, 0), score=0):
    new = {}
    toUpdate = [(target, score)]
    while toUpdate:
        room, score = toUpdate.pop(0)
        if room in new:
            continue
        new[room] = score
        toUpdate.extend([(r, score + 1) for r in rooms[room]])
    return new


if __name__ == "__main__":
    main()
