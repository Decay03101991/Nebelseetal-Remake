# -*- coding: ascii -*-
"""Pruefung der gemeinsamen Spieluhr: ort_tick und fensterproduktion.

Gegenstand sind die NEUEN Funktionen in src/spieloekonomie.py:
  ort_tick(ort, ab, bis, forschung)  -> neuer Ort
  fensterproduktion(orte, jetzt)     -> {rohstoff: menge}

Richtschnur sind die zwoelf Pflichtzusagen aus
docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt, Zeile 592-648, woertlich:
  'tick(3600) gleich 36x tick(100), einschliesslich Forschung, Ankunft und Produktion'.

Regeln aus data/spieloekonomie.json:
  versorgung_stunden = 24, pilot_ausbildung_minuten = 20.

Die Orte werden in dieser Datei selbst als dicts erzeugt. Jede Zusage nennt bei
Verletzung Soll und Ist.

Aufruf:  python -X utf8 tests/test_oekonomie_uhr.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import spieloekonomie as O
import gebaeude_wirkung as GW


# --------------------------------------------------------------------------- Hilfen
def ort(oid, raster, bauten, vorraete=None, bevoelkerung=5.0, ausbildung=None,
        produktionsjournal=None, waren=None, werkstaetten=None):
    """Ein Siedlungs-Ort mit allen Feldern, die ort_tick und fensterproduktion erwarten."""
    return {
        "id": oid,
        "besitzer": "spieler",
        "dimension": 0,
        "x": 0,
        "y": 0,
        "map_id": "karte1",
        "karte": {"raster": list(raster)},
        "bauten": dict(bauten),
        "stufen": {},
        "vorraete": dict(vorraete) if vorraete is not None else {"holz": 100.0},
        "waren": dict(waren) if waren is not None else {},
        "einheiten": {},
        "bevoelkerung": bevoelkerung,
        "importiert": {},
        "verbrauchsjournal": [],
        "produktionsjournal": list(produktionsjournal) if produktionsjournal else [],
        "fertigjournal": [],
        "werkstaetten": dict(werkstaetten) if werkstaetten else {},
        "ausbildung": list(ausbildung) if ausbildung else [],
    }


def wald_ort(vorraete=None, bevoelkerung=5.0, **rest):
    """Ein Ort mit genau einem Holzaeller auf Wald (4 Holz/h)."""
    return ort("W", ["wald"], {"0": "holzfaeller"},
               vorraete=vorraete, bevoelkerung=bevoelkerung, **rest)


def value_fehler(fn):
    """Fuehrt fn aus; liefert (war_es_ValueError, Nachricht)."""
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, "FALSCHE_AUSNAHME " + type(e).__name__ + ": " + str(e)
    return False, "keine Ausnahme"


# ==========================================================================
abschnitt("1. Zerlegung: ort_tick(0, 3600) == 36 x ort_tick(100er-Schritte)")

o = wald_ort()
einmal = O.ort_tick(o, 0, 3600, {})
schritt = o
for i in range(36):
    schritt = O.ort_tick(schritt, i * 100, (i + 1) * 100, {})

wert_einmal = einmal["vorraete"]["holz"]
wert_schritt = schritt["vorraete"]["holz"]
check("1a ein Aufruf (0..3600) ergibt 104.0000 Holz",
      round(wert_einmal, 4) == 104.0, "Ist " + f"{wert_einmal:.4f}")
check("1b 36 Schritte (je 100 s) ergeben 104.0000 Holz",
      round(wert_schritt, 4) == 104.0, "Ist " + f"{wert_schritt:.4f}")
check("1c beide Wege liefern denselben Vorrat auf 4 Stellen",
      round(wert_einmal, 4) == round(wert_schritt, 4),
      "einmal " + f"{wert_einmal:.4f}" + " / 36x " + f"{wert_schritt:.4f}")
check("1d der Unterschied ist nur Gleitkomma-Rauschen (< 1e-9)",
      abs(wert_einmal - wert_schritt) < 1e-9,
      "Differenz " + f"{abs(wert_einmal - wert_schritt):.2e}")
check("1e der Einzelaufruf schreibt genau EINE Journalzeile",
      len(einmal["produktionsjournal"]) == 1,
      "Ist " + str(len(einmal["produktionsjournal"])))
check("1f die 36 Schritte schreiben 36 Journalzeilen (keine ueberschrieben)",
      len(schritt["produktionsjournal"]) == 36,
      "Ist " + str(len(schritt["produktionsjournal"])))


# ==========================================================================
abschnitt("2. Krumme Spanne: die Menge ist linear in der Dauer")

o = wald_ort(vorraete={"holz": 100.0})
d1 = 1234.5
r1 = O.ort_tick(o, 0, d1, {})
prod1 = r1["vorraete"]["holz"] - 100.0
erwartet1 = 4.0 * d1 / 3600.0
check("2a 1234,5 s ergeben 4 Holz/h x Dauer",
      abs(prod1 - erwartet1) < 1e-9,
      "Ist " + f"{prod1:.6f}" + " Soll " + f"{erwartet1:.6f}")
d2 = 2469.0
r2 = O.ort_tick(o, 0, d2, {})
prod2 = r2["vorraete"]["holz"] - 100.0
check("2b doppelte Dauer ergibt doppelte Menge (linear)",
      abs(prod2 - 2.0 * prod1) < 1e-9,
      "Ist " + f"{prod2:.6f}" + " Soll " + f"{2.0 * prod1:.6f}")


# ==========================================================================
abschnitt("3. Der Ertrag kommt aus der Karte (Holzaeller Wald/Steppe/Berg)")

r_wald = O.ort_tick(ort("Wald", ["wald"], {"0": "holzfaeller"}), 0, 3600, {})
p_wald = r_wald["vorraete"]["holz"] - 100.0
r_steppe = O.ort_tick(ort("Steppe", ["steppe"], {"0": "holzfaeller"}), 0, 3600, {})
p_steppe = r_steppe["vorraete"]["holz"] - 100.0
r_berg = O.ort_tick(ort("Berg", ["berg"], {"0": "holzfaeller"}), 0, 3600, {})
p_berg = r_berg["vorraete"]["holz"] - 100.0
check("3a Holzaeller auf Wald liefert 4.0/h", abs(p_wald - 4.0) < 1e-9,
      "Ist " + f"{p_wald:.4f}")
check("3b Holzaeller auf Steppe liefert 2.0/h", abs(p_steppe - 2.0) < 1e-9,
      "Ist " + f"{p_steppe:.4f}")
check("3c Holzaeller auf Berg (nicht passendes Feld) liefert nichts",
      abs(p_berg) < 1e-12, "Ist " + f"{p_berg:.4f}")
check("3d der Berg-Ertrag steht als leere Menge im Journal",
      r_berg["produktionsjournal"][-1]["mengen"] == {},
      str(r_berg["produktionsjournal"][-1]["mengen"]))


# ==========================================================================
abschnitt("4. Forschungsfaktor hebt den Ertrag (Forstwirtschaft)")

o = wald_ort(vorraete={"holz": 100.0})
ohne = O.ort_tick(o, 0, 3600, {})
mit = O.ort_tick(o, 0, 3600, {"Forstwirtschaft": 1})
p_ohne = ohne["vorraete"]["holz"] - 100.0
p_mit = mit["vorraete"]["holz"] - 100.0
check("4a ohne Forschung 4.0 Holz", abs(p_ohne - 4.0) < 1e-9,
      "Ist " + f"{p_ohne:.4f}")
check("4b mit Forstwirtschaft 1 MEHR Holz als ohne",
      p_mit > p_ohne, "mit " + f"{p_mit:.4f}" + " > ohne " + f"{p_ohne:.4f}")
check("4c der Faktor ist genau 1,1 (+10 Prozent je Stufe)",
      abs(p_mit - 4.4) < 1e-9, "Ist " + f"{p_mit:.4f}" + " Soll 4.4000")


# ==========================================================================
abschnitt("5. Siedler wachsen bis zur Grenze, nie darueber")

o = wald_ort(vorraete={"holz": 0.0}, bevoelkerung=5.0)
r = O.ort_tick(o, 0, 1000 * 3600, {})
grenze = GW.bevoelkerungsgrenze([r])
check("5a nach 1000 h ist die Bevoelkerungsgrenze exakt erreicht",
      r["bevoelkerung"] == grenze,
      "Ist " + str(r["bevoelkerung"]) + " Grenze " + str(grenze))
check("5b die Grenze wird nicht ueberschritten", r["bevoelkerung"] <= grenze,
      "Ist " + str(r["bevoelkerung"]))
r2 = O.ort_tick(r, 1000 * 3600, 2000 * 3600, {})
check("5c auch eine weitere lange Spanne hebt sie nicht darueber",
      r2["bevoelkerung"] == grenze and r2["bevoelkerung"] <= grenze,
      "Ist " + str(r2["bevoelkerung"]) + " Grenze " + str(grenze))
check("5d die Bevoelkerung ist ueberhaupt gewachsen (Start 5)",
      r["bevoelkerung"] > 5.0, "Ist " + str(r["bevoelkerung"]))


# ==========================================================================
abschnitt("6. Produktionsjournal: eine Zeile je Spanne, nichts ueberschrieben")

o = wald_ort()
r1 = O.ort_tick(o, 0, 3600, {})
j1 = r1["produktionsjournal"]
check("6a nach dem ersten ort_tick genau EINE neue Journalzeile",
      len(j1) == 1, "Ist " + str(len(j1)))
z = j1[0] if j1 else {}
check("6b die Zeile hat ab=0 und bis=3600",
      z.get("ab") == 0 and z.get("bis") == 3600, str(z))
check("6c die Zeile traegt die Menge 4.0 Holz",
      z.get("mengen") == {"holz": 4.0}, str(z.get("mengen")))
r2 = O.ort_tick(r1, 3600, 7200, {})
j2 = r2["produktionsjournal"]
check("6d nach dem zweiten Aufruf sind es ZWEI Zeilen",
      len(j2) == 2, "Ist " + str(len(j2)))
check("6e die erste Zeile bleibt unveraendert",
      j2[0].get("ab") == 0 and j2[0].get("bis") == 3600
      and j2[0].get("mengen") == {"holz": 4.0}, str(j2[0]))
check("6f die zweite Zeile ist ab=3600 bis=7200",
      j2[1].get("ab") == 3600 and j2[1].get("bis") == 7200, str(j2[1]))


# ==========================================================================
abschnitt("7. Ausbildung wird genau EINMAL gebucht")

# Pilotdauer: 20 Minuten = 1200 s, Ende liegt in der Spanne 0..3600.
auftrag = [{"einheit": "Krieger", "gebaeude": "kriegerakademie",
            "start": 0, "ende": 1200, "gebucht": False}]
o = ort("Aus", ["wald"], {"0": "holzfaeller"}, ausbildung=auftrag)
r1 = O.ort_tick(o, 0, 3600, {})
n1 = r1["einheiten"].get("Krieger", 0)
check("7a der erste ort_tick erzeugt genau EINE Einheit", n1 == 1, "Ist " + str(n1))
check("7b der Auftrag ist als gebucht markiert",
      r1["ausbildung"][0]["gebucht"] is True, str(r1["ausbildung"][0]["gebucht"]))
r2 = O.ort_tick(r1, 0, 3600, {})
n2 = r2["einheiten"].get("Krieger", 0)
check("7c derselbe Zeitraum ein zweites Mal bucht NICHTS nach", n2 == 1,
      "Ist " + str(n2))
check("7d es gibt genau EINEN Einheiten-Eintrag im Fertigjournal",
      len([e for e in r2["fertigjournal"] if e.get("art") == "einheit"]) == 1,
      str(r2["fertigjournal"]))


# ==========================================================================
abschnitt("8. Zeitlauf: bis < ab wirft ValueError")

ok, t = value_fehler(lambda: O.ort_tick(wald_ort(), 100, 50, {}))
check("8a ort_tick mit bis < ab wirft ValueError", ok, t)
ok, t = value_fehler(lambda: O.ort_tick(wald_ort(), 3600, 3599.999, {}))
check("8b auch eine winzige Rueckwaerts-Spanne wird abgelehnt", ok, t)
ok, t = value_fehler(lambda: O.ort_tick(wald_ort(), 0, 0, {}))
check("8c bis == ab ist erlaubt (keine Ausnahme)", not ok and t == "keine Ausnahme", t)


# ==========================================================================
abschnitt("9. Versorgungsfenster 24 h: volle und halbe Menge")

o = wald_ort(produktionsjournal=[{"ab": 0, "bis": 86400.0,
                                  "mengen": {"holz": 96.0}}])
voll = O.fensterproduktion([o], 86400)
halb = O.fensterproduktion([o], 43200)
check("9a bei jetzt=86400 zaehlt die volle Menge 96.0",
      abs(voll.get("holz", 0) - 96.0) < 1e-9,
      "Ist " + f"{voll.get('holz', 0):.4f}")
check("9b bei jetzt=43200 zaehlt die HALBE Menge 48.0",
      abs(halb.get("holz", 0) - 48.0) < 1e-9,
      "Ist " + f"{halb.get('holz', 0):.4f}")


# ==========================================================================
abschnitt("10. Fensterschnitt ueber zwei Journalzeilen")

o = wald_ort(produktionsjournal=[
    {"ab": 0, "bis": 3600.0, "mengen": {"holz": 4.0}},
    {"ab": 3600.0, "bis": 7200.0, "mengen": {"holz": 8.0}},
])
bei7200 = O.fensterproduktion([o], 7200)
bei5400 = O.fensterproduktion([o], 5400)
check("10a bei jetzt=7200 zaehlen beide Zeilen voll (4+8=12.0)",
      abs(bei7200.get("holz", 0) - 12.0) < 1e-9,
      "Ist " + f"{bei7200.get('holz', 0):.4f}")
check("10b bei jetzt=5400 zaehlt die zweite Zeile nur halb (4+4=8.0)",
      abs(bei5400.get("holz", 0) - 8.0) < 1e-9,
      "Ist " + f"{bei5400.get('holz', 0):.4f}")


# ==========================================================================
abschnitt("11. Fenster ohne Journal ergibt {} (kein Absturz)")

leer = O.fensterproduktion([{"id": "leer"}], 86400)
check("11a ein Ort ganz ohne produktionsjournal ergibt {}", leer == {}, str(leer))
leer2 = O.fensterproduktion([wald_ort(produktionsjournal=[])], 86400)
check("11b ein leerer produktionsjournal ergibt {}", leer2 == {}, str(leer2))


# ==========================================================================
abschnitt("12. Kein Rohstoff entsteht: Zuwachs == Journalmenge")

o = ort("M", ["wald", "berg"], {"0": "holzfaeller", "1": "steinmetz"},
        vorraete={"holz": 100.0, "stein": 50.0})
vorher = sum(o["vorraete"].values())
r = O.ort_tick(o, 0, 3600, {})
nachher = sum(r["vorraete"].values())
zeile = r["produktionsjournal"][-1]
zuwachs = nachher - vorher
journal_summe = sum(zeile["mengen"].values())
check("12a der Gesamtzuwachs ist genau die Summe der Journalmengen",
      abs(zuwachs - journal_summe) < 1e-9,
      "Zuwachs " + f"{zuwachs:.6f}" + " Journal " + f"{journal_summe:.6f}")
check("12b Holz waechst genau um die Journalmenge Holz",
      abs((r["vorraete"]["holz"] - 100.0) - zeile["mengen"].get("holz", 0)) < 1e-9,
      "Ist " + f"{r['vorraete']['holz'] - 100.0:.6f}")
check("12c Stein waechst genau um die Journalmenge Stein",
      abs((r["vorraete"]["stein"] - 50.0) - zeile["mengen"].get("stein", 0)) < 1e-9,
      "Ist " + f"{r['vorraete']['stein'] - 50.0:.6f}")
check("12d kein weiterer Rohstoff taucht still auf",
      set(r["vorraete"]) == {"holz", "stein"}, str(sorted(r["vorraete"])))


sys.exit(bericht())
