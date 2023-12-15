
import collections
from enum import Enum

class Op(Enum):
    DASH = "dash"
    EQUAL = "equal"


def hash_algo(s: str):
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res %= 256
    return res

def part1(steps):
    res = 0
    for step in steps:
        res += hash_algo(step)
    return res

def parse(s: str):
    label = []
    operator = None
    focal_length = None
    for idx, i in enumerate(s):
        if i == "=" or i == "-":
            if i == "=":
                operator = Op.EQUAL
                focal_length = int(s[idx + 1:])
            else:
                operator = Op.DASH
            break
        label.append(i)
    return "".join(label), hash_algo("".join(label)), operator, focal_length

def part2(steps):
    boxes = [collections.OrderedDict() for _ in range(256)]
    for step in steps:
        label, box_num, operator, focal_length = parse(step)
        if operator == Op.EQUAL:
            boxes[box_num][label] = focal_length
        else:
            if label in boxes[box_num]:
                boxes[box_num].pop(label)
    for i, b in enumerate(boxes):
        if b:
            print(i, b)
    res = 0
    for b, lenses in enumerate(boxes):
        for i, (label, focal) in enumerate(lenses.items()):
            res += ( b + 1 ) * ( i + 1) * focal
    
    return res




if __name__ == "__main__":
    file_name = "d15-input.text"
    # file_name = "test_input.text"

    with open(file_name, 'r') as f:
        steps = f.readline().strip().split(",")
    
    print(part1(steps))
    print(part2(steps))