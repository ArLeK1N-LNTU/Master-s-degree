import pygame
import random
import sys
import json
from menu import main_menu
from AI.greedy import get_next_direction as greedy_direction
from AI.astar import get_next_direction as astar_direction
import os

CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)
clock = pygame.time.Clock()

def load_records():
    try:
        with open("records.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_records(records):
    with open("records.json", "w") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

def get_best_score(map_name, mode):
    records = load_records()
    return records.get(map_name, {}).get(mode, 0)

def update_record(map_name, mode, score):
    records = load_records()
    if map_name not in records:
        records[map_name] = {}
    records[map_name][mode] = score
    save_records(records)

def load_map(filename):
    walls = []
    snake_start = None
    food_pos = None
    with open(f"maps/{filename}", 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    height = len(lines)
    width = len(lines[0])
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                walls.append((x, y))
            elif char == 'S':
                snake_start = (x, y)
            elif char == 'F':
                food_pos = (x, y)
    return width, height, walls, snake_start, food_pos

def get_offsets(map_width, map_height, screen_width, screen_height):
    offset_x = (screen_width - map_width * CELL_SIZE) // 2
    offset_y = (screen_height - map_height * CELL_SIZE) // 2 + 60
    return offset_x, offset_y

def draw_cell(pos, color, offset_x, offset_y):
    x, y = pos
    rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def draw_score(score, best, is_new):
    pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 0, screen.get_width(), 60))
    text1 = font.render(f"Счёт: {score}", True, WHITE)
    record_text = f"Рекорд: {best}"
    if is_new:
        record_text += " (новый!)"
    text2 = font.render(record_text, True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))

def check_collision(pos, snake, walls, map_width, map_height):
    x, y = pos
    return (
        x < 0 or x >= map_width or
        y < 0 or y >= map_height or
        pos in snake[1:] or
        pos in walls
    )

def game_over_screen(score):
    screen.fill(BLACK)
    text1 = big_font.render("Игра окончена", True, RED)
    text2 = font.render(f"Ваш счёт: {score}", True, WHITE)
    text3 = font.render("Нажмите любую клавишу для перезапуска", True, WHITE)
    screen.blit(text1, (screen.get_width() // 2 - text1.get_width() // 2, 200))
    screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2, 270))
    screen.blit(text3, (screen.get_width() // 2 - text3.get_width() // 2, 320))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def generate_food(snake, walls, map_width, map_height):
    possible_positions = [
        (x, y)
        for x in range(map_width)
        for y in range(map_height)
        if (x, y) not in snake and (x, y) not in walls
    ]
    return random.choice(possible_positions)

def reset_game(filename):
    map_width, map_height, walls, snake_start, food_pos = load_map(filename)
    window_width = max(800, map_width * CELL_SIZE + 100)
    window_height = max(600, map_height * CELL_SIZE + 160)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Змейка: карта " + filename)
    snake = [snake_start or (5, 5)]
    direction = (1, 0)
    food = food_pos or generate_food(snake, walls, map_width, map_height)
    score = 0
    return screen, map_width, map_height, walls, snake, direction, food, score

while True:
    map_filename, difficulty, control_mode = main_menu()

    control_mode = control_mode.strip()
    if control_mode == "ИИ (Greedy)":
        mode_key = "ИИ (Greedy)"
    elif control_mode == "ИИ (A*)":
        mode_key = "ИИ (A*)"
    else:
        mode_key = "Игрок"

    FPS = {"Easy": 8, "Normal": 12, "Hard": 18}[difficulty]
    screen, map_width, map_height, walls, snake, direction, food, score = reset_game(map_filename)
    offset_x, offset_y = get_offsets(map_width, map_height, screen.get_width(), screen.get_height())

    best_record = get_best_score(map_filename, mode_key)
    new_record = False
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if control_mode == "Игрок":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and direction != (0, 1):
                direction = (0, -1)
            elif keys[pygame.K_s] and direction != (0, -1):
                direction = (0, 1)
            elif keys[pygame.K_a] and direction != (1, 0):
                direction = (-1, 0)
            elif keys[pygame.K_d] and direction != (-1, 0):
                direction = (1, 0)
        elif control_mode == "ИИ (Greedy)":
            next_dir = greedy_direction(snake, food, walls, map_width, map_height)
            if next_dir != (0, 0):
                direction = next_dir
        elif control_mode == "ИИ (A*)":
            next_dir = astar_direction(snake, food, walls, map_width, map_height)
            if next_dir != (0, 0):
                direction = next_dir

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if check_collision(new_head, snake, walls, map_width, map_height):
            game_over_screen(score)
            break
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = generate_food(snake, walls, map_width, map_height)
            if score > best_record:
                best_record = score
                new_record = True
                update_record(map_filename, mode_key, best_record)
        else:
            snake.pop()
        screen.fill(BLACK)
        for wall in walls:
            draw_cell(wall, WHITE, offset_x, offset_y)
        draw_cell(food, RED, offset_x, offset_y)
        for segment in snake:
            draw_cell(segment, GREEN, offset_x, offset_y)
        draw_score(score, best_record, new_record)
        pygame.display.flip()