from aocd import submit, get_data


def main():
    day = 13
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/       """: "7,3",
    }
    test_data_b = {
        """/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/""": "6,4",
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
    cartTurns = "lsr"
    cartDirections = "lurd"
    carts = []
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c:
                if c == "<":
                    c = "-"
                    carts.append({"turn": 0, "direction": 0, "position": [x, y]})
                elif c == "^":
                    c = "|"
                    carts.append({"turn": 0, "direction": 1, "position": [x, y]})
                elif c == ">":
                    c = "-"
                    carts.append({"turn": 0, "direction": 2, "position": [x, y]})
                elif c == "v":
                    c = "|"
                    carts.append({"turn": 0, "direction": 3, "position": [x, y]})
                grid[(x, y)] = c

    for step in range(1000):
        for cart in sorted(carts, key=lambda x: x["position"]):
            if cart["direction"] == 0:
                cart["position"][0] -= 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 3
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 1
            elif cart["direction"] == 1:
                cart["position"][1] -= 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 2
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 0
            elif cart["direction"] == 2:
                cart["position"][0] += 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 1
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 3
            elif cart["direction"] == 3:
                cart["position"][1] += 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 0
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 2
            if grid[tuple(cart["position"])] == "+":
                cart["direction"] = (cart["direction"] + cart["turn"] - 1) % len(cartDirections)
                cart["turn"] = (cart["turn"] + 1) % len(cartTurns)

            if len([c["position"] for c in carts if c["position"] == cart["position"]]) >= 2:
                return ",".join(str(p) for p in cart["position"])


def solve_b(data):
    cartTurns = "lsr"
    cartDirections = "lurd"
    carts = []
    grid = {}

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c:
                if c == "<":
                    c = "-"
                    carts.append({"turn": 0, "direction": 0, "position": [x, y]})
                elif c == "^":
                    c = "|"
                    carts.append({"turn": 0, "direction": 1, "position": [x, y]})
                elif c == ">":
                    c = "-"
                    carts.append({"turn": 0, "direction": 2, "position": [x, y]})
                elif c == "v":
                    c = "|"
                    carts.append({"turn": 0, "direction": 3, "position": [x, y]})
                grid[(x, y)] = c

    step = 0
    while True:
        for cart in sorted(carts, key=lambda x: x["position"]):
            if cart["direction"] == 0:
                cart["position"][0] -= 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 3
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 1
            elif cart["direction"] == 1:
                cart["position"][1] -= 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 2
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 0
            elif cart["direction"] == 2:
                cart["position"][0] += 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 1
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 3
            elif cart["direction"] == 3:
                cart["position"][1] += 1
                if grid[tuple(cart["position"])] == "/":
                    cart["direction"] = 0
                if grid[tuple(cart["position"])] == "\\":
                    cart["direction"] = 2
            if grid[tuple(cart["position"])] == "+":
                cart["direction"] = (cart["direction"] + cart["turn"] - 1) % len(cartDirections)
                cart["turn"] = (cart["turn"] + 1) % len(cartTurns)

            crashed = [c["position"] for c in carts if c["position"] == cart["position"]]
            if len(crashed) >= 2:
                for i in range(len(carts)-1, -1, -1):
                    if carts[i]["position"] == cart["position"]:
                        carts.pop(i)
        if len(carts) == 1:
            return ",".join(str(p) for p in carts[0]["position"])
        step += 1


if __name__ == "__main__":
    main()
