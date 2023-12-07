import functools

def eqn(x, T):
    """
    f(x, T) = (T - x) * x = x * T - x ** 2
    df/dx = T - 2 * x
    if df/dx = 0
    T - 2 * x = 0
    T / 2 = X
    """
    return x * T - x ** 2

def part1(time, distance):
    res = []
    for t, d in zip(time, distance):
        v = 0
        for x in range(t):
            if eqn(x, t) > d:
                v += 1
        res.append(v)
    return functools.reduce(lambda a, b: a * b, res)

# def part2(time: int, distance: int):




if __name__ == "__main__":
    file_name = "d6-input.text"

    with open(file_name, 'r') as f:
        time = [int(i) for i in f.readline().split(":")[1].split()]
        distance = [int(i) for i in f.readline().split(":")[1].split()]
    
    print(time, distance)
    print(part1(time, distance))

    time2 = int(functools.reduce(lambda a, b: a + b, [str(i) for i in time]))
    distance2 = int(functools.reduce(lambda a, b: a + b, [str(i) for i in distance]))

    print(time2, distance2)