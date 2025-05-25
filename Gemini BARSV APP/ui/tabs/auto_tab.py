# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'Auto Implicate'.
(Versiune CustomTkinter cu corecție finală pentru butonul de adăugare)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
import traceback

try:
    from core import utils
    from ui.widgets import auto_frame # Presupune că auto_frame.py conține create_vehicle_ui_ctk
except ImportError as e:
     messagebox.showerror("Eroare Import Auto Tab (CTk)", f"Nu s-au putut importa modulele necesare: {e}")
     sys.exit(1)

VAR_PREFIX = "auto_"

DATA_KEYS_PER_AUTO = [
    "tip_autox", "marca_autox", "nr_autox", "VIN_autox", "culoare_autox",
    "proprietar_autox", "sediu_autox", "utilizator_autox", "sediu_util_autox",
    "tara_autox", "an_fabricatie_autox", "itp_autox", "rca_autox",
    "serie_rca_autox", "inceput_rca_autox", "sfarsit_rca_autox",
    "bifa_vinovat_autox", "bifa_victima_autox",
    "nume_sofer_autox", "cnp_sofer_autox", "adresa_sofer_autox",
    "cetatenie_sofer_autox", "nrpc_sofer_autox", "catpc_sofer_autox",
    "vechime_pc_sofer_autox",
    "atestat_sofer_autox", "data_atestat_sofer_autox", "angajat_sofer_autox",
    "functie_sofer_autox", "tel_sofer_autox", "calitate_sofer_autox",
    "diagnostic_sofer_autox",
    "nota_vinovatie_sofer_autox", "articol_sofer_autox",
    "raport_retinere_sofer_autox", "bifa_pc_sofer_autox", "amenda_retinere_autox",
    "serie_pvcc_autox", "raport_retinere_itp_autox", "raport_retinere_rca_autox",
    "art_334_1_autox", "art_336_1_autox", "art_334_2_autox", "art_336_1ind1_autox",
    "art_334_3_autox", "art_336_2_autox", "art_334_4_autox", "art_337_autox",
    "art_335_1_autox", "art_338_1_autox", "art_335_2_autox", "art_338_2_autox",
    "etilo_autox", "serie_etilo_autox", "pozitie_etilo_autox",
    "rezultat_etilo_autox", "drugtest_autox", "serie_drugtest_autox",
    "pozitie_drugtest_autox", "rezultat_drugtest_autox",
    "droguri_drugtest_autox", "inml_autox", "sigiliu_inml_autox",
    "text_declaratie_sofer_autox", "text_pozitie_autox", "text_avarii_autox",
    "examinare_vehicul_visiblex", # Adăugat pentru starea dropdown-ului
    "examinare_anvelope_tipx", "examinare_anvelope_uzurax", "examinare_iluminare_functionalx",
    "examinare_stergatoare_existax", "examinare_stergatoare_functionalx",
    "examinare_portiere_starex", "examinare_portiere_asigurarex", "examinare_portiere_mecanismx",
    "examinare_maneta_vitezex", "examinare_frana_manax", "examinare_airbagurix",
    "examinare_ac_kilometrajx", "examinare_turometrux", "examinare_km_indicatix",
    "examinare_pedala_franax", "examinare_sistem_franarex",
    "examinare_incarcatura_persoanex", "examinare_incarcatura_tipx", "examinare_incarcatura_detaliix",
    "examinare_sig_centurix", "examinare_sig_scaun_copilx", "examinare_sig_reflectorizantex",
    "examinare_sig_cascax", "examinare_sig_geacax", "examinare_sig_pantalunix", "examinare_sig_altelex"
]

