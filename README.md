

Score function:
Given a queen located at (x, y), to find the score of a state we check each entry in column x and sum up all the conflicts, i.e the “1”s. Similarly, we do the same for row y and the diagonals of (x, y). This retrieves how many “conflicts” a queen currently has. To score the current state of the board, we iterate over each queen in the board and sum up their conflicts. The initial state has a score of 600 (each queen has 24 conflicts) and we desire a state with a score of 0. 

The following example has 6 conflicts. A “1”
[1, 0, 0]
[0, 1, 0]
[0, 0, 1]
represents a queen:





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




Note: get_queens() returns a list of (x, y) coordinates which contain all 25 queens. 







Neighbor function:
The neighbor function generates all possible neighbors with the intention to pick the neighboring state with the lowest score. My methodology is as follows: 
To determine which move is optimal, we iterate over the list of queens and generate each possible successor state by moving that queen. Successor states are determined by moving a queen to any location horizontally. That is, we only move queens within their respective rows. This is because the defined initial state places all queens in the diagonal starting in the upper left corner. This is an optimization strategy: queens do not need to be moved vertically since each queen is already in their own rows. 
Once we generate a successor state for a queen, we check its score. If its score is better than the best score seen so far (initially infinity), we retain that successor state. After checking all possible moves for the 25 queens, we return the best, optimal, successor state.

def move(queen, new_x, board):
board[queen[1]][queen[0]] = 0
board[queen[1]][new_x] = 1


def find_best_move_for_queen(queen, board):
best_move = (0, 0, 0, math.inf)  # x, y, x_offset, score

for x in range(len(board)):
test_board = np.copy(board)
move(queen, x, test_board)
score = score_board_state(test_board)

if score <= best_move[3]:
best_move = (queen[0], queen[1], x, score)

return best_move


def make_best_move(board):
best_move = (0, 0, 0, math.inf)  # x, y, x_offset, score

for q in get_queens(board):
queen_best_move = find_best_move_for_queen(q, board)
if queen_best_move[3] <= best_move[3]:
best_move = queen_best_move

move((best_move[0], best_move[1]), best_move[2], board)
return best_move






Best state:
The best state I found was the goal state with zero conflicts. Here, all conditions are satisfied: no two queens share a (1) row, (2) column, (3) diagonals.
This state took 328 steps to generate. It is the fastest (least amount of steps) I was able to generate. On average, finding the goal state for my approach required 1500+ steps.
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 













Approach used:
I used the hill climbing approach with a stochastic randomized gradient. Before the algorithm commits to a specific move, it checks what the score would be like if it made that move. After finding the ideal move, it commits it. 
In my initial attempt, I ran into the issue of getting stuck in a local optima. The board would reach a state where there are remaining conflicts but making any movement would result in a higher amount of conflicts. The solution I came up with was implementing a stochastic randomized gradient. Essentially, once we detect we are in a local optima, we make 25 sequential random moves. One at a time, a queen would be placed in a random location within its current row which does not violate the rules of queen movement. Doing this to every queen results in a state which is equivalent to a random state, however, in contrast to “random restart”, the state generated using my stochastic randomized gradient is reachable from the local optima. This almost always resulted in a state with a higher score (not to be confused with a more desirable score since score reflects number of conflicts), however, it allowed the algorithm to exit the local optima. 



























A* Algorithm: implementation to solve the square puzzle 

Steps to goal state:
The path from the initial state to the goal state took 17 steps. 

Number of states explored before reaching goal state:
While looking for the shortest path, my program expanded (created  successors for) 24 states , explored (computed the Manhattan distance for) 56 states, of which 34 were unique, never seen before. 

Fifth and fifth-to-last state:

Note: “0” represents the blank and “-1” represents the blackhole. 

Fifth state:                Fifth-to-last state:
[ 0  2  3  4  5]
[ 1 -1  7 -1  8]
[ 6 10 11 12 15]
[ 9 -1 14 -1 20]
[13 16 17 18 19]
gn = 4
hn = 16
fn = 20
[ 1  2  3  4  5]
[ 6 -1  7 -1  8]
[ 9 10 11 12 15]
[13 -1 14 -1 20]
[16 17 18 19  0]
gn = 12
hn = 8
fn = 20


























A* Algorithm: Prove A* is optimal given an admissible heuristic function 

Proof by contradiction:

Suppose that A* is not optimal given an admissible heuristic function. A heuristic function estimates of the cost of the path from the current state to the goal state. An Admissible heuristic is a heuristic which never overestimates the coast to reach the goal state from the current state:  is admissible if . That is, the cost is not higher than the possible lowest cost from the current state to the goal state. 

This means that the heuristic for A* overestimates the cost to reach the goal state from the current state. However, we know that A* expands nodes strictly following the inequality:  and calculates the actual cost by:


(Russel & Norvig, page 95)

Where  is a state,  is its successor,  is the cost from  to  given some action . This means that A* always chooses the next state to expand by picking the the one with the lowest estimated cost from the start state to the goal state. Therefore, this is a contradiction and A* is optimal given an admissible heuristic. 






















UCS Algorithm: Clarify difference between UCS and Dijkstra 

