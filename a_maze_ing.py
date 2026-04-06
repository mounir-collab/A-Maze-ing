import sys
import random
import os
from parsing import parse_config
from maze_gene.maze_gen import Maze



# ANSI color codes
COLORS = ["\x1b[46m", "\x1b[38;5;154m", "\033[93m", "\x1b[38;5;31m", "\x1b[38;5;247m", "\x1b[38;5;206m"]
RESET_COLOR = "\033[0m"


def show_maze_and_list(maze, color, config, path=None):
    print(color, end="")
    maze.display(path=path, color=color)   # 👈 دعم path
    print(RESET_COLOR, end="")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_intro():
    clear_screen()

    purple = "\033[95m"
    dim    = "\033[38;5;240m"
    reset  = "\033[0m"

    print(purple)
    print(r"""
   ░███            ░███     ░███    ░███    ░█████████ ░██████████         ░██████░███    ░██   ░██████  
  ░██░██           ░████   ░████   ░██░██         ░██  ░██                   ░██  ░████   ░██  ░██   ░██ 
 ░██  ░██          ░██░██ ░██░██  ░██  ░██       ░██   ░██                   ░██  ░██░██  ░██ ░██        
░█████████ ░██████ ░██ ░████ ░██ ░█████████    ░███    ░█████████  ░██████   ░██  ░██ ░██ ░██ ░██  █████ 
░██    ░██         ░██  ░██  ░██ ░██    ░██   ░██      ░██                   ░██  ░██  ░██░██ ░██     ██ 
░██    ░██         ░██       ░██ ░██    ░██  ░██       ░██                   ░██  ░██   ░████  ░██  ░███ 
░██    ░██         ░██       ░██ ░██    ░██ ░█████████ ░██████████         ░██████░██    ░███   ░█████░█ 
""")
    print(reset)

    print(dim + "=" * 45 + reset)
    print(dim + "  Maze Generator & Solver" + reset)
    print(dim + "  by Anass" + reset)
    print(dim + "=" * 45 + reset)

    print()
    print(dim + "  - Generate random mazes" + reset)
    print(dim + "  - Solve maze automatically" + reset)
    print(dim + "  - Export solution to file" + reset)
    print()

    input(purple + "  Press ENTER to start..." + reset)
    clear_screen()


def main():
    
    show_intro()

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

    # Seed
    if "SEED" in config:
        random.seed(config["SEED"])
    
    my_seed = config.get("SEED")


    # Initial maze
    maze = Maze(width, height, my_seed)
    maze.entry = entry
    maze.exit = exit_

    maze.create_42_cell_indexs(config)
    maze.generate()

    current_color = COLORS[0]
    path = None   # 🔥 مهم

    show_maze_and_list(maze, current_color, config, path)

    i = 1

    while True:
        try:
            color = "\033[94m"
            highlight = "\033[92m"
            reset = "\033[0m"

            print(color)
            print("╔" + "═"*40 + "╗")
            print("║{:^39}║".format("👽 MAZE MENU"))
            print("╠" + "═"*40 + "╣")

            print("║  {}1{} → Generate new random maze          ║".format(highlight, color))
            print("║  {}2{} → Display maze (random color)       ║".format(highlight, color))
            print("║  {}3{} → Solve maze                        ║".format(highlight, color))
            print("║  {}4{} → Exit                              ║".format(highlight, color))

            print("╚" + "═"*40 + "╝")
            print(reset)

            choice = input("\n==> Choose an option (1-4): ").strip()

        except (KeyboardInterrupt, Exception):
            print("\nProgram interrupted. Exiting...")
            break

        if choice == "1":
            maze = Maze(width, height, my_seed)
            maze.entry = entry
            maze.exit = exit_

            maze.create_42_cell_indexs(config)

            algorithms = {
                "dfs": maze.generate_dfs,
                "prims": maze.generate_prims
            }

            algo = input("Choose generation algorithm (dfs/prims): ").lower().strip()

            algorithms.get(algo, maze.generate_dfs)()

            path = None

            print("New random maze generated!")
            show_maze_and_list(maze, current_color, config, path)

           

        elif choice == "2":

            current_color = COLORS[i % len(COLORS)]
            i += 1

            print("Displaying maze in a new random color!")
            show_maze_and_list(maze, current_color, config, path)

        elif choice == "3":
            
            path = maze.solve()
            
            show = input("Show path? (y/n/animate): ").lower().strip()

            if show == "y":
                maze.display(path, color=current_color)

            elif show == "animate":
                maze.display(path, animate=True, delay=0.2, color=current_color)

            elif show == "n":
                maze.display(None, color=current_color)
            maze.export_hex_maze_and_path(path)
        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")
            


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")