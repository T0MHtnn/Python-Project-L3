import tkinter as tk
from threading import Thread
import time
import pygame
from base_frame import BaseFrame

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class Alarme(BaseFrame):
    def __init__(self, parent, controller, switch_value, musics):
        super().__init__(parent, controller, switch_value, musics)
        label = tk.Label(self, text="Alarme", font=LARGEFONT)
        label.pack(pady=20)

        self.hour = tk.StringVar()
        self.min = tk.StringVar()
        self.sec = tk.StringVar()

        self.hour.set("00")
        self.min.set("00")
        self.sec.set("00")

        time_frame = tk.Frame(self)
        time_frame.pack(pady=10)

        hour_entry = tk.Entry(time_frame, textvariable=self.hour, font=smallfont, width=3, justify='center')
        hour_entry.grid(row=0, column=0, padx=5)
        tk.Label(time_frame, text=":", font=smallfont).grid(row=0, column=1)
        min_entry = tk.Entry(time_frame, textvariable=self.min, font=smallfont, width=3, justify='center')
        min_entry.grid(row=0, column=2, padx=5)
        tk.Label(time_frame, text=":", font=smallfont).grid(row=0, column=3)
        sec_entry = tk.Entry(time_frame, textvariable=self.sec, font=smallfont, width=3, justify='center')
        sec_entry.grid(row=0, column=4, padx=5)

        set_alarm_btn = tk.Button(self, text="Définir l'alarme", command=self.start_alarm)
        set_alarm_btn.pack(pady=10)

        stop_alarm_btn = tk.Button(self, text="Arrêter l'alarme", command=self.stop_alarm)
        stop_alarm_btn.pack(pady=10)

        self.alarm_thread = None
        self.is_alarm_running = False

    def update_theme(self, switch_value):
        fg_color = ""
        bg_color = ""
        entry_bg_color = ""

        if switch_value:
            bg_color = "white"
            fg_color = "#26242f"
            entry_bg_color = "white"
        else:
            bg_color = "#26242f"
            fg_color = "white"
            entry_bg_color = "#26242f"

        self.config(bg=bg_color)

        for widget in self.winfo_children():
            widget_type = widget.winfo_class()
            if widget_type == "Label":
                widget.config(bg=bg_color, fg=fg_color)
            elif widget_type == "Button":
                widget.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
            elif widget_type == "Entry":
                widget.config(bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
            elif widget_type == "Frame":
                widget.config(bg=bg_color)
                for child in widget.winfo_children():
                    child_type = child.winfo_class()
                    if child_type == "Label":
                        child.config(bg=bg_color, fg=fg_color)
                    elif child_type == "Entry":
                        child.config(bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)

    def alarm_process(self, set_alarm_time):
        self.is_alarm_running = True
        while self.is_alarm_running:
            time.sleep(0.5)
            if self.controller.manual_time:
                current_time_obj = self.controller.manual_time
            else:
                current_time_obj = self.controller.get_datetime_with_utc()
            current_time_str = current_time_obj.strftime("%H:%M:%S")
            if current_time_str == set_alarm_time:
                if self.controller.current_music_index != -1:
                    pygame.mixer.music.load(self.musics[self.controller.current_music_index])
                    pygame.mixer.music.play()
                else:
                    tk.messagebox.showinfo("Alarme", "Il est l'heure ! (Aucune musique sélectionnée)")
                self.is_alarm_running = False
                break

    def start_alarm(self):
        if self.alarm_thread and self.alarm_thread.is_alive():
            tk.messagebox.showinfo("Info", "Une alarme est déjà en cours d'exécution. Arrêtez-la d'abord.")
            return

        try:
            h = int(self.hour.get())
            m = int(self.min.get())
            s = int(self.sec.get())
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValueError("Heure invalide")
            set_alarm_time = f"{h:02d}:{m:02d}:{s:02d}"
            self.alarm_thread = Thread(target=self.alarm_process, args=(set_alarm_time,), daemon=True)
            self.alarm_thread.start()
            tk.messagebox.showinfo("Alarme", f"Alarme réglée pour {set_alarm_time}")
        except ValueError:
            tk.messagebox.showerror("Erreur", "Veuillez entrer une heure valide (HH:MM:SS).")

    def stop_alarm(self):
        self.is_alarm_running = False
        pygame.mixer.music.stop()
        tk.messagebox.showinfo("Alarme", "Alarme arrêtée.")
