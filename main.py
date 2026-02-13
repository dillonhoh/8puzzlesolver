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


def ucs(initial_state):
    root = Node(initial_state, cost=0)
    q = []
    count = 0
    heapq.heappush(q, (0, count, root))



    return None
