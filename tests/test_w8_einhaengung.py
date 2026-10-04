"""
Pruefung W8: Ist das robuste Speichern wirklich in GameState einghaengt?

Nicht das Modul allein wird geprueft (das tut tests/test_speichern_robust.py),
sondern die EINHAENGUNG: ruft main.py's GameState.save/load das Modul speichern
tatsaechlich und ehrlich auf? Bewiesen wird am echten Spielstand:

  * der Quelltext von GameState.save/load und NebelseetalApp.__init__ nennt
    speichern.speichere / speichern.lade / speichern.wiederherstellen /
    speichern.aufraeumen (eigene Methode pruefe_einhaengung())
  * save() schreibt eine gueltige JSON-Datei, meldet True und laesst keine .tmp liegen
  * ein zweites save() legt .bak mit dem VORIGEN Inhalt an (Sicherung vor dem Ueberschreiben)
  * load() stellt eine beschaedigte Datei aus der .bak wieder her (True) und laedt gueltig
  * load() auf einen fehlenden Pfad gibt False und wirft nichts
  * save() auf ein Verzeichnis gibt False, wirft nichts, loggt 'Speichern fehlgeschlagen'
  * Rundlauf: geaenderte Menge stimmt nach dem Laden, Log nennt 'Gespeichert:'
  * speichern.aufraeumen() entfernt nur die .tmp, Zieldatei und .bak bleiben

Aufruf:  python -X utf8 tests/test_w8_einhaengung.py
"""
from __future__ import annotations

import inspect
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
os.chdir(SRC)

# Eigener, eindeutiger Arbeitsordner - wird am Ende wieder entfernt.
ORDNER = tempfile.mkdtemp(prefix="nebel_w8_einhaengung_")


def pfad(name: str) -> str:
    return os.path.join(ORDNER, name)


def gibt_es(p: str) -> bool:
    return os.path.exists(p)


def lies_json(p: str):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


main = ausnahme("main importieren", lambda: __import__("main"))
import speichern as SP

if main is None:
    shutil.rmtree(ORDNER, ignore_errors=True)
    sys.exit(bericht())


# ==========================================================================
# 1. Einhaengung - der eigene Nachweis, dass main.py W8 wirklich benutzt
# ==========================================================================

abschnitt("1. Einhaengung: main.py ruft src/speichern.py wirklich auf")


def pruefe_einhaengung():
    """Eigene Nachweismethode: main laedt speichern und ruft es in save/load/__init__."""
    check("main.py hat das Modul speichern importiert",
          getattr(main, "speichern", None) is not None)
    check("main.speichern ist DASSELBE Modul wie src/speichern.py",
          getattr(main, "speichern", None) is SP)
    quelle_save = inspect.getsource(main.GameState.save)
    check("GameState.save ruft speichern.speichere auf",
          "speichern.speichere" in quelle_save)
    check("GameState.save legt die Sicherung VOR dem Schreiben an (speichern.sichere_kopie)",
          "speichern.sichere_kopie" in quelle_save)
    quelle_load = inspect.getsource(main.GameState.load)
    check("GameState.load liest ueber speichern.lade",
          "speichern.lade" in quelle_load)
    check("GameState.load stellt aus der Sicherung wieder her (speichern.wiederherstellen)",
          "speichern.wiederherstellen" in quelle_load)
    quelle_init = inspect.getsource(main.NebelseetalApp.__init__)
    check("NebelseetalApp.__init__ raeumt Zwischendateien auf (speichern.aufraeumen)",
          "speichern.aufraeumen" in quelle_init)


ausnahme("Einhaengung pruefen", pruefe_einhaengung)


# ==========================================================================
# 2. GameState.save - gueltige Datei, True, keine .tmp
# ==========================================================================

abschnitt("2. GameState.save schreibt eine gueltige Datei und meldet True")