Dijkstra’s algorithm and Uniform-Cost-Search algorithm have many similarities. It is evident that Uniform-Cost-Search algorithm is a special variant of Dijkstra’s algorithm. Both operate using priority queues to find optimal paths. However, where they differ is in their concrete objective: Dijkstra’s algorithm aims to find the shortest path from a start state to every other state, while Uniform-Cost-Search algorithm aims to find a single shortest path from a start state to a goal state. Because of this, Uniform-Cost-Search is more efficient in time and space complexity. Uniform-Cost-Search algorithm terminates when it has found the shortest path to the goal state (or determined that no path exists) and Dijkstra’s algorithm terminates when it has visited all states (i.e. the priority queue is empty). Uniform-Cost-Search algorithm is more space-efficient because it is careful about how and when it places states in the priority queue whereas Dijkstra’s algorithm places every state it encounters into the priority queue. Uniform-Cost-Search algorithm is more time-efficient because it explores less states. While both are used for uninformed searching (where the distance to the goal state is unknown), Uninformed-Search-Cost algorithm is more ideal if we are seeking a particular state, i.e. a goal state. 


























Open question: create a better heuristic function for problem 2

For this problem, I tried two methods: (1) Euclidean distance and (2) Misplaced Tiles. I will outline my results and conclude that Misplaced Tiles is more admissible than Manhattan distance. 

Definition of better heuristic:
def euclidean_distance(board):
def distance_of(item):
a = index_of(item, board)
b = index_of(item, goal_board)
x = math.pow(abs(a[1] - b[1]), 2)
y = math.pow(abs(a[0] - b[0]), 2)
return math.sqrt(x + y)
return sum([distance_of(item) for row in board for item in row])


def misplaced_tiles(board):
distance = 0
for y in range(len(board)):
for x in range(len(board)):
if board[y][x] != goal_board[y][x]:
distance += 1
return distance


Steps to goal state:
Euclidean distance: 17 steps
Misplaced Tiles: 17 steps
Manhattan distance: 17 steps


Number of states explored before reaching goal state:
Manhattan distance
unique states explored = 34
total states explored = 56
total states expanded = 24
Euclidean distance
unique states explored = 26
total states explored = 44
total states expanded = 20
Misplaced Tiles
unique states explored = 24
total states explored = 40
total states expanded = 18



Fifth and fifth-to-last state:
Note: “0” represents the blank and “-1” represents the blackhole. 
Misplaced Tiles

[ 0  2  3  4  5]
[ 1 -1  7 -1  8]
[ 6 10 11 12 15]
[ 9 -1 14 -1 20]
[13 16 17 18 19]
gn = 4
hn = 13
fn = 17
Manhattan distance

[ 0  2  3  4  5]
[ 1 -1  7 -1  8]
[ 6 10 11 12 15]
[ 9 -1 14 -1 20]
[13 16 17 18 19]
gn = 4
hn = 16
fn = 20
Euclidean distance

[ 0  2  3  4  5]
[ 1 -1  7 -1  8]
[ 6 10 11 12 15]
[ 9 -1 14 -1 20]
[13 16 17 18 19]
gn = 4
hn = 14.82
fn = 18.82
5th





Euclidean distance

[ 1  2  3  4  5]
[ 6 -1  7 -1  8]
[ 9 10 11 12 15]
[13 -1 14 -1 20]
[16 17 18 19  0]
gn = 12
hn = 6.828
fn = 18.82
5th to last
Misplaced Tiles

[ 1  2  3  4  5]
[ 6 -1  7 -1  8]
[ 9 10 11 12 15]
[13 -1 14 -1 20]
[16 17 18 19  0]
gn = 12
hn = 5
fn = 17
Manhattan distance

[ 1  2  3  4  5]
[ 6 -1  7 -1  8]
[ 9 10 11 12 15]
[13 -1 14 -1 20]
[16 17 18 19  0]
gn = 12
hn = 8
fn = 20




























Why it improves on Manhattan distance:
While Manhattan distance is a prevailing heuristic, it was outperformed by both Euclidean distance and Misplaced Tiles. As shown in the above section: “Number of states explored before reaching goal state”, Manhattan distance explored significantly more states which, in turn, results in a higher computational cost and lower efficiency. For this problem, Misplaced Tiles performed best, and it is the heuristic I choose to proclaim as a better heuristic. A heuristic  dominates  if . As stated in class, a heuristic that estimates the cost to the goal state as closely as possible to the real cost (without exceeding it) is preferred. Therefore,  is the preferred heuristic. Manhattan distance cost from the initial state to the goal state was 16 and Misplaced tiles cost from the initial state to the goal state was 15. This forms the inequality: 



This seems to contradict my proclamation, however, the inequality only held true for the initial state.  for Misplaced Tiles never exceed 17 while  for Manhattan distance reached a high of 20. The heuristic function for Misplaced Tiles, from the second state on, decreased by one forming a linear regression, which is desirable. On the other hand, Manhattan distance jumped and dropped almost unpredictably, forming a sort of polynomial regression:
As the graph shows, Misplaced Tiles predicted the cost more consistently which also reflects the fact that Misplaced Tiles explored  40 total states while Manhattan distance explored 56 states total. This is also shown by calculating the standard deviation of the heuristics:

Manhattan: 
Misplaced Tiles: 

Therefore, it can be deduced that the Misplaced Tiles heuristic is the prevalent heuristic since it was constantly more accurate compared to the actual cost. 









