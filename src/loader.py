import pygame
from branch import Branch
from bird import Bird
from collections import deque

# Load images (should be done only once)
BIRD_IMAGES = [
    pygame.image.load("../assets/bird1.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird3.png"),
    pygame.image.load("../assets/bird4.png"),
    pygame.image.load("../assets/bird5.png"),
    pygame.image.load("../assets/bird6.png"),
    pygame.image.load("../assets/bird7.png"),
]

BRANCH_IMAGE = pygame.image.load("../assets/branch.png")
BIRD_IMAGES = [pygame.transform.scale(img, (100, 100)) for img in BIRD_IMAGES]
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (400, 150))

def load_branches_from_file(filename):
    branches = []
    side = "left"

    with open(filename, "r") as file:
        branch_size = int(file.readline().strip()[0])
        Branch.branch_size = branch_size

        left_y = 75
        right_y = 75
        left_x = 200
        right_x = 900
        for line in file:
            line = line.strip()
            
            if line == "\n" or line == "": 
                if side == "right":
                    print("Invalid file format: empty line found")
                    return []
                side = "right"
                continue
                
            if line == "-":
                if side == "left":
                    branch = Branch(left_x, left_y, [], BRANCH_IMAGE, side)
                    left_x = 200
                    left_y += 150

                else:
                    branch = Branch(right_x, right_y, [], BRANCH_IMAGE, side)
                    right_x = 900
                    right_y += 150
            else:
                birds = [Bird(int(char), BIRD_IMAGES[int(char)]) for char in line] if line else []
                if len(birds) > Branch.branch_size:
                    print("Invalid file format: too many birds in a branch")
                    return []
                if side == "left":
                    branch = Branch(left_x, left_y, birds, BRANCH_IMAGE, side)
                    left_x = 200
                    left_y += 150

                else:
                    branch = Branch(right_x, right_y, birds, BRANCH_IMAGE, side)
                    right_x = 900
                    right_y += 150
    
            branches.append(branch)
    return branches    

