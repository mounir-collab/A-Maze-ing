import random 
import os
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

    def has_wall(self, direction):
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





class Maze:

    def __init__(self, width, height):
        self.width = width
        self.height = height

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

        return result

    def unvisited_neighbors(self, cell):

        return [
            n for n in self.neighbors(cell)
            if not n.visited
        ]

    def generate(self):

        stack = []

        start = self.grid[0][0]
        # print(self.grid)
        start.visited = True

        stack.append(start)

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

    def display(self):

        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        os.system("clear")
        # top border
        print("█" * (self.width * 2 + 1))
        
        for y in range(self.height):

            line_top = "█"
            line_bottom = "█"

            for x in range(self.width):

                cell = self.grid[y][x]

                # mark Start / Exit
                if (x, y) == (entry_x, entry_y):
                    line_top += "S"
                elif (x, y) == (exit_x, exit_y):
                    line_top += "E"
                else:
                    line_top += " "

                # east wall
                if cell.has_wall(Cell.EAST):
                    line_top += "█"
                else:
                    line_top += " "

                # south wall
                if cell.has_wall(Cell.SOUTH):
                    line_bottom += "██"
                else:
                    line_bottom += " █"

            print(line_top)
            print(line_bottom)



# ████ 
# ████ 