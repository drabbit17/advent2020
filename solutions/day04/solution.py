from typing import Dict, List
import re


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
