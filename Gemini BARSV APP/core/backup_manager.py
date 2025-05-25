# -*- coding: utf-8 -*-
"""
Modul pentru gestionarea operațiunilor de backup (salvare/încărcare date).

Include funcționalități pentru:
- Salvare automată periodică.
- Salvare manuală a stării curente.
- Încărcarea datelor dintr-un fișier de backup selectat.
- Listarea fișierelor de backup existente.
"""

import os
import time
import threading
from pathlib import Path
import pandas as pd
from tkinter import messagebox

# --- Configurare ---

# Numele folderului de backup în directorul home al utilizatorului
BACKUP_FOLDER_NAME = "BARSV APP Backup"
# Numele fișierului pentru salvarea automată generică
AUTOSAVE_FILENAME = "autosave_backup.xlsx"
# Intervalul de autosave în secunde (ex: 600 secunde = 10 minute)
AUTOSAVE_INTERVAL = 600

# Variabilă globală pentru a controla thread-ul de autosave
autosave_thread = None
stop_autosave_event = threading.Event()

# --- Funcții Helper ---

def _get_backup_folder():
    """
    Obține calea către folderul de backup și îl creează dacă nu există.

    Returns:
        Path: Obiect Path către folderul de backup. None dacă apare o eroare.
    """
    try:
        home_dir = Path.home()
        backup_dir = home_dir / BACKUP_FOLDER_NAME
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir
    except OSError as e:
        messagebox.showerror(
            "Eroare Folder Backup",
            f"Nu s-a putut accesa sau crea folderul de backup:\n{e}"
        )
        return None
    except Exception as e:
         messagebox.showerror(
            "Eroare Necunoscută",
            f"A apărut o eroare la accesarea folderului de backup:\n{e}"
        )
         return None


def _clean_data_for_excel(data):
    """
    Curăță dicționarul de date înainte de a-l salva în Excel.
    Înlocuiește valorile None și NaN cu string-uri goale.

    Args:
        data (dict): Dicționarul cu date.

    Returns:
        dict: Dicționarul curățat.
    """
    cleaned_data = {}
    for key, value in data.items():
        # Verifică dacă valoarea este scalară înainte de a verifica NaN
        if pd.api.types.is_scalar(value) and pd.isna(value):
            cleaned_data[key] = ""
        elif value is None:
             cleaned_data[key] = ""
        else:
            # Convertește listele/dicționarele în stringuri dacă e necesar
            # (Excel nu le poate stoca direct în celule standard)
            # Sau gestionează-le specific dacă structura e complexă.
            if isinstance(value, (list, dict)):
                 # Simplu: convertește în string. Complex: necesită serializare (ex: JSON)
                 cleaned_data[key] = str(value)
            else:
                 cleaned_data[key] = value
    return cleaned_data

# --- Funcționalități Backup ---

