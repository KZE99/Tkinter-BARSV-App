# -*- coding: utf-8 -*-
"""
Modul pentru widget-ul reutilizabil ScrollableFrame.

Oferă un cadru (frame) cu o bară de scroll verticală,
permițând conținutului interior să depășească înălțimea vizibilă.
"""

import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    """
    Un cadru ttk.Frame care suportă scroll vertical.

    Conținutul trebuie adăugat la atributul 'scrollable_frame'.
    """
    def __init__(self, container, bar_width=16, *args, **kwargs):
        """
        Inițializează cadrul scrollabil.

        Args:
            container: Widget-ul părinte în care va fi plasat acest cadru.
            bar_width (int): Lățimea barei de scroll în pixeli.
            *args, **kwargs: Argumente suplimentare pasate către ttk.Frame.
        """
        super().__init__(container, *args, **kwargs)

        # --- Creare Canvas și Scrollbar ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        # Scrollbar vertical
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # Scrollbar orizontal (opțional, dezactivat implicit)
        # self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        # Configurează canvas-ul să folosească scrollbar-ul(ele)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # self.canvas.configure(xscrollcommand=self.hsb.set) # Pentru scroll orizontal

        # --- Aranjare Canvas și Scrollbar în cadrul principal ---
        self.vsb.pack(side="right", fill="y")
        # self.hsb.pack(side="bottom", fill="x") # Pentru scroll orizontal
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Creare Cadru Interior (în Canvas) ---
        # Acesta este cadrul unde se va adăuga conținutul efectiv.
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Plasează cadrul interior în canvas folosind create_window
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw", tags="self.scrollable_frame"
        )

        # --- Binding Evenimente ---
        # Actualizează scrollregion când dimensiunea cadrului interior se schimbă
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        # Actualizează lățimea cadrului interior la lățimea canvas-ului
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        # Permite scroll cu rotița mouse-ului
        self.bind_mousewheel(self) # Leagă pe cadrul principal
        self.bind_mousewheel(self.canvas) # Leagă și pe canvas
        self.bind_mousewheel(self.scrollable_frame) # Leagă și pe cadrul interior
        # Leagă și pentru widget-urile din interior (important!)
        self.scrollable_frame.bind("<Enter>", self._bind_children_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_children_mousewheel)


    def _on_frame_configure(self, event=None):
        """Resetează scrollregion-ul canvas-ului pentru a include cadrul interior."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Ajustează lățimea cadrului interior la lățimea canvas-ului."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        """Gestionează evenimentul de scroll cu rotița mouse-ului."""
        # Determină direcția și magnitudinea scroll-ului (specific platformei)
        if event.num == 5 or event.delta < 0: # Scroll jos (Linux/Windows)
            delta = 1
        elif event.num == 4 or event.delta > 0: # Scroll sus (Linux/Windows)
            delta = -1
        else: # Necunoscut
            delta = 0

        # Aplică scroll pe canvas
        self.canvas.yview_scroll(delta, "units")
        # Returnează "break" pentru a preveni propagarea evenimentului (opțional)
        # return "break"

    def bind_mousewheel(self, widget):
        """Leagă evenimentul de scroll cu rotița la widget-ul specificat."""
        # Folosește evenimente specifice platformei pentru mouse wheel
        widget.bind('<Button-4>', self._on_mousewheel, add='+') # Linux scroll sus
        widget.bind('<Button-5>', self._on_mousewheel, add='+') # Linux scroll jos
        widget.bind('<MouseWheel>', self._on_mousewheel, add='+') # Windows/MacOS

    def unbind_mousewheel(self, widget):
        """Dezleagă evenimentul de scroll cu rotița de la widget-ul specificat."""
        widget.unbind('<Button-4>')
        widget.unbind('<Button-5>')
        widget.unbind('<MouseWheel>')

    def _bind_children_mousewheel(self, event=None):
        """Leagă evenimentul de scroll la toți copiii cadrului interior."""
        self.bind_mousewheel(self.scrollable_frame)
        for child in self.scrollable_frame.winfo_children():
            self.bind_mousewheel(child)

    def _unbind_children_mousewheel(self, event=None):
        """Dezleagă evenimentul de scroll de la toți copiii cadrului interior."""
        self.unbind_mousewheel(self.scrollable_frame)
        for child in self.scrollable_frame.winfo_children():
            self.unbind_mousewheel(child)

    def update_scrollregion(self):
        """Metodă publică pentru a forța actualizarea scrollregion-ului."""
        self.canvas.update_idletasks() # Asigură că toate modificările de layout sunt procesate
        self._on_frame_configure()

# --- Cod de Test (opțional) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test ScrollableFrame")
    root.geometry("400x300")

    # Creează instanța ScrollableFrame
    scroll_frame_widget = ScrollableFrame(root)
    scroll_frame_widget.pack(fill="both", expand=True, padx=10, pady=10)

    # Adaugă conținut în cadrul interior (scrollable_frame)
    for i in range(30):
        # Alternează culorile pentru vizibilitate
        bg_color = "lightblue" if i % 2 == 0 else "lightyellow"
        label = tk.Label(
            scroll_frame_widget.scrollable_frame, # Adaugă la cadrul INTERIOR!
            text=f"Etichetă de test numărul {i+1}",
            pady=5,
            background=bg_color
        )
        label.pack(fill="x", padx=5, pady=2)

        entry = ttk.Entry(scroll_frame_widget.scrollable_frame)
        entry.pack(fill="x", padx=5, pady=2)
        entry.insert(0, f"Câmp de intrare {i+1}")

    # Buton în afara zonei scrollabile
    button = ttk.Button(root, text="Buton Exterior", command=lambda: print("Click!"))
    button.pack(pady=10)

    root.mainloop()
