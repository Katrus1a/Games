import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
size = [440, 600]
Block_size = 20
Block_count = 20
Frame_color = (16, 74, 53)
White_color = (255, 255, 255)
Blue_color = (10, 163, 112)
Violet_color = (116, 38, 240)
Black_color = (0, 0, 0)
Red_color = (255, 0, 0)
margin = 1

# Створення екрану
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SNAKE')

# Налаштування годинника для управління швидкістю гри
clock = pygame.time.Clock()

snake_size = 20
snake_speed = 15

# Шрифти для текстових повідомлень
message_font = pygame.font.SysFont('Arial', 42)
score_font = pygame.font.SysFont('Arial', 30)

# Таймер гри
start_time = pygame.time.get_ticks()

# Функція для виведення рахунку
def print_score(score):
    text = score_font.render("Score:" + str(score), True, White_color)
    screen.blit(text, [0, 0])

# Функція для виведення часу
def print_time():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Конвертуємо в секунди
    time_text = score_font.render(f"Time: {elapsed_time} sec", True, White_color)
    screen.blit(time_text, [size[0] - 150, 0])

# Функція для малювання змійки
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(screen, Violet_color, [pixel[0], pixel[1], snake_size, snake_size])

# Поле у шахматному порядку
def draw_grid():
    for row in range(Block_count):
        for column in range(Block_count):
            if (row + column) % 2 == 0:
                color = Blue_color
            else:
                color = White_color
            pygame.draw.rect(screen, color, [column * Block_size, row * Block_size, Block_size, Block_size])

# Екран Game Over
def game_over_screen():
    screen.fill(Black_color)
    game_over_message = message_font.render("Game Over!", True, Red_color)
    try_again_message = score_font.render("Press R to Try Again", True, White_color)
    screen.blit(game_over_message, [size[0] / 3, size[1] / 3])
    screen.blit(try_again_message, [size[0] / 3, size[1] / 2])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Основна функція гри
def run_game():
    global snake_speed  # Оголошення змінної як глобальної
    global start_time
    start_time = pygame.time.get_ticks()  # Оновлюємо стартовий час при початку нової гри
    game_over = False
    game_close = False

    # Початкова позиція змійки
    x = size[0] / 2
    y = size[1] / 2

    # Початкова швидкість змійки
    x_speed = 0
    y_speed = 0

    snake_pixels = []
    snake_length = 1

    # Початкове положення їжі
    target_x = round(random.randrange(0, size[0] - snake_size) / 20.0) * 20.0
    target_y = round(random.randrange(0, size[1] - snake_size) / 20.0) * 20.0

    while not game_over:

        while game_close:
            game_over_screen()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                if event.key == pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_size
                # Клавіші для збільшення або зменшення швидкості змійки
                if event.key == pygame.K_PLUS:
                    snake_speed += 5
                if event.key == pygame.K_MINUS:
                    snake_speed -= 5

        if x >= size[0] or x < 0 or y >= size[1] or y < 0:
            game_close = True

        x += x_speed
        y += y_speed

        screen.fill(Frame_color)
        draw_grid()
        pygame.draw.rect(screen, Red_color, [target_x, target_y, snake_size, snake_size])

        snake_pixels.append([x, y])

        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True

        draw_snake(snake_size, snake_pixels)
        print_score(snake_length - 1)
        print_time()

        pygame.display.update()

        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, size[0] - snake_size) / 20.0) * 20.0
            target_y = round(random.randrange(0, size[1] - snake_size) / 20.0) * 20.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Запуск гри
run_game()
