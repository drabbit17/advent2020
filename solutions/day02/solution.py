import collections
from typing import List


def problem_2a(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        letters = collections.Counter(e[1])
        if int(low) <= letters[letter] <= int(high):
            matches.append(e)
    return len(matches)


def problem_2b(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        low_l, high_l = e[1][int(low) - 1], e[1][int(high) - 1]
        if (int(low_l == letter) + int(high_l == letter)) == 1:
            matches.append(e)
    return len(matches)
