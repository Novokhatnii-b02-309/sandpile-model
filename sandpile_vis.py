from tkinter import *
import time
from tkinter.messagebox import *
from tkinter import ttk
from PIL import ImageTk, Image
from threading import Thread
import queue

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
    help_text = '''Помощь
    Поле ввода ширина: задаёт длину поля по горизонтали в клетках
    
    Поле ввода высота: задаёт длину поля по вертикальной оси в клетках
    
    Начальное поле песчинок: задаёт начальное положение песчинок, 
    x,y,n - добавляет n песчинок в клетку x,y
    клетки добавляются в каждой строке отдельно
    x - координата в клетках по горизонтали, ось вправо
    y - по вертикали, ось вниз
    0,0 - левая верхняя клетка
    Пример ввода:
    0,0,100
    10,10,20
    
    Показывать процесс распада: 
    показывать ли промежуточные шаги от начального состояния до разваленного
    
    Цвета: задаёт цвета клеток с песчинками
    
    Начать симуляцию:
    Создаёт новую симуляцию/продолжает существующую
    
    Закончить симуляцию:
    Останавливает текущую симуляцию
    '''
    label = Label(win_help, bg="white", fg='black', text=help_text)
    # FIXME
    label.pack()


def main_win_frame(win, x, y, width, height):
    '''Создаёт ячейку для виджета в главном окне'''
    global win_height
    global win_width
    self = Frame(win, bg='white', relief=SOLID, highlightbackground='gray', highlightthickness=1,
                 width=width*win_width, height=height*win_height)
    # убрал (, width=width, height=height)
    self.grid_propagate(False)
    self.place(relx=x, rely=y, relwidth=width, relheight=height)
    return(self)


