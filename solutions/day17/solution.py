import itertools
import copy


def problem17a(data, number_of_cycles, dimensions):
    final_data = [[[elem for elem in row] for row in data]]
    for _ in range(number_of_cycles):
        new_data = create_new_space_recursive(final_data)
        for z_idx, z in enumerate(new_data):
            for x_idx, x in enumerate(z):
                for y_idx, y in enumerate(x):
                    coordinates = get_coordinates(dimensions)
                    actives_count = 0
                    z_original, x_original, y_original = z_idx - 1, x_idx-1, y_idx-1
                    for coordinate in coordinates:
                        if set(coordinate) == {0}:
                           continue 

                        temp_z, temp_x, temp_y = z_original + coordinate[0], x_original + coordinate[1], y_original + coordinate[2]
                        try:
                            if temp_z < 0 or temp_x < 0 or temp_y < 0:
                                raise IndexError
                            actives_count += final_data[temp_z][temp_x][temp_y] =="#"
                        except IndexError:
                            pass
                    try:
                        if z_original>=0 and x_original>=0 and y_original>=0:
                            current_value = final_data[z_original][x_original][y_original]
                        else:
                            raise IndexError
                    except IndexError:
                        current_value = "."

                    if actives_count == 3:
                        new_data[z_idx][x_idx][y_idx] = "#"
                    elif actives_count == 2 and current_value == "#":
                        new_data[z_idx][x_idx][y_idx] = "#"
        final_data = copy.deepcopy(new_data)
        print([(" ").join(["".join(row) for row in e]) for e in new_data])
        print("\n\n\n")



def create_new_space_recursive(current_dimension):
    if isinstance(current_dimension[0], list):
        return [create_new_space_recursive(current_dimension[0]) for _ in range(len(current_dimension)+2)]
    else:
        return ["." for _ in range(len(current_dimension)+2)]


def get_coordinates(dimensions):
    coordinates = list(itertools.product([0, -1, 1], repeat=dimensions))
    return [e for e in coordinates if set(e) != {0}]
