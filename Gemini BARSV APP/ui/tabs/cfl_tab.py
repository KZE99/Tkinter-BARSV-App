# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'CFL'.
(Versiune adaptată și completată pentru CustomTkinter)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

try:
    from core import utils
except ImportError as e:
    messagebox.showerror("Eroare Import CFL (CTk)", f"Nu s-a putut importa 'core.utils': {e}")
    class DummyUtils: # Fallback
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()

# Prefix pentru cheile variabilelor din acest tab
VAR_PREFIX = "cfl_"

# Cheile de date pentru acest tab
DATA_KEYS = [
    "vatamaretip1", "vatamaretip2", "criminalist1", "criminalist2",
    "agent_zona1", "agent_zona2", "serviciu_zona",
    "bifa_pv", "bifa_documente", "bifa_bunuri",
    "bifa_echipe_medicale", "bifa_pompieri", "bifa_descarcerare",
    "auto_descarerat", "aufost_mutate", "mutat_mutate", "cu_fara",
    "acestui_acestor", "a_nua_pututfi", "text_auto_mutate",
    "tip_carosabil", "aderenta_carosabil", "palier_rampa", "drumul_prezinta",
    "latime_drum", "sensuri_circulatie_drum", "are_nuare_marcaje",
    "primul_marcaj", "aldoilea_marcaj", "text_latime_benzi",
    "text_alte_marcaje", "calitate_marcaje", "linii_tramvai",
    "exista_trotuare", "latime_trotuar", "exista_spatii_verzi", "latime_spv",
    "semafoare_auto", "semafoare_pietonale", "text_indicatoare",
    "identificare_viteza", "limita_viteza", "text_limitare_viteza",
    "locul_indicat", "text_locul_indicat", "text_alte_particularitati",
    "text_urme_cfl", "locul_indicat_victima", "text_locul_ridicat_victima",
    "aufost_camere", "text_camere"
]

# --- Funcții Helper Text <-> StringVar (Ideal în utils.py) ---
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

