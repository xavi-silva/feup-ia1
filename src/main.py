import pygame
import random
import game_logic
from collections import deque
from bird import Bird
from branch import Branch

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (135, 206, 250)  # Sky Blue
FPS = 60

# Load images
BIRD_IMAGES = [
    pygame.image.load("../assets/bird1.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
    pygame.image.load("../assets/bird2.png"),
]

BRANCH_IMAGE = pygame.image.load("../assets/branch.png")

# Scale images
BIRD_IMAGES = [pygame.transform.scale(img, (50, 50)) for img in BIRD_IMAGES]
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (120, 30))

# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sorter Game")

# Create Branches and Birds
birds = [Bird(i, BIRD_IMAGES[i]) for i in range(9)]
#branches = [Branch(200, 500, [birds[0], birds[1]], BRANCH_IMAGE), Branch(400, 500, [birds[0], birds[1]], BRANCH_IMAGE), Branch(600, 500, [birds[0], birds[1]], BRANCH_IMAGE)]

branch1 = Branch(200, 500, [birds[0], birds[0]], BRANCH_IMAGE)
branch2 = Branch(300, 500, [], BRANCH_IMAGE)
branch3 = Branch(400, 500, [birds[0]], BRANCH_IMAGE)

branches = [branch1, branch2, branch3]

# Test code here
for branch in branches:
    print(branch)

print("............")

s = game_logic.get_valid_moves(branches)
for pair in s:
    print(f"({pair[0]}, {pair[1]})")

game_logic.move_birds(branch3, branch1)
print("............")

#s = (game_logic.get_valid_moves(branches))

#for move in s:
#    print(f"({move[0]}, {move[1]})")


#s = branch3.full_one_species()
#print(s)

for branch in branches:
    print(branch)

# Game Loop
running = True
clock = pygame.time.Clock()
selected_bird = None
while running:
    screen.fill(BACKGROUND_COLOR)
    
    #for event in pygame.event.get():
    #    if event.type == pygame.QUIT:
    #        running = False
    #    elif event.type == pygame.MOUSEBUTTONDOWN:
    #        for bird in birds:
    #            if bird.rect.collidepoint(event.pos):
    #                selected_bird = bird if not selected_bird else None
    #        for branch in branches:
    #            if branch.rect.collidepoint(event.pos) and selected_bird:
    #                if branch.add_bird(selected_bird):
    #                    birds.remove(selected_bird)
    #                selected_bird = None
    
    # Draw everything
    for branch in branches:
        screen.blit(branch.image, branch.rect)
    #for bird in birds:
     #   screen.blit(bird.image, bird.rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
