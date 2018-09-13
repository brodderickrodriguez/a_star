import numpy as np
import random
import math


def make_board():
    dimension = 25
    board = np.zeros((dimension, dimension), int)
    np.fill_diagonal(board, 1)
    return board


def print_board(board):
    for x in board:
        print(x)


def conflicts_for_location(x, y, board):
    def row_col():
        col = [board[i][x] for i in range(len(board))]
        row = board[y].tolist() if isinstance(board[y], np.ndarray) else board[y]
        return max(col.count(1) - 1, 0) + max(row.count(1) - 1, 0)

    def diagonal():
        d1 = np.diagonal(board, x - y).tolist()
        d2 = np.diagonal(np.fliplr(board), len(board) - y - x - 1).tolist()
        return max(d1.count(1) - 1, 0) + max(d2.count(1) - 1, 0)

    return row_col() + diagonal()


def score_board_state(board):
    return sum([conflicts_for_location(q[0], q[1], board) for q in get_queens(board)])


def get_queens(board):
    return [(x, y) for x in range(len(board)) for y in range(len(board)) if board[y][x] == 1]


def move(queen, new_x, board):
    board[queen[1]][queen[0]] = 0
    board[queen[1]][new_x] = 1


def find_best_move_for_queen(queen, board):
    best_move = (0, 0, 0, math.inf)  # x, y, offset, score

    for x in range(len(board)):
        test_board = np.copy(board)
        move(queen, x, test_board)
        score = score_board_state(test_board)

        if score <= best_move[3]:
            best_move = (queen[0], queen[1], x, score)

    return best_move


def make_best_move(board):
    best_move = (0, 0, 0, math.inf)  # x, y, offset, score

    for q in get_queens(board):
        queen_best_move = find_best_move_for_queen(q, board)
        if queen_best_move[3] <= best_move[3]:
            best_move = queen_best_move

    move((best_move[0], best_move[1]), best_move[2], board)
    return best_move


def random__sequential_move(board):
    queens = get_queens(board)
    for q in queens:
        move(q, random.randint(0, len(queens) - 1), board)


def main():
    board = make_board()
    moves = 0
    last_move = (0, 0, 0, 0)  # format is (x, y, offset, score)
    best_score = (math.inf, board)

    while True:
        score = score_board_state(board)
        print_board(board)
        print("current score is " + str(score))

        if score < best_score[0]:
            best_score = (score, board)

        if score == 0:
            print("found solution!")
            break

        current_move = make_best_move(board)
        moves += 1

        print("moves made " + str(moves) + "\tbest score so far " + str(best_score[0]))
        print("making move: " + str(current_move) + "(format: x, y, new_x, new_score)\n")

        if current_move == last_move:
            moves += len(board)
            random__sequential_move(board)

        last_move = current_move


if __name__ == "__main__":
    main()




