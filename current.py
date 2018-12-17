from numpy import array, array_equal, ndarray
from os import system
from platform import system as os_name
from random import choice


def clear_console():
    if 'Windows' in os_name():
        system('cls')
    else:
        system('clear')


def prep_players():
    def clear_console():
        if 'Windows' in os_name():
            system('cls')
        else:
            system('clear')

    def choose_player_X_or_O():
        player = input("Play as X or O?  (Enter 'X' or 'O'): ")
        if player in ('X', 'x'):
            return 'X'
        elif player in ('O', 'o'):
            return 'O'
        else:
            print("Invalid selection!")
            return choose_player_X_or_O()

    def set_computer_X_or_O(player):
        if player is 'X':
            return 'O'
        elif player is 'O':
            return 'X'

    def who_goes_first():
        first = input("You go first?  (Enter 'Y' or 'N'): ")
        if first in ('Y', 'y', 'Yes', 'yes'):
            return "player"
        elif first in ('N', 'n', 'No', 'no'):
            return "computer"
        else:
            print("Invalid selection!")
            return who_goes_first()

    player = choose_player_X_or_O()
    computer = set_computer_X_or_O(player)
    first = who_goes_first()
    return player, computer, first


def prep_board():
    def init_board():
        board = ndarray((3, 3), dtype=object)
        board[:] = ''
        return board

    def init_possible_moves():
        return [(row, col) for row in range(3) for col in range(3)]

    board = init_board()
    possible_moves = init_possible_moves()
    return board, possible_moves


class Player:
    def __init__(self, player):
        self.player = player

    def convert_int(self, coord):
        try:
            return int(coord)
        except ValueError:
            return -1

    def check_input(self, row, col):
        if 0 <= row <= 2 and 0 <= col <= 2:
            return True
        else:
            return False

    def player_turn(self, board, possible_moves):
        row = self.convert_int(input("Select Row: "))
        col = self.convert_int(input("Select Column: "))
        is_valid_move = self.check_input(row, col)
        if is_valid_move is True and board[row, col] == '':
            board[row, col] = self.player
            del possible_moves[possible_moves.index((row, col))]
        elif is_valid_move is False or board[row, col] != '':
            print("Invalid Selection!")
            return self.player_turn(board, possible_moves)
        return board, possible_moves


class Computer:
    def __init__(self, computer):
        self.computer = computer

    def evaluate(board, score):
        if check_win(board, tuple(computer.computer * 3), False) is True:
            score += 10
        elif check_win(board, tuple(player.player * 3), True) is True:
            score -= 10
        return score

    # def minimax(self, depth, possible_moves, isComputer):
    #     for move in possible_moves:
    #         score = self.minimax(state, depth - 1, not isComputer)
    #     return depth

    def computer_turn(self, board, possible_moves):
        # depth = len(board[board == ''])
        # if depth == 9:
        row, col = choice(possible_moves)
        # else:
        # self.minimax(board, depth, possible_moves, True)
        board[row, col] = self.computer
        del possible_moves[possible_moves.index((row, col))]
        return board, possible_moves


def gen_win_conditions(board, letters):
    return array([[
        array_equal(board[:, i], letters),
        array_equal(board[i, :], letters),
        array_equal(board.diagonal(), letters),
        array_equal(board[:, ::-1].diagonal(), letters)
    ] for i in range(3)])


def check_win(board, letters, isPlayer):
    if True in gen_win_conditions(board, letters):
        print(board)
        if isPlayer is True:
            print("You win!")
        elif isPlayer is False:
            print("You lose!")
        return True
    elif '' not in board:
        print(board)
        print("Draw!")
        return True


'''Prep the game'''
# Init params
player, computer, first = prep_players()
board, possible_moves = prep_board()

# Init objects
player = Player(player)
computer = Computer(computer)

# Play the game
clear_console()
if first is "computer":
    board, possible_moves = computer.computer_turn(board, possible_moves)
while '' in board:
    print(board)
    board, possible_moves = player.player_turn(board, possible_moves)
    if check_win(board, tuple(player.player * 3), True) is True:
        break
    board, possible_moves = computer.computer_turn(board, possible_moves)
    if check_win(board, tuple(computer.computer * 3), False) is True:
        break
    clear_console()
