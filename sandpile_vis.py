from tkinter import *
import time
from tkinter.messagebox import *
from tkinter import ttk

from sandpile_constants import *
import sand_model
import sandpile_func

def size_options():
    '''Настройки размеров для симуляции'''
    win_options = Toplevel()
    win_options.resizable(width=False, height=False)
    win_options.title('Настройки размеров')

    def def_size():
        value = entry.get()
        value = value.split(', ')
        value = list(map(int, value))
        simulation_prop.change_size(value[0], value[1])

    var = StringVar()
    entry = Entry(win_options, width=30, font='Ubuntu, 12', bd=3, relief=SUNKEN, textvariable=var)

    label = Label(win_options, text='Введите размер поля в виде ***, ***')

    button = Button(win_options, text="Настроить размер", command=def_size)

    entry.pack()
    label.pack()
    button.pack()

def set_topple(value):
    simulation_prop.change_topple(value)

def about():
    '''Вывод информации о программе в отдельном окне'''
    win_about = Toplevel()
    win_about.resizable(width=False, height=False)
    win_about.title('О программе')
    about_text = '''Модель песчаной кучи 
    Эта программа моделирует поведение песчаной кучи. 
    Подробнее: https://ru.m.wikipedia.org/wiki/Модель_песчаной_кучи
    Программа создана учениками Б02-309 Артёмом Новохатним и Буторином Глебом'''
    label = Label(win_about, width=70, height=10, bg="white", fg='black', text=about_text)
    label.pack()


def help():
    '''Вывод помощи в отдельном окне'''
    win_help = Toplevel()
    win_help.resizable(width=False, height=False)
    win_help.title('Помощь')
    label = Label(win_help, width=25, height=5, bg="white", fg='black', text='Помощь')
    # FIXME
    label.pack()

def read_vars():
    # print(width_entry.get())
    # FIXME как указать на локальный объект (entry) у функции start_main_window()?
    pass


def start_simulation():
    global running_simulation
    running_simulation = True
    read_vars()
    sand_model.simulation(simulation_prop.width, simulation_prop.height, simulation_prop.how_topple)


def end_simulation():
    global running_simulation
    running_simulation = False


def save_pic():
    pass
    # FIXME


def main_win_frame(win, x, y, width, height):
    self = Frame(win, bg='white', borderwidth=1, relief=SOLID)
    # убрал (, width=width, height=height)
    #self.pack_propagate(False)
    self.place(relx=x, rely=y, relwidth=width, relheight=height)
    return(self)


