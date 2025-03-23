import pygame
import random
import game_logic
from graph import breadth_first_search, depth_first_search, greedy_bf, greedy_df, a_star_search, GameState
from collections import deque
from bird import Bird
from branch import Branch
import loader

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

difficulty = "medium"

if difficulty == "easy":
    branches = loader.load_branches_from_file("../states/easy.txt")
elif difficulty == "medium":
    branches = loader.load_branches_from_file("../states/medium.txt")
elif difficulty == "hard":
    branches = loader.load_branches_from_file("../states/hard.txt")
elif difficulty == "custom":
    branches = loader.load_branches_from_file("../states/custom.txt")
else:
    branches = loader.easy_mode()

if branches == []:
    print("Invlid game state!")
    pygame.quit()

initial_state = GameState(branches)

search_algorithm = "A*"
solution_node = None

if search_algorithm == "bfs":
    solution_node = breadth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "dfs":
    solution_node = depth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "greedy_bf":
    solution_node = greedy_bf(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "greedy_df":
    solution_node = greedy_df(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "A*":
        solution_node = a_star_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
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

sky = pygame.image.load("../assets/sky.webp")
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))

def draw_game(branches):
    #screen.fill(BACKGROUND_COLOR)  # Clear the screen
    screen.blit(sky, (0, 0))
    score = font.render(f"Moves: {moves_count}", True, (0,0,0))
    screen.blit(score, (490,50))

    for branch in branches:
        if not(branch.completed):
            branch.update_color()
            screen.blit(branch.image, branch.rect)

            # Draw birds on top of branches
            for i, bird in enumerate(branch.birds):
                branch_width = branch.image.get_width()
                bird_x = branch.x - (branch_width // 2) + 65 + (i * 100) if branch.side == "left" else branch.x + (branch_width // 2) - 65 - (i * 100)
                bird_img = bird.image if branch.side == "left" else pygame.transform.flip(bird.image, True, False)
                bird_rect = bird.image.get_rect(midbottom=(bird_x, branch.y + 35))
                screen.blit(bird_img, bird_rect)
        #for branch in branches:
              ## pygame.draw.rect(screen, (255, 0, 0), branch.rect, 2)
    pygame.display.flip()  # Update display

# Game Loop
selected_branch = None
move_mode = False
moves_count = 0
font = pygame.font.Font(None, 36)
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
                        if selected_branch and selected_branch != branch and not branch.completed:
                            if (game_logic.move_birds(selected_branch, branch)):
                                moves_count += 1
                                print(moves_count)
                                move_sound.play()
                            #sleep 1 second
                            pygame.time.delay(500)
                            if (branch.full_one_species()):
                                branch_sound.play()
                            selected_branch.selected = False
                            selected_branch.update_color()

                            selected_branch = None
                            move_mode = False

                            if game_logic.check_win(branches):
                                print("You Win!")
                                running = False
                        elif selected_branch and selected_branch == branch:
                            selected_branch.selected = False
                            selected_branch.update_color()
                            selected_branch = None
                            move_mode = False

    # Draw everything
    draw_game(branches)
    #for bird in birds:
     #   screen.blit(bird.image, bird.rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
