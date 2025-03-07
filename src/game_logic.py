from bird import Bird
from branch import Branch

def can_move_birds(origin_branch, destination_branch):
    if len(destination_branch.birds) >= Branch.branch_size:
        return False
    if origin_branch.is_empty():
        return False
    if destination_branch.is_empty():
        return True
    if origin_branch.get_top()[0] == destination_branch.get_top()[0]:
        return True
    return False

def move_birds(origin_branch, destination_branch):
    if can_move_birds(origin_branch, destination_branch):
        top_birds = origin_branch.get_top()
        max_birds = destination_branch.branch_size - len(destination_branch.birds)
        n_birds = min(top_birds[1], max_birds)
        origin_branch.remove_birds(n_birds)
        destination_branch.add_birds(top_birds[0], n_birds)
        return True
    return False

def check_win(branches):
    for branch in branches:
        if not branch.is_empty():
            return False
    return True

# probably unnecessary function
def get_valid_moves(branches):
    moves = []
    for origin_branch in branches:
        for destination_branch in branches:
            if origin_branch != destination_branch:
                if can_move_birds(origin_branch, destination_branch):
                    moves.append((origin_branch, destination_branch))
    return moves











