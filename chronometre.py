import tkinter as tk
import time
from base_frame import BaseFrame

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class Chronometre(BaseFrame):
    def __init__(self, parent, controller, switch_value, musics):
        super().__init__(parent, controller, switch_value, musics)
        label = tk.Label(self, text="Chronomètre", font=LARGEFONT)
        label.pack(pady=20)

        self.sv = tk.StringVar(value="00:00:00")
        self.is_running = False
        self.start_time = None
        self.paused_time = 0
        self.lance = False
        self.after_loop = None

        tk.Label(self, textvariable=self.sv, font='Arial 15').pack(pady=10)
        tk.Button(self, text='Start/Stop', command=self.Start).pack(pady=10)
        tk.Button(self, text='Pause', command=self.Pause).pack(pady=10)
        tk.Button(self, text='Stop', command=self.Stop).pack(pady=10)

    def update_theme(self, switch_value):
        """Met à jour les couleurs selon le thème"""
        self.switch_value = switch_value
        bg_color = "white" if switch_value else "#26242f"
        fg_color = "#26242f" if switch_value else "white"

        self.configure(bg=bg_color)
        self.time_label.config(bg=bg_color, fg=fg_color)
        self.start_button.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
        self.pause_button.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
        self.stop_button.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)

        # Mise à jour du label principal
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget['text'] == "Chronomètre":
                widget.config(bg=bg_color, fg=fg_color)

    def Start(self):
        if not self.is_running:
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.start_time = time.time() - self.paused_time

            self.update_timer()
            self.is_running = True
            self.lance = True

    def Pause(self):
        if self.is_running:
            if self.after_loop:
                self.after_cancel(self.after_loop)
            self.paused_time = time.time() - self.start_time
            self.is_running = False
        elif self.lance:
            self.start_time = time.time() - self.paused_time
            self.update_timer()
            self.is_running = True

    def Stop(self):
        if self.is_running:
            if self.after_loop:
                self.after_cancel(self.after_loop)
            self.is_running = False
            self.lance = False

        self.start_time = None
        self.paused_time = 0
        self.sv.set("00:00:00")

    def update_timer(self):
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.sv.set(self.format_time(elapsed))
            self.after_loop = self.after(50, self.update_timer)

    @staticmethod
    def format_time(elap):
        hours, rem = divmod(elap, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
