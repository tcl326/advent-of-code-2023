"""
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""
from typing import List, Tuple, Dict


letter_mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

reversed_letter_mapping = {reversed(letter): value for letter, value in letter_mapping.items()}


def get_first_digit(line: str) -> Tuple[int, int]:
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i]), i
    return 0, -1

def get_last_digit(line: str) -> Tuple[int, int]:
    for i in range(len(line) - 1, -1, -1):
        if line[i].isdigit():
            return int(line[i]), i
    return 0, -1

def get_first_letter_number(line: str) -> Tuple[int, int]:
    value = 0
    index = -1
    for letter, v in letter_mapping.items():
        i = line.find(letter)
        if i != -1 and (index == -1 or index > i):
            index = i
            value = v
    return value, index


def get_last_letter_number(line: str) -> Tuple[int, int]:
    value = 0
    index = -1
    for letter, v in letter_mapping.items():
        i = line.rfind(letter)
        if i != -1 and (index == -1 or index < i):
            index = i
            value = v
    return value, index


def get_calibration_corrected(line: str) -> int:
    dv, di = get_first_digit(line)
    lv, li = get_first_letter_number(line)
    first_v = 0
    if li != -1 and li < di:
        first_v = lv
    else:
        first_v = dv

    dv, di = get_last_digit(line)
    lv, li = get_last_letter_number(line)
    last_v = 0
    if li != -1 and li > di:
        last_v = lv
    else:
        last_v = dv

    return first_v * 10 + last_v

def get_calibration(line: str) -> int:
    return get_first_digit(line)[0] * 10 + get_last_digit(line)[0]


def part1(lines: List[str]) -> int:
    s = 0
    for line in lines:
        s += get_calibration(line)
    return s


def part2(lines: List[str]) -> int:
    s = 0
    for line in lines:
        s += get_calibration_corrected(line)
    return s


if __name__ == "__main__":
    file_name = "d1-trebuchet-input.text"

    with open(file_name) as f:
        lines = f.readlines()
        print("part1:", part1(lines))
        print("part2:", part2(lines))
