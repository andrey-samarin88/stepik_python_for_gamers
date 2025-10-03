import tkinter as tk
import random

# Настройки игры
WIDTH = 400
HEIGHT = 400
DIRECTIONS = ["Up", "Down", "Left", "Right"]
CELL_SIZE = 10
DELAY = 100

# Главное окно
root = tk.Tk()
root.title("Змейка | Счет: 0")
root.resizable(False, False)


# Игровое поле
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

# Начальное состояние игры
#snake = [(100, 100), (90, 100), (80, 100)]
snake = []
direction = "Right"
score = 0
game_over = False


# Определение координат еды
def create_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)


food = create_food()


# Отрисовка еды на игровом поле
def draw_food():
    canvas.create_rectangle(
        food[0], food[1],
        food[0] + CELL_SIZE,
        food[1] + CELL_SIZE,
        fill="red"
    )


# Отрисовка змейки на игровом поле
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE,
            segment[1] + CELL_SIZE,
            fill="green",
            outline="darkgreen"
        )


# Движение змейки
def move_snake():
    head_x, head_y = snake[0]
    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)
    snake.insert(0, new_head)
    if not check_food_collision():
        snake.pop()


# Обработка нажатия клавиш
def on_key_press(event):
    global direction
    key = event.keysym
    if key in DIRECTIONS:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Uo" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
    elif key =='space' and game_over:
        restart_game()


root.bind("<KeyPress>", on_key_press)


# Проверяем съедена ли еда
def check_food_collision():
    global food, score
    if snake[0] == food:
        score += 1
        food = create_food()
        return True
    return False


# Обновление заголовка
def update_title():
    root.title(f"Змейка | Счёт: {score}")


# Проверка на столкновение со стенами
def check_wall_collision():
    head_x, head_y = snake[0]
    return (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT)


# Завершение игры
def end_game():
    global game_over
    game_over = True
    canvas.create_text(
        WIDTH // 2, HEIGHT // 2,
        text=f"Игра окончена! Счёт: {score}",
        fill="white",
        font=("Roboto", 24)
    )


# Перезапуск игры
def restart_game():
    global snake, direction, food, score, game_over

    # Начальное положение змейки
    #snake = [(100, 100), (90, 100), (80, 100)]
    snake = create_snake()
    direction = "Right"

    # Новая еда
    food = create_food()

    # Сброс счёта и статуса
    score = 0
    game_over = False

    # Очистим холст и обновим
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()

    # Перезапускаем игровой цикл
    root.after(DELAY, game_loop)


# Проверка самостолкновения
def check_self_collision():
    return snake[0] in snake[1:]


# Создание змейки
def create_snake():
    # Вычисляем максимальное значение по X и Y,
    # чтобы вся змейка (3 клетки) уместилась в пределах поля
    max_x = (WIDTH // CELL_SIZE) - 3
    max_y = (HEIGHT // CELL_SIZE) - 1

    # Случайная позиция головы змейки
    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE

    # Возвращаем список из 3 сегментов змейки, направленных вправо
    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]

# Игровой цикл
def game_loop():
    global snake, food, score
    if game_over:
        return
    move_snake()
    if check_wall_collision() or check_self_collision():
        end_game()
        return
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)


# Запуск игрового цикла
snake = create_snake()
draw_food()
draw_snake()
root.after(DELAY, game_loop)

# Главный цикл окна
root.mainloop()