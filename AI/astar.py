from collections import deque
import heapq

target_mode = "food"

def get_next_direction(snake, food, walls, map_width, map_height):
    global target_mode

    head = snake[0]
    tail = snake[-1]
    body = set(snake)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def is_safe(pos):
        x, y = pos
        return (
            0 <= x < map_width and
            0 <= y < map_height and
            pos not in walls and
            pos not in body
        )

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(start, goal):
        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
        came_from = {}
        g_score = {start: 0}
        visited = set()

        while open_set:
            _, cost, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            visited.add(current)

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if not is_safe(neighbor) or neighbor in visited:
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
        return None

    # Спроба знайти шлях до їжі
    path_to_food = astar(head, food)
    if path_to_food:
        target_mode = "food"
        next_cell = path_to_food[0]
        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]
        return (dx, dy)

    # Безпечний режим — шлях до хвоста
    target_mode = "safe"
    path_to_tail = astar(head, tail)
    if path_to_tail:
        next_cell = path_to_tail[0]
        dx = next_cell[0] - head[0]
        dy = next_cell[1] - head[1]
        return (dx, dy)

    # Якщо нічого не знайшли — просто безпечний крок
    for dx, dy in directions:
        new_pos = (head[0] + dx, head[1] + dy)
        if is_safe(new_pos):
            return (dx, dy)

    return (0, 0)