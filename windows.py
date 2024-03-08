import tkinter as tk

from tkinter import ttk
from idlelib import tooltip

from constants import rools, helps
from snake import SnakeGame

class option_window(tk.Toplevel):
    def __init__(self, master, options, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.current_options = options
        self.options = {"Легко": {"width": 600, "height": 600, "scale": 60, "speed": 150, "area_apples": 2},
                        "Нормально": {"width": 600, "height": 600, "scale": 30, "speed": 100, "area_apples": 1},
                        "Сложно": {"width": 600, "height": 600, "scale": 15, "speed": 50, "area_apples": 0},
                        "Сейчас": options}

        self.focus()
        self.title('Змейка: настройки')
        self.iconbitmap(default="icon.ico")
        self.resizable(False, False)
        self.update_idletasks()
        self.attributes("-toolwindow", True)

        self.label = ttk.Label(self, text="Уровень: ", font=15, padding=[10, 10])
        self.label.grid(row=0, column=0, columnspan=2)

        self.choices = ttk.Combobox(self, values=("Легко", "Нормально", "Сложно", "Сейчас"))
        self.choices.current(3)
        self.choices.grid(row=0, column=2, columnspan=2)
        self.choices.bind("<<ComboboxSelected>>", self.make_choice)

        self.btn_ok = ttk.Button(self, text='ОК', command=self.cmd_ok)
        self.btn_ok.grid(row=1, column=1)

        self.btn_undo = ttk.Button(self, text='Отмена', command=lambda: self.destroy())
        self.btn_undo.grid(row=1, column=2)

        self.btn_make_new = ttk.Button(self, text='Настройки', command=self.cmd_make_new)
        self.btn_make_new.grid(row=1, column=3)

        self.update()

    def cmd_make_new(self):
        self.btn_undo.grid_forget()

        self.btn_ok.grid_remove()
        self.btn_make_new.grid_remove()
        self.label.grid_remove()
        self.choices.grid_remove()

        self.labels = [ttk.Label(self, text=s, font=("Helvetica", 10), padding=[10, 10], justify=tk.RIGHT) \
                       for s in ("Размер поля: ", "Скорость: ", "Ограничение спавна яблок: ")]
        for i in range(3):
            self.labels[i].grid(column=0, row=i, columnspan=2)
            tooltip.Hovertip(self.labels[i], helps[i], 500)

        self.size_of_var = tk.IntVar(value=self.options["Сейчас"]["scale"])
        self.size_of_values = [8, 10, 12, 15, 20, 24, 25, 30, 40, 50, 60]
        self.size_of = ttk.Spinbox(self, textvariable=self.size_of_var, values=self.size_of_values, state="readonly")
        self.size_of.grid(row=0, column=2)
        tooltip.Hovertip(self.size_of, helps[3], 500)

        self.speed_var = tk.IntVar(value=100 - self.options["Сейчас"]["speed"])
        self.speed = ttk.Spinbox(self, textvariable=self.speed_var, from_=-100, to=80, increment=2, state="readonly")
        self.speed.grid(row=1, column=2)
        tooltip.Hovertip(self.speed, helps[3], 500)

        self.area_var = tk.IntVar(value=self.options["Сейчас"]["area_apples"])
        self.area_values = [0, 1, 2, 3]
        self.area = ttk.Spinbox(self, textvariable=self.area_var, values=self.area_values, state="readonly")
        self.area.grid(row=2, column=2)
        tooltip.Hovertip(self.area, helps[3], 500)

        self.btn_ok = ttk.Button(self, text="ОК", command=self.cmd_ok_2)
        self.btn_ok.grid(row=3, column=1)
        self.btn_undo.grid(row=3, column=2)

    def make_choice(self, event):
        self.current_options = self.options[self.choices.get()]

    def cmd_ok(self):
        self.current_options = self.options[self.choices.get()]
        self.master.update_options(self.current_options)
        self.destroy()

    def cmd_ok_2(self):
        self.current_options = {"width": 600, "height": 600, "scale": self.size_of_var.get(), "speed": 100 - self.speed_var.get(), "area_apples": self.area_var.get()}
        self.master.update_options(self.current_options)
        self.destroy()

class help_window(tk.Toplevel):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.focus()
        self.title('Змейка: помощь')
        self.iconbitmap(default="icon.ico")
        self.resizable(False, False)
        self.update_idletasks()
        self.attributes("-toolwindow", True)
        self.text = rools
        self.label = ttk.Label(self, text=self.text, font=("Helvetica", 10), padding=[10, 10])
        self.label.pack()
        self.update()

class main_window(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title('Змейка: игра')
        self.resizable(False, False)

        self.iconbitmap('icon.ico')
        self.attributes("-alpha", 1.0)

        self.update_idletasks()

        self.pinned = False
        self.options = {"width": 600, "height": 600, "scale": 30, "speed": 100, "area_apples": 1}

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label='Закрепить окно', command=self.__pin_window)
        self.menubar.add_cascade(label='Вид', menu=self.view_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Правила игры", command=self.__help)
        self.menubar.add_cascade(label='Помощь', menu=self.help_menu)

        self.menubar.add_command(label="Настройки...", command=self.__options)
        self.menubar.add_command(label="Играть!", command=self.__game)

        self.__game()
        self.update()

    def __pin_window(self):
        self.pinned = ~self.pinned
        a, b = "Закрепить окно", "Открепить окно"
        if not self.pinned: a, b = b, a
        self.view_menu.entryconfigure(a, label=b)
        self.attributes("-topmost", self.pinned)

    def __game(self):
        try:
            if not self.game_window.process:
                self.game_window.start_new_game(**self.options)
        except AttributeError:
            self.game_window = SnakeGame(self, **self.options)

    def __options(self):
        option_win = option_window(self, self.options)
        self.wait_window(option_win)

    def __help(self):
        help_win = help_window(self)
        self.wait_window(help_win)

    def update_options(self, new_options):
        self.options = new_options
