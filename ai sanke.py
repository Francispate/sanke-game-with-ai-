import tkinter
import random
import heapq

ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)
canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] #multiple snake tiles
game_over = False
score = 0
ai_mode = True  # Set to True to enable AI control
current_path = []  # Store the current path to food

# A* Algorithm helper functions
def heuristic(a, b):
    # Manhattan distance
    return abs(a.x - b.x) + abs(a.y - b.y)

def get_neighbors(node):
    # Get valid neighboring tiles
    neighbors = []
    for dx, dy in [(0, -TILE_SIZE), (TILE_SIZE, 0), (0, TILE_SIZE), (-TILE_SIZE, 0)]:  # Up, Right, Down, Left
        new_x = node.x + dx
        new_y = node.y + dy
        if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT:
            neighbors.append(Tile(new_x, new_y))
    return neighbors

def astar(start, goal, body):
    # Convert body to a set of (x, y) tuples for O(1) lookup
    body_positions = {(tile.x, tile.y) for tile in body}
    
    # Priority queue for A* algorithm
    frontier = []
    heapq.heappush(frontier, (0, start.x, start.y))
    
    # Dictionaries for tracking
    came_from = {}
    cost_so_far = {(start.x, start.y): 0}
    
    while frontier:
        _, current_x, current_y = heapq.heappop(frontier)
        current = Tile(current_x, current_y)
        
        if current.x == goal.x and current.y == goal.y:
            break
        
        for next_node in get_neighbors(current):
            # Skip if the neighbor is part of the snake's body
            if (next_node.x, next_node.y) in body_positions:
                continue
                
            new_cost = cost_so_far[(current.x, current.y)] + 1
            if (next_node.x, next_node.y) not in cost_so_far or new_cost < cost_so_far[(next_node.x, next_node.y)]:
                cost_so_far[(next_node.x, next_node.y)] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(frontier, (priority, next_node.x, next_node.y))
                came_from[(next_node.x, next_node.y)] = (current.x, current.y)
    
    # Reconstruct path
    path = []
    current = (goal.x, goal.y)
    
    # Check if there is a path
    if current not in came_from and (goal.x, goal.y) != (start.x, start.y):
        return []  # No path found
        
    while current != (start.x, start.y):
        if current not in came_from:
            break
        path.append(Tile(current[0], current[1]))
        current = came_from[current]
    
    path.reverse()
    return path

def find_safe_move():
    global snake, food, snake_body, velocityX, velocityY, current_path
    
    # Get head coordinates
    head_x = snake.x
    head_y = snake.y
    
    # Calculate new path if needed
    if not current_path or len(current_path) == 0:
        current_path = astar(snake, food, snake_body)
    
    # If no path found, try a safe move
    if not current_path:
        # Try all directions and pick the first safe one
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
            new_x = head_x + dx * TILE_SIZE
            new_y = head_y + dy * TILE_SIZE
            
            # Check if move is safe (not hitting wall or body)
            if (0 <= new_x < WINDOW_WIDTH and 
                0 <= new_y < WINDOW_HEIGHT and 
                not any(tile.x == new_x and tile.y == new_y for tile in snake_body)):
                return dx, dy
        
        # If no safe move is found, just continue in the current direction
        return velocityX, velocityY
    
    # Get the next step from the path
    next_step = current_path[0]
    current_path = current_path[1:]
    
    # Determine direction to next step
    dx = (next_step.x - head_x) // TILE_SIZE
    dy = (next_step.y - head_y) // TILE_SIZE
    
    return dx, dy

#game loop
def change_direction(e): #e = event
    global velocityX, velocityY, game_over, ai_mode
    
    if e.keysym == "a":
        ai_mode = not ai_mode
        print(f"AI mode: {'ON' if ai_mode else 'OFF'}")
        return
        
    if game_over:
        if e.keysym == "r":  # Press 'r' to restart
            restart_game()
        return
    
    if not ai_mode:  # Only allow manual control when AI is off
        if (e.keysym == "Up" and velocityY != 1):
            velocityX = 0
            velocityY = -1
            
        elif (e.keysym == "Down" and velocityY != -1):
            velocityX = 0
            velocityY = 1
        elif (e.keysym == "Left" and velocityX != 1):
            velocityX = -1
            velocityY = 0
        elif (e.keysym == "Right" and velocityX != -1):
            velocityX = 1
            velocityY = 0

def restart_game():
    global snake, food, velocityX, velocityY, snake_body, game_over, score, current_path
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0
    current_path = []

def move():
    global snake, food, snake_body, game_over, score, velocityX, velocityY, current_path
    
    if game_over:
        return
    
    # Use AI pathfinding if enabled
    if ai_mode and (velocityX == 0 and velocityY == 0 or True):
        velocityX, velocityY = find_safe_move()
    
    # Check for collisions with walls
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    # Check for collision with self
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    # Check for collision with food
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
        # Reset path after eating food
        current_path = []
    
    # Update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    # Move snake head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score, current_path
    
    move()
    canvas.delete("all")
    
    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')
    
    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')
    
    # Optionally draw the path (for debugging)
    if ai_mode and current_path:
        for tile in current_path:
            canvas.create_rectangle(tile.x + TILE_SIZE//4, tile.y + TILE_SIZE//4, 
                                   tile.x + 3*TILE_SIZE//4, tile.y + 3*TILE_SIZE//4, 
                                   fill='yellow', outline='')
    
    # Game over message
    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", 
                           text=f"Game Over: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30, font="Arial 12", 
                           text="Press 'r' to restart", fill="white")
    else:
        canvas.create_text(55, 20, font="Arial 10", 
                          text=f"Score: {score} | {'AI' if ai_mode else 'Manual'} Mode", fill="white")
        canvas.create_text(WINDOW_WIDTH//2, 20, font="Arial 10", 
                          text="Press 'a' to toggle AI mode", fill="white")
    
    # Schedule the next frame
    window.after(100, draw)

# Start the game loop
draw()

# Key bindings
window.bind("<KeyRelease>", change_direction)
window.mainloop()