# -*- coding: utf-8 -*-
"""Wache: der Spieltest-Verlauf erreicht Einheiten und ein Gefecht, BEVOR er Geld kostet.

Warum diese Datei (belegt 05.11.2026)
-------------------------------------
Der erste 6-Tage-Lauf der Simulation endete mit **0 Einheiten und 0 Kaempfen**, ohne einen einzigen
Grund im Bericht. Drei Ursachen, alle im Messapparat:

1. `GEBAEUDE_REIHENFOLGE` baute nie ein Haus (Eintrag "wohnhaus" - `gelaende.finde_gebaeude` kennt nur
   "haus"), nie eine Schafszucht (Wolle), nie einen Stellmacher (Karren), nie eine Erzmine (Metall).
2. `spielschicht.ware_fertigen` gab die Rezepte nicht an `werkstatt.einreihen` weiter -> `dauer = None`
   -> die Ware wurde NIE fertig. Ohne Ware gibt es keinen Kaempfer.
3. Fehlversuche wurden still verschluckt: `_versuch` lieferte (False, Grund), der Grund landete
   nirgends. Ein Modell haette das Artefakt als Spielbefund gelesen und "Startgold erhoehen" empfohlen.

Was diese Datei beweist
-----------------------
1. Ein 8-Tage-Lauf erzeugt mindestens 2 Einheiten (Also: Werkstatt, Ware und Akademie greifen).
2. Er erzeugt mindestens ein GEFECHT mit Ausgang und Buchung (nicht nur "Kampf versucht").
3. Jeder Eintrag der Baukette ist ein echtes Gebaeude (`finde_gebaeude` findet alle).
4. Der Bericht nennt die Fehlversuche mit Grund (Abschnitt + mindestens eine Zeile).
5. Gegenprobe nach dem Tick: ohne die Rezepte bleibt die Ware liegen - genau der alte Fehler.

Aufruf:  python -X utf8 tests/test_spieltest_erreicht_kampf.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['einheiten', 'forschung', 'gelaende', 'kampfbericht', 'spielschicht', 'werkstatt']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import spieltest_simulation as SIM  # noqa: E402
import gelaende as GE               # noqa: E402
import spielschicht as S            # noqa: E402
import werkstatt as W               # noqa: E402

# ==========================================================================
abschnitt("1. Baukette: jeder Eintrag ist ein echtes Gebaeude")
# ==========================================================================

unbekannt = [g for g in SIM.GEBAEUDE_REIHENFOLGE if GE.finde_gebaeude(g) is None]
check("1 jeder Eintrag der Baukette wird von gelaende.finde_gebaeude gefunden",
      not unbekannt, "unbekannt: %s" % unbekannt)
check("1 die Kette enthaelt eine Werkstatt fuer Waren (Schmiede)",
      "schmiede" in [GE.finde_gebaeude(g) for g in SIM.GEBAEUDE_REIHENFOLGE], "")
check("1 die Kette enthaelt den Stellmacher (Handkarren fuer die Beute)",
      "stellmacher" in [GE.finde_gebaeude(g) for g in SIM.GEBAEUDE_REIHENFOLGE], "")

# ==========================================================================
abschnitt("2. Der Lauf erreicht Einheiten und ein Gefecht")
# ==========================================================================

log = SIM.spielen(8.0, 7)
einheiten = log["ende"]["einheiten"] or {}
anzahl = sum(int(v or 0) for v in einheiten.values())
check("2 der 8-Tage-Lauf bildet mindestens 2 Einheiten aus", anzahl >= 2,
      "Einheiten am Ende: %s" % einheiten)
check("2 mindestens eine Kampfeinheit steht im Heer",
      any(int(v or 0) > 0 for n, v in einheiten.items()
          if __import__("einheiten").rolle(n) == "kaempfer"), str(einheiten))
kaempfe = [k for k in (log.get("kaempfe") or []) if k.get("ok")]
check("2 es kommt mindestens ein Gefecht zustande", len(kaempfe) >= 1,
      "Kaempfe: %s" % (log.get("kaempfe") or []))
check("2 das Gefecht hat einen Ausgang",
      bool(kaempfe) and bool(kaempfe[0].get("ausgang")), str(kaempfe[:1]))
check("2 der Lauf bricht nicht ab (Skip-Mechanik, keine 200 Fehler in Folge)",
      not any("nicht mehr belastbar" in str(e) for e in log.get("ereignisse") or []), "")
check("2 keine Tick-Ausnahme im ganzen Lauf", not (log.get("uebersprungen") or []),
      str((log.get("uebersprungen") or [])[:3]))

# ==========================================================================
abschnitt("3. Fehlversuche stehen mit Grund im Bericht")
# ==========================================================================

fehl = log.get("fehlschlaege") or {}
check("3 der Lauf zaehlt Fehlversuche mit Grund", bool(fehl), "Arten: %s" % list(fehl))
text = SIM.bericht(log, 8.0)
check("3 der Bericht hat den Abschnitt fuer die Grundbilanz",
      "Fehlversuche mit Grund" in text, "")
check("3 der Bericht nennt mindestens einen konkreten Grund",
      any(g in text for g in ("erst bauen", "nicht gebaut", "Zu wenig", "kein passendes Feld")), "")

# ==========================================================================
abschnitt("4. Gegenprobe: ohne Rezepte bleibt die Ware liegen (der alte Fehler)")
# ==========================================================================

zk = S.neuer_zustand()
S.bauen(zk, 0, "schmiede", SIM._feld_fuer(zk["siedlungen"][0], "schmiede"))
# Seit 05.11.2026 prueft und bucht `spielschicht.ware_fertigen` wie der GUI-Weg: Kurzschwert
# braucht Waffentechnik 3 und 4 Metall. Die Probe stellt beides her, weil das SPIEL es verlangt.
zk["forschung"]["Waffentechnik"]["stufe"] = 3
zk["ressourcen"]["metall"] = 10
ok, meldung = S.ware_fertigen(zk, 0, "Kurzschwert", 1, 0.0)
check("4 Kurzschwert laesst sich einreihen", ok is True, meldung)
check("4 die Rezeptkosten sind abgebucht (4 Metall)", zk["ressourcen"]["metall"] == 6,
      str(zk["ressourcen"].get("metall")))
S.tick(zk, 6000, 6000)
check("4 mit Rezepten ist das Kurzschwert nach 6000 s fertig",
      zk["waren"].get("Kurzschwert") == 1, str(zk["waren"]))

# Derselbe Weg OHNE Rezepte - so sah der Code am 05.11.2026 vor dem Fix aus.
zk2 = S.neuer_zustand()
S.bauen(zk2, 0, "schmiede", SIM._feld_fuer(zk2["siedlungen"][0], "schmiede"))
schluessel = "0:schmiede"
schlange = werkstatt_neu = W.neue_warteschlange("schmiede", 1)
zk2.setdefault("werkstaetten", {})[schluessel] = schlange
ok2, meldung2 = W.einreihen(schlange, "Kurzschwert", 1, 1)
S.tick(zk2, 6000, 6000)
check("4 Gegenprobe ohne Rezepte: keine Ware im Lager (dauer = None)",
      zk2["waren"].get("Kurzschwert", 0) == 0, str(zk2["waren"]))
check("4 Gegenprobe: die Warteschlange selbst kennt keine Dauer",
      all(e.get("dauer") is None for e in (schlange.get("einheiten") or [])),
      str(schlange.get("einheiten")))

# ==========================================================================
abschnitt("5. Angriff ohne Karren ist erlaubt, Beute dann leer (Daniel 05.11.2026)")
# ==========================================================================

# Die Regel steht im KERN (spielschicht.angriff + kampfbericht): Kaempfer allein duerfen angreifen,
# die Beute ist durch die Karrenladung begrenzt - ohne Karren also 0. Die Wache sichert beides.
zo = S.neuer_zustand()
# Fixture: zwei Buergerwehr direkt ins Heer (die Entstehung selbst prueft Abschnitt 2 am Lauf).
zo["einheiten"]["Bürgerwehr"] = 2
ziel = {"name": "Bot-Siedlung", "wall_stufe": 0, "wall_zustand_prozent": 100.0,
        "vorraete": {"holz": 400.0, "stein": 300.0}}
ok_o, ergebnis_o = S.angriff(zo, ziel, 3600.0)
check("5 ein Angriff ohne Karren wird ausgefuehrt", ok_o is True,
      str((ergebnis_o or {}).get("grund") or (ergebnis_o or {}).get("ergebnis")))
beute = ((ergebnis_o or {}).get("beute") or {})
check("5 ohne Karren ist die Beute leer (Karrenladung ist die Grenze)", not beute, str(beute))

sys.exit(bericht())
