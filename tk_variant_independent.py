from tkinter import *
import time
from tkinter.messagebox import *

'''WHITE = 0xFFFFFF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
PURPLE = 0x800080
RED = 0xFF0000'''
WIDTH = 100
HEIGHT = 100

WHITE = 'white'
GREEN = 'green'
PURPLE = 'purple'
YELLOW = 'yellow'
RED = 'red'


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

def draw(canvas, sandpiles):
    '''
    Последовательная отрисовка массива с песчинками
    '''
    for i in range(HEIGHT):
        for j in range(WIDTH):
            canvas.create_rectangle(j, i, (j+1), (i+1), fill=color(sandpiles[i][j]), outline='')
    canvas.update()

def size_options():
    win2 = Tk()
    win2.title('Настройки размеров')

    def def_size():
        value = entry.get()
        value = value.split(', ')
        value = list(map(int, value))
        print(value)
        canvas.configure(width=value[0], height=value[1])

    var = StringVar()
    entry = Entry(win2, width=30, font='Ubuntu, 12', bd=3, relief=SUNKEN, textvariable=var)

    label = Label(win2, text='Введите размер поля в виде ***, ***')

    button = Button(win2, text="Настроить размер", command=def_size)

    entry.pack()
    label.pack()
    button.pack()

def start_simulation():
    global running_simulation
    running_simulation = True
    run_simulation()

def end_simulation():
    global running_simulation
    running_simulation = False


def start_main_window():
    global win
    global canvas

    win = Tk()
    win.title('Sandpile model')
    win.geometry('1000x1000')

    m = Menu(win)
    win.config(menu=m)

    item1 = Menu(m, tearoff=0)
    m.add_cascade(label='Настройки', menu=item1)
    item1.add_command(label='Размер поля', command=size_options)

    canvas = Canvas(win, bg="white", width=WIDTH, height=HEIGHT)
    canvas.grid(row=0, columnspan=2)
    canvas.update()

    button_start = Button(win, text="Начать симуляцию", command=start_simulation)
    button_finish = Button(win, text="Закончить симуляцию", command=end_simulation)

    button_start.grid(row=1, column=1, padx=1, pady=1)
    button_finish.grid(row=1, column=2, padx=1, pady=1)


sandpiles = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]
sandpiles[HEIGHT // 2][WIDTH // 2] = 1000


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


def run_simulation():
    global sandpiles
    while running_simulation:
        canvas.delete('all')
        nextsandpiles = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                num = sandpiles[i][j]
                if num <= 3:
                    nextsandpiles[i][j] += num
                else:
                    nextsandpiles = topple(nextsandpiles, i, j, num)

        sandpiles = nextsandpiles
        draw(canvas, sandpiles)
        #time.sleep(0.03)


finished = False
running_simulation = False
start_main_window()
finished = True


win.mainloop()

