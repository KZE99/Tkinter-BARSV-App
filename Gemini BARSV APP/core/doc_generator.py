# -*- coding: utf-8 -*-
"""
Modul pentru generarea documentelor .docx pe baza șabloanelor și datelor din UI.
"""

import os
from pathlib import Path
from tkinter import filedialog, messagebox
from docxtpl import DocxTemplate

# --- Configurare ---

# Definește calea relativă către directorul cu șabloane
# Presupune că 'core' și 'templates' sunt în directorul rădăcină al proiectului
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
    TEMPLATE_DIR = BASE_DIR / "templates"
    if not TEMPLATE_DIR.is_dir():
        # Caută alternativ în directorul curent (util dacă rulat din rădăcină)
        TEMPLATE_DIR = Path.cwd() / "templates"
        if not TEMPLATE_DIR.is_dir():
             raise FileNotFoundError("Directorul 'templates' nu a fost găsit.")
except NameError:
    # Fallback dacă __file__ nu este definit (ex: rulare interactivă)
    TEMPLATE_DIR = Path("templates")
    if not TEMPLATE_DIR.is_dir():
         raise FileNotFoundError("Directorul 'templates' nu a fost găsit.")


# Placeholder pentru câmpurile goale în documente
PLACEHOLDER = '. . . . . . . . . . . . . . . . . . . . . . '

