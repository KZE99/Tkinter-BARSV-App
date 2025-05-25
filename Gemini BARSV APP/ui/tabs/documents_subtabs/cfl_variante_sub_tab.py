# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'CFL' (Variante CFL)
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
# Nu este nevoie de messagebox sau utils aici, deoarece _add_check vine din documents_tab

def create_cfl_variante_content(parent_container, app_instance, add_check_func, checkbox_texts_dict):
    """
    Populează containerul sub-tab-ului 'CFL' cu frame-ul
    pentru Variante CFL.

    Args:
        parent_container (ctk.CTkFrame): Containerul sub-tab-ului.
        app_instance (AppWindow): Instanța principală a aplicației.
        add_check_func (function): Funcția helper din documents_tab.py pentru
                                   a adăuga checkbox-uri.
        checkbox_texts_dict (dict): Dicționarul cu textele pentru checkbox-uri.
    """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(0, weight=0) # Frame-ul nu trebuie să se extindă vertical excesiv

    # Frame Variante CFL
    frame_cfl_var = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_cfl_var.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    ctk.CTkLabel(frame_cfl_var, text="Variante CFL", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 10), padx=10, sticky="w")
    
    cfl_var_keys = [
        'CFL_1auto_Basic', 'CFL_2auto_Basic', 'CFL_3auto_Basic', 
        'CFL_4auto_Basic', 'CFL_5auto_Basic', 'CFL_6auto_Basic', 
        'PV_fara_CFL1'
    ]
    for i, key in enumerate(cfl_var_keys):
        is_default = 1 if key == 'CFL_2auto_Basic' else 0 # Setează default conform vechiului cod
        add_check_func(frame_cfl_var, key, i + 1, 0, app_instance, default=is_default, checkbox_texts_dict=checkbox_texts_dict)

