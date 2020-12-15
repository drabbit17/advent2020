import math
from typing import List


def problem_3a(data: List[str], horizontal_skips: List[int], vertical_skip: int = 1) -> List[int]:
    vals = []

    for skip in horizontal_skips:
        trees = 0
        pointer = 0
        horizontal_length = len(data[0])
        for row in data[::vertical_skip]:
            if row[pointer] == "#":
                trees += 1

            pointer += skip
            if pointer >= horizontal_length:
                pointer = pointer % horizontal_length

        vals.append(trees)
    return vals


def problem_3b(data: List[str]) -> List[int]:
    vals_1 = problem_3a(data, horizontal_skips=[1, 3, 5, 7], vertical_skip=1)
    vals_2 = problem_3a(data, horizontal_skips=[1], vertical_skip=2)
    return math.prod(vals_1) * math.prod(vals_2)
