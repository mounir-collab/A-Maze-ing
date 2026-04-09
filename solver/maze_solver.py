from typing import List, Dict, Set
from collections import deque
from mazegen.maze_gen import Maze, Cell


def solve(maze: Maze) -> List[Cell]:
    """
    Solve the maze using Breadth-First Search (BFS).

    The algorithm explores cells level by level using a queue,
    guaranteeing the shortest path between the entry and exit.

    Args:
        maze: Maze instance containing the grid and topology.

    Returns:
        List[Cell]: Ordered list of cells representing the path
        from entry to exit. Returns an empty list if no path exists.
    """

    start: Cell = maze.grid[maze.entry[1]][maze.entry[0]]
    end: Cell = maze.grid[maze.exit[1]][maze.exit[0]]

    queue: deque[Cell] = deque([start])
    visited: Set[Cell] = {start}
    parent: Dict[Cell, Cell] = {}

    while queue:
        current: Cell = queue.popleft()

        if current == end:
            break

        for neighbor in maze.reachable_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # reconstruct path
    path: List[Cell] = []
    cur: Cell | None = end

    while cur != start:
        if cur is None:
            return []

        path.append(cur)
        cur = parent.get(cur)

    path.append(start)
    path.reverse()

    return path
