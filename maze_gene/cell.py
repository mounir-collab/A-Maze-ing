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


c1 = Cell(0, 0)
c2 = Cell(1, 0)

c1.connect(c2)

print(bin(c1.walls))

print(bin(c2.walls))


# ████ 
# ████ 