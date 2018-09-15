import numpy as np
from queue import PriorityQueue
from itertools import product

blank = 0
black_hole = -1
initial_board = np.array([[2, 3, 7, 4, 5], [1, black_hole, 11, black_hole, 8], [6, 10, blank, 12, 15],
                          [9, black_hole, 14, black_hole, 20], [13, 16, 17, 18, 19]])

goal_board = np.array([[1, 2, 3, 4, 5], [6, black_hole, 7, black_hole, 8], [9, 10, blank, 11, 12],
                       [13, black_hole, 14, black_hole, 15], [16, 17, 18, 19, 20]])


class CustomQueue(PriorityQueue):
    def contains(self, item):
        return self.queue.__contains__(item)

    def peak_item(self, item):
        print("")
        for i in self.queue:
            if i == item:
                return i
        return None

    def remove(self, item):
        if not self.contains(item):
            return False
        print("in remove")
        for i in range(len(self.queue) - 1):
            if self.queue[i] == item:
                del self.queue[i]
        return True


class State:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.gn = parent.gn + 1 if parent else 0
        self.hn = heuristic(board)
        self.fn = self.gn + self.hn

    def __lt__(self, other):
        return self.fn < other.fn

    def __eq__(self, other):
        return (np.array(self.board) == np.array(other.board)).all()

    def set_fn(self):
        self.fn = self.gn + self.hn


def print_state(state):
    def print_board():
        for row in state.board:
            print(row)
    print("")
    print_board()
    print("\tgn = " + str(state.gn) + "\n\thn = " + str(state.hn) + "\n\tfn = " + str(state.fn))


def swap(a, b, board):
    temp = board[b[1]][b[0]]
    board[b[1]][b[0]] = board[a[1]][a[0]]
    board[a[1]][a[0]] = temp


def index_of(item, board):
    for x, y in product(range(len(board)), range(len(board))):
        if board[y][x] == item:
            return x, y


def tiles_misplaced(board):
    distance = 0
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != goal_board[y][x]:
                distance += 1
    return distance


def manhattan(board):
    def distance_of(item):
        a = index_of(item, board)
        b = index_of(item, goal_board)
        return abs(a[1] - b[1]) + abs(a[0] - b[0])
    return sum([distance_of(item) for row in board for item in row])


def heuristic(board):
    return tiles_misplaced(board)


def possible_moves(index, board):
    moves = []
    if index[1] > 0 and board[index[1] - 1][index[0]] != black_hole:
        moves.append((index[0], index[1] - 1))
    if index[0] > 0 and board[index[1]][index[0] - 1] != black_hole:
        moves.append((index[0] - 1, index[1]))
    if index[1] < len(board) - 1 and board[index[1] + 1][index[0]] != black_hole:
        moves.append((index[0], index[1] + 1))
    if index[0] < len(board) - 1 and board[index[1]][index[0] + 1] != black_hole:
        moves.append((index[0] + 1, index[1]))
    return moves


def generate_successor_states(state):
    blank_location = index_of(0, state.board)
    states = []

    for move in possible_moves(blank_location, state.board):
        test_board = np.copy(state.board)
        swap(move, blank_location, test_board)
        states.append(State(test_board, state))

    return states


def a_star(initial_state):
    closed_queue = CustomQueue()
    open_queue = CustomQueue()
    open_queue.put(initial_state)
    goal_state = State(goal_board, None)
    unique_states_explored = 0
    total_states_explored = 0
    total_expanded_states = 0


    while not open_queue.empty():
        current_state = open_queue.get()
        closed_queue.put(current_state)
        print_state(current_state)
        total_expanded_states += 1

        if current_state == goal_state:
            return current_state, unique_states_explored, total_states_explored, total_expanded_states

        successor_states = generate_successor_states(current_state)
        new_gn = current_state.gn + 1

        for successor_state in successor_states:
            open_contains_successor = open_queue.contains(successor_state)
            closed_contains_successor = closed_queue.contains(successor_state)
            successor_state.parent = current_state
            print_state(successor_state)
            total_states_explored += 1

            if not open_contains_successor and not closed_contains_successor:
                unique_states_explored += 1
                open_queue.put(successor_state)
            else:
                successor_state_twin = open_queue.peak_item(successor_state) \
                    if open_contains_successor else closed_queue.peak_item(successor_state)

                if new_gn < successor_state_twin.gn:
                    successor_state_twin.parent = current_state
                    successor_state_twin.gn = new_gn
                    successor_state_twin.set_fn()

                    if closed_contains_successor:
                        closed_queue.remove(successor_state_twin)
                        open_queue.put(successor_state_twin)


def main():
    print("main")
    initial_state = State(initial_board, None)
    initial_state.gn = 0
    result = a_star(initial_state)
    final = result[0]
    path_length = 0

    print("------path------\n\n")
    while final is not None:
        print_state(final)
        final = final.parent
        path_length += 1
    print("path length = " + str(path_length) + "\nunique states explored = " + str(result[1]))
    print("total states explored = " + str(result[2]) + "\ntotal states expanded = " + str(result[3]))


if __name__ == "__main__":
    main()
