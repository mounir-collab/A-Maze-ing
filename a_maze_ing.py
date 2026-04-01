import sys
import random
import os
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
    print(dim + "  by ancheab and manzar" + reset)
    print(dim + "=" * 45 + reset)

    print()
    print(dim + "  - Generate random mazes" + reset)
    print(dim + "  - Solve maze automatically" + reset)
    print(dim + "  - Export solution to file" + reset)
    print()

    input(purple + "  Press ENTER to start..." + reset)
    clear_screen()


def main():
    
    show_intro()  # 👈 هادي جديدة

    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        sys.exit(1)
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
            color = "\033[94m"   # blue
            highlight = "\033[92m"  # green
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
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")