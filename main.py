import datetime
import tkinter as tk
from threading import Thread
from tkinter import messagebox
import time
import math
import pygame
from horloge import Horloge
from horloge import DHorloge
from alarme import Alarme
from minuteur import Minuteur
from chronometre import Chronometre

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

class tKinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Horloge Multifonctions")
        self.geometry("500x750")

        # Cadre supérieur pour les étiquettes de temps et de musique
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Ajout du label pour l'heure de l'application en haut à gauche
        self.app_time_label = tk.Label(top_frame, text="", font=("Tahoma", 12))
        self.app_time_label.pack(side="left", anchor="nw")

        # Ajout du label pour le nom de la musique en haut à droite
        self.music_name_label = tk.Label(top_frame, text="", font=("Tahoma", 10))
        self.music_name_label.pack(side="right", anchor="ne")

        # Création du conteneur
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Ajout des images pour le mode clair et sombre
        self.light = tk.PhotoImage(file=r"Image\dark.png")
        self.dark = tk.PhotoImage(file=r"Image\light.png")
        self.music = tk.PhotoImage(file=r"Image\music.png")
        self.clock = tk.PhotoImage(file=r"Image\clock.png")

        # Ajout des musiques
        self.musics = [r"Music\Sonnerie 2.mp3", r"Music\Sonnerie 1.mp3"]
        self.current_music_index = -1
        pygame.mixer.init()
        self.update_music_label()

        # Paramètre initial du thème
        self.switch_value = True
        self.time_offset = +2  # Décalage horaire en heures
        self.manual_time = None  # Initialisation de l'heure manuelle
        self.create_navigation_bar()

        # Initialisation des frames
        self.frames = {}
        for F in (Horloge, DHorloge, Alarme, Minuteur, Chronometre):
            frame = F(container, self, self.switch_value, self.musics)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.toggle_theme()
        self.show_frame(Horloge)
        self.update_app_time()

    def update_music_label(self):
        if self.current_music_index == -1:
            music_name = "Aucune musique"
        else:
            full_path = self.musics[self.current_music_index]
            # Extraire le nom du fichier sans l'extension
            base_name = full_path.split('\\')[-1]
            music_name = base_name.rsplit('.', 1)[0]  # Sépare le nom du fichier et l'extension
        self.music_name_label.config(text=music_name)

    def update_app_time(self):
        current_time = self.get_datetime_with_utc()
        now = current_time.strftime("%H:%M:%S")
        region = self.get_region_from_utc_offset(self.time_offset)
        self.app_time_label.config(text=f"Fuseau Horaire: {now} (UTC{self.time_offset:+}) - {region}")
        for frame in self.frames.values():
            if isinstance(frame, (Horloge, DHorloge)):
                frame.update_clock()
        self.after(1000, self.update_app_time)

    def get_region_from_utc_offset(self, offset):
        regions = {
            -12: "Baker Island Time (BIT)",
            -11: "Samoa Time (SST)",
            -10: "Hawaii-Aleutian Time (HST)",
            -9: "Alaska Time (AKST)",
            -8: "Pacific Time (PST)",
            -7: "Mountain Time (MST)",
            -6: "Central Time (CST)",
            -5: "Eastern Time (EST)",
            -4: "Atlantic Time (AST)",
            -3: "West Africa Time (WAT)",
            -2: "Mid-Atlantic Time (MAT)",
            -1: "Greenwich Mean Time (GMT-1)",
            0: "Greenwich Mean Time (GMT)",
            1: "Central European Time (CET)",
            2: "Eastern European Time (EET)",
            3: "Moscow Time (MSK)",
            4: "Astrakhan Time (AST)",
            5: "Pakistan Time (PKT)",
            6: "Bangladesh Time (BDT)",
            7: "Krasnoyarsk Time (KRAT)",
            8: "China Standard Time (CST)",
            9: "Japan Standard Time (JST)",
            10: "Australian Western Standard Time (AWST)",
            11: "Solomon Islands Time (SBT)",
            12: "Kiribati Time (GILT)",
            13: "Phoenix Islands Time (PHOT)",
            14: "Line Islands Time (LINT)",
        }
        return regions.get(offset, "Région inconnue")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def toggle_theme(self):
        fg_color = ""
        bg_color = ""
        entry_bg_color = ""
        nav_bg_color = ""

        if self.switch_value:
            self.switch.config(image=self.dark, bg="#26242f", activebackground="#26242f")
            bg_color = "#26242f"
            fg_color = "white"
            entry_bg_color = "#3a3a3a"
            nav_bg_color = "#26242f"
            self.switch_value = False
        else:
            self.switch.config(image=self.light, bg="white", activebackground="white")
            bg_color = "white"
            fg_color = "black"
            entry_bg_color = "white"
            nav_bg_color = "white"
            self.switch_value = True

        self.config(bg=bg_color)
        self.app_time_label.master.config(bg=bg_color)
        self.app_time_label.config(bg=bg_color, fg=fg_color)
        self.music_name_label.config(bg=bg_color, fg=fg_color)

        for frame in self.frames.values():
            frame.config(bg=bg_color)
            for widget in frame.winfo_children():
                widget_type = widget.winfo_class()
                if widget_type == "Label":
                    widget.config(bg=bg_color, fg=fg_color)
                elif widget_type == "Button":
                    widget.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
                elif widget_type == "Entry":
                    widget.config(bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
                elif widget_type == "Canvas":
                    widget.config(bg=bg_color)
                elif widget_type == "Scale":
                    widget.config(bg=bg_color, fg=fg_color, troughcolor=entry_bg_color,
                                  activebackground=bg_color, highlightthickness=0)

        # Modification de la barre de navigation
        self.navigation_bar.config(bg=nav_bg_color)
        for child in self.navigation_bar.winfo_children():
            child.config(bg=nav_bg_color)
            for grandchild in child.winfo_children():
                if isinstance(grandchild, tk.Button):
                    grandchild.config(bg=nav_bg_color, fg=fg_color, activebackground=nav_bg_color,
                                      activeforeground=fg_color,
                                      bd=0, highlightthickness=0)
                elif isinstance(grandchild, tk.Frame):
                    grandchild.config(bg=nav_bg_color)
                    for great_grandchild in grandchild.winfo_children():
                        if isinstance(great_grandchild, tk.Button):
                            great_grandchild.config(bg=nav_bg_color, fg=fg_color, activebackground=nav_bg_color,
                                                    activeforeground=fg_color,
                                                    bd=0, highlightthickness=0)

        if Horloge in self.frames:
            self.frames[Horloge].update_theme(self.switch_value)
        if Minuteur in self.frames:
            self.frames[Minuteur].update_slider(self.switch_value)
        if Alarme in self.frames:
            self.frames[Alarme].update_theme(self.switch_value)
        if hasattr(self, 'timezone_window') and self.timezone_window:
            self.update_timezone_window_theme(self.switch_value)

    def toggle_music(self):
        self.current_music_index = (self.current_music_index + 1) % len(self.musics)
        pygame.mixer.music.load(self.musics[self.current_music_index])
        pygame.mixer.music.play()
        self.update_music_label()
        self.after(3000, pygame.mixer.music.stop)

    def get_datetime_with_utc(self):
        tz = datetime.timezone(datetime.timedelta(hours=self.time_offset))
        current_time = datetime.datetime.now(tz)
        return current_time

    def open_timezone_window(self):
        self.timezone_window = tk.Toplevel(self)
        self.timezone_window.title("Changer Fuseau Horaire")
        self.timezone_window.geometry("400x400")

        # Déterminer la couleur selon switch_value
        if self.switch_value:
            bg_color = "white"
            fg_color = "black"
            entry_bg_color = "white"
        else:
            bg_color = "#26242f"
            fg_color = "white"
            entry_bg_color = "#3a3a3a"

        self.timezone_window.config(bg=bg_color)

        # Changer heure selon UTC
        self.create_timezone_section(bg_color, fg_color, entry_bg_color)

    def create_timezone_section(self, bg_color, fg_color, entry_bg_color):
        time_title = tk.Label(self.timezone_window, text="Nouveau Fuseau UTC : ", font=smallfont, bg=bg_color, fg=fg_color)
        time_title.pack(pady=10)

        self.new_time_entry_var = tk.StringVar(value=str(self.time_offset))
        new_time_entry = tk.Entry(self.timezone_window, textvariable=self.new_time_entry_var, font=smallfont, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        new_time_entry.pack(pady=5)

        change_utc_btn = tk.Button(self.timezone_window, text="Changer l'UTC", command=self.update_timezone, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
        change_utc_btn.pack(pady=5)

    def update_timezone(self):
        try:
            new_offset = int(self.new_time_entry_var.get())
            if -12 <= new_offset <= 14:
                self.time_offset = new_offset
                self.timezone_window.destroy()
                self.update_app_time()  # Mettre à jour immédiatement l'affichage
            else:
                messagebox.showerror("Erreur", "Le décalage horaire doit être entre -12 et +14.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier.")

    def update_timezone_window_theme(self, switch_value):
        if switch_value:
            bg_color = "white"
            fg_color = "black"
            entry_bg_color = "white"
        else:
            bg_color = "#26242f"
            fg_color = "white"
            entry_bg_color = "#3a3a3a"

        self.timezone_window.config(bg=bg_color)

        for widget in self.timezone_window.winfo_children():
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

    def create_navigation_bar(self):
        self.navigation_bar = tk.Frame(self)
        self.navigation_bar.pack(side="bottom", fill="x")

        switch_frame = tk.Frame(self.navigation_bar)
        switch_frame.pack(side="top", fill="x", pady=5)

        self.switch = tk.Button(switch_frame, image=self.light, command=self.toggle_theme, bd=0, highlightthickness=0)
        self.switch.pack(side="left", expand=True, fill="x")

        music = tk.Button(switch_frame, image=self.music, command=self.toggle_music, bd=0, highlightthickness=0)
        music.pack(side="left", expand=True, fill="x")

        timezone = tk.Button(switch_frame, image=self.clock, command=self.open_timezone_window, bd=0,
                             highlightthickness=0)
        timezone.pack(side="left", expand=True, fill="x")

        button_frame = tk.Frame(self.navigation_bar)
        button_frame.pack(side="top", fill="x", pady=5)

        btn1 = tk.Button(button_frame, text="Horloge", command=lambda: self.show_frame(Horloge), bd=0,
                         highlightthickness=0)
        btn2 = tk.Button(button_frame, text="Alarme", command=lambda: self.show_frame(Alarme), bd=0,
                         highlightthickness=0)
        btn3 = tk.Button(button_frame, text="Minuteur", command=lambda: self.show_frame(Minuteur), bd=0,
                         highlightthickness=0)
        btn4 = tk.Button(button_frame, text="Chronomètre", command=lambda: self.show_frame(Chronometre), bd=0,
                         highlightthickness=0)

        btn1.pack(side="left", expand=True, fill="x")
        btn2.pack(side="left", expand=True, fill="x")
        btn3.pack(side="left", expand=True, fill="x")
        btn4.pack(side="left", expand=True, fill="x")

if __name__ == "__main__":
    app = tKinterApp()
    app.mainloop()
