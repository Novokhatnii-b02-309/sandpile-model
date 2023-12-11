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


class Main_window:
    '''Основное окно и его методы'''
    def __init__(self, win):
        self.win = win
        '''Инициализация основного окна программы'''
        self.win_width = 900
        self.win_height = 640

        win.minsize(900, 640)

        self.simulation_prop = sandpile_func.Properties() # класс, в котором будет храниться информация об окне симуляции
        self.running_simulation = False

        win.title('Sandpile model')
        win.geometry(str(self.win_width) + 'x' + str(self.win_height) + '+' + '300+0')
        # win.resizable(False, False)
        win.configure(bg='white')

        control_queue = queue.Queue()

        m = Menu(win)
        win.config(menu=m)

        settings_menu = Menu(m, tearoff=0)
        m.add_cascade(label='Настройки', menu=settings_menu)
        settings_menu.add_command(label='Размер поля', command=self.size_options)

        m.add_command(label='Помощь', command=self.help)

        m.add_command(label='О программе', command=self.about)

        frame_top = self.main_win_frame(win, 0, 0, 1, 2 / 12)
        frame_top.configure(bg='yellow')

        frames_xywh_left = [(0, 2 / 12, 1 / 2, 1 / 12), (0, 3 / 12, 1 / 2, 1 / 12), (0, 4 / 12, 1 / 2, 1 / 12),
                            (0, 5 / 12, 1 / 2, 4 / 12), (0, 9 / 12, 1 / 2, 1 / 12), (0, 10 / 12, 1 / 2, 1 / 12),
                            (0, 11 / 12, 1 / 2, 1 / 12)]
        frames_xywh_right = [(1 / 2, 2 / 12, 1 / 2, 1 / 12), (1 / 2, 3 / 12, 1 / 2, 5 / 12),
                             (1 / 2, 8 / 12, 1 / 2, 1 / 12),
                             (1 / 2, 9 / 12, 1 / 2, 3 / 12)]

        # Делим экран на части справа и слева
        frame_left = []

        for i in range(len(frames_xywh_left)):
            frame_left.append(self.main_win_frame(win, frames_xywh_left[i][0], frames_xywh_left[i][1],
                                             frames_xywh_left[i][2], frames_xywh_left[i][3]))

        frame_right = []

        for i in range(len(frames_xywh_right)):
            frame_right.append(self.main_win_frame(win, frames_xywh_right[i][0], frames_xywh_right[i][1],
                                              frames_xywh_right[i][2], frames_xywh_right[i][3]))

        # Заголовок
        label_title = Label(frame_top, text='Модель песчаной кучи', bg='yellow',
                            foreground='black', font=('TkHeadingFont', 26))
        img = ImageTk.PhotoImage(Image.open("images/title_image.png"))
        panel = Label(frame_top, image=img, bg='yellow')

        # Виджеты текста слева
        label_param = Label(frame_left[0], text='Параметры', bg='white', font=('TkHeadingFont', 15))
        label_width = Label(frame_left[1], text='Ширина:', bg='white')
        label_height = Label(frame_left[2], text='Высота:', bg='white')
        label_sandpiles = Label(frame_left[3], text='Начальное положение песчинок', bg='white')
        label_type_model = Label(frame_left[4], text='Тип модели:', bg='white')
        label_show = Label(frame_left[5], text='Показывать процесс распада:', bg='white')
        label_colors = Label(frame_left[6], text='Цвета:', bg='white')

        # Виджеты текста справа
        # label_buttons = Label(frame_right[0], text='Симуляция', bg='white')
        label_picture = Label(frame_right[1], text='Здесь должна быть картинка', bg='white')
        label_output = Label(frame_right[3], text='Поле вывода', bg='white')
        # separator = ttk.Separator(win, orient='horizontal')
        # separator.pack(side='left', fill='x')

        # Поля ввода длины, ширины и начального положения песчинок
        self.width_entry = Entry(frame_left[1], width=30, font='Ubuntu, 12', bd=3)
        self.width_entry.insert(0, WIDTH)
        self.height_entry = Entry(frame_left[2], width=30, font='Ubuntu, 12', bd=3)
        self.height_entry.insert(0, HEIGHT)

        self.sandpiles_entry = Text(frame_left[3], width=40, height=30, font='Ubuntu, 12', bd=3)
        self.sandpiles_entry.insert(1.0, str(WIDTH // 2) + ',' + str(HEIGHT // 2) + ',' + str(SANDPILES))
        scroll = ttk.Scrollbar(frame_left[3], orient="vertical", command=self.sandpiles_entry.yview)

        # Выбор типа разделения
        self.type_var = IntVar()
        self.type_var.set(1)
        btn_div_4 = Radiobutton(frame_left[4], text='4-разделение', variable=self.type_var, value=1, bg='white')
        btn_div_8 = Radiobutton(frame_left[4], text='8-разделение', variable=self.type_var, value=2, bg='white')

        # Выбор показывать/не показывать шаги симуляции
        self.show_var = BooleanVar()
        self.show_var.set(True)
        btn_show = Radiobutton(frame_left[5], text='Да', variable=self.show_var, value=True, bg='white')
        btn_not_show = Radiobutton(frame_left[5], text='Нет', variable=self.show_var, value=False, bg='white')

        # Выбор цветов
        self.color_var = StringVar()
        self.color_var.set('colorful')
        btn_colorful = Radiobutton(frame_left[6], text='Разноцветный', variable=self.color_var, value='colorful', bg='white')
        btn_red = Radiobutton(frame_left[6], text='Красный', variable=self.color_var, value='red', bg='white')
        btn_green = Radiobutton(frame_left[6], text='Зелёный', variable=self.color_var, value='green', bg='white')
        btn_blue = Radiobutton(frame_left[6], text='Синий', variable=self.color_var, value='blue', bg='white')

        # Кнопки начать, закончить, сохранить
        btn_start = Button(frame_right[0], text="Начать",
                           command=lambda: self.send_command('START', control_queue, self.running_simulation),
                           foreground='darkgreen', font=('TkTooltipFont', 11))
        btn_pause = Button(frame_right[0], text="Приостановить",
                           command=lambda: self.send_command('PAUSE', control_queue, self.running_simulation),
                           foreground='darkblue', font=('TkTooltipFont', 11))
        btn_finish = Button(frame_right[0], text="Закончить",
                            command=lambda: self.send_command('QUIT', control_queue, self.running_simulation),
                            foreground='red', font=('TkTooltipFont', 11))
        btn_save_pic = Button(frame_right[2], text="Сохранить картинку",
                              command=lambda: self.send_command('SAVEFIG', control_queue, self.running_simulation))

        # Поле вывода
        self.text_output = Label(frame_right[3], text='', bg='white', font=('TkDefaultFont', 15))

        # Пакуем виджеты на экране
        label_title.place(relx=0.2, rely=0.25)
        panel.place(relx=0.7, rely=0.0)

        label_param.pack()
        # label_size.pack()
        label_width.pack()
        label_height.pack()
        label_sandpiles.pack()
        # В пятой строке вводятся песчинки
        label_type_model.pack()
        label_show.pack()
        label_colors.pack()

        # label_buttons.pack()
        label_picture.pack()
        label_output.pack()

        self.width_entry.pack()
        self.height_entry.pack()

        self.sandpiles_entry.pack(side=LEFT, padx=10)
        scroll.pack(side=LEFT, fill=Y)

        self.sandpiles_entry.config(yscrollcommand=scroll.set)

        btn_div_4.place(relx=0.2, rely=0.3)
        btn_div_8.place(relx=0.55, rely=0.3)

        btn_start.place(relx=0.05, rely=0.1, relwidth=0.25, relheight=0.8)
        btn_pause.place(relx=0.35, rely=0.1, relwidth=0.25, relheight=0.8)
        btn_finish.place(relx=0.65, rely=0.1, relwidth=0.25, relheight=0.8)
        btn_save_pic.pack()

        btn_show.place(relx=0.2, rely=0.3)
        btn_not_show.place(relx=0.55, rely=0.3)

        btn_colorful.place(relx=0.05, rely=0.3)
        btn_red.place(relx=0.30, rely=0.3)
        btn_green.place(relx=0.55, rely=0.3)
        btn_blue.place(relx=0.80, rely=0.3)

        self.text_output.pack(pady=10)

        win.mainloop()

    def main_win_frame(self, win, x, y, width, height):
        '''Создаёт ячейку для виджета в главном окне'''
        global win_height
        global win_width
        frame = Frame(win, bg='white', relief=SOLID, highlightbackground='gray', highlightthickness=1,
                     width=width * self.win_width, height=height * self.win_height)
        # убрал (, width=width, height=height)
        frame.grid_propagate(False)
        frame.place(relx=x, rely=y, relwidth=width, relheight=height)
        return frame

    def read_vars(self):
        '''Данная функция считывает переменные из строк и кнопок и устанавливает параметры симуляции'''
        self.simulation_prop.change_topple(self.type_var.get())

        sandpiles = self.sandpiles_entry.get(1.0, END)
        if sandpiles[0] == '/':
            new_sandpiles, width, height = sandpile_func.csv_to_np(sandpiles)
        else:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            new_sandpiles = sandpile_func.sandpiles_to_np(sandpiles, width, height)

        self.simulation_prop.change_sandpiles(new_sandpiles)
        self.simulation_prop.change_size(width, height)

        self.simulation_prop.change_colors(self.type_var.get(), self.color_var.get())

        self.simulation_prop.change_show(self.show_var.get())

    def start_simulation(self, control_queue):
        try:
            self.text_output.configure(foreground='black', text='Запуск симуляции')
            self.win.update()
            self.read_vars()
            self.running_simulation = True
            print(self.running_simulation)
            pygame_thread = Thread(target=sand_model.simulation, args=(self.simulation_prop.width, self.simulation_prop.height,
                                   self.simulation_prop.how_topple, self.simulation_prop.sandpiles, self.simulation_prop.colors,
                                   self.simulation_prop.show, control_queue))
            # sand_model.simulation(self.simulation_prop.width, self.simulation_prop.height,
            #                       self.simulation_prop.how_topple, self.simulation_prop.sandpiles,
            #                       self.simulation_prop.colors)
            pygame_thread.start()
            self.running_simulation = False
        except:
            self.show_error()

    def show_error(self):
        self.text_output.configure(fg='red', text='Ошибка')

    def end_simulation(self):
        self.running_simulation = False

    def save_pic(self):
        pass
        # FIXME

    def send_command(self, command, control_queue, running_simulation):
        control_queue.put(command)
        if command == 'START' and self.running_simulation == False:
            self.start_simulation(control_queue)
        elif command == 'QUIT':
            self.end_simulation()

    def size_options(self):
        '''Настройки размеров для симуляции'''
        win_options = Toplevel()
        win_options.resizable(width=False, height=False)
        win_options.title('Настройки размеров')

        def def_size(self):
            value = entry.get()
            value = value.split(', ')
            value = list(map(int, value))
            self.simulation_prop.change_size(value[0], value[1])

        var = StringVar()
        entry = Entry(win_options, width=30, font='Ubuntu, 12', bd=3, relief=SUNKEN, textvariable=var)

        label = Label(win_options, text='Введите размер поля в виде ***, ***')

        button = Button(win_options, text="Настроить размер", command=def_size)

        entry.pack()
        label.pack()
        button.pack()

    def about(self):
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

    def help(self):
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

        Начать:
        Создаёт новую симуляцию/продолжает существующую

        Приостановить:
        Приостанавливает текущую симуляцию

        Закончить:
        Завершает текущую симуляцию
        '''
        label = Label(win_help, bg="white", fg='black', text=help_text)
        label.pack()



# start_main_window()
