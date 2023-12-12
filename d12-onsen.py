

def arrangements(onsen: str) -> int:
    record, groups = onsen.split()
    groups = [int(g) for g in groups.split(",")]
    memo = {}

    def recurse(ri, gi):
        if (ri, gi) in memo:
            return memo[(ri, gi)]
        g = groups[gi]
        if ri + g > len(record):
            memo[(ri, gi)] = 0
            return 0
        for ci in range(ri, ri + g):
            if record[ci] == "#" or record[ci] == "?":
                continue
            else:
                memo[(ri, gi)] = 0
                return 0
        if ri + g < len(record) and record[ri + g] == "#":
            return 0
        if gi == len(groups) - 1:
            if "#" not in record[ri + g:]:
                memo[(ri, gi)] = 1
                return 1
            memo[(ri, gi)] = 0
            return 0
        res = 0
        for j in range(ri, len(record)):
            res += recurse(j + g + 1, gi + 1)
            if j + g + 1 >= len(record) or record[j + g + 1] == "#":
                break
        memo[(ri, gi)] = res
        return res
    res = 0
    for i in range(len(record)):
        res += recurse(i, 0)
        if record[i] == "#":
            break
    return res


def part1(onsens):
    res = 0
    for onsen in onsens:
        v = arrangements(onsen)
        print(v, onsen)
        res += v
    return res


def unfold(onsens):
    res = []
    for onsen in onsens:
        record, groups = onsen.split()
        record = "?".join([record for _ in range(5)])
        groups = ",".join([groups for _ in range(5)])
        unfolded = record + " " + groups
        res.append(unfolded)
    return res


if __name__ == '__main__':
    file_name = "d12-input.text"
    # file_name = "test_input.text"
    onsens = []
    with open(file_name, 'r') as f:
        line = f.readline().strip()
        while line:
            onsens.append(line)
            line = f.readline().strip()
    
    print(part1(onsens))
    print(part1(unfold(onsens)))