import math
import numpy as np
from queue import PriorityQueue, Queue

hole = "X"
blank = 0
goal_board = [[blank, 1, 2], [3, 4, 5], [6, 7, 8]]
# goal_board = [[blank, 1], [2, 3]]


class ClosedQueue(Queue):
    def remove(self, element):
        i = 0
        while i < len(self.queue):
            if self.queue[i] == element:
                break
            i += 1
        if i >= len(self.queue):
            return False
        del self.queue[i]
        return True


class State:
    def __init__(self, gn, board, parent):
        self.board = board
        self.gn = gn
        self.hn = manhattan(self.board)
        self.fn = self.gn + self.hn
        self.parent = parent

    def __lt__(self, other):
        return self.fn < other.fn

    def __eq__(self, other):
        return self.board == other.board


def make_board():
    return [[7, 2, 4], [5, blank, 6], [8, 3, 1]]
    # return [[blank, 2], [3, 1]]


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
            return True
    return False


def get_twin(item, queue):
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

    def distance_of(item, board):
        a = index_of(item, board)
        b = index_of(item, goal_board)
        return abs(a[1] - b[1]) + abs(a[0] - b[0])

    distance = 0
    for row in board:
        for item in row:
            distance += distance_of(item, board)
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
        states.append(State(state.gn + 1, test_board, state))
    return states


def a_star_search(initial_state):
    print("starting A*")
    closed_queue = ClosedQueue()
    open_queue = PriorityQueue()
    open_queue.put(initial_state)

    while open_queue.not_empty:
        current_state = open_queue.get()
        closed_queue.put(current_state)

        if current_state.hn is 0:
            print("found solution!!!")
            return current_state

        successors = generate_successor_states(current_state)

        for successor in successors:
            gn = current_state.gn + 1

            in_open_queue = queue_contains(successor, open_queue)
            in_closed_queue = queue_contains(successor, closed_queue)

            if in_open_queue or in_closed_queue:
                print("seen this before")

            if not in_open_queue and not in_closed_queue:
                print_board(successor.board)
                print(successor.hn)
                # estimate h(n'), g(n') = g(n) + c(n, n'), f(n') = g(n') + h(n')

                successor.hn = manhattan(successor.board)
                successor.gn = gn
                successor.fn = successor.gn + successor.hn
                open_queue.put(successor)
            else:
                print("seen this beofre")
                twin = get_twin(successor, open_queue) if in_open_queue else get_twin(successor, open_queue)

                if gn < twin.gn:
                    twin.parent = current_state
                    twin.gn = gn
                    if in_closed_queue:
                        closed_queue.remove(twin)
                        open_queue.put(twin)


def main():
    print("main")
    board = make_board()

    initial_state = State(0, board, None)
    final = a_star_search(initial_state)

    a = final
    while a is not None:
        print_board(a.board)
        a = a.parent


if __name__ == "__main__":
    main()


# goal_board = [[1,    2,     3,    4,  5],
#              [6, hole,     7, hole,  8],
#              [9,   10, blank,   11, 12],
#              [13, hole,   14, hole, 15],
#              [16,  17,    18,   19, 20]]


# def make_board():
#    board = [[2,    3,     7,    4,  5],
#             [1, hole,    11, hole,  8],
#             [6,   10, blank,   12, 15],
#             [9, hole,    14, hole, 20],
#             [13,  16,    17,   18, 19]]
#    return board
