
from collections import deque
import random

class Cell:
    # bit masks for each direction
    NORTH = 1 << 0  # 0001
    EAST  = 1 << 1  # 0010
    SOUTH = 1 << 2  # 0100
    WEST  = 1 << 3  # 1000

    def __init__(self, x: int, y: int): # Each cell stores its position in the maze grid.
        self.x = x                     # example : (0,0) (1,0) (2,0)
        self.y = y
        self.walls = self.NORTH | self.EAST | self.SOUTH | self.WEST # | is the bitwise OR operator.
        self.visited = False

    def has_wall(self, direction) -> bool:
        return (self.walls & direction) != 0

    def remove_wall(self, direction):
        self.walls &= ~direction

    def connect(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        if dx == 1:  # other is east
            self.remove_wall(self.EAST)
            other.remove_wall(self.WEST)

        elif dx == -1:  # other is west
            self.remove_wall(self.WEST)
            other.remove_wall(self.EAST)

        elif dy == 1:  # other is south
            self.remove_wall(self.SOUTH)
            other.remove_wall(self.NORTH)

        elif dy == -1:  # other is north
            self.remove_wall(self.NORTH)
            other.remove_wall(self.SOUTH)

    def __repr__(self):
        return f"Cell({self.x},{self.y},walls={bin(self.walls)})"

# ce = Cell(1 , 2)
# print(ce)



class Maze:

    def __init__(self, width, height ,seed=None , perfect: bool = True):
        self.width = width
        self.height = height
        self.perfect = perfect

        if seed is not None:
            random.seed(seed)

        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]
        # print(self.grid)


    def get_cell(self, x, y):
        return self.grid[y][x]

    def neighbors(self, cell):

        directions = [
            (0, -1),  # north
            (1, 0),   # east
            (0, 1),   # south
            (-1, 0)   # west
        ]

        result = []

        for dx, dy in directions:

            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                result.append(self.grid[ny][nx])
            # print("neighbours : ")
            # print(result)
        return result

    def unvisited_neighbors(self, cell):

        return [
            n for n in self.neighbors(cell)
            if not n.visited
        ]
    def reachable_neighbors(self, cell):

        result = []

        # north
        if not cell.has_wall(Cell.NORTH) and cell.y > 0:
            result.append(self.grid[cell.y - 1][cell.x])

        # east
        if not cell.has_wall(Cell.EAST) and cell.x < self.width - 1:
            result.append(self.grid[cell.y][cell.x + 1])

        # south
        if not cell.has_wall(Cell.SOUTH) and cell.y < self.height - 1:
            result.append(self.grid[cell.y + 1][cell.x])

        # west
        if not cell.has_wall(Cell.WEST) and cell.x > 0:
            result.append(self.grid[cell.y][cell.x - 1])

        return result
    
    def generate_dfs(self):
        """
        This function generates a random maze using the Recursive Backtracker algorithm
        """
        stack = []
        # print("start :")
        start = self.grid[0][0]
        # print(start)
        # print("grid :")
        # print(self.grid)
        start.visited = True

        stack.append(start)
        # print("stack :")
        # print(stack)
    
        while stack:

            current = stack[-1] # [ (0  , 0)  , (0 , 1)]

            neighbors = self.unvisited_neighbors(current)

            if neighbors:

                next_cell = random.choice(neighbors)

                current.connect(next_cell)

                next_cell.visited = True

                stack.append(next_cell)

            else:
                stack.pop()
        
        if  not self.perfect:
            self.make_imperfect()
        
        # print("grid :")
        # print(self.grid)
        # print(stack)

    def generate_prims(self):
        """
        Generate a maze using Randomized Prim's Algorithm
        """
        start = self.grid[0][0]
        start.visited = True

        frontier = []

        # add neighbors of start to frontier
        for n in self.neighbors(start):
            frontier.append((start, n))

        while frontier:

            current, next_cell = random.choice(frontier)
            frontier.remove((current, next_cell))

            if not next_cell.visited:

                current.connect(next_cell)
                next_cell.visited = True

                for n in self.neighbors(next_cell):
                    if not n.visited:
                        frontier.append((next_cell, n))
        if not self.perfect:
            self.make_imperfect()
    

    def make_imperfect(self, probability=0.1):
        """
        Remove random walls to create loops without breaking special cells.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                # skip “special” 42-pattern cells
                if cell.walls == 15:  # all walls intact
                    continue

                for neighbor in self.neighbors(cell):
                    # avoid processing the same pair twice
                    if neighbor.x < cell.x or neighbor.y < cell.y:
                        continue

                    if random.random() < probability:
                        # only connect if it doesn’t involve a full-wall cell
                        if neighbor.walls != 15:
                            cell.connect(neighbor)
    
    def create_42_cell_indexs(self, config):
        center_x = (config["WIDTH"] // 2) - 3
        center_y = (config["HEIGHT"] // 2) - 2

        config["pattern"] = [
            (center_y, center_x),
            (center_y + 1, center_x),
            (center_y + 2, center_x),
            (center_y + 2, center_x + 1),
            (center_y + 2, center_x + 2),
            (center_y + 1, center_x + 2),
            (center_y + 3, center_x + 2),
            (center_y + 4, center_x + 2),
            (center_y, center_x + 2),
            (center_y + 2, center_x + 2),
            (center_y, center_x + 4),
            (center_y, center_x + 5),
            (center_y , center_x + 6),
            (center_y + 1, center_x + 6),
            (center_y + 2, center_x + 6),
            (center_y + 2, center_x + 5),
            (center_y + 2, center_x + 4),
            (center_y + 3, center_x + 4),
            (center_y + 4, center_x + 4),
            (center_y + 4, center_x + 5),
            (center_y + 4, center_x + 6),
        ]
        if config['WIDTH'] > 7 and config['HEIGHT'] > 5:
            for y, x in config["pattern"]:
                self.grid[y][x].visited = True



# ████ 
# ████ 

# ██👽  


# my_maze = Maze(10 , 10)
# my_maze.generate()
# my_maze.display()

