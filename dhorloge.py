import tkinter as tk
from base_frame import BaseFrame
from horloge import Horloge

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class DHorloge(BaseFrame):
    def __init__(self, parent, controller, switch_value, musics):
        super().__init__(parent, controller, switch_value, musics)
        label = tk.Label(self, text="Horloge Digitale", font=LARGEFONT)
        label.pack(pady=20)

        self.label = tk.Label(self, text="", font=('Times New Roman', 40))
        self.label.pack(pady=20)
        self.update_clock()

        btnClock = tk.Button(self, text="Horloge Analogique", command=lambda: controller.show_frame(Horloge))
        btnClock.pack(pady=10)

    def update_clock(self):
        if self.controller.manual_time:
            current_time = self.controller.manual_time
        else:
            current_time = self.controller.get_datetime_with_utc()
        now = current_time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.after(1000, self.update_clock)
