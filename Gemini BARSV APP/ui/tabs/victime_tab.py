# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'Victime'.
(Versiune adaptată pentru CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk # Importăm customtkinter
from tkinter import messagebox
import sys
import traceback

# Asigură-te că modulele core și widgets există și sunt corecte
try:
    from core import utils
    # Importăm widget-ul victim_frame (care va trebui și el adaptat la CTk)
    from ui.widgets import victim_frame
except ImportError as e:
    messagebox.showerror("Eroare Import Victime (CTk)", f"Nu s-au putut importa modulele necesare (utils, victim_frame): {e}")
    sys.exit(1)


# Prefix pentru cheile variabilelor din acest tab
VAR_PREFIX = "victime_"

# Cheile de date pentru O SINGURĂ victimă
DATA_KEYS_PER_VICTIM = [
    "nume_victimax", "cnp_victimax", "adresa_victimax", "cetatenie_victimax",
    "tel_victimax", "calitate_victimax", "diagnostic_victimax",
    "radio_prezent_cfl_group",
    "nota_vinovatie_victimax", "articol_victimax",
    "declaratie_victimax"
]

# --- Funcții Helper Text <-> StringVar (dacă sunt încă necesare pentru CTkTextbox) ---
# CTkTextbox are propria metodă .get() și .insert(), dar legătura cu StringVar
# poate fi încă utilă, deși implementarea poate necesita ajustări.
# (Păstrăm funcțiile deocamdată, dar s-ar putea să nu fie necesare/optime pentru CTkTextbox)
_text_widget_updating = {}
def _update_text_from_var(text_widget, string_var):
    # ... (codul funcției helper, posibil necesită adaptare pentru CTkTextbox) ...
    pass # Implementare placeholder
def _update_var_from_text(text_widget, string_var):
    # ... (codul funcției helper, posibil necesită adaptare pentru CTkTextbox) ...
    pass # Implementare placeholder
# --- Sfârșit Funcții Helper ---


# --- MODIFICARE NUME FUNCȚIE ---
def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'Victime'
    folosind widget-uri CustomTkinter.

    Args:
        parent_container (ctk.CTkFrame): Containerul oferit de CTkTabview.
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    # Nu mai returnăm un frame, populăm direct parent_container
    parent_container.grid_rowconfigure(0, weight=1) # Permite extinderea CTkScrollableFrame
    parent_container.grid_columnconfigure(0, weight=1)

    # --- **ÎNLOCUIRE:** Folosim CTkScrollableFrame ---
    # Nu mai avem nevoie de tab_frame separat, adăugăm direct în container
    victims_scrollable_area = ctk.CTkScrollableFrame(parent_container)
    victims_scrollable_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5,0))
    # Stocăm referința în tab_frame (parent_container) pentru acces ulterior dacă e nevoie
    parent_container.victims_scrollable_area = victims_scrollable_area
    # --- SFÂRȘIT ÎNLOCUIRE ---

    # --- Buton Adăugare Victimă (folosind CTkButton) ---
    add_button_frame = ctk.CTkFrame(parent_container, fg_color="transparent") # Frame transparent pentru buton
    add_button_frame.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    add_button = ctk.CTkButton(
        add_button_frame,
        text="+ Adaugă Victimă",
        # Pasează containerul tab-ului la funcția de adăugare
        command=lambda: add_new_victim_frame(parent_container, app_instance)
    )
    add_button.pack()

    # --- Adaugă prima victimă implicit ---
    # Pasează containerul tab-ului
    add_new_victim_frame(parent_container, app_instance)

    # TODO: Adaugă secțiunea pentru Martori (folosind widget-uri CTk)


