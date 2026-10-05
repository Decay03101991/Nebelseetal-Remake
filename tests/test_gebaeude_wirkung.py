"""
Wirkungen der 20 Originalgebaeude im Spiel (Paket W4b-5, 04.10.2026).

Beweist, dass die Wirkungen aus den BEBauten FELDERN der Siedlungskarten kommen — und nicht
mehr aus den frueheren fuenf erfundenen Gebaeuden im Spielkern:

  Haus           -> Siedlergrenze 10 je Siedlung, +5 je Haus; 1 Siedler/Stunde (Handbuch S. 11)
  Bibliothek     -> ermoeglicht Forschung (S. 12) und steht nur auf Grasland/Steppe/Nebelsee
  Kriegerakademie-> bildet die 9 Kampfeinheiten aus
  Diebesgilde    -> bildet die 6 Kundschafter aus
  Stellmacher    -> baut 6 Karren und 7 Belagerungswaffen
  Verteidigungswall -> 10 Stufen, Schwellenwerte der Vorrunde, Kriegspunkte = Stufe hoch drei

Aufruf:  python tests/test_gebaeude_wirkung.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import einheiten as E
import gelaende as G
import gebaeude_wirkung as W
import main as M

TYPEN = ("waldreich", "bergreich", "weideland", "nebelseeufer", "gemischt")


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def karte_mit(art, anzahl=1, saaten=range(600)):
    """Eine Siedlungskarte mit mindestens ``anzahl`` Feldern dieser Gelaendeart (+ Feldindizes)."""
    for typ in TYPEN:
        for s in saaten:
            karte = G.siedlungskarte_erzeugen(s, typ_id=typ)
            felder = [i for i, a in enumerate(karte["raster"]) if a == art]
            if len(felder) >= anzahl:
                return karte, felder
    return None, []


def siedlung_mit(karte, bauten=()):
    """Eine Siedlung mit den genannten Gebaeuden (Feldindex, Gebaeudeschluessel)."""
    s = M.Settlement(name="Probesiedlung", map_id="test", karte=karte)
    for feld, geb in bauten:
        ok, meldung = M.bauen_auf_karte(s, geb, feld)
        assert ok, meldung
    return s


def freie_felder(karte, art, belegt=()):
    return [i for i, a in enumerate(karte["raster"]) if a == art and i not in belegt]


# ==========================================================================
# 1. Datengrundlage
# ==========================================================================

abschnitt("Datengrundlage — die 20 Originalgebaeude und ihre Wirkungsdatei")

_geb = json.load(open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8"))["gebaeude"]
_preise = json.load(open(os.path.join(ROOT, "data", "baupreise.json"), encoding="utf-8"))["preise"]
_wirk = json.load(open(os.path.join(ROOT, "data", "gebaeude_wirkung.json"), encoding="utf-8"))

check("es gibt genau 20 Originalgebaeude", len(_geb) == 20, f"{len(_geb)} Stueck")
check("jedes der 20 hat einen Baupreis (kein 'Preis offen')",
      all(g["id"] in _preise for g in _geb),
      str([g["id"] for g in _geb if g["id"] not in _preise]))
check("die Wirkungsdatei nennt ihre Quellen", bool(_wirk.get("_quelle")))
check("Bevoelkerungszahlen sind belegt (10 je Siedlung, +5 je Haus, 1 Siedler/Stunde)",
      (_wirk["bevoelkerung"]["grund_je_siedlung"],
       _wirk["bevoelkerung"]["je_haus"],
       _wirk["bevoelkerung"]["siedler_je_stunde"]) == (10, 5, 1),
      str(_wirk["bevoelkerung"]))
check("Heilkunde ist mit +10 % je Stufe vermerkt",
      _wirk["bevoelkerung"]["heilkunde_prozent_je_stufe"] == 10)
check("die Wirkungsdatei nennt die offenen Luecken (Werkstaetten, Baukunst, Lager)",
      set(_wirk["offene_luecken"]) == {"werkstaetten", "baukunst", "lager"},
      str(sorted(_wirk["offene_luecken"])))

check("die fuenf erfundenen Wirkungsgebaeude sind aus dem Spielkern entfernt",
      M.BUILDINGS == {} and not (
          {"haus", "bibliothek", "kaserne", "turm", "portal"} & set(M.BUILDINGS)),
      str(sorted(M.BUILDINGS)))
check("das Wirkungsmodul ist im Spiel eingebunden", M.gebaeude_wirkung is W)
check("die rohstofferzeugenden Gebaeude stehen weiterhin nur auf der Karte",
      not ({"holzfaeller", "steinmetz", "jaeger"} & set(M.BUILDINGS)))


# ==========================================================================
# 2. Haus und Siedlergrenze
# ==========================================================================

abschnitt("Haus — Siedlergrenze 10 je Siedlung, +5 je Haus (Handbuch S. 11)")

check("ohne Siedlung gilt der belegte Startwert 10", W.bevoelkerungsgrenze([]) == 10,
      str(W.bevoelkerungsgrenze([])))
check("ohne Siedlung waechst kein Siedler", W.siedler_zuwachs_pro_stunde([]) == 0.0,
      str(W.siedler_zuwachs_pro_stunde([])))

karte, gras = karte_mit("grasland", anzahl=3)
check("eine Graslandkarte mit drei Feldern ist zu finden", karte is not None and len(gras) >= 3)

ohne_haus = siedlung_mit(karte)
check("eine Siedlung ohne Haus hat die Grenze 10",
      W.bevoelkerungsgrenze([ohne_haus]) == 10, str(W.bevoelkerungsgrenze([ohne_haus])))

mit_haus = siedlung_mit(karte, [(gras[0], "haus")])
check("ein Haus hebt die Grenze auf 15", W.bevoelkerungsgrenze([mit_haus]) == 15,
      str(W.bevoelkerungsgrenze([mit_haus])))
mit_zwei = siedlung_mit(karte, [(gras[0], "haus"), (gras[1], "haus")])
check("zwei Haeuser heben die Grenze auf 20", W.bevoelkerungsgrenze([mit_zwei]) == 20,
      str(W.bevoelkerungsgrenze([mit_zwei])))
check("zwei Siedlungen zaehlen je 10 Grundwert (10+10+5 = 25)",
      W.bevoelkerungsgrenze([ohne_haus, mit_haus]) == 25,
      str(W.bevoelkerungsgrenze([ohne_haus, mit_haus])))
check("ein Haus wirkt nur in seiner eigenen Siedlung",
      W.siedlergrenze_je_siedlung(ohne_haus) == 10
      and W.siedlergrenze_je_siedlung(mit_haus) == 15)

# Hausausbau (VORSCHLAG, Vorgabe Daniel 05.10.2026: „der Häuserausbau ist noch nicht klug
# entworfen"): jede Ausbaustufe hebt die Siedlergrenze um weitere 5. Stufe 1 = belegtes Haus.
_haus_stufe3 = siedlung_mit(karte, [(gras[0], "haus")])
_haus_stufe3.stufen = {"0": 3}
check("ein Haus auf Stufe 3 hebt die Grenze auf 10 + 15 = 25",
      W.siedlergrenze_je_siedlung(_haus_stufe3) == 25,
      str(W.siedlergrenze_je_siedlung(_haus_stufe3)))
_zwei_haeuser = siedlung_mit(karte, [(gras[0], "haus"), (gras[1], "haus")])
_zwei_haeuser.stufen = {"0": 2}
check("Stufe 2 + Stufe 1 ergeben 10 + 15 = 25 (nur das ausgebaute Haus zaehlt hoeher)",
      W.siedlergrenze_je_siedlung(_zwei_haeuser) == 25,
      str(W.siedlergrenze_je_siedlung(_zwei_haeuser)))
check("alte Spielstaende ohne Stufenangabe zaehlen jedes Haus als Stufe 1",
      W.siedlergrenze_je_siedlung(mit_haus) == 15, str(W.siedlergrenze_je_siedlung(mit_haus)))

check("der Zuwachs ist 1 Siedler je Stunde und Siedlung",
      W.siedler_zuwachs_pro_stunde([mit_haus]) == 1.0,
      str(W.siedler_zuwachs_pro_stunde([mit_haus])))
check("zwei Siedlungen bringen 2 Siedler je Stunde",
      W.siedler_zuwachs_pro_stunde([ohne_haus, mit_haus]) == 2.0,
      str(W.siedler_zuwachs_pro_stunde([ohne_haus, mit_haus])))
check("Heilkunde Stufe 3 erhoeht den Zuwachs um 30 % (1 -> 1,3)",
      W.siedler_zuwachs_pro_stunde([mit_haus], {"heilkunde": 3}) == 1.3,
      str(W.siedler_zuwachs_pro_stunde([mit_haus], {"heilkunde": 3})))

abschnitt("Haus — der Zeitlauf waechst nach der Handbuchregel, nicht mehr erfunden")

st = M.GameState()
check("ein frisches Spiel startet mit 10 Siedlern (Handbuch S. 7)",
      st.population == 10.0, str(st.population))
st.tick(3600)
check("ohne Siedlung waechst die Bevoelkerung nicht", st.population == 10.0, str(st.population))

st.settlements.append(mit_haus)
st.tick(3600)
check("mit einem Haus sind es nach einer Stunde 11 Siedler",
      round(st.population, 2) == 11.0, str(st.population))
check("die Siedlergrenze steht im Spielstand auf 15", st.max_population == 15,
      str(st.max_population))
for _ in range(6):
    st.tick(3600)
check("die Bevoelkerung bleibt an der Grenze stehen (15)",
      round(st.population, 2) == 15.0, str(st.population))
_ok_zwei, _meld_zwei = M.bauen_auf_karte(mit_haus, "haus", gras[1])
check("ein zweites Haus hebt die Grenze dieser Siedlung auf 20",
      _ok_zwei and W.bevoelkerungsgrenze(st.settlements) == 20,
      f"{W.bevoelkerungsgrenze(st.settlements)}")


# ==========================================================================
# 3. Bibliothek und Forschung
# ==========================================================================

abschnitt("Bibliothek — Forschung braucht sie (Handbuch S. 12), und nur auf drei Gelaenden")

check("ohne Bibliothek ist Forschung nicht erlaubt", not W.hat_bibliothek([ohne_haus]))
erlaubt, meldung = W.forschung_erlaubt([ohne_haus])
check("die Begruendung nennt die Bibliothek", "Bibliothek" in meldung, meldung)

for art, soll in (("grasland", True), ("steppe", True), ("nebelsee", True),
                  ("wald", False), ("berg", False), ("huegel", False), ("sumpf", False)):
    ok, txt = G.bau_moeglich("bibliothek", art)
    check(f"Bibliothek auf {art}: {'erlaubt' if soll else 'verboten'}", ok is soll, txt)

karte_gras, gras2 = karte_mit("grasland", anzahl=2)
bib = siedlung_mit(karte_gras, [(gras2[0], "bibliothek")])
check("mit einer Bibliothek ist Forschung erlaubt", W.hat_bibliothek([bib]))
check("die Bibliotheksstufe kommt aus dem Feld (Stufe 1)", W.bibliothek_stufe([bib]) == 1,
      str(W.bibliothek_stufe([bib])))
check("eine zweite Bibliothek in derselben Siedlung wird abgelehnt",
      M.bauen_auf_karte(bib, "bibliothek", gras2[1])[0] is False,
      M.bauen_auf_karte(bib, "bibliothek", gras2[1])[1])

abschnitt("Bibliothek — das Spiel forscht wirklich erst mit ihr")

spiel = M.GameState()
spiel.research["Felderwirtschaft"].level = 0
spiel.settlements.append(ohne_haus)
spiel.resources["holz"].amount = 500
app_los = M.NebelseetalApp.__new__(M.NebelseetalApp)      # ohne Fenster: nur die Methode
app_los.state = spiel
app_los.log = spiel._log
app_los._log = spiel._log
app_los._start_research("Felderwirtschaft")
check("ohne Bibliothek steigt die Forschungsstufe nicht",
      spiel.research["Felderwirtschaft"].level == 0, str(spiel.research["Felderwirtschaft"].level))
check("und es wird kein Holz abgezogen", spiel.resources["holz"].amount == 500,
      str(spiel.resources["holz"].amount))
check("die Meldung nennt die Bibliothek", any("Bibliothek" in z for z in spiel.log[-2:]),
      str(spiel.log[-2:]))

spiel.settlements.append(bib)
gestartet = app_los._start_research("Felderwirtschaft")
check("mit Bibliothek STARTET die Forschung, die Stufe steigt aber noch nicht (W4c)",
      gestartet is True and spiel.research["Felderwirtschaft"].level == 0
      and isinstance(spiel.forschungsauftraege.get("Felderwirtschaft"), dict),
      f"Rueckgabe {gestartet}, Stufe {spiel.research['Felderwirtschaft'].level}, "
      f"Auftraege {sorted(spiel.forschungsauftraege)}")
check("und die Handbuchkosten (Stufe 1 = 50 Holz) sind abgezogen",
      spiel.resources["holz"].amount == 450, str(spiel.resources["holz"].amount))

# W4c: Die Stufe steigt nach ABLAUF der Zeit (Dauer = Stufe zum Quadrat in Stunden, S. 12).
_auftrag = spiel.forschungsauftraege["Felderwirtschaft"]
_jetzt = _auftrag["startzeit"] + M.forschung.dauer_sekunden(1) + 1
_gestiegen = spiel.forschung_fortschreiben(_jetzt)
check("nach Ablauf der Zeit steigt die Stufe genau einmal (kein zweites Mal)",
      _gestiegen == ["Felderwirtschaft"] and spiel.research["Felderwirtschaft"].level == 1
      and "Felderwirtschaft" not in spiel.forschungsauftraege
      and spiel.forschung_fortschreiben(_jetzt) == [],
      f"gestiegen {_gestiegen}, Stufe {spiel.research['Felderwirtschaft'].level}, "
      f"Auftraege {sorted(spiel.forschungsauftraege)}")


# ==========================================================================
# 4. Die drei Ausbildungsstaetten
# ==========================================================================

abschnitt("Ausbildung — jede Einheit kennt ihre Staette (data/units.json)")

_gebaeude_je_einheit = {n: W.ausbildungsgebaeude(n) for n in E.namen()}
check("alle 28 Einheiten haben eine bekannte Ausbildungsstaette",
      all(g in ("kriegerakademie", "diebesgilde", "stellmacher")
          for g in _gebaeude_je_einheit.values()),
      str({k: v for k, v in _gebaeude_je_einheit.items() if v is None}))
check("9 Kampfeinheiten kommen aus der Kriegerakademie",
      sum(1 for n, g in _gebaeude_je_einheit.items() if g == "kriegerakademie") == 9,
      str(sum(1 for g in _gebaeude_je_einheit.values() if g == "kriegerakademie")))
check("6 Kundschafter kommen aus der Diebesgilde",
      sum(1 for g in _gebaeude_je_einheit.values() if g == "diebesgilde") == 6)
check("13 Karren und Belagerungswaffen kommen aus dem Stellmacher",
      sum(1 for g in _gebaeude_je_einheit.values() if g == "stellmacher") == 13)
check("Krieger braucht die Kriegerakademie", W.ausbildungsgebaeude("Krieger") == "kriegerakademie")
check("Streuner braucht die Diebesgilde", W.ausbildungsgebaeude("Streuner") == "diebesgilde")
check("Handkarren braucht den Stellmacher", W.ausbildungsgebaeude("Handkarren") == "stellmacher")
check("Katapult braucht den Stellmacher", W.ausbildungsgebaeude("Katapult") == "stellmacher")
check("eine unbekannte Einheit bekommt keine Staette",
      W.ausbildungsgebaeude("Drache") is None)

abschnitt("Ausbildung — ohne Staette keine Einheit, mit Staette schon")

check("ohne Siedlung ist nichts ausbildbar", W.ausbildbare_einheiten([])[0] == [])
da, staette, stufe = W.ausbildungsstaette([ohne_haus], "Krieger")
check("ohne Akademie: nicht ausbildbar", da is False and stufe == 0,
      f"{da} {staette} {stufe}")
check("und der Grund nennt die Kriegerakademie", staette == "kriegerakademie", str(staette))

# Geländeregel (Vorgabe Daniel 05.10.2026): die Kriegerakademie steht nur auf Grasland,
# Steppe oder Hügel — deshalb wird sie hier auf Grasland gebaut, nicht im Wald.
karte_gras, gras_felder = karte_mit("grasland", anzahl=2)
militaer = siedlung_mit(karte_gras, [(gras_felder[0], "kriegerakademie")])
da, staette, stufe = W.ausbildungsstaette([militaer], "Krieger")
check("mit Akademie: ausbildbar (Stufe 1)", da is True and stufe == 1, f"{da} {stufe}")
moeglich, gesperrt = W.ausbildbare_einheiten([militaer])
check("mit Akademie sind genau die 9 Kampfeinheiten ausbildbar", len(moeglich) == 9,
      f"{len(moeglich)}: {moeglich}")
check("Kundschafter und Karren bleiben gesperrt", "Streuner" in gesperrt and "Handkarren" in gesperrt)

# Für Diebesgilde und Stellmacher (beide im Wald erlaubt) die Waldkarte hier bereitstellen.
karte_wald, wald = karte_mit("wald", anzahl=2)
gilde = siedlung_mit(karte_wald, [(wald[0], "diebesgilde")])
moeglich_g, _ = W.ausbildbare_einheiten([gilde])
check("mit der Diebesgilde sind genau die 6 Kundschafter ausbildbar", len(moeglich_g) == 6,
      f"{len(moeglich_g)}: {moeglich_g}")
stall = siedlung_mit(karte_wald, [(wald[0], "stellmacher")])
moeglich_s, _ = W.ausbildbare_einheiten([stall])
check("mit dem Stellmacher sind genau die 13 Karren und Belagerungswaffen ausbildbar",
      len(moeglich_s) == 13, f"{len(moeglich_s)}: {moeglich_s}")

check("eine zweite Kriegerakademie in derselben Siedlung wird abgelehnt",
      M.bauen_auf_karte(militaer, "kriegerakademie", gras_felder[1])[0] is False,
      M.bauen_auf_karte(militaer, "kriegerakademie", gras_felder[1])[1])

abschnitt("Ausbildung — die Stufe der Staette bestimmt das Tempo")

from bonus_system import get_training_time_multiplier
check("hoehere Stufe erhoeht den Ausbildungsfaktor (Stufe 5 gegen Stufe 1)",
      get_training_time_multiplier({}, 5) > get_training_time_multiplier({}, 1),
      f"{get_training_time_multiplier({}, 5)} gegen {get_training_time_multiplier({}, 1)}")
check("Stufe 5 bringt +25 % (1 + 0,05 je Stufe)",
      round(get_training_time_multiplier({}, 5), 4) == 1.25,
      str(get_training_time_multiplier({}, 5)))
befund("Ausbildungsdauer selbst noch offen",
       "das Handbuch nennt keine Ausbildungsdauer (bonus_system.UNIT_TRAIN_BASE = 0), deshalb "
       "bleibt get_training_time bei 0,5 Minuten stehen und die Stufe senkt noch nichts messbar")

abschnitt("Ausbildung — das Spiel bildet nur mit Staette aus")

spiel2 = M.GameState()
for _r in spiel2.resources.values():
    _r.amount = 5000
spiel2.population = 500.0
app2 = M.NebelseetalApp.__new__(M.NebelseetalApp)
app2.state = spiel2
app2._log = spiel2._log

app2._train_unit("Krieger")
check("ohne Akademie wird kein Krieger ausgebildet",
      spiel2.units["Krieger"].count == 0, str(spiel2.units["Krieger"].count))
check("und der Grund steht im Protokoll",
      any("Kriegerakademie" in z for z in spiel2.log[-2:]), str(spiel2.log[-2:]))

spiel2.settlements.append(militaer)
app2._train_unit("Krieger")
# NEU (Vorgabe Daniel 05.10.2026): mit Staette allein wird NICHT mehr ausgebildet — es fehlen
# Forschung (Kriegskunst 3) und Ausruestung (Schwert + Kettenhemd). Beides steht in
# data/units.json; die Pruefung steckt in main._ausbildungs_hindernis.
check("mit Akademie, aber ohne Forschung/Ausruestung wird der Krieger abgelehnt",
      spiel2.units["Krieger"].count == 0, str(spiel2.units["Krieger"].count))
check("und der Grund nennt die fehlende Forschung mit Soll/Ist",
      any("Kriegskunst Stufe 3" in z and "erreicht" in z for z in spiel2.log[-2:]),
      str(spiel2.log[-2:]))

# Mit erfuellter Forschung bleibt die Ausruestung die zweite Bedingung.
spiel2.research["Kriegskunst"].level = 3
app2._train_unit("Krieger")
check("ohne Ausruestung wird auch mit Forschung nicht ausgebildet",
      spiel2.units["Krieger"].count == 0, str(spiel2.units["Krieger"].count))
check("und der Grund nennt die fehlende Ware mit Soll/Ist",
      any("Ausrüstung" in z and "Schwert" in z for z in spiel2.log[-2:]),
      str(spiel2.log[-2:]))

# Erst Forschung UND Lager: jetzt wird ausgebildet, und die Waren werden verbraucht.
spiel2.waren["Schwert"] = 1
spiel2.waren["Kettenhemd"] = 1
app2._train_unit("Krieger")
check("mit Forschung UND Ausruestung wird der Krieger ausgebildet",
      spiel2.units["Krieger"].count == 1, str(spiel2.units["Krieger"].count))
check("die Ausruestung ist verbraucht (Schwert und Kettenhemd auf 0)",
      spiel2.waren["Schwert"] == 0 and spiel2.waren["Kettenhemd"] == 0,
      f"Schwert {spiel2.waren['Schwert']}, Kettenhemd {spiel2.waren['Kettenhemd']}")
check("und der Siedleranteil kommt von der Bevoelkerung (Handbuch S. 10)",
      spiel2.population < 500.0, str(spiel2.population))

# Einheiten ohne Voraussetzung und ohne Waren bleiben sofort ausbildbar.
app2._train_unit("Bürgerwehr")
check("die Buergerwehr braucht weder Forschung noch Ware (data/units.json)",
      spiel2.units["Bürgerwehr"].count == 1, str(spiel2.units["Bürgerwehr"].count))


# ==========================================================================
# 5. Verteidigungswall
# ==========================================================================

abschnitt("Verteidigungswall — 10 belegte Stufen, Schwellen, Kriegspunkte")

check("es gibt 10 Wallstufen", len(W._wallstufen()) == 10, str(len(W._wallstufen())))
check("Stufe 1 ist der Erdwall", W.wall_name(1) == "Erdwall", str(W.wall_name(1)))
check("Stufe 4 ist die Palisade", W.wall_name(4) == "Palisade", str(W.wall_name(4)))
check("Stufe 10 ist das Bollwerk", W.wall_name(10) == "Bollwerk", str(W.wall_name(10)))
check("Stufe 4 verlangt 160 Schlagkraft der Fusstruppen",
      W.wall_schwelle(4)["fusstruppen"] == 160, str(W.wall_schwelle(4)))
check("bis Stufe 4 ist keine Belagerungswaffe noetig",
      W.wall_schwelle(4)["belagerungswaffen"] is None, str(W.wall_schwelle(4)))
check("ab Stufe 5 sind 500 Schlagkraft der Belagerungswaffen noetig",
      W.wall_schwelle(5)["belagerungswaffen"] == 500, str(W.wall_schwelle(5)))
check("Stufe 10 verlangt 1000 Fusstruppen", W.wall_schwelle(10)["fusstruppen"] == 1000)
check("Kriegspunkte sind Stufe hoch drei (Palisade Stufe 4 = 64)",
      W.wall_kriegspunkte(4) == 64, str(W.wall_kriegspunkte(4)))
check("Kriegspunkte Stufe 10 = 1000", W.wall_kriegspunkte(10) == 1000)
check("eine unbekannte Wallstufe hat keine Schwelle", W.wall_schwelle(11)["fusstruppen"] is None)

check("ohne Wall ist die Wallstufe 0", W.wall_stufe([ohne_haus]) == 0)
check("ohne Wall steht kein Wall in der Beschreibung",
      "kein Verteidigungswall" in W.wall_beschreibung([ohne_haus]))

wall = siedlung_mit(karte_wald, [(wald[0], "verteidigungswall")])
check("mit einem Wall ist die Wallstufe 1", W.wall_stufe([wall]) == 1, str(W.wall_stufe([wall])))
wall.stufen[str(wald[0])] = 4
check("Stufe 4 heisst im Spiel Palisade", W.stufen_name("verteidigungswall", 4) == "Palisade")
check("die Beschreibung nennt Schwellenwert und Kriegspunkte",
      "160" in W.wall_beschreibung([wall]) and "64" in W.wall_beschreibung([wall]),
      W.wall_beschreibung([wall]))

abschnitt("Verteidigungswall — der Verteidigungsbonus kommt jetzt vom Wall, nicht vom Wachturm")

spiel3 = M.GameState()
spiel3.settlements.append(ohne_haus)
check("ohne Wall ist der Militaer-Faktor 1,0",
      M.research_multiplier(spiel3, "militär") == 1.0,
      str(M.research_multiplier(spiel3, "militär")))
spiel3.settlements.append(wall)
check("mit Wall (Stufe 4) steigt der Militaer-Faktor auf 1 + 0,5*4 = 3,0",
      M.research_multiplier(spiel3, "militär") == 3.0,
      str(M.research_multiplier(spiel3, "militär")))
check("es gibt keinen Wachturm mehr, an dem er haengen koennte",
      "turm" not in M.BUILDINGS and "kaserne" not in M.BUILDINGS)


# ==========================================================================
# 6. Ausbaustufen auf der Karte (Wall 10, Staetten und Bibliothek)
# ==========================================================================

abschnitt("Ausbaustufen — was sich ausbauen laesst und was nicht")

check("der Wall laesst sich bis Stufe 10 ausbauen", W.max_stufe("verteidigungswall") == 10)
check("Kriegerakademie, Diebesgilde und Stellmacher haben Stufen (Vorschlag 5)",
      [W.max_stufe(g) for g in ("kriegerakademie", "diebesgilde", "stellmacher")] == [5, 5, 5])
check("die Bibliothek hat Stufen (Vorschlag 5)", W.max_stufe("bibliothek") == 5)
check("ein Holzfäller hat keinen Ausbau (das Handbuch nennt keine Stufen)",
      W.max_stufe("holzfaeller") is None)
check("ein Haus hat Ausbaustufen bis 4 (VORSCHLAG, Vorgabe Daniel 05.10.2026)",
      W.max_stufe("haus") == 4, str(W.max_stufe("haus")))
check("ein Gebaeude ohne Eintrag liefert Stufe 1 (alte Spielstaende)",
      W.stufe_von_feld({"bauten": {"0": "haus"}}, 0) == 1)
check("eine gespeicherte Stufe wird gelesen",
      W.stufe_von_feld({"bauten": {"0": "haus"}, "stufen": {"0": 3}}, 0) == 3)
check("die hoechste Stufe eines Gebaeudes zaehlt (zwei Felder)",
      W.gebaeude_stufe({"bauten": {"0": "haus", "1": "haus"},
                        "stufen": {"0": 1, "1": 4}}, "haus") == 4)
check("ein nicht gebautes Gebaeude hat Stufe 0",
      W.gebaeude_stufe({"bauten": {}}, "haus") == 0)


# ==========================================================================
# 7. Oberflaeche — das Feld ausbauen (Fenster noetig)
# ==========================================================================

abschnitt("Siedlungskarte im Fenster — Ausbauen am Beispiel des Walls")

tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))


def ausbau_probe():
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app.state.resources["holz"].amount = 5000
        app.state.resources["stein"].amount = 5000
        app.state.resources["metall"].amount = 5000
        s = siedlung_mit(karte_wald, [(wald[0], "verteidigungswall")])
        app.state.settlements.append(s)
        app._oeffne_siedlungskarte(s)
        app._karten_feld_waehlen(wald[0])

        def knoepfe(widget):
            treffer = []
            for kind in widget.winfo_children():
                if isinstance(kind, tk.Button):
                    treffer.append(str(kind.cget("text")))
                treffer += knoepfe(kind)
            return treffer

        check("am Wall steht eine Schaltfläche zum Ausbauen",
              any("Ausbauen auf Stufe 2" in t for t in knoepfe(app.content)),
              str(knoepfe(app.content)[:8]))

        holz_vorher = app.state.resources["holz"].amount
        app._karten_ausbauen()
        check("der Wall ist danach auf Stufe 2",
              s.stufen.get(str(wald[0])) == 2, str(s.stufen))
        check("der Ausbau kostet das Doppelte des Grundpreises (2 x 16 Holz = 32)",
              round(holz_vorher - app.state.resources["holz"].amount, 2) == 32,
              f"{holz_vorher} -> {app.state.resources['holz'].amount}")
        check("die Meldung nennt die neue Stufe",
              any("Stufe 2" in z for z in app.state.log[-2:]), str(app.state.log[-2:]))

        app._karten_feld_waehlen(wald[0])
        check("am ausgebauten Wall steht jetzt die naechste Stufe (3)",
              any("Ausbauen auf Stufe 3" in t for t in knoepfe(app.content)),
              str(knoepfe(app.content)[:8]))

        # Ein Gebaeude ohne Stufen bietet keinen Ausbau an, sondern sagt es ehrlich.
        holzfaeller_feld = freie_felder(karte_wald, "wald", (wald[0],))[0]
        app._karten_feld_waehlen(holzfaeller_feld)
        app._karten_bauen("holzfaeller")
        app._karten_feld_waehlen(holzfaeller_feld)
        check("am Holzfäller steht kein Ausbau-Knopf",
              not any("Ausbauen auf Stufe" in t for t in knoepfe(app.content)),
              str(knoepfe(app.content)[:8]))

        # Hoehere Stufe = schneller ausbilden: die Stätte laesst sich ebenfalls ausbauen.
        app._karten_feld_waehlen(wald[0])
        app._karten_abreissen()
        check("der Abriss entfernt auch die Ausbaustufe", str(wald[0]) not in s.stufen,
              str(s.stufen))
        return True
    finally:
        root.destroy()


if tk is not None:
    check("Ausbau im Fenster laeuft durch", bool(ausnahme("Ausbau im Fenster", ausbau_probe)))
else:
    befund("Fensterprüfung übersprungen", "kein tkinter verfügbar")


sys.exit(bericht())
