import math
import numpy as np
from queue import PriorityQueue, Queue
from itertools import product

blank = 0
goal_board = np.array([[blank, 2, 1], [3, 4, 5], [6, 7, 8]])
initial_board = np.array([[2, 3, 1], [4, blank, 5], [6, 7, 8]])


class CustomQueue(PriorityQueue):
    def contains(self, item):
        return self.queue.__contains__(item)

    def remove(self, item):
        index = 0
        while index < len(self.queue):
            if self.queue[index] == item:
                break
        if index >= len(self.queue):
            return False
        del self.queue[index]
        return True


class State:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.gn = math.inf
        self.fn = math.inf
        self.hn = math.inf

    def __lt__(self, other):
        return self.fn < other.fn

    def __eq__(self, other):
        return (np.array(self.board) == np.array(other.board)).all()


def print_state(state):
    def print_board():
        for row in state.board:
            print(row)

    print("")
    print_board()


def swap(a, b, board):
    t = board[b[1]][b[0]]
    board[b[1]][b[0]] = board[a[1]][a[0]]
    board[a[1]][a[0]] = t


def index_of(item, board):
    for x, y in product(range(len(board)), range(len(board))):
        if board[y][x] == item:
            return x, y


def manhattan(board):
    def distance_of(item):
        a = index_of(item, board)
        b = index_of(item, goal_board)
        return abs(a[1] - b[1]) + abs(a[0] - b[0])
    return sum([distance_of(item) for row in board for item in row])


def possible_moves(index, board):
    moves = []
    if index[1] > 0:
        moves.append((index[0], index[1] - 1))
    if index[0] > 0:
        moves.append((index[0] - 1, index[1]))
    if index[1] < len(board) - 1:
        moves.append((index[0], index[1] + 1))
    if index[0] < len(board) - 1:
        moves.append((index[0] + 1, index[1]))
    return moves


def generate_successor_states(state):
    blank_location = index_of(0, state.board)
    print("blank loc is " + str(blank_location))

    moves = possible_moves(blank_location, state.board)
    print(moves)
    states = []

    for move in moves:
        test_board = np.copy(state.board)
        swap(move, blank_location, test_board)
        states.append(State(test_board, state))

    return states


def main():
    print("main")

    initial_state = State(initial_board, None)
    goal_state = State(goal_board, None)
    initial_state.fn = 100
    goal_state.fn = 990

    v = generate_successor_states(initial_state)

    #for state in v:
    #    print_state(state)

    closed_queue = CustomQueue()

    closed_queue.put(goal_state)
    closed_queue.put(initial_state)

    x = closed_queue.get()

    print_state(x)





if __name__ == "__main__":
    main()