# Maparea dintre numele șablonului (fără extensie) și cheia checkbox-ului din UI
# IMPORTANT: Cheile trebuie să corespundă exact cu cele definite în UI (documents_tab.py)
TEMPLATE_CHECKBOX_MAPPING = {
    'Raport_retinere_sofer1': 'raport_retinere_sofer_autox1', # Cheia din UI
    'Raport_retinere_sofer2': 'raport_retinere_sofer_autox2',
    'Raport_retinere_sofer3': 'raport_retinere_sofer_autox3',
    'Raport_retinere_sofer4': 'raport_retinere_sofer_autox4',
    'Raport_retinere_sofer5': 'raport_retinere_sofer_autox5',
    'Raport_retinere_sofer6': 'raport_retinere_sofer_autox6',

    'Trimitere Parchet - Autovatamare Sofer': 'trimitere_parchet_sofer1',
    'Trimitere Parchet - Auto 2 Victime': 'trimitere_parchet_auto2victime',
    'Trimitere Parchet - Auto 3 Victime': 'trimitere_parchet_auto3victime',
    'Trimitere Parchet - 2 Auto Sofer 2': 'trimitere_parchet2auto_victima_sofer2',
    "Trimitere Parchet - Auto - Pieton": "trimitere_parchet_auto1victima",

    "Nota_vinovatie_template_pieton1": "nota_vinovatie_victimax1",
    "Nota_vinovatie_template_pieton2": "nota_vinovatie_victimax2",
    "Nota_vinovatie_template_pieton3": "nota_vinovatie_victimax3",
    "Nota_vinovatie_template_pieton4": "nota_vinovatie_victimax4",
    "Nota_vinovatie_template_sofer1": "nota_vinovatie_sofer_autox1",
    "Nota_vinovatie_template_sofer2": "nota_vinovatie_sofer_autox2",
    "Nota_vinovatie_template_sofer3": "nota_vinovatie_sofer_autox3",
    "Nota_vinovatie_template_sofer4": "nota_vinovatie_sofer_autox4",
    "Nota_vinovatie_template_sofer5": "nota_vinovatie_sofer_autox5",
    "Nota_vinovatie_template_sofer6": "nota_vinovatie_sofer_autox6",

    "#Ordonanta_IUP_Template": "Ordonanta_IUP_Basic",
    "Ordonanta_IUP_Alcool": "Ordonanta_IUP_Alcool",
    "Ordonanta_IUP_Droguri": "Ordonanta_IUP_Droguri",
    "Ordonanta_IUP_fara_pc": "Ordonanta_IUP_fara_pc",
    "Ordonanta_IUP_mort": "Ordonanta_IUP_mort",
    "Ordonanta_IUP_mutare_masina": "Ordonanta_IUP_mutare_masina",
    "Ordonanta_IUP_parasire": "Ordonanta_IUP_parasire",
    "Ordonanta_IUP_pc_suspendat": "Ordonanta_IUP_pc_suspendat",

    "Anexa 2 - auto_bicicleta - Biciclist 1 vinovat": "Anexa2_auto_bicicleta",
    "Anexa 2 - auto_trotineta - trotineta 1 vinovat": "Anexa2_auto_trotineta",
    "Anexa 2 - 2 auto - Auto1 vinovat": "Anexa 2 - 2 auto",
    "Anexa 2 - 3 auto - Auto1 vinovat": "Anexa 2 - 3 auto",
    "Anexa 2 - 4 auto - Auto1 vinovat": "Anexa 2 - 4 auto",
    "Anexa 2 - 5 auto - Auto1 vinovat": "Anexa 2 - 5 auto",
    "Anexa 2 - 6 auto - Auto1 vinovat": "Anexa 2 - 6 auto",

    "#Ordonanta_CFL_Template": "Ordonanta_CFL_Basic",
    "Ordonanta_CFL_Alcool": "Ordonanta_CFL_Alcool",
    "Ordonanta_CFL_AN_mutare_masina": "Ordonanta_CFL_mutare_masina",
    "Ordonanta_CFL_AN_parasire": "Ordonanta_CFL_parasire",
    "Ordonanta_CFL_droguri": "Ordonanta_CFL_droguri",
    "Ordonanta_CFL_fara_pc": "Ordonanta_CFL_fara_pc",
    "Ordonanta_CFL_mort": "Ordonanta_CFL_mort",
    "Ordonanta_CFL_pc_suspendat": "Ordonanta_CFL_pc_suspendat",

    "#Template_CFL_1_auto": "CFL_1auto_Basic",
    "#Template_CFL_TEST": "CFL_2auto_Basic", # Probabil identic cu următorul?
    "#Template_CFL_2_auto": "CFL_2auto_Basic",
    "#Template_CFL_3_auto": "CFL_3auto_Basic",
    "#Template_CFL_4_auto": "CFL_4auto_Basic",
    "#Template_CFL_5_auto": "CFL_5auto_Basic",
    "#Template_CFL_6_auto": "CFL_6auto_Basic",

    "PV fara CFL1": "PV_fara_CFL1",

    'FISA EAC DOCX - auto1_victime1si2': 'eac_auto1_2victime',
    'FISA EAC DOCX - auto3si4': 'eac_auto3si4',
    'FISA EAC DOCX - auto1si2': 'eac_auto1si2',
    'FISA EAC Primele 2 Pagini': 'eac_primele2pagini',
    'FISA EAC DOCX - victime1si2': 'eac_victime_1si2',
    'FISA EAC DOCX - victime3si4': 'eac_victime_3si4',

    'Pagina Caiet - Doc Extra 1 - TEST': 'doc_extra1', # Posibil duplicat?
    'Pagina Caiet - Doc Extra 1': 'doc_extra1',
    'Autoriaztii de Reparatii - Doc Extra 3': 'doc_extra3',

    'Nota Telex -  (1) - Art. 54_1': 'key_Nota Telex -  (1) - Art. 54_1',
    'Nota Telex -  (1) - Art. 54_1 + date auto': 'key_Nota Telex -  (1) - Art. 54_1 + date auto',
    'Nota Telex -  (2) - Art. 51': 'key_Nota Telex -  (2) - Art. 51',
    'Nota Telex -  (2) - Art. 51 + date auto': 'key_Nota Telex -  (2) - Art. 51 + date auto',
    'Nota Telex -  (7) - Art. 57_2': 'key_Nota Telex -  (7) - Art. 57_2',
    'Nota Telex -  (7) - Art. 57_2 + date auto': 'key_Nota Telex -  (7) - Art. 57_2 + date auto',
    'Nota Telex -  (8) - Art. 59_2': 'key_Nota Telex -  (8) - Art. 59_2',
    'Nota Telex -  (8) - Art. 59_2 + date auto': 'key_Nota Telex -  (8) - Art. 59_2 + date auto',
    'Nota Telex -  (6) - Art. 60': 'key_Nota Telex -  (6) - Art. 60',
    'Nota Telex -  (3) - Art. 54_1 cu pieton': 'key_Nota Telex -  (3) - Art. 54_1 cu pieton',
    'Nota Telex -  (5) - Art. 167_1_D': 'key_Nota Telex -  (5) - Art. 167_1_D',
    'Nota Telex -  (4) - Art. 135_H': 'key_Nota Telex -  (4) - Art. 135_H',
}

