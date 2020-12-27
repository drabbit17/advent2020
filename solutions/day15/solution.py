def problem15a(data, stop_point):
    numbers = [int(e) for e in data.split(",")]
    counter, last_time_memo = (
        len(numbers) - 1,
        {k: count for k, count in zip(numbers, range(1, len(numbers)))},
    )
    next_number = numbers[-1]

    while counter < stop_point - 1:
        last_count = last_time_memo.get(next_number, 0)
        counter += 1
        last_time_memo[next_number] = counter
        if last_count == 0:
            next_number = 0
        else:
            next_number = counter - last_count
    return next_number, last_time_memo
