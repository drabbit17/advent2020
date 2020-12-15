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
