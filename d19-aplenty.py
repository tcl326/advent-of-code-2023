from typing import List, Dict, Literal
import operator
import copy
import collections
import functools

operator_map = {
    ">": operator.gt,
    "<": operator.lt,
}


def parse_rules(rules: List[str]):
    parsed = collections.defaultdict(dict)
    for r in rules:
        name, r = r[:-1].split("{")
        conditions = []
        default = ""
        for c in r.split(","):
            if ":" not in c:
                default = c
            else:
                condition, dest = c.split(":")
                if ">" in condition:
                    op = operator.gt
                    i, value = condition.split(">")
                else:
                    op = operator.lt
                    i, value = condition.split("<")
                conditions.append((i, int(value), op, dest))
        parsed[name]["conditions"] = conditions
        parsed[name]["default"] = default

    return parsed


def parse_scores(scores: List[str]) -> List[Dict[str, int]]:
    parsed = []
    for score in scores:
        p = {}
        score = score[1: -1]
        for v in score.split(","):
            k, v = v.split("=")
            p[k] = int(v)
        parsed.append(p)
    return parsed


def part1(score_list, rule_map):

    def start(score, rule: str) -> Literal["A", "R"]:
        workflow = rule_map[rule]
        for k, v, op, dest in workflow["conditions"]:
            if op(score[k], v):
                if dest == "A" or dest == "R":
                    return dest
                else:
                    return start(score, dest)
        else:
            dest = workflow["default"]
            if dest == "A" or dest == "R":
                return dest
            else:
                return start(score, dest)
        raise ValueError("Should not have reached here")


    accepted = []
    rejected = []
    for score in score_list:
        r = start(score, "in")
        if r == "A":
            accepted.append(score)
        else:
            rejected.append(score)
    r = 0
    for a in accepted:
        r += sum(a.values())
    return r


def part2(rule_map):
    def start_range(score_ranges, rule):
        workflow = rule_map[rule]
        for k, v, op, dest in workflow["conditions"]:
            lower, upper = score_ranges[k]
            if op == operator.gt:
                n_lower, n_upper = lower, v + 1
                lower = v + 1
            else:
                n_lower, n_upper = v, upper
                upper = v
            n_score_ranges = copy.deepcopy(score_ranges)
            n_score_ranges[k] = (lower, upper)
            if dest == "A" or dest == "R":
                yield dest, n_score_ranges
            else:
                yield from start_range(n_score_ranges, dest)

            score_ranges[k] = (n_lower, n_upper)
        else:
            dest = workflow["default"]
            if dest == "A" or dest == "R":
                yield dest, score_ranges
            else:
                yield from start_range(score_ranges, dest)
    result = 0
    for r, ra in start_range({"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)}, "in"):
        print(r, ra)
        if r == "A":
            result += functools.reduce(lambda a, b: a * b, [v[1] - v[0] for v in ra.values()])
    return result


if __name__ == "__main__":
    file_name = "d19-input.text"
    rules = []
    scores = []
    with open(file_name, 'r') as f:
        line = f.readline().strip()
        while line:
            rules.append(line)
            line = f.readline().strip()

        line = f.readline().strip()
        while line:
            scores.append(line)
            line = f.readline().strip() 

    rule_map = parse_rules(rules)
    score_list = parse_scores(scores)
    # print(rule_map)
    # print(score_list)

    print(part1(score_list, rule_map))
    print(part2(rule_map))