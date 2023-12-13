
from typing import Tuple, List
from enum import Enum

class MirrorType(Enum):
    ROW = "row"
    COLUMN = "column"

def find_horizontal_mirror(pattern: List[str]) -> int:
    # for p in pattern:
    #     print(p)
    for i in range(1, len(pattern)):
        for c in range(i):
            if i + c >= len(pattern):
                return i
            if pattern[i - c - 1] != pattern[i + c]:
                break
        else:
            return i
    return -1


def find_horizontal_mirror_with_fix(pattern: List[str]) -> int:
    # for p in pattern:
    #     print(p)
    for i in range(1, len(pattern)):
        smudges = 0
        for c in range(i):
            if i + c >= len(pattern):
                if smudges == 1:
                    return i
                break
            for p1, p2 in zip(pattern[i - c - 1], pattern[i + c]):
                if p1 != p2:
                    smudges += 1
        else:
            if smudges == 1:
                return i
    return -1

def find_mirror_with_fix(pattern: List[str]) -> Tuple[MirrorType, int]:
    h = find_horizontal_mirror_with_fix(pattern)
    if h != -1:
        return MirrorType.ROW, h
    
    flipped = []
    for j in range(len(pattern[0])):
        l = []
        for i in range(len(pattern)):
            l.append(pattern[i][j])
        flipped.append("".join(l))
        
    h = find_horizontal_mirror_with_fix(flipped)
    if h != -1:
        return MirrorType.COLUMN, h
    raise ValueError("should not happen")


def find_mirror(pattern: List[str]) -> Tuple[MirrorType, int]:
    h = find_horizontal_mirror(pattern)
    if h != -1:
        return MirrorType.ROW, h
    
    flipped = []
    for j in range(len(pattern[0])):
        l = []
        for i in range(len(pattern)):
            l.append(pattern[i][j])
        flipped.append("".join(l))
        
    h = find_horizontal_mirror(flipped)
    if h != -1:
        return MirrorType.COLUMN, h
    raise ValueError("should not happen")


def part1(patterns):
    r, c = 0, 0
    for p in patterns:
        t, i = find_mirror(p)
        if t == MirrorType.ROW:
            r += i
        elif t == MirrorType.COLUMN:
            c += i
    return r * 100 + c

def part2(patterns):
    r, c = 0, 0
    for p in patterns:
        t, i = find_mirror_with_fix(p)
        if t == MirrorType.ROW:
            r += i
        elif t == MirrorType.COLUMN:
            c += i
    return r * 100 + c



if __name__ == "__main__":
    file_name = "d13-input.text"
    # file_name = "test_input.text"

    patterns = []
    with open(file_name, "r") as f:
        line = f.readline()
        pattern = []
        while line:
            l = line.strip()
            if not l:
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(l)
            line = f.readline()
        if pattern:
            patterns.append(pattern)
    # print(patterns)
    print(part1(patterns))
    print(part2(patterns))
