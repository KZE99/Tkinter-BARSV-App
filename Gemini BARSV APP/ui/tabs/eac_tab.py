# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului principal 'EAC'.
(Versiune adaptată pentru CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

# Importă modulele pentru sub-tab-uri
try:
    # Import relativ din subdirectorul eac_subtabs
    from .eac_subtabs import primele_pagini
    # TODO: Importă și celelalte sub-tab-uri când sunt create
    # from .eac_subtabs import pagina_auto
    # from .eac_subtabs import pagina_victima
except ImportError as e:
    messagebox.showerror("Eroare Import Sub-Tab EAC", f"Nu s-au putut importa modulele sub-tab-urilor EAC (ex: primele_pagini): {e}\nVerifică structura directorului 'ui/tabs/eac_subtabs' și fișierul __init__.py.")
    # Ieșim sau continuăm cu tab-ul gol? Decidem să continuăm cu un mesaj.
    # sys.exit(1)
    primele_pagini = None # Setează la None pentru a evita erori ulterioare
    # pagina_auto = None
    # pagina_victima = None

# Prefix pentru variabilele acestui tab (dacă ar avea propriile date globale)
# VAR_PREFIX = "eac_"
# DATA_KEYS = []

def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul principal 'EAC'.

    Args:
        parent_container (ctk.CTkFrame): Containerul oferit de CTkTabview principal.
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    # Configurăm grid-ul containerului principal al tab-ului EAC
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_columnconfigure(0, weight=1)

    # --- Creează CTkTabview interior pentru sub-tab-urile EAC ---
    inner_tabview = ctk.CTkTabview(parent_container, border_width=1)
    inner_tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Stocăm referința la inner_tabview în containerul părinte pentru acces ușor
    # (util pentru funcțiile get/load data dacă e nevoie)
    parent_container.inner_tabview = inner_tabview

    # Adaugă sub-tab-urile
    tab1_name = " Primele 2 Pagini "
    tab2_name = " Pagina Auto "
    tab3_name = " Pagina Victima "
    inner_tabview.add(tab1_name)
    inner_tabview.add(tab2_name)
    inner_tabview.add(tab3_name)
    inner_tabview.set(tab1_name) # Setează tab-ul activ inițial

    # Obține containerele sub-tab-urilor
    sub_tab1_container = inner_tabview.tab(tab1_name)
    sub_tab2_container = inner_tabview.tab(tab2_name)
    sub_tab3_container = inner_tabview.tab(tab3_name)

    # --- Populează Sub-Tab 1 (Primele 2 Pagini) ---
    if primele_pagini: # Verifică dacă importul a reușit
        try:
            primele_pagini.create_sub_tab_content(sub_tab1_container, app_instance)
        except Exception as e:
            messagebox.showerror("Eroare Populare Sub-Tab", f"Eroare la crearea conținutului pentru '{tab1_name}':\n{e}")
            print(f"Eroare detaliată la populare '{tab1_name}':", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            # Adaugă un label de eroare în tab
            ctk.CTkLabel(sub_tab1_container, text=f"Eroare la încărcarea tab-ului:\n{e}", text_color="red").pack(padx=20, pady=20)
    else:
        ctk.CTkLabel(sub_tab1_container, text="Eroare la importul modulului 'primele_pagini.py'").pack(padx=20, pady=20)


    # --- Populează Sub-Tab 2 (Pagina Auto - Placeholder) ---
    # TODO: Înlocuiește cu apelul real când `pagina_auto.py` este creat
    # if pagina_auto:
    #    pagina_auto.create_sub_tab_content(sub_tab2_container, app_instance)
    # else:
    ctk.CTkLabel(sub_tab2_container, text="Conținut Pagina Auto (în construcție)").pack(padx=20, pady=20)


    # --- Populează Sub-Tab 3 (Pagina Victima - Placeholder) ---
    # TODO: Înlocuiește cu apelul real când `pagina_victima.py` este creat
    # if pagina_victima:
    #    pagina_victima.create_sub_tab_content(sub_tab3_container, app_instance)
    # else:
    ctk.CTkLabel(sub_tab3_container, text="Conținut Pagina Victima (în construcție)").pack(padx=20, pady=20)


def get_data(app_instance):
    """
    Colectează datele din toate sub-tab-urile EAC.
    Deleagă colectarea către funcțiile get_data ale sub-tab-urilor.
    """
    data = {}
    print("Colectare date din tab EAC (CTk)...")
    try:
        if primele_pagini: # Verifică dacă modulul a fost importat corect
            data.update(primele_pagini.get_data(app_instance))
        # TODO: Adaugă colectarea din celelalte sub-tab-uri când sunt gata
        # if pagina_auto:
        #     data.update(pagina_auto.get_data(app_instance))
        # if pagina_victima:
        #     data.update(pagina_victima.get_data(app_instance))
    except Exception as e:
        print(f"Eroare la colectarea datelor din sub-tab-urile EAC: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        # Returnează datele parțiale sau un dicționar gol/None?
        # Alegem să returnăm ce s-a colectat până la eroare.
    return data

def load_data(app_instance, data_to_load):
    """
    Încarcă datele în toate sub-tab-urile EAC.
    Deleagă încărcarea către funcțiile load_data ale sub-tab-urilor.
    """
    print("Încărcare date în tab EAC (CTk)...")
    try:
        if primele_pagini: # Verifică dacă modulul a fost importat corect
            primele_pagini.load_data(app_instance, data_to_load)
        # TODO: Adaugă încărcarea în celelalte sub-tab-uri când sunt gata
        # if pagina_auto:
        #     pagina_auto.load_data(app_instance, data_to_load)
        # if pagina_victima:
        #     pagina_victima.load_data(app_instance, data_to_load)
    except Exception as e:
        print(f"Eroare la încărcarea datelor în sub-tab-urile EAC: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

