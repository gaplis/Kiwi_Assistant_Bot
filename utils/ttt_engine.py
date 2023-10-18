from random import randint


def rand_choice_bot_in_ttt_game(field, x_o):
    while True:
        column = randint(0, 2)
        line = randint(0, 2)

        if field[column][line] is None:
            field[column][line] = x_o
            return field


def check_win(field, x_o, who_turn):
    if field[0][0] == x_o and field[1][0] == x_o and field[2][0] == x_o \
            or field[0][1] == x_o and field[1][1] == x_o and field[2][1] == x_o \
            or field[0][2] == x_o and field[1][2] == x_o and field[2][2] == x_o \
            or field[0][0] == x_o and field[0][1] == x_o and field[0][2] == x_o \
            or field[1][0] == x_o and field[1][1] == x_o and field[1][2] == x_o \
            or field[2][0] == x_o and field[2][1] == x_o and field[2][2] == x_o \
            or field[0][0] == x_o and field[1][1] == x_o and field[2][2] == x_o \
            or field[0][2] == x_o and field[1][1] == x_o and field[2][0] == x_o:
        return who_turn

    count = 9
    for i in field:
        for j in i:
            if j is not None:
                count -= 1
                if count == 0:
                    return "Ничья!"

    return None
