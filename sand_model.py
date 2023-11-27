import pygame
import numpy as np

from sandpile_func import *
from sandpile_constants import *

def simulation(simulation_width, simulation_height):
    screen = pygame.display.set_mode((simulation_width, simulation_height), pygame.SCALED|pygame.RESIZABLE)


    #двумерный массив для записи количества песчтнок в клетке
    sandpiles = np.zeros((simulation_width, simulation_height), dtype=np.uint32)

    #помещаем в центральную клетку много песчинок
    sandpiles[simulation_height // 2][simulation_width // 2] = 3e4

    finished = False

    screen.fill(WHITE)

    while not finished:
        draw(screen, sandpiles, simulation_width, simulation_height)

        pygame.display.update()

        #создаём массив, в который будем записывать состояние после рассыпания; нужен для симметричного процесса отрисоки
        nextsandpiles = np.zeros((simulation_width, simulation_height), dtype=np.uint32)

        for i in range(simulation_height):
            for j in range(simulation_width):
                num = sandpiles[i][j]
                if num <= 7:
                    nextsandpiles[i][j] += num
                else:
                    nextsandpiles = topple_neumann(nextsandpiles, i, j, num)

        sandpiles = nextsandpiles

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
    pygame.quit()