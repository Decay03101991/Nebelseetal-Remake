"""Windows-Testbuild: normaler Spielerweg, getrennte Laufzeitdaten.

Dieser Einstieg blockiert die Admin-Oberflaeche; der volle Admin-Quellcode bleibt
fuer Hermes im Repository. Keine Security-/Anti-Tamper-Garantie fuer Open Source.
"""
import os
from pathlib import Path

# Ersetzt das von Entwicklern eventuell gesetzte Save-Override absichtlich.
basis = os.environ.get("LOCALAPPDATA") or str(Path.home())
os.environ["NEBEL_SPIELDATEN_ORDNER"] = str(
    Path(basis) / "Nebelseetal_Remake" / "Public_Test_FIX04j"
)
os.environ["NEBEL_OEFFENTLICHE_TESTVERSION"] = "1"

from main import main

if __name__ == "__main__":
    main()
