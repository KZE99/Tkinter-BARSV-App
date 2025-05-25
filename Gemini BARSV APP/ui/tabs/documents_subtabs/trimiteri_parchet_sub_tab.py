# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței sub-tab-ului 'Trimiteri Parchet'
(Versiune CustomTkinter cu două coloane, descrieri complete și liste dinamice cu meniuri)
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, Menu as tkMenu

try:
    from core import utils
except ImportError:
    print("AVERTISMENT: Nu s-a putut importa core.utils în trimiteri_parchet_sub_tab (CTk).")
    class DummyUtils:
        def handle_romanian_characters_keypress(self, event): pass
    utils = DummyUtils()

SUB_VAR_PREFIX = "docs_tp_"

DISPLAY_DATA_KEYS_TP = [
    "display_tp_nr_penal", "display_tp_data_doc", "display_tp_nr_disp",
    "display_tp_sector", "display_tp_data_acc", "display_tp_loc_acc",
    "display_tp_articol_penal_principal",
    "display_tp_nr_victime_total", 
]
INPUT_DATA_KEYS_TP = [
    "tp_dosar_file", "tp_procuror_supraveghere",
    "tp_lucrator_repartizat", "tp_prejudiciu"
]
FISA_ARTICLES_DESC_KEY = SUB_VAR_PREFIX + "fisa_articles_text_descriptions"
LISTA_FAPTUITORI_KEY_DISPLAY = SUB_VAR_PREFIX + "lista_faptuitori_text_display" 
LISTA_VSG_KEY_DISPLAY = SUB_VAR_PREFIX + "lista_vsg_text_display" 


ARTICOLE_CP_CHOICES = [
    'art_334_1_capac', 'art_334_2_capac', 'art_334_3_capac', 'art_334_4_capac',
    'art_335_1_capac', 'art_335_2_capac', 'art_336_1_capac', 'art_336_1ind1_capac',
    'art_336_2_capac', 'art_337_capac', 'art_338_1_capac', 'art_338_2_capac'
]

ARTICOLE_CP_DESCRIPTIONS = {
    'art_334_1_capac': "Punerea în circulație sau conducerea unui vehicul neînmatriculat.",
    'art_334_2_capac': "Conducerea unui vehicul cu număr fals de înmatriculare.",
    'art_334_3_capac': "Tractarea unei remorci neînmatriculate/cu număr fals.",
    'art_334_4_capac': "Punerea în circulație a unui vehicul ale cărui plăcuțe au fost retrase.",
    'art_335_1_capac': "Conducerea unui vehicul fără permis de conducere.",
    'art_335_2_capac': "Conducerea unui vehicul având permisul necorespunzător categoriei/suspendat/anulat/retras.",
    'art_336_1_capac': "Conducerea pe drumurile publice a unui vehicul de către o persoană aflată sub influența băuturilor alcoolice.",
    'art_336_1ind1_capac': "Conducerea sub influența alcoolului (între 0.5 și 0.8 g/l alcool pur în sânge).",
    'art_336_2_capac': "Conducerea pe drumurile publice a unui vehicul de către o persoană aflată sub influența altor substanțe psihoactive.",
    'art_337_capac': "Refuzul sau sustragerea de la prelevarea de mostre biologice.",
    'art_338_1_capac': "Părăsirea locului accidentului fără încuviințarea poliției sau a procurorului.",
    'art_338_2_capac': "Modificarea stării locului accidentului sau ștergerea urmelor accidentului de circulație."
}


