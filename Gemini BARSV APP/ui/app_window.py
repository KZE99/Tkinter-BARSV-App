# -*- coding: utf-8 -*-
"""
Modul pentru fereastra principală a aplicației BARSV Tkinter.
(Versiune CTk - Cu integrare Tab EAC)
"""

from tkinter import Menu, messagebox
import customtkinter as ctk
import sys
import traceback

# Importă modulele pentru fiecare tab
try:
    # Folosim '.' pentru import relativ din același pachet (ui)
    from .tabs import (
        principal_tab,
        auto_tab,
        victime_tab,
        martori_tab,
        cfl_tab,
        eac_tab, # <-- Import pentru noul tab EAC
        backup_tab,
        documents_tab
    )
    # Importăm din pachetul 'core'
    from core import backup_manager
except ImportError as e:
    messagebox.showerror(
        "Eroare Import UI",
        f"Nu s-au putut importa modulele tab-urilor sau core: {e}\n"
        "Asigurați-vă că structura directorului este corectă și fișierele __init__.py există."
    )
    sys.exit(1)
except Exception as e:
     messagebox.showerror("Eroare Necunoscută la Import", f"A apărut o eroare: {e}")
     traceback.print_exc(file=sys.stderr)
     sys.exit(1)


class AppWindow:
    """
    Clasa pentru fereastra principală a aplicației. (Versiune CTk)
    """
    def __init__(self, root):
        """
        Inițializează fereastra principală.
        """
        self.root = root
        self.root.title("BARSV App - CustomTkinter Edition")
        self.root.geometry("1000x800")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.data_vars = {}
        self.auto_frames = []
        self.victim_frames = []
        self.tab_containers = {} # Stocăm referințe la containerele tab-urilor

        try:
            self._create_menu()
            self._create_tabview()
            self._populate_tabs()
        except Exception as e:
             messagebox.showerror("Eroare Inițializare UI", f"Nu s-a putut crea interfața:\n{e}")
             print("Eroare detaliată la inițializare UI:", file=sys.stderr)
             traceback.print_exc(file=sys.stderr)
             self.root.destroy()
             sys.exit(1)

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        try:
            backup_manager.start_autosave_thread(self.get_all_data)
        except Exception as e:
            print(f"AVERTISMENT: Nu s-a putut porni autosave: {e}")

    def _create_menu(self):
        """Creează bara de meniu principală."""
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fișier", menu=file_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Ieșire", command=self._on_closing)

    def _create_tabview(self):
        """Creează widget-ul CTkTabview pentru tab-uri."""
        self.tab_view = ctk.CTkTabview(self.root, width=250)
        self.tab_view.pack(pady=10, padx=10, expand=True, fill="both")

        # Adaugă tab-urile și stochează numele exacte
        self.tab_names = {
            "principal": " Principal ",
            "auto": " Auto Implicate ",
            "victime": " Victime ",
            "martori": " Martori ",
            "cfl": " CFL ",
            "eac": " EAC ", # <-- Nume pentru noul tab EAC
            "backup": " Backup Database ",
            "documents": " ## Documente ## "
        }

        for key, name in self.tab_names.items():
            self.tab_view.add(name)

        self.tab_view.set(self.tab_names["principal"]) # Setează tab-ul inițial

    def _populate_tabs(self):
        """Populează fiecare tab cu conținutul său."""
        # Obține și stochează containerele folosind numele exacte
        for key, name in self.tab_names.items():
             try:
                 self.tab_containers[key] = self.tab_view.tab(name)
             except ValueError:
                  print(f"Avertisment: Nu s-a găsit containerul pentru tab-ul '{name}'.", file=sys.stderr)
                  self.tab_containers[key] = None # Sau gestionează eroarea altfel

        # Apelează funcțiile de creare conținut pentru fiecare container existent
        if self.tab_containers.get("principal"):
            principal_tab.create_tab_content(self.tab_containers["principal"], self)
        if self.tab_containers.get("auto"):
            auto_tab.create_tab_content(self.tab_containers["auto"], self)
        if self.tab_containers.get("victime"):
            victime_tab.create_tab_content(self.tab_containers["victime"], self)
        if self.tab_containers.get("martori"):
            martori_tab.create_tab_content(self.tab_containers["martori"], self)
        if self.tab_containers.get("cfl"):
            cfl_tab.create_tab_content(self.tab_containers["cfl"], self)
        # --- ADAUGĂ APEL PENTRU EAC ---
        if self.tab_containers.get("eac"):
            eac_tab.create_tab_content(self.tab_containers["eac"], self)
        # --- SFÂRȘIT ADAUGARE ---
        if self.tab_containers.get("backup"):
            backup_tab.create_tab_content(self.tab_containers["backup"], self)
        if self.tab_containers.get("documents"):
            documents_tab.create_tab_content(self.tab_containers["documents"], self)

    def get_all_data(self):
         """Colectează datele din toate tab-urile."""
         all_data = {}
         print("Colectare date din UI (CTk)...")
         try:
             # Colectează date din fiecare tab existent
             if self.tab_containers.get("principal"):
                 all_data.update(principal_tab.get_data(self))
             if self.tab_containers.get("auto"):
                 all_data.update(auto_tab.get_data(self, self.tab_containers["auto"], self.auto_frames))
             if self.tab_containers.get("victime"):
                 all_data.update(victime_tab.get_data(self, self.tab_containers["victime"], self.victim_frames))
             if self.tab_containers.get("martori"):
                 all_data.update(martori_tab.get_data(self))
             if self.tab_containers.get("cfl"):
                 all_data.update(cfl_tab.get_data(self))
             # --- ADAUGĂ COLECTARE DIN EAC ---
             if self.tab_containers.get("eac"):
                 all_data.update(eac_tab.get_data(self))
             # --- SFÂRȘIT ADAUGARE ---
             # Backup tab nu are date de formular
             if self.tab_containers.get("documents"):
                 all_data.update(documents_tab.get_data(self))

             all_data['auto_number'] = len(self.auto_frames)
             all_data['victim_count'] = len(self.victim_frames)

             print("Date colectate (CTk).")
             return all_data
         except Exception as e:
            messagebox.showerror("Eroare Colectare Date (CTk)", f"A apărut o eroare în timpul colectării:\n{e}")
            print(f"Eroare detaliată la colectare date (CTk): {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return None

    def load_data_into_ui(self, data_to_load):
         """Populează UI-ul cu date."""
         if not data_to_load:
             messagebox.showwarning("Date Lipsă", "Nu există date de încărcat.")
             return

         print("Încărcare date în UI (CTk)...")
         try:
             # Șterge cadrele dinamice înainte de a re-popula
             if self.tab_containers.get("auto"):
                 auto_tab.clear_dynamic_frames(self.tab_containers["auto"], self)
             if self.tab_containers.get("victime"):
                 victime_tab.clear_dynamic_frames(self.tab_containers["victime"], self)
             self.auto_frames.clear()
             self.victim_frames.clear()

             # Încarcă date în fiecare tab existent
             if self.tab_containers.get("principal"):
                 principal_tab.load_data(self, data_to_load)

             if self.tab_containers.get("auto"):
                 auto_count = int(data_to_load.get('auto_number', 0))
                 print(f"  Se vor încărca {auto_count} cadre auto (CTk)...")
                 for i in range(1, auto_count + 1):
                     auto_tab.add_new_auto_tab(self.tab_containers["auto"], self, data_to_load, auto_index=i)

             if self.tab_containers.get("victime"):
                 victim_count = int(data_to_load.get('victim_count', 0))
                 print(f"  Se vor încărca {victim_count} cadre victime (CTk)...")
                 for i in range(1, victim_count + 1):
                     victime_tab.add_new_victim_frame(self.tab_containers["victime"], self, data_to_load, victim_index=i)

             if self.tab_containers.get("martori"):
                 martori_tab.load_data(self, data_to_load)
             if self.tab_containers.get("cfl"):
                 cfl_tab.load_data(self, data_to_load)
             # --- ADAUGĂ ÎNCĂRCARE PENTRU EAC ---
             if self.tab_containers.get("eac"):
                 eac_tab.load_data(self, data_to_load)
             # --- SFÂRȘIT ADAUGARE ---
             # Backup tab nu necesită load
             if self.tab_containers.get("documents"):
                 documents_tab.load_data(self, data_to_load)

             messagebox.showinfo("Încărcare Finalizată", "Datele din backup au fost încărcate în formular.")

         except Exception as e:
            messagebox.showerror("Eroare Încărcare UI (CTk)", f"A apărut o eroare la popularea interfeței:\n{e}")
            print(f"Eroare detaliată la încărcare UI (CTk): {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def _on_closing(self):
        """Funcție apelată la închiderea ferestrei."""
        print("Închidere aplicație (CTk)...")
        try:
            backup_manager.stop_autosave_thread()
        except Exception as e:
             print(f"Eroare la oprirea autosave: {e}")
        self.root.destroy()

# Cod de test (necesită adaptare majoră pentru CTk)
if __name__ == "__main__":
     print("Testarea directă a app_window.py cu CTk necesită adaptarea modulelor dummy și a modului de creare a tab-urilor.")

