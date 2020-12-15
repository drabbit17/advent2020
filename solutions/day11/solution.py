import functools
import itertools
import copy


def problem11a(data):
    grid_stable = False
    while not grid_stable:
        new_grid = change_signs_for_grid_problem11a(data, get_neighbors, 4)
        grid_stable = new_grid == data
        data = new_grid
    return sum([seat == "#" for row in data for seat in row])


def problem11b(data):
    grid_stable = False

    while not grid_stable:
        get_neighbors_function = functools.partial(get_neighbors_first_seat_seen, data=data)
        new_grid = change_signs_for_grid_problem11a(data, get_neighbors_function, 5)
        grid_stable = new_grid == data
        data = new_grid
    return sum([seat == "#" for row in data for seat in row])


def change_signs_for_grid_problem11a(data, get_neighbors_function, taken_seats_threshold):
    taken_sign, no_seat_sign, free_sign = "#", ".", "L"
    new_data = copy.deepcopy(data)
    for row_idx, row in enumerate(data):
        for e_idx, val in enumerate(row):
            if val != no_seat_sign:
                taken_seats = 0
                for x, y in get_neighbors_function(e_idx, row_idx):
                    if (0 <= x < len(data[0])) and (0 <= y < len(data)):
                        taken_seats += data[y][x] == taken_sign

                new_value = new_value_for_seat(
                    taken_seats, data[row_idx][e_idx], free_sign, taken_sign, taken_seats_threshold
                )
                if new_value:
                    new_data[row_idx] = (
                        new_data[row_idx][:e_idx] + new_value + new_data[row_idx][(e_idx + 1) :]  # noqa: E203
                    )
    return new_data


def new_value_for_seat(seats_taken, current_seat_value, free_sign, taken_sign, seats_taken_threshold):
    if seats_taken == 0 and current_seat_value:
        return taken_sign
    elif seats_taken >= seats_taken_threshold:
        return free_sign
    else:
        return None


def get_neighbors(x_val, y_val):
    possible_movements = list(itertools.permutations([1, -1, 0], 2)) + [(1, 1), (-1, -1)]
    return [(x_val + x_shift, y_val + y_shift) for x_shift, y_shift in possible_movements]


def get_neighbors_first_seat_seen(x_val, y_val, data):
    possible_movements = list(itertools.permutations([1, -1, 0], 2)) + [(1, 1), (-1, -1)]
    final_values = []
    for x_shift, y_shift in possible_movements:
        counter = 1
        new_x, new_y = x_val + x_shift * counter, y_val + y_shift * counter
        while (0 <= new_x < len(data[0])) and (0 <= new_y < len(data)) and (data[new_y][new_x] == "."):
            counter += 1
            new_x, new_y = x_val + x_shift * counter, y_val + y_shift * counter
        final_values.append((new_x, new_y))
    return final_values
