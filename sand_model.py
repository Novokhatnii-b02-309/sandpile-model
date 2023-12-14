import pygame
import queue

from sandpile_func import *
from sandpile_constants import *


class Simulation(Properties):
    def __init__(self, properties, control_queue, obj):
        vars_properties = vars(properties)
        for key, value in vars_properties.items():
            setattr(self, key, value)

        screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE)

        finished = False
        running = True

        if self.how_topple == 1:
            n = 4  # количество песчинок, при котором происходит обвал
        elif self.how_topple == 2:
            n = 8

        screen.fill(WHITE)
        toppled = False

        while not finished:
            if running:
                if self.show or not toppled:
                    draw(screen, self.sandpiles, self.width, self.height, self.how_topple, self.colors)

                    pygame.display.update()

            # создаём массив, в который будем записывать состояние после рассыпания;
            # нужен для симметричного процесса отрисоки
            nextsandpiles = np.zeros((self.height, self.width), dtype=np.uint32)

            toppled = False
            for i in range(self.height):
                for j in range(self.width):
                    num = self.sandpiles[i][j]
                    if num < n:
                        nextsandpiles[i][j] += num
                    else:
                        set_topple_function(nextsandpiles, i, j, num, self.how_topple, self.width, self.height)
                        toppled = True

            self.sandpiles = nextsandpiles

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    put_sand(self.sandpiles, x, y, SANDPILES_PUT)

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
