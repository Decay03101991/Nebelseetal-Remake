"""
Forschungspfad (W7) -- was ist jetzt erreichbar, was ist gesperrt, was schaltet frei?

Prueft die reine Datenschicht ``src/forschungspfad.py`` gegen die vorhandenen Datendateien.
Es wird nichts erfunden: die belegten Handbuchzahlen werden woertlich erwartet, und wovon
das Handbuch schweigt, muss ehrlich als Luecke erscheinen (offene_luecken()).
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import forschungspfad as FP

with open(os.path.join(ROOT, "data", "research.json"), encoding="utf-8") as _f:
    DATEN = json.load(_f)
ALLE = list(DATEN["forschungen"].keys())

KUERZEL = {
    "Waffentechnik": [{"art": "bibliothek", "was": "Bibliothek", "stufe": 3},
                      {"art": "forschung", "was": "Schmiedekunst", "stufe": 1}],
    "Mauerbau": [{"art": "forschung", "was": "Verteidigungsanlagen", "stufe": 5}],
    "Kampfmagie": [{"art": "forschung", "was": "Magiekunde", "stufe": 4}],
    "Baukunst": [{"art": "bibliothek", "was": "Bibliothek", "stufe": 1}],
    "N\u00e4hkunst": [{"art": "bibliothek", "was": "Bibliothek", "stufe": 2},
                     {"art": "forschung", "was": "N\u00e4hen", "stufe": 1}],
}


def wirft(aufruf) -> str:
    """Fuehrt aufruf aus und gibt 'ValueError: ...' zurueck, sonst 'KEIN FEHLER'."""
    try:
        aufruf()
    except ValueError as e:
        return f"ValueError: {e}"
    except Exception as e:  # noqa: BLE001 -- alles andere ist hier ein Fehler
        return f"{type(e).__name__}: {e}"
    return "KEIN FEHLER"


def ohne_ziffer(text: str) -> bool:
    return re.search(r"[0-9]", text) is None


# ==========================================================================
abschnitt("1. Abdeckung: alle 21 Forschungen sind bedienbar")

check("research.json hat 21 Forschungen", len(ALLE) == 21, str(len(ALLE)))
for name in ALLE:
    check(f"voraussetzung('{name}') liefert eine Liste",
          isinstance(FP.voraussetzung(name), list))


# ==========================================================================
abschnitt("2. voraussetzung(): Zerlegung der Originaltexte")

check("Waffentechnik == Bibliothek 3 + Schmiedekunst 1",
      FP.voraussetzung("Waffentechnik") == KUERZEL["Waffentechnik"],
      str(FP.voraussetzung("Waffentechnik")))
check("Mauerbau == Verteidigungsanlagen 5",
      FP.voraussetzung("Mauerbau") == KUERZEL["Mauerbau"],
      str(FP.voraussetzung("Mauerbau")))
check("Kampfmagie == Magiekunde 4",
      FP.voraussetzung("Kampfmagie") == KUERZEL["Kampfmagie"],
      str(FP.voraussetzung("Kampfmagie")))
check("Baukunst == Bibliothek 1",
      FP.voraussetzung("Baukunst") == KUERZEL["Baukunst"],
      str(FP.voraussetzung("Baukunst")))
check("N\u00e4hkunst == Bibliothek 2 + N\u00e4hen 1",
      FP.voraussetzung("N\u00e4hkunst") == KUERZEL["N\u00e4hkunst"],
      str(FP.voraussetzung("N\u00e4hkunst")))
check("jede Bedingung hat genau die drei Schluessel",
      all(set(p) == {"art", "was", "stufe"}
          for n in ALLE for p in FP.voraussetzung(n)))
check("jede Bedingung nennt eine gueltige Art",
      all(p["art"] in ("bibliothek", "forschung")
          for n in ALLE for p in FP.voraussetzung(n)))
check("unbekannte Forschung loest ValueError mit dem Namen aus",
      "ValueError" in wirft(lambda: FP.voraussetzung("GibtsNicht"))
      and "GibtsNicht" in wirft(lambda: FP.voraussetzung("GibtsNicht")),
      wirft(lambda: FP.voraussetzung("GibtsNicht")))


# ==========================================================================
abschnitt("3. erfuellt(): gesperrt mit Begruendung, erfuellt wenn alles passt")

ok, grund = FP.erfuellt("Waffentechnik", {}, 1)
check("Waffentechnik mit Bibliothek 1 ist gesperrt", ok is False, grund)
check("die Begruendung nennt Bibliothek 3/1", "Bibliothek 3/1" in grund, grund)
check("die Begruendung nennt Schmiedekunst 0/1", "Schmiedekunst 0/1" in grund, grund)

ok2, grund2 = FP.erfuellt("Waffentechnik", {}, 3)
check("ohne Schmiedekunst bleibt Waffentechnik auch bei Bibliothek 3 gesperrt",
      ok2 is False and "Schmiedekunst 0/1" in grund2, grund2)

ok3, grund3 = FP.erfuellt("Waffentechnik", {"Schmiedekunst": 1}, 3)
check("Bibliothek 3 + Schmiedekunst 1 erfuellt Waffentechnik", ok3 is True, grund3)

ok4, _ = FP.erfuellt("Waffentechnik", {"Schmiedekunst": 2}, 3)
check("hoehere Stufen zaehlen ebenfalls als erfuellt", ok4 is True)

ok5, _ = FP.erfuellt("Baukunst", {}, 1)
check("Baukunst ist ab Bibliothek 1 erforschbar", ok5 is True)
ok6, grund6 = FP.erfuellt("Baukunst", {}, 0)
check("ohne Bibliothek ist Baukunst gesperrt (Bibliothek 1/0)",
      ok6 is False and "Bibliothek 1/0" in grund6, grund6)

ok7, grund7 = FP.erfuellt("Mauerbau", {}, 10)
check("Mauerbau ohne Verteidigungsanlagen bleibt gesperrt",
      ok7 is False and "Verteidigungsanlagen 0/5" in grund7, grund7)
ok8, _ = FP.erfuellt("Mauerbau", {"Verteidigungsanlagen": 5}, 1)
check("Mauerbau erfuellt mit Verteidigungsanlagen 5 (keine Bibliothek noetig)", ok8 is True)

ok9, grund9 = FP.erfuellt("Magiekunde", {}, 5)
check("Magiekunde bei Bibliothek 5 gesperrt (Bibliothek 6/5)",
      ok9 is False and "Bibliothek 6/5" in grund9, grund9)
ok10, _ = FP.erfuellt("Magiekunde", {}, 6)
check("Magiekunde bei Bibliothek 6 erfuellt", ok10 is True)


# ==========================================================================
abschnitt("4. jetzt_moeglich(): was bei dieser Bibliothek sofort geht")

bib1 = FP.jetzt_moeglich({}, 1)
check("Bibliothek 1: Kriegskunst ist moeglich", "Kriegskunst" in bib1, str(bib1))
check("Bibliothek 1: Waffentechnik ist NICHT moeglich", "Waffentechnik" not in bib1, str(bib1))
check("Bibliothek 1: Tierhaltung ist noch nicht moeglich", "Tierhaltung" not in bib1)
check("Bibliothek 1: N\u00e4hkunst fehlt noch (N\u00e4hen fehlt)", "N\u00e4hkunst" not in bib1)
check("Bibliothek 1 liefert genau die acht Direktforschungen",
      set(bib1) == {"Baukunst", "Bogenbau", "Felderwirtschaft", "Heimlichkeit",
                    "Kriegskunst", "N\u00e4hen", "Schmiedekunst", "Wagenbau"},
      str(sorted(bib1)))
check("Bibliothek 1: Liste ist nach Name sortiert (gleiche Bibliotheksstufe)",
      bib1 == sorted(bib1), str(bib1))
check("ohne Bibliothek ist nichts moeglich", FP.jetzt_moeglich({}, 0) == [])

bib2 = FP.jetzt_moeglich({"N\u00e4hen": 1}, 2)
check("Bibliothek 2 + N\u00e4hen 1: N\u00e4hkunst und Tierhaltung sind moeglich",
      "N\u00e4hkunst" in bib2 and "Tierhaltung" in bib2, str(bib2))

bib3 = FP.jetzt_moeglich({"Schmiedekunst": 1}, 3)
check("Bibliothek 3 + Schmiedekunst 1: Waffentechnik ist moeglich",
      "Waffentechnik" in bib3, str(bib3))
check("Bibliothek 3 + Schmiedekunst 1: R\u00fcstungsbau ist moeglich", "R\u00fcstungsbau" in bib3)
check("Bibliothek 3: Mauerbau ist noch gesperrt", "Mauerbau" not in bib3)
check("Bibliothek 3: Kampfmagie ist noch gesperrt", "Kampfmagie" not in bib3)

check("eine bereits erforschte Forschung faellt heraus",
      "Kriegskunst" not in FP.jetzt_moeglich({"Kriegskunst": 1}, 1))


# ==========================================================================
abschnitt("5. blockiert(): was fehlt, und warum")

blk1 = FP.blockiert({}, 1)
nach_name = {e["name"]: e for e in blk1}
check("blockiert belegt Mauerbau als gesperrt", "Mauerbau" in nach_name, str(sorted(nach_name)))
check("Mauerbau: Grund nennt Verteidigungsanlagen 5",
      nach_name.get("Mauerbau", {}).get("fehlt") == ["Verteidigungsanlagen 5"],
      str(nach_name.get("Mauerbau")))
check("Waffentechnik: Grund nennt Bibliothek 3",
      "Bibliothek 3" in nach_name.get("Waffentechnik", {}).get("fehlt", []),
      str(nach_name.get("Waffentechnik")))
check("Waffentechnik: Grund nennt Schmiedekunst 1",
      "Schmiedekunst 1" in nach_name.get("Waffentechnik", {}).get("fehlt", []),
      str(nach_name.get("Waffentechnik")))
check("jeder blockiert-Eintrag hat genau die Schluessel name und fehlt",
      all(set(e) == {"name", "fehlt"} for e in blk1))
check("blockiert und jetzt_moeglich schliessen sich aus",
      not (set(nach_name) & set(bib1)), str(sorted(set(nach_name) & set(bib1))))
check("eine erforschte Forschung steht nicht in blockiert",
      "Kriegskunst" not in {e["name"] for e in FP.blockiert({"Kriegskunst": 1}, 1)})
check("blockiert nennt keine leere Begruendung",
      all(e["fehlt"] for e in blk1))


# ==========================================================================
abschnitt("6. wirkung_text(): Handbuchwortlaut plus belegte Zahl")

for name, zahl in [("Felderwirtschaft", "10"), ("Steinbruch", "10"),
                   ("Forstwirtschaft", "10"), ("Tierhaltung", "5"),
                   ("Minenarbeit", "5"), ("G\u00f6tterkunde", "5"),
                   ("Heilkunde", "10"), ("Mauerbau", "10"), ("Schmiedekunst", "5")]:
    check(f"wirkung_text('{name}') nennt die belegte Zahl {zahl}",
          zahl in FP.wirkung_text(name), FP.wirkung_text(name))

for name in ("Kriegskunst", "Heimlichkeit", "Bogenbau", "N\u00e4hen", "Waffentechnik",
             "R\u00fcstungsbau", "N\u00e4hkunst", "Magiekunde", "Kampfmagie",
             "Baukunst", "Verteidigungsanlagen", "Wagenbau"):
    check(f"wirkung_text('{name}') erfindet keine Zahl", ohne_ziffer(FP.wirkung_text(name)),
          FP.wirkung_text(name))

check("wirkung_text uebernimmt den Handbuchwortlaut woertlich",
      FP.wirkung_text("Felderwirtschaft").startswith(
          DATEN["forschungen"]["Felderwirtschaft"]["wirkung"]))
check("unbekannte Forschung loest in wirkung_text ValueError aus",
      "ValueError" in wirft(lambda: FP.wirkung_text("GibtsNicht")))


# ==========================================================================
abschnitt("7. schaltet_frei(): nur was die Daten hergeben")

wf = FP.schaltet_frei("Waffentechnik")
check("Waffentechnik schaltet Kurzbogen frei", "Kurzbogen" in wf["waren"], str(wf["waren"]))
check("Waffentechnik schaltet Bogen frei", "Bogen" in wf["waren"])
check("Waffentechnik schaltet Langbogen frei", "Langbogen" in wf["waren"])
check("Waffentechnik schaltet Armbrust frei", "Armbrust" in wf["waren"])
check("Waffentechnik schaltet auch Dolch/Kurzschwert/Schwert/Zweih\u00e4nder frei",
      {"Dolch", "Kurzschwert", "Schwert", "Zweih\u00e4nder"} <= set(wf["waren"]),
      str(wf["waren"]))
check("Waffentechnik schaltet den Kurzbogenschuetzen frei",
      "Kurzbogensch\u00fctze" in wf["einheiten"], str(wf["einheiten"]))
check("Waffentechnik schaltet Bogenschuetze/Langbogenschuetze/Armbrustschuetze frei",
      {"Bogensch\u00fctze", "Langbogensch\u00fctze", "Armbrustsch\u00fctze"} <= set(wf["einheiten"]),
      str(wf["einheiten"]))
check("Waffentechnik schaltet den Dieb frei (ueber Dolch)", "Dieb" in wf["einheiten"])
check("schaltet_frei liefert genau die drei Schluessel",
      set(FP.schaltet_frei("Baukunst")) == {"waren", "einheiten", "gebaeude"})

bk = FP.schaltet_frei("Baukunst")
check("Baukunst schaltet die Schmiede frei", "Schmiede" in bk["gebaeude"], str(bk["gebaeude"]))
check("Baukunst schaltet Farm und Goldmine frei",
      "Farm" in bk["gebaeude"] and "Goldmine" in bk["gebaeude"])
check("Baukunst ist bei Holzf\u00e4ller NICHT Voraussetzung (ohne Forschung baubar)",
      "Holzf\u00e4ller" not in bk["gebaeude"])
check("Baukunst schaltet den Verteidigungswall frei", "Verteidigungswall" in bk["gebaeude"])

rs = FP.schaltet_frei("R\u00fcstungsbau")
check("R\u00fcstungsbau schaltet Kettenhemd/Plattenr\u00fcstung frei",
      {"Kettenhemd", "Plattenr\u00fcstung"} <= set(rs["waren"]), str(rs["waren"]))
check("R\u00fcstungsbau schaltet auch den Magischen Paladinharnisch frei",
      "Magischer Paladinharnisch" in rs["waren"])

nk = FP.schaltet_frei("N\u00e4hkunst")
check("N\u00e4hkunst schaltet Diebesumhang/Fellumhang/Fellr\u00fcstung frei",
      {"Diebesumhang", "Fellumhang", "Fellr\u00fcstung"} <= set(nk["waren"]), str(nk["waren"]))
check("unbekannte Forschung loest in schaltet_frei ValueError aus",
      "ValueError" in wirft(lambda: FP.schaltet_frei("GibtsNicht")))

# Grenze der reinen Waren-Ableitung, die offene_luecken() nennt.
check("Heimlichkeit hat keine Ware (nur Einheiten nennen es direkt)",
      FP.schaltet_frei("Heimlichkeit")["waren"] == [],
      str(FP.schaltet_frei("Heimlichkeit")))


# ==========================================================================
abschnitt("8. empfohlene_reihenfolge() und offene_luecken()")

check("ohne Bibliothek ist der Plan leer", FP.empfohlene_reihenfolge(0) == [])
plan1 = FP.empfohlene_reihenfolge(1)
check("Bibliothek 1: die ersten fuenf sind Wirtschaft und Tuer-Oeffner",
      plan1[:5] == ["Baukunst", "Felderwirtschaft", "Schmiedekunst", "Kriegskunst",
                    "Heimlichkeit"], str(plan1[:5]))
check("Bibliothek 1: Waffentechnik steht noch nicht im Plan", "Waffentechnik" not in plan1)
check("Bibliothek 1: Tierhaltung und N\u00e4hkunst stehen noch nicht im Plan",
      "Tierhaltung" not in plan1 and "N\u00e4hkunst" not in plan1)
check("Bibliothek 1: Baukunst steht vor Verteidigungsanlagen",
      plan1.index("Baukunst") < plan1.index("Verteidigungsanlagen"))
check("Bibliothek 1: Verteidigungsanlagen steht vor Mauerbau",
      plan1.index("Verteidigungsanlagen") < plan1.index("Mauerbau"))

plan3 = FP.empfohlene_reihenfolge(3)
check("Bibliothek 3: Waffentechnik ist im Plan", "Waffentechnik" in plan3, str(plan3))
check("Bibliothek 3: Schmiedekunst steht vor Waffentechnik",
      plan3.index("Schmiedekunst") < plan3.index("Waffentechnik"))
check("Bibliothek 3: R\u00fcstungsbau ist im Plan", "R\u00fcstungsbau" in plan3)
check("Bibliothek 3: Mauerbau steht nach Verteidigungsanlagen",
      plan3.index("Verteidigungsanlagen") < plan3.index("Mauerbau"))

plan6 = FP.empfohlene_reihenfolge(6)
check("Bibliothek 6: Magiekunde und Kampfmagie sind im Plan",
      "Magiekunde" in plan6 and "Kampfmagie" in plan6, str(plan6))
check("Bibliothek 6: Magiekunde steht vor Kampfmagie",
      plan6.index("Magiekunde") < plan6.index("Kampfmagie"))
check("der Plan nennt nur gueltige Forschungsnamen",
      all(n in ALLE for n in plan6))
check("der Plan enthaelt keine Dopplung", len(plan6) == len(set(plan6)))

luecken = FP.offene_luecken()
check("offene_luecken() ist eine Liste von Texten",
      isinstance(luecken, list) and all(isinstance(s, str) for s in luecken))
check("offene_luecken() kennzeichnet die Reihenfolge als VORSCHLAG",
      any("VORSCHLAG" in s for s in luecken))
check("offene_luecken() nennt die fehlende Zahl fuer die zwoelf Forschungen",
      sum(1 for s in luecken if "keine Zahl" in s) == 12,
      str(sum(1 for s in luecken if "keine Zahl" in s)))
check("offene_luecken() nennt eine zahlose Forschung namentlich",
      any("Kriegskunst" in s for s in luecken))
check("offene_luecken() nennt die Warengrenze von schaltet_frei",
      any("schaltet_frei" in s for s in luecken))


sys.exit(bericht())
