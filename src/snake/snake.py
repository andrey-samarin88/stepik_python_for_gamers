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
snake = [(100, 100), (90, 100), (80, 100)]
direction = "Right"
food = None
score = 0
game_over = False

# Главный цикл
root.mainloop()