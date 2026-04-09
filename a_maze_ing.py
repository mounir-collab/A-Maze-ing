import sys
import os
from typing import List, Optional, Tuple, TypedDict
from parsing import parse_config
from mazegen.maze_gen import Maze, Cell
from visualizer.maze_displayer import display
from solver.maze_solver import solve
from export_hex_maze.exporter import export_hex_maze_and_path


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    PERFECT: bool
    OUTPUT_FILE: str
    SEED: Optional[int]


# ANSI color codes
COLORS: List[str] = [
    "\x1b[46m",
    "\x1b[38;5;154m",
    "\033[93m",
    "\x1b[38;5;31m",
    "\x1b[38;5;247m",
    "\x1b[38;5;206m",
]

RESET_COLOR: str = "\033[0m"


def show_maze_and_list(
    maze: Maze,
    color: str,
    config: Config,
    path: Optional[List[Cell]] = None,
) -> None:
    """Display the maze with optional solution path."""
    print(color, end="")
    display(maze, path=path, color=color)
    print(RESET_COLOR, end="")


def clear_screen() -> None:
    """Clear terminal screen depending on OS."""
    os.system("cls" if os.name == "nt" else "clear")


def show_intro() -> None:
    """Display introduction banner and instructions."""
    clear_screen()
    purple: str = "\033[95m"
    dim: str = "\033[38;5;240m"
    reset: str = "\033[0m"

    print(purple)
    print(
        r"   ░███            ░███     ░███    ░███    ░█████████ "
        r"░██████████         ░██████░███    ░██   ░██████"
    )
    print(
        r"  ░██░██           ░████   ░████   ░██░██         "
        r"░██  ░██                   ░██  ░████   ░██  ░██   ░██"
    )
    print(
        r" ░██  ░██          ░██░██ ░██░██  ░██  ░██       "
        r"░██   ░██                   ░██  ░██░██  ░██ ░██"
    )
    print(
        r"░█████████ ░██████ ░██ ░████ ░██ ░█████████    "
        r"░███    ░█████████  ░██████   ░██  ░██ ░██ ░██ ░██  █████"
    )
    print(
        r"░██    ░██         ░██  ░██  ░██ ░██    ░██   "
        r"░██      ░██                   ░██  ░██  ░██░██ ░██     ██"
    )
    print(
        r"░██    ░██         ░██       ░██ ░██    ░██  "
        r"░██       ░██                   ░██  ░██   ░████  ░██  ░███"
    )
    print(
        r"░██    ░██         ░██       ░██ ░██    ░██ "
        r"░█████████ ░██████████         ░██████░██    ░███   ░█████░█"
    )
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


def main() -> None:
    """Main program entry point."""
    show_intro()

    if len(sys.argv) != 2:
        print("Usage: python3 main.py config.txt")
        sys.exit(1)

    config_file: str = sys.argv[1]

    # parse config and cast to Config TypedDict
    config: Config = parse_config(config_file)  # type: ignore

    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    entry: Tuple[int, int] = config["ENTRY"]
    exit_: Tuple[int, int] = config["EXIT"]
    perfect_maze: bool = config["PERFECT"]

    my_seed: Optional[int] = config.get("SEED")

    # create Maze instance
    maze: Maze = Maze(
                      width,
                      height,
                      entry,
                      exit_,
                      seed=my_seed,
                      perfect=perfect_maze
                    )
    maze.create_42_cell_indexs(dict(config))  # cast TypedDict to plain dict
    maze.generate_dfs()

    current_color: str = COLORS[0]
    path: Optional[List[Cell]] = None

    show_maze_and_list(maze, current_color, config, path)
    export_hex_maze_and_path(maze,
                             path,
                             entry,
                             exit_,
                             config["OUTPUT_FILE"])
    i: int = 1

    while True:
        try:
            color: str = "\033[94m"
            highlight: str = "\033[92m"
            reset: str = "\033[0m"

            print(color)
            print("╔" + "═" * 40 + "╗")
            print("║{:^39}║".format("👽 MAZE MENU"))
            print("╠" + "═" * 40 + "╣")

            print(
                "║  {}1{} → Generate new random "
                "maze          ║".format(highlight, color)
            )
            print(
                "║  {}2{} → Display maze "
                "(random color)       ║".format(highlight, color)
            )
            print(
                "║  {}3{} → Solve maze                        ║".format(
                    highlight,
                    color,
                )
            )
            print(
                "║  {}4{} → Exit                              ║".format(
                    highlight,
                    color,
                )
            )

            print("╚" + "═" * 40 + "╝")
            print(reset)

            choice: str = input("\n==> Choose an option (1-4): ").strip()

        except (KeyboardInterrupt, Exception):
            print("\nProgram interrupted. Exiting...")
            break

        if choice == "1":
            maze = Maze(
                        width,
                        height,
                        entry,
                        exit_,
                        seed=my_seed,
                        perfect=perfect_maze
                        )
            maze.create_42_cell_indexs(dict(config))
            path = None
            algorithms = {
                "dfs": maze.generate_dfs,
                "prims": maze.generate_prims,
            }

            algo: str = (
                input("Choose generation "
                      "algorithm (dfs/prims): ").lower().strip()
            )

            algorithms.get(algo, maze.generate_dfs)()

            print("New random maze generated!")

            show_maze_and_list(maze, current_color, config, path)
            export_hex_maze_and_path(maze,
                                     path,
                                     config["ENTRY"],
                                     config["EXIT"],
                                     config["OUTPUT_FILE"])
        elif choice == "2":
            current_color = COLORS[i % len(COLORS)]
            i += 1

            print("Displaying maze in a new random color!")
            show_maze_and_list(maze, current_color, config, path)

        elif choice == "3":
            path = solve(maze)

            show: str = input("Show path? (y/n/animate): ").lower().strip()

            if show == "y":
                display(maze, path, color=current_color)
            elif show == "animate":
                display(
                        maze,
                        path,
                        animate=True,
                        delay=0.2,
                        color=current_color
                        )
            else:
                display(maze, None, color=current_color)

            export_hex_maze_and_path(maze,
                                     path,
                                     config["ENTRY"],
                                     config["EXIT"],
                                     config["OUTPUT_FILE"])

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
