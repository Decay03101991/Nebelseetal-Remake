"""Pruefung des Uebergabe-Werkzeugs (tools/zieluebergabe.py).

Es prueft die Uebergabe-Regel aus `docs/PROJEKT_STAND.md` (Abschnitt 0c): ein fremdes aktives
Ziel wird **erkannt**, GENAU die genannte Sitzung kann **sauber beendet** werden, und alles
andere bleibt unberuehrt. Gearbeitet wird ausschliesslich auf einer **Kopie** des Registers
(in einer Zwischendatei) — das echte Register wird nie angefasst.

Aufruf:  python -X utf8 tests/test_zieluebergabe.py
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sqlite3
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import zieluebergabe as Z  # noqa: E402


def register_bauen(pfad, eintraege):
    """Ein kleines Ersatz-Register (nur die Tabelle state_meta) mit den uebergebenen Zielen."""
    if os.path.exists(pfad):
        os.remove(pfad)
    con = sqlite3.connect(pfad)
    con.execute("create table state_meta (key text primary key, value text)")
    for sitzung, status, takte, text in eintraege:
        con.execute("insert into state_meta (key, value) values (?, ?)",
                    (f"goal:{sitzung}", json.dumps({"status": status, "turns_used": takte,
                                                    "max_turns": 20, "goal": text})))
    con.commit()
    con.close()


TEMP = os.path.join(tempfile.gettempdir(), "nebel_zielregister_test.db")

abschnitt("1. Ein fremdes aktives Ziel wird erkannt (Geisterlaeufer)")

register_bauen(TEMP, [
    ("20261005_111111_aaaaaa", "active", 2, "Nebelseetal .exe fertig stellen"),
    ("20261004_222222_bbbbbb", "active", 3, "Nebelseetal .exe fertig stellen"),
    ("20261004_333333_cccccc", "paused", 4, "alte Sache"),
    ("20261004_444444_dddddd", "done", 1, "Sicherheitsregelwerk"),
])
liste = Z.ziele(TEMP)
check("das Register wird gelesen (4 Ziele)", len(liste) == 4, str(len(liste)))
check("die Felder stimmen (Sitzung, Status, Takte, Text)",
      liste[0]["sitzung"] and liste[0]["status"] in ("active", "paused", "done")
      and isinstance(liste[0]["takte"], int) and liste[0]["text"],
      str(liste[0])[:120])
check("aktive Ziele stehen oben", liste[0]["status"] == "active" and liste[1]["status"] == "active",
      str([z["status"] for z in liste]))
geister = Z.fremde_aktive(liste, "20261005_111111_aaaaaa")
check("genau EIN fremdes aktives Ziel gilt als Geisterlaeufer",
      len(geister) == 1 and geister[0]["sitzung"] == "20261004_222222_bbbbbb",
      str([z["sitzung"] for z in geister]))
check("pausierte und erledigte Ziele gelten nicht als Geisterlaeufer",
      all(z["status"] == "active" for z in geister), str(geister))

abschnitt("2. --pruefen meldet es mit Rueckgabewert 1")

code = Z.main(["--db", TEMP, "--pruefen", "--sitzung", "20261005_111111_aaaaaa"])
check("--pruefen liefert 1, solange ein fremdes Ziel aktiv ist", code == 1, str(code))

abschnitt("3. --beenden trifft GENAU die genannte Sitzung")

ok, meldung = Z.beende(TEMP, "20261004_222222_bbbbbb", "Test: sauber beendet")
check("das Beenden meldet Erfolg und nennt den Wechsel",
      ok is True and "cleared" in meldung, meldung)
nachher = {z["sitzung"]: z["status"] for z in Z.ziele(TEMP)}
check("nur die genannte Sitzung ist beendet",
      nachher.get("20261004_222222_bbbbbb") == "cleared"
      and nachher.get("20261005_111111_aaaaaa") == "active"
      and nachher.get("20261004_333333_cccccc") == "paused"
      and nachher.get("20261004_444444_dddddd") == "done",
      str(nachher))
con = sqlite3.connect(f"file:{TEMP}?mode=ro", uri=True)
roh = json.loads(con.execute("select value from state_meta where key=?",
                             ("goal:20261004_222222_bbbbbb",)).fetchone()[0])
con.close()
check("der Grund steht im Datensatz (nachvollziehbar)",
      "Test: sauber beendet" in str(roh.get("paused_reason")), str(roh.get("paused_reason")))
check("das Ziel wird nicht geloescht, sondern auf cleared gesetzt",
      roh.get("status") == "cleared" and str(roh.get("goal")), str(roh)[:80])

ok, meldung = Z.beende(TEMP, "20261001_999999_zzzzzz", "gibt es nicht")
check("eine unbekannte Sitzung wird ehrlich abgelehnt", ok is False and "Kein Ziel" in meldung,
      meldung)

abschnitt("4. Nach der Uebergabe ist die Pruefung still")

code = Z.main(["--db", TEMP, "--pruefen", "--sitzung", "20261005_111111_aaaaaa"])
check("--pruefen liefert 0, wenn nur noch die eigene Sitzung aktiv ist", code == 0, str(code))
code = Z.main(["--db", TEMP, "--pruefen", "--sitzung", "20261009_000000_neu"])
check("aus Sicht einer ganz neuen Sitzung gibt es noch ein aktives (jetzt eigenes) Ziel",
      code == 1, str(code))

abschnitt("5. Der Wiedereinstiegspunkt und die Startzeile")

schritt = Z.naechster_schritt(os.path.join(ROOT, "docs", "AKTUELLER_STAND.md"))
check("der naechste Schritt wird aus dem Uebergabedokument gelesen",
      len(schritt) > 100 and "###" not in schritt, schritt[:100])
check("er nennt den Sammellauf und die Protokollpflicht",
      "Sammellauf" in schritt or "Protokoll" in schritt, schritt[:160])
zeile = Z.startzeile("20261009_000000_neu")
check("die Startzeile nennt die Uebergabe-Datei und die Uebergabe-Pruefung",
      "HERMES_UEBERGABE_AKTUELL.md" in zeile and "zieluebergabe.py --pruefen" in zeile, zeile[:160])
check("die Startzeile nennt /goal und den Sammellauf",
      "/goal" in zeile and "Sammellauf" in zeile)
check("die Startzeile startet NICHTS von allein (kein Sitzungsbefehl)",
      "hermes " not in zeile and "chat -q" not in zeile)

abschnitt("6. Fehlendes Register stuerzt nicht ab")

check("ein fehlendes Register ergibt eine leere Liste", Z.ziele(os.path.join(TEMP, "gibtsnicht")) == [])
ok, meldung = Z.beende(os.path.join(TEMP, "gibtsnicht"), "x", "y")
check("das Beenden eines fehlenden Registers meldet ehrlich", ok is False and "nicht gefunden" in meldung,
      meldung)

abschnitt("7. Ein pausiertes eigenes Ziel wird ehrlich gemeldet — und ist fortsetzbar")

register_bauen(TEMP, [
    ("20261005_111111_aaaaaa", "paused", 3, "Nebelseetal .exe fertig stellen"),
])
puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    code = Z.main(["--db", TEMP, "--pruefen", "--sitzung", "20261005_111111_aaaaaa"])
ausgabe = puffer.getvalue()
check("--pruefen bleibt 0, wenn kein fremdes Ziel aktiv ist", code == 0, str(code))
check("es wird ehrlich gesagt, dass AUCH die eigene Sitzung kein aktives Ziel hat",
      "AUCH DIESE SITZUNG" in ausgabe and "NICHT von selbst weiter" in ausgabe,
      ausgabe[-200:])
check("und der Befehl zum Fortsetzen wird genannt",
      "--fortsetzen 20261005_111111_aaaaaa" in ausgabe, ausgabe[-200:])

ok, meldung = Z.setze_aktiv(TEMP, "20261005_111111_aaaaaa", "Test: Fortsetzung")
check("das Fortsetzen setzt GENAU diese Sitzung auf active",
      ok is True and "active" in meldung
      and {z["sitzung"]: z["status"] for z in Z.ziele(TEMP)}["20261005_111111_aaaaaa"] == "active",
      meldung)
check("ein schon aktives Ziel wird nicht erneut angefasst",
      Z.setze_aktiv(TEMP, "20261005_111111_aaaaaa", "nochmal")[1].endswith("nichts geaendert."))
check("eine unbekannte Sitzung laesst sich nicht fortsetzen",
      Z.setze_aktiv(TEMP, "gibtsnicht", "x")[0] is False)

try:
    os.remove(TEMP)
except OSError:
    pass

sys.exit(bericht())
