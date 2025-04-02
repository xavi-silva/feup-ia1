import pygame
import random
import game_logic
from graph import breadth_first_search, depth_first_search, greedy_search, a_star_search, uniform_cost_search, iterative_deepening_search, give_hint, GameState
from collections import deque
from bird import Bird
from branch import Branch
import loader

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 1200, 800
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 50
BACKGROUND_COLOR = (135, 206, 250)  # Sky Blue
FPS = 60

# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sorter")
sky = pygame.image.load("../assets/sky.png")
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))
hint = pygame.image.load("../assets/hint.png")
hint = pygame.transform.scale(hint, (100, 100))
hint_rect = pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100)  # Create a rectangle for the clickable area
board = pygame.image.load("../assets/board.png")
button_board = pygame.image.load("../assets/button.png")
button_board = pygame.transform.scale(button_board, (250, 50))
menu = pygame.image.load("../assets/menu.gif")
menu = pygame.transform.scale(menu, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Menu Buttons
mode_buttons = [
    {"label": "Easy", "rect": pygame.Rect(WIDTH/2 - 125, 100, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Medium", "rect": pygame.Rect(WIDTH/2 - 125, 160, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Hard", "rect": pygame.Rect(WIDTH/2 - 125, 220, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Custom", "rect": pygame.Rect(WIDTH/2 - 125, 280, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

algorithm_buttons = [
    {"label": "Auto", "rect": pygame.Rect(WIDTH/2 - 125, 100, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Breadth-First Search", "rect": pygame.Rect(WIDTH/2 - 125, 150, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Depth-First Search", "rect": pygame.Rect(WIDTH/2 - 125, 200, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Iterative Deepening", "rect": pygame.Rect(WIDTH/2 - 125, 250, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Uniform Cost", "rect": pygame.Rect(WIDTH/2 - 125, 300, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Greedy", "rect": pygame.Rect(WIDTH/2 - 125, 350, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "A*", "rect": pygame.Rect(WIDTH/2 - 125, 400, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Weighted A*", "rect": pygame.Rect(WIDTH/2 - 125, 450, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

player_buttons = [
    {"label": "You", "rect": pygame.Rect(WIDTH/2 - 125, 150, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Bot", "rect": pygame.Rect(WIDTH/2 - 125, 220, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

def draw_buttons(buttons, hover_index):
    for i, button in enumerate(buttons):
        color = (0, 0, 0) if i == hover_index else (196, 164, 132)
        pygame.draw.rect(screen, (0, 0, 0), button["rect"], border_radius=10)
        pygame.draw.rect(screen, color, button["rect"], border_radius=10)
        screen.blit(button_board, (button["rect"].left, button["rect"].top))
        text_surface = font.render(button["label"], True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

def handle_menu(title, buttons):
    running = True
    choice = None
    hover_index = -1

    if title != "Select Mode":
        back_button = {"label": "Back", "rect": pygame.Rect(WIDTH/2 - 125, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT)}
        buttons = buttons + [back_button]
    
    while running:
        screen.blit(menu, (0, 0))
        title_text = title_font.render(title, True, (0, 0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 30))
        
        draw_buttons(buttons, hover_index)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEMOTION:
                hover_index = -1
                for i, button in enumerate(buttons):
                    if button["rect"].collidepoint(event.pos):
                        hover_index = i
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        choice = button["label"]
                        running = False
                        break
        
        pygame.display.flip()
    
    return choice

def draw_game(branches):
    #screen.fill(BACKGROUND_COLOR)  # Clear the screen
    screen.blit(sky, (0, 0))
    score = font.render(f"Moves: {moves_count}", True, (255,255,255))
    screen.blit(board, (WIDTH/2 - 140, 0))
    screen.blit(score, (495,90))
    screen.blit(hint, (WIDTH - 100, HEIGHT - 100))
    for branch in branches:
        if not(branch.completed):
            branch.update_color()
            screen.blit(branch.image, branch.rect)

            # Draw birds on top of branches
            for i, bird in enumerate(branch.birds):
                branch_width = branch.image.get_width()
                bird_x = branch.x - (branch_width // 2) + 65 + (i * 75) if branch.side == "left" else branch.x + (branch_width // 2) - 65 - (i * 75)
                bird_img = bird.image if branch.side == "left" else pygame.transform.flip(bird.image, True, False)
                bird_rect = bird.image.get_rect(midbottom=(bird_x, branch.y + 35))
                screen.blit(bird_img, bird_rect)
        #for branch in branches:
              ## pygame.draw.rect(screen, (255, 0, 0), branch.rect, 2)
    pygame.display.flip()  # Update display

while True:
    mode = handle_menu("Select Mode", mode_buttons)
    if mode is None:
        pygame.quit()
        exit()

    if mode in ["Easy", "Medium", "Hard", "Custom"]:
        while True:
            player = handle_menu("Select Player", player_buttons)
            if player == "Back":
                break  
            
            while True:
                search_algorithm = handle_menu("Select Algorithm", algorithm_buttons)
                if search_algorithm == "Back":
                    break 

                break

            if search_algorithm != "Back":
                break  

        if player != "Back" and search_algorithm != "Back":
            break 

if mode == "Easy":
    branches = loader.load_branches_from_file("../states/easy.txt")
elif mode == "Medium":
    branches = loader.load_branches_from_file("../states/medium.txt")
elif mode == "Hard":
    branches = loader.load_branches_from_file("../states/hard.txt")
elif mode == "Custom":
    branches = loader.load_branches_from_file("../states/custom.txt")
else:
    print("Invalid game state!")
    pygame.quit()

initial_state = GameState(branches)
solution_node = None

if search_algorithm == "Breadth-First Search":
    solution_node = breadth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "Depth-First Search":
    solution_node = depth_first_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "Iterative Deepening":
    solution_node = iterative_deepening_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states(), 20)
elif search_algorithm == "Uniform Cost":
    solution_node = uniform_cost_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "Greedy":
    solution_node = greedy_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "A*":
        solution_node = a_star_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "Weighted A*":
        solution_node = weighted_a_star_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())
elif search_algorithm == "Auto":
    if mode == "Easy":
        search_algorithm = "A*"
    elif mode == "Medium":
        search_algorithm = "A*"
    elif mode == "Hard":
        search_algorithm = "Greedy"
    elif mode == "Custom":
        search_algorithm = "Greedy"
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

# Draw the win screen
def handle_win_screen(moves_count):
    win_font = pygame.font.Font(None, 72)
    running = True
    hover_index = -1
    wood_color = (87, 75, 56)

    menu_button = {"label": "Menu", "rect": pygame.Rect(WIDTH/2 - 125, 400, BUTTON_WIDTH, BUTTON_HEIGHT)}
    exit_button = {"label": "Exit", "rect": pygame.Rect(WIDTH/2 - 125, 470, BUTTON_WIDTH, BUTTON_HEIGHT)}
    buttons = [menu_button, exit_button]

    while running:
        screen.blit(sky, (0, 0))
        screen.blit(board, (WIDTH/2 - 140, 0))

        move_text = font.render(f"Moves: {moves_count}", True, (255, 255, 255))
        move_rect = move_text.get_rect(center=(WIDTH // 2, 90))
        screen.blit(move_text, move_rect)

        title_text = win_font.render("YOU WIN!", True, wood_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 310))
        screen.blit(title_text, title_rect)

        draw_buttons(buttons, hover_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                hover_index = -1
                for i, button in enumerate(buttons):
                    if button["rect"].collidepoint(event.pos):
                        hover_index = i
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["label"] == "Menu":
                            return "menu"
                        elif button["label"] == "Exit":
                            pygame.quit()
                            exit()

        pygame.display.flip()



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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hint_rect.collidepoint(event.pos):   
                        branches = give_hint(search_algorithm, mode, GameState(branches))
                        break
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
                                action = handle_win_screen(moves_count)
                                if action == "menu":
                                    exec(open("main.py").read())  # Reexecuta o script
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
