from tkinter import ttk
from tkinter import *
import time
from tkinter.messagebox import *
from sandpile_constants import *
from tkinter import ttk


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

'''
def read_vars():
    width_var.get()
    height_var.get()
'''


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
    win.geometry('600x500')
    win.maxsize(900, 600)
    win.configure(bg='white')

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

    label_param = Label(win, text='Параметры', bg='white')
    label_size = Label(win, text='Размеры', font=('Arial', 20), bg='white')
    label_width = Label(win, text='Ширина:', bg='white')
    label_height = Label(win, text='Высота:', bg='white')
    label_sandpiles = Label(win, text='Начальное положение песчинок', bg='white')
    label_type_model = Label(win, text='Тип модели:', bg='white')
    label_show = Label(win, text='Показывать процесс распада:', bg='white')
    label_colors = Label(win, text='Цвета:', bg='white')
    #separator = ttk.Separator(win, orient='horizontal')
    #separator.pack(side='left', fill='x')

    width_var = StringVar()
    width_entry = Entry(win, width=30, font='Ubuntu, 12', bd=3, textvariable=width_var)
    height_var = StringVar()
    height_entry = Entry(win, width=30, font='Ubuntu, 12', bd=3, textvariable=height_var)

    type_var = StringVar()
    type_var.set('division_4')
    btn_div_4 = Radiobutton(win, text='4-разделение', variable=type_var, value='division_4', bg='white')
    btn_div_8 = Radiobutton(win, text='8-разделение', variable=type_var, value='division_8', bg='white')

    show_var = BooleanVar()
    show_var.set(True)
    btn_show = Radiobutton(win, text='Да', variable=show_var, value=True, bg='white')
    btn_not_show = Radiobutton(win, text='Нет', variable=show_var, value=False, bg='white')

    '''
    frame_left = []
    for i in range(9):
        frame_left.append(ttk.Frame(borderwidth=1, relief=SOLID, padding=[1, 1, 1, 1]))
        frame_left[i].grid(row=i, column=0)
    '''

    label_param.grid(row=0, column=0)
    label_size.grid(row=1, column=0)
    label_width.grid(row=2, column=0)
    label_height.grid(row=3, column=0)
    label_sandpiles.grid(row=4, column=0)
    #В пятой строке вводятся песчинки
    label_type_model.grid(row=6, column=0)
    label_show.grid(row=7, column=0)
    label_colors.grid(row=8, column=0)

    width_entry.grid(row=2, column=1)
    height_entry.grid(row=3, column=1)

    btn_div_4.grid(row=6, column=1)
    btn_div_8.grid(row=6, column=2)

    btn_show.grid(row=7, column=1)
    btn_not_show.grid(row=7, column=2)


    '''
    button_start = Button(win, text="Начать симуляцию", command=start_simulation)
    button_finish = Button(win, text="Закончить симуляцию", command=end_simulation)

    button_start.grid(row=1, column=1, padx=10, pady=5,)
    button_finish.grid(row=1, column=2, padx=1, pady=1)
    '''
    win.mainloop()


start_main_window()
