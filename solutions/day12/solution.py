import re


def problem12a(data):
    current_direction, pos = "E", {"x": 0, "y": 0}
    changes_policy = {
        "E": lambda quantity: {"x": quantity},
        "W": lambda quantity: {"x": -quantity},
        "N": lambda quantity: {"y": quantity},
        "S": lambda quantity: {"y": -quantity},
    }
    for instruction in data:
        direction_instruction, quantity = parse_direction_and_quantity_problem_12a(instruction)
        direction_instruction = current_direction if direction_instruction == "F" else direction_instruction
        if direction_instruction in changes_policy:
            for coordinate, change in changes_policy[direction_instruction](quantity).items():
                pos[coordinate] += change
        else:
            current_direction = get_next_direction_problem12(
                current_direction, direction_instruction, quantity
            )
    return abs(pos["x"]) + abs(pos["y"])


def problem12b(data):
    waypoint, pos = {"x": 10, "y": 1}, {"x": 0, "y": 0}
    changes_policy = {
        "E": lambda quantity: {"x": quantity},
        "W": lambda quantity: {"x": -quantity},
        "N": lambda quantity: {"y": quantity},
        "S": lambda quantity: {"y": -quantity},
    }
    for instruction in data:
        direction_instruction, quantity = parse_direction_and_quantity_problem_12a(instruction)
        if direction_instruction in changes_policy:
            for coordinate, change in changes_policy[direction_instruction](quantity).items():
                waypoint[coordinate] += change
        elif direction_instruction == "F":
            for coordinate, change in waypoint.items():
                pos[coordinate] += change * quantity
        else:
            new_waypoint = {}
            for coordinate in ["x", "y"]:
                coordinate_direction = get_direction_from_coordinate_problem_12a(
                    waypoint[coordinate], coordinate
                )
                new_direction = get_next_direction_problem12(
                    coordinate_direction, direction_instruction, quantity
                )
                new_waypoint.update(changes_policy[new_direction](abs(waypoint[coordinate])))
            waypoint = new_waypoint

    return abs(pos["x"]) + abs(pos["y"])


def get_next_direction_problem12(current_direction: str, rotation: str, degrees: int) -> str:
    directions = ["E", "S", "W", "N"]
    for idx, direction in enumerate(directions):
        if current_direction == direction:
            shifts = degrees // 90
            if rotation == "R":
                return directions[(idx + shifts) % len(directions)]
            else:
                return directions[(idx - shifts) % len(directions)]


def get_direction_from_coordinate_problem_12a(coordinate_value, axis):
    if axis == "x":
        return "E" if coordinate_value > 0 else "W"
    else:
        return "N" if coordinate_value > 0 else "S"


def parse_direction_and_quantity_problem_12a(instruction):
    direction_instruction, quantity = re.match(r"([A-Z]{1})([0-9]+)", instruction).groups()
    return direction_instruction, int(quantity)
