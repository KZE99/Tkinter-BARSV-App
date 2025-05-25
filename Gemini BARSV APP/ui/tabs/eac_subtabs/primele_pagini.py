# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Primele 2 Pagini' din EAC.
(Versiune refăcută pentru CustomTkinter, cu variable tracing și corecție creare variabilă)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

# Asigură-te că utils există și e corect
try:
    from core import utils
except ImportError:
    print("AVERTISMENT: Nu s-a putut importa core.utils în primele_pagini (CTk).")
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()

# Prefix specific pentru variabilele acestui sub-tab
SUB_VAR_PREFIX = "eac_pp_"

# Cheile pentru variabilele de *afișare* create în acest modul
DISPLAY_DATA_KEYS = [
    "display_nr_penal", "display_data_ora_cfl", "display_nume_agent1",
    "display_insigna_agent1", "display_numar_vehicule", "display_nr_raniti_grav",
    "display_nr_raniti_usor", "display_autor_necunoscut", "display_data_ora_acc",
    "display_sector", "display_lat_nord", "display_lat_est",
    "display_locul_accidentului",
]

# Cheile pentru variabilele *controlate direct* în acest tab
CONTROL_DATA_KEYS = [
    "ora_ambulanta_eac",
    "in_localitate", # Cheie pentru Radio group
    "nr_benzi_sens", "reper_fix", "distanta_reper",
    "cat_drum", "marcaj_drum", "sens_drum", "sens_unic",
    "checkbox1_restrictii", "checkbox2_restrictii", "checkbox3_restrictii", "checkbox4_restrictii",
    "checkbox5_restrictii", "checkbox6_restrictii", "checkbox7_restrictii", "checkbox8_restrictii",
    "checkbox9_restrictii", "checkbox10_restrictii", "checkbox11_restrictii", "checkbox12_restrictii",
    "checkbox13_restrictii", "checkbox14_restrictii", "checkbox15_restrictii", "checkbox16_restrictii",
    "checkbox17_restrictii", "checkbox18_restrictii", "checkbox19_restrictii", "checkbox20_restrictii",
    "checkbox21_restrictii", "checkbox22_restrictii", "checkbox23_restrictii", "checkbox24_restrictii",
    "checkbox25_restrictii", "checkbox26_restrictii",
    "mij_semnalizare", "car_drum", "config_caract", "compozitie_dr", "meteo",
    "cond_lumina", "aderenta", "stare_supraf", "latime_banda", "acostament",
    "categ_banda", "inclinatie",
    "checkbox1_mijl_sig", "checkbox2_mijl_sig", "checkbox3_mijl_sig", "checkbox4_mijl_sig",
    "checkbox5_mijl_sig", "checkbox6_mijl_sig", "checkbox7_mijl_sig", "checkbox8_mijl_sig",
    "checkbox9_mijl_sig",
    "checkbox1_cp_abateri_cp", "checkbox1_cp_abateri_cs", "checkbox2_cp_abateri_cp", "checkbox2_cp_abateri_cs",
    "checkbox3_cp_abateri_cp", "checkbox3_cp_abateri_cs", "checkbox4_cp_abateri_cp", "checkbox4_cp_abateri_cs",
    "checkbox5_cp_abateri_cp", "checkbox5_cp_abateri_cs", "checkbox6_cp_abateri_cp", "checkbox6_cp_abateri_cs",
    "checkbox7_cp_abateri_cp", "checkbox7_cp_abateri_cs", "checkbox8_cp_abateri_cp", "checkbox8_cp_abateri_cs",
    "checkbox9_cp_abateri_cp", "checkbox9_cp_abateri_cs", "checkbox10_cp_abateri_cp", "checkbox10_cp_abateri_cs",
    "checkbox11_cp_abateri_cp", "checkbox11_cp_abateri_cs", "checkbox12_cp_abateri_cp", "checkbox12_cp_abateri_cs",
    "checkbox13_cp_abateri_cp", "checkbox13_cp_abateri_cs", "checkbox14_cp_abateri_cp", "checkbox14_cp_abateri_cs",
    "checkbox15_cp_abateri_cp", "checkbox15_cp_abateri_cs", "checkbox16_cp_abateri_cp", "checkbox16_cp_abateri_cs",
    "checkbox17_cp_abateri_cp", "checkbox17_cp_abateri_cs", "checkbox18_cp_abateri_cp", "checkbox18_cp_abateri_cs",
    "checkbox19_cp_abateri_cp", "checkbox19_cp_abateri_cs", "checkbox20_cp_abateri_cp", "checkbox20_cp_abateri_cs",
    "checkbox21_cp_abateri_cp", "checkbox21_cp_abateri_cs", "checkbox22_cp_abateri_cp", "checkbox22_cp_abateri_cs",
    "checkbox23_cp_abateri_cp", "checkbox23_cp_abateri_cs", "checkbox24_cp_abateri_cp", "checkbox24_cp_abateri_cs",
    "checkbox25_cp_abateri_cp", "checkbox25_cp_abateri_cs", "checkbox26_cp_abateri_cp", "checkbox26_cp_abateri_cs",
    "checkbox27_cp_abateri_cp", "checkbox27_cp_abateri_cs", "checkbox28_cp_abateri_cp", "checkbox28_cp_abateri_cs",
    "checkbox29_cp_abateri_cp", "checkbox29_cp_abateri_cs", "checkbox30_cp_abateri_cp", "checkbox30_cp_abateri_cs",
    "checkbox31_cp_abateri_cp", "checkbox31_cp_abateri_cs", "checkbox32_cp_abateri_cp", "checkbox32_cp_abateri_cs",
    "checkbox33_cp_abateri_cp", "checkbox33_cp_abateri_cs", "checkbox34_cp_abateri_cp", "checkbox34_cp_abateri_cs",
    "checkbox35_cp_abateri_cp", "checkbox35_cp_abateri_cs", "checkbox36_cp_abateri_cp", "checkbox36_cp_abateri_cs",
    "checkbox37_cp_abateri_cp", "checkbox37_cp_abateri_cs", "checkbox38_cp_abateri_cp", "checkbox38_cp_abateri_cs",
    "checkbox39_cp_abateri_cp", "checkbox39_cp_abateri_cs", "checkbox40_cp_abateri_cp", "checkbox40_cp_abateri_cs",
    "checkbox41_cp_abateri_cp", "checkbox41_cp_abateri_cs",
    "mod_producere",
]
ALL_SUB_TAB_KEYS = DISPLAY_DATA_KEYS + CONTROL_DATA_KEYS

