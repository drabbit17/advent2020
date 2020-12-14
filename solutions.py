from typing import List, Dict
import copy
import collections
import itertools
import functools
import math
import re


def load_txt_file(file_path: str) -> List[str]:
    with open(file_path, "r") as handle:
        content = handle.read().splitlines()
    return content


def problem_1a(data: List[str], target=2020) -> int:
    data = [int(e) for e in data]
    complementaries = {target - e: e for e in data}

    for e in data:
        if complementaries.get(e):
            return e * complementaries.get(e)


def problem_1b(data: List[str], target: int = 2020) -> int:
    data = sorted([int(e) for e in data])

    for idx, e in enumerate(data):
        low, high = idx + 1, len(data) - 1
        while low < high:
            if data[low] + data[idx] + data[high] > target:
                high -= 1
            elif data[low] + data[idx] + data[high] < target:
                low += 1
            else:
                return data[low] * data[idx] * data[high]


def problem_2a(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        letters = collections.Counter(e[1])
        if int(low) <= letters[letter] <= int(high):
            matches.append(e)
    return len(matches)


def problem_2b(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        low_l, high_l = e[1][int(low) - 1], e[1][int(high) - 1]
        if (int(low_l == letter) + int(high_l == letter)) == 1:
            matches.append(e)
    return len(matches)


def problem_3a(data: List[str], horizontal_skips: List[int], vertical_skip: int = 1) -> List[int]:
    vals = []

    for skip in horizontal_skips:
        trees = 0
        pointer = 0
        horizontal_length = len(data[0])
        for row in data[::vertical_skip]:
            if row[pointer] == "#":
                trees += 1

            pointer += skip
            if pointer >= horizontal_length:
                pointer = pointer % horizontal_length

        vals.append(trees)
    return vals


def problem_3b(data: List[str]) -> List[int]:
    vals_1 = problem_3a(data, horizontal_skips=[1, 3, 5, 7], vertical_skip=1)
    vals_2 = problem_3a(data, horizontal_skips=[1], vertical_skip=2)
    return math.prod(vals_1) * math.prod(vals_2)


def problem_4a(data: List[str]) -> int:
    expected_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    passports = problem_4_convert_input_to_list_of_dict(data)
    valid_count = 0
    for passport in passports:
        valid_count += all(field in passport for field in expected_fields)
    return valid_count


def problem_4_convert_input_to_list_of_dict(data: List[str]) -> List[Dict]:
    regex_key_val = re.compile(r"(\w+):(#{0,1}\w+)")
    vals = [re.findall(regex_key_val, e) for e in "\n".join(data).split("\n\n")]
    return [{k: v for k, v in e} for e in vals]


def problem_4b(data: List[str]) -> int:
    rules = {
        "byr": lambda x: 1920 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": problem4b_check_height,
        "hcl": lambda x: re.match(r"#\w{6}$", x) is not None,
        "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
        "pid": lambda x: re.match(r"^[0-9]{9}$", x) is not None,
    }
    passports = problem_4_convert_input_to_list_of_dict(data)
    good_passports = 0
    for passport in passports:
        good_passport = True
        for rule_name, rule in rules.items():
            if passport.get(rule_name) is None or not rule(passport.get(rule_name)):
                good_passport = False
                break
        good_passports += good_passport
    return good_passports


def problem4b_check_height(height):
    try:
        number, metric = re.match(r"([0-9]{2,3})(cm|in)$", height).groups()
        if metric == "cm":
            return 150 <= int(number) <= 193
        elif metric == "in":
            return 59 <= int(number) <= 76
        else:
            return False
    except Exception:
        return False


def problem5a(data):
    highest = 0
    for ticket in data:
        ticket_pos = problem5a_get_ticket_pos(ticket)
        highest = max(ticket_pos, highest)
    return highest


def problem5a_get_ticket_pos(ticket):
    row_info, column_info = ticket[:7], ticket[7:]
    start_row = problem5a_bisect(row_info, "B")
    start_column = problem5a_bisect(column_info, "R")
    return start_row * 8 + start_column


def problem5a_bisect(data, forward_direction):
    start_point, end_point = 1, 2 ** len(data)
    for direction in data:
        split_point = (end_point + start_point) // 2
        if direction == forward_direction:
            start_point = split_point
        else:
            end_point = split_point
    return end_point - 1


def problem5b(data):
    positions = []
    for ticket in data:
        positions.append(problem5a_get_ticket_pos(ticket))
    positions.sort()
    for idx, pos in enumerate(positions):
        if pos > 8 & pos <= 127 * 8:
            if idx > 0 and positions[idx - 1] + 1 != pos:
                return pos - 1


def problem6a(data):
    overall_yes = 0

    single_group_answers = set()
    for answer in data:
        if answer != "":
            for letter in answer:
                single_group_answers.add(letter)
        else:
            overall_yes += len(single_group_answers)
            single_group_answers = set()
    return overall_yes


def problem6b(data):
    overall_yes = 0

    single_group_answers, group_size = collections.defaultdict(lambda: 0), 0
    for answer in data:
        if answer == "":
            for count in single_group_answers.values():
                if count == group_size:
                    overall_yes += 1
            single_group_answers, group_size = collections.defaultdict(lambda: 0), 0
        else:
            group_size += 1
            for letter in answer:
                single_group_answers[letter] += 1
    return overall_yes


def problem7a(data):
    contained_by = collections.defaultdict(set)
    remove_numbers = re.compile(r"[0-9]+ ")
    for line in data:
        if "contain no other bags" in line:
            continue
        container, content = line.split(" contain ")
        bags_contained = re.sub(remove_numbers, "", content.replace(".", "")).split(", ")
        for bag in bags_contained:
            if bag[-3:] == "bag":
                bag = bag + "s"
            contained_by[bag].add(container)
    target = "shiny gold bags"
    valid_containers, queue = [], list(contained_by[target])

    while queue:
        target = queue.pop()
        valid_containers.append(target)
        for potential_bag in contained_by[target]:
            if potential_bag not in queue and potential_bag not in valid_containers:
                queue.append(potential_bag)
    return len(valid_containers)


def problem7b(data):
    contained_by = collections.defaultdict(list)
    get_numbers_and_bags = re.compile(r"([0-9]+) (.*?) bag")
    get_bag = re.compile(r"(.*?) bag")
    for line in data:
        if "contain no other bags" in line:
            continue
        container, content = line.split(" contain ")
        bags_contained = re.findall(get_numbers_and_bags, content)
        for bag in bags_contained:
            contained_by[re.match(get_bag, container).group(1)].append(bag)

    queue, final_number = contained_by["shiny gold"], 0
    while queue:
        number, bag = queue.pop()
        contained_bags = contained_by[bag]
        print(contained_bags, number, bag)
        if contained_bags:
            for inner_bag_data in contained_by[bag]:
                inner_number, inner_bag = inner_bag_data
                queue.append((int(inner_number) * int(number), inner_bag))
        final_number += int(number)
    return final_number


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


def problem10a(data):
    sorted_data = sorted([int(e) for e in data])
    last_point, differences = 0, []
    for idx, adapter in enumerate(sorted_data):
        differences.append(adapter - last_point)
        last_point = sorted_data[idx]
    # add device difference
    differences.append(3)
    diffs_counts = collections.Counter(differences)
    return diffs_counts[1] * diffs_counts[3]


def problem10b(data):
    def get_possible_paths_count(current_jolt, sorted_adapters):
        possible_paths_count = 0

        if not sorted_adapters:
            return 1

        for idx, adapter in enumerate(sorted_adapters):
            if (adapter - current_jolt) <= 3:
                adapter_paths_count = memory.get(adapter)
                if not adapter_paths_count:
                    adapter_paths_count = get_possible_paths_count(
                        adapter, sorted_adapters[(idx + 1) :]  # noqa: E203
                    )  # noqa: E203
                    memory[adapter] = adapter_paths_count
                possible_paths_count += adapter_paths_count
        return possible_paths_count

    sorted_adapters = sorted([int(e) for e in data])
    sorted_adapters.append(max(sorted_adapters) + 3)
    memory = {}
    paths_count = get_possible_paths_count(0, sorted_adapters)
    return paths_count


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
