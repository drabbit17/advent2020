import math


def problem13a(data):
    estimate, busses_ids = int(data[0]), data[1].split(",")
    valid_busses_ids = [int(e) for e in busses_ids if e != "x"]
    closest_bus, best_time_distance = None, math.inf
    for idx, bus_id in enumerate(valid_busses_ids):
        time_left = bus_id - estimate % bus_id
        if time_left < best_time_distance:
            best_time_distance = time_left
            closest_bus = (idx, bus_id, time_left)
    return closest_bus[1] * closest_bus[2]


def problem13b(data):
    """I had to kind of cheat to solve this one, haven't been able to find an efficient solution on my own"""
    busses = data[1].split(",")
    time, step = 0, int(busses[0])

    for t, bus_id in enumerate(busses[1:], start=1):
        if bus_id != "x":
            bus_id = int(bus_id)
        else:
            continue
        while (time + t) % bus_id != 0:
            time += step
        step *= bus_id
    return time
