import pygame
import numpy as np

WHITE = 0xFFFFFF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
PURPLE = 0x800080
RED = 0xFF0000

WIDTH = 200
HEIGHT = 200

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED|pygame.RESIZABLE)


#двумерный массив для записи количества песчтнок в клетке
sandpiles = np.zeros((WIDTH, HEIGHT), dtype=np.uint32)

#помещаем в центральную клетку много песчинок
sandpiles[HEIGHT // 2][WIDTH // 2] = 3e6

def color(cell):
    '''
    В зависимости от количесива песчинок возвращает цвет клетки
    '''

    if cell == 0:
        return WHITE
    elif cell == 1:
        return GREEN
    elif cell == 2:
        return PURPLE
    elif cell == 3:
        return YELLOW
    else:
        return RED

def draw(screen, sandpiles):
    '''
    Последовательная отрисовка массива с песчинками
    '''
    
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pygame.draw.rect(screen, color(sandpiles[i][j]), [i, j, 1, 1])
            # screen.set_at((j, i), color(sandpiles[i][j]))

def topple(sandpiles, i, j, num):
    '''
    Рассыпание песчинок по классическим правилам
    '''

    sandpiles[i][j] += num - 4
    if j - 1 >= 0:
        sandpiles[i][j - 1] += 1
    if j + 1 <= WIDTH - 1:
        sandpiles[i][j + 1] += 1
    if i - 1 >= 0:
        sandpiles[i - 1][j] += 1
    if i + 1 <= HEIGHT - 1:
        sandpiles[i + 1][j] += 1
    return sandpiles

finished = False

screen.fill(WHITE)

while not finished:
    draw(screen, sandpiles)

    pygame.display.update()

    #создаём массив, в который будем записывать сотстояние после рассыпания; нужен для симметричного процесса отрисоки
    nextsandpiles = np.zeros((WIDTH, HEIGHT), dtype=np.uint32)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            num = sandpiles[i][j]
            if num <= 3:
                nextsandpiles[i][j] += num
            else:
                nextsandpiles = topple(nextsandpiles, i, j, num)

    sandpiles = nextsandpiles

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True