def autosave_data(data):
    """
    Salvează datele curente în fișierul de autosave.

    Args:
        data (dict): Dicționarul cu datele curente ale aplicației.
    """
    backup_folder = _get_backup_folder()
    if not backup_folder or not data:
        print("Autosave anulat: folder backup invalid sau date goale.")
        return

    autosave_file = backup_folder / AUTOSAVE_FILENAME

    try:
        cleaned_data = _clean_data_for_excel(data)
        # Creează un DataFrame dintr-o listă ce conține dicționarul
        df = pd.DataFrame([cleaned_data])
        # Salvează în format .xlsx folosind openpyxl
        df.to_excel(autosave_file, index=False, engine='openpyxl')
        print(f"Autosave realizat cu succes: {autosave_file} la {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        # Afișează eroarea în consolă, nu deranja utilizatorul cu popup pentru autosave
        print(f"Eroare la autosave: {e}")


def _autosave_loop(get_data_callback):
    """
    Bucla care rulează într-un thread separat pentru autosave.

    Args:
        get_data_callback (callable): Funcție (fără argumente) care returnează
                                      dicționarul cu datele curente din UI.
    """
    while not stop_autosave_event.is_set():
        try:
            # Așteaptă intervalul specificat sau până când evenimentul de oprire e setat
            stop_autosave_event.wait(AUTOSAVE_INTERVAL)
            if stop_autosave_event.is_set():
                break # Ieși dacă s-a cerut oprirea

            print("Inițiere autosave...")
            current_data = get_data_callback()
            if current_data:
                autosave_data(current_data)
            else:
                print("Autosave omis: nu s-au putut obține datele curente.")

        except Exception as e:
            print(f"Eroare în bucla de autosave: {e}")
            # Așteaptă puțin înainte de a reîncerca pentru a evita spam-ul de erori
            time.sleep(60)


def start_autosave_thread(get_data_callback):
    """
    Pornește thread-ul pentru salvarea automată.

    Args:
        get_data_callback (callable): Funcție (fără argumente) care returnează
                                      dicționarul cu datele curente din UI.
    """
    global autosave_thread, stop_autosave_event
    if autosave_thread is None or not autosave_thread.is_alive():
        stop_autosave_event.clear() # Resetează evenimentul de oprire
        autosave_thread = threading.Thread(
            target=_autosave_loop,
            args=(get_data_callback,),
            daemon=True # Thread-ul se va opri automat când programul principal iese
        )
        autosave_thread.start()
        print("Thread-ul de autosave a pornit.")
    else:
        print("Thread-ul de autosave rulează deja.")


def stop_autosave_thread():
    """Oprește thread-ul de autosave dacă rulează."""
    global autosave_thread, stop_autosave_event
    if autosave_thread and autosave_thread.is_alive():
        print("Se oprește thread-ul de autosave...")
        stop_autosave_event.set() # Semnalează buclei să se oprească
        autosave_thread.join(timeout=2) # Așteaptă puțin ca thread-ul să se termine
        if autosave_thread.is_alive():
             print("Thread-ul de autosave nu s-a oprit la timp.")
        else:
             print("Thread-ul de autosave oprit.")
        autosave_thread = None


def save_backup(data, manual=False):
    """
    Salvează datele curente într-un fișier de backup specific.
    Numele fișierului este generat pe baza nr_penal și a datei curente.

    Args:
        data (dict): Dicționarul cu datele curente ale aplicației.
        manual (bool): True dacă salvarea este inițiată manual de utilizator
                       (pentru a afișa mesaj de succes).
    """
    backup_folder = _get_backup_folder()
    if not backup_folder or not data:
        messagebox.showwarning("Salvare Anulată", "Folderul de backup nu este valid sau nu există date de salvat.")
        return

    # Generează numele fișierului
    nr_penal = data.get("nr_penal", "Dosar_Necunoscut")
    if not nr_penal: nr_penal = "Dosar_Fara_Numar"
    # Folosește data curentă pentru nume, nu cea din document
    current_date_str = time.strftime("%d.%m.%Y")
    # Înlocuiește caracterele invalide pentru nume de fișier
    safe_nr_penal = str(nr_penal).replace('/', '_').replace('\\', '_')
    backup_filename = f"{safe_nr_penal} - {current_date_str}.xlsx"
    backup_file = backup_folder / backup_filename

    try:
        cleaned_data = _clean_data_for_excel(data)
        df = pd.DataFrame([cleaned_data])
        df.to_excel(backup_file, index=False, engine='openpyxl')

        if manual:
            messagebox.showinfo(
                "Salvare Manuală Reușită",
                f"Backup salvat cu succes:\n{backup_file}"
            )
        else:
            # Pentru salvările non-manuale (ex: la generare doc), doar printăm
            print(f"Backup specific salvat: {backup_file}")

    except Exception as e:
        messagebox.showerror(
            "Eroare Salvare Backup",
            f"Nu s-a putut salva fișierul de backup:\n{backup_file}\nEroare: {e}"
        )


def refresh_backup_list():
    """
    Returnează o listă cu numele fișierelor de backup (.xlsx) din folderul dedicat.

    Returns:
        list: O listă de string-uri cu numele fișierelor .xlsx.
              Returnează o listă goală dacă folderul nu există sau e gol.
    """
    backup_folder = _get_backup_folder()
    if not backup_folder:
        return []

    try:
        backup_files = [
            f.name for f in backup_folder.iterdir()
            if f.is_file() and f.suffix.lower() == '.xlsx'
        ]
        # Sortează fișierele, poate descrescător după data modificării
        backup_files.sort(key=lambda name: (backup_folder / name).stat().st_mtime, reverse=True)
        return backup_files
    except Exception as e:
        messagebox.showerror(
            "Eroare Listare Backup",
            f"Nu s-au putut lista fișierele de backup:\n{e}"
        )
        return []


def load_backup(file_path):
    """
    Încarcă datele dintr-un fișier de backup Excel specificat.

    Args:
        file_path (str or Path): Calea către fișierul .xlsx de încărcat.

    Returns:
        dict: Dicționarul cu datele încărcate.
              Returnează None dacă apare o eroare la citire sau fișierul e gol.
    """
    if not file_path or not Path(file_path).is_file():
        messagebox.showerror("Eroare Încărcare", "Calea către fișierul de backup este invalidă.")
        return None

    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        if df.empty:
            messagebox.showwarning("Fișier Gol", "Fișierul de backup selectat este gol.")
            return None

        # Înlocuiește NaN cu string gol la încărcare
        df = df.fillna("")

        # Preia primul rând ca dicționar
        # Asigură-te că toate cheile sunt string-uri
        loaded_data = {str(key): value for key, value in df.iloc[0].to_dict().items()}

        print(f"Backup încărcat cu succes din: {file_path}")
        return loaded_data

    except FileNotFoundError:
         messagebox.showerror("Eroare Încărcare", f"Fișierul de backup nu a fost găsit:\n{file_path}")
         return None
    except Exception as e:
        messagebox.showerror(
            "Eroare Încărcare",
            f"A apărut o eroare la citirea fișierului de backup:\n{file_path}\nEroare: {e}"
        )
        return None

# Cod de test (opțional)
if __name__ == "__main__":
    print("Rulare teste pentru core/backup_manager.py...")
    test_backup_folder = _get_backup_folder()
    if test_backup_folder:
        print(f"Folder backup: {test_backup_folder}")
        print("Listă backup-uri existente:")
        files = refresh_backup_list()
        if files:
            for f in files:
                print(f"- {f}")
        else:
            print("Niciun fișier de backup găsit.")

        # Testare salvare/încărcare (necesită date de test)
        test_data = {'nr_penal': 'TEST/123', 'nume_agent1': 'Agent Test', 'ziua_doc': '01', 'luna_doc': '05', 'anul_doc': '2025', 'some_list': [1, 2], 'is_checked': 1}
        print("\nTestare salvare manuală...")
        save_backup(test_data, manual=True) # Va afișa popup

        print("\nTestare încărcare (selectați fișierul salvat)...")
        # Simulare selecție fișier (în aplicația reală, calea vine de la UI)
        test_file_path = test_backup_folder / "TEST_123 - 01.05.2025.xlsx" # Ajustați numele dacă data diferă
        if test_file_path.exists():
             loaded = load_backup(test_file_path)
             if loaded:
                  print("Date încărcate:", loaded)
        else:
             print(f"Fișierul de test {test_file_path} nu există pentru încărcare.")

        # Testare autosave (necesită o funcție dummy get_data)
        def dummy_get_data():
            print("[Callback] Se returnează datele de test...")
            return {'nr_penal': 'AUTOSAVE', 'nume_agent1': 'Test Autosave', 'timestamp': time.time()}

        print("\nTestare pornire autosave (rulează 15 secunde)...")
        AUTOSAVE_INTERVAL = 5 # Scurtează intervalul pentru test
        start_autosave_thread(dummy_get_data)
        time.sleep(15) # Lasă thread-ul să ruleze de câteva ori
        stop_autosave_thread()
        print("Test autosave finalizat.")

    else:
        print("Folderul de backup nu a putut fi accesat.")
