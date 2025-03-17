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
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (500, 500))

def easy_mode():
    birds = [Bird(i, BIRD_IMAGES[i]) for i in range(7)]

    birds1 = deque([birds[0], birds[0], birds[1]])
    birds2 = deque([birds[1], birds[1], birds[1]])
    birds3 = deque([birds[0], birds[0]])

    branch1 = Branch(200, 200, birds1, BRANCH_IMAGE, side="left")
    branch2 = Branch(900, 400, birds2, BRANCH_IMAGE, side="right")
    branch3 = Branch(200, 600, birds3, BRANCH_IMAGE, side="left")

    return [branch1, branch2, branch3]

def medium_mode():
    birds = [Bird(i, BIRD_IMAGES[i]) for i in range(7)]

    birds1 = deque([birds[0], birds[1],birds[2], birds[3]])
    birds2 = deque([birds[1], birds[0],birds[3], birds[3]])
    birds3 = deque([birds[3], birds[0],birds[2], birds[1]])
    birds4 = deque([])
    birds5 = deque([birds[1], birds[2],birds[4], birds[0]])
    birds6 = deque([birds[5], birds[5],birds[4], birds[5]])
    birds7 = deque([birds[4], birds[4],birds[5], birds[2]])
    birds8 = deque([])

    branch1 = Branch(200, 200, birds1, BRANCH_IMAGE, side="left")
    branch2 = Branch(200, 400, birds2, BRANCH_IMAGE, side="left")
    branch3 = Branch(200, 600, birds3, BRANCH_IMAGE, side="left")
    branch4 = Branch(200, 800, birds4, BRANCH_IMAGE, side="left")
    branch5 = Branch(900, 200, birds5, BRANCH_IMAGE, side="right")
    branch6 = Branch(900, 400, birds6, BRANCH_IMAGE, side="right")
    branch7 = Branch(900, 600, birds7, BRANCH_IMAGE, side="right")
    branch8 = Branch(900, 800, birds8, BRANCH_IMAGE, side="right")
    return [branch1, branch2, branch3, branch4, branch5, branch6, branch7, branch8]

