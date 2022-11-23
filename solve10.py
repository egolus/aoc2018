from aocd import submit, get_data


def main():
    day = 10
    year = 2018
    data = get_data(day=day, year=year)

    test_data_a = {
            """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""": "HI",
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
    points = []
    velocities = []

    for line in data.splitlines():
        sline = line.replace("<", " ").split()
        position = [int(sline[1][:-1]), int(sline[2][:-1])]
        velocity = [int(sline[4][:-1]), int(sline[5][:-1])]
        points.append(position)
        velocities.append(velocity)

    last = -1
    while True:
        for i, point in enumerate(points):
            point[0] += velocities[i][0]
            point[1] += velocities[i][1]
        minx = sorted(points, key=lambda x: x[0])[0][0]
        maxx = sorted(points, key=lambda x: x[0])[-1][0]
        miny = sorted(points, key=lambda x: x[1])[0][1]
        maxy = sorted(points, key=lambda x: x[1])[-1][1]
        new = abs(maxx-minx) + abs(maxy-miny)
        if last != -1 and new > last:
            for i, point in enumerate(points):
                point[0] -= velocities[i][0]
                point[1] -= velocities[i][1]
            for y in range(miny, maxy+1):
                for x in range(minx, maxx+1):
                    if [x, y] in points:
                        print("#", end="")
                    else:
                        print(" ", end="")
                print()
            print()
            return input("please read the answer: ")
        last = new


def solve_b(data):
    points = []
    velocities = []

    for line in data.splitlines():
        sline = line.replace("<", " ").split()
        position = [int(sline[1][:-1]), int(sline[2][:-1])]
        velocity = [int(sline[4][:-1]), int(sline[5][:-1])]
        points.append(position)
        velocities.append(velocity)

    last = -1
    second = 0
    while True:
        for i, point in enumerate(points):
            point[0] += velocities[i][0]
            point[1] += velocities[i][1]
        minx = sorted(points, key=lambda x: x[0])[0][0]
        maxx = sorted(points, key=lambda x: x[0])[-1][0]
        miny = sorted(points, key=lambda x: x[1])[0][1]
        maxy = sorted(points, key=lambda x: x[1])[-1][1]
        new = abs(maxx-minx) + abs(maxy-miny)
        if last != -1 and new > last:
            return second
        last = new
        second += 1


if __name__ == "__main__":
    main()
