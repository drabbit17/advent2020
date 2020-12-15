import collections
import re


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
