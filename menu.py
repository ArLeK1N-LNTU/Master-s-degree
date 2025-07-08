import pygame
import os
import sys

# Настройки
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (70, 140, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню выбора карты, сложности и режима")
font = pygame.font.SysFont("Arial", FONT_SIZE)
clock = pygame.time.Clock()

def get_map_list():
    return [f for f in os.listdir("maps") if f.endswith(".txt")]

def draw_text(text, x, y, selected=False):
    color = BLUE if selected else WHITE
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def main_menu():
    maps = get_map_list()
    if not maps:
        print("Немає доступних карт у папці maps/")
        pygame.quit()
        sys.exit()

    map_index = 0
    difficulties = ["Легко", "Нормально", "Важко"]
    diff_index = 1
    modes = ["Гравець", "ШІ (Greedy)", "ШІ (A*)"]
    mode_index = 0
    selected_option = 0

    running = True
    while running:
        screen.fill(BLACK)

        title = font.render("Вибір карти, складності та режиму", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        draw_text("Карта: " + maps[map_index], 100, 150, selected_option == 0)
        draw_text("Складність: " + difficulties[diff_index], 100, 220, selected_option == 1)
        draw_text("Режим: " + modes[mode_index], 100, 290, selected_option == 2)
        draw_text("Грати", 100, 360, selected_option == 3)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 4
                elif event.key == pygame.K_LEFT:
                    if selected_option == 0:
                        map_index = (map_index - 1) % len(maps)
                    elif selected_option == 1:
                        diff_index = (diff_index - 1) % len(difficulties)
                    elif selected_option == 2:
                        mode_index = (mode_index - 1) % len(modes)
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 0:
                        map_index = (map_index + 1) % len(maps)
                    elif selected_option == 1:
                        diff_index = (diff_index + 1) % len(difficulties)
                    elif selected_option == 2:
                        mode_index = (mode_index + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 3:
                        return maps[map_index], difficulties[diff_index], modes[mode_index]

if __name__ == "__main__":
    chosen_map, chosen_difficulty, chosen_mode = main_menu()
    print("Карта:", chosen_map, "| Сложность:", chosen_difficulty, "| Режим:", chosen_mode)
    pygame.quit()
