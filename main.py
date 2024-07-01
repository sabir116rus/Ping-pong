import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройка окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))  # Создаем окно с заданными размерами
pygame.display.set_caption('Pong Game')  # Устанавливаем заголовок окна

# Цвета
white = (255, 255, 255)  # Белый цвет
black = (0, 0, 0)  # Черный цвет

# Настройка FPS
clock = pygame.time.Clock()  # Создаем объект Clock для управления частотой кадров
fps = 60  # Устанавливаем частоту кадров

# Размеры ракеток
paddle_width, paddle_height = 10, 100

# Позиции ракеток
left_paddle = pygame.Rect(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)  # Левая ракетка
right_paddle = pygame.Rect(width - 30 - paddle_width, height // 2 - paddle_height // 2, paddle_width,
                           paddle_height)  # Правая ракетка

# Размеры мяча
ball_size = 20
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)  # Мяч

# Скорости
ball_speed = [5, 5]  # Скорость мяча по горизонтали и вертикали
left_paddle_speed = 0  # Скорость левой ракетки
right_paddle_speed = 0  # Скорость правой ракетки
paddle_speed = 7  # Скорость движения ракеток

# Очки
left_score = 0  # Очки левого игрока
right_score = 0  # Очки правого игрока
font = pygame.font.Font(None, 74)  # Шрифт для отображения очков


# Функция для перемещения ракеток
def move_paddles():
    global left_paddle_speed, right_paddle_speed
    keys = pygame.key.get_pressed()  # Получаем текущее состояние всех клавиш
    # Управление левой ракеткой
    if keys[pygame.K_w]:
        left_paddle_speed = -paddle_speed  # Двигаем вверх
    elif keys[pygame.K_s]:
        left_paddle_speed = paddle_speed  # Двигаем вниз
    else:
        left_paddle_speed = 0  # Останавливаем ракетку

    # Управление правой ракеткой
    if keys[pygame.K_UP]:
        right_paddle_speed = -paddle_speed  # Двигаем вверх
    elif keys[pygame.K_DOWN]:
        right_paddle_speed = paddle_speed  # Двигаем вниз
    else:
        right_paddle_speed = 0  # Останавливаем ракетку

    # Обновляем позиции ракеток
    left_paddle.y += left_paddle_speed
    right_paddle.y += right_paddle_speed

    # Ограничение движений ракеток по вертикали (чтобы не выходили за границы окна)
    left_paddle.y = max(0, min(height - paddle_height, left_paddle.y))
    right_paddle.y = max(0, min(height - paddle_height, right_paddle.y))


# Функция для перемещения мяча
def move_ball():
    global ball_speed, left_score, right_score
    ball.x += ball_speed[0]  # Обновляем позицию мяча по горизонтали
    ball.y += ball_speed[1]  # Обновляем позицию мяча по вертикали

    # Проверка столкновения мяча с верхней и нижней границами окна
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed[1] = -ball_speed[1]  # Меняем направление движения мяча по вертикали

    # Проверка столкновения мяча с ракетками
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]  # Меняем направление движения мяча по горизонтали

    # Проверка выхода мяча за левую границу
    if ball.left <= 0:
        right_score += 1  # Увеличиваем очки правого игрока
        reset_ball()  # Сбрасываем мяч

    # Проверка выхода мяча за правую границу
    if ball.right >= width:
        left_score += 1  # Увеличиваем очки левого игрока
        reset_ball()  # Сбрасываем мяч


# Функция для сброса мяча в центр экрана
def reset_ball():
    global ball_speed
    ball.x = width // 2 - ball_size // 2  # Устанавливаем мяч в центр по горизонтали
    ball.y = height // 2 - ball_size // 2  # Устанавливаем мяч в центр по вертикали
    ball_speed = [5, 5 if ball_speed[1] > 0 else -5]  # Восстанавливаем начальную скорость мяча


# Функция для отрисовки очков
def draw_score():
    left_text = font.render(str(left_score), True, white)  # Создаем текст с очками левого игрока
    screen.blit(left_text, (width // 4, 10))  # Отображаем текст на экране

    right_text = font.render(str(right_score), True, white)  # Создаем текст с очками правого игрока
    screen.blit(right_text, (3 * width // 4, 10))  # Отображаем текст на экране


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Завершаем работу Pygame
            sys.exit()  # Выходим из программы

    move_paddles()  # Перемещаем ракетки
    move_ball()  # Перемещаем мяч

    # Обновление экрана
    screen.fill(black)  # Заполняем экран черным цветом
    pygame.draw.rect(screen, white, left_paddle)  # Рисуем левую ракетку
    pygame.draw.rect(screen, white, right_paddle)  # Рисуем правую ракетку
    pygame.draw.ellipse(screen, white, ball)  # Рисуем мяч
    draw_score()  # Отображаем очки
    pygame.display.flip()  # Обновляем экран
    clock.tick(fps)  # Ограничиваем частоту кадров
