import pygame
import random
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
]
BRANCH_IMAGE = pygame.image.load("../assets/branch.png")

# Scale images
BIRD_IMAGES = [pygame.transform.scale(img, (50, 50)) for img in BIRD_IMAGES]
BRANCH_IMAGE = pygame.transform.scale(BRANCH_IMAGE, (120, 30))

# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sorter Game")

# Create Branches and Birds
branches = [Branch(200, 500, BRANCH_IMAGE), Branch(400, 500, BRANCH_IMAGE), Branch(600, 500, BRANCH_IMAGE)]
birds = [Bird(random.choice([200, 400, 600]), 200, random.randint(0, 1), BIRD_IMAGES) for _ in range(6)]

# Game Loop
running = True
clock = pygame.time.Clock()
selected_bird = None
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bird in birds:
                if bird.rect.collidepoint(event.pos):
                    selected_bird = bird if not selected_bird else None
            for branch in branches:
                if branch.rect.collidepoint(event.pos) and selected_bird:
                    if branch.add_bird(selected_bird):
                        birds.remove(selected_bird)
                    selected_bird = None
    
    # Draw everything
    for branch in branches:
        screen.blit(branch.image, branch.rect)
    for bird in birds:
        screen.blit(bird.image, bird.rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
