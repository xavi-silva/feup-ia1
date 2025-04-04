import pygame
import random
import game_logic
from graph import give_hint, GameState, move_done, greedy_with_backtracking, weighted_a_star_search
from collections import deque
from bird import Bird
from branch import Branch
import loader
import pickle


# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 1200, 680
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 50
BACKGROUND_COLOR = (135, 206, 250)  # Sky Blue
FPS = 60
undo_stack = []

# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sorter")
sky = pygame.image.load("../assets/sky.png")
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))
board = pygame.image.load("../assets/board.png")
button_board = pygame.image.load("../assets/button.png")
button_board = pygame.transform.scale(button_board, (250, 50))
menu = pygame.image.load("../assets/menu.gif")
menu = pygame.transform.scale(menu, (WIDTH, HEIGHT))

# Interface
pause = pygame.image.load("../assets/pause.png")
pause = pygame.transform.scale(pause, (75, 75))

hint = pygame.image.load("../assets/hint.png")
hint = pygame.transform.scale(hint, (75, 75))
pause_hint_rect = pygame.Rect(WIDTH - 75, HEIGHT - 75, 75, 75) 

undo_img = pygame.image.load("../assets/undo_move.png")
undo_img = pygame.transform.scale(undo_img, (75, 75))
undo_rect = pygame.Rect(20, HEIGHT - 75, 75, 75)

