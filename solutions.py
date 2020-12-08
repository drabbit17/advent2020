from typing import List, Dict
import collections
import math
import re


def load_txt_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as handle:
        content = handle.read().splitlines()
    return content


def problem_1a(data: List[str], target = 2020) -> int:
    data = [int(e) for e in data]
    complementaries = {target-e: e for e in data}

    for e in data:
        if complementaries.get(e):
            return e*complementaries.get(e)

def problem_1b(data: List[str], target: int = 2020) -> int:
    data = sorted([int(e) for e in data])

    for idx, e in enumerate(data):
        low, high = idx+1, len(data)-1
        while low<high:
            if data[low]+data[idx]+data[high]>target:
                high -= 1
            elif data[low]+data[idx]+data[high]<target:
                low+=1
            else:
                return data[low] * data[idx] * data[high]

def problem_2a(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        letters = collections.Counter(e[1])
        if int(low)<=letters[letter]<=int(high):
            matches.append(e)
    return len(matches)


def problem_2b(data: List[str]) -> int:
    data_parsed = [[w.strip() for w in e.split(":")] for e in data]
    matches = []
    for e in data_parsed:
        boundaries, letter = e[0].split(" ")
        low, high = boundaries.split("-")
        low_l, high_l = e[1][int(low)-1], e[1][int(high)-1]
        if (int(low_l==letter) + int(high_l==letter)) == 1:
            matches.append(e)
    return len(matches)


def problem_3a(data: List[str], horizontal_skips: List[int], vertical_skip: int = 1) -> List[int]:
    vals = []

    for skip in horizontal_skips:
        trees = 0
        pointer = 0
        horizontal_length = len(data[0])
        for row in data[::vertical_skip]:
            if row[pointer]=="#":
                trees += 1

            pointer+=skip
            if pointer>=horizontal_length:
                pointer = pointer%horizontal_length

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
    return [{k:v for k,v in e} for e in vals]


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
			return 150<=int(number)<=193
		elif metric == "in":
			return 59<=int(number)<=76
		else:
			return False
	except:
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
    start_point, end_point = 1, 2**len(data)
    for direction in data:
        split_point = (end_point + start_point)//2
        if direction==forward_direction:
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
        if pos>8 & pos <= 127*8:
            if idx>0 and positions[idx-1]+1 != pos:
                return pos - 1


