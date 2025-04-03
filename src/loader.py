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
    pygame.image.load("../assets/bird8.png"),
    pygame.image.load("../assets/bird9.png"),
    pygame.image.load("../assets/bird10.png"),
]

BRANCH_IMAGE = pygame.image.load("../assets/branch.png")
BIRD_IMAGES = [pygame.transform.scale(img, (70, 70)) for img in BIRD_IMAGES]
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (500, 150))

BRANCH_GAP = 100

def load_branches_from_file(filename):
    branches = []
    side = "left"

    with open(filename, "r") as file:
        branch_size = int(file.readline().strip()[0])
        Branch.branch_size = branch_size

        left_y = 35
        right_y = 35
        left_x = 250
        right_x = 950
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
                    left_y += BRANCH_GAP

                else:
                    branch = Branch(right_x, right_y, [], BRANCH_IMAGE, side)
                    right_y += BRANCH_GAP
            else:
                birds = [Bird(int(char), BIRD_IMAGES[int(char)]) for char in line] if line else []
                if len(birds) > Branch.branch_size:
                    print("Invalid file format: too many birds in a branch")
                    return []
                if side == "left":
                    branch = Branch(left_x, left_y, birds, BRANCH_IMAGE, side)
                    left_y += BRANCH_GAP

                else:
                    branch = Branch(right_x, right_y, birds, BRANCH_IMAGE, side)
                    right_y += BRANCH_GAP
    
            branches.append(branch)
    return branches    

