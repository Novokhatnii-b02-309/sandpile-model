from sandpile_constants import *

class Properties:
    '''
    Класс для хранения информации об окне симуляции
    '''

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.how_topple = 1 # 1 - для клссичсекого рассыпания, 2 - для рассыпания по фон Нейману

    def change_size(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

    def change_topple(self, value):
        self.how_topple = value

def color(cell, value):
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
        if value == 1:
            return RED
        elif value == 2:
            if cell == 4:
                return BLUE
            elif cell == 5:
                return CYAN
            elif cell == 6:
                return MAGENTA
            elif cell == 7:
                return ORANGE
            else:
                return RED


def draw(screen, sandpiles, width, height, value):
    '''
    Последовательная отрисовка массива с песчинками
    '''

    for i in range(height):
        for j in range(width):
            # canvas.create_rectangle(j, i, (j+1), (i+1), fill=color(sandpiles[i][j]), outline='')
            screen.set_at((j, i), color(sandpiles[i][j], value))
    # canvas.update()


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

def topple_neumann(sandpiles, i, j, num):
    '''
    Рассыпание песчинок по окрестности фон Неймана
    '''

    sandpiles[i][j] += num - 8
    for s in range(-1, 2):
        for t in range(-1, 2):
            if s == 0 and t == 0:
                continue
            else:
                sandpiles[i + s][j+ t] += 1
    return sandpiles

def set_topple_function(sandpiles, i, j, num, value):
    '''
    По значению value определяет какой тип рассыпания должен быть в симуляции
    '''

    if value == 1:
        return topple(sandpiles, i, j, num)
    elif value == 2:
        return topple_neumann(sandpiles, i, j, num)

def put_sand(sandpiles, x, y, amount):
    '''
    Добавляет в клетку (x, y) amount песчинок
    '''

    sandpiles[y][x] += amount
    return sandpiles