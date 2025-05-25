# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Documente extra'
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
# Nu este nevoie de messagebox sau utils aici, deoarece _add_check vine din documents_tab

def create_doc_extra_content(parent_container, app_instance, add_check_func, checkbox_texts_dict):
    """
    Populează containerul sub-tab-ului 'Documente extra' cu frame-ul
    pentru opțiunile de documente suplimentare.

    Args:
        parent_container (ctk.CTkFrame): Containerul sub-tab-ului.
        app_instance (AppWindow): Instanța principală a aplicației.
        add_check_func (function): Funcția helper din documents_tab.py pentru
                                   a adăuga checkbox-uri.
        checkbox_texts_dict (dict): Dicționarul cu textele pentru checkbox-uri.
    """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(0, weight=0) # Frame-ul nu trebuie să se extindă vertical excesiv

    # Frame Documente Extra
    frame_extra = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_extra.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    ctk.CTkLabel(frame_extra, text="Documente Extra", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 10), padx=10, sticky="w")
    
    doc_extra_keys = [
        'doc_extra1', 
        'doc_extra3'
        # Adaugă 'doc_extra2', 'doc_extra4' aici dacă le definești în DATA_KEYS și CHECKBOX_TEXTS
    ]
    
    for i, key in enumerate(doc_extra_keys):
        is_default = 0
        if key == 'doc_extra1': # Setează default conform vechiului cod
            is_default = 1
        add_check_func(frame_extra, key, i + 1, 0, app_instance, default=is_default, checkbox_texts_dict=checkbox_texts_dict)

