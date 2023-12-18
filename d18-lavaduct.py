
from typing import List, Tuple

directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

direction_list = ["R", "D", "L", "U"]


def parse(s: str) -> Tuple[str, int, str]:
    d, v, color = s.split(" ")
    return d, int(v), color

def parse_color(color: str) -> Tuple[str, int]:
    color = color[1:-1]
    v = int(f"0x{color[1:-1]}", 16)
    d = direction_list[int(color[-1])]
    return d, v


def part1(instruct: List[str], use_color=False) -> int:
    parsed = []
    max_left = 0
    max_right = 0
    max_up = 0
    max_down = 0
    ci, cj = 0, 0
    for inst in instruct:
        d, v, color = parse(inst)
        parsed.append((d, v, color))
        if d == "L":
            cj -= v
        elif d == "R":
            cj += v
        elif d == "U":
            ci -= v
        else:
            ci += v
        max_left = max(max_left, -1 * cj)
        max_right = max(max_right, cj)
        max_up = max(max_up, -1 * ci)
        max_down = max(max_down, ci)
    
    si = max_up
    sj = max_left

    ci, cj = si, sj

    a = 1
    for d, v, color in parsed:
        if use_color:
            d, v = parse_color(color)
        if d == "D":
            a += cj * v
            
        elif d == "U":
            a -= cj * v
            a += v
        elif d == "R":
            a += v
        di, dj = directions[d]
        ci += di * v
        cj += dj * v
    return a


if __name__ == "__main__":
    file_name = "d18-input.text"
    file_name = "test_input.text"
    instruct = []
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            instruct.append(line.strip())
            line = f.readline()
    
    print(part1(instruct))
    print(part1(instruct, use_color=True))