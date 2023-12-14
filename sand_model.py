import pygame
import queue

from sandpile_func import *
from sandpile_constants import *


def simulation(simulation_width, simulation_height, topple_type, sandpiles, colors, show, control_queue, obj):
    screen = pygame.display.set_mode((simulation_width, simulation_height), pygame.SCALED | pygame.RESIZABLE)

    finished = False
    running = True

    if topple_type == 1:
        n = 4  # количество песчинок, при котором происходит обвал
    elif topple_type == 2:
        n = 8

    screen.fill(WHITE)
    toppled = False

    while not finished:
        if running:
            if show or not toppled:
                draw(screen, sandpiles, simulation_width, simulation_height, topple_type, colors)

                pygame.display.update()

        # создаём массив, в который будем записывать состояние после рассыпания;
        # нужен для симметричного процесса отрисоки
        nextsandpiles = np.zeros((simulation_height, simulation_width), dtype=np.uint32)

        toppled = False
        for i in range(simulation_height):
            for j in range(simulation_width):
                num = sandpiles[i][j]
                if num < n:
                    nextsandpiles[i][j] += num
                else:
                    set_topple_function(nextsandpiles, i, j, num, topple_type, simulation_width, simulation_height)
                    toppled = True

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
                if not obj.running_simulation:
                    finished = True
                else:
                    pass
            elif command == 'PAUSE':
                if running:
                    running = False
                elif not running:
                    running = True
            elif command == 'SAVEFIG':
                pass

        except queue.Empty:
            pass

    pygame.quit()
    obj.running_simulation = False
