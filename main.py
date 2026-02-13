import heapq

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)
class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost


def success(state):
    return state == GOAL_STATE

def expand(node):
    children = []
    state = node.state
    blankIndex = state.index(0)

    row = blankIndex // 3
    col = blankIndex % 3
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            newIndex = nr * 3 + nc
            newState = list(state)
            newState[blankIndex], newState[newIndex] = (
                newState[newIndex], newState[blankIndex]
            )
            child = Node(tuple(newState), parent=node, cost=node.cost + 1)
            children.append(child)

    return children


def ucs(initial_state):
    root = Node(initial_state, cost=0)
    q = []
    counter = 0
    heapq.heappush(q, (0, counter, root))

    minCost = {root.state: 0}
    nodesExpanded = 0
    max_queue_size = len(q)

    while q:
        priority, nodeCounter, node = heapq.heappop(q)

        if node.cost > minCost.get(node.state, float('inf')):
            continue

        if success(node.state):
            return node, nodesExpanded, max_queue_size

        nodesExpanded += 1

        for child in expand(node):
            g = child.cost
            if g < minCost.get(child.state, float('inf')):
                minCost[child.state] = g
                counter += 1
                heapq.heappush(q, (g, counter, child))

        max_queue_size = max(max_queue_size, len(q))

    return None, nodesExpanded, max_queue_size

def trace_solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

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
            break
        print("Please enter a value 1-2.")

    node, num_nodes_expanded, max_queue_size = ucs(start)

    if node:
        path = trace_solution(node)
        depth = len(path) - 1
        for step in path:
            print(list(step[:3]))
            print(list(step[3:6]))
            print(list(step[6:]))
            print()
        print(f"Solution depth (moves): {depth}")
        print(f"Nodes expanded: {num_nodes_expanded}")
        print(f"Max queue size: {max_queue_size}")
        print()
    else:
        print("No solution found.")
        

if __name__ == "__main__":
    main()
    
