def problem8a(data):
    accumulator = 0
    visited = []
    pointer = 0
    while pointer not in visited:
        visited.append(pointer)
        pointer, accumulator_delta = problem8_get_pointer_from_line(data[pointer], pointer)
        accumulator += accumulator_delta
    return accumulator


def problem8_get_pointer_from_line(line, pointer):
    instruction, argument, accumulator = line[:3], line[4:], 0
    if instruction == "nop":
        pointer += 1
    else:
        if argument[0] == "-":
            shift = -int(argument[1:])
        else:
            shift = int(argument[1:])
        if instruction == "acc":
            accumulator += shift
            pointer += 1
        else:
            pointer += shift
    return pointer, accumulator


def problem8b(data):
    instruction_change = {"nop": "jmp", "jmp": "nop"}
    to_change, visited = {}, []
    pointer, accumulator = 0, 0
    while pointer not in visited:
        for instruction in instruction_change:
            if instruction in data[pointer]:
                to_change[pointer] = (instruction, accumulator)
        visited.append(pointer)
        pointer, accumulator_delta = problem8_get_pointer_from_line(data[pointer], pointer)
        accumulator += accumulator_delta

    for pointer, (instruction, accumulator) in to_change.items():
        new_instruction_full = data[pointer].replace(instruction, instruction_change[instruction])
        pointer, accumulator_delta = problem8_get_pointer_from_line(new_instruction_full, pointer)
        while pointer not in visited:
            visited.append(pointer)
            pointer, accumulator_delta = problem8_get_pointer_from_line(data[pointer], pointer)
            accumulator += accumulator_delta
            if pointer == len(data):
                return accumulator
