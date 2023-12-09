from typing import List

def predict_next(seq: List[int]) -> int:
    def recurse(seq: List[int]) -> int:
        if all(v == 0 for v in seq):
            return 0
        diff = []
        for i in range(len(seq) - 1):
            diff.append(seq[i + 1] - seq[i])
        return seq[-1] + recurse(diff)
    return recurse(seq)

def predict_prev(seq: List[int]) -> int:
    def recurse(seq: List[int]) -> int:
        if all(v == 0 for v in seq):
            return 0
        diff = []
        for i in range(len(seq) - 1):
            diff.append(seq[i + 1] - seq[i])
        return seq[0] - recurse(diff)
    return recurse(seq)


def part1(sequences: List[List[int]]) -> int:
    res = 0
    for seq in sequences:
        res += predict_next(seq)
    return res

def part2(sequences: List[List[int]]) -> int:
    res = 0
    for seq in sequences:
        res += predict_prev(seq)
    return res

if __name__ == "__main__":
    file_name = 'd9-input.text'
    sequences = []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            sequences.append([int(l) for l in line.strip().split()])
            line = f.readline()
    
    print(part1(sequences))
    print(part2(sequences))