def start_main_window(win):
    '''Инициализация основного окна программы'''

    def read_vars():
        '''Данная функция считывает переменные из строк и кнопок и устанавливает параметры симуляции'''
        width = int(width_entry.get())
        height = int(height_entry.get())
        simulation_prop.change_size(width, height)
        simulation_prop.change_topple(type_var.get())

        sandpiles = sandpiles_entry.get(1.0, END)
        sandpiles = sandpile_func.sandpiles_to_np(sandpiles, width, height)
        simulation_prop.change_sandpiles(sandpiles)

        simulation_prop.change_colors(type_var.get(), color_var.get())

    def start_simulation(control_queue):
        global running_simulation
        try:
            text_output.configure(foreground='black', text='Запуск симуляции')
            win.update()
            read_vars()
            running_simulation = True
            print(running_simulation)
            pygame_thread = Thread(target=sand_model.simulation, args=(simulation_prop.width, simulation_prop.height,
                                  simulation_prop.how_topple, simulation_prop.sandpiles, simulation_prop.colors, control_queue,))
            # sand_model.simulation(simulation_prop.width, simulation_prop.height,
            #                       simulation_prop.how_topple, simulation_prop.sandpiles, simulation_prop.colors)
            pygame_thread.start()
            running_simulation = False
        except:
            text_output.configure(foreground='red', text='Ошибка')

    def end_simulation():
        global running_simulation
        running_simulation = False

    def save_pic():
        pass
        # FIXME

    def send_command(command, control_queue, running_simulation):
        control_queue.put(command)
        if command == 'START' and running_simulation == False:
            start_simulation(control_queue)
        elif command == 'QUIT':
            end_simulation()

    global win_height
    global win_width
    global simulation_prop # класс, в котором будет храниться информация об окне симуляции
    global running_simulation
    win_width = 900
    win_height = 640

    win.minsize(900, 640)

    simulation_prop = sandpile_func.Properties()
    running_simulation = False

    win.title('Sandpile model')
    win.geometry(str(win_width)+'x'+ str(win_height)+'+'+'300+0')
    #win.resizable(False, False)
    win.configure(bg='white')

    control_queue = queue.Queue()

    m = Menu(win)
    win.config(menu=m)

    settings_menu = Menu(m, tearoff=0)
    m.add_cascade(label='Настройки', menu=settings_menu)
    settings_menu.add_command(label='Размер поля', command=size_options)

    m.add_command(label='Помощь', command=help)

    m.add_command(label='О программе', command=about)

    frame_top = main_win_frame(win, 0, 0, 1, 2/12)
    frame_top.configure(bg='yellow')

    frames_xywh_left = [(0, 2/12, 1/2, 1/12), (0, 3/12, 1/2, 1/12), (0, 4/12, 1/2, 1/12),
                        (0, 5/12, 1/2, 4/12), (0, 9/12, 1/2, 1/12), (0, 10/12, 1/2, 1/12), (0, 11/12, 1/2, 1/12)]
    frames_xywh_right = [(1/2, 2/12, 1/2, 1/12), (1/2, 3/12, 1/2, 5/12), (1/2, 8/12, 1/2, 1/12),
                         (1/2, 9/12, 1/2, 3/12)]

    #Делим экран на части справа и слева
    frame_left = []

    for i in range(len(frames_xywh_left)):
        frame_left.append(main_win_frame(win, frames_xywh_left[i][0], frames_xywh_left[i][1],
                                         frames_xywh_left[i][2], frames_xywh_left[i][3]))

    frame_right = []

    for i in range(len(frames_xywh_right)):
        frame_right.append(main_win_frame(win, frames_xywh_right[i][0], frames_xywh_right[i][1],
                                          frames_xywh_right[i][2], frames_xywh_right[i][3]))

    # Заголовок
    label_title = Label(frame_top, text='Модель песчаной кучи', bg='yellow',
                        foreground='black', font=('TkHeadingFont', 26))
    img = ImageTk.PhotoImage(Image.open("images/title_image.png"))
    panel = Label(frame_top, image=img, bg='yellow')




    #Виджеты текста слева
    label_param = Label(frame_left[0], text='Параметры', bg='white', font=('TkHeadingFont', 15))
    label_width = Label(frame_left[1], text='Ширина:', bg='white')
    label_height = Label(frame_left[2], text='Высота:', bg='white')
    label_sandpiles = Label(frame_left[3], text='Начальное положение песчинок', bg='white')
    label_type_model = Label(frame_left[4], text='Тип модели:', bg='white')
    label_show = Label(frame_left[5], text='Показывать процесс распада:', bg='white')
    label_colors = Label(frame_left[6], text='Цвета:', bg='white')

    # Виджеты текста справа
    #label_buttons = Label(frame_right[0], text='Симуляция', bg='white')
    label_picture = Label(frame_right[1], text='Здесь должна быть картинка', bg='white')
    label_output = Label(frame_right[3], text='Поле вывода', bg='white')
    # separator = ttk.Separator(win, orient='horizontal')
    # separator.pack(side='left', fill='x')

    # Поля ввода длины, ширины и начального положения песчинок
    width_entry = Entry(frame_left[1], width=30, font='Ubuntu, 12', bd=3)
    width_entry.insert(0, WIDTH)
    height_entry = Entry(frame_left[2], width=30, font='Ubuntu, 12', bd=3)
    height_entry.insert(0, HEIGHT)

    sandpiles_entry = Text(frame_left[3], width=40, height=30, font='Ubuntu, 12', bd=3)
    sandpiles_entry.insert(1.0, str(WIDTH//2)+','+str(HEIGHT//2)+','+str(SANDPILES))
    scroll = ttk.Scrollbar(frame_left[3], orient="vertical", command=sandpiles_entry.yview)

    # Выбор типа разделения
    type_var = IntVar()
    type_var.set(1)
    btn_div_4 = Radiobutton(frame_left[4], text='4-разделение', variable=type_var, value=1, bg='white')
    btn_div_8 = Radiobutton(frame_left[4], text='8-разделение', variable=type_var, value=2, bg='white')

    # Выбор показывать/не показывать шаги симуляции
    show_var = BooleanVar()
    show_var.set(True)
    btn_show = Radiobutton(frame_left[5], text='Да', variable=show_var, value=True, bg='white')
    btn_not_show = Radiobutton(frame_left[5], text='Нет', variable=show_var, value=False, bg='white')


    # Выбор цветов
    color_var = StringVar()
    color_var.set('colorful')
    btn_colorful = Radiobutton(frame_left[6], text='Разноцветный', variable=color_var, value='colorful', bg='white')
    btn_red = Radiobutton(frame_left[6], text='Красный', variable=color_var, value='red', bg='white')
    btn_green = Radiobutton(frame_left[6], text='Зелёный', variable=color_var, value='green', bg='white')
    btn_blue = Radiobutton(frame_left[6], text='Синий', variable=color_var, value='blue', bg='white')


    # Кнопки начать, закончить, сохранить
    btn_start = Button(frame_right[0], text="Начать симуляцию", command=lambda: send_command('START', control_queue, running_simulation),
                       foreground='darkgreen', font=('TkTooltipFont', 11))
    # FIXME
    btn_pause = Button(frame_right[0], text="Приостановить", command=lambda: send_command('PAUSE', control_queue, running_simulation),
                       foreground='darkgreen', font=('TkTooltipFont', 11))
    btn_finish = Button(frame_right[0], text="Закончить симуляцию", command=lambda: send_command('QUIT', control_queue, running_simulation),
                        foreground='red', font=('TkTooltipFont', 11))
    btn_save_pic = Button(frame_right[2], text="Сохранить картинку", command=lambda: send_command('SAVEFIG', control_queue, running_simulation))

    # Поле вывода
    text_output = Label(frame_right[3], text='', bg='white', font=('TkDefaultFont', 15))

    # Пакуем виджеты на экране
    label_title.place(relx=0.2, rely=0.25)
    panel.place(relx=0.7, rely=0.0)


    label_param.pack()
    #label_size.pack()
    label_width.pack()
    label_height.pack()
    label_sandpiles.pack()
    # В пятой строке вводятся песчинки
    label_type_model.pack()
    label_show.pack()
    label_colors.pack()

    #label_buttons.pack()
    label_picture.pack()
    label_output.pack()

    width_entry.pack()
    height_entry.pack()

    sandpiles_entry.pack(side=LEFT, padx=10)
    scroll.pack(side=LEFT, fill=Y)

    sandpiles_entry.config(yscrollcommand=scroll.set)

    btn_div_4.place(relx=0.2, rely=0.3)
    btn_div_8.place(relx=0.55, rely=0.3)

    btn_start.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)
    btn_finish.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8)
    btn_save_pic.pack()

    btn_show.place(relx=0.2, rely=0.3)
    btn_not_show.place(relx=0.55, rely=0.3)

    btn_colorful.place(relx=0.05, rely=0.3)
    btn_red.place(relx=0.30, rely=0.3)
    btn_green.place(relx=0.55, rely=0.3)
    btn_blue.place(relx=0.80, rely=0.3)

    text_output.pack(pady=10)

    win.mainloop()


# start_main_window()
