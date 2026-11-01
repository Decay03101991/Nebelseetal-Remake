"""Windows-Testbuild: normaler Spielerweg, getrennte Laufzeitdaten.

Dieser Einstieg blockiert die Admin-Oberflaeche; der volle Admin-Quellcode bleibt
fuer Hermes im Repository. Keine Security-/Anti-Tamper-Garantie fuer Open Source.
"""
import os
from pathlib import Path

# Ersetzt das von Entwicklern eventuell gesetzte Save-Override absichtlich.
#
# Daniel 01.11.2026, woertlich: "in der demo exe darf es keine vorhandenen spielstaende geben sie muss
# leer sein." Deshalb bekommt die Demo einen EIGENEN, noch nie benutzten Speicherordner. Der
# Speicherordner der frueheren Testversion bleibt auf der Platte liegen und wird absichtlich NICHT
# mehr gelesen - wer die alte Testversion benutzt hat, startet die Demo dadurch leer. Wer den Namen
# spaeter wieder aendert, nimmt den Spielern ihre Spielstaende: nur mit Daniels Zustimmung anfassen.
basis = os.environ.get("LOCALAPPDATA") or str(Path.home())
os.environ["NEBEL_SPIELDATEN_ORDNER"] = str(
    Path(basis) / "Nebelseetal_Remake" / "Demo"
)
os.environ["NEBEL_OEFFENTLICHE_TESTVERSION"] = "1"

from main import main

if __name__ == "__main__":
    main()
