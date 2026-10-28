"""
Waren und Werkstaetten im Spiel (Paket W3, 04.10.2026).

Beweist, dass die 17 Originalwaren ueber die drei Werkstaetten der Siedlungskarte
laufen und dass die Warteschlange sich genau wie das Handbuchbeispiel verhaelt:

  * die drei Werkstaetten stehen in data/buildings.json (Kategorie "Werkstatt"),
  * jede der 17 Waren aus data/items.json hat eine Werkstatt - oder ehrlich keine,
  * das Handbuchbeispiel: 10 Schwerter a 20 Minuten mit ZWEI Schmieden = 100 Minuten,
    mit EINER Schmiede = 200 Minuten,
  * mehrere gleiche Werkstaetten fertigen mehrere Waren GLEICHZEITIG,
  * eine unbekannte Ware wird abgelehnt,
  * fuer jede Ware ausser dem belegten Schwert wird KEINE Dauer erfunden: die Ware
    wartet mit "Dauer nicht belegt".

Aufruf:  python -X utf8 tests/test_werkstatt.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import spieldaten as SP
import gelaende as G
import werkstatt as W

WAREN = SP.waren()
ALLE = list(WAREN.keys())
WERK = W.werkstaetten()
SCHWERT = "Schwert"                    # die einzige Ware mit belegter Dauer
SCHMELZE = 20 * 60                     # 20 Minuten in Sekunden


# ==========================================================================
# 1. Datengrundlage - die drei Werkstaetten
# ==========================================================================

abschnitt("Datengrundlage - die drei Werkstaetten aus data/buildings.json")

_werkstatt_geb = [g for g in SP.gebaeude() if g.get("kategorie") == "Werkstatt"]

check("es gibt genau 17 Waren in data/items.json", len(ALLE) == 17, f"{len(ALLE)} Stueck")
check("werkstaetten() kennt genau schmiede, bogenbauer, naehstube",
      set(WERK) == {"schmiede", "bogenbauer", "naehstube"}, str(sorted(WERK)))
check("buildings.json fuehrt genau drei Gebaeude der Kategorie 'Werkstatt'",
      len(_werkstatt_geb) == 3, f"{len(_werkstatt_geb)} Stueck")
check("Schmiede lautet im Original 'Schmiede'", WERK.get("schmiede") == "Schmiede",
      str(WERK.get("schmiede")))
check("Bogenbauer lautet im Original 'Bogenbauer'", WERK.get("bogenbauer") == "Bogenbauer",
      str(WERK.get("bogenbauer")))
check("die Werkstattnamen stimmen mit gelaende.gebaeude_name ueberein",
      all(WERK[k] == G.gebaeude_name(k) for k in WERK), str(WERK))
check("alle drei Werkstaetten sind mehrfach baubar",
      all(g.get("mehrfach_moeglich") for g in _werkstatt_geb))
check("alle drei Werkstaetten fertigen parallel (Feld 'fertigt_parallel')",
      all(g.get("fertigt_parallel") for g in _werkstatt_geb))
check("die Daten nennen Nichts erfundenes als Quelle (Hinweisfeld vorhanden)",
      bool(__import__("json").load(
          open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8")).get("_hinweis")))


# ==========================================================================
# 2. Waren je Werkstatt und die Rueckrichtung
# ==========================================================================

abschnitt("Waren je Werkstatt - die 17 Waren aus data/items.json")

SCHMIEDE = W.waren_der_werkstatt("schmiede")
BOGENBAUER = W.waren_der_werkstatt("bogenbauer")
NAEHSTUBE = W.waren_der_werkstatt("naehstube")

check("die Schmiede fertigt 8 Waren", len(SCHMIEDE) == 8, f"{len(SCHMIEDE)}: {SCHMIEDE}")
check("der Bogenbauer fertigt 4 Waren", len(BOGENBAUER) == 4, f"{len(BOGENBAUER)}: {BOGENBAUER}")
check("die Naehstube fertigt 5 Waren", len(NAEHSTUBE) == 5, f"{len(NAEHSTUBE)}: {NAEHSTUBE}")
check("8 + 4 + 5 sind genau die 17 Waren",
      len(SCHMIEDE) + len(BOGENBAUER) + len(NAEHSTUBE) == 17)
check("keine Ware steht in zwei Werkstaetten",
      not (set(SCHMIEDE) & set(BOGENBAUER)) and not (set(SCHMIEDE) & set(NAEHSTUBE))
      and not (set(BOGENBAUER) & set(NAEHSTUBE)))
check("die Schmiede-Liste entspricht items.json (werkstatt = 'Schmiede')",
      set(SCHMIEDE) == {w for w, e in WAREN.items() if e.get("werkstatt") == "Schmiede"},
      str(sorted(SCHMIEDE)))
check("die Bogenbauer-Liste entspricht items.json (werkstatt = 'Bogner')",
      set(BOGENBAUER) == {w for w, e in WAREN.items() if e.get("werkstatt") == "Bogner"},
      str(sorted(BOGENBAUER)))
check("die Naehstube-Liste entspricht items.json",
      set(NAEHSTUBE) == {w for w, e in WAREN.items()
                         if e.get("werkstatt") == WERK.get("naehstube")},
      str(sorted(NAEHSTUBE)))
check("eine unbekannte Werkstatt hat keine Waren", W.waren_der_werkstatt("schlosserei") == [])
check("leere Werkstattkennung hat keine Waren", W.waren_der_werkstatt("") == [])
check("das Original nennt das Gebaeude auch 'Bogner' - beide Namen finden dieselben Waren",
      set(W.waren_der_werkstatt("Bogenbauer")) == set(W.waren_der_werkstatt("Bogner")))

check("werkstatt_fuer('Messer') ist die Schmiede", W.werkstatt_fuer("Messer") == "schmiede")
check("werkstatt_fuer('Armbrust') ist der Bogenbauer",
      W.werkstatt_fuer("Armbrust") == "bogenbauer")
check("werkstatt_fuer('Wollumhang') ist die Naehstube",
      W.werkstatt_fuer("Wollumhang") == "naehstube")
check("eine unbekannte Ware hat keine Werkstatt", W.werkstatt_fuer("Drache") is None)
check("ein Rohstoff hat keine Werkstatt", W.werkstatt_fuer("Holz") is None)
check("leerer Warenname hat keine Werkstatt", W.werkstatt_fuer("") is None)

# Jede der 17 Waren muss ueber die Rueckrichtung in ihrer eigenen Werkstatt landen.
for _w in ALLE:
    _ziel = W.werkstatt_fuer(_w)
    check(f"Rueckrichtung: '{_w}' liegt in der Liste seiner Werkstatt",
          _ziel in WERK and _w in W.waren_der_werkstatt(_ziel), f"-> {_ziel}")


# ==========================================================================
# 3. Dauer - nur wo belegt, sonst ehrlich None
# ==========================================================================

abschnitt("Dauer - das Handbuch belegt NUR das Schwert mit 20 Minuten")

check("dauer_sekunden('Schwert') = 1200 Sekunden", W.dauer_sekunden("Schwert") == 1200.0,
      str(W.dauer_sekunden("Schwert")))
check("1200 Sekunden sind 20 Minuten", W.dauer_sekunden("Schwert") == SCHMELZE)
check("dauer_belegt('Schwert') ist Wahr", W.dauer_belegt("Schwert") is True)
check("dauer_sekunden('Messer') ist None (nicht belegt)",
      W.dauer_sekunden("Messer") is None, str(W.dauer_sekunden("Messer")))
check("dauer_belegt('Messer') ist Unwahr", W.dauer_belegt("Messer") is False)
check("dauer_sekunden('Bogen') ist None (nicht belegt)", W.dauer_sekunden("Bogen") is None)
check("dauer_sekunden('Langbogen') ist None (nicht belegt)",
      W.dauer_sekunden("Langbogen") is None)
check("dauer_sekunden eines Rohstoffs ist None", W.dauer_sekunden("Holz") is None)
check("genau EINE Ware hat eine belegte Dauer (das Schwert)",
      sum(1 for w in ALLE if W.dauer_belegt(w)) == 1,
      str([w for w in ALLE if W.dauer_belegt(w)]))
check("fuer keine andere Ware wird eine Dauer erfunden",
      all(W.dauer_sekunden(w) is None for w in ALLE if w != SCHWERT))

check("hoehere Stufe verkuerzt die belegte Zeit (Stufe 3 < Stufe 1)",
      W.dauer_sekunden("Schwert", 3) < W.dauer_sekunden("Schwert", 1),
      f"{W.dauer_sekunden('Schwert', 3)} < {W.dauer_sekunden('Schwert', 1)}")
check("Stufe 1 ist die belegte Grunddauer (1200 s)",
      W.dauer_sekunden("Schwert", 1) == 1200.0)
check("Stufe 2 ist ebenfalls kuerzer als Stufe 1",
      W.dauer_sekunden("Schwert", 2) < W.dauer_sekunden("Schwert", 1))
check("die Dauer faellt ueber die Stufen 1..5 streng",
      all(W.dauer_sekunden("Schwert", s) > W.dauer_sekunden("Schwert", s + 1)
          for s in range(1, 5)))
check("eine Stufe 0 wird wie Stufe 1 behandelt",
      W.dauer_sekunden("Schwert", 0) == W.dauer_sekunden("Schwert", 1))
check("auch bei hoeherer Stufe bleibt 'belegt' Wahr (Grundwert belegt)",
      W.dauer_belegt("Schwert") is True)
befund("Stufen-Tempo der Werkstaetten ist VORSCHLAG",
       "das Handbuch belegt nur die 20 Minuten des Schwerts; der Faktor +10 % Tempo je "
       "Stufe (werkstatt.STUFE_TEMPO_PROZENT) ist wie die belegten +10 %-Stufenregeln "
       "gesetzt und nicht woertlich belegt")


# ==========================================================================
# 4. Handbuchbeispiel - 10 Schwerter, 2 Schmieden = 100 statt 200 Minuten
# ==========================================================================

abschnitt("Handbuchbeispiel - 10 Schwerter mit zwei Schmieden = 100 Minuten")

check("kapazitaet(1) = 1 Platz", W.kapazitaet(1) == 1)
check("kapazitaet(2) = 2 Plaetze", W.kapazitaet(2) == 2)
check("kapazitaet(10) = 10 Plaetze", W.kapazitaet(10) == 10)
check("kapazitaet(0) = 0 Plaetze", W.kapazitaet(0) == 0)
check("kapazitaet(-3) = 0 Plaetze (nie negativ)", W.kapazitaet(-3) == 0)

zwei = W.neue_warteschlange("schmiede", 2)
check("neue_warteschlange kennt Typ, Werkstatt und Kapazitaet",
      zwei.get("typ") == "schmiede" and zwei.get("kapazitaet") == 2
      and zwei.get("werkstatt") == WERK.get("schmiede"), str(zwei.get("typ")))
ok_ein, meld_ein = W.einreihen(zwei, SCHWERT, 10, 1)
check("10 Schwerter lassen sich einreihen", ok_ein is True, meld_ein)
check("die Meldung nennt 20,0 Minuten je Stueck", "20.0" in meld_ein, meld_ein)

f_start = W.fortschritt(zwei, 0)
check("die Restzeit ist 6000 Sekunden", f_start["rest_sekunden"] == 6000.0,
      str(f_start["rest_sekunden"]))
check("6000 Sekunden sind genau 100 Minuten", f_start["rest_sekunden"] == 100 * 60)
check("zu Beginn fertigen genau zwei Schwerter gleichzeitig",
      len(f_start["laeuft"]) == 2, str(len(f_start["laeuft"])))
check("jedes laufende Schwert braucht 1200 s Restzeit",
      all(round(x["rest_sekunden"], 3) == 1200.0 for x in f_start["laeuft"]),
      str([x["rest_sekunden"] for x in f_start["laeuft"]]))
check("das Handbuchbeispiel liefert 100 statt 200 Minuten",
      f_start["rest_sekunden"] == 100 * 60 and f_start["rest_sekunden"] < 200 * 60)

check("vor Ablauf der 20 Minuten ist noch nichts fertig",
      W.fertige_waren(zwei, 1199) == {}, str(W.fertige_waren(zwei, 1199)))
neu_1200 = W.fertige_waren(zwei, 1200)
check("nach 20 Minuten sind ZWEI Schwerter gleichzeitig fertig",
      neu_1200 == {SCHWERT: 2}, str(neu_1200))
neu_6000 = W.fertige_waren(zwei, 6000)
check("nach 100 Minuten sind die restlichen 8 fertig", sum(neu_6000.values()) == 8,
      str(neu_6000))
check("insgesamt sind es genau 10 Schwerter",
      sum(neu_1200.values()) + sum(neu_6000.values()) == 10)
check("ein zweiter Aufruf zur selben Zeit meldet nichts doppelt",
      W.fertige_waren(zwei, 6000) == {})
check("nach Abschluss bleiben keine Restsekunden",
      W.fortschritt(zwei, 6000)["rest_sekunden"] == 0.0)

# Eine einzelne Schmiede: 10 x 20 Minuten = 200 Minuten.
eins = W.neue_warteschlange("schmiede", 1)
W.einreihen(eins, SCHWERT, 10, 1)
check("mit EINER Schmiede dauert der Auftrag 12000 s (200 Minuten)",
      W.fortschritt(eins, 0)["rest_sekunden"] == 200 * 60,
      str(W.fortschritt(eins, 0)["rest_sekunden"]))
check("mit einer Schmiede laeuft nur EIN Schwert",
      len(W.fortschritt(eins, 0)["laeuft"]) == 1)
check("mit einer Schmiede sind nach 200 Minuten alle 10 fertig",
      W.fertige_waren(eins, 200 * 60) == {SCHWERT: 10},
      str(W.fertige_waren(eins, 200 * 60)))
_drei = W.neue_warteschlange("schmiede", 3)
W.einreihen(_drei, SCHWERT, 9, 1)
check("drei Schmieden lassen drei Schwerter gleichzeitig arbeiten",
      len(W.fortschritt(_drei, 0)["laeuft"]) == 3)
check("neun Schwerter mit drei Schmieden brauchen 3 x 20 = 60 Minuten",
      W.fortschritt(_drei, 0)["rest_sekunden"] == 3 * SCHMELZE,
      str(W.fortschritt(_drei, 0)["rest_sekunden"]))

# Hoehere Stufe: derselbe Auftrag ist schneller fertig.
schnell = W.neue_warteschlange("schmiede", 2)
W.einreihen(schnell, SCHWERT, 10, 3)
check("mit Stufe 3 ist der Auftrag kuerzer als 100 Minuten",
      0 < W.fortschritt(schnell, 0)["rest_sekunden"] < 6000.0,
      str(W.fortschritt(schnell, 0)["rest_sekunden"]))


# ==========================================================================
# 5. Die Warteschlange weist Falsches ab
# ==========================================================================

abschnitt("Warteschlange - unbekannte Waren und falsche Eingaben werden abgewiesen")

q = W.neue_warteschlange("schmiede", 1)
check("eine unbekannte Ware wird abgelehnt", W.einreihen(q, "Drache", 1)[0] is False,
      W.einreihen(q, "Drache", 1)[1])
check("die Ablehnung nennt die Ware", "Drache" in W.einreihen(q, "Drache", 1)[1])
check("ein Rohstoff wird abgelehnt", W.einreihen(q, "Holz", 1)[0] is False)
check("eine Ware aus einer anderen Werkstatt wird abgelehnt",
      W.einreihen(q, "Wollumhang", 1)[0] is False, W.einreihen(q, "Wollumhang", 1)[1])
check("die falsche Werkstatt wird in der Meldung genannt",
      WERK.get("schmiede") in W.einreihen(q, "Wollumhang", 1)[1])
check("die abgelehnten Waren landen NICHT im Stapel", q["einheiten"] == [],
      str(len(q["einheiten"])))
check("die Anzahl 0 wird abgelehnt", W.einreihen(q, SCHWERT, 0)[0] is False)
check("eine negative Anzahl wird abgelehnt", W.einreihen(q, SCHWERT, -1)[0] is False)
check("eine Anzahl, die keine Zahl ist, wird abgelehnt",
      W.einreihen(q, SCHWERT, "zwei")[0] is False)
check("ein leerer Warenname wird abgelehnt", W.einreihen(q, "", 1)[0] is False)
check("einreihen liefert immer (Wahrheitswert, Text)",
      isinstance(W.einreihen(q, SCHWERT, 1)[0], bool)
      and isinstance(W.einreihen(q, SCHWERT, 1)[1], str))


# ==========================================================================
# 6. Keine Dauer erfunden - nicht belegte Waren werden gehalten
# ==========================================================================

abschnitt("Nicht belegte Waren - der Stapel erfindet keine Dauer")

ohne = W.neue_warteschlange("schmiede", 1)
ok_messer, meld_messer = W.einreihen(ohne, "Messer", 3, 1)
check("3 Messer laufen in den Stapel (bekannte Ware)", ok_messer is True, meld_messer)
check("die Einreih-Meldung nennt 'Dauer nicht belegt'", "Dauer nicht belegt" in meld_messer,
      meld_messer)
f_ohne = W.fortschritt(ohne, 1_000_000)
check("fuer eine nicht belegte Ware gibt es KEINE Restzeit (None)",
      f_ohne["rest_sekunden"] is None, str(f_ohne["rest_sekunden"]))
check("der Hinweis lautet 'Dauer nicht belegt'",
      f_ohne["hinweis"] == "Dauer nicht belegt", f_ohne["hinweis"])
check("alle drei Messer stehen als 'ohne belegte Dauer' im Bericht",
      len(f_ohne["unbelegt"]) == 3, str(len(f_ohne["unbelegt"])))
check("kein Messer ist je fertig geworden, auch nach langer Zeit",
      W.fertige_waren(ohne, 10 ** 9) == {}, str(W.fertige_waren(ohne, 10 ** 9)))
check("der Text nennt die fehlende Dauer",
      "Dauer nicht belegt" in f_ohne["text"], f_ohne["text"])
check("eine leere Warteschlange meldet ebenfalls 0 Restsekunden",
      W.fortschritt(W.neue_warteschlange("schmiede", 1), 0)["rest_sekunden"] == 0.0)
_null = W.neue_warteschlange("schmiede", 0)
W.einreihen(_null, SCHWERT, 1, 1)
check("eine Warteschlange ohne Platz (0 Werkstaetten) plant nichts",
      W.fortschritt(_null, 0)["laeuft"] == [])


# ==========================================================================
# 7. Lager - lesbare Bestandszeile
# ==========================================================================

abschnitt("Lager - lesbare Bestandszeile (Handbuch Seite 14)")

check("ein leeres Lager heisst 'Lager: leer'", W.lager_text({}) == "Lager: leer")
check("ein Bestand wird lesbar ausgegeben",
      W.lager_text({SCHWERT: 3}) == "Lager: 3 Schwert", W.lager_text({SCHWERT: 3}))
check("mehrere Waren stehen mit Komma getrennt",
      W.lager_text({"Bogen": 2, SCHWERT: 3}) == "Lager: 2 Bogen, 3 Schwert",
      W.lager_text({"Bogen": 2, SCHWERT: 3}))
check("Mengen von 0 werden weggelassen",
      W.lager_text({"Bogen": 0}) == "Lager: leer", W.lager_text({"Bogen": 0}))
check("negative Mengen werden weggelassen",
      W.lager_text({"Bogen": -2}) == "Lager: leer", W.lager_text({"Bogen": -2}))
check("die Zeile enthaelt immer die Bestandsmenge und den Namen",
      W.lager_text({"Bogen": 5}).endswith("5 Bogen"), W.lager_text({"Bogen": 5}))


# ==========================================================================
# 8. Siedlungskarte - die gebauten Werkstaetten (wie gebaeude_wirkung.py)
# ==========================================================================

abschnitt("Siedlungskarte - Werkstaetten aus bauten/stufen lesen")

_karte = {"bauten": {"0": "schmiede", "1": "schmiede", "2": "haus"}, "stufen": {"0": 1}}
_bestand = W.werkstaetten_bestand([_karte])
check("zwei Schmieden werden gezaehlt", _bestand.get("schmiede") == 2, str(_bestand))
check("nicht gebaute Werkstaetten zaehlen 0",
      _bestand.get("bogenbauer") == 0 and _bestand.get("naehstube") == 0)
check("ein Haus ist keine Werkstatt und faellt heraus", _bestand.get("haus") is None)
check("ohne Siedlung ist der Bestand leer-bauend",
      W.werkstaetten_bestand([]) == {"schmiede": 0, "bogenbauer": 0, "naehstube": 0})
check("die hoechste Stufe einer Werkstatt wird gelesen",
      W.werkstatt_stufe({"bauten": {"0": "schmiede"}, "stufen": {"0": 3}}, "schmiede") == 3)
check("eine nicht gebaute Werkstatt hat Stufe 0",
      W.werkstatt_stufe({"bauten": {}, "stufen": {}}, "schmiede") == 0)
check("eine Werkstatt ohne gespeicherte Stufe gilt als Stufe 1",
      W.werkstatt_stufe({"bauten": {"0": "schmiede"}, "stufen": {}}, "schmiede") == 1)
check("die Siedlung liefert die Werkstattzahl fuer die Warteschlange (2 Schmieden)",
      W.werkstaetten_bestand([_karte])["schmiede"] == W.neue_warteschlange("schmiede", 2)["kapazitaet"])


sys.exit(bericht())
