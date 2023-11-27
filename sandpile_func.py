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


def draw(screen, sandpiles, width, height):
    '''
    Последовательная отрисовка массива с песчинками
    '''

    for i in range(height):
        for j in range(width):
            # canvas.create_rectangle(j, i, (j+1), (i+1), fill=color(sandpiles[i][j]), outline='')
            screen.set_at((j, i), color(sandpiles[i][j]))
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