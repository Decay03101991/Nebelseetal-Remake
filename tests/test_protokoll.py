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

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import glob
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
# ENTSCHEIDUNG Daniel 02.11.2026: zwei Hefte. Das aktive Heft fuehrt ab 02.11.2026; die Historie bis
# 01.11.2026 steht geschlossen daneben.
HISTORIE = os.path.join(ROOT, "docs", "ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md")
# ENTSCHEIDUNG Daniel 05.11.2026 (Frage 4, Register 218): AUSLAGERN statt verdichten. Jedes
# ausgelagerte Heft heisst ENTWICKLUNGSPROTOKOLL_HISTORIE_*.md; Vollstaendigkeit und Belegbarkeit
# gelten fuer das aktive Heft und ALLE Historienhefte ZUSAMMEN - sonst verliert die Wache genau die
# Zeilen aus dem Blick, die nur verschoben wurden.
HISTORIEN = sorted(glob.glob(os.path.join(ROOT, "docs", "ENTWICKLUNGSPROTOKOLL_HISTORIE_*.md")))
VORFASSUNG = os.path.join(ROOT, "archiv", "dokumentation", "protokoll_alte_fassungen", "ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md")
# ENTSCHEIDUNG Daniel 06.11.2026: HEFTWECHSEL statt Verdichtung. Das abgeschlossene Heft liegt
# vollstaendig im Archiv und zaehlt zur Gesamtsumme; geprueft wird zusaetzlich die Naht (der
# erste Eintrag des neuen Hefts ist der letzte Eintrag des Archivhefts).
ARCHIV = os.path.join(ROOT, "archiv", "dokumentation", "protokoll_alte_fassungen",
                      "ENTWICKLUNGSPROTOKOLL_BIS_20261106.md")

abschnitt("1. Das Protokoll haelt seine Zielgroesse")

check("die Datei existiert", os.path.exists(PROTOKOLL))
roh = open(PROTOKOLL, encoding="utf-8").read()
zeilen = roh.splitlines()
check("das geschlossene Geschichtsheft liegt daneben", os.path.exists(HISTORIE),
      os.path.basename(HISTORIE))
historie = open(HISTORIE, encoding="utf-8").read() if os.path.exists(HISTORIE) else ""
# ALLE Historienhefte zusammen (das geschlossene von vor dem 02.11. und die ausgelagerten Sektionen).
historie_alle = "\n".join(open(p, encoding="utf-8").read() for p in HISTORIEN)
archiv_text = open(ARCHIV, encoding="utf-8").read() if os.path.exists(ARCHIV) else ""
gesamt = roh + "\n" + historie_alle + "\n" + archiv_text
check("die Vor-Fassung der Verdichtung ist aufbewahrt", os.path.exists(VORFASSUNG),
      os.path.basename(VORFASSUNG))
if len(zeilen) > pz.ZIELZEILEN:
    befund("Zielgroesse", f"{len(zeilen)} Zeilen — Regel: unter {pz.ZIELZEILEN}, also verdichten "
                          f"(vorher die unveraenderte Fassung sichern und committen)")
else:
    check(f"unter der Zielgroesse von {pz.ZIELZEILEN} Zeilen", True, f"{len(zeilen)} Zeilen")

abschnitt("1b. Zwei Hefte: aktiv ab 02.11.2026, Historie davor geschlossen")

check("das aktive Heft nennt sein Startdatum", "(ab 02.11.2026)" in zeilen[0], zeilen[0][:70])
check("das Geschichtsheft nennt sich selbst HISTORIE bis 01.11.2026",
      bool(historie) and "HISTORIE bis 01.11.2026" in historie.splitlines()[0],
      historie.splitlines()[0][:70] if historie else "fehlt")
check("die Historie traegt die letzte Sektion von vor dem Schnitt (HERMES-UMSETZUNG-02)",
      "HERMES-UMSETZUNG-02" in historie_alle, "")
# Der Schnitt wandert mit jeder Auslagerung. Geprueft wird deshalb nicht ein fester Name, sondern
# die NAHT: die letzte ausgelagerte Sektion steht NUR in den Historienheften, die aelteste Sektion
# des aktiven Hefts NUR im aktiven Heft.
check("jedes Historienheft nennt sich selbst HISTORIE",
      bool(HISTORIEN) and all("HISTORIE" in open(p, encoding="utf-8").read().splitlines()[0]
                              for p in HISTORIEN),
      "%d Hefte" % len(HISTORIEN))
