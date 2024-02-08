from tkinter import Text, Button, BOTH

# Виджеты для вкладки с тестовыми запросами 

class Tab3Widget:
    def __init__(self, parent):
        self.output_test = Text(parent)
        self.output_test.pack(fill=BOTH, expand=True)

def create_test_buttons_and_output(tab3_widgets, start_test_func, stop_test_func):
    # Создание кнопок и окна вывода на основе переданных параметров
    tab3_widgets.start_button_test = Button(
        tab3_widgets.output_test.master,
        text="Пуск для теста",
        command=start_test_func,
        font=("Arial", 10, "bold"),
        foreground="black",
    )
    tab3_widgets.start_button_test.pack()

    tab3_widgets.stop_button_test = Button(
        tab3_widgets.output_test.master,
        text="Стоп тест",
        command=stop_test_func,
        font=("Arial", 10, "bold"),
        foreground="black",
    )
    tab3_widgets.stop_button_test.pack()
