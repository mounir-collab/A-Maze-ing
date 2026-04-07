import random
from typing import List, Tuple, Optional, Dict


class Cell:
    """
    Represents a single cell in the maze grid.
    Each cell stores its coordinates and a bitmask representing walls.
    """

    # bit masks for each direction
    NORTH: int = 1 << 0  # 0001
    EAST: int = 1 << 1  # 0010
    SOUTH: int = 1 << 2  # 0100
    WEST: int = 1 << 3  # 1000

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize a maze cell.

        Args:
            x: X coordinate in the grid.
            y: Y coordinate in the grid.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = self.NORTH | self.EAST | self.SOUTH | self.WEST
        self.visited: bool = False

    def has_wall(self, direction: int) -> bool:
        """
        Check if a wall exists in the given direction.

        Args:
            direction: Direction bitmask.

        Returns:
            True if the wall exists, otherwise False.
        """
        return (self.walls & direction) != 0

    def remove_wall(self, direction: int) -> None:
        """
        Remove a wall in the given direction.

        Args:
            direction: Direction bitmask.
        """
        self.walls &= ~direction

    def connect(self, other: "Cell") -> None:
        """
        Connect this cell to another by removing the wall between them.

        Args:
            other: Adjacent cell to connect with.
        """
        dx: int = other.x - self.x
        dy: int = other.y - self.y

        if dx == 1:  # east
            self.remove_wall(self.EAST)
            other.remove_wall(self.WEST)

        elif dx == -1:  # west
            self.remove_wall(self.WEST)
            other.remove_wall(self.EAST)

        elif dy == 1:  # south
            self.remove_wall(self.SOUTH)
            other.remove_wall(self.NORTH)

        elif dy == -1:  # north
            self.remove_wall(self.NORTH)
            other.remove_wall(self.SOUTH)

    def __repr__(self) -> str:
        """
        Debug representation of a cell.
        """
        return f"Cell({self.x},{self.y},walls={bin(self.walls)})"


class Maze:
    """
    Represents the maze grid and contains algorithms for maze generation.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """
        Initialize a maze.

        Args:
            width: Maze width.
            height: Maze height.
            seed: Optional random seed.
            perfect: Whether the maze should be perfect (no loops).
        """
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit_
        self.perfect: bool = perfect

        if seed is not None:
            random.seed(seed)

        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Return a cell at the given coordinates.
        """
        return self.grid[y][x]

    def neighbors(self, cell: Cell) -> List[Cell]:
        """
        Return all valid neighboring cells.

        Args:
            cell: Reference cell.

        Returns:
            List of adjacent cells inside the maze bounds.
        """
        directions: List[Tuple[int, int]] = [
            (0, -1),  # north
            (1, 0),  # east
            (0, 1),  # south
            (-1, 0),  # west
        ]

        result: List[Cell] = []

        for dx, dy in directions:
            nx: int = cell.x + dx
            ny: int = cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                result.append(self.grid[ny][nx])

        return result

    def unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """
        Return neighbors that have not been visited.
        """
        return [n for n in self.neighbors(cell) if not n.visited]

    def reachable_neighbors(self, cell: Cell) -> List[Cell]:
        """
        Return neighbors reachable without crossing walls.
        """
        result: List[Cell] = []

        if not cell.has_wall(Cell.NORTH) and cell.y > 0:
            result.append(self.grid[cell.y - 1][cell.x])

        if not cell.has_wall(Cell.EAST) and cell.x < self.width - 1:
            result.append(self.grid[cell.y][cell.x + 1])

        if not cell.has_wall(Cell.SOUTH) and cell.y < self.height - 1:
            result.append(self.grid[cell.y + 1][cell.x])

        if not cell.has_wall(Cell.WEST) and cell.x > 0:
            result.append(self.grid[cell.y][cell.x - 1])

        return result

    def generate_dfs(self) -> None:
        """
        Generate a maze using the Recursive Backtracker algorithm.
        """
        stack: List[Cell] = []

        start: Cell = self.grid[0][0]
        start.visited = True
        stack.append(start)

        while stack:
            current: Cell = stack[-1]
            neighbors: List[Cell] = self.unvisited_neighbors(current)

            if neighbors:
                next_cell: Cell = random.choice(neighbors)
                current.connect(next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.perfect:
            self.make_imperfect()

    def generate_prims(self) -> None:
        """
        Generate a maze using Randomized Prim's Algorithm.
        """
        start: Cell = self.grid[0][0]
        start.visited = True

        frontier: List[Tuple[Cell, Cell]] = []

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

    def make_imperfect(self, probability: float = 0.1) -> None:
        """
        Remove random walls to create loops without breaking special cells.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell: Cell = self.grid[y][x]

                if cell.walls == 15:
                    continue

                for neighbor in self.neighbors(cell):
                    if neighbor.x < cell.x or neighbor.y < cell.y:
                        continue

                    if random.random() < probability:
                        if neighbor.walls != 15:
                            cell.connect(neighbor)

    def create_42_cell_indexs(self, config: Dict[str, object]) -> None:
        """
        Mark a predefined pattern of cells as visited to form the '42' pattern.
        """
        center_x: int = (config["WIDTH"] // 2) - 3  # type: ignore
        center_y: int = (config["HEIGHT"] // 2) - 2  # type: ignore

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
            (center_y, center_x + 6),
            (center_y + 1, center_x + 6),
            (center_y + 2, center_x + 6),
            (center_y + 2, center_x + 5),
            (center_y + 2, center_x + 4),
            (center_y + 3, center_x + 4),
            (center_y + 4, center_x + 4),
            (center_y + 4, center_x + 5),
            (center_y + 4, center_x + 6),
        ]

        if config["WIDTH"] > 7 and config["HEIGHT"] > 5:  # type: ignore
            for y, x in config["pattern"]:  # type: ignore
                self.grid[y][x].visited = True
