from aocd import submit, get_data
from rich import print as pprint


def main():
    day = 16
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
        """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]""": 1,
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


def instruction(registers, opcode, a, b, c):
    registers = list(tuple(registers))
    print(f"instruction - registers: {registers}, opcode: {opcode}, {a}, {b}, {c}")
    if opcode == "addr":
        registers[c] = registers[a] + registers[b]
    elif opcode == "addi":
        registers[c] = registers[a] + b

    elif opcode == "mulr":
        registers[c] = registers[a] * registers[b]
    elif opcode == "muli":
        registers[c] = registers[a] * b

    elif opcode == "banr":
        registers[c] = registers[a] & registers[b]
    elif opcode == "bani":
        registers[c] = registers[a] & b

    elif opcode == "borr":
        registers[c] = registers[a] | registers[b]
    elif opcode == "bori":
        registers[c] = registers[a] | b

    elif opcode == "setr":
        registers[c] = registers[a]
    elif opcode == "seti":
        registers[c] = a

    elif opcode == "gtir":
        registers[c] = 1 if a > registers[b] else 0
    elif opcode == "gtri":
        registers[c] = 1 if registers[a] > b else 0
    elif opcode == "gtrr":
        registers[c] = 1 if registers[a] > registers[b] else 0

    elif opcode == "eqir":
        registers[c] = 1 if a == registers[b] else 0
    elif opcode == "eqri":
        registers[c] = 1 if registers[a] == b else 0
    elif opcode == "eqrr":
        registers[c] = 1 if registers[a] == registers[b] else 0
    return registers


def solve_a(data, target=3):
    unknown = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori",
               "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
    highSamples = 0

    before = []
    after = []
    instr = []
    data = data.split("\n\n\n")[0]
    for line in data.splitlines():
        if line.startswith("Before:"):
            before = [int(x) for x in line.split("[")[1][:-1].split(", ")]
        elif line.startswith("After:"):
            after = [int(x) for x in line.split("[")[1][:-1].split(", ")]
            behaves = 0
            print(f"before: {before}, after: {after}, instr: {instr}")
            for opcode in unknown:
                if (ret := instruction(before, opcode, *instr[1:])) == after:
                    behaves += 1
                print(ret, after)
            print(f"behaves like {behaves} opcodes")
            if behaves >= target:
                highSamples += 1
        elif line:
            instr = [int(x) for x in line.split()]

    return highSamples


def solve_b(data):
    registers = [0, 0, 0, 0]
    unknown = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori",
               "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
    opcodes = {i: set(unknown) for i in range(16)}

    before = []
    after = []
    instr = []
    data = data.split("\n\n\n\n")
    for line in data[0].splitlines():
        if line.startswith("Before:"):
            before = [int(x) for x in line.split("[")[1][:-1].split(", ")]
        elif line.startswith("After:"):
            after = [int(x) for x in line.split("[")[1][:-1].split(", ")]
            print(f"before: {before}, after: {after}, instr: {instr}")
            for opcode in list(opcodes[instr[0]]):
                if instruction(before, opcode, *instr[1:]) != after:
                    opcodes[instr[0]].remove(opcode)
                    print(f"droping {opcode} from {instr[0]}")
        elif line:
            instr = [int(x) for x in line.split()]

    out = {}
    while opcodes:
        for k, v in list(opcodes.items()):
            if len(v) == 1:
                opcodes.pop(k)
                x = list(v)[0]
                out[k] = x
                for val in opcodes.values():
                    val.discard(x)
        pprint(opcodes)

    pprint(out)

    for line in data[1].splitlines():
        instr = [int(x) for x in line.split()]
        print(instr)
        registers = instruction(registers, out[instr[0]], *instr[1:])

        print(registers)
    return registers[0]


if __name__ == "__main__":
    main()
