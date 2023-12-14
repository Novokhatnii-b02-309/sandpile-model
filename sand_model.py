import pygame
import queue

from sandpile_func import *
from sandpile_constants import *


class Simulation(Properties):
    """Симуляция и её методы"""
    def __init__(self, properties):
        """Копирование атрибутов properties"""
        vars_properties = vars(properties)
        for key, value in vars_properties.items():
            setattr(self, key, value)

    def run(self, control_queue, obj):
        """Запуск симуляции"""

        screen = pygame.display.set_mode((self._width, self._height), pygame.SCALED | pygame.RESIZABLE)

        finished = False
        running = True

        if self._how_topple == 1:
            n = 4  # количество песчинок, при котором происходит обвал
        elif self._how_topple == 2:
            n = 8

        screen.fill(WHITE)
        toppled = False

        while not finished:
            if running:
                if self._show or not toppled:
                    draw(screen, self._sandpiles, self._width, self._height, self._how_topple, self._colors)

                    pygame.display.update()

            # создаём массив, в который будем записывать состояние после рассыпания;
            # нужен для симметричного процесса отрисоки
            nextsandpiles = np.zeros((self._height, self._width), dtype=np.uint32)

            toppled = False
            for i in range(self._height):
                for j in range(self._width):
                    num = self._sandpiles[i][j]
                    if num < n:
                        nextsandpiles[i][j] += num
                    else:
                        set_topple_function(nextsandpiles, i, j, num, self._how_topple, self._width, self._height)
                        toppled = True

            self._sandpiles = nextsandpiles

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    put_sand(self._sandpiles, x, y, SANDPILES_PUT)

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
