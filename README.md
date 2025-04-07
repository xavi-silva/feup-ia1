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
# Interface

## Menu

When launching the game the level menu is displayed, allowing the user to select between the 6 available.

After that, the user must select if he wants to play or to watch a bot solve the level.

In case the user selected the bot mode, he will need to select a search algorithm for the bot to use. The availability of the search algorithm depends on the chosen level.

## Game

Inside the actual game, the user must click on a branch to select it as the origin branch, which will lighten its color, and select a destination branch to make the actual move. Clicking the same branch twice will unselect it. 

Three different buttons can be found in the interface to improve the user experience:
- **Hint button**: clicking this button will trigger a call to the **greedy_with_backtracking** algorithm and select the origin branch of the first move of the solution path; clicking it again will execute the move.

- **Save button**: saving the current game state is possible by clicking on this button; the game can be continued by selecting the **saved** option in the **level** menu.

- **Undo button**: performing a move adds the previous state to a state stack; clicking this button pops from that stack, going back to the most recent state.

- **Pause button**: the user can pause/resume the bot solution display whenever he want by clicking on this button.

# Problem Formulation

## State Representation

The state of our game is represented by a list of branches and each branch is a list of birds. 

## Initial State

There are currently 6 possible initial states that can be selected in the menu. This topic is explained with more detail in the [Game Levels](#game-levels) section.

## Objective Testing

- Checking branch completeness: **full_one_species** checks if a branch is full of birds of the same species

- Win checking: **check_win** function checks if every branch is either empty or full of birds of the same species

## Operator

There is only one operator in this game, which is the **move** function that receives an *origin branch* and a *destination branch*.

- Cost = 1 for every move
- Preconditions:
    - len(dest_branch) < branch_capacity
    - len(origin_branch) > 0
    - origin_branch.top = destination branch.top V len(dest_branch) = 0
- Effects:
    - specie = dest_branch.top ; n = min(destination_free_space, origin_same_species)
    - dest_branch.add(n) ; origin_branch.remove(specie, n)

# Project Structure

The project core folder **src** is divided in 7 different modules:

- **main.py** handles the game loop and its initialization logic, the menu and draws every screen of the game 
- **graph.py** defines both the *GameState* and the *TreeNode* classes, every search algorithm, the hint logic and its auxiliary function *move_done* that returns which move happened between two states
- **game_logic.py** is where we can find the operator *move_birds*, its auxiliary function *can_move_birds*, and the objective testing *check_win* and its auxiliary *remove_full_branches*
- **branch.py** defines the branch object and its associated functions, such as adding/removing birds, checking branch emptiness and goal testing, getting the top birds and evaluating it
- **bird.py** holds the definition of the bird object
- **loader.py** allows the loading of our game state by reading the state files
- **benchmark.py** was used for generating the time and memory measurements that are displayed in the *results* folder

In the remaining folders, we can find:
- all the images and icons used in the display in **assets**
- every used sound effect in the game in **sounds**
- the possible initial states in **states**
- the binary files for the paths of the algorithms for each level in **solutions**
- the data obtained by benchmark.py in **results**

# State Evaluation

Each state needs to get an associated value for informed search methods to work. In our particular case, we thought that the best way of properly evaluating a game state depended on two simple factors:

- Main factor: The **amount of completed branches**, since this is what the winning condition is all about - having all branches completed (100 points each)
- Secondary factor: The **number of birds placed after birds of the same color**, which is how we are able to reach completed branches - putting birds of the same color together (1 point each)

The value of a certain game state is the sum of values of every branch he has.

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

Our iterative deepening approach uses the function **depth_limited_search** algorithm with increasing depths, starting from depth = 1 up to depth = 10. 

This DLS uses the previously developed depth-first search algorithm with a slight difference - it keeps track of the current search and ends the search when it reaches the **max_depth**.

Despite successfuly finding a solution in small cases such as the **tutorial** level, it struggled in all the other levels, which proves it is much slower then the other algorithms.

## Uniform Cost

Although implemented, Uniform Cost Search was removed from the final game, as it behaved like BFS.

Since every move has an uniform cost of 1, expanding any child state always increased the total cost by 1. This means that all sibling nodes had the same cost, and uniform cost search could not prioritize any particular state more efficiently than BFS, resulting in the same behavior, with higher complexity.

## Greedy Search

**greedy_search** explores the node tree in its depth and selects the best option according to the **evaluate** function of the branches. 

The algorithm iterates over the possible next states and evaluates them. It stores the best value and the associated state and chooses it after trying every possible neighbour.

This algorithm provided fast and good solutions in every level except the **hard** one - in our game, sometimes the best move in a certain state can lead to an impossible path, which makes the simple greedy approach invalid.

## A* Algorithm
This algorithm tries to find the shortest path to a goal. It combines greedy search, which estimates the cost from a state **n** to the goal (**h(n)**), with the real cost from the start to the current state **n** (**g(n)**). To implement this algorithm we used a **priority queue** sorted by the evaluation function **f(n) = g(n) + h(n)**. This function estimates the total cost of the cheapest solution that passes through node **n**.

## Greedy with Backtracking
This algorithm is an adaptation of the A* search algorithm that relies only on the heuristic (**h(n)**), ignoring the actual cost **g(n)**. We noticed that the execution time was faster but it provides a worse solution than the A* algorithm

## Weighted A* 
This algorithm is another adaptation of A*, where we introduce a weight **W > 1** to the heuristic in the evaluation function: **f(n) = g(n) + W * h(n)**. We observed that increasing the value of **W** led to faster execution times, but worse solutions, as the algorithm begins to behave more like the Greedy with Backtracking version. Furthermore, for **W = 0**, the algorithm becomes uniform-cost search (only uses **g(n)**). For **W = 1**, we recover the standard A* search. To balance execution time and solution quality, we chose to use **W = 1.2**, which provided a good trade-off between speed and optimality in our experiments.

## Experimental results
All the conclusions we draw are supported by the following graphs:

# Game Levels
In order to provide different challenges to the user we implemented 4 game difficulties:

- Tutorial
- Easy
- Medium
- Hard

Besides that, the user can resume the level later through the **saved mode**, allowing them to continue from where they left off.

There is also a **custom mode** that allows hardcoding a game state:

- The first line of the file represents the capacity of the branches in the level and the following lines represent the actual branches.

- The lines before the empty line are the branches on the left of the screen, while the lines after the empty line are the branches on the right.

- Each number represents a different bird and having "-" on a line means there aren't any birds on it - it's an empty branch.

All game difficulties and modes are loaded from .txt files located in the **states** folder.

# Bot

We implemented a solver bot capable of solving the game levels using different search algorithms. The user can select which algorithm the bot uses from the available options for each difficulty level:

- Tutorial level: Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deepening, Greedy, Greedy Backtrack, A*, Weighted A*.
- Easy level: Depth-First Search (DFS), Greedy, Greedy Backtrack, A*, Weighted A*.
- Medium level: Depth-First Search (DFS), Greedy, Greedy Backtrack, A*, Weighted A*.
- Hard level: Depth-First Search (DFS), Greedy, Greedy Backtrack, A*, Weighted A*.

For **custom** and **saved mode** user can choose between:

- Depth-First Search (DFS), Greedy, Greedy Backtrack, A*, Weighted A*.

# Future work
- Save the stack of states to allow the user, when resuming the game from saved mode, to revert their moves if desired.
- Button to restart level
- More game levels
- Menu design
- Displaying next level when finishing one
- Perform more testing of the game to identify and fix any bugs

# Materials Used
- https://play.google.com/store/apps/details?id=com.globalplay.birdsort2.color.puzzle&hl=en - rules, graphics ideas, gameplay
- https://realpython.com/pygame-a-primer/ - setup pygame, game loop, draw images, user input
- https://www.youtube.com/watch?v=ySN5Wnu88nE&ab_channel=Computerphile - A* search
- Theoretical slides  

# Conclusion
This project gave us the opportunity to implement the search algorithms we learned in theoretical classes, applying them to a puzzle game.
Moreover, we understood the importance of choosing the right algorithm, as it requires balancing execution time and the proximity to the optimal solution.
Additionally, this experience helped us strengthen our problem-solving skills and gain a deeper understanding of how different algorithms behave in practice.  


Project developed by:  
- Paulo Coutinho, 202205692  
- Rui Xavier Silva, 202207183  
- Tomás Vinhas, 202208437  

Artificial Intelligence 24/25
