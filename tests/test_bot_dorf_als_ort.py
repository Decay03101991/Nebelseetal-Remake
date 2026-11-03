# -*- coding: ascii -*-
"""S-1: ein Bot-Dorf ist ein ORT wie eine Spielersiedlung (03.11.2026).

Daniels Vorgabe: "bots wirkliche gegner ... sie muessen die selben mechaniken nutzen". Der erste
Schritt dahin ist das DATENMODELL: ein Bot-Dorf bekommt die Felder eines Ortes (Karte als Raster,
Bauplaetze, Stufen, Einheiten, Bevoelkerung, Warteschlangen) und laesst sich in die Form bringen,
mit der der Kern rechnet.

Was diese Datei beweist
-----------------------
1. `bot_dorf_als_ort` liefert ein dict, in dem `karte` das 10x10-RASTER ist - nicht die Kennung
   (der Fallstrick aus der Uebergabe: `originalkarten.alle()` liefert Dicts, `karte()` ein Dict).
2. Der Kern rechnet damit: `wirtschaft.ertrag_gesamt` liest die EIGENEN Felder des Bot-Dorfes,
   und der Volksfaktor (V-5) gilt auch hier.
3. `spieloekonomie.ort_tick` bucht auf dem Bot-Dorf: Ernte, Bevoelkerung - und bei Einheiten im
   Ort den NAHRUNGSVERBRAUCH (8 je Einheit und Tag), den Daniel verlangt hat.
4. Der Rueckweg `bot_dorf_aus_ort` schreibt das Ergebnis ins Dorf, ohne die Kartenkennung zu
   verlieren.
5. Alte Spielstaende laden weiter: ein Bot-Dorf ohne die neuen Felder bekommt Vorgaben.

Aufruf:  python -X utf8 tests/test_bot_dorf_als_ort.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende  # noqa: E402
import main as M  # noqa: E402
import spieloekonomie as O  # noqa: E402
import wirtschaft as W  # noqa: E402

# ==========================================================================
# 1. Der Ort aus dem Bot-Dorf: Raster, nicht Kennung
# ==========================================================================
abschnitt("1. Bot-Dorf -> Ort (karte ist ein RASTER)")
_bot = M.BotPlayer("Grom", "zwergisch", 0.5, 0.5, settlements=["Gromsdorf"])
_dorf = M.bot_doerfer_sicherstellen(_bot)[0]
_dorf.karte = "original-036"
_ort = M.bot_dorf_als_ort(_dorf, _bot)
check("der Ort traegt die Karte als DICT", isinstance(_ort.get("karte"), dict), type(_ort.get("karte")).__name__)
check("die Karte hat 10x10 Felder", _ort["karte"].get("spalten") == 10
      and _ort["karte"].get("zeilen") == 10 and len(_ort["karte"].get("raster") or []) == 100,
      str((_ort["karte"].get("spalten"), _ort["karte"].get("zeilen"), len(_ort["karte"].get("raster") or []))))
check("die Originalkennung steht in der Karte", _ort["karte"].get("originalkarte_id") == "original-036",
      str(_ort["karte"].get("originalkarte_id")))
check("das Volk kommt vom Bot", _ort.get("volk") == "zwergisch", str(_ort.get("volk")))
check("das Dorf behaelt seine Kennung fuer die Anzeige", _dorf.karte == "original-036", _dorf.karte)
check("alle Felder eines Ortes sind da",
      all(k in _ort for k in ("karte", "bauten", "stufen", "einheiten", "vorraete",
                              "bevoelkerung", "waren", "werkstaetten", "ausbildung",
                              "produktionsjournal", "fertigjournal")), str(sorted(_ort)))

# ==========================================================================
# 2. Der Kern rechnet damit
# ==========================================================================
abschnitt("2. Der Ertrag kommt aus den EIGENEN Feldern des Bot-Dorfes")
_raster = list(_ort["karte"]["raster"])
_wald = next(i for i, a in enumerate(_raster) if a == "wald")
_ohne = W.ertrag_gesamt([dict(_ort, bauten={})])
check("ohne Gebaeude bleibt nur das Grundeinkommen (1 Holz / 1 Stein, mit Volksfaktor)",
      abs(float(_ohne.get("Holz", 0)) - 0.95) < 1e-9 and abs(float(_ohne.get("Stein", 0)) - 1.05) < 1e-9,
      str(_ohne))
_dorf.bauten = {str(_wald): "holzfaeller"}
_mit = W.ertrag_gesamt([M.bot_dorf_als_ort(_dorf, _bot)])
check("mit Holzfaeller auf Wald kommt der Feldertrag dazu (3,8 + 0,95 Grundeinkommen = 4,75)",
      abs(float(_mit.get("Holz", 0)) - 4.75) < 1e-9, f"Holz {_mit.get('Holz')}")
check("der Volksfaktor wirkt auch beim Bot (zwergisch: Holz -5 %, Stein +5 %)",
      abs(float(_mit.get("Stein", 0)) - 1.05) < 1e-9, f"Stein {_mit.get('Stein')}")
check("der Ertrag des Ortes ist der des Kerns (Siedlung + Grundeinkommen, eine Wahrheit)",
      abs(float(_mit.get("Holz", 0))
          - round(float(W.siedlung_ertrag(M.bot_dorf_als_ort(_dorf, _bot))["Holz"]) + 0.95, 2)) < 1e-9,
      str(_mit))

# ==========================================================================
# 3. ort_tick bucht auf dem Bot-Dorf - inklusive Nahrungsverbrauch
# ==========================================================================
abschnitt("3. Ort-Tick: Ernte, Bevoelkerung und Futter der Garnison")
_dorf.vorraete = {"nahrung": 100.0}
_dorf.einheiten = {}
_dorf.bevoelkerung = 10.0
_ort = M.bot_dorf_als_ort(_dorf, _bot)
_neu = O.ort_tick(_ort, 0.0, 3600.0, {})
check("eine Stunde erntet (das Journal hat eine Zeile)", len(_neu.get("produktionsjournal") or []) == 1,
      str(len(_neu.get("produktionsjournal") or [])))
check("ohne Einheiten isst niemand", abs(float(_neu["vorraete"].get("nahrung", 0)) - 100.0) < 1e-6,
      str(_neu["vorraete"].get("nahrung")))
_dorf.einheiten = {"Krieger": 30}
_ort2 = M.bot_dorf_als_ort(_dorf, _bot)
_neu2 = O.ort_tick(_ort2, 0.0, 3600.0, {})
_verbrauch = 100.0 - float(_neu2["vorraete"].get("nahrung", 0)) + float(
    (_neu2.get("produktionsjournal") or [{}])[-1].get("mengen", {}).get("nahrung", 0))
check("30 Einheiten essen 8 x 30 / 24 = 10 Nahrung je Stunde",
      abs(_verbrauch - 10.0) < 0.51, f"Verbrauch {_verbrauch:.3f}")
check("der Verbrauch steht als eigener Posten im Journal",
      bool((_neu2.get("produktionsjournal") or [{}])[-1].get("verbrauch")),
      str((_neu2.get("produktionsjournal") or [{}])[-1].get("verbrauch")))
check("die Bevoelkerung waechst (Siedlerzuwachs wie beim Spieler)",
      float(_neu2.get("bevoelkerung", 0)) >= 10.0, str(_neu2.get("bevoelkerung")))

# ==========================================================================
# 4. Rueckweg ins Dorf
# ==========================================================================
abschnitt("4. Ort -> Bot-Dorf (Rueckweg)")
M.bot_dorf_aus_ort(_dorf, _neu2)
check("die Vorraete sind zurueckgeschrieben", _dorf.vorraete.get("nahrung") is not None,
      str(_dorf.vorraete))
check("die Garnison steht im Dorf", int(_dorf.einheiten.get("Krieger", 0)) == 30, str(_dorf.einheiten))
check("die Kartenkennung ist unangetastet", _dorf.karte == "original-036", _dorf.karte)
check("das Journal ist im Dorf angekommen", len(_dorf.produktionsjournal) == 1,
      str(len(_dorf.produktionsjournal)))

# ==========================================================================
# 5. Alte Spielstaende und leere Faelle
# ==========================================================================
abschnitt("5. Alte Spielstaende und leere Faelle")
_alt = M.BotDorf(**{"name": "Alt", "vorraete": {"holz": 3}})
check("ein alter Bot-Dorf-Datensatz laedt weiter", _alt.bauten == {} and _alt.stufen == {}
      and _alt.einheiten == {} and _alt.bevoelkerung == 0.0)
check("die Kartenfelder haben Vorgaben", _alt.karte_daten == {} and _alt.waren == {}
      and _alt.ausbildung == [] and _alt.forschungsauftrag is None)
_leer = M.bot_dorf_als_ort(M.BotDorf(name="Ohne Karte"))
check("ein Dorf ohne Karte ergibt keinen Ertrag, aber keinen Absturz",
      W.ertrag_gesamt([_leer]) == {}, str(W.ertrag_gesamt([_leer])))
check("ohne Karte bleibt die Karte leer", _leer.get("karte") == {}, str(_leer.get("karte")))
check("der Rueckweg stuerzt bei leerem Ort nicht ab",
      isinstance(M.bot_dorf_aus_ort(M.BotDorf(name="X"), {}), M.BotDorf))

bericht()
