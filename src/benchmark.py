import os, time, tracemalloc
from graph import depth_first_search, GameState
import game_logic, loader

# Garantir pasta de resultados
os.makedirs("../results", exist_ok=True)

# Carregar estado inicial do nível easy
branches = loader.load_branches_from_file("../states/easy.txt")
initial_state = GameState(branches)

# Conjunto para guardar estados únicos visitados (sem o inicial)
visited_states = set()

def generate_child_tracking(state):
    children = state.generate_child_states()
    for child in children:
        if child not in visited_states:
            visited_states.add(child)
    return children

# Medição de tempo e memória
tracemalloc.start()
start = time.time()

solution_node = depth_first_search(
    initial_state,
    game_logic.check_win,
    generate_child_tracking
)

end = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Reconstruir caminho
path = []
if solution_node:
    while solution_node:
        path.append(solution_node.state)
        solution_node = solution_node.parent
    path.reverse()

# Guardar resultados
with open("../results/easy.txt", "a") as f:
    f.write("Depth-First Search Results:\n")
    if path:
        f.write(f"- Time: {end - start:.3f} seconds\n")
        f.write(f"- Moves: {len(path) - 1}\n")
        f.write(f"- Unique States Visited: {len(visited_states)}\n")
        f.write(f"- Peak Memory: {peak / 1024:.1f} KB\n\n")
    else:
        f.write("- No solution found.\n\n")
