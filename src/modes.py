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

    branch3 = Branch(200, 400, birds3, BRANCH_IMAGE, side="left")
    branch1 = Branch(200, 200, birds1, BRANCH_IMAGE, side="left")
    
    branch2 = Branch(900, 400, birds2, BRANCH_IMAGE, side="right")
    

    return [branch3, branch1, branch2]



