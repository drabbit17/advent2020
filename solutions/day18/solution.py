import operator


def problem18a(data):
    values = 0
    for line in data:
        values += recursive_parser(line)[0]
    return values


def recursive_parser(string):
    pointer, value, next_value, current_operator = 0, 0, "", operator.add

    while string[pointer:]:
        if string[pointer] == "(":
            next_value, pointer_shift = recursive_parser(string[(pointer + 1) :])  # noqa: E203
            value, pointer, next_value = current_operator(value, next_value), pointer + pointer_shift, ""
        elif string[pointer] == ")":
            if next_value:
                value = current_operator(value, int(next_value))
            return value, pointer + 1
        elif string[pointer] == " ":
            if next_value:
                value, next_value = current_operator(value, int(next_value)), ""
        elif string[pointer] == "+":
            current_operator = operator.add
        elif string[pointer] == "*":
            current_operator = operator.mul
        else:
            next_value += string[pointer]

        pointer += 1

    if next_value:
        value = current_operator(value, int(next_value))

    return value, pointer
