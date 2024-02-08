from tkinter import *
import tkinter as tk

# Виджеты основного экрана


class Tab4Widget:


    def __init__(
        self,
        parent,
        start_reading_func,
        stop_reading_func,
        acceleration_func,
        slowdown_func,
        shutdown_func,
        trh_plus_func,
        trh_minus_func,
        trh_write_func,
        write_moment_of_inertia_func,
        start_counting_w_h_func
    ):
        self.start_reading_func = start_reading_func
        self.stop_reading_func = stop_reading_func
        self.acceleration_func = acceleration_func
        self.slowdown_func = slowdown_func
        self.shutdown_func = shutdown_func
        self.trh_plus_func = trh_plus_func
        self.trh_minus_func = trh_minus_func
        self.trh_write_func = trh_write_func
        self.write_moment_of_inertia_func = write_moment_of_inertia_func
        self.start_counting_w_h_func = start_counting_w_h_func
        self.create_output(parent)
        self.create_buttons(
        parent,
        start_reading_func,
        stop_reading_func,
        acceleration_func,
        slowdown_func,
        shutdown_func,
        trh_plus_func,
        trh_minus_func,
        trh_write_func,
        write_moment_of_inertia_func,
        start_counting_w_h_func
    )
        self.create_labels(parent)
        self.create_inputs(parent)
        self.create_indicators(parent)

    def create_output(self, parent):

        self.output_30001 = Text(parent)  # ADC (I1)
        self.output_30001.place(x=150, y=10, width=60, height=25)

        self.output_30002 = Text(parent)  # ADC (I2)
        self.output_30002.place(x=150, y=50, width=60, height=25)

        self.output_30003 = Text(parent)  # ADC (I3)
        self.output_30003.place(x=150, y=90, width=60, height=25)

        self.output_30004 = Text(parent)  # ADC (I4)
        self.output_30004.place(x=150, y=130, width=60, height=25)

        self.output_30005 = Text(parent)  # PWM1
        self.output_30005.place(x=350, y=10, width=60, height=25)

        self.output_30006 = Text(parent)  # PWM2
        self.output_30006.place(x=350, y=50, width=60, height=25)

        self.output_30007 = Text(parent)  # PWM3
        self.output_30007.place(x=350, y=90, width=60, height=25)

        self.output_30008 = Text(parent)  # PWM4
        self.output_30008.place(x=350, y=130, width=60, height=25)

        self.output_30009 = Text(parent)  # RPM
        self.output_30009.place(x=150, y=400, width=80, height=25)

        self.output_30010 = Text(parent)  # freq
        self.output_30010.place(x=150, y=200, width=60, height=25)

        self.output_30011 = Text(parent)  # TRH
        self.output_30011.place(x=150, y=240, width=60, height=25)

        self.output_30012 = Text(parent)  # ADDR
        self.output_30012.place(x=150, y=280, width=60, height=25)

        self.output_30013 = Text(parent)  # VDC
        self.output_30013.place(x=150, y=320, width=60, height=25)

        self.output_30014 = Text(parent)  # ADC
        self.output_30014.place(x=150, y=360, width=80, height=25)

        self.output_30005_percent = Text(parent)
        self.output_30005_percent.place(x=450, y=10, width=50, height=25)

        self.output_30006_percent = Text(parent)
        self.output_30006_percent.place(x=450, y=50, width=50, height=25)

        self.output_30007_percent = Text(parent)
        self.output_30007_percent.place(x=450, y=90, width=50, height=25)

        self.output_30008_percent = Text(parent)
        self.output_30008_percent.place(x=450, y=130, width=50, height=25)

        self.accumulated_kinetic_energy_output = Text(parent)
        self.accumulated_kinetic_energy_output.place(x=150, y=440, width=80, height=25)

        self.kW_power_output = Text(parent)
        self.kW_power_output.place(x=350, y=320, width=120, height=25)

        self.P_output = Text(parent)
        self.P_output.place(x=150, y=480, width=80, height=25)

    def create_buttons(
        self,
        parent,
        start_reading_func,
        stop_reading_func,
        acceleration_func,
        slowdown_func,
        shutdown_func,
        trh_plus_func,
        trh_minus_func,
        trh_write_func,
        write_moment_of_inertia_func,
        start_counting_w_h_func
    ):

        # Кнопки управления чтением на основном окне
        self.start_button = Button(
            parent,
            text="Пуск",
            command=self.start_reading_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.start_button.pack()

        self.stop_button = Button(
            parent,
            text="Стоп",
            command=self.stop_reading_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.stop_button.pack()

        # Кнопки управления PWM (разгон, торможение, стоп)
        self.acceleration_button = Button(
            parent,
            text="Разгон",
            command=self.acceleration_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.acceleration_button.pack()

        self.slowdown_button = Button(
            parent,
            text="Замедление",
            command=self.slowdown_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.slowdown_button.pack()

        self.shutdown_button = Button(
            parent,
            text="Остановка",
            command=self.shutdown_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.shutdown_button.pack()

        # Кнопки управления Trashhold
        self.trh_plus_button = Button(
            parent,
            text="+",
            command=self.trh_plus_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.trh_plus_button.pack()
        self.trh_plus_button.place(x=230, y=240, width=40, height=25)

        self.trh_minus_button = Button(
            parent,
            text="-",
            command=self.trh_minus_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.trh_minus_button.pack()
        self.trh_minus_button.place(x=280, y=240, width=40, height=25)

        self.write_trh_button = Button(
            parent,
            text="Отправить",
            command=self.trh_write_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.write_trh_button.pack()
        self.write_trh_button.place(x=520, y=240, width=100, height=25)

        # Кнока расчета накопленной кинетической єнергии
        self.write_inertia_value_button = Button(
            parent,
            text="Отправить",
            command=self.write_moment_of_inertia_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.write_inertia_value_button.pack()
        self.write_inertia_value_button.place(x=520, y=440, width=100, height=25)

        # Кнока расчета киловатт*ч
        self.kW_power_button = Button(
            parent,
            text="Рассчет W*h",
            command=self.start_counting_w_h_func,
            font=("Arial", 10, "bold"),
            foreground="black",
        )
        self.kW_power_button.pack()
        self.kW_power_button.place(x=480, y=320, width=100, height=25)


    def create_labels(self, parent):

        self.value_trh_label = Label(
            parent,
            text="Новый TRH",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_trh_label.place(x=340, y=240)

        self.accumulated_kinetic_energy_label = Label(
            parent,
            text="Момент иннерции",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.accumulated_kinetic_energy_label.place(x=300, y=440)

        self.value_30001_label = Label(
            parent,
            text="ADC(I1)",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30001_label.place(x=10, y=10)
        self.value_30002_label = Label(
            parent,
            text="ADC(I2)",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30002_label.place(x=10, y=50)
        self.value_30003_label = Label(
            parent,
            text="ADC(I3)",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30003_label.place(x=10, y=90)
        self.value_30004_label = Label(
            parent,
            text="ADC(I4)",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30004_label.place(x=10, y=130)
        self.value_30005_label = Label(
            parent,
            text="PWM1",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30005_label.place(x=250, y=10)
        self.value_30006_label = Label(
            parent,
            text="PWM2",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30006_label.place(x=250, y=50)
        self.value_30007_label = Label(
            parent,
            text="PWM3",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30007_label.place(x=250, y=90)
        self.value_30008_label = Label(
            parent,
            text="PWM4",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30008_label.place(x=250, y=130)
        self.value_30009_label = Label(
            parent,
            text="RPM",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30009_label.place(x=10, y=400)
        self.value_30010_label = Label(
            parent,
            text="Frequency",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30010_label.place(x=10, y=200)
        self.value_30011_label = Label(
            parent,
            text="Trashold",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30011_label.place(x=10, y=240)
        self.value_30012_label = Label(
            parent,
            text="ADDR",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30012_label.place(x=10, y=280)
        self.value_30013_label = Label(
            parent,
            text="Vdc",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30013_label.place(x=10, y=320)
        self.value_30014_label = Label(
            parent,
            text="Adc",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.value_30014_label.place(x=10, y=360)

        self.accumulated_kinetic_energy_output_label = Label(
            parent,
            text="Energy",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.accumulated_kinetic_energy_output_label.place(x=10, y=440)

        self.power_label = Label(
            parent,
            text="Power",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.power_label.place(x=250, y=320)


        self.P_output_label = Label(
            parent,
            text="P",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.P_output_label.place(x=10, y=480)


        self.time_label = Label(
            parent, font=("Arial", 10, "bold"), foreground="white", background="#424242"
        )
        self.time_label.place(x=950, y=10)
        self.time_label_text = Label(
            parent,
            text="Current time:",
            font=("Arial", 10, "bold"),
            foreground="white",
            background="#424242",
        )
        self.time_label_text.place(x=860, y=10)



    def create_inputs(self, parent):

        self.value_trh_entry = Entry(parent)
        self.value_trh_entry.place(x=430, y=240, width=60, height=25)

        self.inertia_value_entry = Entry(parent)
        self.inertia_value_entry.place(x=430, y=440, width=60, height=25)
        self.inertia_value_entry.insert(0, "0.3")

    def create_indicators(self, parent):

        indicator = Canvas(
            parent, width=20, height=20, borderwidth=0, highlightthickness=0, background="#424242"
        )
        indicator.pack()
        indicator.place(x=120, y=242)

        indicator_pwm1 = Canvas(
            parent, width=20, height=20, borderwidth=0, highlightthickness=0, background="#424242"
        )
        indicator_pwm1.pack()
        indicator_pwm1.place(x=420, y=10)

        indicator_pwm2 = Canvas(
            parent, width=20, height=20, borderwidth=0, highlightthickness=0, background="#424242"
        )
        indicator_pwm2.pack()
        indicator_pwm2.place(x=420, y=50)

        indicator_pwm3 = Canvas(
            parent, width=20, height=20, borderwidth=0, highlightthickness=0, background="#424242"
        )
        indicator_pwm3.pack()
        indicator_pwm3.place(x=420, y=90)

        indicator_pwm4 = Canvas(
            parent, width=20, height=20, borderwidth=0, highlightthickness=0, background="#424242"
        )
        indicator_pwm4.pack()
        indicator_pwm4.place(x=420, y=130)


        center_x = 10
        center_y = 10
        radius = 8

        circle = indicator.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="grey",
        )
        circle_pwm1 = indicator_pwm1.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="green",
        )
        circle_pwm2 = indicator_pwm2.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="green",
        )
        circle_pwm3 = indicator_pwm3.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="green",
        )
        circle_pwm4 = indicator_pwm4.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="green",
        )


class TestButtons:
    def __init__(self, parent):
        self.parent = parent
        self.canvas_width = 45
        self.canvas_height = 25
        self.slider_diameter = 25
        self.slider_radius = self.slider_diameter // 2
        self.create_widgets()

    def create_widgets(self):
        #Слайдер 1
        self.canvas = tk.Canvas(
            self.parent, width=self.canvas_width, height=self.canvas_height, bg="#424242", highlightthickness=0
        )
        self.canvas.place(x=530, y=8)

        self.o1 = self.canvas.create_oval(4, 4, 43, 23, fill="red")

        self.canvas.bind("<B1-Motion>", self.on_drag1)

        self.slider_x1 = 0
        self.slider1 = self.canvas.create_oval(
            self.slider_x1 + 5,
            3,
            self.slider_x1 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )
        
        #Слайдер 2
        self.canvas2 = tk.Canvas(
            self.parent, width=self.canvas_width, height=self.canvas_height, bg="#424242", highlightthickness=0
        )
        self.canvas2.place(x=530, y=48)

        self.o2 = self.canvas2.create_oval(4, 4, 43, 23, fill="red")

        self.canvas2.bind("<B1-Motion>", self.on_drag2)

        self.slider_x2 = 0
        self.slider2 = self.canvas2.create_oval(
            self.slider_x2 + 5,
            3,
            self.slider_x2 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )

        #Слайдер 3
        self.canvas3 = tk.Canvas(
            self.parent, width=self.canvas_width, height=self.canvas_height, bg="#424242", highlightthickness=0
        )
        self.canvas3.place(x=530, y=88)

        self.o3 = self.canvas3.create_oval(4, 4, 43, 23, fill="red")

        self.canvas3.bind("<B1-Motion>", self.on_drag3)

        self.slider_x3 = 0
        self.slider3 = self.canvas3.create_oval(
            self.slider_x3 + 5,
            3,
            self.slider_x3 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )

        #Слайдер 4
        self.canvas4 = tk.Canvas(
            self.parent, width=self.canvas_width, height=self.canvas_height, bg="#424242", highlightthickness=0
        )
        self.canvas4.place(x=530, y=128)

        self.o4 = self.canvas4.create_oval(4, 4, 43, 23, fill="red")

        self.canvas4.bind("<B1-Motion>", self.on_drag4)

        self.slider_x4 = 0
        self.slider4 = self.canvas4.create_oval(
            self.slider_x4 + 5,
            3,
            self.slider_x4 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )


    def on_drag1(self, event):
        slider_x1 = event.x - self.slider_radius
        if slider_x1 < 0:
            slider_x1 = 0
        elif slider_x1 > self.canvas_width - self.slider_diameter:
            slider_x1 = self.canvas_width - self.slider_diameter
        self.canvas.coords(
            self.slider1,
            slider_x1 + 5,
            3,
            slider_x1 + self.slider_diameter,
            self.slider_diameter,
        )

        if slider_x1 >= self.canvas_width - self.slider_diameter:
            # self.button1.configure(text="Включено")
            self.canvas.itemconfigure(self.o1, fill="green")
        else:
            # self.button1.configure(text="Выключено")
            self.canvas.itemconfigure(self.o1, fill="red")

    def on_release1(self):
        if self.slider_x1 >= self.canvas_width - self.slider_diameter:
            # self.button1.configure(text="Включено")
            self.canvas.itemconfigure(self.o1, fill="green")
        else:
            # self.button1.configure(text="Выключено")
            self.canvas.itemconfigure(self.o1, fill="red")

    def on_drag2(self, event):
        slider_x2 = event.x - self.slider_radius
        if slider_x2 < 0:
            slider_x2 = 0
        elif slider_x2 > self.canvas_width - self.slider_diameter:
            slider_x2 = self.canvas_width - self.slider_diameter
        self.canvas2.coords(
            self.slider2,
            slider_x2 + 5,
            3,
            slider_x2 + self.slider_diameter,
            self.slider_diameter,
        )

        if slider_x2 >= self.canvas_width - self.slider_diameter:
            # self.button2.configure(text="Включено")
            self.canvas2.itemconfigure(self.o2, fill="green")
        else:
            # self.button2.configure(text="Выключено")
            self.canvas2.itemconfigure(self.o2, fill="red")

    def on_release2(self):
        if self.slider_x2 >= self.canvas_width - self.slider_diameter:
            # self.button2.configure(text="Включено")
            self.canvas2.itemconfigure(self.o2, fill="green")
        else:
            # self.button2.configure(text="Выключено")
            self.canvas2.itemconfigure(self.o2, fill="red")

    def on_drag3(self, event):
            slider_x3 = event.x - self.slider_radius
            if slider_x3 < 0:
                slider_x3 = 0
            elif slider_x3 > self.canvas_width - self.slider_diameter:
                slider_x3 = self.canvas_width - self.slider_diameter
            self.canvas3.coords(
                self.slider3,
                slider_x3 + 5,
                3,
                slider_x3 + self.slider_diameter,
                self.slider_diameter,
            )

            if slider_x3 >= self.canvas_width - self.slider_diameter:
                # self.button2.configure(text="Включено")
                self.canvas3.itemconfigure(self.o3, fill="green")
            else:
                # self.button2.configure(text="Выключено")
                self.canvas3.itemconfigure(self.o3, fill="red")

    def on_release3(self):
        if self.slider_x3 >= self.canvas_width - self.slider_diameter:
            # self.button2.configure(text="Включено")
            self.canvas3.itemconfigure(self.o3, fill="green")
        else:
            # self.button2.configure(text="Выключено")
            self.canvas3.itemconfigure(self.o3, fill="red")

    def on_drag4(self, event):
            slider_x4 = event.x - self.slider_radius
            if slider_x4 < 0:
                slider_x4 = 0
            elif slider_x4 > self.canvas_width - self.slider_diameter:
                slider_x4 = self.canvas_width - self.slider_diameter
            self.canvas4.coords(
                self.slider4,
                slider_x4 + 5,
                3,
                slider_x4 + self.slider_diameter,
                self.slider_diameter,
            )

            if slider_x4 >= self.canvas_width - self.slider_diameter:
                # self.button2.configure(text="Включено")
                self.canvas4.itemconfigure(self.o4, fill="green")
            else:
                # self.button2.configure(text="Выключено")
                self.canvas4.itemconfigure(self.o4, fill="red")

    def on_release4(self):
        if self.slider_x4 >= self.canvas_width - self.slider_diameter:
            # self.button2.configure(text="Включено")
            self.canvas4.itemconfigure(self.o4, fill="green")
        else:
            # self.button2.configure(text="Выключено")
            self.canvas4.itemconfigure(self.o4, fill="red")