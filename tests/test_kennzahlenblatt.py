# -*- coding: utf-8 -*-
"""Wache: das Kennzahlenblatt misst eine Partie vollstaendig, wiederholbar und ohne Nebenwirkung.

Ablauf Schritt 2 (docs/ABLAUF_LLM_20261106.md, Daniel 06.11.2026): ab dem Rachetopf veraendert
jeder Umbau das Spielgefuehl - ohne eine Vorher-Zahl ist "besser" nur ein Gefuehl. Diese Datei
beweist fuenf Dinge:

1. Jede Zeile traegt ALLE Pflichtschluessel und keine fremden.
2. Zwei Laeufe mit demselben Startwert und demselben Stand ergeben eine IDENTISCHE Zeile
   (dafuer bekommt der Lauf einen festen Zufallsgenerator).
3. Ein nicht erreichter Meilenstein ist `null` - und ein bei Tag 0 erreichter bleibt 0
   (sonst ist "nicht erreicht" von "sofort erreicht" nicht zu unterscheiden).
4. `daten_hash` aendert sich, sobald eine Datendatei sich aendert, und bleibt sonst gleich.
5. Das Werkzeug schreibt AUSSCHLIESSLICH unter `docs/balancing/` - `data/` und `src/` bleiben
   Byte fuer Byte unberuehrt; eine halbe Zeile (fehlender Schluessel) wird abgelehnt.

Aufruf:  python -X utf8 tests/test_kennzahlenblatt.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['diplomatie']
PRUEF_DATEN = ['resources.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import hashlib
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import spieltest_simulation as SIM  # noqa: E402

TAGE = 3.0                                    # kurze Partie: die Wache soll Sekunden kosten
SAAT = 7


def _zeile(tage=TAGE, saat=SAAT, stil="breit", wurzel=ROOT):
    """Eine Kennzahlenzeile aus einem echten Lauf - kein zusammengebautes Dikt."""
    return SIM.kennzahlen(SIM.spielen(tage, saat, stil), tage, saat, stil, wurzel=wurzel)


def _dateien(wurzel):
    """Alle Dateien unter einem Ordner mit ihrer Pruefsumme - fuer den Vorher/Nachher-Vergleich."""
    stand = {}
    for pfad, _ordner, namen in os.walk(wurzel):
        for name in namen:
            voll = os.path.join(pfad, name)
            with open(voll, "rb") as f:
                stand[os.path.relpath(voll, wurzel)] = hashlib.sha256(f.read()).hexdigest()
    return stand


# ==========================================================================
abschnitt("1. Pflichtschluessel: alle da, keine fremden")
# ==========================================================================

zeile = _zeile()
check("1 die Zeile hat genau die Pflichtschluessel",
      tuple(sorted(zeile)) == tuple(sorted(SIM.KENNZAHLEN_PFLICHT)),
      f"{len(zeile)} Schluessel gegen {len(SIM.KENNZAHLEN_PFLICHT)} Pflicht")
check("1 der Startwert ist die volle Eingabe (Saat, Stil, Tage)",
      zeile.get("startwert") == {"saat": SAAT, "stil": "breit", "tage": TAGE},
      json.dumps(zeile.get("startwert"), sort_keys=True))
check("1 der Stand nennt einen Kopf-Commit", bool((zeile.get("stand") or {}).get("kopf")),
      json.dumps(zeile.get("stand"), sort_keys=True))
check("1 der Datenhash hat die Form 'sha256:<32 Hexzeichen>'",
      str(zeile.get("daten_hash", "")).startswith("sha256:")
      and len(zeile.get("daten_hash", "")) == len("sha256:") + 32,
      str(zeile.get("daten_hash"))[:20])
check("1 die Fehlschlaege sind Dreierlisten (Aktion, Grund, Anzahl)",
      all(isinstance(z, list) and len(z) == 3 and isinstance(z[2], int)
          for z in zeile.get("fehlschlaege") or []),
      f"{len(zeile.get('fehlschlaege') or [])} Gruende")

# ==========================================================================
abschnitt("2. Derselbe Startwert und derselbe Stand ergeben dieselbe Zeile")
# ==========================================================================

zeile_b = _zeile()
ja = json.dumps(zeile, sort_keys=True, ensure_ascii=False)
jb = json.dumps(zeile_b, sort_keys=True, ensure_ascii=False)
check("2 zwei Laeufe sind Zeichen fuer Zeichen gleich", ja == jb, f"{len(ja)} Zeichen")
# Gegenprobe: eine ANDERE Saat muss eine andere Zeile ergeben - sonst misst der Startwert nichts.
zeile_c = _zeile(saat=11)
check("2 eine andere Saat ergibt eine andere Zeile",
      json.dumps(zeile_c, sort_keys=True) != ja, "")

# ==========================================================================
abschnitt("3. Ein fehlender Meilenstein ist null, ein frueher bleibt 0")
# ==========================================================================

leer = SIM.kennzahlen({}, TAGE, SAAT, "breit", wurzel=ROOT)
felder = ("tag_erstes_haus", "tag_erste_bibliothek", "tag_erste_ware",
          "tag_erster_krieger", "tag_erstes_gefecht", "ruhm_stufe", "handelspunkte")
check("3 ohne Lauf sind alle Meilensteine null",
      all(leer.get(k) is None for k in felder),
      json.dumps({k: leer.get(k) for k in felder}, sort_keys=True))
check("3 fehlende Meilensteine sind NICHT 0",
      all(leer.get(k) != 0 for k in felder), "")
frueh = SIM.kennzahlen({"meilensteine": {"tag_erstes_haus": 0.0}}, TAGE, SAAT, "breit", wurzel=ROOT)
check("3 ein bei Tag 0 erreichter Meilenstein bleibt 0 (nicht null)",
      frueh.get("tag_erstes_haus") == 0.0 and frueh.get("tag_erstes_haus") is not None,
      repr(frueh.get("tag_erstes_haus")))
# Leerlauf ohne Aktionen: die ganze Partie ist Stillstand - aber als ZAHL, nicht als null.
check("3 ein Lauf ohne Aktionen zaehlt seinen Leerlauf",
      leer.get("leerlauf_sek") == 0, "ohne Schritte gibt es auch keine Sekunden Leerlauf")
check("3 die groesste Luecke ohne Meilenstein ist die ganze Partie",
      leer.get("abstand_meilensteine_max") == TAGE, repr(leer.get("abstand_meilensteine_max")))

# ==========================================================================
abschnitt("4. Der Datenhash folgt dem Datenstand")
# ==========================================================================

tmp = tempfile.mkdtemp(prefix="nebel_kennzahlen_")
try:
    os.makedirs(os.path.join(tmp, "data"), exist_ok=True)
    quelle = os.path.join(ROOT, "data", "resources.json")
    ziel_daten = os.path.join(tmp, "data", "resources.json")
    shutil.copyfile(quelle, ziel_daten)
    h1 = SIM.daten_hash(tmp)
    h2 = SIM.daten_hash(tmp)
    check("4 gleicher Inhalt ergibt denselben Hash", h1 == h2, h1[:22])
    with open(ziel_daten, "a", encoding="utf-8") as f:
        f.write("\n")
    h3 = SIM.daten_hash(tmp)
    check("4 geaenderte Datendatei ergibt einen anderen Hash", h3 != h1, f"{h1[:16]} -> {h3[:16]}")
    h4 = SIM.daten_hash(ROOT)
    check("4 der Hash des Projekts ist stabil", h4 == SIM.daten_hash(ROOT), h4[:22])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ==========================================================================
abschnitt("5. Schreiben nur unter docs/balancing, halbe Zeile wird abgelehnt")
# ==========================================================================

tmp2 = tempfile.mkdtemp(prefix="nebel_kennzahlen_schreiben_")
try:
    os.makedirs(os.path.join(tmp2, "data"), exist_ok=True)
    os.makedirs(os.path.join(tmp2, "src"), exist_ok=True)
    for unter, name in (("data", "resources.json"), ("src", "diplomatie.py")):
        quelle = os.path.join(ROOT, unter, name)
        if os.path.isfile(quelle):
            shutil.copyfile(quelle, os.path.join(tmp2, unter, name))
    vorher = _dateien(tmp2)
    ablage = SIM.kennzahlen_schreiben(_zeile(wurzel=tmp2), wurzel=tmp2)
    nachher = _dateien(tmp2)
    neu = sorted(set(nachher) - set(vorher))
    geaendert = sorted(k for k in set(vorher) & set(nachher) if vorher[k] != nachher[k])
    check("5 geschrieben wurde nur unter docs/balancing",
          all(n.replace("\\", "/").startswith("docs/balancing/") for n in neu) and not geaendert,
          f"neu: {neu} | geaendert: {geaendert}")
    check("5 JSONL und Markdown liegen am angekuendigten Ort",
          ablage["jsonl"].replace("\\", "/").endswith("docs/balancing/kennzahlen.jsonl")
          and ablage["markdown"].replace("\\", "/").endswith(".md"), str(ablage["jsonl"]))
    with open(ablage["jsonl"], encoding="utf-8") as f:
        gespeichert = [json.loads(z) for z in f.read().splitlines() if z.strip()]
    check("5 die abgelegte Zeile ist vollstaendig und ohne Zeitstempel",
          len(gespeichert) == 1 and sorted(gespeichert[0]) == sorted(SIM.KENNZAHLEN_PFLICHT)
          and "zeit" not in gespeichert[0], f"{len(gespeichert)} Zeile(n)")
    with open(ablage["markdown"], encoding="utf-8") as f:
        md = f.read()
    check("5 die Markdown-Fassung hat Tabelle, Legende und Determinismus-Hinweis",
          "| # | Stand |" in md and "## Legende" in md and "Determinismus" in md, f"{len(md)} Zeichen")
    def _halb():
        """Eine Zeile mit fehlendem Pflichtschluessel - muss abgelehnt werden."""
        SIM.kennzahlen_schreiben({"stand": {}}, wurzel=tmp2)
    versucht = False
    try:
        _halb()
    except ValueError as fehler:
        versucht = "Pflichtschluessel" in str(fehler)
    check("5 eine halbe Zeile wird abgelehnt statt ergaenzt", versucht, "")
    check("5 die Ablehnung hat nichts geschrieben",
          sorted(_dateien(tmp2)) == sorted(nachher), "")
finally:
    shutil.rmtree(tmp2, ignore_errors=True)

sys.exit(bericht())
