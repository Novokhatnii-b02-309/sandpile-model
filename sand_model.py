import pygame
import numpy as np

from sandpile_func import *
from sandpile_constants import *

def simulation():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED|pygame.RESIZABLE)


    #двумерный массив для записи количества песчтнок в клетке
    sandpiles = np.zeros((WIDTH, HEIGHT), dtype=np.uint32)

    #помещаем в центральную клетку много песчинок
    sandpiles[HEIGHT // 2][WIDTH // 2] = 3e6

    finished = False

    screen.fill(WHITE)

    while not finished:
        draw(screen, sandpiles)

        pygame.display.update()

        #создаём массив, в который будем записывать состояние после рассыпания; нужен для симметричного процесса отрисоки
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
    pygame.quit()