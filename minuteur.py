import tkinter as tk
import pygame
from base_frame import BaseFrame

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class Minuteur(BaseFrame):
    def __init__(self, parent, controller, switch_value, musics):
        super().__init__(parent, controller, switch_value, musics)
        label = tk.Label(self, text="Minuteur", font=LARGEFONT)
        label.pack(pady=20)

        self.is_timer_running = False
        self.time_left_in_seconds = 0
        self.timer_job = None

        self.instructions = tk.Label(self, text="Choisissez la durée de votre minuteur (secondes) :")
        self.instructions.pack(pady=10)

        self.countdown_text = tk.Label(self, text="00:00", font=LARGEFONT)
        self.countdown_text.pack()

        self.slider = tk.Scale(self, orient=tk.HORIZONTAL, from_=1, to=120, length=300)
        self.slider.pack(pady=10)
        self.slider.set(25)

        self.start_button = tk.Button(self, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self, text="Pause Timer", command=self.pause_timer)
        self.pause_button.pack(pady=10)

        self.reset_button = tk.Button(self, text="Reset Timer", command=self.reset_timer)
        self.reset_button.pack(pady=10)

        self.update_slider(self.switch_value)

    def update_slider(self, switch_value):
        self.switch_value = switch_value
        bg_color = 'white' if switch_value else '#26242f'
        fg_color = '#26242f' if switch_value else 'white'
        trough_color = "#d3d3d3" if switch_value else "#3a3a3a"

        self.slider.config(bg=bg_color, fg=fg_color, troughcolor=trough_color,
                           activebackground=bg_color, highlightthickness=0)

    def start_timer(self):
        if not self.is_timer_running:
            if self.time_left_in_seconds == 0:
                self.time_left_in_seconds = int(self.slider.get())
            if self.time_left_in_seconds > 0:
                self.is_timer_running = True
                self.update_timer()

    def pause_timer(self):
        if self.is_timer_running:
            self.is_timer_running = False
            if self.timer_job is not None:
                self.after_cancel(self.timer_job)
                self.timer_job = None

    def reset_timer(self):
        self.is_timer_running = False
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.time_left_in_seconds = 0
        self.countdown_text.config(text="00:00")
        self.slider.set(25)
        pygame.mixer.music.stop()

    def update_timer(self):
        if self.time_left_in_seconds > 0 and self.is_timer_running:
            minutes, seconds = divmod(self.time_left_in_seconds, 60)
            time_formatted = f"{minutes:02d}:{seconds:02d}"
            self.countdown_text.config(text=time_formatted)
            self.slider.set(self.time_left_in_seconds)
            self.time_left_in_seconds -= 1
            self.timer_job = self.after(1000, self.update_timer)
        elif self.is_timer_running:
            self.countdown_text.config(text="00:00")
            self.time_left_in_seconds = 0
            self.is_timer_running = False
            self.timer_job = None
            self.play_timer_music()

    def play_timer_music(self):
        if self.controller.current_music_index != -1:
            pygame.mixer.music.load(self.musics[self.controller.current_music_index])
            pygame.mixer.music.play()
            # Optionnel: Arrêter après un certain temps
            # self.after(25000, pygame.mixer.music.stop)
        else:
            tk.messagebox.showinfo("Minuteur", "Temps écoulé ! (Aucune musique sélectionnée)")
