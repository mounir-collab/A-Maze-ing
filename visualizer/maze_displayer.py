import os
import time
from typing import Iterable, Optional, Tuple, Set, List
from mazegen.maze_gen import Maze, Cell


def display(
    maze: Maze,
    path: Optional[Iterable[Cell]] = None,
    animate: bool = False,
    delay: float = 0.2,
    color: str = "\033[97m",
) -> None:
    """
    Display the maze in the terminal.

    Optionally shows a path and can animate the path traversal.

    Args:
        maze: Maze instance containing the grid and dimensions.
        path: Optional iterable of cells representing a solution path.
        animate: If True, animate the path step-by-step.
        delay: Delay between animation frames in seconds.
        color: ANSI color code used for drawing the maze walls.

    Raises:
        ValueError: If entry or exit is placed in a blocked cell.
    """

    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit

    RESET: str = "\033[0m"

    # CHECK ENTRY / EXIT
    entry_cell: Cell = maze.grid[entry_y][entry_x]
    exit_cell: Cell = maze.grid[exit_y][exit_x]

    if entry_cell.walls == 15:
        raise ValueError("ENTRY is placed inside a blocked cell (42 pattern)")

    if exit_cell.walls == 15:
        raise ValueError("EXIT is placed inside a blocked cell (42 pattern)")

    path_coords: List[Tuple[int, int]] = []
    if path:
        path_coords = [(cell.x, cell.y) for cell in path]

    steps: List[Tuple[int, int]] = path_coords if animate and path else []
    animated_set: Set[Tuple[int, int]] = set()

    for step_index in range(len(steps) if animate else 1):
        os.system("clear")
        if animate:
            animated_set.add(steps[step_index])

        print(color + "██" * (maze.width * 2 + 1) + RESET)

        for y in range(maze.height):
            line_top: str = color + "██"
            line_bottom: str = color + "██"

            for x in range(maze.width):
                cell: Cell = maze.grid[y][x]
                current_path: Set[Tuple[int, int]] = (
                    animated_set if animate else set(path_coords)
                )

                if (x, y) == (entry_x, entry_y):
                    line_top += "👽"
                elif (x, y) == (exit_x, exit_y):
                    line_top += "🌍"
                elif (x, y) in current_path:
                    line_top += "🛸"
                elif cell.walls == 15:
                    line_top += "⬜"
                else:
                    line_top += "  "

                if cell.has_wall(Cell.EAST):
                    line_top += color + "██"
                else:
                    line_top += "  "

                if cell.has_wall(Cell.SOUTH):
                    line_bottom += color + "████"
                else:
                    line_bottom += "  ██"

            print(line_top + RESET)
            print(line_bottom + RESET)

        if animate:
            time.sleep(delay)
