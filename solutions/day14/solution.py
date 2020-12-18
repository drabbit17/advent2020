# flake8: noqa


def problem14a(data):
    memory = {}
    current_mask = None
    for line in data:
        if "mask =" in line:
            current_mask = line[7:]
        else:
            memory_address, value = get_memory_address_and_value_from_line(line)
            value_bin = bin(int(value)[2:])
            new_mask = [
                new_value if mask_value == "X" else mask_value
                for new_value, mask_value in zip(value_bin[::-1], current_mask[::-1])
            ][::-1]
            final_value = current_mask[: -len(value_bin)].replace("X", "0") + "".join(new_mask)
            memory[memory_address] = int(final_value, 2)
    print(len(memory))
    return sum(memory.values())


def problem14b(data):
    memory = {}
    current_mask = None
    for line in data:
        if "mask =" in line:
            current_mask = line[7:]
        else:
            memory_address, value = get_memory_address_and_value_from_line(line)
            final_value = get_new_mask_problem14b(memory_address, current_mask)
            x_positions = [idx for idx, x in enumerate(final_value) if x == "X"]
            replacement_permutations = [
                bin(e)[2:].zfill(len(x_positions)) for e in range(2 ** len(x_positions))
            ]
            for permutation in replacement_permutations:
                new_memory_address = str(final_value)
                for new_value, position_to_replace in zip(permutation, x_positions):
                    new_memory_address = (
                        new_memory_address[:position_to_replace]
                        + str(new_value)
                        + new_memory_address[position_to_replace + 1 :]
                    )
                memory[int(new_memory_address, 2)] = int(value)
    return sum(memory.values())


def get_memory_address_and_value_from_line(line):
    memory_address, value = line.split(" = ")
    memory_address = memory_address.replace("mem[", "").replace("]", "")
    return memory_address, value


def get_new_mask_problem14b(memory_address, current_mask):
    new_value = bin(int(memory_address))[2:]
    new_mask = [
        new_value if mask_value == "0" else mask_value
        for new_value, mask_value in zip(new_value[::-1], current_mask[::-1])
    ][::-1]
    return current_mask[: -len(new_value)] + "".join(new_mask)