# --- Funcții Helper ---

def _prepare_context(data):
    """
    Pregătește dicționarul 'context' pentru randarea șabloanelor.

    Adaugă chei dinamice și valori implicite pentru câmpurile lipsă.

    Args:
        data (dict): Dicționarul cu datele brute preluate din UI.

    Returns:
        dict: Dicționarul context pregătit pentru docxtpl.
    """
    context = data.copy() # Creează o copie pentru a nu modifica dicționarul original

    # Extrage numărul curent de victime și auto (presupunând că sunt în 'data')
    # Dacă nu sunt, va trebui să le obținem altfel (ex: argumente separate)
    victim_count = int(data.get('victim_count', 0)) # Default la 0 dacă lipsește
    auto_number = int(data.get('auto_number', 0))   # Default la 0 dacă lipsește

    # --- Adaugă valori implicite și chei dinamice ---

    # Exemplu pentru victime (se va extinde pentru toate câmpurile necesare)
    for i in range(1, victim_count + 1):
        context[f'ok_nume_victimax{i}'] = data.get(f'nume_victimax{i}', PLACEHOLDER)
        context[f'ok_cnp_victimax{i}'] = data.get(f'cnp_victimax{i}', PLACEHOLDER)
        context[f'ok_adresa_victimax{i}'] = data.get(f'adresa_victimax{i}', PLACEHOLDER)
        context[f'ok_cetatenie_victimax{i}'] = data.get(f'cetatenie_victimax{i}', PLACEHOLDER)
        context[f'ok_tel_victimax{i}'] = data.get(f'tel_victimax{i}', PLACEHOLDER)
        context[f'ok_calitate_victimax{i}'] = data.get(f'calitate_victimax{i}', PLACEHOLDER)
        context[f'ok_diagnostic_victimax{i}'] = data.get(f'diagnostic_victimax{i}', PLACEHOLDER)
        # context[f'ok_nota_vinovatie_victimax{i}'] = data.get(f'nota_vinovatie_victimax{i}', False) # Valoare booleană
        context[f'ok_articol_victimax{i}'] = data.get(f'articol_victimax{i}', PLACEHOLDER)

        # JustText (texte condiționale pentru Pagina Caiet, etc.)
        has_victim_data = bool(data.get(f'nume_victimax{i}'))
        context[f'justtext_nr_victimax{i}'] = f'Nr. {i}' if has_victim_data else ''
        context[f'justtext_cnp_victimax{i}'] = ', CNP ' if has_victim_data else ''
        context[f'justtext_domiciliu_victimax{i}'] = 'Domiciliu: ' if has_victim_data else ''
        context[f'justtext_tel_victimax{i}'] = ', Tel.' if has_victim_data else ''
        context[f'justtext_articol_victimax{i}'] = ', Articol: ' if has_victim_data and data.get(f'articol_victimax{i}') else ''
        context[f'justtext_diagnostic_victimax{i}'] = 'Diagnostic: ' if has_victim_data and data.get(f'diagnostic_victimax{i}') else ''


    # Exemplu pentru auto/șoferi (se va extinde similar)
    for i in range(1, auto_number + 1):
        # Date vehicul
        context[f'ok_tip_autox{i}'] = data.get(f'tip_autox{i}', PLACEHOLDER)
        context[f'ok_marca_autox{i}'] = data.get(f'marca_autox{i}', PLACEHOLDER)
        context[f'ok_nr_autox{i}'] = data.get(f'nr_autox{i}', PLACEHOLDER)
        context[f'ok_VIN_autox{i}'] = data.get(f'VIN_autox{i}', PLACEHOLDER)
        context[f'ok_culoare_autox{i}'] = data.get(f'culoare_autox{i}', PLACEHOLDER)
        context[f'ok_proprietar_autox{i}'] = data.get(f'proprietar_autox{i}', PLACEHOLDER)
        context[f'ok_sediu_autox{i}'] = data.get(f'sediu_autox{i}', PLACEHOLDER)
        context[f'ok_utilizator_autox{i}'] = data.get(f'utilizator_autox{i}', PLACEHOLDER)
        context[f'ok_sediu_util_autox{i}'] = data.get(f'sediu_util_autox{i}', PLACEHOLDER)
        context[f'ok_tara_autox{i}'] = data.get(f'tara_autox{i}', PLACEHOLDER)
        context[f'ok_an_fabricatie_autox{i}'] = data.get(f'an_fabricatie_autox{i}', PLACEHOLDER)
        context[f'ok_itp_autox{i}'] = data.get(f'itp_autox{i}', PLACEHOLDER)
        context[f'ok_rca_autox{i}'] = data.get(f'rca_autox{i}', PLACEHOLDER)
        context[f'ok_serie_rca_autox{i}'] = data.get(f'serie_rca_autox{i}', PLACEHOLDER)
        context[f'ok_inceput_rca_autox{i}'] = data.get(f'inceput_rca_autox{i}', PLACEHOLDER)
        context[f'ok_sfarsit_rca_autox{i}'] = data.get(f'sfarsit_rca_autox{i}', PLACEHOLDER)

        # Date șofer
        context[f'ok_nume_sofer_autox{i}'] = data.get(f'nume_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_cnp_sofer_autox{i}'] = data.get(f'cnp_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_adresa_sofer_autox{i}'] = data.get(f'adresa_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_cetatenie_sofer_autox{i}'] = data.get(f'cetatenie_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_nrpc_sofer_autox{i}'] = data.get(f'nrpc_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_catpc_sofer_autox{i}'] = data.get(f'catpc_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_vechime_pc_sofer_autox{i}'] = data.get(f'vechime_pc{i}', PLACEHOLDER) # Ajustat cheia dacă e necesar
        context[f'ok_atestat_sofer_autox{i}'] = data.get(f'atestat_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_data_atestat_sofer_autox{i}'] = data.get(f'data_atestat_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_angajat_sofer_autox{i}'] = data.get(f'angajat_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_functie_sofer_autox{i}'] = data.get(f'functie_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_tel_sofer_autox{i}'] = data.get(f'tel_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_calitate_sofer_autox{i}'] = data.get(f'calitate_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_diagnostic_sofer_autox{i}'] = data.get(f'diagnostic_sofer_autox{i}', PLACEHOLDER)

        # Testări
        context[f'ok_etilo_autox{i}'] = data.get(f'etilo_autox{i}', PLACEHOLDER)
        context[f'ok_serie_etilo_autox{i}'] = data.get(f'serie_etilo_autox{i}', PLACEHOLDER)
        context[f'ok_pozitie_etilo_autox{i}'] = data.get(f'pozitie_etilo_autox{i}', PLACEHOLDER)
        context[f'ok_rezultat_etilo_autox{i}'] = data.get(f'rezultat_etilo_autox{i}', PLACEHOLDER)
        context[f'ok_drugtest_autox{i}'] = data.get(f'drugtest_autox{i}', PLACEHOLDER)
        context[f'ok_serie_drugtest_autox{i}'] = data.get(f'serie_drugtest_autox{i}', PLACEHOLDER)
        context[f'ok_pozitie_drugtest_autox{i}'] = data.get(f'pozitie_drugtest_autox{i}', PLACEHOLDER)
        context[f'ok_rezultat_drugtest_autox{i}'] = data.get(f'rezultat_drugtest_autox{i}', PLACEHOLDER)
        context[f'ok_droguri_drugtest_autox{i}'] = data.get(f'droguri_drugtest_autox{i}', PLACEHOLDER) # Cheia corectă? Verificați UI.
        context[f'ok_inml_autox{i}'] = data.get(f'inml_autox{i}', PLACEHOLDER)
        context[f'ok_sigiliu_inml_autox{i}'] = data.get(f'sigiliu_inml_autox{i}', PLACEHOLDER)

        # Texte lungi
        context[f'ok_text_declaratie_sofer_autox{i}'] = data.get(f'text_declaratie_sofer_autox{i}', PLACEHOLDER)
        context[f'ok_text_pozitie_autox{i}'] = data.get(f'text_pozitie_autox{i}', PLACEHOLDER)
        context[f'ok_text_avarii_autox{i}'] = data.get(f'text_avarii_autox{i}', PLACEHOLDER)

        # Adăugare logică complexă pentru `cfl_date_sofer_autox{i}`, `cfl_date_bici_autox{i}`, etc.
        # Aceasta necesită o implementare atentă, similară cu cea din PySimpleGUI,
        # verificând tipul vehiculului, dacă șoferul e angajat, are atestat etc.
        # și construind string-ul corespunzător.
        # Exemplu simplificat (necesită extindere):
        is_driver = bool(data.get(f'nume_sofer_autox{i}'))
        vehicle_type = data.get(f'tip_autox{i}', '')
        is_employed = bool(data.get(f'angajat_sofer_autox{i}'))
        has_certificate = bool(data.get(f'atestat_sofer_autox{i}'))

        if is_driver:
            if vehicle_type in ('Bicicletă', 'Trotinetă electrică','Tracțiune animală'):
                 context[f'cfl_date_bici_autox{i}'] = f"● {data.get(f'nume_sofer_autox{i}', '')}, CNP {data.get(f'cnp_sofer_autox{i}', '')}..." # Adaugă restul detaliilor
                 context[f'cfl_date_sofer_autox{i}'] = "" # Golește cealaltă variantă
            else:
                 context[f'cfl_date_sofer_autox{i}'] = f"● {data.get(f'nume_sofer_autox{i}', '')}, CNP {data.get(f'cnp_sofer_autox{i}', '')}..." # Adaugă restul detaliilor
                 context[f'cfl_date_bici_autox{i}'] = "" # Golește cealaltă variantă
                 # Aici se poate adăuga logica pentru atestat/angajat
        else:
             context[f'cfl_date_sofer_autox{i}'] = ""
             context[f'cfl_date_bici_autox{i}'] = ""

        # ... continuă pentru toate celelalte chei dinamice și 'justtext' ...

    # Adaugă alte chei necesare care nu sunt direct din UI sau sunt calculate
    # Exemplu:
    context['articol_penal'] = data.get('articol_penal', 'art. 196 alin. 2 și 3') # Valoare default

    # ... adaugă aici restul logicii de pregătire a contextului ...

    # Înlocuiește valorile None cu string gol sau placeholder
    for key, value in context.items():
        if value is None:
            context[key] = '' # Sau PLACEHOLDER dacă preferi

    return context

