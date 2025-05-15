import tkinter as tk

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class BaseFrame(tk.Frame):
    def __init__(self, parent, controller, switch_value, musics):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.switch_value = switch_value
        self.musics = musics