st = main.GameState()
P1 = pfad("save1.json")
res1 = ausnahme("erste Speicherung", lambda: st.save(P1))
check("save() gibt True zurueck", res1 is True, repr(res1))
check("die Zieldatei existiert danach", gibt_es(P1))
check("nach dem Speichern bleibt KEINE .tmp liegen", not gibt_es(P1 + ".tmp"))
daten1 = ausnahme("Datei mit json.load lesen", lambda: lies_json(P1))
check("die Datei ist mit json.load lesbar", isinstance(daten1, dict))
check("die Datei enthaelt den Schluessel 'resources'",
      isinstance(daten1, dict) and "resources" in daten1)
check("der gespeicherte Holz-Wert ist der Startwert 100",
      isinstance(daten1, dict) and daten1["resources"]["holz"]["amount"] == 100.0,
      str(daten1["resources"]["holz"]["amount"]) if isinstance(daten1, dict) else "—")


# ==========================================================================
# 3. Zweites save() legt .bak mit dem VORIGEN Inhalt an
# ==========================================================================

abschnitt("3. Zweites Speichern legt .bak mit dem VORIGEN Inhalt an")

st.resources["holz"].amount = 123.0
res2 = ausnahme("zweite Speicherung", lambda: st.save(P1))
check("das zweite save() gibt True zurueck", res2 is True, repr(res2))
check("eine Sicherung .bak ist entstanden", gibt_es(P1 + ".bak"))
bak_daten = ausnahme("bak lesen", lambda: lies_json(P1 + ".bak")) if gibt_es(P1 + ".bak") else None
check("die .bak traegt den VORIGEN Inhalt (Holz = 100)",
      isinstance(bak_daten, dict) and bak_daten["resources"]["holz"]["amount"] == 100.0,
      str(bak_daten["resources"]["holz"]["amount"]) if isinstance(bak_daten, dict) else "keine bak")
neu_daten = ausnahme("Hauptdatei lesen", lambda: lies_json(P1))
check("die Hauptdatei traegt den NEUEN Inhalt (Holz = 123)",
      isinstance(neu_daten, dict) and neu_daten["resources"]["holz"]["amount"] == 123.0,
      str(neu_daten["resources"]["holz"]["amount"]) if isinstance(neu_daten, dict) else "—")


# ==========================================================================
# 4. load() stellt eine kaputte Datei aus der .bak wieder her
# ==========================================================================

abschnitt("4. load() stellt eine beschaedigte Datei aus der .bak wieder her")

bak_vorher = lies_json(P1 + ".bak")
with open(P1, "w", encoding="utf-8") as f:
    f.write('{"resources": ')                       # bewusst kaputt
check("die Hauptdatei ist jetzt beschaedigt",
      SP.pruefe_datei(P1)["json_ok"] is False)
st2 = main.GameState()
lade1 = ausnahme("load nach Beschaedigung", lambda: st2.load(P1))
check("load() meldet True (Wiederherstellung gelungen)", lade1 is True, repr(lade1))
check("die Hauptdatei ist wieder gueltiges JSON", SP.pruefe_datei(P1)["json_ok"] is True)
wieder = ausnahme("wiederhergestellte Datei lesen", lambda: lies_json(P1))
check("der wiederhergestellte Inhalt entspricht der .bak", wieder == bak_vorher)
check("der wiederhergestellte Holz-Wert ist 100",
      isinstance(wieder, dict) and wieder["resources"]["holz"]["amount"] == 100.0)
check("auch im geladenen Zustand steht Holz auf 100", st2.resources["holz"].amount == 100.0)


# ==========================================================================
# 5. load() auf einen fehlenden Pfad - False ohne Ausnahme
# ==========================================================================

abschnitt("5. load() auf einen fehlenden Pfad - False ohne Ausnahme")

P_missing = pfad("gibtsnicht.json")
check("die Datei fehlt wirklich", not gibt_es(P_missing))
lade2 = ausnahme("load fehlender Pfad", lambda: st2.load(P_missing))
check("load() auf fehlenden Pfad gibt False zurueck", lade2 is False, repr(lade2))


