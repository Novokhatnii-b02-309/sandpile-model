from sandpile_constants import *
import numpy as np


class Properties:
    '''
    Класс для хранения информации об окне симуляции
    '''

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.how_topple = 1 # 1 - для клссичсекого рассыпания, 2 - для рассыпания по фон Нейману
        self.sandpiles = np.zeros((self.height, self.width), dtype=np.uint32)
        self.colors = COLORFUL_CLAS

    def change_size(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

    def change_topple(self, value):
        self.how_topple = value

    def change_sandpiles(self, new_sandpiles):
        self.sandpiles = new_sandpiles

    def change_colors(self, value, new_color):
        self.colors = COLOR_TYPES[value][new_color]


def sandpiles_to_np(sandpiles, width, height):
    '''
    Переводит поле текста в np.array - поле размера width x height с песчинками
    На вход берёт поле текста с песчинками, введёнными в формате ('x','y','количество песчинок в клетке')
    возвращает поле np.array с песчинками
    '''

    sandpiles = sandpiles.split('\n')
    for i in range(len(sandpiles)-1, -1, -1):
        if sandpiles[i] == '':
            sandpiles.pop(i)
            continue
        sandpiles[i] = sandpiles[i].split(',')
        sandpiles[i] = list(map(int, sandpiles[i]))

    new_sandpiles = np.zeros((height, width), dtype=np.uint32)
    for sand in sandpiles:
        new_sandpiles[sand[1]][sand[0]] = sand[2]
    return(new_sandpiles)


def color(cell, value, colors):
    '''
    В зависимости от количесива песчинок возвращает цвет клетки
    '''

    if cell == 0:
        return WHITE
    elif value == 1:
        if cell < 4:
            return colors[cell-1]
        else:
            return colors[3]
    else:
        if cell < 8:
            return colors[cell-1]
        else:
            return colors[7]


def draw(screen, sandpiles, width, height, value, colors):
    '''
    Последовательная отрисовка массива с песчинками
    '''

    for i in range(height):
        for j in range(width):
            # canvas.create_rectangle(j, i, (j+1), (i+1), fill=color(sandpiles[i][j]), outline='')
            screen.set_at((j, i), color(sandpiles[i][j], value, colors))
    # canvas.update()


def topple(sandpiles, i, j, num, width, height):
    '''
    Рассыпание песчинок по классическим правилам
    '''

    sandpiles[i][j] += num - 4
    if j - 1 >= 0:
        sandpiles[i][j - 1] += 1
    if j + 1 <= width - 1:
        sandpiles[i][j + 1] += 1
    if i - 1 >= 0:
        sandpiles[i - 1][j] += 1
    if i + 1 <= height - 1:
        sandpiles[i + 1][j] += 1
    return sandpiles

def topple_neumann(sandpiles, i, j, num, width, height):
    '''
    Рассыпание песчинок по окрестности фон Неймана
    '''

    sandpiles[i][j] += num - 8
    for s in range(-1, 2):
        for t in range(-1, 2):
            if s == 0 and t == 0:
                continue
            else:
                if 0 <= i + s <= height - 1 and 0 <= j + t <= width - 1:
                    sandpiles[i + s][j + t] += 1
    return sandpiles

def set_topple_function(sandpiles, i, j, num, value, width, height):
    '''
    По значению value определяет какой тип рассыпания должен быть в симуляции
    '''

    if value == 1:
        return topple(sandpiles, i, j, num, width, height)
    elif value == 2:
        return topple_neumann(sandpiles, i, j, num, width, height)


def put_sand(sandpiles, x, y, amount):
    '''
    Добавляет в клетку (x, y) amount песчинок
    '''

    sandpiles[y][x] += amount
    return sandpiles
