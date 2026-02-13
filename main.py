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

    while q:
        priority, nodeCounter, node = heapq.heappop(q)

        if node.cost > minCost.get(node.state, float('inf')):
            continue

        if success(node.state):
            return node

        for child in expand(node):
            g = child.cost
            if g < minCost.get(child.state, float('inf')):
                minCost[child.state] = g
                counter += 1
                heapq.heappush(q, (g, counter, child))

    return None

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
        
        node = ucs(DEFAULT1)
        if node:
            print(f"Default 1: solved")
        else:
            print(f"Default 1: no solution found")

        node = ucs(DEFAULT2)
        if node:
            print(f"Default 2: solved")
        else:
            print(f"Default 2: no solution found")

        node = ucs(DEFAULT3)
        if node:
            print(f"Default 3: solved")
        else:
            print(f"Default 3: no solution found")
        break
        

if __name__ == "__main__":
    main()
    
