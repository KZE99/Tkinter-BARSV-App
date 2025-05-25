# -*- coding: utf-8 -*-
"""
Modul pentru funcții utilitare diverse.

Include funcționalități precum gestionarea automată a caracterelor
românești (ș, ț, ă, â, î) în widget-urile de intrare text,
bazat pe o abordare care gestionează diferite layout-uri și stări
ale tastelor modificatoare.
"""

import tkinter as tk

# --- Handler Caractere Românești (Abordare Reddit) ---

# Mapare pentru caracterele care pot necesita filtrare pe layout-ul Standard RO
# (Uneori, sistemul trimite caracterul corect, dar event.char poate fi problematic)
# Folosim keysym_num pentru identificare sigură.
# (Ex: 0x1fe = ș, 0x1fe = Ș, 0x1fe = ț, 0x1fe = Ț) - Verifică keysym_num pe sistemul țintă!
# Notă: Valorile exacte keysym_num pot varia. Testarea este esențială.
# Acestea sunt valori comune pe Linux/X11 pentru layout RO Standard.
# Pe Windows pot fi diferite (ex: tk.symbol_to_numeric('scaron') etc.)
# Momentan, lăsăm gol, deoarece inserarea directă e de obicei ok pt layout standard.
# REMEDIED_CHARS_STD = {
#     0x01fe: 'ș', 0x01de: 'Ș', # keysym pentru s cu virgulă / S cu virgulă
#     0x01ff: 'ț', 0x01df: 'Ț', # keysym pentru t cu virgulă / T cu virgulă
#     # Adaugă și ăâî dacă e necesar
# }
REMEDIED_CHARS_STD = {} # De obicei nu e necesar dacă layout-ul RO e setat corect

# Mapare pentru layout-ul Programmers (sau US + AltGr)
# Folosește keysym_num pentru tasta de bază ('s', 't', etc.)
# Valorile sunt perechi: (caracter mic, caracter MARE)
# Replace tk.symbol_to_numeric with hardcoded keysym_num values or keysym strings
REMEDIED_CHARS_PROG = {
    ord('ș'): ('ș', 'Ș'),  # Use ord() to get the numeric value of the character
    ord('ț'): ('ț', 'Ț'),
    ord('ă'): ('ă', 'Ă'),
    ord('â'): ('â', 'Â'),
    ord('î'): ('î', 'Î'),
}

# Constante pentru măștile de stare (din X11/Tkinter)
SHIFT_MASK = 0x0001
LOCK_MASK = 0x0002 # Caps Lock

def handle_romanian_characters_keypress(event):
    """
    Gestionează evenimentul KeyPress pentru a insera corect ș, ț, ă, â, î.

    Această funcție trebuie legată (bind) la evenimentul '<KeyPress>'
    al widget-urilor tk.Entry și tk.Text.
    Gestionează atât layout-ul standard (dacă e necesar), cât și cel Programmers.

    Args:
        event (tk.Event): Obiectul eveniment generat de Tkinter.
                          Conține: keysym_num, state, widget, char.

    Returns:
        str or None: Returnează "break" pentru a preveni procesarea implicită
                     dacă s-a făcut o inserare manuală. Altfel, None.
    """
    widget = event.widget
    keysym_num = event.keysym_num
    state = event.state # Masca de biți pentru starea modificatoarelor

    corrected_char = None

    # 1. Verifică maparea pentru layout-ul Standard (dacă e necesar)
    #    (De obicei, nu e necesar dacă layout-ul e corect configurat în OS)
    # if keysym_num in REMEDIED_CHARS_STD:
    #    corrected_char = REMEDIED_CHARS_STD[keysym_num]
    #    print(f"Debug: Standard layout match for keysym {keysym_num}")

    # 2. Verifică maparea pentru layout-ul Programmers
    if not corrected_char and keysym_num in REMEDIED_CHARS_PROG:
        chars_pair = REMEDIED_CHARS_PROG[keysym_num]
        # Determină dacă Shift sau Caps Lock sunt active (dar nu ambele - XOR)
        is_upper = bool(state & SHIFT_MASK) ^ bool(state & LOCK_MASK)
        corrected_char = chars_pair[1] if is_upper else chars_pair[0]
        # print(f"Debug: Programmers layout match for keysym {keysym_num}. State: {state}, Upper: {is_upper}")

    # 3. Dacă am găsit un caracter de corectat/inserat
    if corrected_char:
        try:
            # Inserează caracterul corectat la poziția cursorului
            widget.insert(tk.INSERT, corrected_char)
            # Previne inserarea caracterului original (ex: 's' sau 't')
            # sau a celui problematic trimis de sistem.
            return "break"
        except tk.TclError as e:
            print(f"Eroare la inserarea caracterului '{corrected_char}': {e}")
            return None # Permite comportamentul default în caz de eroare

    # 4. Dacă nu s-a făcut nicio înlocuire, permite comportamentul normal
    # print(f"Debug: No match for keysym {keysym_num}. Char: '{event.char}', State: {state}")
    return None

# --- Alte Utilitare (adăugați aici dacă este necesar) ---

# --- Cod de Test (opțional) ---
if __name__ == "__main__":
    # Creează o fereastră simplă pentru testare
    root = tk.Tk()
    root.title("Test Utilitare - Caractere Românești (Reddit)")
    root.geometry("400x250")

    info_text = (
        "Introduceți text (s/t/a/q/i devin ș/ț/ă/â/î):\n"
        "- Funcționează cu Shift și Caps Lock.\n"
        "- Testează pe layout-ul tău (RO Standard/Programmers)."
    )
    label = tk.Label(root, text=info_text, justify=tk.LEFT)
    label.pack(pady=10)

    # Test cu tk.Entry
    entry_label = tk.Label(root, text="Câmp Entry:")
    entry_label.pack()
    entry = tk.Entry(root, width=40)
    entry.pack(pady=5)
    # Leagă funcția la evenimentul KeyPress pentru Entry
    entry.bind("<KeyPress>", handle_romanian_characters_keypress)

    # Test cu tk.Text
    text_label = tk.Label(root, text="Câmp Text:")
    text_label.pack()
    text_widget = tk.Text(root, height=5, width=40)
    text_widget.pack(pady=5)
    # Leagă funcția la evenimentul KeyPress pentru Text
    text_widget.bind("<KeyPress>", handle_romanian_characters_keypress)

    # Setează focus pe primul câmp pentru a putea tasta direct
    entry.focus_set()

    print("Notă: Valorile keysym_num pot diferi între OS (Linux/Windows/Mac).")
    print("Maparea REMEDIED_CHARS_PROG folosește tk.symbol_to_numeric pentru portabilitate.")
    print("Maparea REMEDIED_CHARS_STD este goală implicit (ajustați dacă e necesar).")

    root.mainloop()
