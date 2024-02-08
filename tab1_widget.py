from tkinter import *

# Виджеты для вкладки с функционалом чтения отдельных Holding registers

class Tab1Widget:
    def __init__(self, parent, clear_func, start_func, stop_func):
        self.clear_func = clear_func
        self.start_func = start_func
        self.stop_func = stop_func
        self.create_output(parent)
        self.create_buttons(parent, clear_func, start_func, stop_func)
        self.create_labels(parent)
        self.create_inputs(parent)

    def create_output(self, parent):
        self.holding_output = Text(parent)
        self.holding_output.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(parent, command=self.holding_output.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.holding_output.configure(yscrollcommand=self.scrollbar.set)

    def create_buttons(self, parent, clear_func, start_func, stop_func):

        self.start_loging_button = Button(
            parent,
            text="Пуск",
            command=self.start_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.start_loging_button.pack()

        self.stop_loging_button = Button(
            parent,
            text="Стоп",
            command=self.stop_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.stop_loging_button.pack()

        self.clear_button = Button(
            parent,
            text="Очистить",
            command=self.clear_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.clear_button.pack()



    def create_labels(self, parent):

        self.starting_adress_label = Label(
            parent,
            text="Стартовый адрес",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.starting_adress_label.place(x=10, y=10)

        self.numbers_to_read_label = Label(
            parent,
            text="Количество регистров",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.numbers_to_read_label.place(x=10, y=40)


    def create_inputs(self, parent):
        self.register_address_entry = Entry(parent)
        self.register_address_entry.place(x=200, y=10)
        self.value_entry = Entry(parent)
        self.value_entry.place(x=200, y=40)

        self.starting_adress_entry = Entry(parent)
        self.starting_adress_entry.place(x=200, y=10)
        self.numbers_to_read_entry = Entry(parent)
        self.numbers_to_read_entry.place(x=200, y=40)