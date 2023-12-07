import pygame
import numpy as np
import queue

from sandpile_func import *
from sandpile_constants import *


def simulation(simulation_width, simulation_height, topple_type, sandpiles, colors, control_queue):
    screen = pygame.display.set_mode((simulation_width, simulation_height), pygame.SCALED|pygame.RESIZABLE)

    finished = False
    running = True

    if topple_type == 1:
        N = 4 # количество песчинок, при котором происходит обвал
    elif topple_type == 2:
        N = 8

    screen.fill(WHITE)

    while not finished:
        if running:
            draw(screen, sandpiles, simulation_width, simulation_height, topple_type, colors)

            pygame.display.update()

            #создаём массив, в который будем записывать состояние после рассыпания; нужен для симметричного процесса отрисоки
            nextsandpiles = np.zeros((simulation_height, simulation_width), dtype=np.uint32)

            for i in range(simulation_height):
                for j in range(simulation_width):
                    num = sandpiles[i][j]
                    if num < N:
                        nextsandpiles[i][j] += num
                    else:
                        set_topple_function(nextsandpiles, i, j, num, topple_type, simulation_width, simulation_height)

            sandpiles = nextsandpiles

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                put_sand(sandpiles, x, y, 1e3)

        try:
            command = control_queue.get(block=False)
            if command == 'START':
                running = True
            elif command == 'QUIT':
                finished = True
            elif command == 'PAUSE':
                if running == True:
                    running = False
                elif running == False:
                    running = True
            elif command == 'SAVEFIG':
                pass

        except queue.Empty:
            pass

    pygame.quit()
