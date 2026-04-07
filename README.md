# A-Maze-ing

> A terminal-based maze generator, solver, and exporter written in Python.

Generate random mazes, watch them being solved step-by-step, and export the solution — all from your terminal.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Program](#running-the-program)
5. [Configuration](#configuration)
6. [How to Use](#how-to-use)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

- **Two generation algorithms** — Depth-First Search (Recursive Backtracker) and Randomized Prim's
- **Perfect & imperfect mazes** — perfect mazes have exactly one path between any two cells; imperfect mazes introduce extra loops
- **BFS solver** — finds the guaranteed shortest path from entry to exit
- **Animated solution** — watch the solution path drawn cell-by-cell in the terminal
- **Colorized display** — cycle through multiple ANSI color themes
- **Hex export** — save the maze walls (as hexadecimal bitmasks) and the solution directions to a `.txt` file
- **Reproducible mazes** — set an optional random seed in the config
- **Hidden 42 pattern** — configurable cells are pre-marked to embed the number "42" inside larger mazes

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Build system | [Poetry](https://python-poetry.org/) |
| Linting | [flake8](https://flake8.pycqa.org/) |
| Type checking | [mypy](https://mypy-lang.org/) |
| Stdlib modules used | `random`, `collections.deque`, `os`, `time`, `sys`, `re` |

No third-party runtime dependencies are required.

---

## Project Structure

```
A-Maze-ing/
├── a_maze_ing.py          # Main entry point — menu loop and program orchestration
├── config.txt             # Default configuration file
├── parsing.py             # Config file parser with validation
├── maze_gene/
│   └── maze_gen.py        # Cell and Maze classes; DFS and Prim's generation algorithms
├── solver/
│   └── maze_solver.py     # BFS-based maze solver (shortest path)
├── visualizer/
│   └── maze_displayer.py  # Terminal renderer with ANSI colors and animation support
├── export_hex_maze/
│   └── exporter.py        # Exports maze walls (hex) and solution path to a text file
├── Makefile               # Convenience targets: run, build, lint, clean
├── pyproject.toml         # Project metadata (Poetry)
└── LICENSE                # GNU General Public License v3
```

---

## Getting Started

### Prerequisites

- Python **3.10** or later
- `pip` (comes with Python)

Optional, for linting and type-checking:

```bash
make install
# equivalent to: pip install mypy flake8
```

### Installation

Clone the repository:

```bash
git clone https://github.com/mounir-collab/A-Maze-ing.git
cd A-Maze-ing
```

No additional package installation is required to run the program.

### Running the Program

```bash
make run
# equivalent to: python3 a_maze_ing.py config.txt
```

Or pass a custom config file directly:

```bash
python3 a_maze_ing.py my_config.txt
```

---

## Configuration

Edit `config.txt` to customize the maze before running:

```ini
WIDTH=20          # Number of columns
HEIGHT=20         # Number of rows
ENTRY=0,0         # Entry cell (x,y) — must be within bounds
EXIT=19,19        # Exit cell (x,y)  — must differ from ENTRY
PERFECT=False     # True = perfect maze (no loops), False = adds random loops
OUTPUT_FILE=maze.txt  # File to write the exported maze and solution path
#SEED=10          # Uncomment to fix the random seed for reproducibility
```

**Constraints:**
- `ENTRY` and `EXIT` must be within `[0, WIDTH-1] × [0, HEIGHT-1]`.
- `OUTPUT_FILE` must end in `.txt` and cannot be `config.txt`.

---

## How to Use

After starting the program with `make run`, an intro banner is displayed. Press **Enter** to continue.

The interactive menu provides four options:

| Option | Action |
|--------|--------|
| `1` | Generate a new random maze. You will be prompted to choose the algorithm: `dfs` (Recursive Backtracker) or `prims` (Randomized Prim's). |
| `2` | Redisplay the current maze with a different ANSI color. |
| `3` | Solve the maze with BFS. You will be asked whether to show the path (`y`), animate it (`animate`), or skip display (`n`). The maze and solution are always exported to `OUTPUT_FILE`. |
| `4` | Exit the program. |

### Terminal display legend

| Symbol | Meaning |
|--------|---------|
| `👽` | Entry cell |
| `🌍` | Exit cell |
| `🛸` | Solution path cell |
| `⬜` | Blocked cell (part of the hidden 42 pattern) |
| `██` | Wall |

### Exported file format (`maze.txt`)

The file contains two sections:

1. **Maze walls** — one row per line; each character is a hexadecimal bitmask of the walls for that cell (`N=1, E=2, S=4, W=8`).
2. **Solution path** — a string of compass directions (`N`, `S`, `E`, `O` for west) prefixed with `path:`.

Example:

```
BD1795...
...

path: SESSSENEESSEESO...
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/my-improvement
   ```
2. **Make your changes.** Keep the code style consistent with the existing codebase.
3. **Lint and type-check** before committing:
   ```bash
   make lint
   ```
4. **Commit** with a clear, descriptive message and open a **Pull Request** against `main`.

For larger changes, please open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the **GNU General Public License v3.0**.
See the [LICENSE](LICENSE) file for the full text.