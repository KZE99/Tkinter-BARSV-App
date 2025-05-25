# -*- coding: utf-8 -*-
"""
Modul pentru widget-ul reutilizabil care afișează și permite
editarea detaliilor unui singur vehicul și a conducătorului auto asociat
(Versiune CustomTkinter - Secțiune Examinare Repoziționată și Corectată).
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

try:
    from core import utils
except ImportError:
    print("AVERTISMENT: Nu s-a putut importa core.utils în auto_frame (CTk). Handler-ul RO nu va funcționa.")
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()

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

def create_vehicle_ui_ctk(parent_scrollable_frame, auto_number, vehicle_vars):
    """
    Creează și adaugă widget-urile CTk pentru un vehicul și șofer
    direct în cadrul scrollabil părinte folosind .pack().
    """
    # --- Frame Vehicul ---
    frame_vehicul = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_vehicul.pack(fill="x", padx=5, pady=5, expand=False)
    frame_vehicul.grid_columnconfigure(7, weight=1)
    ctk.CTkLabel(frame_vehicul, text=f" VEHICUL NR. {auto_number} ", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=9, pady=(5, 10), sticky="ew")
    r_veh = 1
    ctk.CTkLabel(frame_vehicul, text="Tip Vehicul:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    combo_tip_veh = ctk.CTkComboBox(frame_vehicul, width=160, state="readonly",
                                    variable=vehicle_vars.get(f'tip_autox{auto_number}'),
                                    values=['Autoturism', 'Autospecială', 'Autobuz','Tramvai','Troleibuz',
                                            'Autoutilitară', 'Motocicletă','Moped','Trotinetă electrică',
                                            'Bicicletă', 'Autorulotă', 'Tractor', 'Cap tractor', 'Tracțiune animală'],
                                    button_color=None)
    combo_tip_veh.grid(row=r_veh, column=1, padx=2, pady=2, sticky="w")
    combo_tip_veh.set('Autoturism')
    ctk.CTkLabel(frame_vehicul, text="Marca/ Tip:").grid(row=r_veh, column=2, padx=(10,2), pady=2, sticky="w")
    entry_marca = ctk.CTkEntry(frame_vehicul, width=130, textvariable=vehicle_vars.get(f'marca_autox{auto_number}'))
    entry_marca.grid(row=r_veh, column=3, padx=2, pady=2, sticky="w")
    entry_marca.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_vehicul, text="Nr.:").grid(row=r_veh, column=4, padx=(10,2), pady=2, sticky="w")
    entry_nr = ctk.CTkEntry(frame_vehicul, width=90, textvariable=vehicle_vars.get(f'nr_autox{auto_number}'))
    entry_nr.grid(row=r_veh, column=5, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_vehicul, text="Serie Șasiu:").grid(row=r_veh, column=6, padx=(10,2), pady=2, sticky="w")
    entry_vin = ctk.CTkEntry(frame_vehicul, textvariable=vehicle_vars.get(f'VIN_autox{auto_number}'))
    entry_vin.grid(row=r_veh, column=7, columnspan=2, padx=(0,5), pady=2, sticky="ew")
    r_veh += 1
    ctk.CTkLabel(frame_vehicul, text="Culoare:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    entry_culoare = ctk.CTkEntry(frame_vehicul, width=160, textvariable=vehicle_vars.get(f'culoare_autox{auto_number}'))
    entry_culoare.grid(row=r_veh, column=1, padx=2, pady=2, sticky="w")
    entry_culoare.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_vehicul, text="Proprietar:").grid(row=r_veh, column=2, padx=(10,2), pady=2, sticky="w")
    entry_prop = ctk.CTkEntry(frame_vehicul, width=130, textvariable=vehicle_vars.get(f'proprietar_autox{auto_number}'))
    entry_prop.grid(row=r_veh, column=3, padx=2, pady=2, sticky="w")
    entry_prop.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_vehicul, text="cu domiciliul/ sediul în:").grid(row=r_veh, column=4, columnspan=2, padx=(10,2), pady=2, sticky="w")
    entry_sediu_prop = ctk.CTkEntry(frame_vehicul, textvariable=vehicle_vars.get(f'sediu_autox{auto_number}'))
    entry_sediu_prop.grid(row=r_veh, column=6, columnspan=3, padx=(0,5), pady=2, sticky="ew")
    entry_sediu_prop.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    r_veh += 1
    ctk.CTkLabel(frame_vehicul, text="Utilizator:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    entry_util = ctk.CTkEntry(frame_vehicul, width=160, textvariable=vehicle_vars.get(f'utilizator_autox{auto_number}'))
    entry_util.grid(row=r_veh, column=1, padx=2, pady=2, sticky="w")
    entry_util.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_vehicul, text="cu domiciliul/ sediul în:").grid(row=r_veh, column=2, columnspan=2, padx=(10,2), pady=2, sticky="w")
    entry_sediu_util = ctk.CTkEntry(frame_vehicul, textvariable=vehicle_vars.get(f'sediu_util_autox{auto_number}'))
    entry_sediu_util.grid(row=r_veh, column=4, columnspan=5, padx=(0,5), pady=2, sticky="ew")
    entry_sediu_util.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    r_veh += 1
    ctk.CTkLabel(frame_vehicul, text="Țara înmatriculare:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    entry_tara = ctk.CTkEntry(frame_vehicul, width=160, textvariable=vehicle_vars.get(f'tara_autox{auto_number}'))
    entry_tara.grid(row=r_veh, column=1, padx=2, pady=2, sticky="w")
    entry_tara.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_vehicul, text="An fabricație:").grid(row=r_veh, column=2, padx=(10,2), pady=2, sticky="w")
    entry_an_fab = ctk.CTkEntry(frame_vehicul, width=130, textvariable=vehicle_vars.get(f'an_fabricatie_autox{auto_number}'))
    entry_an_fab.grid(row=r_veh, column=3, padx=2, pady=2, sticky="w")
    r_veh += 1
    ctk.CTkLabel(frame_vehicul, text="ITP:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    entry_itp = ctk.CTkEntry(frame_vehicul, width=160, textvariable=vehicle_vars.get(f'itp_autox{auto_number}'))
    entry_itp.grid(row=r_veh, column=1, padx=2, pady=2, sticky="w")
    r_veh += 1
    ctk.CTkLabel(frame_vehicul, text="Asigurat la:").grid(row=r_veh, column=0, padx=(5,2), pady=2, sticky="w")
    combo_rca = ctk.CTkComboBox(frame_vehicul, width=250, variable=vehicle_vars.get(f'rca_autox{auto_number}'),
                                values=['______________________','GRAWE', 'OMNIASIG','GROUPAMA', 'GENERALI',
                                        'ASIROM','AXERIA IARD','Hellas Direct Insurance LTD Nicosia – Sucursala Bucuresti',
                                        'ALLIANZ ȚIRIAC'], button_color=None)
    combo_rca.grid(row=r_veh, column=1, columnspan=2, padx=2, pady=2, sticky="w")
    combo_rca.set('______________________')
    ctk.CTkLabel(frame_vehicul, text="cu seria:").grid(row=r_veh, column=3, padx=(10,2), pady=2, sticky="w")
    entry_serie_rca = ctk.CTkEntry(frame_vehicul, width=150, textvariable=vehicle_vars.get(f'serie_rca_autox{auto_number}'))
    entry_serie_rca.grid(row=r_veh, column=4, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_vehicul, text="valabilitate:").grid(row=r_veh, column=5, padx=(10,2), pady=2, sticky="w")
    entry_start_rca = ctk.CTkEntry(frame_vehicul, width=100, textvariable=vehicle_vars.get(f'inceput_rca_autox{auto_number}'))
    entry_start_rca.grid(row=r_veh, column=6, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_vehicul, text="până la:").grid(row=r_veh, column=7, padx=(10,2), pady=2, sticky="w")
    entry_end_rca = ctk.CTkEntry(frame_vehicul, width=100, textvariable=vehicle_vars.get(f'sfarsit_rca_autox{auto_number}'))
    entry_end_rca.grid(row=r_veh, column=8, padx=(0,5), pady=(2,5), sticky="w")

    # --- Frame Vinovăție ---
    frame_vinovatie = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
    frame_vinovatie.pack(fill="x", padx=5, pady=5, expand=False)
    frame_vinovatie.columnconfigure(0, weight=1)
    frame_vinovatie.columnconfigure(1, weight=1)
    chk_vinovat = ctk.CTkCheckBox(frame_vinovatie, text="VINOVAT",
                                  variable=vehicle_vars.get(f'bifa_vinovat_autox{auto_number}'), onvalue=1, offvalue=0,
                                  hover_color="red", text_color_disabled="gray")
    chk_vinovat.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    chk_victima = ctk.CTkCheckBox(frame_vinovatie, text="VICTIMĂ",
                                  variable=vehicle_vars.get(f'bifa_victima_autox{auto_number}'), onvalue=1, offvalue=0,
                                  hover_color="red", text_color_disabled="gray")
    chk_victima.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # --- Frame Conducător Auto ---
    frame_sofer = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_sofer.pack(fill="x", padx=5, pady=5, expand=False)
    frame_sofer.columnconfigure(1, weight=1)
    frame_sofer.columnconfigure(3, weight=1)
    frame_sofer.columnconfigure(5, weight=1)
    frame_sofer.columnconfigure(6, weight=1)
    ctk.CTkLabel(frame_sofer, text=f" Conducător Auto nr. {auto_number} ", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=7, pady=(5, 10), sticky="ew")
    r_sof = 1
    ctk.CTkLabel(frame_sofer, text="Nume, prenume:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="w")
    entry_nume_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'nume_sofer_autox{auto_number}'))
    entry_nume_sof.grid(row=r_sof, column=1, padx=2, pady=2, sticky="ew")
    entry_nume_sof.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_sofer, text="CNP:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
    entry_cnp_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'cnp_sofer_autox{auto_number}'))
    entry_cnp_sof.grid(row=r_sof, column=3, padx=2, pady=2, sticky="ew")
    ctk.CTkLabel(frame_sofer, text="cu domiciliul/ sediul în:").grid(row=r_sof, column=4, columnspan=2, padx=(10,0), pady=2, sticky="w")
    r_sof += 1
    entry_adresa_sof = ctk.CTkEntry(frame_sofer, placeholder_text="Adresa...", textvariable=vehicle_vars.get(f'adresa_sofer_autox{auto_number}'))
    entry_adresa_sof.grid(row=r_sof, column=0, columnspan=5, padx=5, pady=2, sticky="ew")
    entry_adresa_sof.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_sofer, text="Cetățenie:").grid(row=r_sof, column=5, padx=(10,2), pady=2, sticky="w")
    entry_cet_sof = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'cetatenie_sofer_autox{auto_number}'))
    entry_cet_sof.grid(row=r_sof, column=6, padx=(0,5), pady=2, sticky="ew")
    entry_cet_sof.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    r_sof += 1
    ctk.CTkLabel(frame_sofer, text="PC nr.:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="w")
    entry_nrpc = ctk.CTkEntry(frame_sofer, width=120, textvariable=vehicle_vars.get(f'nrpc_sofer_autox{auto_number}'))
    entry_nrpc.grid(row=r_sof, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_sofer, text="Categoriile:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
    entry_catpc = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'catpc_sofer_autox{auto_number}'))
    entry_catpc.grid(row=r_sof, column=3, padx=2, pady=2, sticky="ew")
    entry_catpc.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_sofer, text="cu vechime din anul:").grid(row=r_sof, column=4, padx=(10,2), pady=2, sticky="w")
    entry_vechime = ctk.CTkEntry(frame_sofer, width=60, textvariable=vehicle_vars.get(f'vechime_pc_sofer_autox{auto_number}'))
    entry_vechime.grid(row=r_sof, column=5, padx=2, pady=2, sticky="w")
    r_sof += 1
    # ... (Continuă cu restul câmpurilor din frame_sofer) ...
    ctk.CTkLabel(frame_sofer, text="cu atestat profesional:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="w")
    entry_atestat = ctk.CTkEntry(frame_sofer, width=180, textvariable=vehicle_vars.get(f'atestat_sofer_autox{auto_number}'))
    entry_atestat.grid(row=r_sof, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_sofer, text="eliberat la data de:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
    entry_data_atestat = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'data_atestat_sofer_autox{auto_number}'))
    entry_data_atestat.grid(row=r_sof, column=3, padx=2, pady=2, sticky="ew")
    r_sof += 1
    ctk.CTkLabel(frame_sofer, text="angajat la:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="w")
    entry_angajat = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'angajat_sofer_autox{auto_number}'))
    entry_angajat.grid(row=r_sof, column=1, columnspan=2, padx=2, pady=2, sticky="ew")
    entry_angajat.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    ctk.CTkLabel(frame_sofer, text="în funcția de:").grid(row=r_sof, column=3, padx=(10,2), pady=2, sticky="w")
    entry_functie = ctk.CTkEntry(frame_sofer, textvariable=vehicle_vars.get(f'functie_sofer_autox{auto_number}'))
    entry_functie.grid(row=r_sof, column=4, columnspan=3, padx=(0,5), pady=2, sticky="ew")
    entry_functie.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    r_sof += 1
    ctk.CTkLabel(frame_sofer, text="Telefon:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="w")
    entry_tel_sof = ctk.CTkEntry(frame_sofer, width=180, textvariable=vehicle_vars.get(f'tel_sofer_autox{auto_number}'))
    entry_tel_sof.grid(row=r_sof, column=1, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_sofer, text="în calitate de:").grid(row=r_sof, column=2, padx=(10,2), pady=2, sticky="w")
    combo_cal_sof = ctk.CTkComboBox(frame_sofer, width=200, state="readonly",
                                    variable=vehicle_vars.get(f'calitate_sofer_autox{auto_number}'),
                                    values=['','conducător auto','conducător tramvai','conducător autobuz',
                                            'conducător moto','conducător moped','conducător trotinetă',
                                            'conducător bicicletă'], button_color=None)
    combo_cal_sof.grid(row=r_sof, column=3, columnspan=2, padx=2, pady=2, sticky="w")
    combo_cal_sof.set('conducător auto')
    r_sof += 1
    ctk.CTkLabel(frame_sofer, text="Diagnostic:").grid(row=r_sof, column=0, padx=(5,2), pady=2, sticky="nw")
    textbox_diag_sof = ctk.CTkTextbox(frame_sofer, height=60, wrap=tk.WORD)
    textbox_diag_sof.grid(row=r_sof, column=1, columnspan=6, padx=(0,5), pady=(2,5), sticky="ew")
    textbox_diag_sof.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    diag_sof_var = vehicle_vars.get(f'diagnostic_sofer_autox{auto_number}')
    if diag_sof_var:
        init_diag_sof = diag_sof_var.get()
        if init_diag_sof: textbox_diag_sof.insert("1.0", init_diag_sof)
        textbox_diag_sof.bind("<FocusOut>", lambda event, w=textbox_diag_sof, v=diag_sof_var: _update_var_from_text(w, v))

    # --- Frame Documente și Articole CP ---
    frame_docs_cp_container = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
    frame_docs_cp_container.pack(fill="x", padx=5, pady=5, expand=False)
    frame_docs_cp_container.columnconfigure(0, weight=1)
    frame_docs_cp_container.columnconfigure(1, weight=1)

    # Frame Întocmire Documente
    frame_docs = ctk.CTkFrame(frame_docs_cp_container, border_width=1, corner_radius=10)
    frame_docs.grid(row=0, column=0, padx=(0,5), pady=0, sticky="nsew")
    ctk.CTkLabel(frame_docs, text="Întocmire documente", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=4, pady=(5, 10), sticky="ew")
    # ... (Restul widget-urilor din frame_docs) ...
    r_doc = 1
    chk_nota_sof = ctk.CTkCheckBox(frame_docs, text="Notă vinovăție", variable=vehicle_vars.get(f'nota_vinovatie_sofer_autox{auto_number}'), onvalue=1, offvalue=0)
    chk_nota_sof.grid(row=r_doc, column=0, padx=5, pady=2, sticky="w")
    ctk.CTkLabel(frame_docs, text="Articol OUG 195:").grid(row=r_doc, column=1, padx=(5,2), pady=2, sticky="w")
    entry_art_oug = ctk.CTkEntry(frame_docs, width=100, textvariable=vehicle_vars.get(f'articol_sofer_autox{auto_number}'))
    entry_art_oug.grid(row=r_doc, column=2, columnspan=2, padx=2, pady=2, sticky="w")
    r_doc += 1
    chk_ret_acc = ctk.CTkCheckBox(frame_docs, text="Raport Reținere PC - Accident", variable=vehicle_vars.get(f'raport_retinere_sofer_autox{auto_number}'), onvalue=1, offvalue=0)
    chk_ret_acc.grid(row=r_doc, column=0, columnspan=4, padx=5, pady=2, sticky="w")
    r_doc += 1
    chk_pc_ret = ctk.CTkCheckBox(frame_docs, text="A fost reținut PC", variable=vehicle_vars.get(f'bifa_pc_sofer_autox{auto_number}'), onvalue=1, offvalue=0)
    chk_pc_ret.grid(row=r_doc, column=0, columnspan=2, padx=5, pady=2, sticky="w")
    r_doc += 1
    ctk.CTkLabel(frame_docs, text="Amendă:").grid(row=r_doc, column=0, padx=5, pady=2, sticky="w")
    combo_amenda = ctk.CTkComboBox(frame_docs, width=150, variable=vehicle_vars.get(f'amenda_retinere_autox{auto_number}'),
                                   values=['', 'AVERTISMENT', '_______________'], button_color=None)
    combo_amenda.grid(row=r_doc, column=1, columnspan=3, padx=2, pady=2, sticky="w")
    combo_amenda.set('_______________')
    r_doc += 1
    ctk.CTkFrame(frame_docs, height=1, fg_color="gray50").grid(row=r_doc, column=0, columnspan=4, sticky='ew', pady=5, padx=5)
    r_doc += 1
    chk_ret_itp = ctk.CTkCheckBox(frame_docs, text="Raport Reținere ITP Expirat", variable=vehicle_vars.get(f'raport_retinere_itp_autox{auto_number}'), onvalue=1, offvalue=0)
    chk_ret_itp.grid(row=r_doc, column=0, columnspan=2, padx=5, pady=2, sticky="w")
    ctk.CTkLabel(frame_docs, text="Serie PVCC:").grid(row=r_doc, column=2, padx=(5,2), pady=2, sticky="w")
    entry_pvcc = ctk.CTkEntry(frame_docs, width=80, textvariable=vehicle_vars.get(f'serie_pvcc_autox{auto_number}'))
    entry_pvcc.grid(row=r_doc, column=3, padx=2, pady=2, sticky="w")
    r_doc += 1
    chk_ret_rca = ctk.CTkCheckBox(frame_docs, text="Raport Reținere RCA Expirat", variable=vehicle_vars.get(f'raport_retinere_rca_autox{auto_number}'), onvalue=1, offvalue=0)
    chk_ret_rca.grid(row=r_doc, column=0, columnspan=4, padx=5, pady=(2,5), sticky="w")

    # Frame Articole CP
    frame_cp = ctk.CTkFrame(frame_docs_cp_container, border_width=1, corner_radius=10)
    frame_cp.grid(row=0, column=1, padx=(5,0), pady=0, sticky="nsew")
    ctk.CTkLabel(frame_cp, text="+ alt articol CP:", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=(5, 10), sticky="ew")
    # ... (Restul widget-urilor din frame_cp) ...
    cp_keys = [
        'art_334_1_autox', 'art_336_1_autox', 'art_334_2_autox', 'art_336_1ind1_autox',
        'art_334_3_autox', 'art_336_2_autox', 'art_334_4_autox', 'art_337_autox',
        'art_335_1_autox', 'art_338_1_autox', 'art_335_2_autox', 'art_338_2_autox'
    ]
    cp_texts = {
        'art_334_1_autox': 'Art. 334/1', 'art_336_1_autox': 'Art. 336/1',
        'art_334_2_autox': 'Art. 334/2', 'art_336_1ind1_autox': 'Art. 336/1^1',
        'art_334_3_autox': 'Art. 334/3', 'art_336_2_autox': 'Art. 336/2',
        'art_334_4_autox': 'Art. 334/4', 'art_337_autox': 'Art. 337',
        'art_335_1_autox': 'Art. 335/1', 'art_338_1_autox': 'Art. 338/1',
        'art_335_2_autox': 'Art. 335/2', 'art_338_2_autox': 'Art. 338/2'
    }
    r_cp = 1
    c_cp = 0
    for key in cp_keys:
        chk = ctk.CTkCheckBox(frame_cp, text=cp_texts[key], width=110, variable=vehicle_vars.get(key), onvalue=1, offvalue=0)
        chk.grid(row=r_cp, column=c_cp, padx=10, pady=2, sticky="w")
        c_cp = (c_cp + 1) % 2
        if c_cp == 0: r_cp += 1

    # --- Frame Testări ---
    frame_testari = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_testari.pack(fill="x", padx=5, pady=5, expand=False)
    frame_testari.columnconfigure(1, weight=1)
    frame_testari.columnconfigure(3, weight=1)
    frame_testari.columnconfigure(5, weight=1)
    ctk.CTkLabel(frame_testari, text="Testări", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, columnspan=7, pady=(5, 10), sticky="ew")
    # ... (Restul widget-urilor din frame_testari) ...
    r_test = 1
    combo_etilo = ctk.CTkComboBox(frame_testari, width=150, state="readonly", variable=vehicle_vars.get(f'etilo_autox{auto_number}'),
                                  values=['A fost testat','Nu a fost testat', 'A refuzat testarea'], button_color=None)
    combo_etilo.grid(row=r_test, column=0, padx=(5,2), pady=2, sticky="w")
    combo_etilo.set('A fost testat')
    ctk.CTkLabel(frame_testari, text="cu aparatul etilotest marca Drager seria").grid(row=r_test, column=1, padx=(5,2), pady=2, sticky="w")
    entry_serie_etilo = ctk.CTkEntry(frame_testari, width=100, textvariable=vehicle_vars.get(f'serie_etilo_autox{auto_number}'))
    entry_serie_etilo.grid(row=r_test, column=2, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_testari, text="care la poziția").grid(row=r_test, column=3, padx=(10,2), pady=2, sticky="w")
    entry_poz_etilo = ctk.CTkEntry(frame_testari, width=100, textvariable=vehicle_vars.get(f'pozitie_etilo_autox{auto_number}'))
    entry_poz_etilo.grid(row=r_test, column=4, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_testari, text="a indicat o valoare de").grid(row=r_test, column=5, padx=(10,2), pady=2, sticky="w")
    combo_rez_etilo = ctk.CTkComboBox(frame_testari, width=80, variable=vehicle_vars.get(f'rezultat_etilo_autox{auto_number}'),
                                      values=['0,00', ' '], button_color=None)
    combo_rez_etilo.grid(row=r_test, column=6, padx=(0,5), pady=2, sticky="w")
    combo_rez_etilo.set('0,00')
    r_test += 1
    ctk.CTkLabel(frame_testari, text="mg/l alcool pur în aerul expirat.").grid(row=r_test, column=0, columnspan=7, padx=5, pady=(0,5), sticky="w")
    r_test += 1
    combo_drug = ctk.CTkComboBox(frame_testari, width=150, state="readonly", variable=vehicle_vars.get(f'drugtest_autox{auto_number}'),
                                 values=['A fost testat','Nu a fost testat', 'A refuzat testarea'], button_color=None)
    combo_drug.grid(row=r_test, column=0, padx=(5,2), pady=2, sticky="w")
    combo_drug.set('Nu a fost testat')
    ctk.CTkLabel(frame_testari, text="cu aparatul Drugtest marca Drager seria").grid(row=r_test, column=1, padx=(5,2), pady=2, sticky="w")
    entry_serie_drug = ctk.CTkEntry(frame_testari, width=100, textvariable=vehicle_vars.get(f'serie_drugtest_autox{auto_number}'))
    entry_serie_drug.grid(row=r_test, column=2, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_testari, text="care la poziția").grid(row=r_test, column=3, padx=(10,2), pady=2, sticky="w")
    entry_poz_drug = ctk.CTkEntry(frame_testari, width=100, textvariable=vehicle_vars.get(f'pozitie_drugtest_autox{auto_number}'))
    entry_poz_drug.grid(row=r_test, column=4, padx=2, pady=2, sticky="w")
    ctk.CTkLabel(frame_testari, text="a indicat un rezultat").grid(row=r_test, column=5, padx=(10,2), pady=2, sticky="w")
    combo_rez_drug = ctk.CTkComboBox(frame_testari, width=100, state="readonly", variable=vehicle_vars.get(f'rezultat_drugtest_autox{auto_number}'),
                                     values=['Pozitiv', 'Negativ', '-----------'], button_color=None)
    combo_rez_drug.grid(row=r_test, column=6, padx=(0,5), pady=2, sticky="w")
    combo_rez_drug.set('-----------')
    r_test += 1
    ctk.CTkLabel(frame_testari, text="la").grid(row=r_test, column=0, padx=5, pady=2, sticky="e")
    entry_droguri = ctk.CTkEntry(frame_testari, width=150, textvariable=vehicle_vars.get(f'droguri_drugtest_autox{auto_number}'))
    entry_droguri.grid(row=r_test, column=1, columnspan=2, padx=2, pady=2, sticky="w")
    r_test += 1
    combo_inml = ctk.CTkComboBox(frame_testari, width=180, state="readonly", variable=vehicle_vars.get(f'inml_autox{auto_number}'),
                                 values=['Au fost recoltate','Nu au fost recoltate'], button_color=None)
    combo_inml.grid(row=r_test, column=0, columnspan=2, padx=(5,2), pady=(5,5), sticky="w")
    combo_inml.set('Nu au fost recoltate')
    ctk.CTkLabel(frame_testari, text="probe biologice. Sigiliu trusa:").grid(row=r_test, column=2, padx=(10,2), pady=(5,5), sticky="w")
    entry_sigiliu = ctk.CTkEntry(frame_testari, width=150, textvariable=vehicle_vars.get(f'sigiliu_inml_autox{auto_number}'))
    entry_sigiliu.grid(row=r_test, column=3, columnspan=2, padx=2, pady=(5,5), sticky="w")

    # --- Frame Declarație ---
    frame_decl = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_decl.pack(fill="x", padx=5, pady=5, expand=False)
    frame_decl.columnconfigure(0, weight=1)
    frame_decl.rowconfigure(1, weight=1)
    ctk.CTkLabel(frame_decl, text="Declarație", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=5, sticky="ew")
    textbox_decl = ctk.CTkTextbox(frame_decl, height=100, wrap=tk.WORD)
    textbox_decl.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
    textbox_decl.insert('1.0', 'Persoana în cauză nu a fost prezentă la fața locului la momentul efectuării CFL.')
    textbox_decl.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    decl_sof_var = vehicle_vars.get(f'text_declaratie_sofer_autox{auto_number}')
    if decl_sof_var:
        init_decl_sof = decl_sof_var.get()
        if init_decl_sof and init_decl_sof != 'Persoana în cauză nu a fost prezentă la fața locului la momentul efectuării CFL.':
             textbox_decl.delete("1.0", "end")
             textbox_decl.insert("1.0", init_decl_sof)
        textbox_decl.bind("<FocusOut>", lambda event, w=textbox_decl, v=decl_sof_var: _update_var_from_text(w, v))

    # --- Frame Poziție Vehicul ---
    frame_poz = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_poz.pack(fill="x", padx=5, pady=5, expand=False)
    frame_poz.columnconfigure(0, weight=1)
    frame_poz.rowconfigure(1, weight=1)
    ctk.CTkLabel(frame_poz, text="La fața locului vehiculul se afla în următoarea poziție:", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=5, sticky="ew")
    textbox_poz = ctk.CTkTextbox(frame_poz, height=100, wrap=tk.WORD)
    textbox_poz.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
    textbox_poz.insert('1.0', 'Vehiculul nu se afla în poziția inițială producerii accidentului la momentul efectuării CFL.')
    textbox_poz.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    poz_var = vehicle_vars.get(f'text_pozitie_autox{auto_number}')
    if poz_var:
        init_poz = poz_var.get()
        if init_poz and init_poz != 'Vehiculul nu se afla în poziția inițială producerii accidentului la momentul efectuării CFL.':
             textbox_poz.delete("1.0", "end")
             textbox_poz.insert("1.0", init_poz)
        textbox_poz.bind("<FocusOut>", lambda event, w=textbox_poz, v=poz_var: _update_var_from_text(w, v))

    # --- Frame Avarii (SINGURUL ȘI POZIȚIONAT ÎNAINTE DE EXAMINARE) ---
    frame_avarii = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    frame_avarii.pack(fill="x", padx=5, pady=5, expand=False)
    frame_avarii.columnconfigure(0, weight=1)
    frame_avarii.rowconfigure(1, weight=1)
    ctk.CTkLabel(frame_avarii, text=f"Avarii Vehicul nr. {auto_number}", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=5, sticky="ew")
    textbox_avarii = ctk.CTkTextbox(frame_avarii, height=100, wrap=tk.WORD)
    textbox_avarii.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
    textbox_avarii.insert('1.0', 'Nu există avarii.')
    textbox_avarii.bind("<KeyPress>", utils.handle_romanian_characters_keypress)
    avarii_var = vehicle_vars.get(f'text_avarii_autox{auto_number}')
    if avarii_var:
        init_avarii = avarii_var.get()
        if init_avarii and init_avarii != 'Nu există avarii.':
             textbox_avarii.delete("1.0", "end")
             textbox_avarii.insert("1.0", init_avarii)
        textbox_avarii.bind("<FocusOut>", lambda event, w=textbox_avarii, v=avarii_var: _update_var_from_text(w, v))


    # --- SECȚIUNE EXAMINARE VEHICUL (COLLAPSIBLE) ---
    # Starea de vizibilitate este legată la o variabilă Tkinter
    examinare_visible_var_key = f'examinare_vehicul_visible{auto_number}'
    examinare_visible_var = vehicle_vars.get(examinare_visible_var_key)
    # Asigură-te că variabila există (ar trebui creată în auto_tab.py)
    if not isinstance(examinare_visible_var, tk.IntVar):
        print(f"AVERTISMENT: Variabila {examinare_visible_var_key} nu este IntVar sau lipsește. Se creează default.")
        examinare_visible_var = tk.IntVar(value=0) # Inițial colapsat
        # Nu o adăugăm în vehicle_vars aici, ar trebui să vină din auto_tab.py

    # Frame-ul care va fi ascuns/afișat
    frame_examinare_content = ctk.CTkFrame(parent_scrollable_frame, border_width=1, corner_radius=10)
    # Inițial nu îl adăugăm cu .pack() sau .grid() pentru a fi ascuns

    def toggle_examinare():
        if examinare_visible_var.get() == 0: # Dacă e ascuns, îl afișăm
            # Adaugă frame_examinare_content DUPĂ butonul de toggle
            frame_examinare_content.pack(fill="x", padx=5, pady=(0,5), expand=False, after=btn_toggle_examinare)
            btn_toggle_examinare.configure(text="▼ Examinând vehiculul am constatat următoarele:")
            examinare_visible_var.set(1)
        else: # Dacă e vizibil, îl ascundem
            frame_examinare_content.pack_forget()
            btn_toggle_examinare.configure(text="▶ Examinând vehiculul am constatat următoarele:")
            examinare_visible_var.set(0)

    btn_toggle_examinare = ctk.CTkButton(
        parent_scrollable_frame,
        text="▶ Examinând vehiculul am constatat următoarele:",
        command=toggle_examinare,
        anchor="w",
        fg_color=("gray70", "gray25"), # Un fundal mai vizibil pentru buton
        text_color=(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
        hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"]
    )
    # Adaugă butonul de toggle DUPĂ frame_avarii
    btn_toggle_examinare.pack(fill="x", padx=5, pady=(10,0))

    # Populăm frame_examinare_content
    ex_row = 0
    ctk.CTkLabel(frame_examinare_content, text="Detalii suplimentare vehicul:", font=ctk.CTkFont(weight="bold")).grid(
        row=ex_row, column=0, columnspan=4, pady=(5,10), padx=5, sticky="ew")
    ex_row += 1
    # Anvelope
    frame_anv = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_anv.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_anv, text="- tipul anvelopelor:").pack(side="left")
    combo_anv_tip = ctk.CTkComboBox(frame_anv, width=100, variable=vehicle_vars.get(f'examinare_anvelope_tip{auto_number}'), values=['vară', 'iarnă', 'mixt'], button_color=None)
    combo_anv_tip.pack(side="left", padx=2)
    ctk.CTkLabel(frame_anv, text=", uzura anvelopelor:").pack(side="left")
    combo_anv_uzura = ctk.CTkComboBox(frame_anv, width=120, variable=vehicle_vars.get(f'examinare_anvelope_uzura{auto_number}'), values=['redusă', 'medie', 'peste limită'], button_color=None)
    combo_anv_uzura.pack(side="left", padx=2)
    ex_row += 1
    # Iluminare
    frame_ilum = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_ilum.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_ilum, text="- sistemul de iluminare semnalizare – în stare de funcționare:").pack(side="left")
    combo_ilum = ctk.CTkComboBox(frame_ilum, width=150, variable=vehicle_vars.get(f'examinare_iluminare_functional{auto_number}'), values=['da', 'nu', 'nu se poate stabili'], button_color=None)
    combo_ilum.pack(side="left", padx=2)
    ex_row += 1
    # ... (restul câmpurilor din frame_examinare_content, exact ca în versiunea anterioară) ...
    # Ștergătoare
    frame_sterg = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_sterg.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_sterg, text="- ștergătoare de parbriz – există:").pack(side="left")
    combo_sterg_ex = ctk.CTkComboBox(frame_sterg, width=80, variable=vehicle_vars.get(f'examinare_stergatoare_exista{auto_number}'), values=['da', 'nu'], button_color=None)
    combo_sterg_ex.pack(side="left", padx=2)
    ctk.CTkLabel(frame_sterg, text=", în stare de funcționare:").pack(side="left")
    combo_sterg_func = ctk.CTkComboBox(frame_sterg, width=150, variable=vehicle_vars.get(f'examinare_stergatoare_functional{auto_number}'), values=['da', 'nu', 'nu se poate stabili'], button_color=None)
    combo_sterg_func.pack(side="left", padx=2)
    ex_row += 1
    # Portiere
    frame_port = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_port.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_port, text="- portierele:").pack(side="left")
    combo_port_stare = ctk.CTkComboBox(frame_port, width=100, variable=vehicle_vars.get(f'examinare_portiere_stare{auto_number}'), values=['închise', 'deschise'], button_color=None)
    combo_port_stare.pack(side="left", padx=2)
    combo_port_asig = ctk.CTkComboBox(frame_port, width=120, variable=vehicle_vars.get(f'examinare_portiere_asigurare{auto_number}'), values=['asigurate', 'neasigurate'], button_color=None)
    combo_port_asig.pack(side="left", padx=2)
    ctk.CTkLabel(frame_port, text="cu mecanism:").pack(side="left")
    combo_port_mec = ctk.CTkComboBox(frame_port, width=100, variable=vehicle_vars.get(f'examinare_portiere_mecanism{auto_number}'), values=['asistat', 'manual'], button_color=None)
    combo_port_mec.pack(side="left", padx=2)
    ex_row += 1
    # Manete și airbaguri
    frame_manete = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_manete.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
    frame_manete.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_manete, text="- poziția manetei schimbător de viteze:").grid(row=0, column=0, sticky="w", pady=1)
    ctk.CTkEntry(frame_manete, textvariable=vehicle_vars.get(f'examinare_maneta_viteze{auto_number}')).grid(row=0, column=1, sticky="ew", padx=5, pady=1)
    ctk.CTkLabel(frame_manete, text="- poziția manetei frână de mână:").grid(row=1, column=0, sticky="w", pady=1)
    ctk.CTkEntry(frame_manete, textvariable=vehicle_vars.get(f'examinare_frana_mana{auto_number}')).grid(row=1, column=1, sticky="ew", padx=5, pady=1)
    ctk.CTkLabel(frame_manete, text="- airbag-uri declanșate:").grid(row=2, column=0, sticky="w", pady=1)
    ctk.CTkEntry(frame_manete, textvariable=vehicle_vars.get(f'examinare_airbaguri{auto_number}')).grid(row=2, column=1, sticky="ew", padx=5, pady=1)
    ex_row += 1
    # Kilometraj
    frame_km = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_km.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_km, text="- poziția acului kilometraj:").pack(side="left")
    ctk.CTkEntry(frame_km, width=70, textvariable=vehicle_vars.get(f'examinare_ac_kilometraj{auto_number}')).pack(side="left", padx=2)
    ctk.CTkLabel(frame_km, text="km/h, turometru:").pack(side="left")
    ctk.CTkEntry(frame_km, width=70, textvariable=vehicle_vars.get(f'examinare_turometru{auto_number}')).pack(side="left", padx=2)
    ctk.CTkLabel(frame_km, text="rot/min, km indicați:").pack(side="left")
    ctk.CTkEntry(frame_km, width=100, textvariable=vehicle_vars.get(f'examinare_km_indicati{auto_number}')).pack(side="left", padx=2)
    ex_row += 1
    # Frâne
    frame_frane = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_frane.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_frane, text="- pedala/maneta frânei de serviciu – opune rezistență:").pack(side="left")
    combo_ped_frana = ctk.CTkComboBox(frame_frane, width=150, variable=vehicle_vars.get(f'examinare_pedala_frana{auto_number}'), values=['da', 'nu', 'nu se poate stabili'], button_color=None)
    combo_ped_frana.pack(side="left", padx=2)
    ctk.CTkLabel(frame_frane, text=", sistemul de frânare:").pack(side="left")
    combo_sist_frana = ctk.CTkComboBox(frame_frane, width=150, variable=vehicle_vars.get(f'examinare_sistem_franare{auto_number}'), values=['clasic', 'servo-asistat', 'ABS'], button_color=None)
    combo_sist_frana.pack(side="left", padx=2)
    ex_row += 1
    # Încărcătură
    frame_incarc = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_incarc.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="ew")
    frame_incarc.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_incarc, text="- încărcat cu: persoane nr.").grid(row=0, column=0, sticky="w", pady=1)
    ctk.CTkEntry(frame_incarc, width=50, textvariable=vehicle_vars.get(f'examinare_incarcatura_persoane{auto_number}')).grid(row=0, column=1, sticky="w", padx=2, pady=1)
    ctk.CTkLabel(frame_incarc, text="/ tip încărcătură:").grid(row=0, column=2, sticky="w", pady=1)
    ctk.CTkEntry(frame_incarc, textvariable=vehicle_vars.get(f'examinare_incarcatura_tip{auto_number}')).grid(row=0, column=3, sticky="ew", padx=2, pady=1)
    ctk.CTkLabel(frame_incarc, text="- greutatea, modul de așezare și prindere a încărcăturii:").grid(row=1, column=0, columnspan=4, sticky="w", pady=1)
    ctk.CTkEntry(frame_incarc, placeholder_text="Detalii încărcătură...", textvariable=vehicle_vars.get(f'examinare_incarcatura_detalii{auto_number}')).grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=1)
    ex_row += 1
    # Elemente siguranță
    frame_sig = ctk.CTkFrame(frame_examinare_content, fg_color="transparent")
    frame_sig.grid(row=ex_row, column=0, columnspan=4, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_sig, text="- elemente de siguranță și protecție:").pack(anchor="w")
    sig_options_frame = ctk.CTkFrame(frame_sig, fg_color="transparent")
    sig_options_frame.pack(anchor="w", fill="x")
    ctk.CTkCheckBox(sig_options_frame, text="centuri", variable=vehicle_vars.get(f'examinare_sig_centuri{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkCheckBox(sig_options_frame, text="scaun copil", variable=vehicle_vars.get(f'examinare_sig_scaun_copil{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkCheckBox(sig_options_frame, text="reflectorizante", variable=vehicle_vars.get(f'examinare_sig_reflectorizante{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkCheckBox(sig_options_frame, text="cască", variable=vehicle_vars.get(f'examinare_sig_casca{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkCheckBox(sig_options_frame, text="geacă", variable=vehicle_vars.get(f'examinare_sig_geaca{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkCheckBox(sig_options_frame, text="pantaloni", variable=vehicle_vars.get(f'examinare_sig_pantaloni{auto_number}'), onvalue=1, offvalue=0).pack(side="left", padx=5)
    ctk.CTkEntry(sig_options_frame, placeholder_text="Altele...", width=150, textvariable=vehicle_vars.get(f'examinare_sig_altele{auto_number}')).pack(side="left", padx=5, pady=(0,5), expand=True, fill="x")


    # Inițializează starea butonului de toggle și vizibilitatea cadrului
    if examinare_visible_var.get() == 1:
        frame_examinare_content.pack(fill="x", padx=5, pady=(0,5), expand=False, after=btn_toggle_examinare)
        btn_toggle_examinare.configure(text="▼ Examinând vehiculul am constatat următoarele:")
    else:
        # frame_examinare_content nu este adăugat cu pack inițial, deci e ascuns
        btn_toggle_examinare.configure(text="▶ Examinând vehiculul am constatat următoarele:")

    # NU mai returnăm nimic, widget-urile sunt adăugate direct la parent_scrollable_frame

# ... (restul codului, inclusiv if __name__ == "__main__":)
