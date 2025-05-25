# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Anexa 2'
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
# Nu este nevoie de messagebox sau utils aici, deoarece _add_check vine din documents_tab

def create_anexa2_content(parent_container, app_instance, add_check_func, checkbox_texts_dict):
    """
    Populează containerul sub-tab-ului 'Anexa 2' cu frame-ul
    pentru opțiunile Anexa 2.

    Args:
        parent_container (ctk.CTkFrame): Containerul sub-tab-ului.
        app_instance (AppWindow): Instanța principală a aplicației.
        add_check_func (function): Funcția helper din documents_tab.py pentru
                                   a adăuga checkbox-uri.
        checkbox_texts_dict (dict): Dicționarul cu textele pentru checkbox-uri.
    """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(0, weight=0) # Frame-ul nu trebuie să se extindă vertical excesiv

    # Frame Anexa 2
    frame_anexa2 = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_anexa2.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    ctk.CTkLabel(frame_anexa2, text="Anexa 2", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 10), padx=10, sticky="w")
    
    anexa2_keys = [
        'Anexa2_auto_bicicleta', 'Anexa2_auto_trotineta', 'Anexa 2 - 2 auto',
        'Anexa 2 - 3 auto', 'Anexa 2 - 4 auto', 'Anexa 2 - 5 auto', 'Anexa 2 - 6 auto'
    ]
    
    for i, key in enumerate(anexa2_keys):
        is_default = 1 if key == 'Anexa 2 - 2 auto' else 0 # Setează default conform vechiului cod
        add_check_func(frame_anexa2, key, i + 1, 0, app_instance, default=is_default, checkbox_texts_dict=checkbox_texts_dict)

