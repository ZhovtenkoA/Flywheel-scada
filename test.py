
# import tkinter as tk

# # --- functions ---

# def move(steps=10, distance=0.1):
#     if steps > 0:
#         # get current position
#         relx = float(frame.place_info()['relx'])

#         # set new position
#         frame.place_configure(relx=relx+distance)

#         # repeate it after 10ms
#         root.after(10, move, steps-1, distance)

# def toggle(event):
#     if button["text"] == "Yes":
#         move(25, 0.02)  # 50*0.02 = 1
#         button["text"] = "No"
#         print("Clicked on yes")
#     elif button["text"] == "No":
#         move(25, -0.02)
#         button["text"] = "Yes"
#         print("Clicked on no")


# # --- main --

# root = tk.Tk()

# frame = tk.Frame(root, background='red')
# frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

# # to center label and button
# frame.grid_columnconfigure(0, weight=1)
# frame.grid_rowconfigure(0, weight=1)
# frame.grid_rowconfigure(3, weight=1)




# button = tk.Button(frame, text='Yes',width=5,height=1)
# button.place(relx=0.25,rely=0.5,relwidth=0.5, relheight=0.1)
# button.bind("<Button-1>",toggle)


# root.mainloop()


import tkinter as tk


class ToggleButton(tk.Button):

    ON_config = {'bg': 'green',
                 'text': 'button is ON',
                 'relief': 'sunken',
                 }
    OFF_config =  {'bg': 'white',
                 'text': 'button is OFF',
                 'relief': 'raised',
                 }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.toggled = False
        self.config = self.OFF_config
        self.config_button()

        self.bind("<Button-1>", self.toggle)

    def toggle(self, *args):
        if self.toggled:   # True = ON --> toggle to OFF
            self.config = self.OFF_config
        else:
            self.config = self.ON_config
        self.toggled = not self.toggled
        return self.config_button()

    def config_button(self):
        self['bg'] = self.config['bg']
        self['text'] = self.config['text']
        self['relief'] = self.config['relief']
        return "break"

    def __str__(self):
        return f"{self['text']}, {self['bg']}, {self['relief']}"


def button_placeholder():
    print('toggling now!')


if __name__ == '__main__':

    root = tk.Tk()

    button = ToggleButton(root)
    button.pack()

    root.mainloop()