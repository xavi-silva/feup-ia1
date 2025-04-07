# Game Definition

- **Bird Sort** is a single player puzzle game played on a pre-generated board
- The goal is to sort birds by type in different branches 
- The game ends when all the birds have flows away (puzzle solved)


# Setup

**Download the Project**

1. Download the ZIP of this project from GitHub
2. Extract the ZIP to a folder on your computer
3. Open that folder in your terminal or file explorer

## One-Click Setup (Windows Only)

Just double-click the **setup.bat** file in the project folder.

It will:
- Check if Python is installed
- Install dependencies
- Run the game from the correct folder

**Note:** This only works if **Python and pip are already installed and available in your system PATH**.  

If you prefer installing manually, check the next section

## Manual Setup

1. **Install Python**

Download and install from: https://www.python.org/downloads/ <br>
Version **3.9 to 3.12** recommended

2. **Install dependencies**

Run the following command in the **project root folder** (where `requirements.txt` is):

```bash
pip install -r requirements.txt
```

This installs **Pygame**

**Recommended** Pygame version : **2.6.1**

3. **Run the game**

Navigate to the **src** folder and launch the game:

```bash
cd src
python main.py
```

# Search Methods

The function **check_win(branches)** is used as the goal condition in all search algorithms. It iterates through all the branches and return **True** if every branch is either empty or completed, with birds of the same type.

The method **state.generate_child_states()** is also used by every search strategy to generate all valid next states based on possible bird movements.

## Breadth-first Search

It uses a **queue** to store states, ensuring that the shallowest solutions are explored first. 
When generating the child states, adds them to the queue if they haven't been visited yet.

This method guarantees the shortest solution (in number of moves), but is inefficient for complex levels due to memory and time constraints.

In our project, BFS was only able to resolve the tutorial level before becoming impractical.

## Depth-first Search

We used a recursive helper function **dfs_recursive** , which explores as deep as possible along each path before backtracking.

A visited set keeps track of already visited states to avoid infinite loops. 

DFS successfully found solutions in all levels, but in harder levels the solution path was very long. This confirms that DFS can find a solution, but it does not guarantee the shortest one.

## Iterative Deepening

## Uniform Cost

Although implemented, Uniform Cost Search was removed from the final game, as it behaved like BFS.

Since every move has an uniform cost of 1, expanding any child state always increased the total cost by 1. This means that all sibling nodes had the same cost, and uniform cost search could not prioritize any particular state more efficiently than BFS, resulting in the same behavior, with higher complexity.

## Greedy Search

## Greedy with Backtracking

## A* Algorithm

## Weighted A* 