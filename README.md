AI Snake Game
A classic Snake game enhanced with artificial intelligence that automatically navigates the snake to food using the A* pathfinding algorithm.


🎮 Overview
This project implements the classic Snake game with an AI twist. The snake can be controlled manually using arrow keys or automatically using an A* pathfinding algorithm that calculates the optimal path to the food while avoiding obstacles.
✨ Features

A Pathfinding Algorithm*: The snake intelligently finds the shortest path to food
Dual Control Modes: Toggle between AI and manual control by pressing 'a'
Path Visualization: Yellow squares show the planned path (when in AI mode)
Game Restart: Press 'r' after game over to play again
Score Tracking: Monitor your progress with an in-game score counter

🚀 How to Run

Ensure you have Python installed (Python 3.6+ recommended)
Install the tkinter library if not already installed:

It comes pre-installed with most Python distributions
If needed: pip install tk or apt-get install python3-tk (Linux)


Download snake_game.py
Run the game:
Copypython snake_game.py


🎯 How to Play

Starting the game: The game begins with the snake stationary. Press any arrow key to start moving in manual mode, or toggle AI mode with 'a'.
Manual Controls:

↑ (Up Arrow): Move up
↓ (Down Arrow): Move down
← (Left Arrow): Move left
→ (Right Arrow): Move right


AI Mode:

Press 'a' to toggle AI mode ON/OFF
Watch as the snake automatically navigates to food


Restart:

Press 'r' after game over to restart



🧠 Understanding the AI Algorithm
The game uses the A* (A-star) pathfinding algorithm, which:

Calculates the optimal path from the snake's head to food
Avoids collisions with the snake's body and walls
Uses Manhattan distance as a heuristic to estimate distance to food
Recalculates the path each time the snake moves or eats food

If no valid path exists, the AI makes the safest possible move to avoid immediate collisions.
🔧 Code Structure
For beginners and those interested in understanding the code:

Tile Class: Represents positions on the game grid
Game Setup: Creates the window and initializes game variables
A Algorithm*: Implemented with the following key functions:

heuristic(): Calculates Manhattan distance between points
get_neighbors(): Finds valid adjacent tiles
astar(): Core pathfinding algorithm
find_safe_move(): Determines the next move for the snake


Game Loop: Handles drawing, movement, and collision detection

🛠️ Customization
You can modify these variables at the top of the file to customize the game:
pythonCopyROWS = 25         # Number of grid rows
COLS = 25         # Number of grid columns  
TILE_SIZE = 25    # Size of each tile in pixels
🔍 For Advanced Users
Interested in extending the game? Here are some ideas:

Implement different pathfinding algorithms (Dijkstra's, BFS) for comparison
Add difficulty levels by adjusting the game speed
Create obstacles on the game board
Implement a smarter AI that plans ahead to avoid trapping itself
Add a two-player mode where one snake is AI-controlled and another is manual

📝 Notes for Developers

The A* implementation uses a priority queue via Python's heapq module
The snake's body is tracked as a list of Tile objects
We calculate the path to food each time the food is eaten or when there's no current path
The AI visualization can be disabled by removing/commenting the code section that draws yellow squares

🤝 Contributing
Feel free to fork this repository and submit pull requests to enhance the game. Some ideas for contributions:

Add sound effects
Implement high score tracking
Create multiple food items
Add obstacles or walls

📃 License
This project is open source and available under the MIT License.

Created with ❤️ by Francis pate 
