from tkinter import *

# Виджеты для вкладки с функционалом записи отдельных Holding registers


class Tab2Widget:
    def __init__(self, parent, write_func):
        self.write_func = write_func
        self.create_buttons(parent, write_func)
        self.create_labels(parent)
        self.create_inputs(parent)

    def create_buttons(self, parent, write_func):
        self.write_button = Button(
            parent,
            text="Отправить",
            command=self.write_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.write_button.pack()

    def create_labels(self, parent):
        self.value_label = Label(
            parent,
            text="Значение",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_label.place(x=10, y=40)

        self.register_address_label = Label(
            parent,
            text="Адрес регистра",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.register_address_label.place(x=10, y=10)

    def create_inputs(self, parent):
        self.register_address_entry = Entry(parent)
        self.register_address_entry.place(x=200, y=10)
        self.value_entry = Entry(parent)
        self.value_entry.place(x=200, y=40)
