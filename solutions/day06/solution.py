import collections


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
