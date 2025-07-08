from collections import deque

target_mode = "food"

def get_next_direction(snake, food, walls, map_width, map_height):
    global target_mode

    head = snake[0]
    tail = snake[-1]
    body = set(snake)

    directions = [
        (0, -1), (0, 1), (-1, 0), (1, 0)
    ]

    # Перевірка безпеки
    def is_safe(pos):
        x, y = pos
        return (
            0 <= x < map_width and
            0 <= y < map_height and
            pos not in walls and
            pos not in body
        )

    # BFS-перевірка досяжності
    def bfs_path(start, goal):
        visited = set()
        prev = {}
        queue = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            if current == goal:
                # Відновимо шлях
                path = []
                while current != start:
                    path.append(current)
                    current = prev[current]
                path.reverse()
                return path

            for d in directions:
                nx, ny = current[0] + d[0], current[1] + d[1]
                neighbor = (nx, ny)
                if neighbor not in visited and is_safe(neighbor):
                    visited.add(neighbor)
                    prev[neighbor] = current
                    queue.append(neighbor)
        return None

    # 1. Перевіряємо шлях до їжі
    path_to_food = bfs_path(head, food)
    if path_to_food:
        target_mode = "food"
    else:
        target_mode = "safe"

    # 2. У режимі FOOD — просто йдемо до їжі
    if target_mode == "food" and path_to_food:
        next_cell = path_to_food[0]
        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]
        return (dx, dy)

    # 3. У режимі SAFE — намагаємося дійти до хвоста
    path_to_tail = bfs_path(head, tail)
    if path_to_tail:
        next_cell = path_to_tail[0]
        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]
        return (dx, dy)

    # 4. Якщо нічого не спрацювало — шукаємо просто безпечний крок
    for d in directions:
        nx, ny = head[0] + d[0], head[1] + d[1]
        if is_safe((nx, ny)):
            return d

    # 5. Все заблоковано
    return (0, 0)




