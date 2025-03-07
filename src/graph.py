from collections import deque
import game_logic
from branch import Branch 
from bird import Bird

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

# not tested yet
def child_states(branches):
    new_states = []
    for origin_branch in branches:
        for destination_branch in branches:
            if origin_branch != destination_branch:
                if game_logic.can_move_birds(origin_branch, destination_branch):
                    new_branches = [Branch(branch.x, branch.y, branch.birds.copy(), branch.image) for branch in branches]
                    game_logic.move_birds(new_branches[origin_branch], new_branches[destination_branch])
                    new_states.append(new_branches)
    return new_states

# copied search algorithms from buckets example, needs adjustments

# Breadth-First Search
def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])
    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        for state in operators_func(node.state):   # go through next states
            if state not in visited:
              child = TreeNode(state, node)
              queue.append(child)
              visited.add(state)

    return None

# Depth-First Search
def depth_first_search(initial_state, goal_state_func, operators_func):
    visited = set()
    return dfs_recursive(initial_state, goal_state_func, operators_func, visited, None)

def dfs_recursive(state, goal_state_func, operators_func, visited, parent):
    visited.add(state)
    node = TreeNode(state, parent)

    if goal_state_func(state):
        return node  # Return the goal node

    for neighbor in operators_func(state):
        if neighbor not in visited:
          result = dfs_recursive(neighbor, goal_state_func, operators_func, visited, node)
          if result:
              return result  # Return the found path

    return None  # No solution found

# Depth-Limited Search
def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    visited = set()
    return dls_recursive(initial_state, goal_state_func, operators_func, visited, None, depth_limit, 0)

def dls_recursive(state, goal_state_func, operators_func, visited, parent, depth_limit, depth):
    depth = depth + 1
    if depth > depth_limit:
        return None

    visited.add(state)
    node = TreeNode(state, parent)

    if goal_state_func(state):
        return node  # Return the goal node

    for neighbor in operators_func(state):
        if neighbor not in visited:
          result = dls_recursive(neighbor, goal_state_func, operators_func, visited, node, depth_limit, depth)
          if result:
              return result  # Return the found path

    return None  # No solution found

# Iterative Deepening Search
def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    for current_limit in range(depth_limit):
        s = depth_limited_search(initial_state, goal_state_func, operators_func, current_limit)
        if s:
            return s
    return None

# Auxiliar print function to show the solution
def print_solution(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    print(f"Found goal in {len(path) - 1} steps:")
    for step in path:
        print(step)