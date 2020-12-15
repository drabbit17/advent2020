from typing import List


def problem_1a(data: List[str], target=2020) -> int:
    data = [int(e) for e in data]
    complementaries = {target - e: e for e in data}

    for e in data:
        if complementaries.get(e):
            return e * complementaries.get(e)


def problem_1b(data: List[str], target: int = 2020) -> int:
    data = sorted([int(e) for e in data])

    for idx, e in enumerate(data):
        low, high = idx + 1, len(data) - 1
        while low < high:
            if data[low] + data[idx] + data[high] > target:
                high -= 1
            elif data[low] + data[idx] + data[high] < target:
                low += 1
            else:
                return data[low] * data[idx] * data[high]
