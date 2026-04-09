*This project has been created as part of the 42 curriculum by <manzar>, <ancheab>.*

## Description

A-Maze-ing is an interactive maze generation and solving application. It enables users to generate random mazes using different algorithms and then solve them using pathfinding techniques. The project combines maze generation, visualization, and solver capabilities in an integrated tool.

**Project Goal:** To demonstrate proficiency in algorithm implementation, object-oriented design, and interactive terminal-based applications by creating a fully functional maze generator and solver.

## Instructions

### Compilation & Installation

1. **Prerequisites:** Python 3.10 or higher
2. **Install dependencies:**
   ```bash
   make install
   ```
3. **Build the package (optional):**
   ```bash
   make build
   ```

### Execution

Run the application with:
```bash
make run
```

Or directly:
```bash
python3 a_maze_ing.py config.txt
```

The program will display an interactive menu where you can:
- Generate new random mazes
- Display mazes with different color schemes
- Solve mazes and visualize the solution
- Export solutions to files

## Configuration File Structure

The `config.txt` file controls application parameters:

```
WIDTH=20              # Maze width (number of cells)
HEIGHT=20             # Maze height (number of cells)
ENTRY=0,0             # Starting position (row, column)
EXIT=19,19            # Exit position (row, column)
PERFECT=False         # True for perfect maze (single path), False otherwise
OUTPUT_FILE=maze.txt  # Output file for maze/solution export
#SEED=10              # Optional: reproducible maze generation (commented out by default)
```

**Parameters Explanation:**
- `WIDTH` & `HEIGHT`: Define maze dimensions
- `ENTRY` & `EXIT`: Specify start and end points
- `PERFECT`: Controls maze type (perfect mazes have exactly one path between any two points)
- `OUTPUT_FILE`: File path where solutions are exported
- `SEED`: Optional parameter for reproducible maze generation

## Maze Generation Algorithm

### DFS (Depth-First Search)
- **Default algorithm** used for maze generation
- Creates mazes by recursively visiting unvisited cells
- Generates long, winding paths with fewer branches

### Prim's Algorithm
- Alternative algorithm available in the interactive menu
- Creates mazes by randomly selecting edges from a minimum spanning tree
- Generates more balanced, distributed maze patterns

### Why DFS?
DFS was chosen as the primary algorithm because:
- Efficient time complexity O(W×H) and space complexity O(W×H)
- Produces natural-looking, aesthetically pleasing mazes
- Simpler implementation compared to other algorithms
- Better stack space locality for recursive implementation
- Well-suited for interactive real-time generation

## Reusable Components

The project is structured with reusable, modular components:

### 1. **maze_gene Package**
- **Location:** `maze_gene/` directory
- **Reusability:** Can be imported as a standalone package for maze generation
- **Usage:** 
  ```python
  from maze_gene.maze_gen import Maze
  maze = Maze(width=20, height=20, entry=(0,0), exit=(19,19))
  maze.generate_dfs()
  ```
- **Contains:** Core maze generation logic, cell management, and generation algorithms

### 2. **solver Module**
- **Location:** `solver/` directory
- **Reusability:** Independent solver module for any grid-based maze
- **Usage:**
  ```python
  from solver.maze_solver import solve
  path = solve(maze)
  ```
- **Contains:** Pathfinding algorithms (BFS, A*, Dijkstra)

### 3. **visualizer Module**
- **Location:** `visualizer/` directory
- **Reusability:** Generic maze display function for ASCII visualization
- **Usage:**
  ```python
  from visualizer.maze_displayer import display
  display(maze, path=None, color="\033[92m", animate=False)
  ```
- **Features:** Color support, animation capability, terminal rendering

### 4. **export_hex_maze Module**
- **Location:** `export_hex_maze/` directory
- **Reusability:** Export mazes and solutions to text files
- **Usage:**
  ```python
  from export_hex_maze.exporter import export_hex_maze_and_path
  export_hex_maze_and_path(maze, path, "output.txt")
  ```

### 5. **parsing Module**
- **Location:** `parsing.py`
- **Reusability:** Configuration file parser
- **Usage:**
  ```python
  from parsing import parse_config
  config = parse_config("config.txt")
  ```

## Team & Project Management

### Team Composition
- **manzar**: Developer and Project Lead
  - Responsible for overall architecture
  - Maze generation and solver implementation
  - Testing and integration
- **ancheab** Developer and Project Partner
  - Maze parsing and hadling errors
  - Testing and integration
  - Maze displaying and make decorations

### Planning & Evolution
**Initial Plan:**
- Create basic maze generator with DFS
- Implement BFS solver
- Add terminal visualization

**Evolution During Development:**
- Expanded to include Prim's algorithm for variety
- Added color support and animation features
- Implemented interactive menu system
- Packaged maze_gene as reusable library
- Added export functionality for maze solutions

### What Worked Well
- Modular architecture allowed independent development of components
- TypedDict usage provided better code documentation and IDE support
- Color-coded terminal output improved user experience
- Interactive menu made the application more user-friendly
- Package structure enables reusability

### Areas for Improvement
- Could implement more advanced algorithms (recursive backtracking optimization)
- GUI version would enhance usability
- Performance optimization for very large mazes
- More sophisticated path visualization (3D, web-based)
- Additional solver algorithms (A*, Dijkstra's, bidirectional search)

### Tools & Technologies Used
- **Python 3.10+**: Core language
- **Poetry**: Dependency management and packaging
- **mypy**: Static type checking for code quality
- **flake8**: Code linting and style enforcement
- **Makefile**: Build automation and task runner
- **ANSI escape codes**: Terminal color and formatting
- **Git & GitHub**: Version control and collaboration

## Advanced Features

### Multi-Algorithm Support
Choose between DFS and Prim's algorithm during maze generation:
```
Choose generation algorithm (dfs/prims): dfs
```

### Color Display Options
Cycle through 6 different color schemes for maze visualization:
- Cyan background
- Lime green
- Yellow
- Blue
- Gray
- Magenta

### Solution Visualization
Multiple viewing modes for solutions:
- **Static display**: Show complete path at once
- **Step-by-step**: Display path on demand
- **Animation**: Animated path visualization with adjustable speed (0.2s per cell)

### Export Functionality
Solutions and mazes can be exported to text files in hexadecimal representation for:
- External analysis
- Sharing maze data
- Archival purposes

## Resources

### Documentation & References
- [Depth-First Search Algorithm](https://en.wikipedia.org/wiki/Depth-first_search)
- [Prim's Algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)

### AI Usage

**GitHub Copilot was used for the following tasks:**

1. **Code Structure & Architecture**: Guidance on modular design patterns and package organization
2. **Algorithm Implementation**: Assistance with DFS and Prim's algorithm implementations
3. **Type Hints**: Help with Python type annotations and TypedDict usage
4. **Error Handling**: Best practices for exception handling and validation
5. **Documentation**: README and docstring generation
6. **Code Optimization**: Performance suggestions for maze operations
7. **Testing Assistance**: Unit test structure recommendations
8. **ANSI Color Codes**: Terminal formatting and color code references

**Parts NOT using AI:**
- Core algorithmic logic validation
- Final testing and debugging
- Project architecture decisions
- UI/UX design choices
