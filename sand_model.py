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
        if self.neutral_element_mode:
            self.neutral_element_run(control_queue, obj)

        else:
            self.normal_run(control_queue, obj)





    def step(self, control_queue, obj, screen):
        if self.running:
            if self.show or not self.toppled:
                draw(screen, self.sandpiles, self.width, self.height, self.how_topple, self.colors)

                pygame.display.update()

            # создаём массив, в который будем записывать состояние после рассыпания;
            # нужен для симметричного процесса отрисоки
            nextsandpiles = np.zeros((self.height, self.width), dtype=np.uint32)

            self.toppled = False
            for i in range(self.height):
                for j in range(self.width):
                    num = self.sandpiles[i][j]
                    if num < self.n:
                        nextsandpiles[i][j] += num
                    else:
                        set_topple_function(nextsandpiles, i, j, num, self.how_topple, self.width, self.height)
                        self.toppled = True

            self.sandpiles = nextsandpiles

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                put_sand(self.sandpiles, x, y, SANDPILES_PUT)

        try:
            command = control_queue.get(block=False)
            if command == 'START':
                self.running = True
            elif command == 'QUIT':
                if not obj.running_simulation:
                    self.finished = True
                else:
                    pass
            elif command == 'PAUSE':
                if self.running:
                    self.running = False
                elif not self.running:
                    self.running = True
            elif command == 'SAVEFIG':
                pass

        except queue.Empty:
            pass

    def normal_run(self, control_queue, obj):
        """Запуск симуляции"""

        screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE)

        self.finished = False
        self.running = True
        self.toppled = False

        if self.how_topple == 1:
            self.n = 4  # количество песчинок, при котором происходит обвал
        elif self.how_topple == 2:
            self.n = 8

        screen.fill(WHITE)

        while not self.finished:
            self.step(control_queue, obj, screen)

        pygame.quit()
        obj.running_simulation = False

    def neutral_element_run(self, control_queue, obj):
        screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE)

        self.finished = False
        self.running = True
        self.toppled = True

        if self.how_topple == 1:
            self.n = 4  # количество песчинок, при котором происходит обвал
        elif self.how_topple == 2:
            self.n = 8

        screen.fill(WHITE)

        sandpiles8 = np.zeros((self.height, self.width), dtype=np.uint32)
        for i in range(self.height):
            for j in range(self.width):
                sandpiles8[i][j] = 8
        self.sandpiles = sandpiles8

        while not self.finished and self.toppled:
            self.step(control_queue, obj, screen)

        self.sandpiles = sandpiles8 - self.sandpiles

        while not self.finished:
            self.step(control_queue, obj, screen)

        pygame.quit()
        obj.running_simulation = False
