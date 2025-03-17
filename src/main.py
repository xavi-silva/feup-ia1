import pygame
import random
import game_logic
from graph import breadth_first_search, depth_first_search, GameState
from collections import deque
from bird import Bird
from branch import Branch
import modes

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 1100, 800
BACKGROUND_COLOR = (135, 206, 250)  # Sky Blue
FPS = 60


# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sorter")

difficulty = "easy"

if difficulty == "easy":
    branches = modes.easy_mode()
elif difficulty == "medium":
    branches = modes.medium_mode()
elif difficulty == "hard":
    branches = modes.hard_mode()
else:
    branches = modes.easy_mode()

initial_state = GameState(branches)

search_algorithm = "dfs"

if search_algorithm == "bfs":
    solution_node = breadth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "dfs":
    solution_node = depth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
else:
    print("Invalid search algorithm.")

# Print the solution path
if solution_node:
    print("Solution Found!\n")
    path = []
    while solution_node:
        path.append(solution_node.state)
        solution_node = solution_node.parent

    path.reverse()

    for step_num, state in enumerate(path):
        print(f"Step {step_num}:")
        print(state)
        print("------------------")
else:
    print("No solution found.")

#print("Initial State:")
#for branch in branches:
#    print(branch)

# Generate child states
#new_states = initial_state.generate_child_states()

#print("\nGenerated States:")
#for i, state in enumerate(new_states):
#    print(f"State {i+1}:")
#    print(state)  # Print the GameState object directly (uses __str__ method)
#    print("------------------")

#print("............")


#for branch in branches:
#    print(branch)

#print("............")

#s = game_logic.get_valid_moves(branches)
#for pair in s:
#    print(f"({pair[0]}, {pair[1]})")

#game_logic.move_birds(branch3, branch1)
#print("............")

#s = (game_logic.get_valid_moves(branches))

#for move in s:
#    print(f"({move[0]}, {move[1]})")


#s = branch3.full_one_species()
#print(s)

#for branch in branches:
#    print(branch)
sky = pygame.image.load("../assets/sky.webp")
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))

def draw_game(branches):
    #screen.fill(BACKGROUND_COLOR)  # Clear the screen
    screen.blit(sky, (0, 0))

    for branch in branches:
        branch.update_color()
        screen.blit(branch.image, branch.rect)

        # Draw birds on top of branches
        for i, bird in enumerate(branch.birds):
            branch_width = branch.image.get_width()
            bird_x = branch.x - (branch_width // 2) + 150 + (i * 100) if branch.side == "left" else branch.x + (branch_width // 2) - 150 - (i * 100)
            bird_img = bird.image if branch.side == "left" else pygame.transform.flip(bird.image, True, False)
            bird_rect = bird.image.get_rect(midbottom=(bird_x, branch.y))
            screen.blit(bird_img, bird_rect)

    pygame.display.flip()  # Update display

# Game Loop
selected_branch = None
move_mode = False

draw_game(branches)
pygame.time.delay(2000)
running = True

pygame.mixer.music.load("../sounds/background.mp3")
pygame.mixer.music.play(-1)
bird_sound = pygame.mixer.Sound("../sounds/bird.wav")
move_sound = pygame.mixer.Sound("../sounds/wings.wav")
branch_sound = pygame.mixer.Sound("../sounds/leaves.wav")

clock = pygame.time.Clock()
selected_bird = None
while running:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for branch in branches:
                if branch.rect.collidepoint(event.pos):
                    if not move_mode:
                        if selected_branch:
                            selected_branch.selected = False
                            selected_branch.update_color()

                        selected_branch = branch
                        bird_sound.play()
                        selected_branch.selected = True
                        selected_branch.update_color()

                        move_mode = True
                    else:
                        if selected_branch and selected_branch != branch:
                            move_sound.play()
                            game_logic.move_birds(selected_branch, branch)
                            #sleep 1 second
                            pygame.time.delay(1000)
                            if (branch.full_one_species()):
                                branch_sound.play()
                            selected_branch.selected = False
                            selected_branch.update_color()

                            selected_branch = None
                            move_mode = False

                            if game_logic.check_win(branches):
                                print("You Win!")
                                running = False

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
    draw_game(branches)
    #for bird in birds:
     #   screen.blit(bird.image, bird.rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
