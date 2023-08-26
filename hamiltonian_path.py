def insert_neighbors(x, n, m):
    """Inserts neighboring positions of x into a list."""
    neighbors = []

    # Check if there's a position on the right
    if (x % n) + 1 < n:
        neighbors.append(x + 1)

    # Check if there's a position on the left
    if (x % n) - 1 >= 0:
        neighbors.append(x - 1)

    # Check if there's a position above
    if x - n >= 0:
        neighbors.append(x - n)
    
    # Check if there's a position below
    if x + n <= n * m - 1:
        neighbors.append(x + n)

    return neighbors


def search_hamiltonian_path(graph, path, pos):
    """Recursively searches for a Hamiltonian path in the graph."""
    if pos == len(graph):
        if path[0] in graph[path[pos - 1]]:
            return True
        else:
            return False
        
    for neighbor in graph[path[pos - 1]]:
        if neighbor not in path:
            path[pos] = neighbor
            if search_hamiltonian_path(graph, path, pos + 1):
                return True
            path[pos] = -1

    return False

def hamiltonian_path(start, width, height):
    """Finds a Hamiltonian path starting from the given position in a grid."""
    graph = [insert_neighbors(i, width, height) for i in range(width * height)]
    path = [-1] * (width * height)
    path[0] = start[0] + start[1] * width

    if search_hamiltonian_path(graph, path, 1):
        return path
    return None

def hamiltonian_path_snake(matrix, n, m):
    """Finds a Hamiltonian path for a snake-like pattern in a grid."""
    if n % 2 == 1 and m % 2 == 1:
        return None
    
    num_positions = n * m
    path = [-1] * num_positions
    path[0] = 0
    
    # Set the default one, the first column which will point to (0, 0) position
    for i in range(num_positions - 1, num_positions - m, -1):
        path[i] = n * (m - (i % m))

    remaing_index = num_positions - m

    start_x = 1
    start_y = m - 1
    if m % 2 == 1:
        while start_x != n:
            path[remaing_index] = start_x + (start_y * n)
            remaing_index -= 1

            if start_y == m - 1:
                start_y -= 1
            else:
                start_y += 1
            path[remaing_index] = start_x + (start_y * n)
            remaing_index -= 1
            start_x += 1

        start_x = n - 1
    else:
        while start_x != n - 1:
            path[remaing_index] = start_x + (start_y * n)
            remaing_index -= 1
            start_x += 1

        path[remaing_index] = start_x + (start_y * n)
        remaing_index -= 1

    start_y -= 1
    direction = -1  # Go from right to left, then reverse the direction
    while start_y != -1:
        while start_x != 0 and start_x != n:
            path[remaing_index] = start_x + (start_y * n)
            remaing_index -= 1
            start_x += direction
        
        if direction == -1:
            start_x = 1
        else: 
            start_x = n - 1

        start_y -= 1
        direction *= -1

    return path