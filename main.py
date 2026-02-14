import heapq
import sys

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)


class Node:
    def __init__(self, state, parent=None, cost=0): # puzzle state, parent node, path cost
        self.state = state  # tuple of board state
        self.parent = parent  # parent node
        self.cost = cost  # g(n) represents cost from the start state to current node


def success(state):
    return state == GOAL_STATE


def expand(node):
    children = []
    state = node.state
    blankIndex = state.index(0)  # blank tile index

    
    row = blankIndex // 3 # index to row, col
    col = blankIndex % 3
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # left, right, up, down

    for dr, dc in directions:
        nr, nc = row + dr, col + dc # check all legal directions
        if 0 <= nr < 3 and 0 <= nc < 3: # edge cases
            newIndex = nr * 3 + nc
            newState = list(state)
            
            newState[blankIndex], newState[newIndex] = (newState[newIndex], newState[blankIndex]
            ) # swap with blank
            
            child = Node(tuple(newState), parent=node, cost=node.cost + 1) # create child
            children.append(child)

    return children


def ucs(initial_state, heuristic=None):
    root = Node(initial_state, cost=0)
    q = []  # minheap
    counter = 0  

    if heuristic is None:
        start_priority = 0 # h(n) is 0
    else:
        start_priority = heuristic(initial_state)
    heapq.heappush(q, (start_priority, counter, root))

    minCost = {root.state: 0}  # min g-cost for each visited state
    nodesExpanded = 0  # number of nodes expanded
    max_queue_size = len(q)  # queue size at its most

    while q:
        priority, nodeCounter, node = heapq.heappop(q)

        if node.cost > minCost.get(node.state, float('inf')): # skip if g is not a better cost
            continue

        if success(node.state): # "if problem.goal-test(node.state)"
            return node, nodesExpanded, max_queue_size

        nodesExpanded += 1

        
        for child in expand(node): # expand and push children
            g = child.cost # g = path cost to reach this child instance
            if g < minCost.get(child.state, float('inf')): # only accept this if better g cost
                minCost[child.state] = g
                counter += 1
                if heuristic is None:
                    heapq.heappush(q, (g, counter, child))
                else:
                    heapq.heappush(q, (g + heuristic(child.state), counter, child))

        max_queue_size = max(max_queue_size, len(q))

    return None, nodesExpanded, max_queue_size


def heuristic_misplaced(state):
    
    return sum(1 for i, v in enumerate(state) if v != 0 and v != GOAL_STATE[i]) # tiles that are not in their goal position. max 8


def heuristic_manhattan(state):
   
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue  # skip blank
        goal_idx = GOAL_STATE.index(val)
        r1 = idx // 3
        c1 = idx % 3
        r2 = goal_idx // 3
        c2 = goal_idx % 3
        # converting index to r, c
        dist += abs(r1 - r2) + abs(c1 - c2) # sum of all tile's distance from its current position to its goal position
    return dist


def trace_solution(node):
    path = []
    while node: # add last state(goal), go up to parent, add parent
        path.append(node.state)
        node = node.parent 
    return path[::-1] # print in reverse ( starting from root)


def main():
    DEFAULT1 = (1, 2, 3,
                4, 5, 6,
                7, 8, 0)  # solved
    DEFAULT2 = (1, 3, 6,
                5, 0, 2,
                4, 7, 8)  # depth 8
    DEFAULT3 = (0, 7, 2,
                4, 6, 1,
                3, 5, 8)  # depth 24
    def inputPuzzle():
        print("Each row should only contain 3 numbers. Only integers 0-8 can be inputed, each exactly once.")
        rows = []
        for r in range(1, 4):
            rowInput = input(f"Enter row {r} : ")
            nums = rowInput.replace(',', ' ').split()
            if len(nums) != 3:
                print("Invalid input, each row must contain exactly 3 numbers.")
                sys.exit(1)
            for n in nums:
                if not n.isdigit() or not (0 <= int(n) <= 8): 
                    print("Invalid input, please enter only integers 0-8.")
                    sys.exit(1)
            rows.extend(int(n) for n in nums) # append to our actual row

        if set(rows) != set(range(9)):
            print("Invalid input, numbers must be unique 0-8.")
            sys.exit(1)

        return tuple(rows) # normalize back to tuple
    
    while True:
        puzzleMode = input("This is an 8-Puzzle Solver. Type '1' for default puzzles, or '2' to input your own puzzle: ")
        if puzzleMode == '1':
            while True:
                choice = input("Choose a puzzle. Type '1' for a solved puzzle, '2' for a Depth 8 puzzle, or '3' for a Depth 24 puzzle: ")
                if choice == '1':
                    start = DEFAULT1
                    break
                if choice == '2':
                    start = DEFAULT2
                    break
                if choice == '3':
                    start = DEFAULT3
                    break
                print("Please enter a value 1-3.")
            break
        if puzzleMode == '2':
            start = inputPuzzle() 
            break
        print("Please enter a value 1-2.")

    while True:
        alg = input("Choose an algorithm: Type '1' for UCS, '2' for Misplaced Tile Heuristic, or '3' for Manhattan Distance Heuristic: ").strip()
        if alg in ('1', '2', '3'): 
            break
        print("Please enter a value 1-3.")

    if alg == '1':
        node, nodesExpanded, max_queue_size = ucs(start)
    elif alg == '2':
        node, nodesExpanded, max_queue_size = ucs(start, heuristic_misplaced)
    else:
        node, nodesExpanded, max_queue_size = ucs(start, heuristic_manhattan)

    if node:
        path = trace_solution(node) # remember path is already reversed within the fyunction
        depth = len(path) - 1
        for step in path:
            print(list(step[:3])) # list for bracket []
            print(list(step[3:6]))
            print(list(step[6:]))
            print()
        print(f"Solution depth (moves): {depth}")
        print(f"Nodes expanded: {nodesExpanded}")
        print(f"Max queue size: {max_queue_size}")
        print()
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
    