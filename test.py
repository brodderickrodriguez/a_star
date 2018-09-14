import math
import numpy as np
from queue import PriorityQueue, Queue

hole = "X"
blank = 0
goal_board = [[blank, 2, 1], [3, 4, 5], [6, 7, 8]]


class ClosedQueue(Queue):
    def remove(self, element):
        i = 0
        while i < len(self.queue):
            if self.queue[i] is element:
                break
            i += 1
        if i >= len(self.queue):
            return False
        del self.queue[i]
        return True


class State:
    def __init__(self, board, parent):
        self.board = board
        self.gn = 0 if not parent else parent.gn + 1
        self.hn = manhattan(self.board)
        self.fn = self.gn + self.hn
        self.parent = parent

    def __lt__(self, other):
        return self.fn < other.fn

    def __eq__(self, other):
        return (self.board == other.board).all()


def make_board():
    return [[7, 2, 4], [5, blank, 6], [8, 3, 1]]
    # return [[blank, 2], [3, 1]]


def print_state(state):
    print_board(state.board)
    print("\tgn = " + str(state.gn))
    print("\thn = " + str(state.hn) + " ")
    print("\tfn = " + str(state.fn))


def print_board(board):
    print("")
    for x in board:
        print(x)


def swap(a, b, board):
    t = board[b[1]][b[0]]
    board[b[1]][b[0]] = board[a[1]][a[0]]
    board[a[1]][a[0]] = t


def queue_contains(item, queue):
    for i in queue.queue:
        if i is item:
            return i
    return None


def index_of(item, board):
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] == item:
                return x, y


def manhattan(board):
    def distance_of(item):
        a = index_of(item, board)
        b = index_of(item, goal_board)
        return abs(a[1] - b[1]) + abs(a[0] - b[0])

    distance = 0
    for row in board:
        for it in row:
            distance += distance_of(it)

    return distance


def neighbors_of(item, board):
    neighbors = []
    if item[0] > 0:
        neighbors.append((item[0] - 1, item[1]))
    if item[1] > 0:
        neighbors.append((item[0], item[1] - 1))
    if item[0] < len(board) - 1:
        neighbors.append((item[0] + 1, item[1]))
    if item[1] < len(board) - 1:
        neighbors.append((item[0], item[1] + 1))
    return neighbors


def generate_successor_states(state):
    blank_location = index_of(0, state.board)
    possible_moves = neighbors_of(blank_location, state.board)
    states = []
    for item in possible_moves:
        test_board = np.copy(state.board)
        swap(item, blank_location, test_board)
        states.append(State(test_board, state))
    return states


def a_star_search(initial_state):
    closed_queue = ClosedQueue()
    open_queue = PriorityQueue()
    open_queue.put(initial_state)

    while not open_queue.empty():
        current = open_queue.get()
        print_state(current)

        if current.board is goal_board:
            print("found goal!")
            return current

        successors = generate_successor_states(current)

        for successor in successors:
            successor.parent = current

            in_open = queue_contains(successor, open_queue)
            in_closed = queue_contains(successor, closed_queue)
            new_gn = current.gn + 1

            if not in_open and not in_closed:
                print("in neither")
                successor.hn = manhattan(successor.board)
                successor.gn = new_gn
                successor.fn = successor.gn + successor.hn
                open_queue.put(successor)
            else:
                if in_open:
                    print("in open")
                    if new_gn < in_open.gn:
                        in_open.gn = new_gn
                else:
                    if new_gn < in_closed.gn:
                        print("in closed")
                        closed_queue.remove(in_closed)
                        in_closed.gn = new_gn

    print("failed to find goal")
    return None


def main():
    print("main")
    board = make_board()

    initial_state = State(board, None)
    print_state(initial_state)

    result = a_star_search(initial_state)

    while result is not None:
        print_state(result)
        result = result.parent


if __name__ == "__main__":
    main()