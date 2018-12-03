from itertools import cycle
from numpy import array, array_equal, count_nonzero, ndarray
from random import choice


def init_board():
    board = ndarray((3, 3), dtype=object)
    board[:] = ''
    return board


def init_possible_moves():
    return [(row, col) for row in range(3) for col in range(3)]


def init_spaces_left(board):
    spaces = board == ''
    return count_nonzero(spaces)


def gen_win_conditions(board, letters):
    return array([[
        array_equal(board[:, i], letters),
        array_equal(board[i, :], letters),
        array_equal(board.diagonal(), letters),
        array_equal(board[:, ::-1].diagonal(), letters)
    ] for i in range(3)])


def check_win(board, letters):
    win_conditions = gen_win_conditions(board, letters)
    if True in win_conditions:
        print(board)
        print(letters[0] + " wins!")
        return True
    elif '' not in board:
        print(board)
        print("Draw!")
        return True


def check_input(row, col):
    if 0 <= row <= 2 and 0 <= col <= 2:
        return True
    else:
        return False


def convert_int(coord):
    try:
        return int(coord)
    except ValueError:
        return -1


def disemvowel(word):
    newword = ""
    for letter in word:
        if (letter not in 'aeiou'):
            newword += letter
    return newword


def player_turn(board, letter, possible_moves):
    print(board)
    row = convert_int(input("Select Row: "))
    col = convert_int(input("Select Column: "))
    is_valid_move = check_input(row, col)
    if is_valid_move is True and board[row, col] == '':
        board[row, col] = letter
        del possible_moves[possible_moves.index((row, col))]
    elif is_valid_move is False or board[row, col] != '':
        print("Invalid Selection!")
        player_turn(board, letter, possible_moves)
    return board, possible_moves


def computer_turn(board, letter, possible_moves):
    row, col = choice(possible_moves)
    # row, col = minimax_tree(board)
    if board[row, col] == '':
        board[row, col] = letter
        del possible_moves[possible_moves.index((row, col))]
    elif board[row, col] != '':
        computer_turn(board, letter, possible_moves)
    return board, possible_moves


def init_minimax_level_0(board, spaces_left):
    return [board.copy() for k in range(spaces_left)]


def init_minimax_moves_0(possible_moves):
    return [possible_moves.copy() for move in possible_moves]


def run_level_0(minimax_level_0, minimax_moves_0, spaces_left, letter):
    for node, move, i in zip(minimax_level_0, minimax_moves_0,
                             range(spaces_left)):
        node[move[i]] = letter
        del move[i]
    minimax_records["Level 0"] = minimax_level_0.copy()


def init_minimax_level_1(minimax_level_0, spaces_left):
    return {
        "Level 1-%d" % i: [game.copy() for j in range(spaces_left)]
        for i, game in enumerate(minimax_level_0)
    }


def init_minimax_moves_1(minimax_moves_0, spaces_left):
    return {
        "Level 1-%d" % i: [move.copy() for j in range(spaces_left)]
        for i, move in enumerate(minimax_moves_0)
    }


def run_level_n(minimax_level_n, minimax_moves_n, spaces_left, letter, n):
    for lev_key, mov_key in zip(minimax_level_n.keys(),
                                minimax_moves_n.keys()):
        for node, move, i in zip(minimax_level_n[lev_key],
                                 minimax_moves_n[mov_key], range(spaces_left)):
            node[move[i]] = letter
            del move[i]
    minimax_records["Level %d" % n] = minimax_level_n.copy()


def init_minimax_level_n(minimax_level_n, spaces_left, n):
    return {
        "Level %d-%d (%s)" % (n, i, lev_key):
        [game.copy() for j in range(spaces_left)]
        for lev_key in minimax_level_n.keys()
        for i, game in enumerate(minimax_level_n[lev_key])
    }


def init_minimax_moves_n(minimax_moves_n, spaces_left, n):
    return {
        "Level %d-%d (%s)" % (n, i, move_key):
        [move.copy() for j in range(spaces_left)]
        for move_key in minimax_moves_n.keys()
        for i, move in enumerate(minimax_moves_n[move_key])
    }


# Init game
turn = cycle(('X', 'O'))
board = init_board()
possible_moves = init_possible_moves()
spaces_left = init_spaces_left(board)
minimax_records = {}

# Init level 0
minimax_level_n = init_minimax_level_0(board, spaces_left)
minimax_moves_n = init_minimax_moves_0(possible_moves)

# Complete level 0
run_level_0(minimax_level_n, minimax_moves_n, spaces_left, next(turn))
spaces_left -= 1

# Init level 1
minimax_level_n = init_minimax_level_1(minimax_level_n, spaces_left)
minimax_moves_n = init_minimax_moves_1(minimax_moves_n, spaces_left)

# Complete level 1
run_level_n(minimax_level_n, minimax_moves_n, spaces_left, next(turn), 1)
spaces_left -= 1

# Recursively populate the remainder of the minimax gametree
for i in range(2, spaces_left + 2):
    minimax_level_n = init_minimax_level_n(minimax_level_n, spaces_left, i)
    minimax_moves_n = init_minimax_moves_n(minimax_moves_n, spaces_left, i)
    run_level_n(minimax_level_n, minimax_moves_n, spaces_left, next(turn), i)
    spaces_left -= 1

# Play the game
while '' in board:
    board, possible_moves = player_turn(board, 'X', possible_moves)
    win = check_win(board, ('X', 'X', 'X'))
    if win is True:
        break
    board, possible_moves = computer_turn(board, 'O', possible_moves)
    win = check_win(board, ('O', 'O', 'O'))
    if win is True:
        break
