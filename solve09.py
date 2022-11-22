from aocd import submit, get_data


def main():
    day = 9
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        "9 players; last marble is worth 25 points": 32,
        "10 players; last marble is worth 1618 points": 8317,
        "13 players; last marble is worth 7999 points": 146373,
        "17 players; last marble is worth 1104 points": 2764,
        "21 players; last marble is worth 6111 points": 54718,
        "30 players; last marble is worth 5807 points": 37305,
    }
    test_data_b = {
        "": True,
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
    numPlayers = int(data.split()[0])
    numMarbles = int(data.split()[6])

    circle = [0]
    players = [0 for _ in range(numPlayers)]
    activePlayer = 0
    position = 0

    for marble in range(1, numMarbles+1):
        if not marble % 23:
            players[activePlayer] += marble
            position = (position - 6) % len(circle)
            players[activePlayer] += circle.pop(position)
            position = (position - 1) % len(circle)
        else:
            position = (position + 2) % len(circle)
            circle = circle[:position+1] + [marble] + circle[position+1:]
        activePlayer = (activePlayer + 1) % len(players)
    return max(players)


def solve_b(data):
    pass


if __name__ == "__main__":
    main()
