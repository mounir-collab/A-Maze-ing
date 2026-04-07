from typing import List
from maze_gene.maze_gen import Maze, Cell


def export_hex_maze_and_path(maze: Maze,
                             path: List[Cell],
                             filename: str) -> None:
    with open(filename, "w") as f:
        # ---- MAZE WALLS (hex) ----
        for y in range(maze.height):
            line = ""
            for x in range(maze.width):
                cell: Cell = maze.grid[y][x]

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
        for i in range(len(path) - 1):
            c: Cell = path[i]
            n: Cell = path[i + 1]

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