save = pygame.image.load("../assets/download.png")
save = pygame.transform.scale(save, (75, 75))
save_rect = pygame.Rect(WIDTH - 150, HEIGHT - 75, 75, 75) 

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Menu Buttons
mode_buttons = [
    {"label": "Tutorial", "rect": pygame.Rect(WIDTH/2 - 125, 100, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Easy", "rect": pygame.Rect(WIDTH/2 - 125, 160, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Medium", "rect": pygame.Rect(WIDTH/2 - 125, 220, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Hard", "rect": pygame.Rect(WIDTH/2 - 125, 280, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Custom", "rect": pygame.Rect(WIDTH/2 - 125, 340, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Saved", "rect": pygame.Rect(WIDTH/2 - 125, 400, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

algorithm_buttons = [
    {"label": "Breadth-First Search", "rect": pygame.Rect(WIDTH/2 - 125, 150, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Depth-First Search", "rect": pygame.Rect(WIDTH/2 - 125, 200, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Iterative Deepening", "rect": pygame.Rect(WIDTH/2 - 125, 250, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Greedy", "rect": pygame.Rect(WIDTH/2 - 125, 300, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Backtrack Greedy", "rect": pygame.Rect(WIDTH/2 - 125, 350, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "A*", "rect": pygame.Rect(WIDTH/2 - 125, 400, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Weighted A*", "rect": pygame.Rect(WIDTH/2 - 125, 450, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

player_buttons = [
    {"label": "You", "rect": pygame.Rect(WIDTH/2 - 125, 150, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"label": "Bot", "rect": pygame.Rect(WIDTH/2 - 125, 220, BUTTON_WIDTH, BUTTON_HEIGHT)}
]

menu_button = {
    "label": "Menu",
    "rect": pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 85, BUTTON_WIDTH, BUTTON_HEIGHT)
}

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

def draw_game(branches):
    #screen.fill(BACKGROUND_COLOR)  # Clear the screen
    screen.blit(sky, (0, 0))
    score = font.render(f"Moves: {moves_count}", True, (255,255,255))
    screen.blit(board, (WIDTH/2 - 140, 0))
    screen.blit(score, (495,90))
    screen.blit(save, (WIDTH - 150, HEIGHT - 75))

    # Button going back to menu
    hovering = menu_button["rect"].collidepoint(pygame.mouse.get_pos())
    color = (0, 0, 0) if hovering else (196, 164, 132)
    pygame.draw.rect(screen, (0, 0, 0), menu_button["rect"], border_radius=10)
    pygame.draw.rect(screen, color, menu_button["rect"], border_radius=10)
    screen.blit(button_board, (menu_button["rect"].left, menu_button["rect"].top))
    text_surface = font.render(menu_button["label"], True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=menu_button["rect"].center)
    screen.blit(text_surface, text_rect)
    
    if player == "You":
        screen.blit(undo_img, (undo_rect.x, undo_rect.y))
        screen.blit(hint, (WIDTH - 75, HEIGHT - 75))
    elif player == "Bot":
        screen.blit(pause, (WIDTH - 75, HEIGHT - 75))
    for branch in branches:
        if not(branch.completed):
            branch.update_color()
            screen.blit(branch.image, branch.rect)

            # Draw birds on top of branches
            branch_width = branch.image.get_width()
            num_slots = Branch.branch_size
            usable_width = branch_width - 2 * 65
            spacing = usable_width / max(num_slots - 1, 1)

            for i, bird in enumerate(branch.birds):
                if branch.side == "left":
                    bird_x = branch.x - (branch_width // 2) + 65 + (i * spacing)
                else:
                    bird_x = branch.x + (branch_width // 2) - 65 - (i * spacing)

                bird_img = bird.image if branch.side == "left" else pygame.transform.flip(bird.image, True, False)
                bird_rect = bird.image.get_rect(midbottom=(bird_x, branch.y + 18))
                screen.blit(bird_img, bird_rect)

        #for branch in branches:
            #pygame.draw.rect(screen, (255, 0, 0), branch.rect, 2)
    pygame.display.flip()  # Update display

def write_moves_to_file(path, filename):
    with open(filename, "wb") as file:
        moves = []
        for i in range(len(path) - 1):
            o, d = move_done(path[i], path[i + 1])  # Get the move
            moves.append((o, d))
        pickle.dump(moves, file)  # Save moves as a binary file
    print(f"Moves saved")

def read_moves_from_file(filename):
    """Reads move indices from a file and returns them as a list."""
    try:
        with open(filename, "rb") as file:
            moves = pickle.load(file)  # Load move data
        print(f"✅ Moves loaded from {filename}: {moves}")
        return moves
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []

player = None

while True:
    mode = handle_menu("Select Mode", mode_buttons)
    if mode is None:
        pygame.quit()
        exit()

    if mode in ["Tutorial", "Easy", "Medium", "Hard", "Custom", "Saved"]:
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

if mode == "Tutorial":
    branches = loader.load_branches_from_file("../states/tutorial.txt")
elif mode == "Easy":
    branches = loader.load_branches_from_file("../states/easy.txt")
elif mode == "Medium":
    branches = loader.load_branches_from_file("../states/medium.txt")
elif mode == "Hard":
    branches = loader.load_branches_from_file("../states/hard.txt")
elif mode == "Custom":
    branches = loader.load_branches_from_file("../states/custom.txt")
elif mode == "Saved":
    branches = loader.load_branches_from_file("../states/saved.txt")
else:
    print("Invalid game state!")
    pygame.quit()

"""
initial_state = GameState(branches)
path = []
solution_node = weighted_a_star_search(initial_state, game_logic.check_win, lambda state: state.generate_child_states())

if solution_node:
    print("Solution Found!\n")
    while solution_node:
        path.append(solution_node.state)
        solution_node = solution_node.parent

    path.reverse()
else:
    print("No solution found.")


file = "../solutions/hard/weighted_a_star.txt"
write_moves_to_file(path, file)

moves = []
"""

if mode == "Tutorial":
    if search_algorithm == "Bread-First Search":
        moves = read_moves_from_file("../solutions/tutorial/bfs.txt")
    elif search_algorithm == "Depth-First Search":
        moves = read_moves_from_file("../solutions/tutorial/dfs.txt")
    elif search_algorithm == "Iterative Deepening":
        moves = read_moves_from_file("../solutions/tutorial/iterative_deepening.txt")
    elif search_algorithm == "A*":
        moves = read_moves_from_file("../solutions/tutorial/a_star.txt")
    elif search_algorithm == "Weighted A*":
        moves = read_moves_from_file("../solutions/tutorial/weighted_a_star.txt")
    elif search_algorithm == "Greedy":
        moves = read_moves_from_file("../solutions/tutorial/greedy.txt")
    elif search_algorithm == "Greedy Backtrack":
        moves = read_moves_from_file("../solutions/tutorial/greedy_backtrack.txt")

elif mode == "Easy":
    if search_algorithm == "Bread-First Search":
        moves = read_moves_from_file("../solutions/easy/bfs.txt")
    elif search_algorithm == "Depth-First Search":
        moves = read_moves_from_file("../solutions/easy/dfs.txt")
    elif search_algorithm == "Iterative Deepening":
        moves = read_moves_from_file("../solutions/easy/iterative_deepening.txt")
    elif search_algorithm == "A*":
        moves = read_moves_from_file("../solutions/easy/a_star.txt")
    elif search_algorithm == "Weighted A*":
        moves = read_moves_from_file("../solutions/easy/weighted_a_star.txt")
    elif search_algorithm == "Greedy":
        moves = read_moves_from_file("../solutions/easy/greedy.txt")
    elif search_algorithm == "Greedy Backtrack":
        moves = read_moves_from_file("../solutions/easy/greedy_backtrack.txt")

elif mode == "Medium":
    if search_algorithm == "Depth-First Search":
        moves = read_moves_from_file("../solutions/medium/dfs.txt")
    elif search_algorithm == "A*":
        moves = read_moves_from_file("../solutions/medium/a_star.txt")
    elif search_algorithm == "Weighted A*":
        moves = read_moves_from_file("../solutions/medium/weighted_a_star.txt")
    elif search_algorithm == "Greedy":
        moves = read_moves_from_file("../solutions/medium/greedy.txt")
    elif search_algorithm == "Greedy Backtrack":
        moves = read_moves_from_file("../solutions/medium/greedy_backtrack.txt")

elif mode == "Hard":
    if search_algorithm == "Depth-First Search":
        moves = read_moves_from_file("../solutions/hard/dfs.txt")
    elif search_algorithm == "A*":
        moves = read_moves_from_file("../solutions/hard/a_star.txt")
    elif search_algorithm == "Weighted A*":
        moves = read_moves_from_file("../solutions/hard/weighted_a_star.txt")
    elif search_algorithm == "Greedy":
        moves = read_moves_from_file("../solutions/hard/greedy.txt")
    elif search_algorithm == "Greedy Backtrack":
        moves = read_moves_from_file("../solutions/hard/greedy_backtrack.txt")

# Game Loop
selected_branch = None
move_mode = False
moves_count = 0
font = pygame.font.Font(None, 36)
draw_game(branches)
pygame.time.delay(2000)
running = True

# Music
pygame.mixer.music.load("../sounds/background.mp3")
pygame.mixer.music.set_volume(0.05)  
pygame.mixer.music.play(-1)  
bird_sound = pygame.mixer.Sound("../sounds/bird.wav")
bird_sound.set_volume(0.05)  
move_sound = pygame.mixer.Sound("../sounds/wings.wav")
move_sound.set_volume(0.2)  
branch_sound = pygame.mixer.Sound("../sounds/leaves.wav")
branch_sound.set_volume(0.2) 

clock = pygame.time.Clock()
selected_bird = None

i = 0
BOT_MOVE_EVENT = pygame.USEREVENT + 1  
pygame.time.set_timer(BOT_MOVE_EVENT, 500)  # Trigger every 500ms
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == BOT_MOVE_EVENT and player == "Bot":
            if not paused:
                if i < len(moves) - 1:
                    origin, destination = moves[i]
                    i += 1
                    if game_logic.move_birds(branches[origin], branches[destination]):
                        moves_count += 1
                else:
                    print("You Win!")
                    action = handle_win_screen(moves_count)
                    if action == "menu":
                        exec(open("main.py").read())
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player=="Bot" and pause_hint_rect.collidepoint(event.pos):
                paused = not paused
            elif player=="You" and pause_hint_rect.collidepoint(event.pos):   
                (origin, destination) = give_hint(GameState(branches))
                if origin == 0 and destination == 0 and undo_stack:
                    branches = undo_stack.pop()
                    moves_count += 1
                elif selected_branch and selected_branch == branches[origin]:
                    game_logic.move_birds(branches[origin], branches[destination])
                    moves_count += 1
                    move_sound.play()
                    selected_branch.selected = False
                    selected_branch.update_color()
                    selected_branch = None
                    move_mode = False         
                else:
                    if selected_branch:
                        selected_branch.selected = False
                        selected_branch.update_color()
                        selected_branch = None
                        move_mode = False                           
                    selected_branch = branches[origin]
                    bird_sound.play()
                    selected_branch.selected = True
                    selected_branch.update_color()
                    move_mode = True
            elif player == "You" and undo_rect.collidepoint(event.pos) and undo_stack:
                branches = undo_stack.pop()
                moves_count += 1
            elif save_rect.collidepoint(event.pos):
                GameState(branches).save_branches_to_file()  
                print("Saving...")    
            elif menu_button["rect"].collidepoint(event.pos):
                print("Menu button clicked")
                exec(open("main.py").read()) 
                running = False
            else:
                for branch in branches:
                    if player == "You" and branch.rect.collidepoint(event.pos):
                        if not move_mode and len(branch.birds)!=0:
                            #if selected_branch:
                                #selected_branch.selected = False
                                #selected_branch.update_color()
                            selected_branch = branch
                            bird_sound.play()
                            selected_branch.selected = True
                            selected_branch.update_color()

                            move_mode = True
                        else:
                            if selected_branch and selected_branch != branch and not branch.completed:
                                if game_logic.can_move_birds(selected_branch, branch):
                                    undo_stack.append(Branch.clone_all_branches(branches, loader.BRANCH_IMAGE))
                                    if game_logic.move_birds(selected_branch, branch):
                                        moves_count += 1
                                        move_sound.play()
                                        pygame.time.delay(500)

                                        if branch.full_one_species():
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
    #print("flips")
    clock.tick(FPS)

pygame.quit()