def create_trimiteri_parchet_content(parent_container, app_instance, checkbox_texts_dict):
    """ Populează containerul sub-tab-ului 'Trimiteri Parchet'. """
    parent_container.grid_columnconfigure(0, weight=1)
    parent_container.grid_rowconfigure(0, weight=1)

    main_content_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    main_content_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    main_content_frame.grid_columnconfigure(0, weight=3, minsize=700) 
    main_content_frame.grid_columnconfigure(1, weight=1, minsize=350) 
    main_content_frame.grid_rowconfigure(0, weight=1)

    # --- Coloana Stânga (Scrollabilă) ---
    scroll_area_stanga = ctk.CTkScrollableFrame(main_content_frame, label_text="Previzualizare Document și Fișă")
    scroll_area_stanga.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=0)
    doc_viewer_frame = scroll_area_stanga
    doc_viewer_frame.grid_columnconfigure(0, weight=1)

    # --- Coloana Dreapta (Pentru Selecții) ---
    frame_dreapta_selections = ctk.CTkFrame(main_content_frame, fg_color=("gray92", "gray17"), corner_radius=10)
    frame_dreapta_selections.grid(row=0, column=1, sticky="nsew", padx=(5,0), pady=0)
    frame_dreapta_selections.grid_columnconfigure(0, weight=1) 
    
    # --- Inițializare Variabile Tkinter și Liste Interne ---
    for key in INPUT_DATA_KEYS_TP:
        full_key = SUB_VAR_PREFIX + key
        app_instance.data_vars.setdefault(full_key, tk.StringVar())
    for key in DISPLAY_DATA_KEYS_TP:
        full_key = SUB_VAR_PREFIX + key
        app_instance.data_vars.setdefault(full_key, tk.StringVar(value="..."))

    if not hasattr(app_instance, 'selected_tp_articles_list'):
        app_instance.selected_tp_articles_list = []
    
    if not hasattr(app_instance, 'tp_selected_faptuitori'):
        app_instance.tp_selected_faptuitori = [] 
    if not hasattr(app_instance, 'tp_selected_vsg'):
        app_instance.tp_selected_vsg = []       

    app_instance.data_vars.setdefault(FISA_ARTICLES_DESC_KEY, tk.StringVar())
    fisa_articles_desc_var = app_instance.data_vars[FISA_ARTICLES_DESC_KEY]

    app_instance.data_vars.setdefault(LISTA_FAPTUITORI_KEY_DISPLAY, tk.StringVar(value="Niciun făptuitor selectat."))
    app_instance.data_vars.setdefault(LISTA_VSG_KEY_DISPLAY, tk.StringVar(value="Nicio persoană vătămată selectată."))

    text_trimitere_static_var = tk.StringVar()
    app_instance.data_vars.setdefault(SUB_VAR_PREFIX + "text_trimitere_static", text_trimitere_static_var)

    # --- Creare Widget-uri pentru Coloana Dreaptă ---
    
    # Secțiunea Articole
    lbl_articles_title = ctk.CTkLabel(frame_dreapta_selections, text="Articole Penale Suplimentare", font=ctk.CTkFont(weight="bold"))
    lbl_articles_title.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,2))
    articles_placeholder_container = ctk.CTkScrollableFrame(frame_dreapta_selections, label_text="")
    articles_placeholder_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,5))
    add_article_button_dreapta = ctk.CTkButton(frame_dreapta_selections, text="+ Adaugă Articol Penal", width=250, height=28)
    add_article_button_dreapta.grid(row=2, column=0, sticky="n", padx=10, pady=(0,10))

    # Secțiunea Făptuitori
    lbl_faptuitori_title = ctk.CTkLabel(frame_dreapta_selections, text="Făptuitori Selectați", font=ctk.CTkFont(weight="bold"))
    lbl_faptuitori_title.grid(row=3, column=0, sticky="ew", padx=10, pady=(10,2))
    faptuitori_placeholder_container = ctk.CTkScrollableFrame(frame_dreapta_selections, label_text="")
    faptuitori_placeholder_container.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0,5))
    add_faptuitor_button = ctk.CTkButton(frame_dreapta_selections, text="+ Adaugă Făptuitor", width=250, height=28)
    add_faptuitor_button.grid(row=5, column=0, sticky="n", padx=10, pady=(0,10))
    
    # Secțiunea Persoane Vătămate
    lbl_vsg_title = ctk.CTkLabel(frame_dreapta_selections, text="Persoane Vătămate Selectate", font=ctk.CTkFont(weight="bold"))
    lbl_vsg_title.grid(row=6, column=0, sticky="ew", padx=10, pady=(10,2))
    vsg_placeholder_container = ctk.CTkScrollableFrame(frame_dreapta_selections, label_text="")
    vsg_placeholder_container.grid(row=7, column=0, sticky="nsew", padx=10, pady=(0,5))
    add_vsg_button = ctk.CTkButton(frame_dreapta_selections, text="+ Adaugă Persoană Vătămată", width=250, height=28)
    add_vsg_button.grid(row=8, column=0, sticky="n", padx=10, pady=(0,10))

    frame_dreapta_selections.grid_rowconfigure(1, weight=1) 
    frame_dreapta_selections.grid_rowconfigure(4, weight=1) 
    frame_dreapta_selections.grid_rowconfigure(7, weight=1) 

    # --- Funcții Utilitare și Callback ---
    def get_var_value_or_default(key, default_value="..."):
        var = app_instance.data_vars.get(key)
        if var:
            val = var.get()
            if isinstance(val, str) and (not val.strip() or val.strip() == "..."):
                return default_value
            elif val is None: 
                return default_value
            return val
        return default_value

    def default_value_for_key(key_name, main_source_key=""):
        base_key_part = key_name.split('_')[-1] if '_' in key_name else key_name
        if "ziua" in base_key_part or "luna" in base_key_part: return "??"
        if "anul" in base_key_part: return "????"
        if "ora" in base_key_part and "display_tp_data_ora" not in main_source_key : return "??:??"
        return "..."

    def _get_all_available_persons_for_menu():
        persons = []

        # Colectează șoferii din auto_frame
        if hasattr(app_instance, 'auto_frames'):
            for auto_index, auto_data in enumerate(app_instance.auto_frames, start=1):
                nume = auto_data.get('nume_sofer', '')
                cnp = auto_data.get('cnp_sofer', 'N/A')
                if nume:
                    persons.append({
                        'id': f'auto_{auto_index}_sofer',
                        'display_text': f"{nume} (Șofer Auto {auto_index})",
                        'nume': nume,
                        'cnp': cnp,
                        'type': 'sofer',
                        'original_index': auto_index
                    })

        # Colectează victimele din victim_frames
        if hasattr(app_instance, 'victim_frames'):
            for victim_index, victim_frame in enumerate(app_instance.victim_frames, start=1):
                # Verifică dacă victim_frame este un widget sau un dicționar
                if isinstance(victim_frame, dict):  # Dacă este un dicționar
                    nume = victim_frame.get('nume_victima', '')
                    cnp = victim_frame.get('cnp_victima', 'N/A')
                elif hasattr(victim_frame, 'data'):  # Dacă este un widget cu atributul `data`
                    nume = victim_frame.data.get('nume_victima', '')
                    cnp = victim_frame.data.get('cnp_victima', 'N/A')
                else:
                    continue  # Dacă nu este niciunul dintre cazuri, treci la următorul

                if nume:
                    persons.append({
                        'id': f'victim_{victim_index}',
                        'display_text': f"{nume} (Victimă {victim_index})",
                        'nume': nume,
                        'cnp': cnp,
                        'type': 'victima',
                        'original_index': victim_index
                    })

        return persons
    
    def _get_prima_victima_relevanta():
        if app_instance.tp_selected_vsg:
            first_vsg = app_instance.tp_selected_vsg[0]
            return {'nume': first_vsg['nume'], 'cnp': first_vsg['cnp']}

        all_persons = _get_all_available_persons_for_menu() 
        for person in all_persons:
            if person['type'] == 'victima':
                return {'nume': person['nume'], 'cnp': person['cnp']}
            elif person['type'] == 'sofer':
                is_victima_sofer_var = app_instance.data_vars.get(f"auto_{person['original_index']}_bifa_victima_autox")
                is_victima_sofer = is_victima_sofer_var.get() == 1 if is_victima_sofer_var else False
                has_diag_var = app_instance.data_vars.get(f"auto_{person['original_index']}_diagnostic_sofer_autox")
                has_diag = False
                if has_diag_var:
                    diag_val = has_diag_var.get()
                    if diag_val and diag_val.strip() and diag_val.strip() != "...":
                        has_diag = True
                if is_victima_sofer or has_diag:
                    return {'nume': person['nume'], 'cnp': person['cnp']}
        return {'nume': "...", 'cnp': "..."}

    def _update_display_text_for_person_lists():
        fapt_display_list = [f"{p['nume']}, CNP {p['cnp']}" for p in app_instance.tp_selected_faptuitori]
        app_instance.data_vars[LISTA_FAPTUITORI_KEY_DISPLAY].set("\n".join(fapt_display_list) if fapt_display_list else "Niciun făptuitor selectat.")

        vsg_display_list = []
        for p in app_instance.tp_selected_vsg:
            text = f"{p['nume']}, CNP {p['cnp']}"
            if p.get('type') == 'sofer':
                 text += f" (conducător auto {p.get('original_index', '')})"
            elif p.get('type') == 'victima':
                 text += f" (victimă {p.get('original_index', '')})"
            vsg_display_list.append(text)
        app_instance.data_vars[LISTA_VSG_KEY_DISPLAY].set("\n".join(vsg_display_list) if vsg_display_list else "Nicio persoană vătămată selectată.")

    def _update_static_text_trimitere_and_fisa_articles(*args):
        nr_p_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_nr_penal")
        data_d_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_data_doc")
        data_a_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_data_acc")
        loc_a_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_loc_acc")
        sect_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_sector")
        art_princ_val = get_var_value_or_default(SUB_VAR_PREFIX + "display_tp_articol_penal_principal")

        info_victima_principala = _get_prima_victima_relevanta()
        nume_v_val = info_victima_principala['nume']
        cnp_v_val = info_victima_principala['cnp']
        
        text_intro_victima = "..."
        if nume_v_val and nume_v_val != "...":
            text_intro_victima = f"vătămarea corporală a numitului/ei {nume_v_val}, CNP {cnp_v_val}"
        else:
            text_intro_victima = "producerea de pagube materiale și/sau vătămarea corporală a uneia sau mai multor persoane"

        text_static_part1_content = (
            "      În conformitate cu prevederile art. 8 din Ordinul Comun al M.A.I. și P.Î.C.C.J. nr. 231/20.12.2024 – nr. 284/2024, "
            f"vă înaintăm alăturat procesul-verbal întocmit de organele de poliție din cadrul Brigăzii Rutiere, înregistrat la "
            f"această unitate de poliție sub nr. {nr_p_val} din {data_d_val} privind accidentul de circulație produs la data de {data_a_val} "
            f"în București, pe strada/ în intersecția {loc_a_val}, sector {sect_val}, soldat cu {text_intro_victima}; "
            f"având ca obiect infr. prev. și ped. de {art_princ_val} din C.P."
        )
        text_trimitere_static_var.set(text_static_part1_content + ".")

        descriptions = [art['text_long'] for art in app_instance.selected_tp_articles_list]
        fisa_articles_desc_var.set(" " + "; ".join(descriptions) if descriptions else "")
        _update_display_text_for_person_lists()

    def _add_person_to_list_and_display(person_data, target_list_attr_name, placeholder_container):
        internal_list = getattr(app_instance, target_list_attr_name)
        if any(p['id'] == person_data['id'] for p in internal_list):
            messagebox.showwarning("Persoană Duplicată", f"{person_data['nume']} este deja în această listă.")
            return
        internal_list.append(person_data)
        
        p_frame = ctk.CTkFrame(placeholder_container, fg_color=("gray85", "gray20"), corner_radius=6)
        p_frame.pack(side="top", fill="x", padx=2, pady=2)
        
        text_to_display = person_data['display_text']
        ctk.CTkLabel(p_frame, text=text_to_display, font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
        
        remove_btn = ctk.CTkButton(p_frame, text="X", width=18, height=18, fg_color="transparent", hover_color=("gray70","gray30"),
                                   command=lambda pd=person_data, la=target_list_attr_name, pf=p_frame: _remove_person_from_list(pd, la, pf))
        remove_btn.pack(side="right", padx=(0,3))
        
        _update_display_text_for_person_lists()
        _update_static_text_trimitere_and_fisa_articles() 

    def _remove_person_from_list(person_data_to_remove, target_list_attr_name, placeholder_frame):
        internal_list = getattr(app_instance, target_list_attr_name)
        setattr(app_instance, target_list_attr_name, [p for p in internal_list if p['id'] != person_data_to_remove['id']])
        placeholder_frame.destroy()
        _update_display_text_for_person_lists()
        _update_static_text_trimitere_and_fisa_articles()

    def _show_person_selection_menu(event_widget, target_list_attr_name_str, placeholder_container_widget):
        menu = tkMenu(frame_dreapta_selections, tearoff=0)
        all_persons = _get_all_available_persons_for_menu()
        current_selection_ids = [p['id'] for p in getattr(app_instance, target_list_attr_name_str)]
        available_to_add = [p for p in all_persons if p['id'] not in current_selection_ids]

        if not available_to_add:
            menu.add_command(label="Nicio persoană nouă disponibilă", state="disabled")
        else:
            for person in available_to_add:
                menu.add_command(label=person['display_text'], 
                                 command=lambda p_data=person: _add_person_to_list_and_display(p_data, target_list_attr_name_str, placeholder_container_widget))
        try:
            menu.tk_popup(event_widget.winfo_rootx(), event_widget.winfo_rooty() + event_widget.winfo_height())
        finally:
            menu.grab_release()

    def _remove_article_placeholder_ui(article_key, placeholder_frame): 
        placeholder_frame.destroy()
        app_instance.selected_tp_articles_list = [
            art for art in app_instance.selected_tp_articles_list if art['key'] != article_key
        ]
        _update_static_text_trimitere_and_fisa_articles()

    def _add_article_placeholder_ui(article_key, article_text_short, container_to_add): 
        if any(art['key'] == article_key for art in app_instance.selected_tp_articles_list):
            messagebox.showwarning("Articol Duplicat", f"Articolul '{article_text_short}' a fost deja adăugat.")
            return

        placeholder_frame = ctk.CTkFrame(container_to_add, fg_color=("gray80", "gray25"), corner_radius=6, height=20)
        placeholder_frame.pack(side="top", padx=2, pady=2, fill="x", anchor="n")

        ctk.CTkLabel(placeholder_frame, text=article_text_short, padx=5, font=ctk.CTkFont(size=11)).pack(side="left")
        remove_btn = ctk.CTkButton(placeholder_frame, text=" X ", width=18, height=18,
                                   fg_color="transparent", hover_color=("gray60", "gray40"), text_color=("black", "white"),
                                   command=lambda k=article_key, pf=placeholder_frame: _remove_article_placeholder_ui(k, pf))
        remove_btn.pack(side="right", padx=(0,2))

        article_description = ARTICOLE_CP_DESCRIPTIONS.get(article_key, article_text_short)
        app_instance.selected_tp_articles_list.append({'key': article_key, 'text_short': article_text_short, 'text_long': article_description, 'placeholder_frame': placeholder_frame})
        _update_static_text_trimitere_and_fisa_articles()

    def _show_article_menu_ui(event_widget, container_to_add_placeholders): 
        menu = tkMenu(frame_dreapta_selections, tearoff=0) 
        available_articles = {
            k: checkbox_texts_dict.get(k, k) for k in ARTICOLE_CP_CHOICES
            if k not in [art['key'] for art in app_instance.selected_tp_articles_list]
        }
        if not available_articles:
            menu.add_command(label="Niciun articol disponibil", state="disabled")
        else:
            for key, text in available_articles.items():
                menu.add_command(label=text, command=lambda k=key, t=text: _add_article_placeholder_ui(k, t, container_to_add_placeholders))
        try:
            menu.tk_popup(event_widget.winfo_rootx(), event_widget.winfo_rooty() + event_widget.winfo_height())
        finally:
            menu.grab_release()

    # --- Configurare Comenzi Butoane Coloana Dreapta ---
    add_article_button_dreapta.configure(command=lambda: _show_article_menu_ui(add_article_button_dreapta, articles_placeholder_container))
    add_faptuitor_button.configure(command=lambda: _show_person_selection_menu(add_faptuitor_button, 'tp_selected_faptuitori', faptuitori_placeholder_container))
    add_vsg_button.configure(command=lambda: _show_person_selection_menu(add_vsg_button, 'tp_selected_vsg', vsg_placeholder_container))


    # --- Funcții de Actualizare Display ---
    def _update_display_var(source_var_key_list, target_var_key, format_str="{0}", default_val="..."):
        target_var = app_instance.data_vars.get(target_var_key)
        if not target_var: return
        values = []
        for src_key in source_var_key_list:
            source_var = app_instance.data_vars.get(src_key)
            val = source_var.get() if source_var and source_var.get() else default_value_for_key(src_key, source_var_key_list[0] if source_var_key_list else "")
            values.append(str(val))
        try:
            target_var.set(format_str.format(*values))
        except IndexError:
            target_var.set(default_val)
        _update_static_text_trimitere_and_fisa_articles()

    def update_tp_data_doc(*args):
        zi = get_var_value_or_default("principal_ziua_doc", "??")
        luna = get_var_value_or_default("principal_luna_doc", "??")
        an = get_var_value_or_default("principal_anul_doc", "????")
        target_var = app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_doc")
        if target_var:
            target_var.set(f"{zi}.{luna}.{an}")
        _update_static_text_trimitere_and_fisa_articles()

    def update_tp_data_acc(*args):
        zi = get_var_value_or_default("principal_ziua_acc", "??")
        luna = get_var_value_or_default("principal_luna_acc", "??")
        an = get_var_value_or_default("principal_anul_acc", "????")
        target_var = app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_acc")
        if target_var:
            target_var.set(f"{zi}.{luna}.{an}")
        _update_static_text_trimitere_and_fisa_articles()
        
    # --- Adaugă Tracing ---
    source_target_map_tp = { 
        "principal_nr_penal": SUB_VAR_PREFIX + "display_tp_nr_penal",
        "principal_nr_disp": SUB_VAR_PREFIX + "display_tp_nr_disp",
        "principal_sector": SUB_VAR_PREFIX + "display_tp_sector",
        "principal_locul_accidentului": SUB_VAR_PREFIX + "display_tp_loc_acc",
        "principal_articol_penal": SUB_VAR_PREFIX + "display_tp_articol_penal_principal",
        "principal_nr_victime": SUB_VAR_PREFIX + "display_tp_nr_victime_total",
    }
    for source_key, target_key in source_target_map_tp.items():
        source_var = app_instance.data_vars.get(source_key)
        if source_var:
            source_var.trace_add("write", lambda *a, sk_list=[source_key], tk=target_key: _update_display_var(sk_list, tk))

    for k in ["principal_ziua_doc", "principal_luna_doc", "principal_anul_doc"]:
        var_to_trace = app_instance.data_vars.get(k)
        if var_to_trace: var_to_trace.trace_add("write", update_tp_data_doc)

    for k in ["principal_ziua_acc", "principal_luna_acc", "principal_anul_acc"]:
        var_to_trace = app_instance.data_vars.get(k)
        if var_to_trace: var_to_trace.trace_add("write", update_tp_data_acc)
    
    person_data_triggers = []
    max_autos = getattr(app_instance, 'max_supported_autos', 7) 
    max_victims = getattr(app_instance, 'max_supported_victims', 7)

    for i in range(1, max_autos + 1):
        person_data_triggers.extend([
            f"auto_{i}_nume_sofer_autox", f"auto_{i}_cnp_sofer_autox",
            f"auto_{i}_bifa_victima_autox", f"auto_{i}_diagnostic_sofer_autox",
            f"auto_{i}_bifa_vinovat_autox" # Este important pentru a re-evalua cine e victimă principală etc.
        ])
    for i in range(1, max_victims + 1):
        person_data_triggers.extend([
            f"victime_{i}_nume_victimax", f"victime_{i}_cnp_victimax"
        ])
    
    for key in person_data_triggers:
        var = app_instance.data_vars.get(key)
        if var: 
            var.trace_add("write", _update_static_text_trimitere_and_fisa_articles)


    # --- UI pentru Coloana Stânga (Document și Fișă) ---
    current_row_doc = 0
    ctk.CTkLabel(doc_viewer_frame, text="MINISTERUL AFACERILOR INTERNE,\nINSPECTORATUL GENERAL AL POLIŢIEI ROMÂNE,\nDIRECŢIA GENERALĂ DE POLIŢIE A MUNICIPIULUI BUCUREŞTI,\nBRIGADA RUTIERĂ,",
                 justify="center", font=ctk.CTkFont(size=10)).grid(row=current_row_doc, column=0, padx=5, pady=(5,10), sticky="ew"); current_row_doc +=1
    frame_nr_dosare_container = ctk.CTkFrame(doc_viewer_frame, fg_color="transparent")
    frame_nr_dosare_container.grid(row=current_row_doc, column=0, padx=5, pady=2, sticky="w"); current_row_doc +=1
    frame_dosar_p = ctk.CTkFrame(frame_nr_dosare_container, fg_color="transparent")
    frame_dosar_p.pack(side="top", anchor="w")
    ctk.CTkLabel(frame_dosar_p, text="Nr. dosar P: ").pack(side="left")
    ctk.CTkLabel(frame_dosar_p, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_nr_penal")).pack(side="left")
    ctk.CTkLabel(frame_dosar_p, text=" din ").pack(side="left")
    ctk.CTkLabel(frame_dosar_p, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_doc")).pack(side="left")
    frame_dosar_d = ctk.CTkFrame(frame_nr_dosare_container, fg_color="transparent")
    frame_dosar_d.pack(side="top", anchor="w", pady=(2,0))
    ctk.CTkLabel(frame_dosar_d, text="Nr. dosar D: ").pack(side="left")
    ctk.CTkLabel(frame_dosar_d, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_nr_disp")).pack(side="left")
    ctk.CTkLabel(frame_dosar_d, text=" din ").pack(side="left")
    ctk.CTkLabel(frame_dosar_d, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_doc")).pack(side="left")
    ctk.CTkLabel(doc_viewer_frame, text="Către,").grid(row=current_row_doc, column=0, padx=5, pady=(10,0), sticky="w"); current_row_doc +=1
    frame_parchet_dest = ctk.CTkFrame(doc_viewer_frame, fg_color="transparent")
    frame_parchet_dest.grid(row=current_row_doc, column=0, padx=5, pady=0, sticky="w")
    ctk.CTkLabel(frame_parchet_dest, text="PARCHETUL DE PE LÂNGĂ JUDECĂTORIA SECTORULUI ").pack(side="left")
    ctk.CTkLabel(frame_parchet_dest, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_sector")).pack(side="left")
    ctk.CTkLabel(frame_parchet_dest, text=" BUCUREȘTI").pack(side="left")
    current_row_doc +=1
    ctk.CTkLabel(doc_viewer_frame, textvariable=text_trimitere_static_var, wraplength=680, justify="left", anchor="w").grid(
        row=current_row_doc, column=0, padx=5, pady=5, sticky="ew"); current_row_doc +=1
    frame_dosar_file = ctk.CTkFrame(doc_viewer_frame, fg_color="transparent")
    frame_dosar_file.grid(row=current_row_doc, column=0, padx=5, pady=(5,2), sticky="w"); current_row_doc +=1
    ctk.CTkLabel(frame_dosar_file, text="Dosarul conține ").pack(side="left")
    ctk.CTkEntry(frame_dosar_file, width=50, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "tp_dosar_file")).pack(side="left", padx=2)
    ctk.CTkLabel(frame_dosar_file, text=" file.").pack(side="left")
    ctk.CTkLabel(doc_viewer_frame, text="Cu stimă,", anchor="w").grid(row=current_row_doc, column=0, padx=5, pady=(10,0), sticky="w"); current_row_doc +=1
    ctk.CTkLabel(doc_viewer_frame, text="Î/ŞEFUL BRIGĂZII RUTIERE,\nComisar-şef de poliţie\nVLĂȘCEANU IONUȚ",
                 justify="left", anchor="w").grid(row=current_row_doc, column=0, padx=5, pady=(5,10), sticky="w"); current_row_doc +=1
    ctk.CTkFrame(doc_viewer_frame, height=2, fg_color="gray50").grid(row=current_row_doc, column=0, pady=10, sticky="ew"); current_row_doc +=1

    # --- Fișa Infracțiunii ---
    frame_fisa = ctk.CTkFrame(doc_viewer_frame, fg_color="transparent")
    frame_fisa.grid(row=current_row_doc, column=0, padx=0, pady=10, sticky="ew")
    frame_fisa.columnconfigure(1, weight=1)
    ctk.CTkLabel(frame_fisa, text="FIȘA INFRACȚIUNII SESIZATE", font=ctk.CTkFont(weight="bold", size=14)).grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
    r_fisa = 1
    ctk.CTkLabel(frame_fisa, text="PROCURORUL DE SUPRAVEGHERE:").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkEntry(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "tp_procuror_supraveghere")).grid(row=r_fisa, column=1, padx=10, pady=2, sticky="ew"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, text="LUCRĂTORUL CĂRUIA I S-A REPARTIZAT LUCRAREA:").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkEntry(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "tp_lucrator_repartizat")).grid(row=r_fisa, column=1, padx=10, pady=2, sticky="ew"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, text="ORGANUL PRIM SESIZAT ȘI DATA SESIZĂRII: Proces Verbal Sesizare –").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_doc")).grid(row=r_fisa, column=1, padx=10, pady=2, sticky="w"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, text="DATA SĂVÂRȘIRII FAPTEI:").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_acc")).grid(row=r_fisa, column=1, padx=10, pady=2, sticky="w"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, text="DATA Î.U.P. IN REM:").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkLabel(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_data_doc")).grid(row=r_fisa, column=1, padx=10, pady=2, sticky="w"); r_fisa+=1

    frame_infractiune_fisa_container = ctk.CTkFrame(frame_fisa, fg_color="transparent")
    frame_infractiune_fisa_container.grid(row=r_fisa, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    frame_text_prefix_infractiune = ctk.CTkFrame(frame_infractiune_fisa_container, fg_color="transparent")
    frame_text_prefix_infractiune.pack(side="top", fill="x", anchor="w") 
    ctk.CTkLabel(frame_text_prefix_infractiune, text="INFRACȚIUNE (încadrare juridică): vătămarea corporală din culpă a ").pack(side="left")
    ctk.CTkLabel(frame_text_prefix_infractiune, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "display_tp_nr_victime_total")).pack(side="left")
    ctk.CTkLabel(frame_text_prefix_infractiune, text=" persoane;").pack(side="left")
    lbl_descrieri_articole = ctk.CTkLabel(frame_infractiune_fisa_container,
                                           textvariable=fisa_articles_desc_var,
                                           wraplength=650, justify="left", anchor="w")
    lbl_descrieri_articole.pack(side="top", fill="x", anchor="w", pady=(2,0))
    r_fisa+=1

    ctk.CTkLabel(frame_fisa, text="FĂPTUITOR(I) SELECTAȚI:", font=ctk.CTkFont(weight="bold")).grid(row=r_fisa, column=0, padx=10, pady=(5,0), sticky="w"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, textvariable=app_instance.data_vars.get(LISTA_FAPTUITORI_KEY_DISPLAY), wraplength=680, justify="left", anchor="nw").grid(row=r_fisa, column=0, columnspan=2, padx=10, pady=2, sticky="ew"); r_fisa+=1
    
    ctk.CTkLabel(frame_fisa, text="PERSOANE VĂTĂMATE SELECTATE:", font=ctk.CTkFont(weight="bold")).grid(row=r_fisa, column=0, padx=10, pady=(5,0), sticky="w"); r_fisa+=1
    ctk.CTkLabel(frame_fisa, textvariable=app_instance.data_vars.get(LISTA_VSG_KEY_DISPLAY), wraplength=680, justify="left", anchor="nw").grid(row=r_fisa, column=0, columnspan=2, padx=10, pady=2, sticky="ew"); r_fisa+=1
    
    ctk.CTkLabel(frame_fisa, text="PREJUDICIU:").grid(row=r_fisa, column=0, padx=10, pady=2, sticky="w")
    ctk.CTkEntry(frame_fisa, textvariable=app_instance.data_vars.get(SUB_VAR_PREFIX + "tp_prejudiciu")).grid(row=r_fisa, column=1, padx=10, pady=(2,10), sticky="ew")


    # --- Inițializare Finală și Stocare Referințe ---
    _update_static_text_trimitere_and_fisa_articles() 
    
    for sk, tk_key in source_target_map_tp.items():
        var_to_init = app_instance.data_vars.get(sk)
        if var_to_init and get_var_value_or_default(sk, ""): 
             _update_display_var([sk], tk_key) 
    
    if any(get_var_value_or_default(k, "") for k in ["principal_ziua_doc", "principal_luna_doc", "principal_anul_doc"]):
        update_tp_data_doc()
    if any(get_var_value_or_default(k, "") for k in ["principal_ziua_acc", "principal_luna_acc", "principal_anul_acc"]):
        update_tp_data_acc()

    app_instance._tp_update_texts_callback_ref = _update_static_text_trimitere_and_fisa_articles
    app_instance.articles_placeholder_container_dreapta_ref = articles_placeholder_container 
    app_instance._tp_add_article_placeholder_ref = lambda key, short_text: _add_article_placeholder_ui(key, short_text, articles_placeholder_container) 

    app_instance.faptuitori_placeholder_container_ref = faptuitori_placeholder_container 
    app_instance.vsg_placeholder_container_ref = vsg_placeholder_container            
    app_instance._tp_get_all_available_persons_ref = _get_all_available_persons_for_menu 
    app_instance.tp_add_faptuitor_ref = lambda pd: _add_person_to_list_and_display(pd, 'tp_selected_faptuitori', faptuitori_placeholder_container)
    app_instance.tp_add_vsg_ref = lambda pd: _add_person_to_list_and_display(pd, 'tp_selected_vsg', vsg_placeholder_container)


def get_data(app_instance):
    data = {}
    data_vars = app_instance.data_vars
    for key in INPUT_DATA_KEYS_TP:
        full_key = SUB_VAR_PREFIX + key
        var = data_vars.get(full_key)
        data[key] = var.get() if var else ""
    for article_key_template in ARTICOLE_CP_CHOICES:
        data[article_key_template] = 0
    if hasattr(app_instance, 'selected_tp_articles_list'):
        for selected_article in app_instance.selected_tp_articles_list:
            if selected_article['key'] in data:
                data[selected_article['key']] = 1
    
    fisa_desc_var = data_vars.get(FISA_ARTICLES_DESC_KEY)
    data["tp_fisa_articles_text_descriptions"] = fisa_desc_var.get() if fisa_desc_var else ""
    
    data["tp_selected_faptuitori_data"] = getattr(app_instance, 'tp_selected_faptuitori', [])
    data["tp_selected_vsg_data"] = getattr(app_instance, 'tp_selected_vsg', [])
        
    data[LISTA_FAPTUITORI_KEY_DISPLAY.replace(SUB_VAR_PREFIX, "")] = data_vars.get(LISTA_FAPTUITORI_KEY_DISPLAY, tk.StringVar()).get()
    data[LISTA_VSG_KEY_DISPLAY.replace(SUB_VAR_PREFIX, "")] = data_vars.get(LISTA_VSG_KEY_DISPLAY, tk.StringVar()).get()
    
    return data

def load_data(app_instance, data_to_load, checkbox_texts_dict=None):
    data_vars = app_instance.data_vars
    for key in INPUT_DATA_KEYS_TP:
        full_key = SUB_VAR_PREFIX + key
        if key in data_to_load and full_key in data_vars:
            var_to_set = data_vars[full_key]
            if isinstance(var_to_set, tk.StringVar):
                var_to_set.set(str(data_to_load[key]) if data_to_load[key] is not None else "")

    # Încărcare articole CP
    if hasattr(app_instance, 'articles_placeholder_container_dreapta_ref') and \
       hasattr(app_instance, '_tp_add_article_placeholder_ref') and \
       checkbox_texts_dict:
        container_ref = app_instance.articles_placeholder_container_dreapta_ref 
        for widget in list(container_ref.winfo_children()):
            widget.destroy()
        if hasattr(app_instance, 'selected_tp_articles_list'):
            app_instance.selected_tp_articles_list.clear()
        else:
            app_instance.selected_tp_articles_list = []
        add_article_func = app_instance._tp_add_article_placeholder_ref
        for article_key in ARTICOLE_CP_CHOICES:
            if data_to_load.get(article_key) == 1 or str(data_to_load.get(article_key)) == "1":
                article_short_text = checkbox_texts_dict.get(article_key, article_key)
                add_article_func(article_key, article_short_text)
    
    # Încărcare făptuitori și VSG selectați
    all_persons_available_for_load = []
    if hasattr(app_instance, '_tp_get_all_available_persons_ref'):
        all_persons_available_for_load = app_instance._tp_get_all_available_persons_ref()
    else:
        print("Avertisment load_data: _tp_get_all_available_persons_ref nu este definit în app_instance.")


    if hasattr(app_instance, 'tp_add_faptuitor_ref') and hasattr(app_instance, 'faptuitori_placeholder_container_ref'):
        fapt_container_ref = app_instance.faptuitori_placeholder_container_ref
        for widget in list(fapt_container_ref.winfo_children()): 
            widget.destroy()
        app_instance.tp_selected_faptuitori = [] 
        
        selected_faptuitori_data_from_load = data_to_load.get("tp_selected_faptuitori_data", [])
        for person_data_saved in selected_faptuitori_data_from_load:
            actual_person_data = next((p for p in all_persons_available_for_load if p.get('id') == person_data_saved.get('id')), person_data_saved)
            if actual_person_data and actual_person_data.get('id'):
                if 'display_text' not in actual_person_data and actual_person_data.get('nume'):
                    type_prefix = ""
                    if actual_person_data.get('type') == 'sofer':
                        type_prefix = f" (Șofer {actual_person_data.get('original_index', '')})"
                    elif actual_person_data.get('type') == 'victima':
                        type_prefix = f" (Victimă {actual_person_data.get('original_index', '')})"
                    actual_person_data['display_text'] = f"{actual_person_data['nume']}{type_prefix}"
                app_instance.tp_add_faptuitor_ref(actual_person_data)

    if hasattr(app_instance, 'tp_add_vsg_ref') and hasattr(app_instance, 'vsg_placeholder_container_ref'):
        vsg_container_ref = app_instance.vsg_placeholder_container_ref
        for widget in list(vsg_container_ref.winfo_children()): 
            widget.destroy()
        app_instance.tp_selected_vsg = [] 
        selected_vsg_data_from_load = data_to_load.get("tp_selected_vsg_data", [])
        for person_data_saved in selected_vsg_data_from_load:
            actual_person_data = next((p for p in all_persons_available_for_load if p.get('id') == person_data_saved.get('id')), person_data_saved)
            if actual_person_data and actual_person_data.get('id'):
                if 'display_text' not in actual_person_data and actual_person_data.get('nume'):
                    type_prefix = ""
                    if actual_person_data.get('type') == 'sofer':
                        type_prefix = f" (Șofer {actual_person_data.get('original_index', '')})"
                    elif actual_person_data.get('type') == 'victima':
                        type_prefix = f" (Victimă {actual_person_data.get('original_index', '')})"
                    actual_person_data['display_text'] = f"{actual_person_data['nume']}{type_prefix}"
                app_instance.tp_add_vsg_ref(actual_person_data)

    # Forțează actualizarea finală a tuturor textelor
    if hasattr(app_instance, '_tp_update_texts_callback_ref'):
        app_instance._tp_update_texts_callback_ref()