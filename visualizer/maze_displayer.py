import os
import time
from maze_gene.maze_gen import Cell

def display(maze, path=None, animate=False, delay= 0.2, color="\033[97m"):
    entry_x, entry_y = maze.entry #( 0 , 0)
    exit_x, exit_y = maze.exit #(19 , 19)

    RESET = "\033[0m"

    path_coords = []
    if path:
        path_coords = [(cell.x, cell.y) for cell in path]

    steps = path_coords if animate and path else []
    animated_set = set()

    for step_index in range(len(steps) if animate else 1):
        # os.system("clear")

        if animate:
            animated_set.add(steps[step_index])

        print(color + "██" * (maze.width * 2 + 1) + RESET)

        for y in range(maze.height):
            line_top = color + "██"
            line_bottom = color + "██"

            for x in range(maze.width):
                cell = maze.grid[y][x]
                current_path = animated_set if animate else set(path_coords)

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