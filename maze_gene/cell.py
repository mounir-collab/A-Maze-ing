import random 
import os
from collections import deque
class Cell:
    # bit masks for each direction
    NORTH = 1 << 0  # 0001
    EAST  = 1 << 1  # 0010
    SOUTH = 1 << 2  # 0100
    WEST  = 1 << 3  # 1000

    def __init__(self, x: int, y: int): # Each cell stores its position in the maze grid.
        self.x = x                      # example : (0,0) (1,0) (2,0)
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

    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height

        if seed is not None:
            random.seed(seed)

        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]
        


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
    def generate(self):
        """
        This function generates a random maze using the Recursive Backtracker algorithm
        """
        stack = []
        # print("start :")
        start = self.grid[0][0]
        # print(start)
        print("grid :")
        print(self.grid)
        start.visited = True

        stack.append(start)
        # print("stack :")
        # print(stack)
        while stack:

            current = stack[-1]

            neighbors = self.unvisited_neighbors(current)

            if neighbors:

                next_cell = random.choice(neighbors)

                current.connect(next_cell)

                next_cell.visited = True

                stack.append(next_cell)

            else:
                stack.pop()
        
        print("grid :")
        print(self.grid)
        # print(stack)

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

        for y, x in config["pattern"]:
            self.grid[y][x].visited = True

    def solve(self):

        start = self.grid[self.entry[1]][self.entry[0]]
        end = self.grid[self.exit[1]][self.exit[0]]

        queue = deque([start])
        visited = {start}
        parent = {}

        while queue:

            current = queue.popleft()

            if current == end:
                break

            for neighbor in self.reachable_neighbors(current):

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        # rebuild path
        path = []
        cell = end

        while cell != start:
            path.append(cell)
            cell = parent[cell]

        path.append(start)
        path.reverse()

        return path
    def display(self, path = None):

        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        os.system("clear")

        # convert path to coordinate set
        path_coords = set()
        if path:
            path_coords = {(cell.x, cell.y) for cell in path}

        # top border
        print("██" * (self.width * 2 + 1))
        for y in range(self.height):
            line_top = "██"
            line_bottom = "██"

            for x in range(self.width):

                cell = self.grid[y][x]

                # mark Start / Exit
                if (x, y) == (entry_x, entry_y):
                    line_top += "👽"
                elif (x, y) == (exit_x, exit_y):
                    line_top += "🛸"
                elif (x, y) in path_coords:
                    line_top += "🧶"
                elif (cell.walls == 15):
                    line_top += "⬜"
                else:
                    line_top += "  "

                # east wall
                if cell.has_wall(Cell.EAST):
                    line_top += "██"
                else:
                    line_top += "  "

                # south wall
                if cell.has_wall(Cell.SOUTH):
                    line_bottom += "████"
                else:
                    line_bottom += "  ██"

                
            print(line_top)
            print(line_bottom)
    
    def export_hex_maze_and_path(self, path, filename="maze.txt"):

        with open(filename, "w") as f:

        # ---- MAZE WALLS (hex) ----
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    cell = self.grid[y][x]
                    value = 0
                    if cell.has_wall(Cell.NORTH):
                        value |= 1
                    if cell.has_wall(Cell.EAST):
                        value |= 2
                    if cell.has_wall(Cell.SOUTH):
                        value |= 4
                    if cell.has_wall(Cell.WEST):
                        value |= 8
                    line += format(value, "X")
                f.write(line + "\n")

            # ---- PATH (as letters) ----
            directions = ""
            for i in range(len(path)-1):
                c = path[i]
                n = path[i+1]
                dx = n.x - c.x
                dy = n.y - c.y

                if dx == 1:
                    directions += "E"
                elif dx == -1:
                    directions += "O"
                elif dy == 1:
                    directions += "S"
                elif dy == -1:
                    directions += "N"

            f.write("\npath: " + directions + "\n")


# ████ 
# ████ 

# ██👽  


# my_maze = Maze(10 , 10)
# my_maze.generate()
# my_maze.display()