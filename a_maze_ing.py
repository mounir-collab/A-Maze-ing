import sys
import random
from maze_gene.parsing import parse_config
from maze_gene.cell import Maze

# ANSI color codes
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
RESET_COLOR = "\033[0m"


def show_maze_and_list(maze, color, config):
    print(color, end="")

    # maze.create_42_cell_indexs(config)

    # path = maze.solve()   # compute the path

    maze.display()

    print(RESET_COLOR, end="")


def main():

    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    # Load config
    config = parse_config(config_file)

    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]

    # Seed if exists
    if "SEED" in config:
        random.seed(config["SEED"])
    
    my_seed = config.get("SEED")

    # Initial maze
    maze = Maze(width, height , my_seed)
    maze.entry = entry
    maze.exit = exit_

    
    maze.create_42_cell_indexs(config)
    maze.generate()
    
    current_color = COLORS[0]

    show_maze_and_list(maze, current_color, config)
    i = 1
    while True:
        try:
            print("\n=== Maze Menu ===")
            print("1: Generate new random maze")
            print("2: Display maze in random color")
            print("3: Solve maze")
            print("4: Exit")

            choice = input("Choose an option: ")

        except (KeyboardInterrupt, Exception):
            print("\nProgram interrupted. Exiting...")
            break

        if choice == "1":
            maze = Maze(width, height , my_seed)
            maze.entry = entry
            maze.exit = exit_

            maze.create_42_cell_indexs(config)
            maze.generate()
            

            print("New random maze generated!")
            show_maze_and_list(maze, current_color, config)

        elif choice == "2":

            current_color = COLORS[i % len(COLORS)]
            i += 1

            print("Displaying maze in a new random color!")
            show_maze_and_list(maze, current_color, config)
        
        elif choice == "3":

            path = maze.solve()
            maze.export_hex_maze_and_path(path, "maze.txt")
            
            print("Maze solved!")

            print(current_color, end="")
            maze.display(path)
            print(RESET_COLOR, end="")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()