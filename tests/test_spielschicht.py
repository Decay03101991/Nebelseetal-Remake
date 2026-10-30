"""
FACH-SCHICHT (Spielebene) von Nebelseetal — Pruefung (Paket W7, 04.10.2026).

Beweist, dass ``src/spielschicht.py`` die GUI-Aktionen traegt und dabei die
Kindmodule richtig benutzt:

  * ein neuer Zustand ist ein serialisierbares dict (json.dumps),
  * bauen / ausbauen / abreissen kosten und buchen exakt, Fehlversuche aendern nichts,
  * Forschung steigt ERST nach der Zeit (nicht beim Klick) und braucht eine Bibliothek,
  * die Werkstatt liefert nach der BELEGTEN Zeit (Handbuchbeispiel 10 Schwerter mit
    2 Schmieden = 100 min),
  * Ausbildung nur mit der passenden Ausbildungsstaette,
  * ein Angriff laeuft ueber kampfbericht (Vorrunde, Mauerschaden, Beute, Bericht),
  * die Punkte kommen aus ``src/punkte.py``,
  * tick sammelt Ereignisse und wiederholt sie bei gleichem Zeitstempel nicht.

Aufruf:  python -X utf8 tests/test_spielschicht.py
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import spielschicht as S
import forschung as F
import gebaeude_wirkung as GW
import gelaende as G
import punkte as P
import werkstatt as W

TAG = 86400


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def raster(z):
    return z["siedlungen"][0]["karte"]["raster"]


def feld(z, arten=None):
    """Ein freies, bebaubares Feld (optional nur bestimmter Gelaendearten)."""
    bauten = z["siedlungen"][0]["bauten"]
    for i, a in enumerate(raster(z)):
        if str(i) in bauten or a == G.SUMPF:
            continue
        if arten is None or a in arten:
            return i
    return None


def eingefroren(z):
    """Der Zustand als Text — fuer 'hat sich nichts geaendert?'."""
    return json.dumps(z, sort_keys=True, ensure_ascii=False)


# Gelaenderegeln (Vorgabe Daniel 05.10.2026, data/buildings.json): jedes Gebaeude hat jetzt eine
# Eignungsregel. Die Pruefungen waehlen ihre Felder deshalb nach der Regel, nicht beliebig.
_SCHMIEDE_FELDER = {"grasland", "steppe", "huegel", "berg"}
_AKADEMIE_FELDER = {"grasland", "steppe", "huegel"}
_GILDE_FELDER = {"grasland", "steppe", "wald"}
_WALL_FELDER = {"grasland", "steppe", "wald", "huegel", "berg"}


def leeres_feld(z):
    """Ein Feld OHNE Gebaeude (fuer die Abriss-Fehlerpruefung)."""
    bauten = z["siedlungen"][0]["bauten"]
    for i in range(len(raster(z))):
        if str(i) not in bauten:
            return i
    return None


# ==========================================================================
# 1. Der Zustand selbst
# ==========================================================================

abschnitt("1. Neuer Zustand — rein, serialisierbar, tkinter-frei")

z0 = S.neuer_zustand()

check("spielschicht laeuft ohne tkinter", "tkinter" not in sys.modules,
      "tkinter ist nicht geladen")
check("die GUI-Datei main.py wurde nicht mitgeladen", "main" not in sys.modules)
check("neuer_zustand() liefert ein dict", isinstance(z0, dict))
check("die Pflichtschluessel liegen vor",
      all(k in z0 for k in ("ressourcen", "siedlungen", "forschung", "einheiten",
                            "waren", "werkstaetten", "ereignisse", "bevoelkerung")))
check("alle neun Originalrohstoffe liegen vor",
      sorted(z0["ressourcen"].keys()) == sorted(["holz", "stein", "metall", "mana",
                                                  "nahrung", "gold", "wolle", "leder", "pferde"]),
      str(sorted(z0["ressourcen"].keys())))
check("Startwerte 100 Holz / 100 Stein (Handbuch S. 7)",
      z0["ressourcen"]["holz"] == 100 and z0["ressourcen"]["stein"] == 100)
check("uebrige Rohstoffe starten bei 0",
      all(z0["ressourcen"][r] == 0 for r in ("metall", "mana", "nahrung", "gold", "wolle",
                                             "leder", "pferde")))
check("10 Siedler zum Start (Handbuch S. 7)", z0["bevoelkerung"] == 10)
check("genau eine Start-Siedlung mit eigener Karte",
      len(z0["siedlungen"]) == 1 and isinstance(z0["siedlungen"][0].get("karte"), dict))
# GPT-FIX01 (28.10.2026): Das alte 8x7/40-Felder-Pilotmodell wurde
# durch Originalkarten mit 10x10 Raster abgeloest. Die Zahl bebaubarer
# Felder ist KARTENABHAENGIG und damit keine feste 40/86-Konstante.
_startkarte = z0["siedlungen"][0]["karte"]
_baubar = sum(typ != G.SUMPF for typ in raster(z0))
check("die Startkarte hat das 10x10-Originalraster und einen passenden Bauplatzzaehler",
      len(raster(z0)) == 100 and _startkarte.get("bauplaetze") == _baubar,
      f"{len(raster(z0))} Felder, {_startkarte.get('bauplaetze')} Bauplaetze, "
      f"nachgerechnet {_baubar}")

_gebiete = sorted(z0["forschung"].keys())
check("der Forschungsstand sind die 21 Originalgebiete",
      len(_gebiete) == 21, f"{len(_gebiete)} Gebiete")
check("alle Forschungsgebiete starten auf Stufe 0",
      all(e["stufe"] == 0 for e in z0["forschung"].values()))
check("der neue Zustand ist mit json.dumps serialisierbar",
      bool(ausnahme("json.dumps", lambda: json.dumps(z0))))
_text = json.dumps(z0, ensure_ascii=False)
check("json.loads gibt den Zustand unveraendert zurueck",
      json.loads(_text) == z0)
check("die Ereignisliste ist am Anfang leer", S.ereignisse(z0) == [])
check("werkstaetten-Bestand ist am Anfang leer", z0["werkstaetten"] == {})


# ==========================================================================
# 2. Bauen
# ==========================================================================

abschnitt("2. Bauen — Kosten, Bebauung, Fehlversuche")

zb = S.neuer_zustand()
_vor = eingefroren(zb)
ok, meldung = S.bauen(zb, 0, "gibtsnicht", 0)
check("unbekanntes Gebaeude wird abgelehnt", ok is False and bool(meldung), meldung)
check("unbekanntes Gebaeude aendert den Zustand nicht", eingefroren(zb) == _vor)

ok, meldung = S.bauen(zb, 7, "haus", 0)
check("unbekannte Siedlung wird abgelehnt", ok is False and "Siedlung" in meldung, meldung)
check("unbekannte Siedlung aendert den Zustand nicht", eingefroren(zb) == _vor)

ok, meldung = S.bauen(zb, 0, "haus", 999)
check("Feld ausserhalb der Karte wird abgelehnt", ok is False and "Feld" in meldung, meldung)

_gras = feld(zb, {"grasland", "steppe", "nebelsee"})
ok, meldung = S.bauen(zb, 0, "holzfaeller", _gras)
check("falsches Gelaende (Holzfaeller ohne Wald) wird abgelehnt",
      ok is False and "liefert" in meldung, meldung)
check("abgelehnter Bau aendert nichts", eingefroren(zb) == _vor)

_wald = feld(zb, {"wald"})
ok, meldung = S.bauen(zb, 0, "holzfaeller", _wald)
check("Holzfaeller auf Wald wird gebaut", ok is True, meldung)
check("der Bau bucht 10 Holz ab", zb["ressourcen"]["holz"] == 90, str(zb["ressourcen"]["holz"]))
check("der Bau bucht 5 Stein ab", zb["ressourcen"]["stein"] == 95, str(zb["ressourcen"]["stein"]))
check("der Bau verbraucht 1 Siedler", zb["bevoelkerung"] == 9, str(zb["bevoelkerung"]))
check("das Feld traegt das Gebaeude",
      zb["siedlungen"][0]["bauten"].get(str(_wald)) == "holzfaeller",
      str(zb["siedlungen"][0]["bauten"]))
check("das neue Gebaeude hat Stufe 1",
      zb["siedlungen"][0]["stufen"].get(str(_wald)) == 1)

ok, meldung = S.bauen(zb, 0, "holzfaeller", _wald)
check("ein belegtes Feld wird abgelehnt", ok is False and "belegt" in meldung, meldung)
check("belegtes Feld aendert nichts", zb["siedlungen"][0]["bauten"].get(str(_wald)) == "holzfaeller")

# leere Kasse
zk = S.neuer_zustand()
zk["ressourcen"]["holz"] = 0
zk["ressourcen"]["stein"] = 0
_vor = eingefroren(zk)
_w = feld(zk, {"wald"})
ok, meldung = S.bauen(zk, 0, "holzfaeller", _w)
check("zu wenig Rohstoffe wird abgelehnt", ok is False and "fehlen" in meldung, meldung)
check("zu wenig Rohstoffe aendert nichts", eingefroren(zk) == _vor)

# max_je_siedlung: Bibliothek je Siedlung nur einmal
zmax = S.neuer_zustand()
_g1 = feld(zmax, {"grasland", "steppe", "nebelsee"})
S.bauen(zmax, 0, "bibliothek", _g1)
_g2 = feld(zmax, {"grasland", "steppe", "nebelsee"})
_vor = eingefroren(zmax)
ok, meldung = S.bauen(zmax, 0, "bibliothek", _g2)
check("die zweite Bibliothek je Siedlung wird abgelehnt",
      ok is False and "hoechstens" in meldung, meldung)
check("abgelehnte Bibliothek aendert nichts", eingefroren(zmax) == _vor)

# zwei Werkstaetten derselben Art sind erlaubt (Warteschlange parallel)
zw = S.neuer_zustand()
_p1, _p2 = feld(zw, _SCHMIEDE_FELDER), None
S.bauen(zw, 0, "schmiede", _p1)
_p2 = feld(zw, _SCHMIEDE_FELDER)
ok, meldung = S.bauen(zw, 0, "schmiede", _p2)
check("eine zweite Schmiede ist erlaubt (max_je_siedlung leer)", ok is True, meldung)
_bestand = GW.bestand(zw["siedlungen"]).get("schmiede")
check("zwei Schmiede stehen auf der Karte", _bestand == 2, str(_bestand))


# ==========================================================================
# 3. Ausbauen
# ==========================================================================

abschnitt("3. Ausbauen — nur wo belegte Stufen, n-facher Preis")

za = S.neuer_zustand()
_leer = leeres_feld(za)
ok, meldung = S.ausbauen(za, 0, _leer)
check("Ausbau auf leerem Feld wird abgelehnt", ok is False and "kein Gebaeude" in meldung, meldung)

_wh = feld(za, {"wald"})
S.bauen(za, 0, "holzfaeller", _wh)
_vor = eingefroren(za)
ok, meldung = S.ausbauen(za, 0, _wh)
check("Ausbau ohne belegte Stufen (Holzfaeller) wird abgelehnt",
      ok is False and "keine Stufen" in meldung, meldung)
check("abgelehnter Ausbau aendert nichts", eingefroren(za) == _vor)

# Wall: 16 Holz + 16 Stein Grundpreis, Stufe 2 kostet das Doppelte
zwall = S.neuer_zustand()
_wf = feld(zwall, _WALL_FELDER)
ok, meldung = S.bauen(zwall, 0, "verteidigungswall", _wf)
check("Verteidigungswall wird gebaut", ok is True, meldung)
_h1, _s1 = zwall["ressourcen"]["holz"], zwall["ressourcen"]["stein"]
ok, meldung = S.ausbauen(zwall, 0, _wf)
check("Wall auf Stufe 2 ausgebaut", ok is True, meldung)
check("Ausbau auf Stufe 2 kostet das n-fache (32 Holz)",
      _h1 - zwall["ressourcen"]["holz"] == 32, str(_h1 - zwall["ressourcen"]["holz"]))
check("Ausbau auf Stufe 2 kostet 32 Stein",
      _s1 - zwall["ressourcen"]["stein"] == 32, str(_s1 - zwall["ressourcen"]["stein"]))
check("die Wallstufe ist jetzt 2",
      zwall["siedlungen"][0]["stufen"].get(str(_wf)) == 2)

# ueber die belegte Hoechststufe hinaus
zwall["siedlungen"][0]["stufen"][str(_wf)] = GW.max_stufe("verteidigungswall")
zwall["ressourcen"]["holz"] = 10000
zwall["ressourcen"]["stein"] = 10000
_vor = eingefroren(zwall)
ok, meldung = S.ausbauen(zwall, 0, _wf)
check("Ausbau ueber die Hoechststufe (10) wird abgelehnt",
      ok is False and "hoechste" in meldung, meldung)
check("abgelehnter Ausbau ueber Hoechststufe aendert nichts", eingefroren(zwall) == _vor)

# Ausbau ohne Rohstoffe
zarm = S.neuer_zustand()
_af = feld(zarm, _WALL_FELDER)
S.bauen(zarm, 0, "verteidigungswall", _af)
zarm["ressourcen"]["holz"] = 0
zarm["ressourcen"]["stein"] = 0
_vor = eingefroren(zarm)
ok, meldung = S.ausbauen(zarm, 0, _af)
check("Ausbau ohne Rohstoffe wird abgelehnt", ok is False and "fehlen" in meldung, meldung)
check("Ausbau ohne Rohstoffe aendert nichts", eingefroren(zarm) == _vor)


# ==========================================================================
# 4. Abreissen
# ==========================================================================

abschnitt("4. Abreissen — Feld frei, keine Erstattung (belegte Regel)")

zr = S.neuer_zustand()
_leer = leeres_feld(zr)
ok, meldung = S.abreissen(zr, 0, _leer)
check("Abriss ohne Gebaeude wird abgelehnt", ok is False and "kein Gebaeude" in meldung, meldung)

_wr = feld(zr, {"wald"})
S.bauen(zr, 0, "holzfaeller", _wr)
_h, _s = zr["ressourcen"]["holz"], zr["ressourcen"]["stein"]
ok, meldung = S.abreissen(zr, 0, _wr)
check("Abriss gelingt", ok is True, meldung)
check("das Feld ist wieder frei", str(_wr) not in zr["siedlungen"][0]["bauten"])
check("der Stufen-Eintrag ist entfernt", str(_wr) not in zr["siedlungen"][0]["stufen"])
check("Abriss erstattet keine Rohstoffe (belegte Regel)",
      zr["ressourcen"]["holz"] == _h and zr["ressourcen"]["stein"] == _s)
ok, meldung = S.bauen(zr, 0, "holzfaeller", _wr)
check("auf dem freien Feld laesst sich wieder bauen", ok is True, meldung)
check("der Abriss steht in den Nachrichten",
      any("abgerissen" in e["text"] for e in S.ereignisse(zr)))


# ==========================================================================
# 5. Forschung
# ==========================================================================

abschnitt("5. Forschung — Bibliothek noetig, Stufe steigt erst nach der Zeit")

zf = S.neuer_zustand()
_vor = eingefroren(zf)
ok, meldung = S.forschung_starten(zf, "Forstwirtschaft", 0.0)
check("Forschung ohne Bibliothek wird abgelehnt", ok is False and "Bibliothek" in meldung, meldung)
check("abgelehnte Forschung aendert nichts", eingefroren(zf) == _vor)

# Bibliothek bauen
_gb = feld(zf, {"grasland", "steppe", "nebelsee"})
ok, meldung = S.bauen(zf, 0, "bibliothek", _gb)
check("Bibliothek fuer die Forschung gebaut", ok is True, meldung)
_h_vor = zf["ressourcen"]["holz"]
ok, meldung = S.forschung_starten(zf, "Forstwirtschaft", 0.0)
check("mit Bibliothek startet die Forschung", ok is True, meldung)
check("die Startkosten (50 Holz, Stufe 1) werden abgebucht",
      _h_vor - zf["ressourcen"]["holz"] == 50, str(_h_vor - zf["ressourcen"]["holz"]))
check("die Stufe steigt NICHT beim Klick", zf["forschung"]["Forstwirtschaft"]["stufe"] == 0)

_stand = S.forschung_stand(zf, 1800)
_fw = _stand["Forstwirtschaft"]
check("forschung_stand zeigt den laufenden Auftrag", _fw["laufend"] is True)
check("forschung_stand nennt 0,5 Reststunden nach 1800 s",
      abs(_fw["reststunden"] - 0.5) < 1e-9, str(_fw["reststunden"]))

ok, meldung = S.forschung_starten(zf, "Forstwirtschaft", 1800)
check("zweiter Auftrag in derselben Siedlung wird abgelehnt (Handbuch S. 12)",
      ok is False and ("laeuft" in meldung or "forscht" in meldung), meldung)
ok, meldung = S.forschung_starten(zf, "GibtsNicht", 1800)
check("unbekanntes Forschungsgebiet wird abgelehnt", ok is False, meldung)

_neu = S.tick(zf, 1800, 1800)
check("tick vor Ablauf laesst die Stufe bei 0", zf["forschung"]["Forstwirtschaft"]["stufe"] == 0)
check("tick vor Ablauf meldet kein Forschungsereignis",
      not any(e.get("typ") == "forschung" for e in _neu["ereignisse"]))

_neu = S.tick(zf, 3600, 1800)
check("tick nach Ablauf hebt die Stufe auf 1",
      zf["forschung"]["Forstwirtschaft"]["stufe"] == 1)
check("tick nach Ablauf meldet die fertige Forschung",
      any(e.get("typ") == "forschung" for e in _neu["ereignisse"]))
check("nach dem Abschluss laeuft kein Auftrag mehr",
      zf["forschung"]["Forstwirtschaft"]["auftrag"] is None)

_anzahl = len(S.ereignisse(zf))
_dup = S.tick(zf, 3600, 1800)
check("zweiter tick mit gleichem Zeitstempel liefert keine Ereignisse",
      _dup["ereignisse"] == [], str(_dup["ereignisse"]))
check("zweiter tick mit gleichem Zeitstempel verdoppelt die Nachrichten nicht",
      len(S.ereignisse(zf)) == _anzahl)
check("Forschungspunkte nach Stufe 1 sind 1",
      S.punkte(zf, 3600)["forschungspunkte"] == 1)


# ==========================================================================
# 6. Ausbildung
# ==========================================================================

abschnitt("6. Ausbildung — nur mit der passenden Ausbildungsstaette")

zt = S.neuer_zustand()
_vor = eingefroren(zt)
ok, meldung = S.ausbilden(zt, "GibtsNicht")
check("unbekannte Einheit wird abgelehnt", ok is False and "Unbekannt" in meldung, meldung)
ok, meldung = S.ausbilden(zt, "Bürgerwehr")
check("Ausbildung ohne Staette wird abgelehnt", ok is False and "nicht gebaut" in meldung, meldung)
check("abgelehnte Ausbildung aendert nichts", eingefroren(zt) == _vor)

_ka = feld(zt, _AKADEMIE_FELDER)
ok, meldung = S.bauen(zt, 0, "kriegerakademie", _ka)
check("Kriegerakademie gebaut", ok is True, meldung)
_vor = eingefroren(zt)
ok, meldung = S.ausbilden(zt, "Handkarren")
check("Karren brauchen den Stellmacher (falsches Gebaeude wird abgelehnt)",
      ok is False and "Stellmacher" in meldung, meldung)
check("abgelehnte Karren-Ausbildung aendert nichts", eingefroren(zt) == _vor)

zt["ressourcen"]["nahrung"] = 500
zt["ressourcen"]["leder"] = 500
zt["ressourcen"]["wolle"] = 500
_bev_vor = zt["bevoelkerung"]
ok, meldung = S.ausbilden(zt, "Bürgerwehr")
check("Bürgerwehr (Kriegerakademie) wird ausgebildet", ok is True, meldung)
check("die Einheit ist im Bestand", zt["einheiten"].get("Bürgerwehr") == 1)
check("die Ausbildung kostet 1 Siedler", _bev_vor - zt["bevoelkerung"] == 1)
check("die Ausbildung kostet 100 Nahrung",
      500 - zt["ressourcen"]["nahrung"] == 100, str(zt["ressourcen"]["nahrung"]))
check("die Ausbildung steht in den Nachrichten",
      any(e.get("typ") == "ausbildung" for e in S.ereignisse(zt)))

# fehlende Ware im Lager
zdg = S.neuer_zustand()
_dg = feld(zdg, _GILDE_FELDER)
S.bauen(zdg, 0, "diebesgilde", _dg)
zdg["ressourcen"]["nahrung"] = 500
zdg["ressourcen"]["gold"] = 500
_vor = eingefroren(zdg)
ok, meldung = S.ausbilden(zdg, "Streuner")
check("fehlende Ware im Lager fuehrt zur Ablehnung",
      ok is False and "Wollumhang" in meldung, meldung)
check("fehlende Ware aendert den Zustand nicht", eingefroren(zdg) == _vor)


# ==========================================================================
# 7. Werkstatt
# ==========================================================================

abschnitt("7. Werkstatt — Warteschlange und belegte Fertigungsdauer")

zws = S.neuer_zustand()
_vor = eingefroren(zws)
ok, meldung = S.ware_fertigen(zws, 0, "GibtsNicht", 1, 0.0)
check("unbekannte Ware wird abgelehnt", ok is False and "Unbekannte Ware" in meldung, meldung)
ok, meldung = S.ware_fertigen(zws, 0, "Schwert", 1, 0.0)
check("ohne Werkstatt wird das Fertigen abgelehnt",
      ok is False and "erst bauen" in meldung, meldung)
check("abgelehntes Fertigen aendert nichts", eingefroren(zws) == _vor)

check("Werkstatt-Zuordnung: Schwert -> Schmiede", W.werkstatt_fuer("Schwert") == "schmiede")
check("die belegte Schwerdauer ist 1200 s (20 min)", W.dauer_sekunden("Schwert") == 1200.0)

_ws = feld(zws, _SCHMIEDE_FELDER)
S.bauen(zws, 0, "schmiede", _ws)
ok, meldung = S.ware_fertigen(zws, 0, "Schwert", 1, 0.0)
check("Schwert wird in die Warteschlange gestellt", ok is True, meldung)
S.tick(zws, 600, 600)
check("vor der belegten Zeit ist noch nichts fertig", zws["waren"].get("Schwert", 0) == 0)
_neu = S.tick(zws, 1200, 600)
check("nach 20 Minuten ist 1 Schwert fertig", zws["waren"].get("Schwert") == 1,
      str(zws["waren"]))
check("das fertige Schwert steht in den Nachrichten",
      any(e.get("typ") == "werkstatt" for e in _neu["ereignisse"]))

# Handbuchbeispiel: 10 Schwerter mit zwei Schmieden = 100 min statt 200 min
z2 = S.neuer_zustand()
S.bauen(z2, 0, "schmiede", feld(z2, _SCHMIEDE_FELDER))
S.bauen(z2, 0, "schmiede", feld(z2, _SCHMIEDE_FELDER))
ok, meldung = S.ware_fertigen(z2, 0, "Schwert", 10, 0.0)
check("10 Schwerter bei 2 Schmieden werden eingereiht", ok is True, meldung)
S.tick(z2, 5999, 5999)
check("nach 5999 s sind 8 Schwerter fertig (Handbuchbeispiel)",
      z2["waren"].get("Schwert") == 8, str(z2["waren"]))
S.tick(z2, 6000, 1)
check("nach 6000 s (=100 min) sind alle 10 Schwerter fertig",
      z2["waren"].get("Schwert") == 10, str(z2["waren"]))


# ==========================================================================
# 8. Angriff
# ==========================================================================

abschnitt("8. Angriff — ueber kampfbericht (Vorrunde, Mauer, Beute)")

zang = S.neuer_zustand()
ok, ergebnis = S.angriff(zang, {"wall_stufe": 0}, 0.0)
check("Angriff ohne Einheiten wird abgelehnt",
      ok is False and "Keine Kaempfer" in ergebnis.get("grund", ""), str(ergebnis.get("grund")))

# schwache Truppe gegen Wall 5 -> Vorrunde scheitert
zang["einheiten"] = {"Bürgerwehr": 1}
_vor = eingefroren(zang)
ok, ergebnis = S.angriff(zang, {"wall_stufe": 5, "wall_zustand_prozent": 100.0}, 0.0)
check("gegen Wall 5 scheitert die Vorrunde", ok is False and ergebnis["bestanden"] is False)
check("der Bericht nennt den Rueckzug",
      "Vorrunde" in " ".join(ergebnis["bericht"]["zeilen"]) or
      "Schwelle" in " ".join(ergebnis["bericht"]["zeilen"]))
check("der gescheiterte Angriff aendert den Zustand nicht", eingefroren(zang) == _vor)
check("der Bericht ist trotzdem vom Typ kampf", ergebnis["bericht"]["typ"] == "kampf")

# erfolgreicher Angriff (kein Wall), Beute durch Karrenladung begrenzt
zsieg = S.neuer_zustand()
zsieg["einheiten"] = {"Ritter": 50, "Handkarren": 10}
_holz_vor = zsieg["ressourcen"]["holz"]
ok, ergebnis = S.angriff(zsieg, {"wall_stufe": 0, "wall_zustand_prozent": 100.0,
                                 "vorraete": {"holz": 1000, "stein": 500}}, 0.0,
                         random.Random(1))
check("starker Angreifer besteht die Vorrunde", ok is True and ergebnis["bestanden"] is True)
check("Beute wird gemacht", bool(ergebnis["beute"]), str(ergebnis["beute"]))
check("die Beute ist durch die Karrenladung begrenzt (10 x 40 = 400)",
      sum(ergebnis["beute"].values()) <= 400, str(sum(ergebnis["beute"].values())))
check("die Beute ist durch den Vorrat begrenzt",
      all(m <= 1000 for m in ergebnis["beute"].values()))
check("die Beute wird dem Spieler gutgeschrieben",
      zsieg["ressourcen"]["holz"] >= _holz_vor + ergebnis["beute"].get("holz", 0))
check("der Angriff erzeugt einen Bericht fuer die Nachrichten",
      ergebnis["bericht"]["typ"] == "kampf" and bool(ergebnis["bericht"]["titel"]))
check("der Angriff steht in den Nachrichten",
      any(e.get("typ") == "kampf" for e in S.ereignisse(zsieg)))

# Mauerschaden gegen einen Wall
zms = S.neuer_zustand()
zms["einheiten"] = {"Ritter": 20, "Katapult": 12}
ok, ergebnis = S.angriff(zms, {"wall_stufe": 5, "wall_zustand_prozent": 100.0,
                               "vorraete": {"holz": 500}}, 0.0, random.Random(7))
check("mit Belagerungswaffen wird die Mauer beschaedigt",
      ok is True and ergebnis["ergebnis"]["mauer_zustand"] < 100.0,
      str(ergebnis.get("ergebnis", {}).get("mauer_zustand")))


# ==========================================================================
# 9. Punkte
# ==========================================================================

abschnitt("9. Punkte — aus src/punkte.py")

zp = S.neuer_zustand()
_p = S.punkte(zp, 0.0)
check("punkte liefert die erwarteten Schluessel",
      all(k in _p for k in ("forschungspunkte", "kriegspunkte", "gesamtpunkte", "ruf",
                            "wall_stufe", "goetterschutz", "lage")))

zp["forschung"]["Forstwirtschaft"]["stufe"] = 3
_p = S.punkte(zp, 0.0)
check("Forschungspunkte = Summe Stufe hoch drei (3^3 = 27)",
      _p["forschungspunkte"] == 27, str(_p["forschungspunkte"]))
check("Forschungspunkte stimmen mit src/punkte.py ueberein",
      _p["forschungspunkte"] == P.forschungspunkte({"Forstwirtschaft": 3}))

zp["einheiten"] = {"Bürgerwehr": 2}
_p = S.punkte(zp, 0.0)
check("Kriegspunkte enthalten die Einheitenwerte (2 x 1 = 2)",
      _p["kriegspunkte"] == 2, str(_p["kriegspunkte"]))

# Wallstufe hoch drei zaehlt mit
zwall2 = S.neuer_zustand()
_wf = feld(zwall2, _WALL_FELDER)
S.bauen(zwall2, 0, "verteidigungswall", _wf)
S.ausbauen(zwall2, 0, _wf)
_pw = S.punkte(zwall2, 0.0)
check("die Wallstufe geht hoch drei in die Kriegspunkte ein (2^3 = 8)",
      _pw["kriegspunkte"] == 8 and _pw["wall_stufe"] == 2, str(_pw["kriegspunkte"]))

check("die Gesamtpunktzahl ist die halbe Summe",
      _p["gesamtpunkte"] == (_p["forschungspunkte"] + _p["kriegspunkte"]) // 2,
      f"{_p['gesamtpunkte']} vs ({_p['forschungspunkte']}+{_p['kriegspunkte']})//2")

check("Goetterschutz ist zu Beginn aktiv", S.punkte(zp, 0.0)["goetterschutz"] is True)
check("Goetterschutz ist nach sieben Tagen vorbei",
      S.punkte(zp, 7 * TAG)["goetterschutz"] is False)


# ==========================================================================
# 10. Portal, Nachrichten, offene Luecken
# ==========================================================================

abschnitt("10. Portal (W5), Nachrichten und offene Luecken")

zpo = S.neuer_zustand()
_vor = eingefroren(zpo)
ok, meldung = S.portalwechsel(zpo, 3, 0.0)
check("Koordinatenwechsel ohne Mana wird abgelehnt",
      ok is False and "Mana" in meldung, meldung)
check("abgelehnter Wechsel aendert nichts", eingefroren(zpo) == _vor)

zpo["ressourcen"]["mana"] = 6000
ok, meldung = S.portalwechsel(zpo, 3, 0.0)
check("mit Mana gelingt der Wechsel", ok is True, meldung)
check("der Wechsel kostet 5000 Mana", zpo["ressourcen"]["mana"] == 1000,
      str(zpo["ressourcen"]["mana"]))
check("die eigene Dimension ist jetzt 3", zpo["eigene_dimension"] == 3)
zpo["ressourcen"]["mana"] = 6000
ok, meldung = S.portalwechsel(zpo, 4, 1000.0)
check("ein zweiter Wechsel innerhalb von 24 h wird abgelehnt",
      ok is False and "24" in meldung, meldung)

zcopy = S.neuer_zustand()
_liste = S.ereignisse(zcopy)
_liste.append({"zeit": 0, "typ": "x", "text": "gefaelscht"})
check("ereignisse() gibt eine Kopie zurueck", len(S.ereignisse(zcopy)) == 0)

_luecken = S.offene_luecken()
check("offene_luecken ist ein Verzeichnis", isinstance(_luecken, dict) and bool(_luecken))
check("offene_luecken nennt die fehlende Auftragsdatei",
      "auftraege" in _luecken and "auftraege.py" in _luecken["auftraege"])
check("offene_luecken buendelt die Luecken von gebaeude_wirkung",
      "gebaeude_wirkung_luecken" in _luecken)
check("offene_luecken buendelt die Luecken von kampfbericht",
      "kampfbericht_luecken" in _luecken)
check("auftrag_starten fehlt absichtlich (kein erfundenes In-Betrieb-Nehmen)",
      not hasattr(S, "auftrag_starten"))
check("die geforderten uebrigen Aktionen sind vorhanden",
      all(hasattr(S, n) for n in ("neuer_zustand", "tick", "bauen", "ausbauen",
                                  "abreissen", "forschung_starten", "forschung_stand",
                                  "ausbilden", "ware_fertigen", "angriff", "punkte",
                                  "ereignisse", "offene_luecken")))

befund("auftrag_starten", "src/auftraege.py fehlt noch — absichtlich nicht eingebaut, "
                          "siehe offene_luecken().")

sys.exit(bericht())