def add_new_victim_frame(tab_container, app_instance, data_to_load=None, victim_index=None):
    """
    Adaugă un nou cadru pentru o victimă în CTkScrollableFrame.
    Creează variabilele Tkinter și UI-ul CTk.

    Args:
        tab_container (ctk.CTkFrame): Containerul tab-ului ('Victime').
        app_instance (AppWindow): Instanța principală a aplicației.
        data_to_load (dict, optional): Datele de încărcat.
        victim_index (int, optional): Indexul specific.
    """
    if victim_index is None:
        current_victim_count = len(app_instance.victim_frames)
        victim_number = current_victim_count + 1
    else:
        victim_number = victim_index

    print(f"Adăugare cadru CTk pentru Victima Nr. {victim_number}")

    victim_vars = {}
    for key_template in DATA_KEYS_PER_VICTIM:
        base_key = key_template
        data_key = f"{base_key}{victim_number}"
        var_key = f"{VAR_PREFIX}{victim_number}_{base_key}"

        if var_key not in app_instance.data_vars:
            if key_template == "nota_vinovatie_victimax":
                var = tk.IntVar(value=0) # Păstrăm IntVar pentru CheckBox
            else:
                # Păstrăm StringVar pentru Entry, ComboBox, RadioButton, Textbox
                var = tk.StringVar()
                if key_template == "radio_prezent_cfl_group":
                    var.set("NU") # Default
            app_instance.data_vars[var_key] = var
        else:
            var = app_instance.data_vars[var_key]
        victim_vars[data_key] = var

    try:
        # --- **MODIFICARE:** Apelăm funcția adaptată din victim_frame ---
        # Aceasta trebuie să returneze un CTkFrame și să folosească widget-uri CTk
        # Părintele este direct CTkScrollableFrame
        new_victim_frame_widget = victim_frame.create_victim_ui_ctk(
            tab_container.victims_scrollable_area, # Adăugăm direct în scroll area
            victim_number,
            victim_vars
        )
        # --- SFÂRȘIT MODIFICARE ---

        # Adăugăm noul cadru (CTkFrame) în zona scrollabilă
        # CTkScrollableFrame folosește pack/grid intern, noi adăugăm la el
        new_victim_frame_widget.pack(pady=10, padx=5, fill='x', expand=False)

    except AttributeError as e:
         # Eroare dacă victim_frame.py nu are încă funcția adaptată 'create_victim_ui_ctk'
         messagebox.showerror("Eroare Widget Victimă", f"Funcția 'create_victim_ui_ctk' lipsește sau conține erori în 'ui/widgets/victim_frame.py'.\n{e}")
         print(f"Eroare: 'create_victim_ui_ctk' nu a fost găsit în victim_frame.py", file=sys.stderr)
         traceback.print_exc(file=sys.stderr)
         return
    except Exception as e:
        messagebox.showerror("Eroare Creare UI Victimă (CTk)", f"Nu s-a putut crea interfața pentru victima {victim_number}:\n{e}")
        print(f"Eroare detaliată la creare UI victimă {victim_number} (CTk):", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return

    app_instance.victim_frames.append(new_victim_frame_widget) # Stocăm referința la CTkFrame

    if data_to_load:
        print(f"Încărcare date CTk pentru Victima {victim_number}...")
        for key_template in DATA_KEYS_PER_VICTIM:
            base_key = key_template
            data_key = f"{base_key}{victim_number}"
            var_key = f"{VAR_PREFIX}{victim_number}_{base_key}"

            if data_key in data_to_load and var_key in app_instance.data_vars:
                try:
                    target_var = app_instance.data_vars[var_key]
                    value_from_data = data_to_load[data_key]

                    # Setăm variabilele Tkinter (IntVar, StringVar)
                    # Funcția create_victim_ui_ctk trebuie să lege aceste variabile
                    # la widget-urile CTk corespunzătoare.
                    if isinstance(target_var, tk.IntVar):
                        value_to_set = 1 if value_from_data else 0
                        target_var.set(value_to_set)
                    elif isinstance(target_var, tk.StringVar):
                        value_to_set = str(value_from_data) if value_from_data is not None else ""
                        target_var.set(value_to_set)
                    else:
                        print(f"Avertisment: Tip necunoscut pentru variabila {var_key} la încărcare.")

                except tk.TclError as e:
                    print(f"Avertisment: Nu s-a putut seta valoarea pentru {var_key} (cheie date: {data_key}): {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Eroare la încărcarea datei pentru {var_key} (cheie date: {data_key}): {e}", file=sys.stderr)

    # Nu mai este necesar update_scrollregion explicit pentru CTkScrollableFrame


# --- MODIFICARE SEMNĂTURĂ ---
def get_data(app_instance, tab_frame=None, victim_frames_list=None):
    """
    Colectează datele de la toate victimele adăugate (Versiune CTk).

    Args:
        app_instance (AppWindow): Instanța principală a aplicației.
        tab_frame (ctk.CTkFrame, optional): Containerul tab-ului (nu mai e necesar direct).
        victim_frames_list (list, optional): Lista cadrelor (nu mai e necesară direct).

    Returns:
        dict: Dicționar cu datele colectate.
    """
    all_victim_data = {}
    # Determinăm numărul de victime din numărul de cadre stocate în app_instance
    num_victims = len(app_instance.victim_frames)
    data_vars = app_instance.data_vars

    print(f"Colectare date CTk pentru {num_victims} victime...")

    for i in range(1, num_victims + 1):
        for key_template in DATA_KEYS_PER_VICTIM:
            base_key = key_template
            original_key = f"{base_key}{i}"
            var_key = f"{VAR_PREFIX}{i}_{base_key}"

            print(f"  Procesare Victimă {i}, Cheie Var: '{var_key}'")

            if var_key in data_vars:
                try:
                    # Citim direct din variabilele Tkinter (IntVar/StringVar)
                    # Presupunem că widget-urile CTk sunt legate corect la ele
                    # sau că funcțiile helper _update_var_from_text funcționează pt CTkTextbox
                    all_victim_data[original_key] = data_vars[var_key].get()
                except Exception as e:
                    print(f"EROARE la citirea variabilei '{var_key}': {e}", file=sys.stderr)
                    all_victim_data[original_key] = f"EROARE_CITIRE_{var_key}"
            else:
                print(f"AVERTISMENT: Cheia variabilă '{var_key}' nu a fost găsită!", file=sys.stderr)
                all_victim_data[original_key] = f"CHEIE_LIPSĂ_{var_key}"

    return all_victim_data

# --- MODIFICARE SEMNĂTURĂ ---
def clear_dynamic_frames(tab_container, app_instance):
    """
    Șterge toate cadrele de victime din CTkScrollableFrame
    și resetează starea asociată (Versiune CTk).

    Args:
        tab_container (ctk.CTkFrame): Containerul tab-ului ('Victime').
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    print("Curățare cadre dinamice victime (CTk)...")
    # Distruge widget-urile victimelor (care sunt copii ai scrollable_area)
    if hasattr(tab_container, 'victims_scrollable_area'):
        for victim_widget in list(tab_container.victims_scrollable_area.winfo_children()):
            # Verificăm dacă este un cadru adăugat de noi (ar trebui să fie CTkFrame)
            if isinstance(victim_widget, ctk.CTkFrame): # Sau tipul returnat de create_victim_ui_ctk
                try:
                    victim_widget.destroy()
                except tk.TclError as e:
                    print(f"Eroare la distrugerea widget-ului victimă: {e}")
    else:
         print("Avertisment: 'victims_scrollable_area' nu a fost găsit în containerul tab-ului.")


    app_instance.victim_frames.clear()

    keys_to_delete = [key for key in app_instance.data_vars if key.startswith(VAR_PREFIX)]
    print(f"  Se vor șterge {len(keys_to_delete)} variabile din data_vars...")
    for key in keys_to_delete:
        if key in app_instance.data_vars:
             del app_instance.data_vars[key]

    print("Cadrele dinamice victime au fost curățate (CTk).")

# --- MODIFICARE SEMNĂTURĂ ---
def load_data(app_instance, data_to_load):
    """
    Logica de încărcare este gestionată în AppWindow.load_data_into_ui
    prin apeluri repetate la add_new_victim_frame.
    """
    pass

