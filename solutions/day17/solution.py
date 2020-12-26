import itertools


def problem17a(data, number_of_cycles, dimensions):
    data = [[[elem for elem in row] for row in data]]
    for _ in range(number_of_cycles):
        new_data = create_new_space_recursive(data)
        for z_idx, z in enumerate(new_data):
            for x_idx, x in enumerate(z):
                for y_idx, y in enumerate(x):
                    actives_count, z_idx_data, x_idx_data, y_idx_data = 0, z_idx - 1, x_idx-1, y_idx-1
                    for coordinate in get_coordinates(dimensions):
                        z_idx_check, x_idx_check, y_idx_check = z_idx_data + coordinate[0], x_idx_data + coordinate[1], y_idx_data + coordinate[2]
                        actives_count += get_value_from_space(data, z_idx_check, x_idx_check, y_idx_check) == "#"

                    current_value = get_value_from_space(data, z_idx_data, x_idx_data, y_idx_data)
                    if actives_count == 3:
                        new_data[z_idx][x_idx][y_idx] = "#"
                    elif actives_count == 2 and current_value == "#":
                        new_data[z_idx][x_idx][y_idx] = "#"
        data = drop_unused_borders(new_data)

    return data


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

    # clean lowest plane
    while len(set([e for row in space[0] for e in row])) == 1:
        space = space[1:]
    # clean highest plane
    while len(set([e for row in space[-1] for e in row])) == 1:
        space = space[:-1]
    return space


def get_value_from_space(space, z, x, y):
    try:
        if z < 0 or x < 0 or y < 0:
            raise IndexError
        return space[z][x][y]
    except IndexError:
        return "."


def create_new_space_recursive(current_dimension):
    if isinstance(current_dimension[0], list):
        return [create_new_space_recursive(current_dimension[0]) for _ in range(len(current_dimension)+2)]
    else:
        return ["." for _ in range(len(current_dimension)+2)]


def get_coordinates(dimensions):
    coordinates = list(itertools.product([0, -1, 1], repeat=dimensions))
    return [e for e in coordinates if set(e) != {0}]
