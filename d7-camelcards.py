
from functools import cmp_to_key
from enum import Enum


labels = [
    "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2",
]

labels_hierarchy = {
    l: i for i, l in enumerate(labels)
}

class Hand(Enum):
    FIVE_A_KIND = 0
    FOUR_A_KIND = 1
    FULL_HOUSE = 2
    THREE_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6

hand_hierarcy = {
    h: i for i, h in enumerate(Hand) 
}


def get_hand_with_joker(hand: str, joker="J"):
    if joker not in hand:
        return get_hand(hand)
    
    letters = set(hand)
    letter_count = {}
    for l in letters:
        letter_count[l] = hand.count(l)
    joker_count = letter_count[joker]
    max_count = max(letter_count.values())
    if max_count == 5:
        return Hand.FIVE_A_KIND
    elif max_count == 4:
        return Hand.FIVE_A_KIND
    elif max_count == 3:
        if len(letter_count) == 2:
            return Hand.FIVE_A_KIND
        else:
            return Hand.FOUR_A_KIND
    elif max_count == 2:
        if len(letter_count) == 3:
            if joker_count == 1:
                return Hand.FULL_HOUSE
            elif joker_count == 2:
                return Hand.FOUR_A_KIND
        else:
            return Hand.THREE_A_KIND
    if joker_count == 1:
        return Hand.ONE_PAIR
    return Hand.HIGH_CARD


def compare_equal_hand_joker(hand1, hand2, joker="J") -> int:
    for h1, h2 in zip(hand1, hand2):
        v1, v2 = labels_hierarchy[h1], labels_hierarchy[h2]
        if h1 == joker:
            v1 = len(labels) + 1
        if h2 == joker:
            v2 = len(labels) + 1
        if v2 > v1:
            return -1
        elif v2 < v1:
            return 1
    return 0


def get_hand(hand: str) -> Hand:
    letters = set(hand)
    letter_count = {}
    for l in letters:
        letter_count[l] = hand.count(l)
    max_count = max(letter_count.values())
    if max_count == 5:
        return Hand.FIVE_A_KIND
    elif max_count == 4:
        return Hand.FOUR_A_KIND
    elif max_count == 3:
        if len(letter_count) == 2:
            return Hand.FULL_HOUSE
        else:
            return Hand.THREE_A_KIND
    elif max_count == 2:
        if len(letter_count) == 3:
            return Hand.TWO_PAIR
        else:
            return Hand.ONE_PAIR
    return Hand.HIGH_CARD

def compare_equal_hand(hand1, hand2) -> int:
    for h1, h2 in zip(hand1, hand2):
        v1, v2 = labels_hierarchy[h1], labels_hierarchy[h2]
        if v2 > v1:
            return -1
        elif v2 < v1:
            return 1
    return 0


def compare(v1, v2):
    hand1, _ = v1
    hand2, _ = v2
    h1, h2 = get_hand(hand1), get_hand(hand2)

    v1, v2 = hand_hierarcy[h1], hand_hierarcy[h2]
    if v2 > v1:
        return -1
    elif v2 < v1:
        return 1
    return compare_equal_hand(hand1, hand2)


def compare_joker(v1, v2, joker="J"):
    hand1, _ = v1
    hand2, _ = v2
    h1, h2 = get_hand_with_joker(hand1, joker), get_hand_with_joker(hand2, joker)
    if joker in hand1 or joker in hand2:
        print(hand1, hand2, h1, h2)
    v1, v2 = hand_hierarcy[h1], hand_hierarcy[h2]
    if v2 > v1:
        return -1
    elif v2 < v1:
        return 1
    return compare_equal_hand_joker(hand1, hand2, joker)
    


def part1(hands_with_bid) -> int:
    res = 0
    sorted_hands_with_bid = sorted(hands_with_bid, key=cmp_to_key(compare))
    for i, (h, b) in enumerate(sorted_hands_with_bid):
        res += b * (len(sorted_hands_with_bid) - i)
    return res

def part2(hands_with_bid) -> int:
    res = 0
    sorted_hands_with_bid = sorted(hands_with_bid, key=cmp_to_key(compare_joker))
    for i, (h, b) in enumerate(sorted_hands_with_bid):
        res += b * (len(sorted_hands_with_bid) - i)
    print(sorted_hands_with_bid[:100])
    return res

if __name__ == "__main__":
    # file_name = "d7-test.text"
    file_name = "d7-input.text"
    hands = []
    bids = []

    with open(file_name, 'r') as f:
        line = f.readline()
        i = 0
        while line:
            hand, bid = line.split()
            hands.append(hand)
            bids.append(int(bid))
            line = f.readline()
            i += 1
    
    hands_with_bid = [(hand, bid) for hand, bid in zip(hands, bids)]

    print(part1(hands_with_bid))    
    print(part2(hands_with_bid))
