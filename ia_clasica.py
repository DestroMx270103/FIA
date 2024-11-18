import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Representación del laberinto: 0 = camino, 1 = pared
maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
]

start = (0, 0)  # Posición inicial
end = (5, 5)    # Posición objetivo

def bfs(maze, start, end):
    """
    Algoritmo de búsqueda BFS para encontrar el camino más corto en un laberinto.
    
    Args:
        maze (list): Laberinto representado como una lista de listas.
        start (tuple): Coordenadas iniciales (fila, columna).
        end (tuple): Coordenadas objetivo (fila, columna).

    Returns:
        list: Camino desde el inicio hasta el objetivo o una lista vacía si no hay solución.
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}  # Rastrear el camino

    while queue:
        current = queue.popleft()
        if current == end:
            # Reconstruir el camino
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Invertir el camino

        # Expandir los vecinos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and neighbor not in visited and maze[neighbor[0]][neighbor[1]] == 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []  # Si no se encuentra solución

def dfs(maze, start, end, path=None, visited=None):
    """
    Algoritmo de búsqueda DFS para explorar todas las rutas posibles en un laberinto.
    
    Args:
        maze (list): Laberinto representado como una lista de listas.
        start (tuple): Coordenadas iniciales (fila, columna).
        end (tuple): Coordenadas objetivo (fila, columna).

    Returns:
        list: Camino desde el inicio hasta el objetivo o una lista vacía si no hay solución.
    """
    if path is None:
        path = []
    if visited is None:
        visited = set()

    path.append(start)
    visited.add(start)

    if start == end:
        return path

    # Expandir los vecinos
    rows, cols = len(maze), len(maze[0])
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor = (start[0] + dr, start[1] + dc)
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and neighbor not in visited and maze[neighbor[0]][neighbor[1]] == 0:
            result = dfs(maze, neighbor, end, path, visited)
            if result:
                return result

    path.pop()  # Retroceder si no hay solución en esta rama
    return []

def visualize_maze(maze, path):
    """
    Visualiza el laberinto y el camino encontrado utilizando matplotlib.
    
    Args:
        maze (list): Laberinto representado como una lista de listas.
        path (list): Lista de coordenadas del camino encontrado.
    """
    maze_array = np.array(maze)
    plt.imshow(maze_array, cmap="binary")

    # Dibujar el camino
    if path:
        x, y = zip(*path)
        plt.plot(y, x, color="red", linewidth=2, marker="o")

    plt.title("Laberinto Resuelto")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    print("Laberinto Original:")
    for row in maze:
        print(row)

    print("\nResolviendo con BFS...")
    bfs_path = bfs(maze, start, end)
    if bfs_path:
        print("Camino encontrado con BFS:", bfs_path)
    else:
        print("No se encontró un camino con BFS.")

    print("\nResolviendo con DFS...")
    dfs_path = dfs(maze, start, end)
    if dfs_path:
        print("Camino encontrado con DFS:", dfs_path)
    else:
        print("No se encontró un camino con DFS.")

    print("\nVisualizando el laberinto con el camino encontrado (BFS)...")
    visualize_maze(maze, bfs_path)
