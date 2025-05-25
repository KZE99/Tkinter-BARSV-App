# -*- coding: utf-8 -*-
"""
Fișierul principal, punctul de intrare al aplicației BARSV Tkinter (cu CustomTkinter).
"""

# import tkinter as tk # Nu mai folosim tk pentru fereastra principală
# from tkinter import messagebox # Îl importăm în modulele unde e necesar
import customtkinter as ctk # Folosim customtkinter pentru fereastra principală
from tkinter import messagebox # Păstrăm messagebox pentru erori inițiale
import sys
import os
import traceback # Pentru depanare

# Importă modulele necesare din proiect
try:
    from core import security
    # Importăm clasa AppWindow adaptată pentru CTk
    from ui.app_window import AppWindow
except ImportError as e:
    messagebox.showerror(
        "Eroare Import Principal",
        f"Nu s-au putut importa modulele necesare (core.security, ui.app_window): {e}\n"
        "Asigurați-vă că structura directorului este corectă și fișierele __init__.py există."
    )
    sys.exit(1)
except Exception as e:
     messagebox.showerror("Eroare Necunoscută la Import", f"A apărut o eroare la import: {e}")
     traceback.print_exc(file=sys.stderr)
     sys.exit(1)


def run_security_checks():
    """
    Rulează verificările de securitate pentru hostname și utilizator.
    """
    try:
        if not security.check_hostname():
            messagebox.showerror(
                "Acces Interzis",
                "Aplicația nu are permisiunea de a rula pe acest computer."
            )
            return False
        if not security.check_user():
            messagebox.showerror(
                "Acces Interzis",
                "Acest utilizator nu are permisiunea de a utiliza aplicația."
            )
            return False
        return True
    except Exception as e:
        messagebox.showerror("Eroare Securitate", f"A apărut o eroare la verificările de securitate:\n{e}")
        traceback.print_exc(file=sys.stderr)
        return False

def main():
    """
    Funcția principală a aplicației (versiune CTk).
    """
    print("Pornire aplicație BARSV (CTk)...") # Mesaj de start

    # Rulează verificările de securitate
    if not run_security_checks():
        sys.exit(1)

    # --- MODIFICARE: Folosim ctk.CTk() ---
    root = ctk.CTk()
    # --- SFÂRȘIT MODIFICARE ---

    # --- ELIMINARE: root.withdraw() nu mai este necesar ---
    # root.withdraw()
    # --- SFÂRȘIT ELIMINARE ---

    try:
        # Inițializează și rulează fereastra principală a aplicației
        app = AppWindow(root) # Pasează fereastra rădăcină CTk
    except Exception as e:
         # Prinde erorile care pot apărea în AppWindow.__init__
         messagebox.showerror("Eroare Fatală la Inițializare", f"Nu s-a putut inițializa fereastra principală:\n{e}")
         print("Eroare fatală în AppWindow.__init__:", file=sys.stderr)
         traceback.print_exc(file=sys.stderr)
         # Asigură-te că fereastra se închide dacă inițializarea eșuează
         try:
             root.destroy()
         except:
             pass
         sys.exit(1)


    # Pornește bucla principală de evenimente Tkinter/CTk
    # Aceasta face fereastra vizibilă și interactivă
    try:
        root.mainloop()
    except Exception as e:
        print(f"Eroare în bucla principală (mainloop): {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)


# Punctul de intrare standard pentru scripturi Python
if __name__ == "__main__":
    main()
