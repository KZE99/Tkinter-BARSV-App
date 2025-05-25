# -*- coding: utf-8 -*-
"""
Modul pentru widget-ul reutilizabil care afișează și permite
editarea detaliilor unei singure victime (Versiune CustomTkinter - Declarație Colapsabilă).
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

# Asigură-te că utils.py există și funcționează
try:
    from core import utils
except ImportError:
    print("AVERTISMENT: Nu s-a putut importa core.utils în victim_frame (CTk). Handler-ul RO nu va funcționa.")
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()


# --- Funcții Helper Text <-> StringVar (Pot necesita ajustări pt CTkTextbox) ---
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


def create_victim_ui_ctk(parent, victim_number, victim_vars):
    """
    Creează și returnează un CTkFrame cu widget-urile CTk pentru o victimă.

    Args:
        parent (ctk.CTkFrame): Widget-ul părinte (CTkScrollableFrame).
        victim_number (int): Numărul victimei.
        victim_vars (dict): Dicționarul cu variabilele Tkinter.

    Returns:
        ctk.CTkFrame: Cadrul creat conținând UI-ul pentru victimă.
    """
    victim_frame = ctk.CTkFrame(parent, border_width=1, corner_radius=10)
    victim_frame.columnconfigure(1, weight=1)
    victim_frame.columnconfigure(3, weight=1)
    victim_frame.columnconfigure(5, weight=1)

    title_label = ctk.CTkLabel(victim_frame, text=f" VICTIMA NR. {victim_number} ", font=ctk.CTkFont(weight="bold"))
    title_label.grid(row=0, column=0, columnspan=6, pady=(5, 10), padx=10, sticky="ew")

    # --- Rând 1: Nume, CNP, Domiciliu Label ---
    ctk.CTkLabel(victim_frame, text="Nume, prenume:").grid(row=1, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nume = ctk.CTkEntry(victim_frame, width=230,
                              textvariable=victim_vars.get(f'nume_victimax{victim_number}'))
    entry_nume.grid(row=1, column=1, padx=2, pady=2, sticky="ew")
    entry_nume.bind("<KeyPress>", utils.handle_romanian_characters_keypress)

    ctk.CTkLabel(victim_frame, text="CNP:").grid(row=1, column=2, padx=(10,2), pady=2, sticky="w")
    entry_cnp = ctk.CTkEntry(victim_frame, width=140,
                             textvariable=victim_vars.get(f'cnp_victimax{victim_number}'))
    entry_cnp.grid(row=1, column=3, padx=2, pady=2, sticky="ew")

    ctk.CTkLabel(victim_frame, text="cu domiciliul/ sediul în:").grid(row=1, column=4, padx=(10,0), pady=2, sticky="w")

    # --- Rând 2: Adresa, Cetățenie ---
    entry_adresa = ctk.CTkEntry(victim_frame, placeholder_text="Adresa...",
                                textvariable=victim_vars.get(f'adresa_victimax{victim_number}'))
    entry_adresa.grid(row=2, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
    entry_adresa.bind("<KeyPress>", utils.handle_romanian_characters_keypress)

    ctk.CTkLabel(victim_frame, text="Cetățenie:").grid(row=2, column=4, padx=(10,2), pady=2, sticky="w")
    entry_cetatenie = ctk.CTkEntry(victim_frame, width=140,
                                   textvariable=victim_vars.get(f'cetatenie_victimax{victim_number}'))
    entry_cetatenie.grid(row=2, column=5, padx=(0,10), pady=2, sticky="ew")
    entry_cetatenie.bind("<KeyPress>", utils.handle_romanian_characters_keypress)

    # --- Rând 3: Telefon, Calitate ---
    ctk.CTkLabel(victim_frame, text="Telefon:").grid(row=3, column=0, padx=(10,2), pady=2, sticky="w")
    entry_tel = ctk.CTkEntry(victim_frame, width=150,
                             textvariable=victim_vars.get(f'tel_victimax{victim_number}'))
    entry_tel.grid(row=3, column=1, padx=2, pady=2, sticky="w")

    ctk.CTkLabel(victim_frame, text="în calitate de:").grid(row=3, column=2, padx=(10,2), pady=2, sticky="w")
    combo_calitate = ctk.CTkComboBox(victim_frame, width=200, state="readonly",
                                     variable=victim_vars.get(f'calitate_victimax{victim_number}'),
                                     values=['Pasager auto', 'Pieton', 'Conducător auto',
                                             'Conducător bicicletă', 'Conducător trotinetă electrică'],
                                     button_color=None)
    combo_calitate.grid(row=3, column=3, padx=2, pady=2, sticky="w")
    combo_calitate.set('Pasager auto')

    # --- Rând 4: Diagnostic și Prezent CFL ---
    ctk.CTkLabel(victim_frame, text="Diagnostic:").grid(row=4, column=0, padx=(10,2), pady=2, sticky="nw")
    textbox_diagnostic = ctk.CTkTextbox(victim_frame, height=100, width=300, wrap=tk.WORD)
    textbox_diagnostic.grid(row=4, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")
    textbox_diagnostic.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    diag_var = victim_vars.get(f'diagnostic_victimax{victim_number}')
    if diag_var:
        initial_diag_text = diag_var.get()
        if initial_diag_text:
            textbox_diagnostic.insert("1.0", initial_diag_text)
        textbox_diagnostic.bind("<FocusOut>", lambda event, w=textbox_diagnostic, v=diag_var: _update_var_from_text(w, v))

    frame_prezent = ctk.CTkFrame(victim_frame, fg_color="transparent")
    frame_prezent.grid(row=4, column=4, columnspan=2, padx=10, pady=2, sticky="nw")
    ctk.CTkLabel(frame_prezent, text="PREZENT LA FAȚA LOCULUI:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
    radio_var_prezent_cfl = victim_vars.get(f'radio_prezent_cfl_group{victim_number}') # Variabila de stare
    radio_da = ctk.CTkRadioButton(frame_prezent, text="DA", value="DA", variable=radio_var_prezent_cfl)
    radio_da.pack(side=tk.LEFT, anchor="w", padx=(0, 10), pady=5)
    radio_nu = ctk.CTkRadioButton(frame_prezent, text="NU", value="NU", variable=radio_var_prezent_cfl)
    radio_nu.pack(side=tk.LEFT, anchor="w", pady=5)
    if not radio_var_prezent_cfl.get(): # Setează default dacă e goală
        radio_var_prezent_cfl.set("NU")

    # --- Rând 5: Notă Vinovăție ---
    chk_nota = ctk.CTkCheckBox(victim_frame, text="Notă vinovăție",
                               variable=victim_vars.get(f'nota_vinovatie_victimax{victim_number}'),
                               onvalue=1, offvalue=0)
    chk_nota.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    ctk.CTkLabel(victim_frame, text="Articol:").grid(row=5, column=2, padx=(10,2), pady=10, sticky="w")
    entry_articol = ctk.CTkEntry(victim_frame, width=150,
                                 textvariable=victim_vars.get(f'articol_victimax{victim_number}'))
    entry_articol.grid(row=5, column=3, padx=2, pady=10, sticky="w")

    # --- Rând 6: Label Declarație (va fi gestionat de funcția de toggle) ---
    label_declaratie_titlu = ctk.CTkLabel(victim_frame, text="Declaratie victimă - dacă este prezent la CFL:", font=ctk.CTkFont(weight="bold"))
    # Nu facem .grid() aici inițial

    # --- Rând 7: Text Declarație (va fi gestionat de funcția de toggle) ---
    textbox_declaratie = ctk.CTkTextbox(victim_frame, height=80, wrap=tk.WORD)
    textbox_declaratie.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    decl_var = victim_vars.get(f'declaratie_victimax{victim_number}')
    if decl_var:
        initial_decl_text = decl_var.get()
        if initial_decl_text:
            textbox_declaratie.insert("1.0", initial_decl_text)
        textbox_declaratie.bind("<FocusOut>", lambda event, w=textbox_declaratie, v=decl_var: _update_var_from_text(w, v))
    # Nu facem .grid() aici inițial

    # --- Funcție și Tracing pentru vizibilitatea declarației ---
    def _toggle_declaratie_visibility(*args):
        if radio_var_prezent_cfl.get() == "DA":
            label_declaratie_titlu.grid(row=6, column=0, columnspan=6, padx=10, pady=(10, 2), sticky="w")
            textbox_declaratie.grid(row=7, column=0, columnspan=6, padx=10, pady=(0,10), sticky="ew")
            victim_frame.rowconfigure(7, weight=1) # Permite extinderea textbox-ului
        else:
            label_declaratie_titlu.grid_remove()
            textbox_declaratie.grid_remove()
            victim_frame.rowconfigure(7, weight=0) # Resetează weight-ul

    if radio_var_prezent_cfl: # Adaugă trace doar dacă variabila există
        radio_var_prezent_cfl.trace_add("write", _toggle_declaratie_visibility)
        _toggle_declaratie_visibility() # Setează starea inițială

    return victim_frame


# --- Cod de Test (adaptat pentru CTk) ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Test VictimFrame (CTk) - Declarație Colapsabilă")
    root.geometry("850x550") # Mărit puțin pentru a vedea mai bine

    try:
        victim_keys = [
            "nume_victimax", "cnp_victimax", "adresa_victimax", "cetatenie_victimax",
            "tel_victimax", "calitate_victimax", "diagnostic_victimax",
            "radio_prezent_cfl_group",
            "nota_vinovatie_victimax", "articol_victimax",
            "declaratie_victimax"
        ]
        test_vars_victim1 = {}
        for key_template in victim_keys:
            data_key = f"{key_template}1"
            if key_template == "nota_vinovatie_victimax":
                test_vars_victim1[data_key] = tk.IntVar(value=0)
            elif key_template == "radio_prezent_cfl_group":
                test_vars_victim1[data_key] = tk.StringVar(value="NU") # Default NU
            else:
                test_vars_victim1[data_key] = tk.StringVar()

        test_vars_victim1['nume_victimax1'].set("Popescu Ion (CTk)")
        test_vars_victim1['declaratie_victimax1'].set("Aceasta este o declarație de test.")

        scroll = ctk.CTkScrollableFrame(root)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        victim_widget = create_victim_ui_ctk(scroll, 1, test_vars_victim1)
        victim_widget.pack(padx=10, pady=10, fill="x")

        def show_values():
            vals = {key: var.get() for key, var in test_vars_victim1.items()}
            print(vals)
            messagebox.showinfo("Valori Variabile", str(vals))

        btn_show = ctk.CTkButton(root, text="Afișează Valori", command=show_values)
        btn_show.pack(pady=10)

    except Exception as e:
         ctk.CTkLabel(root, text=f"Eroare la creare test UI:\n{e}").pack(padx=20, pady=20)
         traceback.print_exc(file=sys.stderr)

    root.mainloop()
