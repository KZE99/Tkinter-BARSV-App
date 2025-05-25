# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'EAC' (Variante EAC)
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
# Nu este nevoie de messagebox sau utils aici, deoarece _add_check vine din documents_tab

def create_eac_variante_content(parent_container, app_instance, add_check_func, checkbox_texts_dict):
    """
    Populează containerul sub-tab-ului 'EAC' cu frame-ul
    pentru Variante EAC.

    Args:
        parent_container (ctk.CTkFrame): Containerul sub-tab-ului.
        app_instance (AppWindow): Instanța principală a aplicației.
        add_check_func (function): Funcția helper din documents_tab.py pentru
                                   a adăuga checkbox-uri.
        checkbox_texts_dict (dict): Dicționarul cu textele pentru checkbox-uri.
    """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(0, weight=0) # Frame-ul nu trebuie să se extindă vertical excesiv

    # Frame Variante EAC
    frame_eac = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_eac.grid(row=0, column=0, padx=10, pady=10, sticky="ew") # Folosim grid aici pentru consistență
    
    ctk.CTkLabel(frame_eac, text="Variante EAC", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 5), padx=10, sticky="w")
    ctk.CTkLabel(frame_eac, text="**În fișele EAC se precompletează doar datele auto, datele persoanelor implicate, valori etilo, diagnostice...\nCelelalte date (bifele) se completează cu pixul.",
                 wraplength=600, justify=tk.LEFT).grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="w")
    
    eac_keys = [
        'eac_primele2pagini', 'eac_auto1_2victime', 'eac_victime_1si2',
        'eac_victime_3si4', 'eac_auto1si2', 'eac_auto3si4', 'eac_auto5si6'
    ]
    
    for i, key in enumerate(eac_keys):
        is_default = 0
        if key in ['eac_primele2pagini', 'eac_auto1_2victime']: # Setează default conform vechiului cod
            is_default = 1
        add_check_func(frame_eac, key, i + 2, 0, app_instance, colspan=2, default=is_default, checkbox_texts_dict=checkbox_texts_dict)

