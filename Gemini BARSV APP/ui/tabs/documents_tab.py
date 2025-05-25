# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului '## Documente ##'.
(Versiune refactorizată cu sub-tab-uri CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

try:
    from core import doc_generator
    # Importăm modulele pentru TOATE sub-tab-urile
    from .documents_subtabs import ordonante_sub_tab
    from .documents_subtabs import cfl_variante_sub_tab
    from .documents_subtabs import eac_variante_sub_tab
    from .documents_subtabs import trimiteri_parchet_sub_tab
    from .documents_subtabs import anexa2_sub_tab
    from .documents_subtabs import nota_telex_sub_tab
    from .documents_subtabs import doc_extra_sub_tab
except ImportError as e:
    messagebox.showerror("Eroare Import Documents Tab (CTk)", f"Nu s-au putut importa modulele de sub-tab necesare: {e}\nVerifică directorul 'ui/tabs/documents_subtabs/' și fișierele __init__.py.")
    ordonante_sub_tab = cfl_variante_sub_tab = eac_variante_sub_tab = None
    trimiteri_parchet_sub_tab = anexa2_sub_tab = nota_telex_sub_tab = doc_extra_sub_tab = None

VAR_PREFIX = "docs_"

DATA_KEYS = [
    'raport_retinere_sofer_autox1', 'raport_retinere_sofer_autox2',
    'raport_retinere_sofer_autox3', 'raport_retinere_sofer_autox4',
    'raport_retinere_sofer_autox5', 'raport_retinere_sofer_autox6',
    'trimitere_parchet_sofer1', 'trimitere_parchet_auto2victime',
    'trimitere_parchet_auto3victime', 'trimitere_parchet2auto_victima_sofer2',
    'trimitere_parchet_auto1victima',
    'nota_vinovatie_victimax1', 'nota_vinovatie_victimax2',
    'nota_vinovatie_victimax3', 'nota_vinovatie_victimax4',
    'nota_vinovatie_sofer_autox1', 'nota_vinovatie_sofer_autox2',
    'nota_vinovatie_sofer_autox3', 'nota_vinovatie_sofer_autox4',
    'nota_vinovatie_sofer_autox5', 'nota_vinovatie_sofer_autox6',
    'Ordonanta_IUP_Basic', 'Ordonanta_IUP_Alcool', 'Ordonanta_IUP_Droguri',
    'Ordonanta_IUP_fara_pc', 'Ordonanta_IUP_mort', 'Ordonanta_IUP_mutare_masina',
    'Ordonanta_IUP_parasire', 'Ordonanta_IUP_pc_suspendat',
    'Anexa2_auto_bicicleta', 'Anexa2_auto_trotineta', 'Anexa 2 - 2 auto',
    'Anexa 2 - 3 auto', 'Anexa 2 - 4 auto', 'Anexa 2 - 5 auto', 'Anexa 2 - 6 auto',
    'Ordonanta_CFL_Basic', 'Ordonanta_CFL_Alcool', 'Ordonanta_CFL_mutare_masina',
    'Ordonanta_CFL_parasire', 'Ordonanta_CFL_droguri', 'Ordonanta_CFL_fara_pc',
    'Ordonanta_CFL_mort', 'Ordonanta_CFL_pc_suspendat',
    'CFL_1auto_Basic', 'CFL_2auto_Basic', 'CFL_3auto_Basic', 'CFL_4auto_Basic',
    'CFL_5auto_Basic', 'CFL_6auto_Basic', 'PV_fara_CFL1',
    'eac_primele2pagini', 'eac_auto1_2victime', 'eac_victime_1si2',
    'eac_victime_3si4', 'eac_auto1si2', 'eac_auto3si4', 'eac_auto5si6',
    'doc_extra1', 'doc_extra3',
    'key_Nota Telex -  (1) - Art. 54_1', 'key_Nota Telex -  (1) - Art. 54_1 + date auto',
    'key_Nota Telex -  (2) - Art. 51', 'key_Nota Telex -  (2) - Art. 51 + date auto',
    'key_Nota Telex -  (7) - Art. 57_2', 'key_Nota Telex -  (7) - Art. 57_2 + date auto',
    'key_Nota Telex -  (8) - Art. 59_2', 'key_Nota Telex -  (8) - Art. 59_2 + date auto',
    'key_Nota Telex -  (6) - Art. 60', 'key_Nota Telex -  (3) - Art. 54_1 cu pieton',
    'key_Nota Telex -  (5) - Art. 167_1_D', 'key_Nota Telex -  (4) - Art. 135_H',
    'art_334_1_capac', 'art_336_1_capac', 'art_334_2_capac', 'art_336_1ind1_capac',
    'art_334_3_capac', 'art_336_2_capac', 'art_334_4_capac', 'art_337_capac',
    'art_335_1_capac', 'art_338_1_capac', 'art_335_2_capac', 'art_338_2_capac'
]

CHECKBOX_TEXTS = {
    'Ordonanta_IUP_Basic': 'Ordonanță IUP',
    'Ordonanta_IUP_parasire': 'Ordonanță IUP Părăsire - 338/1',
    'Ordonanta_IUP_mutare_masina': 'Ordonanță IUP Mutare mașină - 338/2',
    'Ordonanta_IUP_Alcool': 'Ordonanță IUP Alcool',
    'Ordonanta_IUP_Droguri': 'Ordonanță IUP Droguri',
    'Ordonanta_IUP_fara_pc': 'Ordonanță IUP Fara PC - 335/1',
    'Ordonanta_IUP_pc_suspendat': 'Ordonanță IUP PC suspendat - 335/2',
    'Ordonanta_IUP_mort': 'Ordonanță IUP Mortal',
    'Ordonanta_CFL_Basic': 'Ordonanță CFL',
    'Ordonanta_CFL_parasire': 'Ordonanță CFL Părăsire - 338/1',
    'Ordonanta_CFL_mutare_masina': 'Ordonanță CFL Mutare mașină - 338/2',
    'Ordonanta_CFL_Alcool': 'Ordonanță CFL Alcool',
    'Ordonanta_CFL_droguri': 'Ordonanță CFL Droguri',
    'Ordonanta_CFL_fara_pc': 'Ordonanță CFL Fără PC - 335/1',
    'Ordonanta_CFL_pc_suspendat': 'Ordonanță CFL PC suspendat - 335/2',
    'Ordonanta_CFL_mort': 'Ordonanță CFL Mortal',
    'CFL_1auto_Basic': 'CFL 1 Auto',
    'CFL_2auto_Basic': 'CFL 2 Auto',
    'CFL_3auto_Basic': 'CFL 3 Auto',
    'CFL_4auto_Basic': 'CFL 4 Auto',
    'CFL_5auto_Basic': 'CFL 5 Auto',
    'CFL_6auto_Basic': 'CFL 6 Auto',
    'PV_fara_CFL1': 'PV Fără CFL - Șofer 1/ Victimă 1',
    'eac_primele2pagini': 'Pagină EAC Primele 2 pagini',
    'eac_auto1_2victime': 'Pagină EAC - Vehicul nr. 1 (față) ; Victime pasager/pieton 1 și 2 (verso)',
    'eac_victime_1si2': 'Pagină EAC doar cu Victime pasager/pieton 1 și 2',
    'eac_victime_3si4': 'Pagină EAC doar cu Victime pasager/pieton 3 și 4',
    'eac_auto1si2': 'Pagină EAC - Vehicul nr. 1 (față) ; Vehicul nr. 2 (verso)',
    'eac_auto3si4': 'Pagină EAC - Vehicul nr. 3 (față) ; Vehicul nr. 4 (verso)',
    'eac_auto5si6': 'Pagină EAC - Vehicul nr. 5 (față) ; Vehicul nr. 6 (verso)',
    'trimitere_parchet_sofer1': 'Trimitere Parchet - Autovătămare Șofer 1',
    'trimitere_parchet_auto1victima': 'Trimitere Parchet - Auto - cu victima pasager/pieton',
    'trimitere_parchet2auto_victima_sofer2': 'Trimitere Parchet - 2 Auto - Victima Șofer 2',
    'trimitere_parchet_auto2victime': 'Trimitere Parchet - Auto - cu 2 Victime (pasageri/pietoni)',
    'trimitere_parchet_auto3victime': 'Trimitere Parchet - Auto - cu 3 Victime (pasageri/pietoni)',
    'Anexa2_auto_bicicleta': 'Anexa 2 - Bicicleta - 1 Auto ## Biciclist vinovat',
    'Anexa2_auto_trotineta': 'Anexa 2 - Trotineta - 1 Auto ## Trotinetist vinovat',
    'Anexa 2 - 2 auto': 'Anexa 2 - 2 auto - Auto1 vinovat',
    'Anexa 2 - 3 auto': 'Anexa 2 - 3 auto - Auto1 vinovat',
    'Anexa 2 - 4 auto': 'Anexa 2 - 4 auto - Auto1 vinovat',
    'Anexa 2 - 5 auto': 'Anexa 2 - 5 auto - Auto1 vinovat',
    'Anexa 2 - 6 auto': 'Anexa 2 - 6 auto - Auto1 vinovat',
    'key_Nota Telex -  (1) - Art. 54_1': 'Nota Telex - Art. 54/1',
    'key_Nota Telex -  (1) - Art. 54_1 + date auto': 'Nota Telex - Art. 54/1 + date extra',
    'key_Nota Telex -  (2) - Art. 51': 'Nota Telex - Art. 51',
    'key_Nota Telex -  (2) - Art. 51 + date auto': 'Nota Telex - Art. 51 + date extra',
    'key_Nota Telex -  (7) - Art. 57_2': 'Nota Telex - Art. 57/2',
    'key_Nota Telex -  (7) - Art. 57_2 + date auto': 'Nota Telex - Art. 57/2 + date extra',
    'key_Nota Telex -  (8) - Art. 59_2': 'Nota Telex - Art. 59/2',
    'key_Nota Telex -  (8) - Art. 59_2 + date auto': 'Nota Telex - Art. 59/2 + date extra',
    'key_Nota Telex -  (6) - Art. 60': 'Nota Telex - Art. 60',
    'key_Nota Telex -  (3) - Art. 54_1 cu pieton': 'Nota Telex - Art. 54/1 cu pieton',
    'key_Nota Telex -  (5) - Art. 167_1_D': 'Nota Telex - Art. 167/1/D',
    'key_Nota Telex -  (4) - Art. 135_H': 'Nota Telex - Art. 135/H',
    'doc_extra1': 'Pagina Caiet Accidente 1',
    'doc_extra3': 'Autorizatii de Reparatii',
    'art_334_1_capac': 'Art. 334/1', 'art_336_1_capac': 'Art. 336/1',
    'art_334_2_capac': 'Art. 334/2', 'art_336_1ind1_capac': 'Art. 336/1^1',
    'art_334_3_capac': 'Art. 334/3', 'art_336_2_capac': 'Art. 336/2',
    'art_334_4_capac': 'Art. 334/4', 'art_337_capac': 'Art. 337',
    'art_335_1_capac': 'Art. 335/1', 'art_338_1_capac': 'Art. 338/1',
    'art_335_2_capac': 'Art. 335/2', 'art_338_2_capac': 'Art. 338/2'
}

def _add_check(parent, key, row, col, app_instance, colspan=1, default=0, checkbox_texts_dict=None):
    """Funcție helper pentru a crea un CTkCheckBox."""
    full_key = f"{VAR_PREFIX}{key}"
    var = app_instance.data_vars.get(full_key)

    if var is None:
        var = tk.IntVar(value=default)
        app_instance.data_vars[full_key] = var
    elif not isinstance(var, tk.IntVar):
        var = tk.IntVar(value=default)
        app_instance.data_vars[full_key] = var
    else:
        current_value = var.get()
        if default != 0 and current_value == 0 and key not in getattr(app_instance, 'loaded_checkbox_keys', set()):
            var.set(default)
        elif default == 0 and current_value != 0 and key not in getattr(app_instance, 'loaded_checkbox_keys', set()):
            var.set(default)

    text_map = checkbox_texts_dict if checkbox_texts_dict else CHECKBOX_TEXTS
    text = text_map.get(key, key)

    chk = ctk.CTkCheckBox(parent, text=text, variable=var, onvalue=1, offvalue=0)
    chk.grid(row=row, column=col, columnspan=colspan, padx=5, pady=2, sticky="w")
    return chk


def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul '## Documente ##'.
    """
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_rowconfigure(1, weight=0)
    parent_container.grid_columnconfigure(0, weight=1)

    if not hasattr(app_instance, 'loaded_checkbox_keys'):
        app_instance.loaded_checkbox_keys = set()

    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if full_key not in app_instance.data_vars:
            app_instance.data_vars[full_key] = tk.IntVar(value=0)

    inner_tabview = ctk.CTkTabview(parent_container, border_width=1)
    inner_tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tab_names_ordered = [
        "Ordonanțe", "CFL", "EAC", "Trimiteri Parchet",
        "Anexa 2", "Nota Telex", "Documente extra"
    ]
    sub_tab_containers = {}

    for name in tab_names_ordered:
        inner_tabview.add(name)
        sub_tab_containers[name] = inner_tabview.tab(name)
        sub_tab_containers[name].grid_rowconfigure(0, weight=1)
        sub_tab_containers[name].grid_columnconfigure(0, weight=1)

    inner_tabview.set("Ordonanțe")

    # --- Populează Sub-Tab-urile ---
    if "Ordonanțe" in sub_tab_containers and ordonante_sub_tab:
        ordonante_sub_tab.create_ordonante_content(sub_tab_containers["Ordonanțe"], app_instance, _add_check, CHECKBOX_TEXTS)

    if "CFL" in sub_tab_containers and cfl_variante_sub_tab:
        cfl_variante_sub_tab.create_cfl_variante_content(sub_tab_containers["CFL"], app_instance, _add_check, CHECKBOX_TEXTS)
    elif "CFL" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["CFL"], text="Modulul cfl_variante_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)

    if "EAC" in sub_tab_containers and eac_variante_sub_tab:
        eac_variante_sub_tab.create_eac_variante_content(sub_tab_containers["EAC"], app_instance, _add_check, CHECKBOX_TEXTS)
    elif "EAC" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["EAC"], text="Modulul eac_variante_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)

    # --- MODIFICARE APEL: Eliminăm _add_check ---
    if "Trimiteri Parchet" in sub_tab_containers and trimiteri_parchet_sub_tab:
        trimiteri_parchet_sub_tab.create_trimiteri_parchet_content(sub_tab_containers["Trimiteri Parchet"], app_instance, CHECKBOX_TEXTS)
    elif "Trimiteri Parchet" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["Trimiteri Parchet"], text="Modulul trimiteri_parchet_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)
    # --- SFÂRȘIT MODIFICARE ---

    if "Anexa 2" in sub_tab_containers and anexa2_sub_tab:
        anexa2_sub_tab.create_anexa2_content(sub_tab_containers["Anexa 2"], app_instance, _add_check, CHECKBOX_TEXTS)
    elif "Anexa 2" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["Anexa 2"], text="Modulul anexa2_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)

    if "Nota Telex" in sub_tab_containers and nota_telex_sub_tab:
        nota_telex_sub_tab.create_nota_telex_content(sub_tab_containers["Nota Telex"], app_instance)
    elif "Nota Telex" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["Nota Telex"], text="Modulul nota_telex_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)

    if "Documente extra" in sub_tab_containers and doc_extra_sub_tab:
        doc_extra_sub_tab.create_doc_extra_content(sub_tab_containers["Documente extra"], app_instance, _add_check, CHECKBOX_TEXTS)
    elif "Documente extra" in sub_tab_containers:
        ctk.CTkLabel(sub_tab_containers["Documente extra"], text="Modulul doc_extra_sub_tab.py lipsește sau conține erori.").pack(padx=20, pady=20)


    # --- Buton Generare Documente ---
    def _generate_docs():
        print("Buton 'Generează documente' apăsat (CTk).")
        current_data = app_instance.get_all_data()
        if current_data:
            doc_generator.generate_documents(current_data)
        else:
            messagebox.showerror("Eroare Generare", "Nu s-au putut colecta datele necesare.")

    generate_button_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    generate_button_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
    generate_button_frame.columnconfigure(0, weight=1)
    generate_button = ctk.CTkButton(generate_button_frame, text="Generează documente",
                                    command=_generate_docs, width=200)
    generate_button.grid(row=0, column=0)


def get_data(app_instance):
    """Colectează starea checkbox-urilor din acest tab."""
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din tab Documente (CTk)...")
    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if full_key in data_vars:
            try:
                data[key] = data_vars[full_key].get()
            except Exception as e:
                print(f"Eroare la citirea variabilei {full_key}: {e}", file=sys.stderr)
                data[key] = 0
        else:
            # Dacă o cheie din DATA_KEYS nu are variabilă creată, o tratăm ca 0
            # (deși bucla de la începutul create_tab_content ar trebui să le creeze pe toate)
            print(f"Avertisment MAJOR: Cheia {full_key} nu a fost găsită în data_vars la colectare pentru documents_tab.", file=sys.stderr)
            data[key] = 0
    return data

def load_data(app_instance, data_to_load):
    """Setează starea checkbox-urilor pe baza datelor primite."""
    data_vars = app_instance.data_vars
    print("Încărcare date în tab Documente (CTk)...")
    if not hasattr(app_instance, 'loaded_checkbox_keys'): # Asigură existența atributului
        app_instance.loaded_checkbox_keys = set()
    else:
        app_instance.loaded_checkbox_keys.clear() # Resetează pentru fiecare încărcare

    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if key in data_to_load and full_key in data_vars:
            try:
                target_var = data_vars[full_key]
                if isinstance(target_var, tk.IntVar):
                    value = 1 if data_to_load[key] else 0
                    target_var.set(value)
                    if value == 1:
                        app_instance.loaded_checkbox_keys.add(key)
            except tk.TclError as e:
                 print(f"Avertisment: Nu s-a putut seta valoarea pentru {full_key}: {e}", file=sys.stderr)
            except Exception as e:
                 print(f"Eroare la încărcarea datei pentru {full_key}: {e}", file=sys.stderr)