def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'CFL'.
    """
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_columnconfigure(0, weight=1)

    inner_tabview = ctk.CTkTabview(parent_container, border_width=1)
    inner_tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    tab1_name = " Detalii de la fața locului "
    tab2_name = " Activitati CFL "
    inner_tabview.add(tab1_name)
    inner_tabview.add(tab2_name)
    inner_tabview.set(tab1_name)

    sub_tab1_container = inner_tabview.tab(tab1_name)
    sub_tab2_container = inner_tabview.tab(tab2_name)

    # --- Definire Variabile Tkinter ---
    for key in DATA_KEYS:
        full_key = VAR_PREFIX + key
        if full_key not in app_instance.data_vars:
            if key.startswith("bifa_"):
                 app_instance.data_vars[full_key] = tk.IntVar(value=0)
            else:
                 app_instance.data_vars[full_key] = tk.StringVar()

    # --- Sub-Tab 1: Detalii de la fața locului ---
    sub_tab1_container.grid_rowconfigure(0, weight=1)
    sub_tab1_container.grid_columnconfigure(0, weight=1)
    sub_tab1_scroll = ctk.CTkScrollableFrame(sub_tab1_container, label_text="")
    sub_tab1_scroll.grid(row=0, column=0, sticky="nsew")
    content_frame1 = sub_tab1_scroll
    content_frame1.columnconfigure(0, weight=1)

    current_row_s1 = 0
    # Frame Tip Vătămare
    frame_vatamare = ctk.CTkFrame(content_frame1, border_width=1, corner_radius=10)
    frame_vatamare.grid(row=current_row_s1, column=0, padx=5, pady=5, sticky="ew")
    ctk.CTkLabel(frame_vatamare, text="Tip Vătămare", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5, 10), padx=10, sticky="ew")
    # ... (restul widget-urilor din frame_vatamare ca în versiunea anterioară) ...
    ctk.CTkLabel(frame_vatamare, text="●").grid(row=1, column=0, sticky="w", padx=(5, 5))
    combo_vt1 = ctk.CTkComboBox(frame_vatamare, width=200, state="readonly",
                             variable=app_instance.data_vars[VAR_PREFIX + 'vatamaretip1'],
                             values=['Vătămarea corporală a', 'Decesul a'], button_color=None)
    combo_vt1.grid(row=1, column=1, padx=2, pady=2, sticky="w")
    combo_vt1.set('Vătămarea corporală a')
    ctk.CTkLabel(frame_vatamare, text="- _____ - persoane").grid(row=1, column=2, padx=5, pady=2, sticky="w")
    ctk.CTkLabel(frame_vatamare, text="●").grid(row=2, column=0, sticky="w", padx=(5, 5))
    combo_vt2 = ctk.CTkComboBox(frame_vatamare, width=500, state="readonly",
                             variable=app_instance.data_vars[VAR_PREFIX + 'vatamaretip2'],
                             values=['Autorul nu a părăsit locul faptei',
                                     'Autorul a părăsit locul faptei',
                                     'Autorul nu a părăsit locul faptei, abandonând autovehiculul la fața locului',
                                     'Autorul nu a părăsit locul faptei, transportând victima la spital'],
                             button_color=None)
    combo_vt2.grid(row=2, column=1, columnspan=2, padx=2, pady=(2,5), sticky="ew")
    combo_vt2.set('Autorul nu a părăsit locul faptei')
    current_row_s1 += 1

    # Frame Criminalisti
    frame_criminalisti = ctk.CTkFrame(content_frame1, border_width=1, corner_radius=10)
    frame_criminalisti.grid(row=current_row_s1, column=0, padx=5, pady=5, sticky="ew")
    frame_criminalisti.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_criminalisti, text="Criminalisti", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 10), sticky="ew")
    # ... (restul widget-urilor din frame_criminalisti) ...
    ctk.CTkLabel(frame_criminalisti, text="Criminalist 1:").grid(row=1, column=0, padx=(5,2), pady=2, sticky="w")
    entry_crim1 = ctk.CTkEntry(frame_criminalisti, textvariable=app_instance.data_vars[VAR_PREFIX + 'criminalist1'])
    entry_crim1.grid(row=1, column=1, padx=(0,5), pady=2, sticky="ew")
    entry_crim1.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_criminalisti, text="Criminalist 2:").grid(row=2, column=0, padx=(5,2), pady=2, sticky="w")
    entry_crim2 = ctk.CTkEntry(frame_criminalisti, textvariable=app_instance.data_vars[VAR_PREFIX + 'criminalist2'])
    entry_crim2.grid(row=2, column=1, padx=(0,5), pady=(2,5), sticky="ew")
    entry_crim2.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    current_row_s1 += 1

    # Frame Agenti din teren
    frame_agenti = ctk.CTkFrame(content_frame1, border_width=1, corner_radius=10)
    frame_agenti.grid(row=current_row_s1, column=0, padx=5, pady=5, sticky="ew")
    frame_agenti.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_agenti, text="Agenti din teren la fața locului", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 10), sticky="ew")
    # ... (restul widget-urilor din frame_agenti) ...
    ag_row = 1
    ctk.CTkLabel(frame_agenti, text="Agent Zona 1:").grid(row=ag_row, column=0, padx=(5,2), pady=2, sticky="w")
    entry_ag_zona1 = ctk.CTkEntry(frame_agenti, textvariable=app_instance.data_vars[VAR_PREFIX + 'agent_zona1'])
    entry_ag_zona1.grid(row=ag_row, column=1, padx=(0,5), pady=2, sticky="ew")
    entry_ag_zona1.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ag_row += 1
    ctk.CTkLabel(frame_agenti, text="Agent Zona 2:").grid(row=ag_row, column=0, padx=(5,2), pady=2, sticky="w")
    entry_ag_zona2 = ctk.CTkEntry(frame_agenti, textvariable=app_instance.data_vars[VAR_PREFIX + 'agent_zona2'])
    entry_ag_zona2.grid(row=ag_row, column=1, padx=(0,5), pady=2, sticky="ew")
    entry_ag_zona2.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ag_row += 1
    ctk.CTkLabel(frame_agenti, text="Serviciu:").grid(row=ag_row, column=0, padx=(5,2), pady=2, sticky="w")
    combo_serv_zona = ctk.CTkComboBox(frame_agenti, width=180, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'serviciu_zona'],
                                   values=['SSRS 3-4-5', 'SSRS 1-2-6', 'SOS - BMT'], button_color=None)
    combo_serv_zona.grid(row=ag_row, column=1, padx=(0,5), pady=2, sticky="w")
    ag_row += 1
    ctk.CTkLabel(frame_agenti, text="De la care am preluat:").grid(row=ag_row, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    ag_row += 1
    chk_pv = ctk.CTkCheckBox(frame_agenti, text="procesul-verbal de sesizare;",
                             variable=app_instance.data_vars[VAR_PREFIX + 'bifa_pv'], onvalue=1, offvalue=0)
    chk_pv.grid(row=ag_row, column=0, columnspan=2, padx=10, pady=1, sticky="w")
    ag_row += 1
    chk_doc = ctk.CTkCheckBox(frame_agenti, text="documentele persoanelor implicate în accident;",
                              variable=app_instance.data_vars[VAR_PREFIX + 'bifa_documente'], onvalue=1, offvalue=0)
    chk_doc.grid(row=ag_row, column=0, columnspan=2, padx=10, pady=1, sticky="w")
    ag_row += 1
    chk_bunuri = ctk.CTkCheckBox(frame_agenti, text="bunuri sau valori aparținând persoanelor implicate în accident.",
                                 variable=app_instance.data_vars[VAR_PREFIX + 'bifa_bunuri'], onvalue=1, offvalue=0)
    chk_bunuri.grid(row=ag_row, column=0, columnspan=2, padx=10, pady=(1,5), sticky="w")
    app_instance.data_vars[VAR_PREFIX + 'bifa_pv'].set(1)
    app_instance.data_vars[VAR_PREFIX + 'bifa_documente'].set(1)
    current_row_s1 += 1

    # Frame Modificări Loc Faptă
    frame_modificari = ctk.CTkFrame(content_frame1, border_width=1, corner_radius=10)
    frame_modificari.grid(row=current_row_s1, column=0, padx=5, pady=5, sticky="ew")
    frame_modificari.columnconfigure(3, weight=1)
    ctk.CTkLabel(frame_modificari, text="Până la sosirea echipei de cercetare...", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=4, pady=(5, 10), sticky="ew")
    # ... (restul widget-urilor din frame_modificari) ...
    mod_row = 1
    chk_med = ctk.CTkCheckBox(frame_modificari, text="au intervenit echipe medicale...",
                              variable=app_instance.data_vars[VAR_PREFIX + 'bifa_echipe_medicale'], onvalue=1, offvalue=0)
    chk_med.grid(row=mod_row, column=0, columnspan=4, padx=10, pady=1, sticky="w")
    mod_row += 1
    chk_pomp = ctk.CTkCheckBox(frame_modificari, text="au intervenit echipe de pompieri...",
                               variable=app_instance.data_vars[VAR_PREFIX + 'bifa_pompieri'], onvalue=1, offvalue=0)
    chk_pomp.grid(row=mod_row, column=0, columnspan=4, padx=10, pady=1, sticky="w")
    mod_row += 1
    chk_desc = ctk.CTkCheckBox(frame_modificari, text="s-a intervenit în vederea descarcerării...",
                               variable=app_instance.data_vars[VAR_PREFIX + 'bifa_descarcerare'], onvalue=1, offvalue=0)
    chk_desc.grid(row=mod_row, column=0, padx=10, pady=1, sticky="w")
    entry_auto_desc = ctk.CTkEntry(frame_modificari, width=200,
                                   textvariable=app_instance.data_vars[VAR_PREFIX + 'auto_descarerat'])
    entry_auto_desc.grid(row=mod_row, column=1, columnspan=3, padx=2, pady=1, sticky="ew")
    mod_row += 1
    ctk.CTkLabel(frame_modificari, text="Vehiculul/ Vehiculele:").grid(row=mod_row, column=0, columnspan=4, padx=5, pady=5, sticky="w")
    mod_row += 1
    combo_mutat1 = ctk.CTkComboBox(frame_modificari, width=110, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'aufost_mutate'],
                                   values=['A fost', 'Au fost', 'Nu a fost', 'Nu au fost'], button_color=None)
    combo_mutat1.grid(row=mod_row, column=0, padx=(5,2), pady=2, sticky="w")
    combo_mutat1.set('Nu au fost')
    combo_mutat2 = ctk.CTkComboBox(frame_modificari, width=110, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'mutat_mutate'],
                                   values=['mutat', 'mutate'], button_color=None)
    combo_mutat2.grid(row=mod_row, column=1, padx=2, pady=2, sticky="w")
    combo_mutat2.set('mutate')
    combo_mutat3 = ctk.CTkComboBox(frame_modificari, width=110, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'cu_fara'],
                                   values=['cu', 'fara'], button_color=None)
    combo_mutat3.grid(row=mod_row, column=2, padx=2, pady=2, sticky="w")
    combo_mutat3.set('fara')
    ctk.CTkLabel(frame_modificari, text="acordul echpei...").grid(row=mod_row, column=3, padx=(5,5), pady=2, sticky="w")
    mod_row += 1
    ctk.CTkLabel(frame_modificari, text="Poziția inițială").grid(row=mod_row, column=0, padx=(5,2), pady=2, sticky="w")
    combo_poz1 = ctk.CTkComboBox(frame_modificari, width=160, state="readonly",
                                 variable=app_instance.data_vars[VAR_PREFIX + 'acestui_acestor'],
                                 values=['a acestui vehicul', 'a acestor vehicule'], button_color=None)
    combo_poz1.grid(row=mod_row, column=1, padx=2, pady=2, sticky="w")
    combo_poz1.set('a acestor vehicule')
    combo_poz2 = ctk.CTkComboBox(frame_modificari, width=130, state="readonly",
                                 variable=app_instance.data_vars[VAR_PREFIX + 'a_nua_pututfi'],
                                 values=['a putut fi', 'nu a putut fi'], button_color=None)
    combo_poz2.grid(row=mod_row, column=2, padx=2, pady=2, sticky="w")
    combo_poz2.set('a putut fi')
    ctk.CTkLabel(frame_modificari, text="stabilită astfel:").grid(row=mod_row, column=3, padx=(5,5), pady=2, sticky="w")
    mod_row += 1
    textbox_auto_mutate = ctk.CTkTextbox(frame_modificari, height=80, wrap=tk.WORD) # CTkTextbox
    textbox_auto_mutate.grid(row=mod_row, column=0, columnspan=4, padx=5, pady=(2,5), sticky="ew")
    textbox_auto_mutate.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    auto_mut_var = app_instance.data_vars[VAR_PREFIX + 'text_auto_mutate']
    if auto_mut_var:
        init_auto_mut = auto_mut_var.get()
        if init_auto_mut: textbox_auto_mutate.insert("1.0", init_auto_mut)
        textbox_auto_mutate.bind("<FocusOut>", lambda event, w=textbox_auto_mutate, v=auto_mut_var: _update_var_from_text(w, v))
    current_row_s1 += 1


    # --- Sub-Tab 2: Activitati CFL ---
    sub_tab2_container.grid_rowconfigure(0, weight=1)
    sub_tab2_container.grid_columnconfigure(0, weight=1)
    sub_tab2_scroll = ctk.CTkScrollableFrame(sub_tab2_container, label_text="")
    sub_tab2_scroll.grid(row=0, column=0, sticky="nsew")
    content_frame2 = sub_tab2_scroll
    content_frame2.columnconfigure(0, weight=1) # Permite extinderea cadrelor interioare

    current_row_s2 = 0
    # Frame Fixarea locului Faptei
    frame_fixare = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_fixare.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_fixare.columnconfigure(3, weight=1) # Extindere combo/text
    ctk.CTkLabel(frame_fixare, text="Fixarea locului Faptei", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=5, pady=(5, 10), padx=10, sticky="ew")
    current_row_s2 += 1
    r_fix = 1
    # Linia 1
    ctk.CTkLabel(frame_fixare, text="Segmentul de drum... acoperit cu:").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_tip_carosabil = ctk.CTkComboBox(frame_fixare, width=120, state="readonly",
                                          variable=app_instance.data_vars[VAR_PREFIX + 'tip_carosabil'],
                                          values=['asfalt', 'beton', 'piatră cubică', 'pământ'], button_color=None)
    combo_tip_carosabil.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_tip_carosabil.set('asfalt')
    ctk.CTkLabel(frame_fixare, text="partea carosabilă fiind").grid(row=r_fix, column=2, padx=(10,2), pady=2, sticky="w")
    combo_aderenta = ctk.CTkComboBox(frame_fixare, width=160, state="readonly",
                                     variable=app_instance.data_vars[VAR_PREFIX + 'aderenta_carosabil'],
                                     values=['uscată', 'umedă', 'acoperită cu polei', 'acoperită cu zăpadă',
                                             'acoperită cu mâzgă', 'acoperită cu gheață', 'acoperită cu noroi'], button_color=None)
    combo_aderenta.grid(row=r_fix, column=3, columnspan=2, padx=(0,5), pady=2, sticky="ew")
    combo_aderenta.set('uscată')
    r_fix += 1
    # Linia 2
    ctk.CTkLabel(frame_fixare, text="În profilul longitudinal drumul este:").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_palier = ctk.CTkComboBox(frame_fixare, width=100, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'palier_rampa'],
                                   values=['în palier', 'în rampă'], button_color=None)
    combo_palier.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_palier.set('în palier')
    ctk.CTkLabel(frame_fixare, text="și").grid(row=r_fix, column=2, padx=(10,2), pady=2, sticky="w")
    combo_prez_curbe = ctk.CTkComboBox(frame_fixare, width=120, state="readonly",
                                       variable=app_instance.data_vars[VAR_PREFIX + 'drumul_prezinta'],
                                       values=['prezintă', 'nu prezintă'], button_color=None)
    combo_prez_curbe.grid(row=r_fix, column=3, padx=2, pady=2, sticky="w")
    combo_prez_curbe.set('nu prezintă')
    ctk.CTkLabel(frame_fixare, text="curbe și declivități.").grid(row=r_fix, column=4, padx=(0,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 3
    ctk.CTkLabel(frame_fixare, text="Pe porțiunea respectivă de drum având o lățime de").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    entry_latime_drum = ctk.CTkEntry(frame_fixare, width=70, textvariable=app_instance.data_vars[VAR_PREFIX + 'latime_drum'])
    entry_latime_drum.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_fixare, text="m, circulația rutieră se desfășoară").grid(row=r_fix, column=2, columnspan=3, padx=(5,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 4
    combo_sensuri = ctk.CTkComboBox(frame_fixare, width=180, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'sensuri_circulatie_drum'],
                                    values=['pe ambele sensuri', 'pe un singur sens'], button_color=None)
    combo_sensuri.grid(row=r_fix, column=0, columnspan=2, padx=(5,2), pady=2, sticky="w")
    combo_sensuri.set('pe ambele sensuri')
    combo_marcaje = ctk.CTkComboBox(frame_fixare, width=350, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'are_nuare_marcaje'],
                                    values=['și are aplicate marcaje longitudinale cu linie', 'și nu are aplicate marcaje'], button_color=None)
    combo_marcaje.grid(row=r_fix, column=2, columnspan=3, padx=(5,5), pady=2, sticky="ew")
    combo_marcaje.set('și are aplicate marcaje longitudinale cu linie')
    r_fix += 1
    # Linia 5
    combo_marcaj1 = ctk.CTkComboBox(frame_fixare, width=250, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'primul_marcaj'],
                                    values=['continuă', 'discontinuă', 'fără marcaj', '. . . . . . . . . . . . . . . . . . . . . . . . . . . .'], button_color=None)
    combo_marcaj1.grid(row=r_fix, column=0, columnspan=2, padx=(5,2), pady=2, sticky="w")
    combo_marcaj1.set('. . . . . . . . . . . . . . . . . . . . . . . . . . . .')
    ctk.CTkLabel(frame_fixare, text="de separare a sensurilor de circulație și cu linie").grid(row=r_fix, column=2, columnspan=3, padx=(5,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 6
    combo_marcaj2 = ctk.CTkComboBox(frame_fixare, width=250, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'aldoilea_marcaj'],
                                    values=['continuă', 'discontinuă', 'fără marcaj', '. . . . . . . . . . . . . . . . . . . . . . . . . . . .'], button_color=None)
    combo_marcaj2.grid(row=r_fix, column=0, columnspan=2, padx=(5,2), pady=2, sticky="w")
    combo_marcaj2.set('. . . . . . . . . . . . . . . . . . . . . . . . . . . .')
    ctk.CTkLabel(frame_fixare, text="de separare a benzilor de circulație de pe același sens,").grid(row=r_fix, column=2, columnspan=3, padx=(5,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 7
    ctk.CTkLabel(frame_fixare, text="fiecare bandă având o lățime de:").grid(row=r_fix, column=0, columnspan=5, padx=(5,5), pady=5, sticky="w")
    r_fix += 1
    # Linia 8 - Text Latime Benzi
    textbox_lat_benzi = ctk.CTkTextbox(frame_fixare, height=40, wrap=tk.WORD) # CTkTextbox
    textbox_lat_benzi.grid(row=r_fix, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
    textbox_lat_benzi.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    lat_benzi_var = app_instance.data_vars[VAR_PREFIX + 'text_latime_benzi']
    if lat_benzi_var:
        init_lat_b = lat_benzi_var.get()
        if init_lat_b: textbox_lat_benzi.insert("1.0", init_lat_b)
        textbox_lat_benzi.bind("<FocusOut>", lambda event, w=textbox_lat_benzi, v=lat_benzi_var: _update_var_from_text(w, v))
    r_fix += 1
    # Linia 9 - Alte Marcaje
    ctk.CTkLabel(frame_fixare, text="Alte marcaje pentru reglementarea circulației rutiere:").grid(row=r_fix, column=0, columnspan=5, padx=(5,5), pady=5, sticky="w")
    r_fix += 1
    # Linia 10 - Text Alte Marcaje
    textbox_alte_marc = ctk.CTkTextbox(frame_fixare, height=60, wrap=tk.WORD) # CTkTextbox
    textbox_alte_marc.grid(row=r_fix, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
    textbox_alte_marc.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    alte_marc_var = app_instance.data_vars[VAR_PREFIX + 'text_alte_marcaje']
    if alte_marc_var:
        init_alte_m = alte_marc_var.get()
        if init_alte_m: textbox_alte_marc.insert("1.0", init_alte_m)
        textbox_alte_marc.bind("<FocusOut>", lambda event, w=textbox_alte_marc, v=alte_marc_var: _update_var_from_text(w, v))
    r_fix += 1
    # Linia 11
    ctk.CTkLabel(frame_fixare, text="Calitatea marcajelor:").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_cal_marc = ctk.CTkComboBox(frame_fixare, width=130, state="readonly",
                                     variable=app_instance.data_vars[VAR_PREFIX + 'calitate_marcaje'],
                                     values=['vizibile', 'parțial vizibile', 'nu există'], button_color=None)
    combo_cal_marc.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_cal_marc.set('vizibile')
    combo_linii_tramvai = ctk.CTkComboBox(frame_fixare, width=100, state="readonly",
                                          variable=app_instance.data_vars[VAR_PREFIX + 'linii_tramvai'],
                                          values=['Există', 'Nu există'], button_color=None)
    combo_linii_tramvai.grid(row=r_fix, column=2, padx=(10,2), pady=2, sticky="w")
    combo_linii_tramvai.set('Nu există')
    ctk.CTkLabel(frame_fixare, text="linii de tramvai").grid(row=r_fix, column=3, padx=2, pady=2, sticky="w")
    r_fix += 1
    # Linia 12
    ctk.CTkLabel(frame_fixare, text="Drumul").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_ex_trot = ctk.CTkComboBox(frame_fixare, width=90, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'exista_trotuare'],
                                    values=['este', 'nu este'], button_color=None)
    combo_ex_trot.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_ex_trot.set('este')
    ctk.CTkLabel(frame_fixare, text="prevăzut cu trotuare, având o lățime de").grid(row=r_fix, column=2, padx=(10,2), pady=2, sticky="w")
    entry_lat_trot = ctk.CTkEntry(frame_fixare, width=70, textvariable=app_instance.data_vars[VAR_PREFIX + 'latime_trotuar'])
    entry_lat_trot.grid(row=r_fix, column=3, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_fixare, text="metri.").grid(row=r_fix, column=4, padx=(0,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 13
    combo_ex_spv = ctk.CTkComboBox(frame_fixare, width=100, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'exista_spatii_verzi'],
                                   values=['Există', 'Nu există'], button_color=None)
    combo_ex_spv.grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_ex_spv.set('Nu există')
    ctk.CTkLabel(frame_fixare, text="vegetație/ spații verzi, având o lățime de").grid(row=r_fix, column=1, columnspan=2, padx=(5,2), pady=2, sticky="w")
    entry_lat_spv = ctk.CTkEntry(frame_fixare, width=70, textvariable=app_instance.data_vars[VAR_PREFIX + 'latime_spv'])
    entry_lat_spv.grid(row=r_fix, column=3, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_fixare, text="metri.").grid(row=r_fix, column=4, padx=(0,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 14
    ctk.CTkLabel(frame_fixare, text="Semafoare auto").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_sem_auto = ctk.CTkComboBox(frame_fixare, width=120, state="readonly",
                                     variable=app_instance.data_vars[VAR_PREFIX + 'semafoare_auto'],
                                     values=['Funcționale', 'Nefuncționale', 'Nu există'], button_color=None)
    combo_sem_auto.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_sem_auto.set('Nu există')
    ctk.CTkLabel(frame_fixare, text="Semafoare pietonale").grid(row=r_fix, column=2, padx=(10,2), pady=2, sticky="w")
    combo_sem_piet = ctk.CTkComboBox(frame_fixare, width=120, state="readonly",
                                     variable=app_instance.data_vars[VAR_PREFIX + 'semafoare_pietonale'],
                                     values=['Funcționale', 'Nefuncționale', 'Nu există'], button_color=None)
    combo_sem_piet.grid(row=r_fix, column=3, columnspan=2, padx=(2,5), pady=2, sticky="w")
    combo_sem_piet.set('Nu există')
    r_fix += 1
    # Linia 15 - Indicatoare
    ctk.CTkLabel(frame_fixare, text="Indicatoare pentru reglementarea circulației rutiere și calitatea acestora:").grid(row=r_fix, column=0, columnspan=5, padx=(5,5), pady=5, sticky="w")
    r_fix += 1
    # Linia 16 - Text Indicatoare
    textbox_ind = ctk.CTkTextbox(frame_fixare, height=40, wrap=tk.WORD) # CTkTextbox
    textbox_ind.grid(row=r_fix, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
    textbox_ind.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ind_var = app_instance.data_vars[VAR_PREFIX + 'text_indicatoare']
    if ind_var:
        init_ind = ind_var.get()
        if init_ind: textbox_ind.insert("1.0", init_ind)
        textbox_ind.bind("<FocusOut>", lambda event, w=textbox_ind, v=ind_var: _update_var_from_text(w, v))
    r_fix += 1
    # Linia 17
    ctk.CTkLabel(frame_fixare, text="În zona producerii accidentului").grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_id_vit = ctk.CTkComboBox(frame_fixare, width=100, state="readonly",
                                   variable=app_instance.data_vars[VAR_PREFIX + 'identificare_viteza'],
                                   values=['au fost', 'n-au fost'], button_color=None)
    combo_id_vit.grid(row=r_fix, column=1, padx=2, pady=2, sticky="w")
    combo_id_vit.set('n-au fost')
    ctk.CTkLabel(frame_fixare, text="identificate indicatoare de limitare de viteză la").grid(row=r_fix, column=2, columnspan=2, padx=(10,2), pady=2, sticky="w")
    r_fix += 1
    # Linia 18
    combo_lim_vit = ctk.CTkComboBox(frame_fixare, width=70,
                                    variable=app_instance.data_vars[VAR_PREFIX + 'limita_viteza'],
                                    values=['50', '30', '........', ''], button_color=None)
    combo_lim_vit.grid(row=r_fix, column=0, padx=(5,2), pady=2, sticky="w")
    combo_lim_vit.set('........')
    ctk.CTkLabel(frame_fixare, text="Km/h, amplasate astfel:").grid(row=r_fix, column=1, columnspan=4, padx=(5,5), pady=2, sticky="w")
    r_fix += 1
    # Linia 19 - Text Limitare Viteza
    textbox_lim_vit = ctk.CTkTextbox(frame_fixare, height=40, wrap=tk.WORD) # CTkTextbox
    textbox_lim_vit.grid(row=r_fix, column=0, columnspan=5, padx=5, pady=(2,5), sticky="ew")
    textbox_lim_vit.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    lim_vit_var = app_instance.data_vars[VAR_PREFIX + 'text_limitare_viteza']
    if lim_vit_var:
        init_lim_v = lim_vit_var.get()
        if init_lim_v: textbox_lim_vit.insert("1.0", init_lim_v)
        textbox_lim_vit.bind("<FocusOut>", lambda event, w=textbox_lim_vit, v=lim_vit_var: _update_var_from_text(w, v))
    r_fix += 1
    current_row_s2 +=1


    # Frame Locul producerii accidentului
    frame_loc_prod = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_loc_prod.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_loc_prod.columnconfigure(2, weight=1)
    ctk.CTkLabel(frame_loc_prod, text="Locul producerii accidentului", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5,10), padx=10, sticky="ew")
    current_row_s2 += 1
    r_lp = 1
    ctk.CTkLabel(frame_loc_prod, text="Locul producerii accidentului a fost").grid(row=r_lp, column=0, padx=(5,2), pady=2, sticky="w")
    combo_loc_ind = ctk.CTkComboBox(frame_loc_prod, width=90, state="readonly",
                                    variable=app_instance.data_vars[VAR_PREFIX + 'locul_indicat'],
                                    values=['indicat', 'afirmat'], button_color=None)
    combo_loc_ind.grid(row=r_lp, column=1, padx=2, pady=2, sticky="w")
    combo_loc_ind.set('indicat')
    ctk.CTkLabel(frame_loc_prod, text="de către:").grid(row=r_lp, column=2, padx=(10,5), pady=2, sticky="w")
    r_lp += 1
    textbox_loc_ind = ctk.CTkTextbox(frame_loc_prod, height=100, wrap=tk.WORD) # CTkTextbox
    textbox_loc_ind.grid(row=r_lp, column=0, columnspan=3, padx=5, pady=(2,5), sticky="ew")
    textbox_loc_ind.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    loc_ind_var = app_instance.data_vars[VAR_PREFIX + 'text_locul_indicat']
    if loc_ind_var:
        init_loc_i = loc_ind_var.get()
        if init_loc_i: textbox_loc_ind.insert("1.0", init_loc_i)
        textbox_loc_ind.bind("<FocusOut>", lambda event, w=textbox_loc_ind, v=loc_ind_var: _update_var_from_text(w,v))


    # Frame Alte particularități
    frame_alte_part = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_alte_part.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_alte_part.columnconfigure(0, weight=1)
    frame_alte_part.rowconfigure(1, weight=1)
    ctk.CTkLabel(frame_alte_part, text="Alte particularități ale locului faptei:", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=10, sticky="ew")
    current_row_s2 += 1
    textbox_alte_part = ctk.CTkTextbox(frame_alte_part, height=100, wrap=tk.WORD) # CTkTextbox
    textbox_alte_part.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
    textbox_alte_part.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    alte_part_var = app_instance.data_vars[VAR_PREFIX + 'text_alte_particularitati']
    if alte_part_var:
        init_alte_p = alte_part_var.get()
        if init_alte_p: textbox_alte_part.insert("1.0", init_alte_p)
        textbox_alte_part.bind("<FocusOut>", lambda event, w=textbox_alte_part, v=alte_part_var: _update_var_from_text(w,v))


    # Frame Urme descoperite
    frame_urme = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_urme.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_urme.columnconfigure(0, weight=1)
    frame_urme.rowconfigure(1, weight=1)
    ctk.CTkLabel(frame_urme, text="Urme descoperite la fața locului:", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=10, sticky="ew")
    current_row_s2 += 1
    textbox_urme = ctk.CTkTextbox(frame_urme, height=100, wrap=tk.WORD) # CTkTextbox
    textbox_urme.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
    textbox_urme.insert('1.0', 'La locul săvârșirii faptei nu au fost descoperite urme și mijloace materiale de probă.')
    textbox_urme.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    urme_var = app_instance.data_vars[VAR_PREFIX + 'text_urme_cfl']
    if urme_var:
        init_urme = urme_var.get()
        if init_urme and init_urme != 'La locul săvârșirii faptei nu au fost descoperite urme și mijloace materiale de probă.':
            textbox_urme.delete("1.0", "end")
            textbox_urme.insert("1.0", init_urme)
        textbox_urme.bind("<FocusOut>", lambda event, w=textbox_urme, v=urme_var: _update_var_from_text(w,v))


    # Frame Locul ridicare victimă
    frame_loc_vict = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_loc_vict.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_loc_vict.columnconfigure(2, weight=1)
    ctk.CTkLabel(frame_loc_vict, text="Locul de unde a fost ridicată victima", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5,10), padx=10, sticky="ew")
    current_row_s2 += 1
    r_lv = 1
    ctk.CTkLabel(frame_loc_vict, text="Locul de unde a fost ridicată victima a fost").grid(row=r_lv, column=0, padx=(5,2), pady=2, sticky="w")
    combo_loc_ind_v = ctk.CTkComboBox(frame_loc_vict, width=90, state="readonly",
                                      variable=app_instance.data_vars[VAR_PREFIX + 'locul_indicat_victima'],
                                      values=['indicat', 'afirmat'], button_color=None)
    combo_loc_ind_v.grid(row=r_lv, column=1, padx=2, pady=2, sticky="w")
    combo_loc_ind_v.set('indicat')
    ctk.CTkLabel(frame_loc_vict, text="de către:").grid(row=r_lv, column=2, padx=(10,5), pady=2, sticky="w")
    r_lv += 1
    textbox_loc_rid_vict = ctk.CTkTextbox(frame_loc_vict, height=100, wrap=tk.WORD) # CTkTextbox
    textbox_loc_rid_vict.grid(row=r_lv, column=0, columnspan=3, padx=5, pady=(2,5), sticky="ew")
    textbox_loc_rid_vict.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    loc_rid_v_var = app_instance.data_vars[VAR_PREFIX + 'text_locul_ridicat_victima']
    if loc_rid_v_var:
        init_loc_rv = loc_rid_v_var.get()
        if init_loc_rv: textbox_loc_rid_vict.insert("1.0", init_loc_rv)
        textbox_loc_rid_vict.bind("<FocusOut>", lambda event, w=textbox_loc_rid_vict, v=loc_rid_v_var: _update_var_from_text(w,v))


    # Frame Camere Video
    frame_camere = ctk.CTkFrame(content_frame2, border_width=1, corner_radius=10)
    frame_camere.grid(row=current_row_s2, column=0, padx=5, pady=5, sticky="ew")
    frame_camere.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_camere, text="Camere Video", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5,10), padx=10, sticky="ew")
    current_row_s2 += 1
    r_cam = 1
    ctk.CTkLabel(frame_camere, text="În urma verificărilor efectuate, în zona producerii accidentului").grid(row=r_cam, column=0, padx=(5,2), pady=2, sticky="w")
    combo_aufost_cam = ctk.CTkComboBox(frame_camere, width=110, state="readonly",
                                       variable=app_instance.data_vars[VAR_PREFIX + 'aufost_camere'],
                                       values=['au fost', 'nu au fost'], button_color=None)
    combo_aufost_cam.grid(row=r_cam, column=1, padx=2, pady=2, sticky="w")
    combo_aufost_cam.set('nu au fost')
    ctk.CTkLabel(frame_camere, text="identificate").grid(row=r_cam, column=2, padx=(5,5), pady=2, sticky="w")
    r_cam += 1
    ctk.CTkLabel(frame_camere, text="camere de supraveghere video după cum urmează:").grid(row=r_cam, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    r_cam += 1
    textbox_cam = ctk.CTkTextbox(frame_camere, height=100, wrap=tk.WORD) # CTkTextbox
    textbox_cam.grid(row=r_cam, column=0, columnspan=3, padx=5, pady=(2,5), sticky="ew")
    textbox_cam.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    cam_var = app_instance.data_vars[VAR_PREFIX + 'text_camere']
    if cam_var:
        init_cam = cam_var.get()
        if init_cam: textbox_cam.insert("1.0", init_cam)
        textbox_cam.bind("<FocusOut>", lambda event, w=textbox_cam, v=cam_var: _update_var_from_text(w,v))


# --- Funcții get/load data (rămân la fel) ---
def get_data(app_instance):
    """Colectează datele din variabilele Tkinter pentru acest tab (Versiune CTk)."""
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din tab CFL (CTk)...")
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

def load_data(app_instance, data_to_load):
    """Încarcă datele primite în variabilele Tkinter pentru acest tab (Versiune CTk)."""
    data_vars = app_instance.data_vars
    print("Încărcare date în tab CFL (CTk)...")
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
            except tk.TclError as e:
                 print(f"Avertisment: Nu s-a putut seta valoarea pentru {full_key}: {e}", file=sys.stderr)
            except Exception as e:
                 print(f"Eroare la încărcarea datei pentru {full_key}: {e}", file=sys.stderr)

