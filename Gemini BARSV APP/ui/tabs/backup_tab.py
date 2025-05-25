# -*- coding: utf-8 -*-
"""
Modul pentru crearea interfeței tab-ului 'Backup Database'.
(Versiune adaptată pentru CustomTkinter)
"""

import tkinter as tk
# from tkinter import ttk # Nu mai folosim ttk
import customtkinter as ctk # Folosim customtkinter
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
import traceback

# Asigură-te că backup_manager există și funcționează
try:
    from core import backup_manager
except ImportError as e:
    messagebox.showerror("Eroare Import Backup Tab (CTk)", f"Nu s-a putut importa 'core.backup_manager': {e}")
    sys.exit(1)


# Prefix pentru cheile variabilelor (nu sunt folosite direct aici)
# VAR_PREFIX = "backup_"
# DATA_KEYS = []

# --- MODIFICARE NUME FUNCȚIE ---
def create_tab_content(parent_container, app_instance):
    """
    Creează și populează conținutul pentru tab-ul 'Backup Database'
    folosind widget-uri CustomTkinter.

    Args:
        parent_container (ctk.CTkFrame): Containerul oferit de CTkTabview.
        app_instance (AppWindow): Instanța principală a aplicației.
    """
    # Nu mai returnăm un frame, populăm direct parent_container
    parent_container.grid_columnconfigure(0, weight=1) # Permite extinderea listei
    parent_container.grid_rowconfigure(2, weight=1) # Permite extinderea listei

    # --- Variabile Tkinter ---
    selected_file_var = tk.StringVar() # Păstrăm StringVar pentru compatibilitate
    # Referință la cadrul listei pentru a putea șterge/adăuga elemente
    list_scroll_frame_ref = {}

    # --- Funcții Helper Specifice Tab-ului (Adaptate pentru CTk) ---

    def _browse_file():
        """ Deschide dialogul pentru selectarea unui fișier de backup (.xlsx) """
        backup_dir = backup_manager._get_backup_folder()
        if not backup_dir: return

        filepath = filedialog.askopenfilename(
            title="Selectați fișierul de backup",
            initialdir=backup_dir,
            filetypes=[("Fișiere Excel", "*.xlsx"), ("Fișiere Excel Vechi", "*.xls"), ("Toate fișierele", "*.*")]
        )
        if filepath:
            selected_file_var.set(filepath)
            # Deselectează vizual itemul din lista custom (dacă implementăm)
            _clear_list_selection()

    def _clear_list_selection():
         """ Deselectează vizual itemul selectat în lista custom. """
         list_scroll_frame = list_scroll_frame_ref.get("frame")
         if list_scroll_frame:
              for widget in list_scroll_frame.winfo_children():
                   if isinstance(widget, ctk.CTkButton): # Sau CTkLabel dacă folosim asta
                        widget.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]) # Culoare default

    def _on_backup_select(filename, button_widget):
         """ Actualizează câmpul de selecție când un item e ales din lista custom. """
         _clear_list_selection() # Deselectează vizual celelalte
         backup_dir = backup_manager._get_backup_folder()
         if backup_dir and filename:
              full_path = backup_dir / filename
              selected_file_var.set(str(full_path))
              # Evidențiază butonul selectat
              button_widget.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"]) # Culoare hover
         else:
              selected_file_var.set("")


    def _refresh_list():
        """ Reîmprospătează lista custom de fișiere de backup. """
        list_scroll_frame = list_scroll_frame_ref.get("frame")
        if not list_scroll_frame:
            print("Eroare: Cadrul listei de backup nu a fost găsit.")
            return

        # Șterge elementele vechi (butoane/labels)
        for widget in list_scroll_frame.winfo_children():
            widget.destroy()

        backup_files = backup_manager.refresh_backup_list()
        if backup_files:
            for filename in backup_files:
                # Creează un buton pentru fiecare fișier
                backup_button = ctk.CTkButton(
                    list_scroll_frame,
                    text=filename,
                    anchor="w", # Aliniază textul la stânga
                    fg_color="transparent", # Fundal transparent inițial
                    hover=False, # Dezactivează hover default dacă dorim control manual
                    command=lambda f=filename, b=None: _on_backup_select(f, b) # Trimite numele fișierului
                )
                 # Trick pentru a pasa referința butonului la command
                backup_button.configure(command=lambda f=filename, b=backup_button: _on_backup_select(f, b))
                backup_button.pack(fill="x", padx=5, pady=1)
        else:
            # Afișează un label dacă nu există backup-uri
            no_backup_label = ctk.CTkLabel(list_scroll_frame, text=" (Niciun backup găsit) ", text_color="gray")
            no_backup_label.pack(padx=5, pady=5)

        selected_file_var.set("") # Golește câmpul de selecție
        _clear_list_selection()


    def _load_selected_backup():
        """ Încarcă datele din fișierul selectat. """
        file_to_load = selected_file_var.get()
        if not file_to_load:
            messagebox.showwarning("Nicio Selecție", "Vă rugăm selectați un fișier de backup din listă sau folosind butonul 'Răsfoiește'.")
            return

        file_path = Path(file_to_load)
        if not file_path.is_file():
             messagebox.showerror("Fișier Invalid", f"Fișierul selectat nu este valid sau nu există:\n{file_path}")
             return

        loaded_data = backup_manager.load_backup(file_path)
        if loaded_data:
            try:
                # Apelează metoda din AppWindow (care trebuie adaptată pt CTk)
                app_instance.load_data_into_ui(loaded_data)
            except Exception as e:
                 messagebox.showerror("Eroare Încărcare UI (CTk)", f"A apărut o eroare la aplicarea datelor în interfață:\n{e}")
                 print("Eroare detaliată la încărcare UI (CTk):", file=sys.stderr)
                 traceback.print_exc(file=sys.stderr)


    def _save_manual_backup():
        """ Salvează starea curentă a formularului într-un fișier nou. """
        # Obține datele din TOATE tab-urile (funcția trebuie adaptată pt CTk)
        current_data = app_instance.get_all_data()
        if current_data:
            backup_manager.save_backup(current_data, manual=True)
            _refresh_list() # Actualizează lista după salvare
        else:
            # Mesajul de eroare este afișat de get_all_data dacă eșuează
            print("Salvare manuală anulată: nu s-au putut colecta datele.")


    # --- Creare Widget-uri CTk ---

    # Frame Selecție Fișier
    browse_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    browse_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10), padx=5)
    browse_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(browse_frame, text="Selectați fișier:").grid(row=0, column=0, padx=(0, 5), sticky="w")
    # Folosim CTkEntry, dar îl facem readonly prin state (nu există opțiune directă ca la ttk)
    entry_selected_file = ctk.CTkEntry(browse_frame, textvariable=selected_file_var, width=400) # Ajustează lățimea
    entry_selected_file.grid(row=0, column=1, sticky="ew")
    entry_selected_file.configure(state="disabled") # Îl facem non-editabil

    button_browse = ctk.CTkButton(browse_frame, text="Răsfoiește...", command=_browse_file, width=100)
    button_browse.grid(row=0, column=2, padx=(5, 0))

    # Frame Butoane Acțiuni
    action_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
    action_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=5)
    action_frame.columnconfigure(0, weight=1) # Spațiu stânga
    action_frame.columnconfigure(1, weight=0) # Buton Load
    action_frame.columnconfigure(2, weight=1) # Spațiu mijloc
    action_frame.columnconfigure(3, weight=0) # Buton Save
    action_frame.columnconfigure(4, weight=1) # Spațiu dreapta

    button_load = ctk.CTkButton(action_frame, text="Încarcă Backup Selectat", command=_load_selected_backup, width=200)
    button_load.grid(row=0, column=1, padx=10)

    button_save = ctk.CTkButton(action_frame, text="Salvează Backup Manual Acum", command=_save_manual_backup, width=200)
    button_save.grid(row=0, column=3, padx=10)

    # Frame Listă Backup-uri (Folosind CTkScrollableFrame)
    list_container_frame = ctk.CTkFrame(parent_container, border_width=1, corner_radius=10)
    list_container_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0), padx=5)
    list_container_frame.grid_rowconfigure(1, weight=1)    # Scrollable frame se extinde
    list_container_frame.grid_columnconfigure(0, weight=1) # Scrollable frame se extinde

    ctk.CTkLabel(list_container_frame, text="Backup-uri Existente", font=ctk.CTkFont(weight="bold")).grid(
        row=0, column=0, pady=(5, 5), padx=10, sticky="ew")

    # **ÎNLOCUIRE Listbox:** Folosim CTkScrollableFrame
    list_scroll_frame = ctk.CTkScrollableFrame(list_container_frame, label_text="") # Fără label propriu
    list_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0,5))
    list_scroll_frame_ref["frame"] = list_scroll_frame # Stocăm referința

    # Buton Refresh Listă
    button_refresh = ctk.CTkButton(list_container_frame, text="Actualizează Lista", command=_refresh_list, width=150)
    button_refresh.grid(row=2, column=0, pady=(5, 10))

    # --- Populare Inițială Listă ---
    _refresh_list()

    # Nu mai returnăm nimic


# --- Funcții get/load data (nu sunt necesare pentru acest tab) ---

# --- MODIFICARE SEMNĂTURĂ ---
def get_data(app_instance):
    """ Acest tab nu are date de formular proprii de colectat. """
    return {}

# --- MODIFICARE SEMNĂTURĂ ---
def load_data(app_instance, data_to_load):
    """ Acest tab nu încarcă date în propriile widget-uri. """
    pass

