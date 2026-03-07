from maze_gene.parsing import parse_config
from maze_gene.cell import Maze
import random

# ANSI color codes
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
RESET_COLOR = "\033[0m"

def show_maze_and_list(maze, color, config):
    # Display colored maze
    print(color, end="")
    maze.create_42_cell_indexs(config)
    maze.display()
    print(RESET_COLOR, end="")

    # Show internal grid as list
    print("\nMaze grid (internal representation):")
    # for row in maze.grid:
    #     print([cell.walls for cell in row])  # assuming each cell has .walls

def main():
    # Load config
    config = parse_config("config.txt")
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]

    # Seed if exists
    if "SEED" in config:
        random.seed(config["SEED"])

    # Initial maze
    maze = Maze(width, height)
    maze.entry = entry
    maze.exit = exit_
    maze.create_42_cell_indexs(config)
    maze.generate()
    current_color = random.choice(COLORS)

    # Show initial maze and list
    show_maze_and_list(maze, current_color, config)

    while True:
        print("\n=== Maze Menu ===")
        print("1: Generate new random maze")
        print("2: Display maze in random color")
        print("3: Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            maze = Maze(width, height)
            maze.entry = entry
            maze.exit = exit_
            maze.create_42_cell_indexs(config)
            maze.generate()
            print("New random maze generated!")
            show_maze_and_list(maze, current_color, config)

        elif choice == "2":
            current_color = random.choice(COLORS)
            print("Displaying maze in a new random color!")
            show_maze_and_list(maze, current_color, config)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()