check("der Schnitt ist sauber: die Sektion HERMES-BOTDORF-06 steht NUR im Historienheft",
      "## HERMES-BOTDORF-06" not in roh and "## HERMES-BOTDORF-06" in historie_alle, "")
check("der Schnitt ist sauber: die Sektion HERMES-BOTNAHRUNG-01 steht NUR im Archivheft",
      "## HERMES-BOTNAHRUNG-01" not in roh and "## HERMES-BOTNAHRUNG-01" in archiv_text, "")
check("das abgeschlossene Heft liegt im Archiv", os.path.exists(ARCHIV),
      os.path.basename(ARCHIV))
_zeit = re.compile(r"^\|\s*\d{1,2}[:.]\d{2}")
_archiv_zeilen = [z for z in archiv_text.splitlines() if _zeit.match(z)]
_neue_zeilen = [z for z in zeilen if _zeit.match(z)]
check("die Naht stimmt: erster Eintrag des neuen Hefts = letzter Eintrag des Archivhefts",
      bool(_archiv_zeilen) and bool(_neue_zeilen)
      and _neue_zeilen[0].strip() == _archiv_zeilen[-1].strip(),
      (_neue_zeilen[0][:60] if _neue_zeilen else "kein Eintrag"))
check("das neue Heft verweist auf das Archivheft",
      os.path.basename(ARCHIV) in roh, "")
check("das aktive Heft verweist auf das ausgelagerte",
      "ENTWICKLUNGSPROTOKOLL_HISTORIE_20261102_bis_20261103.md" in roh, "")
check("alle Hefte zusammen ergeben das Protokoll",
      bool(historie_alle) and len(gesamt) > len(roh), f"{len(roh)} + {len(historie_alle)} Zeichen")

abschnitt("2. Keine Sicherungen im Protokoll, Sicherungen woanders")
sicherungszeilen = [z for z in zeilen
                    if re.match(r"^\|\s*\d{1,2}[:.]\d{2}\s*\|\s*\*{0,2}Sicherungszeile", z)]
check("keine Sicherungszeile im Protokoll (sie gehoeren nach archiv/dokumentation/projektunterlagen_historisch/SICHERUNGEN.md)",
      not sicherungszeilen, f"{len(sicherungszeilen)} gefunden")
check("die Sicherungsdatei selbst gibt es", os.path.exists(os.path.join(ROOT, "archiv", "dokumentation", "projektunterlagen_historisch", "SICHERUNGEN.md")))

abschnitt("3. Jede genannte Commit-Kennung gibt es wirklich")

kennungen = sorted({k for k in set(pz.COMMIT.findall(gesamt)) if not k.isdigit()})
unbekannt = [k for k in kennungen if not pz.git_kennt(k)]
check("keine erfundene Commit-Kennung", not unbekannt,
      f"{len(kennungen)} geprueft, unbekannt: {unbekannt if unbekannt else 'keine'}")

abschnitt("4. Verdichten hat nichts weggenommen")

if os.path.exists(VORFASSUNG):
    alt = open(VORFASSUNG, encoding="utf-8").read()
    alt_kennungen = {k for k in set(pz.COMMIT.findall(alt)) if not k.isdigit()}
    fehlende_k = sorted(alt_kennungen - set(kennungen))
    alt_zahlen = set(pz.PRUEFZAHL.findall(alt))
    fehlende_z = sorted(alt_zahlen - set(pz.PRUEFZAHL.findall(gesamt)))
    check("keine Commit-Kennung der Vor-Fassung verloren", not fehlende_k,
          f"{len(alt_kennungen)} geprueft" + (f", fehlt {fehlende_k}" if fehlende_k else ""))
    check("keine Pruefzahl der Vor-Fassung verloren", not fehlende_z,
          f"{len(alt_zahlen)} geprueft" + (f", fehlt {fehlende_z[:6]}" if fehlende_z else ""))
    anfaenge = {a.strip() for a in re.findall(r"^\*\*([^*\n]{8,80})\*\*", alt, re.M)}
    fehlende_a = sorted(a for a in anfaenge if a not in gesamt)
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
