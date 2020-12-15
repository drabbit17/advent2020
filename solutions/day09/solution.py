def problem9a(data):
    start, end = 0, 25
    data = [int(e) for e in data]
    while end < len(data):
        container_check, good_set = set(), False
        candidates = data[start:end]
        for candidate in candidates:
            if (data[end] - candidate) not in container_check:
                container_check.add(data[end] - candidate)
        for candidate in candidates:
            if candidate in container_check and candidate != (data[end] - candidate):
                good_set = True
        if not good_set:
            return data[end]
        start += 1
        end += 1


def problem9b(data):
    result = problem9a(data)
    data = [int(e) for e in data]
    pointer_1, pointer_2 = 0, 1
    while pointer_2 < len(data):
        interval = data[pointer_1:pointer_2]
        interval_sum = sum(interval)
        if interval_sum == result:
            return min(interval) + max(interval)
        elif interval_sum > result:
            pointer_1 += 1
        if interval_sum < result:
            pointer_2 += 1
