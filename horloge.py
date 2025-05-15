import tkinter as tk
import math
from base_frame import BaseFrame

LARGEFONT = ("Georgia", 35)
smallfont = ("Tahoma", 20)

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
