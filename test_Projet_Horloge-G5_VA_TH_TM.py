import datetime
import tkinter as tk
from threading import Thread
from tkinter import messagebox
import time
import math
import pygame

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
        self.musics = [r"Music\reveil.mp3", r"Music\KJF 4.mp3", r"Music\PLL - Maya.mp3",
                       r"Music\TKS 2G - Celibataire Polygame.mp3",
                       r"Music\Sébastien Patoche - Quand Il Pète Il Troue Son Slip.mp3"]
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


class BaseFrame(tk.Frame):
    def __init__(self, parent, controller, switch_value, musics):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.switch_value = switch_value
        self.musics = musics

class Horloge(BaseFrame):
    def __init__(self, parent, controller, switch_value, musics):
        super().__init__(parent, controller, switch_value, musics)

        # Configuration des constantes de classe
        self.IMAGES = {
            'light': r'Image\white_dial.png',
            'dark': r'Image\black_dial.png'
        }
        self.COLORS = {
            'light': {'hands': 'black', 'seconds': 'red'},
            'dark': {'hands': 'white', 'seconds': 'red'}
        }

        # Initialisation des dimensions de l'horloge
        self.center_x = 200
        self.center_y = 200
        self.seconds_hand_len = 95
        self.minutes_hand_len = 80
        self.hours_hand_len = 60

        # Création et placement des widgets
        label = tk.Label(self, text="Horloge", font=LARGEFONT)
        label.pack(pady=10)

        # Canvas pour l'horloge
        self.canvas = tk.Canvas(self, width=400, height=400, highlightthickness=0)
        self.canvas.pack(pady=15)

        # Bouton pour passer à l'horloge digitale
        btnDClock = tk.Button(self, text="Horloge Digitale", command=lambda: controller.show_frame(DHorloge))
        btnDClock.pack(pady=10)

        # Initialisation de l'horloge
        self.update_theme(self.switch_value)

    def update_theme(self, switch_value):
        """Met à jour le thème de l'horloge selon la valeur du commutateur"""
        self.switch_value = switch_value

        # Nettoie le canvas
        self.canvas.delete("all")

        # Sélectionne le thème approprié
        theme = 'light' if switch_value else 'dark'
        bg_file = self.IMAGES.get(theme)
        self.hands_color = self.COLORS[theme]['hands']
        self.seconds_color = self.COLORS[theme]['seconds']

        # Charge l'image de fond
        if bg_file:
            try:
                self.bg = tk.PhotoImage(file=bg_file)
                self.canvas.create_image(self.center_x, self.center_y, image=self.bg)
            except tk.TclError:
                bg_file = None  # Fallback si l'image n'est pas trouvée

        if not bg_file:
            bg_color_canvas = 'white' if switch_value else '#26242f'
            self.canvas.config(bg=bg_color_canvas)
            self.canvas.create_oval(10, 10, 390, 390, fill=bg_color_canvas, outline='gray')

        # Crée les aiguilles
        self.seconds_hand = self.canvas.create_line(
            self.center_x, self.center_y,
            self.center_x, self.center_y,
            width=1.5, fill=self.seconds_color, tag="hand"
        )

        self.minutes_hand = self.canvas.create_line(
            self.center_x, self.center_y,
            self.center_x, self.center_y,
            width=2, fill=self.hands_color, tag="hand"
        )

        self.hours_hand = self.canvas.create_line(
            self.center_x, self.center_y,
            self.center_x, self.center_y,
            width=4, fill=self.hands_color, tag="hand"
        )

        # Ajoute un point central
        self.canvas.create_oval(
            self.center_x - 5, self.center_y - 5,
            self.center_x + 5, self.center_y + 5,
            fill=self.hands_color, outline=""
        )

        # Met à jour l'horloge
        self.update_clock()

    def update_clock(self):
        """Met à jour la position des aiguilles selon l'heure actuelle"""
        if self.controller.manual_time:
            current_time = self.controller.manual_time
        else:
            current_time = self.controller.get_datetime_with_utc()

        hours = int(current_time.strftime("%I"))
        minutes = int(current_time.strftime("%M"))
        seconds = int(current_time.strftime("%S"))

        # Calcule la position de l'aiguille des secondes (6 degrés par seconde)
        seconds_angle = math.radians(seconds * 6)
        seconds_x = self.center_x + self.seconds_hand_len * math.sin(seconds_angle)
        seconds_y = self.center_y - self.seconds_hand_len * math.cos(seconds_angle)
        self.canvas.coords(self.seconds_hand, self.center_x, self.center_y, seconds_x, seconds_y)

        # Calcule la position de l'aiguille des minutes (6 degrés par minute)
        minutes_angle = math.radians(minutes * 6)
        minutes_x = self.center_x + self.minutes_hand_len * math.sin(minutes_angle)
        minutes_y = self.center_y - self.minutes_hand_len * math.cos(minutes_angle)
        self.canvas.coords(self.minutes_hand, self.center_x, self.center_y, minutes_x, minutes_y)

        # Calcule la position de l'aiguille des heures (30 degrés par heure + ajustement pour minutes et secondes)
        hours_angle = math.radians(hours * 30 + minutes * 0.5 + seconds * (1 / 120))
        hours_x = self.center_x + self.hours_hand_len * math.sin(hours_angle)
        hours_y = self.center_y - self.hours_hand_len * math.cos(hours_angle)
        self.canvas.coords(self.hours_hand, self.center_x, self.center_y, hours_x, hours_y)

        # Met à jour les couleurs si le thème a changé
        theme = 'light' if self.controller.switch_value else 'dark'
        hands_color = self.COLORS[theme]['hands']
        seconds_color = self.COLORS[theme]['seconds']
        if self.canvas.itemcget(self.minutes_hand, "fill") != hands_color:
            self.canvas.itemconfig(self.minutes_hand, fill=hands_color)
            self.canvas.itemconfig(self.hours_hand, fill=hands_color)
            self.canvas.itemconfig(self.seconds_hand, fill=seconds_color)
            # Recréer le point central pour la couleur
            self.canvas.create_oval(
                self.center_x - 5, self.center_y - 5,
                self.center_x + 5, self.center_y + 5,
                fill=hands_color, outline=""
            )

        # Planifie la prochaine mise à jour
        self.after(1000, self.update_clock)

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

if __name__ == "__main__":
    app = tKinterApp()
    app.mainloop()
