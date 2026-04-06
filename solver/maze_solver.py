from collections import deque

def solve(maze):

    start = maze.grid[maze.entry[1]][maze.entry[0]]
    end = maze.grid[maze.exit[1]][maze.exit[0]]

    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft()

        if current == end:
            break

        for neighbor in maze.reachable_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # reconstruct path
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent.get(cur)

        if cur is None:
            return []

    path.append(start)
    path.reverse()

    return path