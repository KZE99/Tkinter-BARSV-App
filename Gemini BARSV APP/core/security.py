# -*- coding: utf-8 -*-
"""
Modul pentru verificările de securitate ale aplicației.

Conține funcții pentru a verifica dacă aplicația rulează pe un computer
permis (hostname) și dacă este utilizată de un utilizator autorizat.
"""

import socket
import os
import getpass # O alternativă mai robustă la os.getlogin() în unele cazuri

# Liste predefinite cu hostnames și usernames permise
# ATENȚIE: Păstrați aceste liste actualizate conform cerințelor!
ALLOWED_HOSTNAMES = [
    'DESKTOP-7H7ELRD', 'DESKTOP-1NNK2DH', 'DESKTOP-2JSKFMS', 'PC-B1-BR-039',
    'PC-B1-BR-040', 'PC-B1-BR041', 'PC-B1-BR042', 'PC-B1-BR043',
    'PC-B1-BR044', 'PC-B1-BR045', 'PC-B1-BR046', 'PC-B1-BR047',
    'PC-B1-BR048', 'PC-B1-BR049', 'PC-B1-BR050', 'PC-B1-BR051',
    'PC-B1-BR052', 'DESKTOP-GICB227',
    # Adăugați aici și alte hostnames permise, dacă este necesar
]

ALLOWED_USERS = [
    'gabriel.nica.b', 'florin.raducu.b', 'andrei.odagiu.b', 'nicusor.bratu.b',
    'florin.vasile.b', 'marius.petre.b', 'andrei.pastrama.b', 'daniel.dinita.b',
    'daniel.musa.b', 'george.pufulescu.b', 'cosmin.matei.b', 'gabyn',
    'Programare', 'user', 'danye',
    # Adăugați aici și alți utilizatori permiși, dacă este necesar
]

def get_local_hostname():
    """
    Obține hostname-ul local al computerului.

    Returns:
        str: Hostname-ul local.
    """
    try:
        return socket.gethostname()
    except socket.error as e:
        print(f"Eroare la obținerea hostname-ului: {e}")
        # Returnează o valoare implicită sau ridică excepția mai departe,
        # în funcție de cum dorești să gestionezi eroarea.
        return "unknown_host"

def get_logged_in_user():
    """
    Obține numele utilizatorului logat curent.

    Încearcă mai multe metode pentru compatibilitate crescută.

    Returns:
        str: Numele utilizatorului logat.
    """
    try:
        # getpass.getuser() este adesea mai fiabil decât os.getlogin()
        return getpass.getuser()
    except Exception: # Prinde orice excepție posibilă
        try:
            # Încercare alternativă cu os.getlogin()
            return os.getlogin()
        except OSError as e:
            print(f"Eroare la obținerea utilizatorului logat: {e}")
            # Returnează o valoare implicită sau gestionează altfel
            return "unknown_user"

def check_hostname():
    """
    Verifică dacă hostname-ul local este în lista celor permise.

    Returns:
        bool: True dacă hostname-ul este permis, False altfel.
    """
    local_hostname = get_local_hostname()
    print(f"Verificare hostname: {local_hostname}") # Mesaj de depanare
    if local_hostname in ALLOWED_HOSTNAMES:
        return True
    else:
        print(f"Acces refuzat pentru hostname: {local_hostname}") # Mesaj de depanare
        return False

def check_user():
    """
    Verifică dacă utilizatorul logat curent este în lista celor permiși.

    Returns:
        bool: True dacă utilizatorul este permis, False altfel.
    """
    logged_in_user = get_logged_in_user()
    print(f"Verificare utilizator: {logged_in_user}") # Mesaj de depanare
    if logged_in_user in ALLOWED_USERS:
        return True
    else:
        print(f"Acces refuzat pentru utilizator: {logged_in_user}") # Mesaj de depanare
        return False

# Cod de test (opțional, rulează doar dacă scriptul este executat direct)
if __name__ == "__main__":
    print("Rulare teste pentru core/security.py...")
    hostname_ok = check_hostname()
    user_ok = check_user()
    print(f"Verificare hostname: {'OK' if hostname_ok else 'EȘUAT'}")
    print(f"Verificare utilizator: {'OK' if user_ok else 'EȘUAT'}")

    if hostname_ok and user_ok:
        print("Verificările de securitate au trecut.")
    else:
        print("Verificările de securitate NU au trecut.")