# --- Funcția Principală ---

def generate_documents(values):
    """
    Generează documentele .docx selectate de utilizator.

    Args:
        values (dict): Dicționar cu toate datele colectate din interfața Tkinter.
                       Se așteaptă ca valorile booleene de la Checkbuttons să fie 0 sau 1.
                       Se așteaptă să conțină 'victim_count' și 'auto_number'.
    """
    print("Inițiere generare documente...") # Mesaj de depanare
    # print("Date primite:", values) # Atenție: Poate afișa date sensibile

    # 1. Obține folderul destinație
    selected_folder = filedialog.askdirectory(
        title="Selectați folderul pentru salvarea documentelor"
    )
    if not selected_folder:
        messagebox.showwarning("Anulat", "Operațiunea de generare a fost anulată.")
        return

    destination_folder = Path(selected_folder)

    # 2. Creează subfolderul specific (bazat pe nr_penal)
    nr_penal = values.get("nr_penal", "Dosar_Necunoscut")
    if not nr_penal: # Verifică dacă nr_penal este gol
        nr_penal = "Dosar_Fara_Numar"

    output_folder_path = destination_folder / str(nr_penal).replace('/','_').replace('\\','_') # Înlocuiește caractere invalide
    try:
        output_folder_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        messagebox.showerror(
            "Eroare Creare Folder",
            f"Nu s-a putut crea folderul de ieșire:\n{output_folder_path}\nEroare: {e}"
        )
        return

    # 3. Pregătește contextul pentru șabloane
    try:
        context = _prepare_context(values)
    except Exception as e:
         messagebox.showerror(
            "Eroare Context",
            f"A apărut o eroare la pregătirea datelor pentru documente:\n{e}"
        )
         return

    # 4. Iterează prin șabloane și generează documentele selectate
    generated_files_count = 0
    errors = []

    for template_name, checkbox_key in TEMPLATE_CHECKBOX_MAPPING.items():
        # Verifică dacă checkbox-ul este bifat (presupunând valoare 1 pentru bifat)
        if values.get(checkbox_key) == 1: # Tkinter IntVar returnează 0 sau 1
            template_file_path = TEMPLATE_DIR / f"{template_name}.docx"

            if not template_file_path.is_file():
                error_msg = f"Șablonul '{template_name}.docx' nu a fost găsit în {TEMPLATE_DIR}."
                print(error_msg)
                errors.append(error_msg)
                continue # Treci la următorul șablon

            try:
                # Încarcă șablonul
                doc = DocxTemplate(template_file_path)

                # Render șablonul
                doc.render(context)

                # Construiește calea fișierului de ieșire
                output_filename = f"{nr_penal}_{template_name.replace(' ', '_').replace('#', '')}.docx"
                output_path = output_folder_path / output_filename

                # Salvează documentul generat
                doc.save(output_path)
                generated_files_count += 1
                print(f"Generat: {output_path}") # Mesaj de depanare

            except Exception as e:
                error_msg = f"Eroare la generarea '{template_name}.docx': {e}"
                print(error_msg)
                errors.append(error_msg)

    # 5. Afișează rezultatul final
    if generated_files_count > 0 and not errors:
        messagebox.showinfo(
            "Succes",
            f"Au fost generate {generated_files_count} documente în folderul:\n{output_folder_path}"
        )
    elif generated_files_count > 0 and errors:
        messagebox.showwarning(
            "Generare Parțială",
            f"Au fost generate {generated_files_count} documente, dar au apărut {len(errors)} erori:\n\n" + "\n".join(errors) +
            f"\n\nVerificați folderul: {output_folder_path}"
        )
    elif not errors:
         messagebox.showwarning(
            "Nimic Generat",
            "Nu a fost selectat niciun document pentru generare sau nu au fost găsite șabloane."
        )
    else: # Doar erori
        messagebox.showerror(
            "Eroare Generare",
            f"Nu s-a putut genera niciun document din cauza următoarelor erori:\n\n" + "\n".join(errors)
        )

# Cod de test (opțional)
if __name__ == "__main__":
    print(f"Directorul de șabloane configurat: {TEMPLATE_DIR}")
    if not TEMPLATE_DIR.exists():
         print("AVERTISMENT: Directorul de șabloane nu există!")
    else:
         print("Directorul de șabloane există.")

    # Aici s-ar putea adăuga un mic test, creând un dicționar 'values'
    # de probă și apelând generate_documents(test_values)
    # Dar necesită crearea unui root Tkinter pentru filedialog,
    # deci testarea completă e mai ușoară prin rularea aplicației principale.
