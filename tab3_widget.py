from tkinter import Text, Button, BOTH

# Виджеты для вкладки с тестовыми запросами 

class Tab3Widget:
    def __init__(self, parent, start_test_func, end_test_func):
        self.start_test_func = start_test_func
        self.end_test_func = end_test_func
        self.create_test_buttons_and_output(parent, start_test_func, end_test_func)


    def create_test_buttons_and_output(self, parent, start_test_func, end_test_func):
        self.output_test = Text(parent)
        self.output_test.pack(fill=BOTH, expand=True)

        self.start_button_test = Button(
            parent,
            text="Пуск для теста",
            command=self.start_test_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.start_button_test.pack()

        self.stop_button_test = Button(
            parent,
            text="Стоп тест",
            command=self.end_test_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.stop_button_test.pack()