# ==========================================================================
# 6. save() auf ein unmoegliches Ziel - ehrlich statt Absturz
# ==========================================================================

abschnitt("6. save() auf ein unmoegliches Ziel (Verzeichnis) - ehrlich statt Absturz")

ZIELDIR = pfad("zieldir")
os.makedirs(ZIELDIR, exist_ok=True)
marker = os.path.join(ZIELDIR, "beweis.txt")
with open(marker, "w", encoding="utf-8") as f:
    f.write("unversehrt")
st3 = main.GameState()
res6 = ausnahme("save auf Verzeichnis", lambda: st3.save(ZIELDIR))
check("save() auf ein Verzeichnis gibt False zurueck", res6 is False, repr(res6))
check("das Verzeichnis existiert weiterhin", os.path.isdir(ZIELDIR))
check("das Verzeichnis ist unveraendert (Beweisdatei liegt vor)", gibt_es(marker))
check("neben dem Verzeichnis bleibt keine .tmp liegen", not gibt_es(ZIELDIR + ".tmp"))
check("state.log nennt ehrlich 'Speichern fehlgeschlagen'",
      any("Speichern fehlgeschlagen" in z for z in st3.log), str(st3.log[-3:]))


# ==========================================================================
# 7. Rundlauf - geaenderte Menge ueberlebt, Log nennt 'Gespeichert:'
# ==========================================================================

abschnitt("7. Rundlauf - geaenderte Menge ueberlebt, Log nennt 'Gespeichert:'")

st4 = main.GameState()
st4.resources["stein"].amount = 777.5
P7 = pfad("rundlauf.json")
ausnahme("Rundlauf speichern", lambda: st4.save(P7))
check("der Log nennt 'Gespeichert:' (Meldung aus speichern)",
      any("Gespeichert:" in z for z in st4.log), str(st4.log[-3:]))
st5 = main.GameState()
check("eine frische GameState startet mit Stein = 100", st5.resources["stein"].amount == 100.0)
lade3 = ausnahme("Rundlauf laden", lambda: st5.load(P7))
check("load() meldet True", lade3 is True, repr(lade3))
check("die geaenderte Menge ist nach dem Laden identisch (777.5)",
      st5.resources["stein"].amount == 777.5, str(st5.resources["stein"].amount))


# ==========================================================================
# 8. speichern.aufraeumen() entfernt nur liegengelassene .tmp
# ==========================================================================

abschnitt("8. speichern.aufraeumen() entfernt nur liegengelassene .tmp")

P8 = pfad("raum.json")
SP.speichere({"x": 1}, P8)
SP.sichere_kopie(P8)
rest = P8 + ".tmp"
with open(rest, "w", encoding="utf-8") as f:
    f.write("halb")
check("ein liegengebliebener .tmp-Rest liegt vor", gibt_es(rest))
SP.aufraeumen(P8)
check("aufraeumen() entfernt den .tmp-Rest", not gibt_es(rest))
check("die Hauptdatei bleibt erhalten", gibt_es(P8))
check("die .bak-Sicherung bleibt erhalten", gibt_es(P8 + ".bak"))


# ==========================================================================
# 9. Ehrliche Grenzen des Verfahrens - als Befunde, nicht als Fehler
# ==========================================================================

abschnitt("9. Ehrliche Grenzen des Verfahrens (Befunde, kein Fehler)")

_luecken = SP.offene_luecken()
check("offene_luecken() benennt mindestens 3 Grenzen",
      isinstance(_luecken, dict) and len(_luecken) >= 3, f"{len(_luecken)} Punkte")
for _k in sorted(_luecken):
    befund(f"Grenze: {_k}", str(_luecken[_k])[:90])


# ------------------------------------------------------------------ Abschluss
shutil.rmtree(ORDNER, ignore_errors=True)
sys.exit(bericht())
