import pygame
from branch import Branch
from bird import Bird

# Load images (should be done only once)
BIRD_IMAGES = [
    pygame.image.load("../assets/bird1.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird3.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
]

BRANCH_IMAGE = pygame.image.load("../assets/branch.png")
BIRD_IMAGES = [pygame.transform.scale(img, (100, 100)) for img in BIRD_IMAGES]
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (500, 500))

def easy_mode():
    birds = [Bird(i, BIRD_IMAGES[i]) for i in range(9)]
    
    branch1 = Branch(200, 200, [birds[0], birds[0], birds[1]], BRANCH_IMAGE, side="left")
    branch2 = Branch(900, 400, [birds[1], birds[1], birds[1]], BRANCH_IMAGE, side="right")
    branch3 = Branch(200, 600, [birds[0], birds[0]], BRANCH_IMAGE, side="left")

    return [branch1, branch2, branch3]

def medium_mode():
    birds = [Bird(i, BIRD_IMAGES[i]) for i in range(9)]

