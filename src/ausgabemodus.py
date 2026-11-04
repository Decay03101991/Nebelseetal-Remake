"""Laufzeitmodus der getrennten Windows-Testfassung.

Die Projektquellen einschliesslich Admin-Logik bleiben vollstaendig auf GitHub.
Der separate EXE-Einstieg setzt den oeffentlichen Modus vor Import der GUI.
Dies ist Bedienungs-Trennung, kein manipulationssicherer Kopierschutz.
"""
import os

def ist_oeffentliche_testversion() -> bool:
    return os.environ.get("NEBEL_OEFFENTLICHE_TESTVERSION") == "1"
