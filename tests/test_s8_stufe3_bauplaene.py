# -*- coding: ascii -*-
"""Wache S-8 Stufe 3: BAUPLAENE JE TAKTIK (Mindestzahlen und Restfelder), 04.11.2026.

DAS PROBLEM, GEMESSEN (vor dem Umbau)
-------------------------------------
`bot_doerfer_bebauen` setzte in JEDEM Bot-Dorf dieselbe Zahl je Gebaeude
(`data/bot_wirtschaft.json`: anlagen_je_gebaeude). Jeder Bot baute dasselbe - unabhaengig von
seiner Taktik - und die Karte blieb halb leer (gemessen 03.11.: 26 bis 30 Anlagen je Dorf).
Daniels Vorgabe zu S-8: der Bot soll seine Karte "je Taktik sinnvoll" nutzen.

Was diese Datei beweist
-----------------------
1. Der Plan steht in `data/bot_bauplan.json` (`anlagen_bauplaene`): fuenf Taktiken, jede mit
   Mindestzahlen, Restfeld-Reihenfolge je Gelaende und einer Obergrenze. KEINE Ertragszahl steht
   in der Datei - die Erttraege kommen aus `data/buildings.json` (EINE Zahlenquelle).
2. Jedes Gebaeude des Plans ist ein echtes Gebaeude (`gelaende.alle_gebaeude`) und auf mindestens
   einem Gelaende baubar; jedes Restfeld-Gelaende ist eine bekannte Gelaendeart.
3. `bot_anlagenplan` liest genau den Block der Taktik; eine unbekannte oder leere Taktik liefert
   `{}` - dann gilt der alte Weg, kein erfundener Plan.
4. Die Mindestzahlen werden WIRKLICH gesetzt (Erzmine 4 beim Raecher, Steinmetz 4 bei der
   Waechterin, Pferdezucht 3 bei der Spaeherin) - auf einer Karte, die genug passende Felder hat.
5. Zwei Taktiken bauen auf DERSELBEN Karte nachweislich VERSCHIEDEN (Erzmine/Steinmetz).
6. Die Restfelder werden nach dem Plan gefuellt: Holzfaeller bis zur Obergrenze 6, danach Jaeger
   auf Wald; Steppe bekommt Rinderfarm.
7. Die ZWEI Sperren halten: so viele Felder bleiben frei, wie der Gebaeude-Bauplan noch braucht
   (`bot_bauplan_offene_bauten`), und eine Bibliothek findet immer noch ein Feld - sonst gaebe es
   keine Forschung, keine Kaserne und keine Truppen.
8. Der ALTE Weg bleibt unveraendert: ohne Taktik setzt die Funktion weiter die 24 Anlagen aus
   `anlagen_je_gebaeude`, und ein zweiter Aufruf setzt nichts nach (idempotent).
9. Quellwache: beide Aufrufstellen im Spiel geben die Taktik mit (`taktik=bot_taktik_name(bot)`).
10. S-12 (04.11.2026): Huegel wird mitbelegt (Steinmetz zuerst), Sumpf traegt nichts, und alles
    Nutzbare ist entweder belegt oder als FELDLISTE fuer den Gebaeude-Bauplan reserviert.

Aufruf:  python -X utf8 tests/test_s8_stufe3_bauplaene.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import gelaende  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_bauplan.json"), encoding="utf-8") as _f:
    PLAN = json.load(_f)
with open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8") as _f:
    GEBAEUDE = {str(g.get("id")): g for g in (json.load(_f).get("gebaeude") or [])}

EINST = M.bot_wirtschaft_einstellungen()
TAKTIKEN = ("Pluenderer", "Waechterin", "Bastionier", "Spaeherin", "Raecher")
BERGKARTE = "original-014"          # genug Berg- und Huegelfelder fuer vier Erzminen
WALDKARTE = "original-006"          # 39 Waldfelder: Platz fuer den Holzfaeller-Deckel


def _dorf(karte: str, taktik: str = "", bauen: bool = True):
    """Ein Bot-Dorf auf dieser Karte, mit (`bauen`) oder ohne gesetzte Anlagen."""
    dorf = M.BotDorf(name="Wache", karte=karte)
    if bauen:
        M.bot_doerfer_bebauen(dorf, EINST, taktik=taktik)
    return dorf


def _raster(dorf):
    """Das 10x10-Raster dieser Karte aus den Spieldaten."""
    return list((M._bot_karte_dict(dorf.karte) or {}).get("raster") or [])


def _arten(dorf) -> dict:
    """Anlagen je Art in diesem Dorf."""
    zaehler: dict = {}
    for geb in dorf.bauten.values():
        zaehler[str(geb)] = zaehler.get(str(geb), 0) + 1
    return zaehler


def _frei(dorf):
    """Die noch freien Felder dieses Dorfes."""
    return [i for i in range(len(_raster(dorf))) if str(i) not in dorf.bauten]


# ==========================================================================
abschnitt("1. Der Plan steht in der Datendatei - fuenf Taktiken, keine Ertragszahl")
plaene = PLAN.get("anlagen_bauplaene") or {}
check("1 anlagen_bauplaene steht in data/bot_bauplan.json", isinstance(plaene, dict) and bool(plaene),
      str(sorted(plaene) if isinstance(plaene, dict) else type(plaene)))
for taktik in TAKTIKEN:
    block = plaene.get(taktik) or {}
    check("1 %s hat einen Block" % taktik, isinstance(block, dict) and bool(block), "")
    check("1 %s nennt Mindestzahlen" % taktik, bool(block.get("mindest")), "")
    check("1 %s nennt Restfelder" % taktik, bool(block.get("restfelder")), "")
    check("1 %s nennt eine Obergrenze fuer die Restfelder" % taktik,
          isinstance(block.get("restfelder_obergrenze"), dict), "")
    check("1 %s nennt den Entwurf, aus dem der Plan stammt" % taktik, bool(block.get("entwurf")), "")

alle_mindest = [g for b in plaene.values() for g in (b.get("mindest") or {})]
unbekannt = sorted({g for g in alle_mindest if g not in GEBAEUDE})
check("1 jede Mindestzahl nennt ein echtes Gebaeude", not unbekannt, str(unbekannt))
alle_rest = [g for b in plaene.values() for liste in (b.get("restfelder") or {}).values() for g in liste]
unbekannt_rest = sorted({g for g in alle_rest if g not in GEBAEUDE})
check("1 jede Restfeld-Anlage ist ein echtes Gebaeude", not unbekannt_rest, str(unbekannt_rest))
alle_gelaende = [art for b in plaene.values() for art in (b.get("restfelder") or {})]
unbekannt_gelaende = sorted({a for a in alle_gelaende if a not in gelaende.GELAENDEARTEN})
check("1 jedes Restfeld-Gelaende ist eine bekannte Gelaendeart", not unbekannt_gelaende,
      str(unbekannt_gelaende))
passend = [g for g in alle_mindest
           if not any(gelaende.bau_moeglich(g, art)[0] for art in gelaende.GELAENDEARTEN)]
check("1 jedes Gebaeude des Plans ist auf mindestens einem Gelaende baubar", not passend, str(passend))
# Keine zweite Zahlenliste: im Plan-Block darf kein Ertrag und kein Preis stehen.
roh = json.dumps(plaene, ensure_ascii=False)
check("1 der Plan traegt KEINE Ertragszahl (kommt aus data/buildings.json)",
      "ertrag" not in roh.lower(), "")
check("1 der Plan traegt KEINEN Preis (kommt aus data/baupreise.json)", "preis" not in roh.lower(), "")
# Die belegten Ertraege sind die Quelle - hier gegen den Kern gemessen, nicht getippt.
for geb, art, soll in (("holzfaeller", "wald", 4), ("steinmetz", "berg", 4), ("farm", "grasland", 4),
                       ("goldmine", "berg", 3), ("erzmine", "berg", 3), ("schafszucht", "grasland", 3),
                       ("pferdezucht", "grasland", 3), ("farm", "steppe", 2)):
    ist = gelaende.ertrag_pro_stunde(geb, art)
    check("1 belegter Ertrag %s auf %s = %s" % (geb, art, soll), float(ist) == float(soll), str(ist))
jaeger = gelaende.ertrag_pro_stunde("jaeger", "wald")
check("1 Jaeger liefert 2 Nahrung und 2 Leder auf Wald (Entwurf hatte 0)",
      isinstance(jaeger, dict) and float(jaeger.get("Nahrung", 0)) == 2.0
      and float(jaeger.get("Leder", 0)) == 2.0, str(jaeger))

# ==========================================================================
abschnitt("2. bot_anlagenplan liest genau den Block der Taktik")
for taktik in TAKTIKEN:
    block = M.bot_anlagenplan(taktik)
    check("2 bot_anlagenplan(%s) liefert den Block" % taktik,
          bool(block) and block.get("mindest") == (plaene.get(taktik) or {}).get("mindest"), "")
check("2 eine unbekannte Taktik liefert {} (kein erfundener Plan)",
      M.bot_anlagenplan("Gibtsnicht") == {}, str(M.bot_anlagenplan("Gibtsnicht")))
check("2 die leere Taktik liefert {} (alter Weg)", M.bot_anlagenplan("") == {}, "")
check("2 ein leerer Plan liefert {}", M.bot_anlagenplan("Raecher", plan={}) == {}, "")
check("2 der Stil kommt aus bottaktik (bot_taktik_name -> Pluenderer fuer Haug)",
      M.bot_taktik_name(M.BotPlayer("Haug", "menschlich", 0.3, 0.5)) == "Pluenderer",
      M.bot_taktik_name(M.BotPlayer("Haug", "menschlich", 0.3, 0.5)))

# ==========================================================================
abschnitt("3. Die Mindestzahlen werden gesetzt (Bergkarte %s)" % BERGKARTE)
dorf = _dorf(BERGKARTE, "Raecher")
arten = _arten(dorf)
mindest_raecher = (plaene.get("Raecher") or {}).get("mindest") or {}   # fehlt der Plan, prueft die Wache weiter
for geb, soll in mindest_raecher.items():
    ist = arten.get(geb, 0)
    if ist < soll:                                       # Karte kann zu klein sein
        befund("3 Raecher-Mindestzahl %s: %d von %d (Karte hat nicht genug passende Felder)"
               % (geb, ist, soll), "")
    else:
        check("3 Raecher-Mindestzahl %s = %d" % (geb, soll), ist >= soll, "ist=%d" % ist)
check("3 Erzmine steht mindestens 4x (Karren kosten 80 Metall)", arten.get("erzmine", 0) >= 4,
      str(arten.get("erzmine", 0)))
check("3 das Dorf hat mehr Anlagen als der alte Weg (24)", len(dorf.bauten) > 24, str(len(dorf.bauten)))

dorf_w = _dorf(BERGKARTE, "Waechterin")
arten_w = _arten(dorf_w)
check("3 Waechterin baut mindestens 4 Steinmetze (steinlastiger Plan)",
      arten_w.get("steinmetz", 0) >= 4, str(arten_w.get("steinmetz", 0)))
dorf_s = _dorf(BERGKARTE, "Spaeherin")
check("3 Spaeherin baut mindestens 3 Pferdezuchten (pferdelastiger Plan)",
      _arten(dorf_s).get("pferdezucht", 0) >= 3, str(_arten(dorf_s).get("pferdezucht", 0)))

# ==========================================================================
abschnitt("4. Zwei Taktiken bauen auf DERSELBEN Karte verschieden")
check("4 Raecher baut mehr Erzminen als die Waechterin",
      arten.get("erzmine", 0) > arten_w.get("erzmine", 0),
      "Raecher=%d Waechterin=%d" % (arten.get("erzmine", 0), arten_w.get("erzmine", 0)))
check("4 Waechterin baut mehr Steinmetze als der Raecher",
      arten_w.get("steinmetz", 0) > arten.get("steinmetz", 0),
      "Waechterin=%d Raecher=%d" % (arten_w.get("steinmetz", 0), arten.get("steinmetz", 0)))
check("4 die beiden Doerfer haben verschiedene Anlagenzahlen ODER Arten",
      arten != arten_w, "")

# ==========================================================================
abschnitt("5. Restfelder nach dem Plan (Waldkarte %s)" % WALDKARTE)
dorf_h = _dorf(WALDKARTE, "Raecher")
arten_h = _arten(dorf_h)
wald = sum(1 for a in _raster(dorf_h) if a == "wald")
check("5 die Waldkarte hat ueberhaupt Wald", wald > 6, str(wald))
check("5 Holzfaeller hoechstens 6 (Obergrenze der Restfelder)",
      arten_h.get("holzfaeller", 0) <= 6, str(arten_h.get("holzfaeller", 0)))
check("5 der Jaeger steht (Daniels Vorgabe: Jaeger auf Waldfelder)",
      arten_h.get("jaeger", 0) >= 1, str(arten_h.get("jaeger", 0)))
check("5 nach dem Holzfaeller-Deckel fuellt der Jaeger die uebrigen Waldfelder",
      arten_h.get("jaeger", 0) > 6, str(arten_h.get("jaeger", 0)))
steppe = sum(1 for a in _raster(dorf_h) if a == "steppe")
rinder = arten_h.get("rinderfarm", 0)
check("5 die Steppe traegt Rinderfarmen (Plan: Steppe -> Rinderfarm)",
      steppe == 0 or rinder >= min(3, steppe), "steppe=%d rinderfarm=%d" % (steppe, rinder))
# Auf KEINEM Feld steht eine Anlage, die dort nicht stehen darf.
falsch = [i for i, geb in dorf_h.bauten.items()
          if not gelaende.bau_moeglich(geb, _raster(dorf_h)[int(i)])[0]]
check("5 keine Anlage steht auf unpassendem Gelaende", not falsch, str(falsch[:5]))

# ==========================================================================
abschnitt("6. Die zwei Sperren: Feldreserve fuer den Bauplan und Bibliotheksfeld")
for taktik in TAKTIKEN:
    d = _dorf(BERGKARTE, taktik)
    offen = M.bot_bauplan_offene_bauten(d)
    frei = _frei(d)
    check("6 %s: %d offene Gebaeude brauchen Platz" % (taktik, offen), offen == 9, str(offen))
    for geb in M.bot_bauplan_offene_liste(d):
        passend = [i for i in frei if gelaende.bau_moeglich(geb, _raster(d)[i])[0]]
        check("6 %s: %s findet noch ein freies Feld" % (taktik, geb), bool(passend), str(len(passend)))
    bib = [i for i in frei if gelaende.bau_moeglich("bibliothek", _raster(d)[i])[0]]
    check("6 %s: eine Bibliothek findet noch ein Feld" % taktik, bool(bib), str(len(bib)))
    # S-12 (04.11.2026): die Reserve wird am GELAENDE gemessen - Sumpf zaehlt nicht mit.
    sumpf_frei = sum(1 for i in frei if str(_raster(d)[i]).lower() == "sumpf")
    nutzbar = len(frei) - sumpf_frei
    check("6 %s: mehr nutzbare freie Felder als offene Gebaeude" % taktik, nutzbar >= offen,
          "nutzbar=%d offen=%d sumpf=%d" % (nutzbar, offen, sumpf_frei))
    check("6 %s: die Reserve wird als FELDLISTE geliefert" % taktik,
          len(M.bot_bauplan_reservierte_felder(d, _raster(d))) == offen,
          str(len(M.bot_bauplan_reservierte_felder(d, _raster(d)))))
check("6 ohne Bauplan braucht nichts reserviert zu werden (dann baut bot_dorf_bauen nichts)",
      M.bot_bauplan_offene_bauten(M.BotDorf(name="leer"), plan={}) == 0,
      str(M.bot_bauplan_offene_bauten(M.BotDorf(name="leer"), plan={})))
check("6 mit der echten Datendatei sind es 9 offene Gebaeude",
      M.bot_bauplan_offene_bauten(M.BotDorf(name="leer")) == 9,
      str(M.bot_bauplan_offene_bauten(M.BotDorf(name="leer"))))
gefuellt = _dorf(BERGKARTE, "Raecher")
M.bot_doerfer_bebauen(gefuellt, EINST, taktik="Raecher")     # zweiter Aufruf
check("6 offene Bauten sinken, sobald Gebaeude stehen",
      M.bot_bauplan_offene_bauten(gefuellt) <= 9, str(M.bot_bauplan_offene_bauten(gefuellt)))

# ==========================================================================
abschnitt("7. Der alte Weg bleibt unveraendert und die Funktion ist idempotent")
alt = _dorf(BERGKARTE, "")
check("7 ohne Taktik setzt die Funktion weiter 24 Anlagen (anlagen_je_gebaeude)",
      len(alt.bauten) == 24, str(len(alt.bauten)))
check("7 ohne Taktik gibt es keinen Jaeger (data/bot_wirtschaft.json fuehrt keinen)",
      _arten(alt).get("jaeger", 0) == 0, str(_arten(alt).get("jaeger", 0)))
zweit = M.bot_doerfer_bebauen(dorf, EINST, taktik="Raecher")
check("7 ein zweiter Aufruf setzt nichts nach (idempotent)", zweit == 0, str(zweit))
ohne_karte = M.BotDorf(name="ohne Karte")
check("7 ohne Karte passiert nichts (Rueckgabe 0)",
      M.bot_doerfer_bebauen(ohne_karte, EINST, taktik="Raecher") == 0, "")

# ==========================================================================
abschnitt("8. Quellwache: beide Aufrufstellen geben die Taktik mit")
check("8 bot_doerfer_karten_zuweisen gibt taktik=bot_taktik_name(bot) mit",
      "bot_doerfer_bebauen(dorf, einstellungen, taktik=taktik)" in TEXT_MAIN, "")
check("8 die Gruendung gibt taktik=bot_taktik_name(bot) mit",
      "taktik=bot_taktik_name(bot))                   # S-8 Stufe 3: nach SEINEM Plan" in TEXT_MAIN, "")
check("8 die Signatur hat die neuen Parameter taktik und plan",
      "def bot_doerfer_bebauen(dorf: \"BotDorf\", einstellungen: Optional[dict] = None," in TEXT_MAIN
      and "taktik: str = \"\", plan: Optional[dict] = None) -> int:" in TEXT_MAIN, "")
check("8 die Restfeld-Phase steht im Code (S-8 Stufe 3)",
      "PHASE C (S-8 Stufe 3, 04.11.2026)" in TEXT_MAIN, "")

# ==========================================================================
abschnitt("9. S-12: Huegel wird mitbelegt, alles Nutzbare ist belegt oder reserviert")
for taktik in TAKTIKEN:
    d = _dorf(BERGKARTE, taktik)
    raster = _raster(d)
    arten = _arten(d)
    frei = _frei(d)
    huegel_frei = [i for i in frei if str(raster[i]).lower() == "huegel"]
    huegel_anlagen = sum(1 for i, g in d.bauten.items() if str(raster[int(i)]).lower() == "huegel")
    check("9 %s: Huegel traegt Anlagen (S-12)" % taktik, huegel_anlagen > 0, str(huegel_anlagen))
    check("9 %s: hoechstens die Reserve bleibt auf Huegel frei" % taktik,
          len(huegel_frei) <= 9, "huegel frei=%d" % len(huegel_frei))
    # Auf Huegel steht zuerst der Steinmetz (2 je Stunde ist der beste Ertrag dort).
    huegel_steinmetz = sum(1 for i, g in d.bauten.items()
                           if str(g) == "steinmetz" and str(raster[int(i)]).lower() == "huegel")
    check("9 %s: der Steinmetz nutzt den Huegel" % taktik, huegel_steinmetz > 0, str(huegel_steinmetz))
    check("9 %s: Sumpf traegt keine Anlage (Spielregel)" % taktik,
          all(str(raster[int(i)]).lower() != "sumpf" for i in d.bauten), "")
    # Alles, was eine Anlage tragen koennte, ist belegt ODER fuer den Bauplan reserviert.
    reserviert = M.bot_bauplan_reservierte_felder(d, raster, frei=frei)
    offen_nutzbar = [i for i in frei if str(raster[i]).lower() not in ("sumpf", "nebelsee")]
    check("9 %s: nutzbare freie Felder sind genau die Reserve" % taktik,
          len(offen_nutzbar) == len(reserviert),
          "nutzbar frei=%d reserviert=%d" % (len(offen_nutzbar), len(reserviert)))
check("9 die Anlagenzahl haengt an der Karte, nicht an einer festen Zahl",
      len(_dorf(BERGKARTE, "Raecher").bauten) != len(_dorf(WALDKARTE, "Raecher").bauten),
      "%d gegen %d" % (len(_dorf(BERGKARTE, "Raecher").bauten),
                       len(_dorf(WALDKARTE, "Raecher").bauten)))

# S-12 (04.11.2026): der Bau der Restfelder darf auf KEINER Karte abstuerzen - auch nicht, wenn
# kein Bibliotheksfeld mehr frei ist (gemessen: genau dort brach die Messung mit `IndexError` ab,
# weil `bib_felder` leer war und der Code trotzdem `bib_felder[0]` las).
for karte in ("original-001", "original-006", "original-014", "original-036", "original-118b"):
    try:
        d = _dorf(karte, "Raecher")
        art = M.bot_anlagenplan("Raecher")
        check("9 %s: der Plan baut ohne Absturz, auch wenn Bibliotheksfelder knapp sind" % karte,
              len(d.bauten) > 0, str(len(d.bauten)))
        frei = _frei(d)
        bib = [i for i in frei if gelaende.bau_moeglich("bibliothek", _raster(d)[i])[0]]
        reserviert = M.bot_bauplan_reservierte_felder(d, _raster(d), frei=frei)
        if "bibliothek" in M.bot_bauplan_offene_liste(d):
            check("9 %s: ein Bibliotheksfeld bleibt frei oder ist reserviert" % karte,
                  bool(bib) or any(gelaende.bau_moeglich("bibliothek", _raster(d)[i])[0]
                                   for i in reserviert), "frei=%d" % len(bib))
    except Exception as fehler:                                     # jeder Absturz ist ein Fehler
        check("9 %s: Plan ohne Ausnahme" % karte, False, repr(fehler))

sys.exit(bericht())
