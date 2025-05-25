# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'Principal'.
(Versiune adaptată pentru CustomTkinter)
"""

import tkinter as tk
# from tkinter import ttk # Nu mai folosim ttk
import customtkinter as ctk # Folosim customtkinter
from tkinter import messagebox
import sys
import traceback

# Asigură-te că utils există și e corect
try:
    from core import utils
except ImportError as e:
    messagebox.showerror("Eroare Import Principal (CTk)", f"Nu s-a putut importa 'core.utils': {e}")
    # Continuăm fără handler RO dacă importul eșuează
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()


# Definirea cheilor pentru variabilele Tkinter asociate acestui tab
VAR_PREFIX = "principal_"
DATA_KEYS = [
    "ziua_doc", "luna_doc", "anul_doc", "nume_agent1", "insigna_agent1",
    "nume_agent2", "ora_disp", "ora_112", "nr_disp", "nr_telex", "nr_penal",
    "articol_penal", "nr_victime", "autor_necunoscut",
    "ziua_acc", "luna_acc", "anul_acc", "ora_accident", "locul_accidentului",
    "sector", "cfl_dela", "cfl_panala", "spital_dela", "spital_panala",
    "cfl_zi_noapte", "conditii_atmosferice", "conditii_lumina", "tip_lumina1",
    "bifa_masuratori", "bifa_aparat_foto", "bifa_camera_video",
    "numar_vehicule", "numar_raniti_grav", "numar_raniti_usor",
    "lat_nord", "lat_est"
]

# --- MODIFICARE NUME FUNCȚIE ---
def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'Principal'
    folosind widget-uri CustomTkinter.

    Args:
        parent_container (ctk.CTkFrame): Containerul oferit de CTkTabview.
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    # Nu mai returnăm un frame, populăm direct parent_container
    # Configurăm grid-ul containerului părinte pentru a permite extinderea
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_columnconfigure(1, weight=1)
    # Row 0 va conține frame_principale și frame_detalii_cfl
    # Row 1 va conține frame_autor_necunoscut și frame_detalii_cfl (continuare)
    # Row 2 va conține frame_accident și frame_eac
    parent_container.grid_rowconfigure(2, weight=1) # Permite extinderea pe verticală (opțional)


    # --- Definire Variabile Tkinter (păstrăm tk.StringVar/IntVar) ---
    # Creează variabilele doar dacă nu există deja
    app_instance.data_vars.setdefault(VAR_PREFIX + 'autor_necunoscut', tk.StringVar(value="NU"))

    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if full_key not in app_instance.data_vars:
            if key.startswith("bifa_"):
                 app_instance.data_vars[full_key] = tk.IntVar(value=0)
            elif key != "autor_necunoscut":
                 app_instance.data_vars[full_key] = tk.StringVar()


    # --- Funcție pentru actualizare culoare text "Autor Necunoscut" ---
    autor_necunoscut_label_ref = {}
    def update_autor_necunoscut_color(*args):
        var = app_instance.data_vars.get(VAR_PREFIX + 'autor_necunoscut')
        label = autor_necunoscut_label_ref.get('label')
        if label and var:
            # Folosim culorile temei curente
            theme_colors = ctk.ThemeManager.theme["CTkLabel"]
            default_color = theme_colors["text_color"]
            color = "red" if var.get() == "DA" else default_color
            label.configure(text_color=color) # Folosim text_color pentru CTkLabel

    autor_var = app_instance.data_vars.get(VAR_PREFIX + 'autor_necunoscut')
    if autor_var:
        autor_var.trace_add("write", update_autor_necunoscut_color)


    # --- Creare Cadre (folosind CTkFrame) ---
    frame_principale = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_principale.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    ctk.CTkLabel(frame_principale, text="Date principale", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=6, pady=(5, 10), padx=10, sticky="ew")

    frame_autor_necunoscut = ctk.CTkFrame(parent_container, fg_color="transparent") # Fără margine/fundal
    frame_autor_necunoscut.grid(row=1, column=0, padx=15, pady=5, sticky="w") # Aliniat stânga

    frame_accident = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_accident.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    ctk.CTkLabel(frame_accident, text="Date Accident", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=8, pady=(5, 10), padx=10, sticky="ew")

    frame_detalii_cfl = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_detalii_cfl.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")
    ctk.CTkLabel(frame_detalii_cfl, text="Detalii CFL", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5, 10), padx=10, sticky="ew")

    frame_eac = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    frame_eac.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    ctk.CTkLabel(frame_eac, text="Detalii FIȘĂ EAC", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 10), padx=10, sticky="ew")


    # --- Populare Frame 'Date principale' (cu widget-uri CTk) ---
    row_idx = 1 # Începem de la rândul 1 după titlu
    ctk.CTkLabel(frame_principale, text="Ziua:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_ziua = ctk.CTkEntry(frame_principale, width=60,
                              textvariable=app_instance.data_vars.get(VAR_PREFIX + 'ziua_doc'))
    entry_ziua.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_principale, text="Luna:").grid(row=row_idx, column=2, padx=(10,2), pady=2, sticky="w")
    entry_luna = ctk.CTkEntry(frame_principale, width=60,
                              textvariable=app_instance.data_vars.get(VAR_PREFIX + 'luna_doc'))
    entry_luna.grid(row=row_idx, column=3, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_principale, text="Anul:").grid(row=row_idx, column=4, padx=(10,2), pady=2, sticky="w")
    entry_anul = ctk.CTkEntry(frame_principale, width=60,
                              textvariable=app_instance.data_vars.get(VAR_PREFIX + 'anul_doc'))
    entry_anul.grid(row=row_idx, column=5, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Nume Agent:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_agent1 = ctk.CTkEntry(frame_principale, width=200,
                                textvariable=app_instance.data_vars.get(VAR_PREFIX + 'nume_agent1'))
    entry_agent1.grid(row=row_idx, column=1, columnspan=3, padx=2, pady=2, sticky="ew")
    entry_agent1.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_principale, text="Insigna:").grid(row=row_idx, column=4, padx=(10,2), pady=2, sticky="w")
    entry_insigna = ctk.CTkEntry(frame_principale, width=70,
                                 textvariable=app_instance.data_vars.get(VAR_PREFIX + 'insigna_agent1'))
    entry_insigna.grid(row=row_idx, column=5, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Nume Agent 2:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_agent2 = ctk.CTkEntry(frame_principale, width=200,
                                textvariable=app_instance.data_vars.get(VAR_PREFIX + 'nume_agent2'))
    entry_agent2.grid(row=row_idx, column=1, columnspan=3, padx=2, pady=2, sticky="ew")
    entry_agent2.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Ora Dispecerat:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_ora_disp = ctk.CTkEntry(frame_principale, width=60,
                                  textvariable=app_instance.data_vars.get(VAR_PREFIX + 'ora_disp'))
    entry_ora_disp.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_principale, text="112:").grid(row=row_idx, column=2, padx=(10,2), pady=2, sticky="w")
    entry_ora_112 = ctk.CTkEntry(frame_principale, width=60,
                                 textvariable=app_instance.data_vars.get(VAR_PREFIX + 'ora_112'))
    entry_ora_112.grid(row=row_idx, column=3, padx=2, pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Nr. Dispecerat:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nr_disp = ctk.CTkEntry(frame_principale, width=150,
                                 textvariable=app_instance.data_vars.get(VAR_PREFIX + 'nr_disp'))
    entry_nr_disp.grid(row=row_idx, column=1, columnspan=2, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_principale, text="Nr. Telex:").grid(row=row_idx, column=3, padx=(10,2), pady=2, sticky="w")
    entry_nr_telex = ctk.CTkEntry(frame_principale, width=150,
                                  textvariable=app_instance.data_vars.get(VAR_PREFIX + 'nr_telex'))
    entry_nr_telex.grid(row=row_idx, column=4, columnspan=2, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Nr. Penal:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nr_penal = ctk.CTkEntry(frame_principale, width=150,
                                  textvariable=app_instance.data_vars.get(VAR_PREFIX + 'nr_penal'))
    entry_nr_penal.grid(row=row_idx, column=1, columnspan=2, padx=2, pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Articol Penal:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_art_penal = ctk.CTkComboBox(frame_principale, width=250, state="readonly",
                                      variable=app_instance.data_vars.get(VAR_PREFIX + 'articol_penal'),
                                      values=['art. 196 alin. 2 și 3', 'art. 196 alin. 1,2 și 3', 'art. 196 alin 2,3 și 4'],
                                      button_color=None)
    combo_art_penal.grid(row=row_idx, column=1, columnspan=3, padx=2, pady=(2,10), sticky="w")
    combo_art_penal.set('art. 196 alin. 2 și 3')
    row_idx += 1

    ctk.CTkLabel(frame_principale, text="Număr victime:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_nr_victime = ctk.CTkComboBox(frame_principale, width=80, state="readonly",
                                       variable=app_instance.data_vars.get(VAR_PREFIX + 'nr_victime'),
                                       values=['unei'] + [str(i) for i in range(2, 21)],
                                       button_color=None)
    combo_nr_victime.grid(row=row_idx, column=1, padx=2, pady=(2,10), sticky="w")
    combo_nr_victime.set('unei')
    row_idx += 1

    # --- Populare Frame 'Autor Necunoscut' (cu widget-uri CTk) ---
    autor_label = ctk.CTkLabel(frame_autor_necunoscut, text="AUTOR NECUNOSCUT:")
    autor_label.pack(side=tk.LEFT, padx=(0, 10))
    autor_necunoscut_label_ref['label'] = autor_label

    radio_da = ctk.CTkRadioButton(frame_autor_necunoscut, text="DA", value="DA",
                                  variable=app_instance.data_vars.get(VAR_PREFIX + 'autor_necunoscut'))
    radio_da.pack(side=tk.LEFT, padx=5)
    radio_nu = ctk.CTkRadioButton(frame_autor_necunoscut, text="NU", value="NU",
                                  variable=app_instance.data_vars.get(VAR_PREFIX + 'autor_necunoscut'))
    radio_nu.pack(side=tk.LEFT, padx=5)
    update_autor_necunoscut_color() # Setează culoarea inițială


    # --- Populare Frame 'Date Accident' (cu widget-uri CTk) ---
    row_idx = 1 # Începem de la rândul 1 după titlu
    ctk.CTkLabel(frame_accident, text="Ziua Accidentului:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_ziua_acc = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'ziua_acc'))
    entry_ziua_acc.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_accident, text="Luna:").grid(row=row_idx, column=2, padx=(10,2), pady=2, sticky="w")
    entry_luna_acc = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'luna_acc'))
    entry_luna_acc.grid(row=row_idx, column=3, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_accident, text="Anul:").grid(row=row_idx, column=4, padx=(10,2), pady=2, sticky="w")
    entry_anul_acc = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'anul_acc'))
    entry_anul_acc.grid(row=row_idx, column=5, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_accident, text="Ora Accidentului:").grid(row=row_idx, column=6, padx=(10,2), pady=2, sticky="w")
    entry_ora_acc = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'ora_accident'))
    entry_ora_acc.grid(row=row_idx, column=7, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_accident, text="Locul Accidentului:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_loc_acc = ctk.CTkEntry(frame_accident, placeholder_text="Locația...",
                                 textvariable=app_instance.data_vars.get(VAR_PREFIX + 'locul_accidentului'))
    entry_loc_acc.grid(row=row_idx, column=1, columnspan=5, padx=2, pady=2, sticky="ew")
    entry_loc_acc.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_accident, text="Sector:").grid(row=row_idx, column=6, padx=(10,2), pady=2, sticky="w")
    entry_sector = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'sector'))
    entry_sector.grid(row=row_idx, column=7, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_accident, text="Ora CFL:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_cfl_dela = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'cfl_dela'))
    entry_cfl_dela.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_accident, text="--").grid(row=row_idx, column=2, padx=5, pady=0)
    entry_cfl_panala = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'cfl_panala'))
    entry_cfl_panala.grid(row=row_idx, column=3, padx=2, pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_accident, text="Ora Spital:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_spital_dela = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'spital_dela'))
    entry_spital_dela.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_accident, text="--").grid(row=row_idx, column=2, padx=5, pady=0)
    entry_spital_panala = ctk.CTkEntry(frame_accident, width=60, textvariable=app_instance.data_vars.get(VAR_PREFIX + 'spital_panala'))
    entry_spital_panala.grid(row=row_idx, column=3, padx=2, pady=(2,10), sticky="w")
    row_idx += 1


    # --- Populare Frame 'Detalii CFL' (cu widget-uri CTk) ---
    row_idx = 1 # Începem de la rândul 1 după titlu
    ctk.CTkLabel(frame_detalii_cfl, text="A fost efectuat pe timp de:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_cfl_timp = ctk.CTkComboBox(frame_detalii_cfl, width=100, state="readonly",
                                     variable=app_instance.data_vars.get(VAR_PREFIX + 'cfl_zi_noapte'),
                                     values=['zi', 'noapte'], button_color=None)
    combo_cfl_timp.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    combo_cfl_timp.set('zi')
    row_idx += 1

    ctk.CTkLabel(frame_detalii_cfl, text="În condiții atmosferice:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_cfl_atmos = ctk.CTkComboBox(frame_detalii_cfl, width=150, state="readonly",
                                      variable=app_instance.data_vars.get(VAR_PREFIX + 'conditii_atmosferice'),
                                      values=['normale', 'lapoviță', 'ninsoare', 'ploaie', 'ceață', 'vânt puternic', 'viscol'],
                                      button_color=None)
    combo_cfl_atmos.grid(row=row_idx, column=1, columnspan=2, padx=2, pady=2, sticky="w")
    combo_cfl_atmos.set('normale')
    row_idx += 1

    ctk.CTkLabel(frame_detalii_cfl, text="În condiții de lumină:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_cfl_lumina = ctk.CTkComboBox(frame_detalii_cfl, width=120, state="readonly",
                                       variable=app_instance.data_vars.get(VAR_PREFIX + 'conditii_lumina'),
                                       values=['naturală', 'artificială'], button_color=None)
    combo_cfl_lumina.grid(row=row_idx, column=1, padx=2, pady=2, sticky="w")
    combo_cfl_lumina.set('naturală')
    row_idx += 1

    ctk.CTkLabel(frame_detalii_cfl, text="astfel:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    combo_cfl_tip_lumina = ctk.CTkComboBox(frame_detalii_cfl, width=300, state="readonly",
                                           variable=app_instance.data_vars.get(VAR_PREFIX + 'tip_lumina1'),
                                           values=['', 'în zori', 'la lumina zilei', 'soare orbitor', 'cer înnorat',
                                                   'fum/praf', 'în amurg', 'iluminat stradal funcțional',
                                                   'iluminat stradal nefuncțional', 'iluminat stradal oprit',
                                                   'fără iluminat stradal', 'alte mijloace de iluminare'],
                                           button_color=None)
    combo_cfl_tip_lumina.grid(row=row_idx, column=1, columnspan=2, padx=(2,10), pady=2, sticky="ew")
    combo_cfl_tip_lumina.set('la lumina zilei')
    row_idx += 1

    check_masuratori = ctk.CTkCheckBox(frame_detalii_cfl, text="au fost efectuate Măsurători cu ruleta metrică;",
                                       variable=app_instance.data_vars.get(VAR_PREFIX + 'bifa_masuratori'), onvalue=1, offvalue=0)
    check_masuratori.grid(row=row_idx, column=0, columnspan=3, padx=10, pady=2, sticky="w")
    row_idx += 1
    check_foto = ctk.CTkCheckBox(frame_detalii_cfl, text="au fost efectuate Fotografii Judiciare;",
                                 variable=app_instance.data_vars.get(VAR_PREFIX + 'bifa_aparat_foto'), onvalue=1, offvalue=0)
    check_foto.grid(row=row_idx, column=0, columnspan=3, padx=10, pady=2, sticky="w")
    row_idx += 1
    check_video = ctk.CTkCheckBox(frame_detalii_cfl, text="a fost efectuată Video - Filmare Judiciară;",
                                  variable=app_instance.data_vars.get(VAR_PREFIX + 'bifa_camera_video'), onvalue=1, offvalue=0)
    check_video.grid(row=row_idx, column=0, columnspan=3, padx=10, pady=(2,10), sticky="w")
    row_idx += 1


    # --- Populare Frame 'Detalii FIȘĂ EAC' (cu widget-uri CTk) ---
    row_idx = 1 # Începem de la rândul 1 după titlu
    ctk.CTkLabel(frame_eac, text="Număr Vehicule implicate:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nr_veh = ctk.CTkEntry(frame_eac, width=80,
                                textvariable=app_instance.data_vars.get(VAR_PREFIX + 'numar_vehicule'))
    entry_nr_veh.grid(row=row_idx, column=1, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_eac, text="Număr Răniți Grav:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nr_rg = ctk.CTkEntry(frame_eac, width=80,
                               textvariable=app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_grav'))
    entry_nr_rg.grid(row=row_idx, column=1, padx=(2,10), pady=2, sticky="w")
    if not app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_grav').get():
        app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_grav').set('---')
    row_idx += 1

    ctk.CTkLabel(frame_eac, text="Număr Răniți Usor:").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_nr_ru = ctk.CTkEntry(frame_eac, width=80,
                               textvariable=app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_usor'))
    entry_nr_ru.grid(row=row_idx, column=1, padx=(2,10), pady=2, sticky="w")
    if not app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_usor').get():
        app_instance.data_vars.get(VAR_PREFIX + 'numar_raniti_usor').set('---')
    row_idx += 1

    ctk.CTkLabel(frame_eac, text="Poziție GPS: Lat. N").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_lat_n = ctk.CTkEntry(frame_eac, width=120,
                               textvariable=app_instance.data_vars.get(VAR_PREFIX + 'lat_nord'))
    entry_lat_n.grid(row=row_idx, column=1, padx=(2,10), pady=2, sticky="w")
    row_idx += 1

    ctk.CTkLabel(frame_eac, text="                Lat. E").grid(row=row_idx, column=0, padx=(10,2), pady=2, sticky="w")
    entry_lat_e = ctk.CTkEntry(frame_eac, width=120,
                               textvariable=app_instance.data_vars.get(VAR_PREFIX + 'lat_est'))
    entry_lat_e.grid(row=row_idx, column=1, padx=(2,10), pady=(2,10), sticky="w")
    row_idx += 1


    # Nu mai returnăm nimic


# --- Funcții get/load data (cu corecție) ---

# --- MODIFICARE SEMNĂTURĂ ---
def get_data(app_instance):
    """
    Colectează datele din variabilele Tkinter pentru acest tab (Versiune CTk).

    Args:
        app_instance (AppWindow): Instanța principală a aplicației.

    Returns:
        dict: Dicționar cu datele din acest tab.
    """
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din tab Principal (CTk)...")
    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if full_key in data_vars:
            try:
                data[key] = data_vars[full_key].get()
            except Exception as e:
                print(f"Eroare la citirea variabilei {full_key}: {e}", file=sys.stderr)
                data[key] = None
        else:
            print(f"Avertisment: Cheia {full_key} nu a fost găsită la colectare.", file=sys.stderr)
            data[key] = None
    return data

# --- MODIFICARE SEMNĂTURĂ ---
def load_data(app_instance, data_to_load):
    """
    Încarcă datele primite în variabilele Tkinter pentru acest tab (Versiune CTk).

    Args:
        app_instance (AppWindow): Instanța principală a aplicației.
        data_to_load (dict): Dicționarul cu datele de încărcat.
    """
    data_vars = app_instance.data_vars
    print("Încărcare date în tab Principal (CTk)...")
    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if key in data_to_load and full_key in data_vars:
            try:
                target_var = data_vars[full_key]
                value_from_data = data_to_load[key]

                if isinstance(target_var, tk.IntVar):
                    value_to_set = 1 if value_from_data else 0
                    target_var.set(value_to_set)
                elif isinstance(target_var, tk.StringVar):
                    value_to_set = str(value_from_data) if value_from_data is not None else ""
                    target_var.set(value_to_set)
                # else: Nu ar trebui să avem alte tipuri

            except tk.TclError as e:
                 print(f"Avertisment: Nu s-a putut seta valoarea pentru {full_key}: {e}", file=sys.stderr)
            except Exception as e:
                 print(f"Eroare la încărcarea datei pentru {full_key}: {e}", file=sys.stderr)

    # Asigură actualizarea culorii pentru autor necunoscut după încărcare
    autor_var = data_vars.get(VAR_PREFIX + 'autor_necunoscut')
    if autor_var:
        autor_var.set(autor_var.get()) # Forțează rularea callback-ului