def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'Auto Implicate'.
    """
    parent_container.grid_rowconfigure(0, weight=1)
    parent_container.grid_columnconfigure(0, weight=1)

    parent_container.inner_tabview = ctk.CTkTabview(parent_container, border_width=1)
    parent_container.inner_tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5,0))

    add_button_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    add_button_frame.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    add_button = ctk.CTkButton(
        add_button_frame,
        text="+ Adaugă Vehicul",
        command=lambda: add_new_auto_tab(parent_container, app_instance)
    )
    add_button.pack()

    add_new_auto_tab(parent_container, app_instance, auto_index=1)
    add_new_auto_tab(parent_container, app_instance, auto_index=2)


def add_new_auto_tab(tab_container, app_instance, data_to_load=None, auto_index=None):
    """
    Adaugă un nou sub-tab pentru un vehicul.
    """
    inner_tabview = tab_container.inner_tabview

    if auto_index is None:
        # --- CORECȚIE: Folosim len(app_instance.auto_frames) pentru a determina numărul ---
        auto_number = len(app_instance.auto_frames) + 1
        # --- SFÂRȘIT CORECȚIE ---
    else:
        auto_number = auto_index

    print(f"Adăugare sub-tab CTk pentru Vehiculul Nr. {auto_number}")

    tab_name = f" Vehicul {auto_number} "
    try:
        existing_tab = None
        try:
            # Verifică dacă tab-ul există deja
            existing_tab = inner_tabview.tab(tab_name)
        except ValueError:
            pass # Tab-ul nu există, e ok

        if existing_tab:
            print(f"Avertisment: Tab-ul '{tab_name}' există deja. Se selectează.")
            inner_tabview.set(tab_name)
            # TODO: Aici ar trebui să actualizăm datele tab-ului existent dacă data_to_load este furnizat
            # Poate prin ștergerea și recrearea conținutului său sau printr-o funcție de update dedicată.
            return
        else:
            inner_tabview.add(tab_name) # Adaugă noul tab

    except Exception as ex: # Prinde alte excepții posibile la .add()
         print(f"Eroare neașteptată la adăugarea tab-ului '{tab_name}': {ex}", file=sys.stderr)
         traceback.print_exc(file=sys.stderr)
         return

    new_tab_container = inner_tabview.tab(tab_name)
    if not new_tab_container:
        print(f"Eroare: Nu s-a putut obține containerul pentru tab-ul '{tab_name}'")
        return

    new_tab_container.grid_rowconfigure(0, weight=1)
    new_tab_container.grid_columnconfigure(0, weight=1)

    vehicle_scrollable_frame = ctk.CTkScrollableFrame(new_tab_container)
    vehicle_scrollable_frame.grid(row=0, column=0, sticky="nsew")

    vehicle_vars = {}
    for key_template in DATA_KEYS_PER_AUTO:
        base_key = key_template[:-1] if key_template.endswith('x') else key_template
        data_key = f"{base_key}{auto_number}" # Cheia originală pentru date (ex: tip_auto1)
        var_key = f"{VAR_PREFIX}{auto_number}_{base_key}" # Cheia unică în app_instance.data_vars

        if var_key not in app_instance.data_vars:
            if key_template.startswith("bifa_") or \
               key_template.startswith("art_") or \
               key_template == "nota_vinovatie_sofer_autox" or \
               key_template.startswith("examinare_sig_") or \
               key_template == "examinare_vehicul_visiblex": # Adăugat pentru starea dropdown
                var = tk.IntVar(value=0)
            else:
                var = tk.StringVar()
            app_instance.data_vars[var_key] = var
        else:
            var = app_instance.data_vars[var_key]
        vehicle_vars[data_key] = var # Folosim cheia originală (cu index) pentru dict-ul local

    try:
        auto_frame.create_vehicle_ui_ctk(
            vehicle_scrollable_frame,
            auto_number,
            vehicle_vars
        )
        print(f"auto_frame.create_vehicle_ui_ctk apelat pentru Auto {auto_number}")
    except Exception as e:
         messagebox.showerror("Eroare Creare UI Auto", f"Nu s-a putut crea interfața pentru vehiculul {auto_number}:\n{e}")
         print(f"Eroare detaliată la creare UI auto {auto_number}:", file=sys.stderr)
         traceback.print_exc(file=sys.stderr)
         try: inner_tabview.delete(tab_name)
         except: pass
         return

    app_instance.auto_frames.append({"tab_name": tab_name, "scroll_frame": vehicle_scrollable_frame})

    if data_to_load:
        print(f"Încărcare date CTk pentru Vehiculul {auto_number}...")
        for key_template in DATA_KEYS_PER_AUTO:
            base_key = key_template[:-1] if key_template.endswith('x') else key_template
            data_key = f"{base_key}{auto_number}"
            var_key = f"{VAR_PREFIX}{auto_number}_{base_key}"

            if data_key in data_to_load and var_key in app_instance.data_vars:
                try:
                    target_var = app_instance.data_vars[var_key]
                    value_from_data = data_to_load[data_key]

                    if isinstance(target_var, tk.IntVar):
                        value_to_set = 1 if value_from_data else 0
                        target_var.set(value_to_set)
                    elif isinstance(target_var, tk.StringVar):
                        value_to_set = str(value_from_data) if value_from_data is not None else ""
                        target_var.set(value_to_set)
                except tk.TclError as e:
                    print(f"Avertisment: Nu s-a putut seta valoarea pentru {var_key} (cheie date: {data_key}): {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Eroare la încărcarea datei pentru {var_key} (cheie date: {data_key}): {e}", file=sys.stderr)

    inner_tabview.set(tab_name)


def get_data(app_instance, tab_frame=None, auto_frames_list=None):
    """Colectează datele de la toate vehiculele adăugate."""
    all_auto_data = {}
    num_autos = len(app_instance.auto_frames)
    data_vars = app_instance.data_vars
    print(f"Colectare date CTk pentru {num_autos} vehicule...")

    for i in range(1, num_autos + 1):
        for key_template in DATA_KEYS_PER_AUTO:
            base_key = key_template[:-1] if key_template.endswith('x') else key_template
            original_key = f"{base_key}{i}"
            var_key = f"{VAR_PREFIX}{i}_{base_key}"
            if var_key in data_vars:
                try:
                    all_auto_data[original_key] = data_vars[var_key].get()
                except Exception as e:
                    print(f"EROARE la citirea variabilei '{var_key}': {e}", file=sys.stderr)
                    all_auto_data[original_key] = f"EROARE_CITIRE_{var_key}"
            else:
                print(f"AVERTISMENT: Cheia variabilă '{var_key}' nu a fost găsită!", file=sys.stderr)
                all_auto_data[original_key] = f"CHEIE_LIPSĂ_{var_key}"
    return all_auto_data

def clear_dynamic_frames(tab_container, app_instance):
    """Șterge toate sub-tab-urile de vehicule."""
    print("Curățare cadre dinamice auto (CTk)...")
    inner_tabview = getattr(tab_container, 'inner_tabview', None)
    if not inner_tabview:
        print("Avertisment: Nu s-a găsit inner_tabview în containerul tab-ului auto.")
        return

    for item in list(app_instance.auto_frames):
        tab_name_to_delete = item["tab_name"]
        scroll_frame_to_destroy = item["scroll_frame"]
        try:
            print(f"  Ștergere tab: {tab_name_to_delete}")
            inner_tabview.delete(tab_name_to_delete)
            if scroll_frame_to_destroy and scroll_frame_to_destroy.winfo_exists():
                 scroll_frame_to_destroy.destroy()
        except Exception as e:
            print(f"Eroare la ștergerea tab-ului auto '{tab_name_to_delete}': {e}")

    app_instance.auto_frames.clear()

    keys_to_delete = [key for key in app_instance.data_vars if key.startswith(VAR_PREFIX)]
    print(f"  Se vor șterge {len(keys_to_delete)} variabile din data_vars...")
    for key in keys_to_delete:
        if key in app_instance.data_vars:
             del app_instance.data_vars[key]
    print("Cadrele dinamice auto au fost curățate (CTk).")

def load_data(app_instance, data_to_load):
    """Logica de încărcare este gestionată în AppWindow.load_data_into_ui."""
    pass

