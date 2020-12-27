import itertools


def problem17a(data, number_of_cycles, dimensions):
    data = [[[elem for elem in row] for row in data]]
    for _ in range(number_of_cycles):
        new_data = create_new_space_recursive(data)
        for z_idx, z in enumerate(new_data):
            for x_idx, x in enumerate(z):
                for y_idx, y in enumerate(x):
                    actives_count, z_idx_data, x_idx_data, y_idx_data = 0, z_idx - 1, x_idx - 1, y_idx - 1
                    for coor in get_coordinates(dimensions):
                        z_idx_check, x_idx_check, y_idx_check = (
                            z_idx_data + coor[0],
                            x_idx_data + coor[1],
                            y_idx_data + coor[2],
                        )
                        actives_count += access_element(data, [z_idx_check, x_idx_check, y_idx_check]) == "#"

                    current_value = access_element(data, [z_idx_data, x_idx_data, y_idx_data])
                    if actives_count == 3:
                        new_data[z_idx][x_idx][y_idx] = "#"
                    elif actives_count == 2 and current_value == "#":
                        new_data[z_idx][x_idx][y_idx] = "#"
        data = new_data

    return sum([e == "#" for plane in data for row in plane for e in row])


def problem17b(data, number_of_cycles, dimensions):
    data = [[[[elem for elem in row] for row in data]]]
    for _ in range(number_of_cycles):
        new_data = create_new_space_recursive(data)
        for w_idx, w in enumerate(new_data):
            for z_idx, z in enumerate(w):
                for x_idx, x in enumerate(z):
                    for y_idx, _ in enumerate(x):
                        actives_count, w_idx_data, z_idx_data, x_idx_data, y_idx_data = (
                            0,
                            w_idx - 1,
                            z_idx - 1,
                            x_idx - 1,
                            y_idx - 1,
                        )
                        for coor in get_coordinates(dimensions):
                            w_idx_check, z_idx_check, x_idx_check, y_idx_check = (
                                w_idx_data + coor[0],
                                z_idx_data + coor[1],
                                x_idx_data + coor[2],
                                y_idx_data + coor[3],
                            )
                            actives_count += (
                                access_element(data, [w_idx_check, z_idx_check, x_idx_check, y_idx_check])
                                == "#"
                            )

                        current_value = access_element(data, [w_idx_data, z_idx_data, x_idx_data, y_idx_data])
                        if actives_count == 3:
                            new_data[w_idx][z_idx][x_idx][y_idx] = "#"
                        elif actives_count == 2 and current_value == "#":
                            new_data[w_idx][z_idx][x_idx][y_idx] = "#"
        data = new_data

    return sum([e == "#" for space in data for plane in space for row in plane for e in row])


def drop_unused_borders(space):
    # clean north border
    while len(set([elem for plane in space for elem in plane[0]])) == 1:
        space = [[row for row in plane[1:]] for plane in space]
    # clean south border
    while len(set([elem for plane in space for elem in plane[-1]])) == 1:
        space = [[row for row in plane[:-1]] for plane in space]
    # clean east border
    while len(set([row[-1] for plane in space for row in plane])) == 1:
        space = [[row[:-1] for row in plane] for plane in space]
    # clean west border
    while len(set([row[0] for plane in space for row in plane])) == 1:
        space = [[row[1:] for row in plane] for plane in space]

    return space


def access_element(space, list_of_indexes):
    try:
        if list_of_indexes and list_of_indexes[0] < 0:
            raise IndexError
        elif len(list_of_indexes) > 1:
            return access_element(space[list_of_indexes[0]], list_of_indexes[1:])
        else:
            return space[list_of_indexes[0]]
    except IndexError:
        return "."


def create_new_space_recursive(current_dimension):
    if isinstance(current_dimension[0], list):
        return [create_new_space_recursive(current_dimension[0]) for _ in range(len(current_dimension) + 2)]
    else:
        return ["." for _ in range(len(current_dimension) + 2)]


def get_coordinates(dimensions):
    coordinates = list(itertools.product([0, -1, 1], repeat=dimensions))
    return [e for e in coordinates if set(e) != {0}]
