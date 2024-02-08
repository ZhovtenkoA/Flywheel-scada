import tkinter as tk
from ttkthemes import ThemedTk


class testbuttons:
    def __init__(self, root):
        self.root = root

        window_width = 1024
        window_height = 720
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        # self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.canvas_width = 50
        self.canvas_height = 30

        self.slider_diameter = 30
        self.slider_radius = self.slider_diameter // 2

        # self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height, bg="#f0f0f0"
        )
        self.canvas.place(x=220, y=200)

        self.o1 = self.canvas.create_oval(5, 5, 50, 28, fill="red")
        self.canvas.place(x=100, y=80)

        self.canvas.bind("<B1-Motion>", self.on_drag1)

        self.slider_x1 = 0
        self.slider1 = self.canvas.create_oval(
            self.slider_x1 + 5,
            3,
            self.slider_x1 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )

        self.button1 = tk.Button(
            self.root,
            text="Выключено",
            font=("Arial", 12),
            width=10,
            command=self.on_release1,
        )
        self.button1.pack(pady=10)

        self.canvas2 = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height, bg="#f0f0f0"
        )
        self.canvas2.place(x=220, y=230)

        self.o2 = self.canvas2.create_oval(5, 5, 50, 28, fill="red")
        self.canvas2.place(x=100, y=260)

        self.canvas2.bind("<B1-Motion>", self.on_drag2)

        self.slider_x2 = 0
        self.slider2 = self.canvas2.create_oval(
            self.slider_x2 + 5,
            3,
            self.slider_x2 + self.slider_diameter,
            self.slider_diameter,
            fill="gray",
        )

        self.button2 = tk.Button(
            self.root,
            text="Выключено",
            font=("Arial", 12),
            width=10,
            command=self.on_release2,
        )
        self.button2.pack(pady=10)

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
            self.button1.configure(text="Включено")
            self.canvas.itemconfigure(self.o1, fill="green")
        else:
            self.button1.configure(text="Выключено")
            self.canvas.itemconfigure(self.o1, fill="red")

    def on_release1(self):
        if self.slider_x1 >= self.canvas_width - self.slider_diameter:
            self.button1.configure(text="Включено")
            self.canvas.itemconfigure(self.o1, fill="green")
        else:
            self.button1.configure(text="Выключено")
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
            self.button2.configure(text="Включено")
            self.canvas2.itemconfigure(self.o2, fill="green")
        else:
            self.button2.configure(text="Выключено")
            self.canvas2.itemconfigure(self.o2, fill="red")

    def on_release2(self):
        if self.slider_x2 >= self.canvas_width - self.slider_diameter:
            self.button2.configure(text="Включено")
            self.canvas2.itemconfigure(self.o2, fill="green")
        else:
            self.button2.configure(text="Выключено")
            self.canvas2.itemconfigure(self.o2, fill="red")