RADIO_OPTIONS = {
    "in_localitate": ["DA", "NU"],
    "cat_drum": ["autostradă", "drum naţional", "drum judeţean", "drum comunal", "stradă", "alte drumuri"],
    "marcaj_drum": ["inexistent", "numai pe margine", "separare benzi", "separare benzi şi margine"],
    "sens_drum": ["ascendent", "descendent"],
    "sens_unic": ["DA", "NU"],
    "mij_semnalizare": ["barieră - operator uman (trecere CF)", "barieră automată (trecere CF)", "cu semnalizare (curbă)", "fără barieră (trecere CF)", "fără semnalizare (curbă)", "indicatoare & marcaje (intersecţie)", "fără mijloace de semnalizare", "lucrări", "nedirijată (intersecţie)", "persoană autorizată (intersecţie)", "semafor (intersecţie)", "semnalizare automată (trecere CF)", "staţie mijloace transport în comun", "trecere CF industrială (trecere CF)", "trecere pentru pietoni", "altele"],
    "car_drum": ["curbă", "fără", "în tunel", "intersecţie", "pe pod", "sub pod", "trecere cale ferată"],
    "config_caract": ["cale ferată", "curbă L (90 grade)", "curbă U (180 grade)", "dublu T", "fără", "sens giratoriu", "în cruce (intersecţie)", "în stea (intersecţie)", "în Y (intersecţie)", "în T (intersecţie)", "succesiune de curbe (S)", "altele"],
    "compozitie_dr": ["asfalt", "beton", "pământ", "piatră", "piatră cubică"],
    "meteo": ["ceaţă", "lapoviţă", "ninsoare", "normal", "ploaie", "vânt puternic", "viscol"],
    "cond_lumina": ["cer înnourat", "fără iluminat stradal", "fum (praf)", "i. stradal în funcţiune", "i. stradal nefuncţional", "i. stradal oprit", "în amurg", "în zori", "la lumina zilei", "soare orbitor"],
    "aderenta": ["altele", "alunecos", "gheaţă", "inundaţii", "mâzgă", "polei", "umed", "uscat", "zăpadă"],
    "stare_supraf": ["denivelări generalizate", "denivelări rare", "gropi", "şanţuri", "netedă"],
    "latime_banda": ["< 2.75m", "2.75m-3.25m", "3.25m-3.75m", "> 3.75m"],
    "acostament": ["consolidat", "neconsolidat", "fără acostament"],
    "categ_banda": ["normală", "reversibilă", "rezervată", "suplimentară", "urgenţă"],
    "inclinatie": ["drept", "pantă", "rampă", "vârf de rampă", "în şa"],
    "mod_producere": ["acroşare", "acvaplanare", "altele", "cădere din vehicul", "cădere în vehicul", "cădere în afara drumului", "coliziune faţă-spate", "coliziune frontală", "coliziune în lanţ", "coliziune laterală", "coliziune urmată de incendiu", "coliziune urmată de răsturnare", "coliziune cu vehicul în staţionare", "derapare", "lovire animal", "lovire obstacol în afara părţii carosabile", "lovire obstacol pe carosabil", "lovire pieton", "părăsire vehicul (participant)", "răsturnare"],
    "autor_necunoscut_an": ["DA", "NU"],
}
RESTRICTII_TEXTS = {
    "checkbox1_restrictii": "acces interzis autobuzelor", "checkbox2_restrictii": "acces interzis autovehiculelor",
    "checkbox3_restrictii": "acces interzis AV & V cu tracțiune animală", "checkbox4_restrictii": "acces interzis bicicliștilor",
    "checkbox5_restrictii": "acces interzis motocicletelor", "checkbox6_restrictii": "acces interzis pietonilor",
    "checkbox7_restrictii": "acces interzis vehiculelor cu tracțiune animală", "checkbox8_restrictii": "acces interzis vehiculelor",
    "checkbox9_restrictii": "acces limitat in funcţie de masă", "checkbox10_restrictii": "cedează trecerea",
    "checkbox11_restrictii": "circulaţie interzisă în ambele sensuri", "checkbox12_restrictii": "depăşire interzisă",
    "checkbox13_restrictii": "distanţă minimă obligatorie", "checkbox14_restrictii": "întoarcere interzisă",
    "checkbox15_restrictii": "limită gabarit în înalţime", "checkbox16_restrictii": "limită gabarit în lăţime",
    "checkbox17_restrictii": "limită gabarit în lungime", "checkbox18_restrictii": "limitare de viteză",
    "checkbox19_restrictii": "nerestricţionat", "checkbox20_restrictii": "oprire obligatorie (STOP)",
    "checkbox21_restrictii": "oprire interzisă", "checkbox22_restrictii": "prioritate sens contrasens",
    "checkbox23_restrictii": "staţionare interzisă", "checkbox24_restrictii": "virajul la dreapta interzis",
    "checkbox25_restrictii": "virajul la stânga interzis", "checkbox26_restrictii": "viteză minimă obligatorie"
}
MIJL_SIG_TEXTS = {
    "checkbox1_mijl_sig": "bariere de siguranţă", "checkbox2_mijl_sig": "butoni r. semi-îngropaţi",
    "checkbox3_mijl_sig": "glisiere", "checkbox4_mijl_sig": "parapeţi", "checkbox5_mijl_sig": "spaţiu de separare",
    "checkbox6_mijl_sig": "spaţiu verde", "checkbox7_mijl_sig": "stâlpi de separare",
    "checkbox8_mijl_sig": "stâlpi reflectorizanţi", "checkbox9_mijl_sig": "inexistent"
}
CAUZE_TEXTS = {
    "checkbox1_cp_abateri": "adormire la volan", "checkbox2_cp_abateri": "alte abateri săvârşite de conducătorii auto",
    "checkbox3_cp_abateri": "alte preocupări de natură a distrage atenţia", "checkbox4_cp_abateri": "circulaţie pe sensul opus",
    "checkbox5_cp_abateri": "conducere fără permis", "checkbox6_cp_abateri": "conducere sub influenţa alcoolului",
    "checkbox7_cp_abateri": "conducere sub influenţa drogurilor", "checkbox8_cp_abateri": "depăşire neregulamentară",
    "checkbox9_cp_abateri": "folosire incorectă, lumini & mijloace semnalizare", "checkbox10_cp_abateri": "întoarcere neregulamentară",
    "checkbox11_cp_abateri": "neacordare de prioritate pietonilor", "checkbox12_cp_abateri": "neacordare de prioritate vehiculelor",
    "checkbox13_cp_abateri": "neasigurare schimbare bandă", "checkbox14_cp_abateri": "neasigurare schimbarea direcţiei de mers",
    "checkbox15_cp_abateri": "nerespectare distanţă între vehicule", "checkbox16_cp_abateri": "nerespectare indic.rutiere de obligare sau reglement.",
    "checkbox17_cp_abateri": "nerespectare reguli mers înapoi", "checkbox18_cp_abateri": "nerespectare reguli trecere la nivel cu calea ferată",
    "checkbox19_cp_abateri": "nerespectare semnificaţie culoare semafor", "checkbox20_cp_abateri": "oprire, staţionare neregulamentară",
    "checkbox21_cp_abateri": "viteză neadaptată la condiţiile de drum", "checkbox22_cp_abateri": "viteză neregulamentară",
    "checkbox23_cp_abateri": "abateri ale cond. de atelaje sau animale", "checkbox24_cp_abateri": "abateri ale conducătorilor de utilaje",
    "checkbox25_cp_abateri": "abateri biciclişti", "checkbox26_cp_abateri": "defecţiuni tehnice vehicul",
    "checkbox27_cp_abateri": "parbriz, lunetă, oglinzi lipsă sau inutilizabile", "checkbox28_cp_abateri": "alte cauze referitoare la drum",
    "checkbox29_cp_abateri": "drum deteriorat sau în lucru", "checkbox30_cp_abateri": "lipsă dispozitive pentru siguranţa circulaţiei",
    "checkbox31_cp_abateri": "obstacol nesemnalizat pe carosabil", "checkbox32_cp_abateri": "semnalizare rutieră incompletă / insuficientă",
    "checkbox33_cp_abateri": "vizibilitate redusă datorită terenului", "checkbox34_cp_abateri": "rugozitate scăzută",
    "checkbox35_cp_abateri": "abateri pasageri/călători/însoţitori", "checkbox36_cp_abateri": "animale sau alte obiecte",
    "checkbox37_cp_abateri": "cauze medicale", "checkbox38_cp_abateri": "depăşire încărcatură",
    "checkbox39_cp_abateri": "alte abateri pietoni", "checkbox40_cp_abateri": "pietoni pe partea carosabilă",
    "checkbox41_cp_abateri": "traversare neregulamentară pietoni"
}

