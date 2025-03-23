from collections import deque
import game_logic
from branch import Branch 
from bird import Bird
import heapq

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

class GameState:
    #branches = []
    def __init__(self, branches):
        self.branches = tuple(branches)
    def __eq__(self, other):
        return isinstance(other, GameState) and self.branches == other.branches

    def __hash__(self):
        return hash(self.branches)

    def __str__(self):
        return "\n".join(str(branch) for branch in self.branches)

    def generate_child_states(self):
        child_states = []
        for origin in self.branches:
            if origin.completed:  
                continue 

            for destination in self.branches:
                if origin != destination and not destination.completed and game_logic.can_move_birds(origin, destination):
                    new_branches = [Branch(branch.x, branch.y, branch.birds.copy(), branch.image) for branch in self.branches]

                    origin_index = self.branches.index(origin)
                    destination_index = self.branches.index(destination)

                    game_logic.move_birds(new_branches[origin_index], new_branches[destination_index])

                    new_branches = game_logic.remove_full_branches(new_branches)

                    new_state = GameState(tuple(new_branches))

                    if new_state not in child_states:
                        child_states.append(new_state)

        return child_states
    
    def evaluate(self):
        points = 0
        for branch in self.branches:
            points += branch.evaluate()
        return points

# Breadth-First Search
def breadth_first_search(initial_state, goal_state_func, operators_func):
    print("\nStarting BFS Search")
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])
    while queue:
        node = queue.popleft()   # get first element in the queue
        print("\nExpanding State:")
        print(node.state)
        if goal_state_func(node.state.branches):   # check goal state
            return node

        new_states = operators_func(node.state)  # Generate next states
        print(f"Generated {len(new_states)} new states:")
        for i, state in enumerate(new_states, 1):
            print(f"State {i}:")
            print(state)
            print("------------------")

        for state in operators_func(node.state):   # go through next states
            if state not in visited:
              child = TreeNode(state, node)
              queue.append(child)
              visited.add(state)

    return None

# Depth-First Search
def depth_first_search(initial_state, goal_state_func, operators_func):
    visited = set()
    print("\nStarting DFS Search")
    root = TreeNode(initial_state)
    return dfs_recursive(initial_state, goal_state_func, operators_func, visited, None)

def dfs_recursive(state, goal_state_func, operators_func, visited, parent):
    print("\nExpanding State:")
    print(state)
    visited.add(state)
    node = TreeNode(state, parent)

    if goal_state_func(state.branches):
        return node  # Return the goal node

    new_states = operators_func(state)

    print(f"Generated {len(new_states)} new states:")
    for i, child_state in enumerate(new_states, 1):
        print(f"State {i}:")
        print(child_state)
        print("------------------")

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

# Greedy Algorithm
def greedy_bf(initial_state, check_win, new_states):
    #print("\nStarting BFS Search")
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_state])
    while queue:
        node = queue.popleft()   # get first element in the queue
        #print("\nExpanding State:")
        #print(node.state)
        if check_win(node.state.branches):   # check goal state
            return node

        #new_states = new_states(node.state) 
        #print(f"Generated {len(new_states)} new states:")
        #for i, state in enumerate(new_states, 1):
            #print(f"State {i}:")
            #print(state)
            #print("------------------")

        best_state = None
        best_score = 0

        # Evaluate each new state and select the best one
        for state in new_states(node.state):
            if state not in visited:
                score = state.evaluate()  # Evaluate state
                
                if score > best_score:  # Keep track of the best state
                    best_score = score
                    best_state = state

        # Expand only the best state
        if best_state:
            child = TreeNode(best_state, node)
            queue.append(child)
            visited.add(best_state)

    return None


def greedy_df(initial_state, check_win, new_states):
    root = TreeNode(initial_state)  # Create the root node
    stack = [root]  # Use a stack instead of a queue (DFS)
    visited = set([initial_state])

    while stack:
        node = stack.pop()  # DFS: Get the last inserted node (LIFO)

        if check_win(node.state.branches):  # Check goal state
            return node  # Return the solution node

        best_state = None
        best_score = 0

        # Evaluate all possible next states and pick the best one
        for state in new_states(node.state):
            if state not in visited:
                score = state.evaluate()  # Evaluate state
                
                if score > best_score:  # Keep track of the best option
                    best_score = score
                    best_state = state

        # Expand only the best state (Greedy choice)
        if best_state:
            child = TreeNode(best_state, node)
            stack.append(child)  # Use stack for DFS behavior
            visited.add(best_state)

    return None  # No solution found

def a_star_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    priority_queue = []
    heapq.heappush(priority_queue, (0, id(root), root)) #f(n) = g(n)->number of movements + h(n)-> greedy heuristic
    visited = {}
    visited[initial_state] = 0
    while priority_queue:
       _, _, node = heapq.heappop(priority_queue)
       if goal_state_func(node.state.branches):
           return node
       g = visited[node.state] + 1 #g(n)
       for state in operators_func(node.state):
           h = 100 - state.evaluate()
           f = g + h
           if state not in visited or g < visited[state]:
               visited[state] = g 
               child = TreeNode(state, node)
               heapq.heappush(priority_queue, (f, id(child), child))
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