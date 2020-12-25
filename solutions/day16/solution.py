from typing import List, Tuple, Dict
import functools
import operator


def problem16a(data):
    rules, my_ticket, other_tickets = prepare_the_data(data)
    combined_rules = build_combined_rules(rules)
    bad_numbers = []
    _, bad_numbers = get_bad_tickets_and_numbers(other_tickets, combined_rules)
    return sum(bad_numbers)


def get_bad_tickets_and_numbers(tickets, combined_rules):
    bad_numbers, bad_tickets_idx = [], []
    for idx, ticket in enumerate(tickets):
        for number in ticket:
            for rule in combined_rules:
                if number < rule[0] or number > rule[1]:
                    bad_numbers.append(number)
                    bad_tickets_idx.append(idx)
    return bad_tickets_idx, bad_numbers


def problem16b(data):
    rules, my_ticket, other_tickets = prepare_the_data(data)
    combined_rules = build_combined_rules(rules)
    bad_tickets_idx, _ = get_bad_tickets_and_numbers(other_tickets, combined_rules)
    good_tickets = [e for idx, e in enumerate(other_tickets) if idx not in bad_tickets_idx]
    matching_rules = {rule: {idx: 0 for idx in range(len(my_ticket))} for rule in rules}
    for ticket in good_tickets:
        for idx, ticket_value in enumerate(ticket):
            for rule_name, rule in rules.items():
                valid = (rule[0][0] <= ticket_value <= rule[0][1]) or (
                    rule[1][0] <= ticket_value <= rule[1][1]
                )
                matching_rules[rule_name][idx] += valid

    used_rules_and_pos, number_of_good_tickets, iterations = dict(), len(good_tickets), 0
    while len(used_rules_and_pos) <= 20 and iterations <= 20:
        for rule, counter in matching_rules.items():
            unique_matches, good_pos = 0, None
            for pos, count in counter.items():
                if pos not in used_rules_and_pos and count == number_of_good_tickets:
                    unique_matches += 1
                    good_pos = pos
            if unique_matches == 1:
                used_rules_and_pos[good_pos] = rule
        iterations += 1
    return functools.reduce(
        operator.mul, [my_ticket[pos] for pos, rule in used_rules_and_pos.items() if "departure" in rule]
    )


def build_combined_rules(rules):
    rules = sorted([e for rule in rules.values() for e in rule], key=lambda x: x[0])
    new_intervals = [rules[0]]
    for rule in rules:
        if rule[0] <= new_intervals[-1][1]:
            if rule[1] >= new_intervals[-1][1]:
                new_intervals[-1][1] = rule[1]
        else:
            new_intervals.append(rule)
    return new_intervals


def prepare_the_data(data: List[str]) -> Tuple[Dict[str, List[List[int]]], List[int], List[List[int]]]:
    empty_lines, rules, my_ticket, other_tickets = 0, {}, [], []
    for line in data:
        if line == "":
            empty_lines += 1
        else:
            if empty_lines == 0:
                rules.update(parse_rule(line))
            elif ":" in line:
                continue
            elif empty_lines == 1:
                my_ticket = [int(e) for e in line.split(",")]
            else:
                other_tickets.append([int(e) for e in line.split(",")])
    return rules, my_ticket, other_tickets


def parse_rule(line: str) -> Dict[str, List[List[int]]]:
    name, intervals = line.split(":")
    intervals = [[int(number) for number in e.split("-")] for e in intervals.split(" or ")]
    return {name: intervals}
