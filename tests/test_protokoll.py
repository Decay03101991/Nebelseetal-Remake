"""Prueft die Regeln des Entwicklungsprotokolls (Vorgabe Daniel: „vor allem das Protokoll").

Das Protokoll ist kein Beiwerk, sondern das Dokument, mit dem Daniel die Entstehung des Spiels
mitschreibt. Diese Pruefdatei haelt seine eigenen Regeln fest:

  1. **Zielgroesse** — deutlich unter dem Umfang, ab dem verdichtet wird (ueber der Grenze: Befund).
  2. **Keine Sicherungen im Protokoll** — die gehoeren nach `archiv/dokumentation/projektunterlagen_historisch/SICHERUNGEN.md`.
  3. **Belegbarkeit** — jede genannte Commit-Kennung muss es in git wirklich geben (keine erfundene).
  4. **Verdichten nimmt nichts weg** — gegenueber der Vor-Fassung darf keine Commit-Kennung und
     keine Pruefzahl fehlen.
  5. **Absaetze bleiben** — die Prosa-Anfaenge der Vor-Fassung muessen wieder vorkommen (Befund,
     weil ein umformulierter Anfang erlaubt ist, ein fehlender Absatz aber nicht).
  6. **Die Regeln stehen im Protokoll selbst** — inklusive „immer anhaengen".

Aufruf:  python -X utf8 tests/test_protokoll.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pruefe_protokoll as pz  # noqa: E402  (Werkzeug als Modul: dieselben Pruefungen)

PROTOKOLL = os.path.join(ROOT, "docs", "ENTWICKLUNGSPROTOKOLL.md")
VORFASSUNG = os.path.join(ROOT, "archiv", "dokumentation", "protokoll_alte_fassungen", "ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md")

abschnitt("1. Das Protokoll haelt seine Zielgroesse")

check("die Datei existiert", os.path.exists(PROTOKOLL))
roh = open(PROTOKOLL, encoding="utf-8").read()
zeilen = roh.splitlines()
check("die Vor-Fassung der Verdichtung ist aufbewahrt", os.path.exists(VORFASSUNG),
      os.path.basename(VORFASSUNG))
if len(zeilen) > pz.ZIELZEILEN:
    befund("Zielgroesse", f"{len(zeilen)} Zeilen — Regel: unter {pz.ZIELZEILEN}, also verdichten "
                          f"(vorher die unveraenderte Fassung sichern und committen)")
else:
    check(f"unter der Zielgroesse von {pz.ZIELZEILEN} Zeilen", True, f"{len(zeilen)} Zeilen")

abschnitt("2. Keine Sicherungen im Protokoll, Sicherungen woanders")

sicherungszeilen = [z for z in zeilen
                    if re.match(r"^\|\s*\d{1,2}[:.]\d{2}\s*\|\s*\*{0,2}Sicherungszeile", z)]
check("keine Sicherungszeile im Protokoll (sie gehoeren nach archiv/dokumentation/projektunterlagen_historisch/SICHERUNGEN.md)",
      not sicherungszeilen, f"{len(sicherungszeilen)} gefunden")
check("die Sicherungsdatei selbst gibt es", os.path.exists(os.path.join(ROOT, "archiv", "dokumentation", "projektunterlagen_historisch", "SICHERUNGEN.md")))

abschnitt("3. Jede genannte Commit-Kennung gibt es wirklich")

kennungen = sorted({k for k in set(pz.COMMIT.findall(roh)) if not k.isdigit()})
unbekannt = [k for k in kennungen if not pz.git_kennt(k)]
check("keine erfundene Commit-Kennung", not unbekannt,
      f"{len(kennungen)} geprueft, unbekannt: {unbekannt if unbekannt else 'keine'}")

abschnitt("4. Verdichten hat nichts weggenommen")

if os.path.exists(VORFASSUNG):
    alt = open(VORFASSUNG, encoding="utf-8").read()
    alt_kennungen = {k for k in set(pz.COMMIT.findall(alt)) if not k.isdigit()}
    fehlende_k = sorted(alt_kennungen - set(kennungen))
    alt_zahlen = set(pz.PRUEFZAHL.findall(alt))
    fehlende_z = sorted(alt_zahlen - set(pz.PRUEFZAHL.findall(roh)))
    check("keine Commit-Kennung der Vor-Fassung verloren", not fehlende_k,
          f"{len(alt_kennungen)} geprueft" + (f", fehlt {fehlende_k}" if fehlende_k else ""))
    check("keine Pruefzahl der Vor-Fassung verloren", not fehlende_z,
          f"{len(alt_zahlen)} geprueft" + (f", fehlt {fehlende_z[:6]}" if fehlende_z else ""))
    anfaenge = {a.strip() for a in re.findall(r"^\*\*([^*\n]{8,80})\*\*", alt, re.M)}
    fehlende_a = sorted(a for a in anfaenge if a not in roh)
    if fehlende_a:
        befund("Absatz-Anfaenge", f"{len(fehlende_a)} Absatz-Anfang/Anfaenge der Vor-Fassung kommen "
                                  f"nicht mehr woertlich vor — einzeln nachsehen, ob Inhalt verloren "
                                  f"ging: {' | '.join(fehlende_a[:5])}")
    else:
        check("alle Absatz-Anfaenge der Vor-Fassung sind noch da", True, f"{len(anfaenge)} geprueft")
else:
    befund("Vor-Fassung fehlt", "Vollstaendigkeit der Verdichtung nicht pruefbar")

abschnitt("5. Die Regeln stehen im Protokoll selbst")

kopf = roh[:roh.find("## Vorgeschichte")]
for regel in ("Nach jedem groben Schritt eine Zeile", "anhängen", "eine Zeile je grobem Schritt",
              "Fehler und Irrwege gehören hinein", "Sicherungen stehen nicht hier",
              "Kosten nur gemessen", "Zielgröße"):
    check(f"Regel im Kopf: „{regel}\"", regel in kopf)

abschnitt("6. Das Pruefwerkzeug laeuft im Sammellauf durch")

lauf = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "tools", "pruefe_protokoll.py")],
                      capture_output=True, text=True, timeout=180)
check("tools/pruefe_protokoll.py endet ohne Fehler", lauf.returncode == 0,
      f"Rueckgabe {lauf.returncode}")

sys.exit(bericht())