# --- Funcții Helper Text <-> StringVar ---
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

def create_sub_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru sub-tab-ul 'Primele 2 Pagini'.
    """
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_columnconfigure(0, weight=1)

    scroll_area = ctk.CTkScrollableFrame(parent_container, label_text="")
    scroll_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    content_frame = scroll_area
    content_frame.columnconfigure(0, weight=1)

    # --- Definire Variabile Tkinter ---
    for key in ALL_SUB_TAB_KEYS:
        full_key = SUB_VAR_PREFIX + key
        if full_key not in app_instance.data_vars:
            is_cp_cs = "_cp" in key or "_cs" in key
            is_checkbox = key.startswith("checkbox") or is_cp_cs

            # --- **CORECTIE LOGICĂ CREARE VARIABILĂ** ---
            # Verificăm explicit dacă cheia e pentru un grup radio
            is_radio_key = key in RADIO_OPTIONS or key == "autor_necunoscut_an"

            if is_radio_key:
                app_instance.data_vars[full_key] = tk.StringVar(value="") # Corect: StringVar pentru Radio
            elif is_checkbox:
                 app_instance.data_vars[full_key] = tk.IntVar(value=0) # Corect: IntVar pentru Checkbox
            else: # Include display_ și alte chei (Entry, Textbox)
                 app_instance.data_vars[full_key] = tk.StringVar() # Corect: StringVar pentru restul
            # --- **SFÂRȘIT CORECȚIE** ---

    # --- Funcții Callback și Tracing (rămân la fel) ---
    def _update_display_var(source_var_key, target_var_key, default="N/A"):
        source_var = app_instance.data_vars.get(source_var_key)
        target_var = app_instance.data_vars.get(target_var_key)
        if source_var and target_var:
            value = source_var.get()
            target_var.set(str(value) if value else default)
    def _update_data_ora_cfl(*args):
        zi = app_instance.data_vars.get("principal_ziua_doc", tk.StringVar(value="??")).get()
        luna = app_instance.data_vars.get("principal_luna_doc", tk.StringVar(value="??")).get()
        an = app_instance.data_vars.get("principal_anul_doc", tk.StringVar(value="????")).get()
        ora_d = app_instance.data_vars.get("principal_cfl_dela", tk.StringVar(value="??:??")).get()
        ora_p = app_instance.data_vars.get("principal_cfl_panala", tk.StringVar(value="??:??")).get()
        target_var = app_instance.data_vars.get(SUB_VAR_PREFIX + "display_data_ora_cfl")
        if target_var: target_var.set(f"{zi}.{luna}.{an} / {ora_d}-{ora_p}")
    def _update_data_ora_acc(*args):
        zi = app_instance.data_vars.get("principal_ziua_acc", tk.StringVar(value="??")).get()
        luna = app_instance.data_vars.get("principal_luna_acc", tk.StringVar(value="??")).get()
        an = app_instance.data_vars.get("principal_anul_acc", tk.StringVar(value="????")).get()
        ora = app_instance.data_vars.get("principal_ora_accident", tk.StringVar(value="??:??")).get()
        target_var = app_instance.data_vars.get(SUB_VAR_PREFIX + "display_data_ora_acc")
        if target_var: target_var.set(f"{zi}.{luna}.{an} Ora: {ora}")
    source_target_map = {
        "principal_nr_penal": SUB_VAR_PREFIX + "display_nr_penal",
        "principal_nume_agent1": SUB_VAR_PREFIX + "display_nume_agent1",
        "principal_insigna_agent1": SUB_VAR_PREFIX + "display_insigna_agent1",
        "principal_numar_vehicule": SUB_VAR_PREFIX + "display_numar_vehicule",
        "principal_nr_raniti_grav": SUB_VAR_PREFIX + "display_nr_raniti_grav",
        "principal_nr_raniti_usor": SUB_VAR_PREFIX + "display_nr_raniti_usor",
        "principal_autor_necunoscut": SUB_VAR_PREFIX + "display_autor_necunoscut",
        "principal_sector": SUB_VAR_PREFIX + "display_sector",
        "principal_lat_nord": SUB_VAR_PREFIX + "display_lat_nord",
        "principal_lat_est": SUB_VAR_PREFIX + "display_lat_est",
        "principal_locul_accidentului": SUB_VAR_PREFIX + "display_locul_accidentului",
    }
    for source_key, target_key in source_target_map.items():
        source_var = app_instance.data_vars.get(source_key)
        if source_var:
            source_var.trace_add("write", lambda *args, sk=source_key, tk=target_key: _update_display_var(sk, tk))
            _update_display_var(source_key, target_key)
    date_cfl_sources = ["principal_ziua_doc", "principal_luna_doc", "principal_anul_doc", "principal_cfl_dela", "principal_cfl_panala"]
    for src_key in date_cfl_sources:
        src_var = app_instance.data_vars.get(src_key)
        if src_var: src_var.trace_add("write", _update_data_ora_cfl)
    _update_data_ora_cfl()
    date_acc_sources = ["principal_ziua_acc", "principal_luna_acc", "principal_anul_acc", "principal_ora_accident"]
    for src_key in date_acc_sources:
        src_var = app_instance.data_vars.get(src_key)
        if src_var: src_var.trace_add("write", _update_data_ora_acc)
    _update_data_ora_acc()

    # --- Funcții helper pentru UI (rămân la fel) ---
    def create_radio_group(parent, label_text, key_base, options):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=(5,2))
        var = app_instance.data_vars.get(SUB_VAR_PREFIX + key_base)
        if var:
            for option in options:
                rb = ctk.CTkRadioButton(frame, text=option, value=option, variable=var)
                rb.pack(anchor="w", padx=15, pady=1)
        else:
            print(f"AVERTISMENT: Variabila lipsă pentru grupul radio: {SUB_VAR_PREFIX + key_base}")
        return frame

    def create_checkbox_group(parent, label_text, keys_dict):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=(5,2))
        for key, text in keys_dict.items():
             var = app_instance.data_vars.get(SUB_VAR_PREFIX + key)
             if var:
                 chk = ctk.CTkCheckBox(frame, text=text, variable=var, onvalue=1, offvalue=0)
                 chk.pack(anchor="w", padx=15, pady=1)
             else:
                  print(f"AVERTISMENT: Variabila lipsă pentru checkbox: {SUB_VAR_PREFIX + key}")
        return frame

    # --- Populare UI (cu corecție la 'În localitate') ---
    current_row = 0
    # == Secțiunea Constatator / Consecințe ==
    frame_constatator = ctk.CTkFrame(content_frame, border_width=1, corner_radius=10)
    frame_constatator.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    # ... (populare frame_constatator ca înainte) ...
    ctk.CTkLabel(frame_constatator, text="Constatator", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, pady=5, padx=10, sticky="w")
    ctk.CTkLabel(frame_constatator, text="TELEX", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, pady=5, padx=10, sticky="w")
    ctk.CTkLabel(frame_constatator, text="Consecințe", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, pady=5, padx=10, sticky="w")
    const_col = 0; r=1
    ctk.CTkLabel(frame_constatator, text="I.P.J. (DGPMB):", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="BR – SAR – BARSV", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="P.V. C.F.L. numărul:*", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nr_penal", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="P.V. C.F.L. data și ora:", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_data_ora_cfl", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Agent Constatator\n(grad, nume, prenume):", justify="left", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nume_agent1", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Insigna:", anchor="w").grid(row=r, column=const_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_insigna_agent1", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=const_col, padx=10, pady=(1,5), sticky="w")
    telex_col = 1; r=1
    ctk.CTkLabel(frame_constatator, text="Nr. Telex:").grid(row=r, column=telex_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get("principal_nr_telex", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=telex_col, padx=10, pady=1, sticky="w")
    cons_col = 2; r=1
    ctk.CTkLabel(frame_constatator, text="Număr vehicule:").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_numar_vehicule", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Număr morți:").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="0", anchor="w").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Număr răniți grav:").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nr_raniti_grav", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Număr răniți ușor:").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_nr_raniti_usor", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, text="Autor necunoscut:").grid(row=r, column=cons_col, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_constatator, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_autor_necunoscut", tk.StringVar(value="N/A")), anchor="w").grid(row=r, column=cons_col, padx=10, pady=(1,5), sticky="w")

    current_row += 1

    # == Secțiunea Data și Locul ==
    frame_data_loc = ctk.CTkFrame(content_frame, border_width=1, corner_radius=10)
    frame_data_loc.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_data_loc.grid_columnconfigure(0, weight=1)
    frame_data_loc.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_data_loc, text="Data şi locul accidentului", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=4, pady=(5, 10), padx=10, sticky="ew")
    current_row += 1
    # ... (populare frame_data_loc ca înainte) ...
    # Coloana Stânga
    r=1
    ctk.CTkLabel(frame_data_loc, text="Dată, oră, zi săptamână:").grid(row=r, column=0, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_data_ora_acc", tk.StringVar(value="N/A"))).grid(row=r, column=0, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, text="Judeţ/ Sector:").grid(row=r, column=0, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_sector", tk.StringVar(value="N/A"))).grid(row=r, column=0, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, text="Pe raza localităţii:").grid(row=r, column=0, padx=10, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, text="BUCUREȘTI").grid(row=r, column=0, padx=10, pady=(1,5), sticky="w")
    # Coloana Dreapta
    r=1
    ctk.CTkLabel(frame_data_loc, text="Ora prezentării ambulanței:").grid(row=r, column=2, padx=10, pady=1, sticky="w")
    ctk.CTkEntry(frame_data_loc, width=100, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "ora_ambulanta_eac")).grid(row=r, column=3, padx=5, pady=1, sticky="w"); r+=1 # Cheie nouă
    ctk.CTkLabel(frame_data_loc, text="În localitate:").grid(row=r, column=2, padx=10, pady=1, sticky="w")
    frame_in_loc = ctk.CTkFrame(frame_data_loc, fg_color="transparent")
    frame_in_loc.grid(row=r+1, column=2, columnspan=2, sticky="w", padx=5)
    # --- Folosim cheia corectă ---
    in_localitate_var = app_instance.data_vars.get(SUB_VAR_PREFIX + "in_localitate")
    if in_localitate_var:
        ctk.CTkRadioButton(frame_in_loc, text="DA", value="DA", variable=in_localitate_var).pack(side="left", padx=(0,5))
        ctk.CTkRadioButton(frame_in_loc, text="NU", value="NU", variable=in_localitate_var).pack(side="left")
        # Setăm default doar dacă variabila e goală (poate a fost încărcată din backup)
        if not in_localitate_var.get():
            in_localitate_var.set("DA")
    else:
        ctk.CTkLabel(frame_in_loc, text="Eroare var 'in_localitate'").pack()
    # --- Sfârșit corecție ---
    r+=2
    ctk.CTkLabel(frame_data_loc, text="Poziție GPS: Lat. N").grid(row=r, column=2, padx=10, pady=1, sticky="w")
    ctk.CTkLabel(frame_data_loc, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_lat_nord", tk.StringVar(value="N/A"))).grid(row=r, column=3, padx=5, pady=1, sticky="w"); r+=1
    ctk.CTkLabel(frame_data_loc, text="                Lat. E").grid(row=r, column=2, padx=10, pady=1, sticky="w")
    ctk.CTkLabel(frame_data_loc, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_lat_est", tk.StringVar(value="N/A"))).grid(row=r, column=3, padx=5, pady=(1,5), sticky="w")


    # ... (Restul secțiunilor UI ca înainte) ...
    # == Secțiunea Drum și Condiții ==
    frame_drum = ctk.CTkFrame(content_frame, border_width=1, corner_radius=10)
    frame_drum.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_drum.grid_columnconfigure(0, weight=1)
    frame_drum.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_drum, text="Drum şi condiţii", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 10), padx=10, sticky="ew")
    current_row += 1
    # ... (populare frame_drum ca înainte) ...
    drum_col1 = ctk.CTkFrame(frame_drum, fg_color="transparent")
    drum_col1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    r_drum1 = 0
    ctk.CTkLabel(drum_col1, text="Locul accidentului:").grid(row=r_drum1, column=0, sticky="w", pady=1); r_drum1+=1
    ctk.CTkLabel(drum_col1, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_locul_accidentului", tk.StringVar(value="N/A")), wraplength=300, justify="left").grid(row=r_drum1, column=0, sticky="w", pady=1); r_drum1+=1
    ctk.CTkLabel(drum_col1, text="Număr benzi (pe sens):").grid(row=r_drum1, column=0, sticky="w", pady=1)
    ctk.CTkEntry(drum_col1, width=50, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "nr_benzi_sens")).grid(row=r_drum1, column=1, sticky="w", pady=1); r_drum1+=1
    ctk.CTkLabel(drum_col1, text="Reper fix:").grid(row=r_drum1, column=0, sticky="w", pady=1)
    ctk.CTkEntry(drum_col1, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "reper_fix")).grid(row=r_drum1, column=1, sticky="ew", pady=1); r_drum1+=1
    ctk.CTkLabel(drum_col1, text="Distanță reper:").grid(row=r_drum1, column=0, sticky="w", pady=1)
    ctk.CTkEntry(drum_col1, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "distanta_reper")).grid(row=r_drum1, column=1, sticky="ew", pady=1); r_drum1+=1
    drum_col2 = ctk.CTkFrame(frame_drum, fg_color="transparent")
    drum_col2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    create_radio_group(drum_col2, "Categorie drum:", "cat_drum", RADIO_OPTIONS["cat_drum"]).pack(anchor="w")
    create_radio_group(drum_col2, "Marcaj drum:", "marcaj_drum", RADIO_OPTIONS["marcaj_drum"]).pack(anchor="w", pady=(10,0))
    create_radio_group(drum_col2, "Sens drum:", "sens_drum", RADIO_OPTIONS["sens_drum"]).pack(anchor="w", pady=(10,0))
    create_radio_group(drum_col2, "Sens unic:", "sens_unic", RADIO_OPTIONS["sens_unic"]).pack(anchor="w", pady=(10,0))

    # == Secțiunea Restricții ==
    frame_restrictii = ctk.CTkFrame(content_frame, border_width=1, corner_radius=10)
    frame_restrictii.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_restrictii.grid_columnconfigure(0, weight=1)
    frame_restrictii.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_restrictii, text="Restricții", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 5), padx=10, sticky="w")
    current_row += 1
    # ... (populare frame_restrictii ca înainte) ...
    restr_col_left = ctk.CTkFrame(frame_restrictii, fg_color="transparent")
    restr_col_left.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    restr_col_right = ctk.CTkFrame(frame_restrictii, fg_color="transparent")
    restr_col_right.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    restr_keys = list(RESTRICTII_TEXTS.keys())
    mid_point = len(restr_keys) // 2 + (len(restr_keys) % 2)
    for i, key in enumerate(restr_keys):
        parent_col = restr_col_left if i < mid_point else restr_col_right
        text = RESTRICTII_TEXTS[key]
        var = app_instance.data_vars.get(SUB_VAR_PREFIX + key)
        if var:
            chk = ctk.CTkCheckBox(parent_col, text=text, variable=var, onvalue=1, offvalue=0)
            chk.pack(anchor="w", padx=5, pady=1)

    # == Secțiunea Mijloace Semnalizare ==
    frame_semnalizare = create_radio_group(content_frame, "Mijloace de semnalizare:", "mij_semnalizare", RADIO_OPTIONS["mij_semnalizare"])
    frame_semnalizare.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    current_row += 1

    # == Secțiunea Caracteristică Drum / Configurație / Compoziție ==
    frame_caract_etc = ctk.CTkFrame(content_frame, fg_color="transparent")
    frame_caract_etc.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_caract_etc.grid_columnconfigure(0, weight=1)
    frame_caract_etc.grid_columnconfigure(1, weight=1)
    frame_caract_etc.grid_columnconfigure(2, weight=1)
    current_row += 1
    create_radio_group(frame_caract_etc, "Caracteristică drum:", "car_drum", RADIO_OPTIONS["car_drum"]).grid(row=0, column=0, sticky="nsew", padx=2)
    create_radio_group(frame_caract_etc, "Configuraţie caracteristică:", "config_caract", RADIO_OPTIONS["config_caract"]).grid(row=0, column=1, sticky="nsew", padx=2)
    create_radio_group(frame_caract_etc, "Compoziţie carosabil:", "compozitie_dr", RADIO_OPTIONS["compozitie_dr"]).grid(row=0, column=2, sticky="nsew", padx=2)


    # == Secțiunea Condiții Meteo / Luminozitate / Aderență / Stare Suprafață ==
    frame_conditii = ctk.CTkFrame(content_frame, fg_color="transparent")
    frame_conditii.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_conditii.grid_columnconfigure(0, weight=1)
    frame_conditii.grid_columnconfigure(1, weight=1)
    frame_conditii.grid_columnconfigure(2, weight=1)
    frame_conditii.grid_columnconfigure(3, weight=1)
    current_row += 1
    create_radio_group(frame_conditii, "Condiţii meteo:", "meteo", RADIO_OPTIONS["meteo"]).grid(row=0, column=0, sticky="nsew", padx=2)
    create_radio_group(frame_conditii, "Condiţii luminozitate:", "cond_lumina", RADIO_OPTIONS["cond_lumina"]).grid(row=0, column=1, sticky="nsew", padx=2)
    create_radio_group(frame_conditii, "Aderenţă carosabil:", "aderenta", RADIO_OPTIONS["aderenta"]).grid(row=0, column=2, sticky="nsew", padx=2)
    create_radio_group(frame_conditii, "Stare suprafaţă:", "stare_supraf", RADIO_OPTIONS["stare_supraf"]).grid(row=0, column=3, sticky="nsew", padx=2)


    # == Secțiunea Cauze și Mod Producere ==
    frame_cauze_mod = ctk.CTkFrame(content_frame, border_width=1, corner_radius=10)
    frame_cauze_mod.grid(row=current_row, column=0, padx=5, pady=5, sticky="ew")
    frame_cauze_mod.grid_columnconfigure(0, weight=2) # Cauze
    frame_cauze_mod.grid_columnconfigure(1, weight=1) # Mijloace siguranță / Lățime / etc.
    frame_cauze_mod.grid_columnconfigure(2, weight=1) # Mod producere
    ctk.CTkLabel(frame_cauze_mod, text="Cauze şi mod de producere", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=3, pady=(5, 10), padx=10, sticky="ew")
    current_row += 1
    # ... (populare frame_cauze_mod ca înainte) ...
    cauze_frame = ctk.CTkScrollableFrame(frame_cauze_mod, label_text="Cauze care au contribuit", height=300)
    cauze_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    cauze_frame.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(cauze_frame, text="Cauză").grid(row=0, column=0, padx=5)
    ctk.CTkLabel(cauze_frame, text="C.P.").grid(row=0, column=1, padx=5)
    ctk.CTkLabel(cauze_frame, text="C.S.").grid(row=0, column=2, padx=5)
    r_cauza = 1
    for key, text in CAUZE_TEXTS.items():
        cp_var_key = SUB_VAR_PREFIX + key + "_cp"
        cs_var_key = SUB_VAR_PREFIX + key + "_cs"
        if cp_var_key not in app_instance.data_vars: app_instance.data_vars[cp_var_key] = tk.IntVar(value=0)
        if cs_var_key not in app_instance.data_vars: app_instance.data_vars[cs_var_key] = tk.IntVar(value=0)
        ctk.CTkLabel(cauze_frame, text=text, wraplength=250, justify="left").grid(row=r_cauza, column=0, padx=5, pady=1, sticky="w")
        ctk.CTkCheckBox(cauze_frame, text="", variable=app_instance.data_vars[cp_var_key], onvalue=1, offvalue=0, width=20).grid(row=r_cauza, column=1, padx=5, pady=1)
        ctk.CTkCheckBox(cauze_frame, text="", variable=app_instance.data_vars[cs_var_key], onvalue=1, offvalue=0, width=20).grid(row=r_cauza, column=2, padx=5, pady=1)
        r_cauza += 1
    misc_frame = ctk.CTkFrame(frame_cauze_mod, fg_color="transparent")
    misc_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    create_checkbox_group(misc_frame, "Mijloace de siguranţă:", MIJL_SIG_TEXTS).pack(anchor="w", fill="x")
    create_radio_group(misc_frame, "Lăţime bandă:", "latime_banda", RADIO_OPTIONS["latime_banda"]).pack(anchor="w", fill="x", pady=(10,0))
    create_radio_group(misc_frame, "Acostament:", "acostament", RADIO_OPTIONS["acostament"]).pack(anchor="w", fill="x", pady=(10,0))
    create_radio_group(misc_frame, "Categorie bandă:", "categ_banda", RADIO_OPTIONS["categ_banda"]).pack(anchor="w", fill="x", pady=(10,0))
    create_radio_group(misc_frame, "Înclinaţie:", "inclinatie", RADIO_OPTIONS["inclinatie"]).pack(anchor="w", fill="x", pady=(10,0))
    mod_prod_frame = create_radio_group(frame_cauze_mod, "Mod de producere:", "mod_producere", RADIO_OPTIONS["mod_producere"])
    mod_prod_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)


# --- Funcții get/load data (rămân la fel) ---
def get_data(app_instance):
    """Colectează datele din variabilele Tkinter pentru acest sub-tab."""
    # ... (codul funcției get_data rămâne același ca în versiunea v3) ...
    data = {}
    data_vars = app_instance.data_vars
    print("Colectare date din sub-tab Primele Pagini (CTk)...")
    for key in ALL_SUB_TAB_KEYS: # Folosim lista combinată
        full_key = SUB_VAR_PREFIX + key
        if key.startswith("checkbox") and "cp_abateri" in key:
             cp_key = full_key + "_cp"
             cs_key = full_key + "_cs"
             orig_cp_key = key + "_cp"
             orig_cs_key = key + "_cs"
             if cp_key in data_vars: data[orig_cp_key] = data_vars[cp_key].get()
             if cs_key in data_vars: data[orig_cs_key] = data_vars[cs_key].get()
        elif full_key in data_vars:
            try:
                original_key = key.replace("display_", "")
                data[original_key] = data_vars[full_key].get()
            except Exception as e:
                print(f"Eroare la citirea variabilei {full_key}: {e}", file=sys.stderr)
                data[key] = None
        else:
            if not key.startswith("display_") and not key.endswith(("_eac", "_an")) and key not in ["numar_vehicule", "nr_penal", "nr_raniti_grav", "data_ora_cfl", "nr_raniti_usor", "nume_agent1", "insigna_agent1", "autor_necunoscut", "data_ora_acc", "sector", "lat_nord", "lat_est", "locul_accidentului"]:
                 print(f"Avertisment: Cheia {full_key} nu a fost găsită la colectare.", file=sys.stderr)
    return data

def load_data(app_instance, data_to_load):
    """Încarcă datele primite în variabilele Tkinter pentru acest sub-tab."""
    # ... (codul funcției load_data rămâne același ca în versiunea v3) ...
    data_vars = app_instance.data_vars
    print("Încărcare date în sub-tab Primele Pagini (CTk)...")
    data_ora_cfl_str = f"{data_to_load.get('ziua_doc','??')}.{data_to_load.get('luna_doc','??')}.{data_to_load.get('anul_doc','????')} / {data_to_load.get('cfl_dela','??:??')}-{data_to_load.get('cfl_panala','??:??')}"
    data_vars.get(SUB_VAR_PREFIX + "display_data_ora_cfl", tk.StringVar()).set(data_ora_cfl_str)
    data_ora_acc_str = f"{data_to_load.get('ziua_acc','??')}.{data_to_load.get('luna_acc','??')}.{data_to_load.get('anul_acc','????')} Ora: {data_to_load.get('ora_accident','??:??')}"
    data_vars.get(SUB_VAR_PREFIX + "display_data_ora_acc", tk.StringVar()).set(data_ora_acc_str)
    mapped_keys = ["numar_vehicule", "nr_penal", "nr_raniti_grav", "nr_raniti_usor",
                   "nume_agent1", "insigna_agent1", "autor_necunoscut", "sector",
                   "lat_nord", "lat_est", "locul_accidentului"]
    for key in mapped_keys:
        display_key = SUB_VAR_PREFIX + "display_" + key
        target_var = data_vars.get(display_key)
        if target_var:
             value = data_to_load.get(key, "")
             if isinstance(target_var, tk.StringVar):
                 target_var.set(str(value) if value is not None else "")
    for key in CONTROL_DATA_KEYS:
        full_key = SUB_VAR_PREFIX + key
        if key.startswith("checkbox") and "cp_abateri" in key:
             cp_key_orig = key + "_cp"
             cs_key_orig = key + "_cs"
             cp_var_key = full_key + "_cp"
             cs_var_key = full_key + "_cs"
             if cp_key_orig in data_to_load and cp_var_key in data_vars:
                 data_vars[cp_var_key].set(1 if data_to_load[cp_key_orig] else 0)
             if cs_key_orig in data_to_load and cs_var_key in data_vars:
                 data_vars[cs_var_key].set(1 if data_to_load[cs_key_orig] else 0)
        elif key in data_to_load and full_key in data_vars:
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

