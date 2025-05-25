# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Ordonanțe'
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

def create_ordonante_content(parent_container, app_instance, add_check_func, checkbox_texts_dict):
    """
    Populează containerul sub-tab-ului 'Ordonanțe' cu frame-urile
    pentru Ordonanțe IUP și Ordonanțe CFL.

    Args:
        parent_container (ctk.CTkFrame): Containerul sub-tab-ului.
        app_instance (AppWindow): Instanța principală a aplicației.
        add_check_func (function): Funcția helper din documents_tab.py pentru
                                   a adăuga checkbox-uri.
        checkbox_texts_dict (dict): Dicționarul cu textele pentru checkbox-uri.
    """
    parent_container.grid_columnconfigure(0, weight=1)

    current_row = 0

    # Frame Ordonanțe IUP
    frame_iup = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_iup.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
    ctk.CTkLabel(frame_iup, text="Ordonanțe IUP", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 10), padx=10, sticky="w")
    
    iup_keys = [
        'Ordonanta_IUP_Basic', 'Ordonanta_IUP_parasire', 'Ordonanta_IUP_mutare_masina',
        'Ordonanta_IUP_Alcool', 'Ordonanta_IUP_Droguri', 'Ordonanta_IUP_fara_pc',
        'Ordonanta_IUP_pc_suspendat', 'Ordonanta_IUP_mort'
    ]
    for i, key in enumerate(iup_keys):
        is_default = 1 if key == 'Ordonanta_IUP_Basic' else 0
        # --- APEL CORECTAT ---
        add_check_func(frame_iup, key, i + 1, 0, app_instance, default=is_default, checkbox_texts_dict=checkbox_texts_dict)
        # --- SFÂRȘIT APEL CORECTAT ---
    current_row += 1

    # Frame Ordonanțe CFL
    frame_cfl_ord = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_cfl_ord.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
    ctk.CTkLabel(frame_cfl_ord, text="Ordonanțe CFL", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 10), padx=10, sticky="w")
        
    cfl_ord_keys = [
        'Ordonanta_CFL_Basic', 'Ordonanta_CFL_parasire', 'Ordonanta_CFL_mutare_masina',
        'Ordonanta_CFL_Alcool', 'Ordonanta_CFL_droguri', 'Ordonanta_CFL_fara_pc',
        'Ordonanta_CFL_pc_suspendat', 'Ordonanta_CFL_mort'
    ]
    for i, key in enumerate(cfl_ord_keys):
        is_default = 1 if key == 'Ordonanta_CFL_Basic' else 0
        # --- APEL CORECTAT ---
        add_check_func(frame_cfl_ord, key, i + 1, 0, app_instance, default=is_default, checkbox_texts_dict=checkbox_texts_dict)
        # --- SFÂRȘIT APEL CORECTAT ---
    current_row += 1
