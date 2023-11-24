from tkinter import *
import time
from tkinter.messagebox import *
from sandpile_constants import *


class Options:
    '''Опции на главном экране'''
    pass


def size_options():
    '''Настройки размеров для симуляции'''
    win_options = Toplevel()
    win_options.resizable(width=False, height=False)
    win_options.title('Настройки размеров')

    def def_size():
        global WIDTH
        global HEIGHT
        value = entry.get()
        value = value.split(', ')
        value = list(map(int, value))
        WIDTH = value[0]
        HEIGHT = value[1]


    var = StringVar()
    entry = Entry(win_options, width=30, font='Ubuntu, 12', bd=3, relief=SUNKEN, textvariable=var)

    label = Label(win_options, text='Введите размер поля в виде ***, ***')

    button = Button(win_options, text="Настроить размер", command=def_size)

    entry.pack()
    label.pack()
    button.pack()


def about():
    '''Вывод информации о программе в отдельном окне'''
    win_about = Toplevel()
    win_about.resizable(width=False, height=False)
    win_about.title('О программе')
    about_text = '''Модель песчаной кучи 
    Эта программа моделирует поведение песчаной кучи. 
    Подробнее: https://ru.m.wikipedia.org/wiki/Модель_песчаной_кучи
    Программа создана учениками Б02-309 Артёмом Новохатним и Буторином Глебом'''
    label = Label(win_about, width=70, height=10, bg="white",
                fg='black', text=about_text)
    label.pack()


def help():
    '''Вывод помощи в отдельном окне'''
    win_help = Toplevel()
    win_help.resizable(width=False, height=False)
    win_help.title('Помощь')
    label = Label(win_help, width=25, height=5, bg="white",
                fg='black', text='Помощь')
    # FIXME
    label.pack()


def start_simulation():
    global running_simulation
    running_simulation = True
    #run_simulation()


def end_simulation():
    global running_simulation
    running_simulation = False


def start_main_window():
    '''Инициализация основного окна программы'''
    global win
    #global canvas

    win = Tk()
    win.title('Sandpile model')
    win.geometry('500x500')

    m = Menu(win)
    win.config(menu=m)

    settings_menu = Menu(m, tearoff=0)
    m.add_cascade(label='Настройки', menu=settings_menu)
    settings_menu.add_command(label='Размер поля', command=size_options)

    m.add_command(label='Помощь', command=help)

    m.add_command(label='О программе', command=about)

    #canvas = Canvas(win, bg="white", width=WIDTH, height=HEIGHT)
    #canvas.grid(row=0, columnspan=2)
    #canvas.update()

    button_start = Button(win, text="Начать симуляцию", command=start_simulation)
    button_finish = Button(win, text="Закончить симуляцию", command=end_simulation)

    button_start.grid(row=1, column=1, padx=1, pady=1)
    button_finish.grid(row=1, column=2, padx=1, pady=1)
    win.mainloop()


#start_main_window()