def start_main_window(win):
    '''Инициализация основного окна программы'''
    # global canvas
    global win_height
    global win_width
    global simulation_prop # класс, в котором будет храниться информация об окне симуляции
    win_width = 900
    win_height = 660
    simulation_prop = sandpile_func.Properties()

    win.title('Sandpile model')
    win.geometry(str(win_width)+'x'+ str(win_height)+'+'+'300+300')
    win.resizable(False, False)
    win.configure(bg='white')

    m = Menu(win)
    win.config(menu=m)

    settings_menu = Menu(m, tearoff=0)
    m.add_cascade(label='Настройки', menu=settings_menu)
    settings_menu.add_command(label='Размер поля', command=size_options)

    m.add_command(label='Помощь', command=help)

    m.add_command(label='О программе', command=about)

    # canvas = Canvas(win, bg="white", width=WIDTH, height=HEIGHT)
    # canvas.grid(row=0, columnspan=2)
    # canvas.update()

    frames_xywh_left = [(0, 0, 1/2, 1/11), (0, 1/11, 1/2, 1/11), (0, 2/11, 1/2, 1/11), (0, 3/11, 1/2, 1/11),
                        (0, 4/11, 1/2, 4/11), (0, 8/11, 1/2, 1/11), (0, 9/11, 1/2, 1/11), (0, 10/11, 1/2, 1/11)]
    frames_xywh_right = [(1/2, 0, 1/2, 1/11), (1/2, 1/11, 1/2, 1/11), (1/2, 2/11, 1/2, 5/11), (1/2, 7/11, 1/2, 1/11),
                         (1/2, 8/11, 1/2, 3/11)]

    frame_left = []

    for i in range(len(frames_xywh_left)):
        frame_left.append(main_win_frame(win, frames_xywh_left[i][0], frames_xywh_left[i][1],
                                         frames_xywh_left[i][2], frames_xywh_left[i][3]))

    frame_right = []

    for i in range(len(frames_xywh_right)):
        frame_right.append(main_win_frame(win, frames_xywh_right[i][0], frames_xywh_right[i][1],
                                          frames_xywh_right[i][2], frames_xywh_right[i][3]))

    label_param = Label(frame_left[0], text='Параметры', bg='white')
    label_size = Label(frame_left[1], text='Размеры', bg='white')
    label_width = Label(frame_left[2], text='Ширина:', bg='white')
    label_height = Label(frame_left[3], text='Высота:', bg='white')
    label_sandpiles = Label(frame_left[4], text='Начальное положение песчинок', bg='white')
    label_type_model = Label(frame_left[5], text='Тип модели:', bg='white')
    label_show = Label(frame_left[6], text='Показывать процесс распада:', bg='white')
    label_colors = Label(frame_left[7], text='Цвета:', bg='white')

    label_buttons = Label(frame_right[0], text='Симуляция', bg='white')
    label_picture = Label(frame_right[2], text='Здесь должна быть картинка', bg='white')
    label_output = Label(frame_right[4], text='Здесь должно быть поле вывода', bg='white')
    # separator = ttk.Separator(win, orient='horizontal')
    # separator.pack(side='left', fill='x')

    width_entry = Entry(frame_left[2], width=30, font='Ubuntu, 12', bd=3)
    height_entry = Entry(frame_left[3], width=30, font='Ubuntu, 12', bd=3)

    sandpiles_entry = Text(frame_left[4], width=40, height=30, font='Ubuntu, 12', bd=3)
    scroll = ttk.Scrollbar(frame_left[4], orient="vertical", command=sandpiles_entry.yview)

    # FIXME
    type_var = StringVar()
    type_var.set('division_4')
    btn_div_4 = Radiobutton(frame_left[5], text='4-разделение', variable=type_var, value='division_4', command=set_topple(1), bg='white')
    btn_div_8 = Radiobutton(frame_left[5], text='8-разделение', variable=type_var, value='division_8', command=set_topple(2), bg='white')

    show_var = BooleanVar()
    show_var.set(True)
    btn_show = Radiobutton(frame_left[6], text='Да', variable=show_var, value=True, bg='white')
    btn_not_show = Radiobutton(frame_left[6], text='Нет', variable=show_var, value=False, bg='white')

    btn_start = Button(frame_right[1], text="Начать симуляцию", command=start_simulation)
    btn_finish = Button(frame_right[1], text="Закончить симуляцию", command=end_simulation)
    btn_save_pic = Button(frame_right[3], text="Сохранить картинку", command=save_pic)

    label_param.pack()
    label_size.pack()
    label_width.pack()
    label_height.pack()
    label_sandpiles.pack()
    # В пятой строке вводятся песчинки
    label_type_model.pack()
    label_show.pack()
    label_colors.pack()

    label_buttons.pack()
    label_picture.pack()
    label_output.pack()

    width_entry.pack()
    height_entry.pack()

    sandpiles_entry.pack(side=LEFT, padx=10)
    scroll.pack(side=LEFT, fill=Y)

    sandpiles_entry.config(yscrollcommand=scroll.set)

    btn_div_4.pack()
    btn_div_8.pack()

    btn_start.pack()
    btn_finish.pack()
    btn_save_pic.pack()

    btn_show.pack()
    btn_not_show.pack()

    win.mainloop()


# start_main_window()
