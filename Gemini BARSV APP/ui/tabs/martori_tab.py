# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'Martori'.
(Versiune adaptată pentru CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

# Asigură-te că modulele core și widgets există și sunt corecte
try:
    from core import utils
    # CTkScrollableFrame este în customtkinter, nu mai importăm separat
except ImportError as e:
    messagebox.showerror("Eroare Import Martori Tab (CTk)", f"Nu s-a putut importa 'core.utils': {e}")
    # Continuăm fără handler RO dacă importul eșuează
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()


# Prefix pentru cheile variabilelor din acest tab
VAR_PREFIX = "martor_"

# Numărul de martori pentru care creăm cadre
NUM_MARTORI = 4

# Cheile de date pentru UN SINGUR martor (bazate pe original)
# Vom genera chei unice pentru fiecare (ex: martor_1_nume_martor)
DATA_KEYS_PER_MARTOR = [
    "nume_martor",
    "adresa_martor",
    "cnp_martor",
    "tel_martor",
    "text_martor" # Pentru CTkTextbox
]

# --- Funcții Helper Text <-> StringVar (Pot necesita ajustări pt CTkTextbox) ---
# (Copiate - ideal ar fi în utils.py)
_text_widget_updating = {}
def _update_text_from_var(text_widget, string_var):
    widget_id = str(text_widget)
    if _text_widget_updating.get(widget_id): return
    try:
        _text_widget_updating[widget_id] = True
        current_text = text_widget.get("0.0", "end")
        if current_text.endswith('\n'): current_text = current_text[:-1]
        new_text = string_var.get()
        if current_text != new_text:
            text_widget.delete("0.0", "end")
            if new_text: text_widget.insert("0.0", new_text)
    except Exception as e:
        print(f"Eroare în _update_text_from_var pentru {text_widget}: {e}")
    finally:
        _text_widget_updating[str(text_widget)] = False

def _update_var_from_text(text_widget, string_var):
    widget_id = str(text_widget)
    if _text_widget_updating.get(widget_id): return
    try:
        _text_widget_updating[widget_id] = True
        current_var_value = string_var.get()
        new_widget_value = text_widget.get("0.0", "end")
        if new_widget_value.endswith('\n'): new_widget_value = new_widget_value[:-1]
        if current_var_value != new_widget_value:
            string_var.set(new_widget_value)
    except Exception as e:
        print(f"Eroare în _update_var_from_text pentru {text_widget}: {e}")
    finally:
         _text_widget_updating[str(text_widget)] = False
# --- Sfârșit Funcții Helper ---


def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'Martori'
    folosind widget-uri CustomTkinter.

    Args:
        parent_container (ctk.CTkFrame): Containerul oferit de CTkTabview.
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_columnconfigure(0, weight=1)

    # --- Cadru Scrollabil pentru Martori ---
    scroll_area = ctk.CTkScrollableFrame(parent_container, label_text="Martori / Persoane prezente")
    scroll_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    scroll_area.columnconfigure(0, weight=1) # Permite extinderea cadrelor martorilor

    # --- Definire Variabile Tkinter și Creare Cadre Martori ---
    for i in range(1, NUM_MARTORI + 1):
        martor_vars = {} # Variabile locale pentru acest martor
        for key_template in DATA_KEYS_PER_MARTOR:
            # Cheia originală (ex: nume_martor1)
            data_key = f"{key_template}{i}"
            # Cheia unică în data_vars (ex: martor_1_nume_martor)
            var_key = f"{VAR_PREFIX}{i}_{key_template}"

            if var_key not in app_instance.data_vars:
                app_instance.data_vars[var_key] = tk.StringVar()
            # Stocăm referința local pentru a o pasa la create_martor_frame
            martor_vars[data_key] = app_instance.data_vars[var_key]

        # Creează cadrul pentru martorul curent
        martor_frame = _create_martor_frame(scroll_area, i, martor_vars)
        # Adaugă cadrul în zona scrollabilă
        martor_frame.pack(fill="x", expand=False, padx=5, pady=10)


def _create_martor_frame(parent, martor_number, martor_vars):
    """
    Creează un cadru (CTkFrame) cu widget-uri pentru un singur martor.

    Args:
        parent (ctk.CTkFrame): Părintele (CTkScrollableFrame).
        martor_number (int): Numărul martorului.
        martor_vars (dict): Dicționarul cu variabilele Tkinter pentru acest martor.

    Returns:
        ctk.CTkFrame: Cadrul creat.
    """
    frame = ctk.CTkFrame(parent, border_width=1, corner_radius=10)
    frame.columnconfigure(1, weight=1) # Extinde câmpul nume/adresă

    ctk.CTkLabel(frame, text=f" Martor {martor_number} ", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=4, pady=(5, 10), padx=10, sticky="ew")

    r = 1 # Rând intern
    # Nume
    ctk.CTkLabel(frame, text="Nume, prenume:").grid(row=r, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nume = ctk.CTkEntry(frame, width=300,
                              textvariable=martor_vars.get(f'nume_martor{martor_number}'))
    entry_nume.grid(row=r, column=1, padx=2, pady=2, sticky="ew")
    entry_nume.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame, text="cu domiciliul în:").grid(row=r, column=2, padx=(10,5), pady=2, sticky="w")
    r += 1

    # Adresa
    entry_adresa = ctk.CTkEntry(frame, placeholder_text="Adresa completă...",
                                textvariable=martor_vars.get(f'adresa_martor{martor_number}'))
    entry_adresa.grid(row=r, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
    entry_adresa.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    r += 1

    # CNP și Telefon
    ctk.CTkLabel(frame, text="CNP:").grid(row=r, column=0, padx=(10,2), pady=2, sticky="w")
    entry_cnp = ctk.CTkEntry(frame, width=150,
                             textvariable=martor_vars.get(f'cnp_martor{martor_number}'))
    entry_cnp.grid(row=r, column=1, padx=2, pady=2, sticky="w")

    ctk.CTkLabel(frame, text="Telefon:").grid(row=r, column=2, padx=(10,2), pady=2, sticky="w")
    entry_tel = ctk.CTkEntry(frame, width=150,
                             textvariable=martor_vars.get(f'tel_martor{martor_number}'))
    entry_tel.grid(row=r, column=3, padx=(2,10), pady=2, sticky="w")
    r += 1

    # Declarație
    ctk.CTkLabel(frame, text="Acesta declară verbal următoarele:").grid(
        row=r, column=0, columnspan=4, padx=10, pady=(10, 2), sticky="w")
    r += 1
    textbox_decl = ctk.CTkTextbox(frame, height=100, wrap=tk.WORD)
    textbox_decl.grid(row=r, column=0, columnspan=4, padx=10, pady=(0,10), sticky="ew")
    textbox_decl.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    # Legare la StringVar
    decl_var = martor_vars.get(f'text_martor{martor_number}')
    if decl_var:
        init_decl = decl_var.get()
        if init_decl: textbox_decl.insert("1.0", init_decl)
        textbox_decl.bind("<FocusOut>", lambda event, w=textbox_decl, v=decl_var: _update_var_from_text(w, v))
    r += 1

    # Configurare extindere pentru Textbox
    frame.rowconfigure(r-1, weight=1)

    return frame


# --- Funcții get/load data (adaptate) ---

def get_data(app_instance):
    """
    Colectează datele din variabilele Tkinter pentru toți martorii.

    Args:
        app_instance (AppWindow): Instanța principală a aplicației.

    Returns:
        dict: Dicționar cu datele din acest tab.
    """
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din tab Martori (CTk)...")

    for i in range(1, NUM_MARTORI + 1):
        for key_template in DATA_KEYS_PER_MARTOR:
            original_key = f"{key_template}{i}" # Cheia originală (ex: nume_martor1)
            var_key = f"{VAR_PREFIX}{i}_{key_template}" # Cheia variabilei (ex: martor_1_nume_martor)

            if var_key in data_vars:
                try:
                    # Citim direct din variabilele Tkinter
                    # Presupunem că _update_var_from_text a fost apelat pentru Textbox
                    data[original_key] = data_vars[var_key].get()
                except Exception as e:
                    print(f"Eroare la citirea variabilei {var_key}: {e}", file=sys.stderr)
                    data[original_key] = None
            else:
                # Acest lucru nu ar trebui să se întâmple dacă create_tab_content a rulat corect
                print(f"Avertisment: Cheia {var_key} nu a fost găsită la colectare.", file=sys.stderr)
                data[original_key] = None
    return data

def load_data(app_instance, data_to_load):
    """
    Încarcă datele primite în variabilele Tkinter pentru martori.

    Args:
        app_instance (AppWindow): Instanța principală a aplicației.
        data_to_load (dict): Dicționarul cu datele de încărcat.
    """
    data_vars = app_instance.data_vars
    print("Încărcare date în tab Martori (CTk)...")

    for i in range(1, NUM_MARTORI + 1):
        for key_template in DATA_KEYS_PER_MARTOR:
            original_key = f"{key_template}{i}"
            var_key = f"{VAR_PREFIX}{i}_{key_template}"

            if original_key in data_to_load and var_key in data_vars:
                try:
                    target_var = data_vars[var_key]
                    value_from_data = data_to_load[original_key]

                    # Setăm variabila (va actualiza și CTkTextbox prin trace/load)
                    if isinstance(target_var, tk.StringVar):
                        value_to_set = str(value_from_data) if value_from_data is not None else ""
                        target_var.set(value_to_set)
                    # else: Nu avem alte tipuri aici

                except tk.TclError as e:
                     print(f"Avertisment: Nu s-a putut seta valoarea pentru {var_key}: {e}", file=sys.stderr)
                except Exception as e:
                     print(f"Eroare la încărcarea datei pentru {var_key}: {e}", file=sys.stderr)

