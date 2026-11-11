# -*- coding: ascii -*-
"""G8: die Drosselung im Auftrag - Prozentwahl neben dem Ziel (Daniel 11.11.2026, Register 392).

Daniels Wort (Register 392): "Im Dialog Auftrag anlegen als Prozentwahl neben dem Ziel".
Belegt ist die Regel im Handbuch S. 20, Z. 1191: die Geschwindigkeit ist "in 10-%-Schritten
drosselbar". Der Kern (`auftraege`) konnte das seit jeher - die OBERFLAECHE reichte die Zahl nie
durch, und keine Pruefdatei startete je einen Auftrag MIT Drosselung (Befund D6 des Gesamtaudits
vom 11.11.2026). Diese Datei schliesst beides.

Was sie beweist
---------------
1. Der Kern: Drosselung verlaengert die Reisezeit und senkt die Goldkosten - gemessen an den
   Funktionen, nicht am Wortlaut.
2. Die Kette: `NebelseetalApp._angriff_auftrag_starten` nimmt die Zahl und gibt sie an
   `GameState.auftrag_starten` weiter; der gestartete Auftrag traegt sie in `drosselung`.
3. Der Dialog: die Truppenauswahl hat die Prozentwahl (0 bis 90 in Zehnerschritten) und liest sie
   beim Starten aus. Gegenprobe: sie steht NICHT in der Spionage-Auswahl.
4. Gegenprobe zum Kern: ohne Drosselung bleibt alles wie vorher (0 Prozent ist die Vorgabe).

Aufruf:  python -X utf8 tests/test_drosselung_auftrag.py
"""
from __future__ import annotations

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import auftraege as A  # noqa: E402
import main  # noqa: E402


# ==========================================================================
abschnitt("1. Der Kern: langsamer reisen dauert laenger und kostet weniger Gold")

_leer = A.reisezeit_sekunden(10, 1.0, 1.0, 0)
_halb = A.reisezeit_sekunden(10, 1.0, 1.0, 50)
_voll = A.reisezeit_sekunden(10, 1.0, 1.0, 90)
check("1 ungedrosselt ist die Reise am kuerzesten", _leer < _halb < _voll,
      "%.0f / %.0f / %.0f s" % (_leer, _halb, _voll))
check("1 50 Prozent Drosselung verdoppelt die Reisezeit etwa", abs(_halb / _leer - 2.0) < 0.05,
      "%.2f-fach" % (_halb / _leer))
check("1 90 Prozent Drosselung verzehnfacht sie etwa", abs(_voll / _leer - 10.0) < 0.5,
      "%.2f-fach" % (_voll / _leer))

_EINHEIT = "K\u00e4mpfer"          # Kaempfer als Escape (Pruefdateien bleiben ASCII)
_truppen = {_EINHEIT: 10}
_gold_leer = A.kosten_der_mission(_truppen, 10, 1.0, 0)["gold"]
_gold_halb = A.kosten_der_mission(_truppen, 10, 1.0, 50)["gold"]
check("1 Drosselung senkt die Goldkosten", _gold_halb < _gold_leer,
      "%.2f zu %.2f" % (_gold_halb, _gold_leer))
check("1 Drosselung ist nie negativ und nie ueber 90 Prozent gedeckelt",
      A.reisezeit_sekunden(10, 1.0, 1.0, 300) == A.reisezeit_sekunden(10, 1.0, 1.0, 90)
      and A.reisezeit_sekunden(10, 1.0, 1.0, -20) == A.reisezeit_sekunden(10, 1.0, 1.0, 0), "")


# ==========================================================================
abschnitt("2. Die Kette: App -> Spielstand -> Auftrag traegt die Drosselung")

_app_quelle = inspect.getsource(main.NebelseetalApp._angriff_auftrag_starten)
check("2 die Angriffsmethode nimmt die Drosselung an",
      "drosselung_prozent: float = 0.0" in _app_quelle, "")
check("2 sie gibt sie an den Spielstand weiter",
      "drosselung_prozent=float(drosselung_prozent or 0.0)" in _app_quelle, "")
_state_quelle = inspect.getsource(main.GameState.auftrag_starten)
check("2 der Spielstand reicht sie an `auftraege.starten` weiter",
      "drosselung_prozent=float(drosselung_prozent or 0.0)" in _state_quelle, "")

# Ein echter Auftrag mit Drosselung - der Kern bucht sie in den Eintrag.
_liste = []
_ok, _meldung = A.starten(_liste, "angreifen", {_EINHEIT: 5}, "Ort A", {"name": "Ort B"},
                          10, 1000.0, drosselung_prozent=50)
check("2 der Auftrag startet mit Drosselung", _ok is True, str(_meldung))
check("2 der Eintrag traegt die Drosselung", _liste and float(_liste[-1].get("drosselung") or 0) == 50.0,
      str(_liste[-1].get("drosselung") if _liste else None))
_liste2 = []
A.starten(_liste2, "angreifen", {_EINHEIT: 5}, "Ort A", {"name": "Ort B"}, 10, 1000.0)
check("2 ohne Angabe bleibt es bei 0 (kein Auftrag aendert sich still)",
      float((_liste2[-1].get("drosselung") if _liste2 else -1) or 0) == 0.0,
      str(_liste2[-1].get("drosselung") if _liste2 else None))


# ==========================================================================
abschnitt("3. Der Dialog: Prozentwahl neben dem Ziel, nicht in der Spionage")

_dialog = inspect.getsource(main.NebelseetalApp._truppen_auswahl)
check("3 die Truppenauswahl baut die Prozentwahl", "Drosselung" in _dialog, "")
check("3 sie bietet 0 bis 90 in Zehnerschritten", 'range(0, 100, 10)' in _dialog, "")
check("3 der Wert wird beim Starten ausgelesen", 'replace("%", "")' in _dialog, "")
check("3 sie steht NICHT in der Spionage-Auswahl", "if not spion:" in _dialog, "")
check("3 die Vorgabe ist ungedrosselt", 'tk.StringVar(value="0 %")' in _dialog, "")
check("3 die Anzeige nennt die gewaehlte Drosselung", "gedrosselt auf" in _dialog, "")

sys.exit(bericht())
