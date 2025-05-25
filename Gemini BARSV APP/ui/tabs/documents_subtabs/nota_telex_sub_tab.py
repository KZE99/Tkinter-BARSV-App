# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Nota Telex'
din cadrul tab-ului principal de Documente.
(Versiune CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

try:
    from core import utils
except ImportError:
    print("AVERTISMENT: Nu s-a putut importa core.utils în nota_telex_sub_tab (CTk).")
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()

# Prefix specific pentru variabilele create în acest sub-tab
SUB_VAR_PREFIX = "docs_nt_" # nt = nota telex

# Cheile pentru variabilele de *afișare* și control din acest sub-tab
# Cheia pentru ComboBox
NOTA_TELEX_TYPE_KEY = "selected_nota_telex_type"

# Cheile pentru câmpurile afișate/editate în Nota Telex (bazate pe template-ul Art. 135_H)
# Acestea vor fi legate la variabile sursă din alte tab-uri
NOTA_TELEX_DISPLAY_FIELDS = {
    "display_nt_data_acc": ["principal_ziua_acc", "principal_luna_acc", "principal_anul_acc"],
    "display_nt_ora_acc": ["principal_ora_accident"],
    "display_nt_nume_sofer1": ["auto_1_nume_sofer_auto"],
    "display_nt_cnp_sofer1": ["auto_1_cnp_sofer_auto"],
    "display_nt_adresa_sofer1": ["auto_1_adresa_sofer_auto"],
    "display_nt_nrpc_sofer1": ["auto_1_nrpc_sofer_auto"],
    "display_nt_catpc_sofer1": ["auto_1_catpc_sofer_auto"],
    "display_nt_vechime_pc1": ["auto_1_vechime_pc_sofer_auto"], # Asigură-te că cheia sursă e corectă
    "display_nt_tip_vehicul1": ["auto_1_tip_autox"],
    "display_nt_marca_auto1": ["auto_1_marca_autox"],
    "display_nt_nr_auto1": ["auto_1_nr_autox"],
    "display_nt_culoare_auto1": ["auto_1_culoare_autox"],
    "display_nt_nume_victima1": ["victime_1_nume_victimax"], # Presupunem victima 1
    "display_nt_cnp_victima1": ["victime_1_cnp_victimax"],
    "display_nt_adresa_victima1": ["victime_1_adresa_victimax"],
    "display_nt_diagnostic_victima1": ["victime_1_diagnostic_victimax"],
    "display_nt_nume_agent1": ["principal_nume_agent1"],
    "display_nt_nume_agent2": ["principal_nume_agent2"], # Dacă e relevant
    # Câmpuri editabile direct în Nota Telex UI (dacă sunt necesare)
    "nt_strada_accident": tk.StringVar, # Exemplu: strada din Nota Telex
    "nt_dinspre": tk.StringVar,
    "nt_catre": tk.StringVar,
    "nt_intersectie_imobil": tk.StringVar,
    "nt_traversare_victima_detalii": tk.StringVar, # Detalii despre traversare
    "nt_spital_victima": tk.StringVar,
    "nt_rezultat_etilotest_sofer1": ["auto_1_rezultat_etilo_auto"], # Din auto_tab
    "nt_retinut_pc_sofer1": ["auto_1_bifa_pc_sofer_auto"], # Din auto_tab (IntVar)
    "nt_caz_filmat_mediatizat": tk.StringVar, # Poate fi un ComboBox DA/NU/Poate
}

# Opțiunile pentru ComboBox-ul de Nota Telex
# Cheile trebuie să corespundă cu cele din documents_tab.DATA_KEYS și CHECKBOX_TEXTS
# Valorile sunt textele afișate în ComboBox
NOTA_TELEX_OPTIONS = {
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
}


def create_nota_telex_content(parent_container, app_instance):
    """
    Populează containerul sub-tab-ului 'Nota Telex'.
    """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(1, weight=1) # Frame-ul de conținut se va extinde

    # --- Definire Variabile Tkinter ---
    # Variabila pentru ComboBox
    selected_nota_var_key = SUB_VAR_PREFIX + NOTA_TELEX_TYPE_KEY
    if selected_nota_var_key not in app_instance.data_vars:
        app_instance.data_vars[selected_nota_var_key] = tk.StringVar(value="Selectați tipul...")
    selected_nota_var = app_instance.data_vars[selected_nota_var_key]

    # Variabile pentru câmpurile editabile din Nota Telex
    for key, var_type in NOTA_TELEX_DISPLAY_FIELDS.items():
        if isinstance(var_type, type): # Dacă e un tip (tk.StringVar)
            full_key = SUB_VAR_PREFIX + key
            if full_key not in app_instance.data_vars:
                app_instance.data_vars[full_key] = var_type()

    # --- Frame pentru ComboBox ---
    combo_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    combo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    ctk.CTkLabel(combo_frame, text="Selectați Tipul de Notă Telex:").pack(side="left", padx=(0,10))
    
    combo_nota_telex = ctk.CTkComboBox(
        combo_frame,
        width=350,
        variable=selected_nota_var,
        values=["Selectați tipul..."] + list(NOTA_TELEX_OPTIONS.values()), # Adaugă opțiunile
        state="readonly",
        button_color=None
    )
    combo_nota_telex.pack(side="left")

    # --- Frame pentru Conținutul Notei Telex (inițial ascuns sau gol) ---
    content_nota_frame = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    # Nu facem .grid() sau .pack() aici, va fi gestionat de funcția de toggle

    # --- Funcția de Toggle și Populare Conținut ---
    def _on_nota_telex_select(selected_value):
        if selected_value == "Selectați tipul...":
            content_nota_frame.grid_forget() # Ascunde frame-ul
            return

        # Găsește cheia originală pe baza valorii selectate
        selected_key = None
        for k, v in NOTA_TELEX_OPTIONS.items():
            if v == selected_value:
                selected_key = k
                break
        
        if not selected_key:
            content_nota_frame.grid_forget()
            return

        # Șterge conținutul vechi (dacă există)
        for widget in content_nota_frame.winfo_children():
            widget.destroy()
        
        # Afișează frame-ul
        content_nota_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        content_nota_frame.columnconfigure(1, weight=1) # Pentru extinderea unor entry-uri

        # --- Populează UI-ul specific pentru Nota Telex (exemplu Art. 135_H) ---
        # Această parte va trebui adaptată pentru fiecare tip de Notă Telex
        # sau să avem o funcție generică care construiește UI-ul pe baza cheilor.
        # Deocamdată, implementăm un exemplu bazat pe template-ul Art. 135_H.
        
        ctk.CTkLabel(content_nota_frame, text=f"PREVIZUALIZARE: {selected_value}", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        r = 1
        # Data și ora
        ctk.CTkLabel(content_nota_frame, text="La data de:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_data_acc")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="în jurul orelor:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_ora_acc")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1

        # Șofer 1
        ctk.CTkLabel(content_nota_frame, text="Conducător auto:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nume_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="CNP:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_cnp_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Domiciliat în:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_adresa_sofer1"), wraplength=400).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Posesor PC nr.:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nrpc_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Categoriile:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_catpc_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Cu vechime din anul:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_vechime_pc1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="A condus:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_tip_vehicul1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Marca:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_marca_auto1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Nr. înmatriculare:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nr_auto1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Culoare:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_culoare_auto1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1

        # Câmpuri editabile pentru Nota Telex
        ctk.CTkLabel(content_nota_frame, text="Pe str.:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_strada_accident")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Dinspre:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_dinspre")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Către:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_catre")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Când a ajuns la intersecția / în dreptul imobilului nr.:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_intersectie_imobil")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1
        
        ctk.CTkLabel(content_nota_frame, text="A surprins și accidentat pe:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nume_victima1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        # TODO: Adaugă și celelalte victime dacă sunt mai multe, poate într-un Textbox
        r+=1
        ctk.CTkLabel(content_nota_frame, text="CNP victimă:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_cnp_victima1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Domiciliu victimă:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_adresa_victima1"), wraplength=400).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1

        ctk.CTkLabel(content_nota_frame, text="Care s-a angajat în traversarea străzii (detalii):").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkTextbox(content_nota_frame, height=60, wrap=tk.WORD, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_traversare_victima_detalii")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1

        ctk.CTkLabel(content_nota_frame, text="Din accident a rezultat vătămarea corporală a numitului(ei):").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nume_victima1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Care a fost transportat/ă la Spitalul:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkEntry(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_spital_victima")).grid(row=r, column=1, padx=2, pady=2, sticky="ew")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="cu diagnosticul:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_diagnostic_victima1"), wraplength=400).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1

        ctk.CTkLabel(content_nota_frame, text="Conducătorul auto testat etilotest, rezultat:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_rezultat_etilotest_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        ctk.CTkLabel(content_nota_frame, text="S-a reținut PC:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_retinut_pc_sofer1")).grid(row=r, column=1, padx=2, pady=2, sticky="w") # Va afișa 0 sau 1
        r+=1
        ctk.CTkLabel(content_nota_frame, text="Cazul filmat/mediatizat:").grid(row=r, column=0, padx=5, pady=2, sticky="w")
        ctk.CTkComboBox(content_nota_frame, width=150, variable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nt_caz_filmat_mediatizat"), values=["Poate fi mediatizat", "Nu poate fi mediatizat", "A fost filmat"], button_color=None).grid(row=r, column=1, padx=2, pady=2, sticky="w")
        r+=1
        # ... (Continuă cu restul câmpurilor și legăturile)

        # Întocmit de
        ctk.CTkLabel(content_nota_frame, text="Întocmit,").grid(row=r, column=0, columnspan=2, padx=5, pady=(10,2), sticky="w"); r+=1
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nume_agent1")).grid(row=r, column=0, padx=15, pady=2, sticky="w")
        ctk.CTkLabel(content_nota_frame, text="Șef tură,").grid(row=r, column=1, padx=5, pady=2, sticky="e"); r+=1
        ctk.CTkLabel(content_nota_frame, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nt_nume_agent2")).grid(row=r, column=0, padx=15, pady=2, sticky="w")
        # TODO: Adaugă un ComboBox sau Entry pentru numele șefului de tură dacă e diferit de agent2

    combo_nota_telex.configure(command=_on_nota_telex_select)

    # --- Funcții Callback pentru Tracing (definite în create_sub_tab_content) ---
    def _update_display_field(source_var_keys, target_var_key, format_func=None, default_val="N/A"):
        target_var = app_instance.data_vars.get(target_var_key)
        if not target_var: return

        source_values = []
        all_sources_valid = True
        for src_key in source_var_keys:
            source_var = app_instance.data_vars.get(src_key)
            if source_var:
                source_values.append(source_var.get())
            else:
                source_values.append(default_value_for_key(src_key)) # Folosește un default specific
                all_sources_valid = False # Poate nu vrem să actualizăm dacă o sursă lipsește

        if all_sources_valid or True: # Decide dacă actualizezi chiar dacă o sursă lipsește
            if format_func:
                target_var.set(format_func(*source_values))
            elif len(source_values) == 1:
                target_var.set(str(source_values[0]) if source_values[0] else default_val)
            else:
                target_var.set(default_val) # Fallback

    def default_value_for_key(key_name_part):
        if "ziua" in key_name_part: return "??"
        if "luna" in key_name_part: return "??"
        if "anul" in key_name_part: return "????"
        if "ora" in key_name_part: return "??:??"
        return "..."

    # --- Adaugă Tracing pentru actualizări în timp real ---
    for display_key_suffix, source_keys_list in NOTA_TELEX_DISPLAY_FIELDS.items():
        if not isinstance(source_keys_list, list): # Dacă e un tip de variabilă (pt câmpuri editabile)
            continue
        target_full_key = SUB_VAR_PREFIX + display_key_suffix
        
        # Creează variabila de display dacă nu există
        if target_full_key not in app_instance.data_vars:
            app_instance.data_vars[target_full_key] = tk.StringVar(value="N/A")

        # Definirea funcției de formatare specifică dacă e necesar
        formatter = None
        if display_key_suffix == "display_nt_data_acc":
            formatter = lambda zi, lu, an: f"{zi or '??'}.{lu or '??'}.{an or '????'}"
        elif display_key_suffix == "display_nt_retinut_pc_sofer1":
            formatter = lambda val: "DA" if val == 1 else "NU"


        for src_key in source_keys_list:
            source_var = app_instance.data_vars.get(src_key)
            if source_var:
                source_var.trace_add("write", lambda *args, sk_list=source_keys_list, tk=target_full_key, fmt=formatter: _update_display_field(sk_list, tk, fmt))
        _update_display_field(source_keys_list, target_full_key, formatter) # Apel inițial


def get_data(app_instance):
    """Colectează datele din acest sub-tab."""
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din sub-tab Nota Telex (CTk)...")

    # Salvează tipul de Notă Telex selectat
    selected_type_var = data_vars.get(SUB_VAR_PREFIX + NOTA_TELEX_TYPE_KEY)
    if selected_type_var:
        data[NOTA_TELEX_TYPE_KEY] = selected_type_var.get()

    # Salvează valorile câmpurilor editabile
    for key, var_type in NOTA_TELEX_DISPLAY_FIELDS.items():
        if isinstance(var_type, type): # Doar cele definite ca editabile
            full_key = SUB_VAR_PREFIX + key
            original_key = key # Sau un nume mai simplu dacă preferi
            if full_key in data_vars:
                data[original_key] = data_vars[full_key].get()
            else:
                data[original_key] = ""
    return data

def load_data(app_instance, data_to_load):
    """Încarcă datele în acest sub-tab."""
    data_vars = app_instance.data_vars
    print("Încărcare date în sub-tab Nota Telex (CTk)...")

    # Setează tipul de Notă Telex selectat
    selected_type_var = data_vars.get(SUB_VAR_PREFIX + NOTA_TELEX_TYPE_KEY)
    if selected_type_var and NOTA_TELEX_TYPE_KEY in data_to_load:
        selected_type_var.set(data_to_load[NOTA_TELEX_TYPE_KEY])
        # Forțează actualizarea UI-ului dacă e necesar (deja se face prin command)

    # Încarcă valorile câmpurilor editabile
    for key, var_type in NOTA_TELEX_DISPLAY_FIELDS.items():
        if isinstance(var_type, type):
            full_key = SUB_VAR_PREFIX + key
            original_key = key
            if original_key in data_to_load and full_key in data_vars:
                if isinstance(data_vars[full_key], tk.StringVar):
                    data_vars[full_key].set(str(data_to_load[original_key]) if data_to_load[original_key] is not None else "")
    
    # Variabilele de display sunt actualizate automat prin tracing.
