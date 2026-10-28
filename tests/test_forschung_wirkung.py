"""
Wirkung der 21 Originalforschungen auf die Produktion (W4b-6, 04.10.2026).

Beweist, dass genau die im Handbuch belegten Forschungen die neun Rohstoffe, die
Siedlerproduktion und den Verteidigungswert anheben -- und dass alles, wovon das
Handbuch schweigt, den Faktor 1,0 behaelt. Es wird nichts erfunden.

Belegte Werte (Handbuch 2009, Abschnitt 5 'Forschung'):
  Felderwirtschaft  Nahrung +10 % je Stufe
  Steinbruch        Stein   +10 % je Stufe
  Forstwirtschaft   Holz    +10 % je Stufe
  Tierhaltung       Pferde, Wolle, Leder je +5 % je Stufe
  Minenarbeit       Metall, Gold je +5 % je Stufe
  Goetterkunde      Mana +5 % je Stufe
  Heilkunde         Siedlerproduktion +10 % je Stufe
  Mauerbau          Verteidigungswert +10 % je Stufe
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import spieldaten
import forschung_wirkung as FW

GOETTERKUNDE = "G\u00f6tterkunde"
RESSOURCEN_FORSCHUNGEN = (
    "Felderwirtschaft", "Steinbruch", "Forstwirtschaft",
    "Tierhaltung", "Minenarbeit", GOETTERKUNDE,
)
SIEBEN_THEMEN = RESSOURCEN_FORSCHUNGEN + ("Heilkunde",)
ROHSTOFFE = ("holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde")

# Rohstoff -> (Forschungsname, Prozent je Stufe) -- aus dem Handbuch abgeschrieben.
ERWARTET = {
    "holz":    ("Forstwirtschaft", 10),
    "stein":   ("Steinbruch",      10),
    "nahrung": ("Felderwirtschaft", 10),
    "metall":  ("Minenarbeit",      5),
    "gold":    ("Minenarbeit",      5),
    "mana":    (GOETTERKUNDE,       5),
    "pferde":  ("Tierhaltung",      5),
    "wolle":   ("Tierhaltung",      5),
    "leder":   ("Tierhaltung",      5),
}


def nur_diese(rohstoffe, stand, erwartete_ziele):
    """True, wenn alle neun Rohstoffe den Faktor > 1 genau fuer die Ziele zeigen."""
    for r in ROHSTOFFE:
        soll_hoeher = r in erwartete_ziele
        ist_hoeher = FW.faktor(stand, r) > 1.0
        if soll_hoeher != ist_hoeher:
            return False
    return True


# ==========================================================================
abschnitt("1. Datenbindung: die belegten Namen stehen wirklich in research.json")

daten = spieldaten.forschungen()
check("research.json hat 21 Forschungen", len(daten) == 21, str(len(daten)))
check("die neun Rohstoffe des Moduls sind vollstaendig und eindeutig",
      len(ROHSTOFFE) == 9 and len(set(ROHSTOFFE)) == 9, str(ROHSTOFFE))

for name in RESSOURCEN_FORSCHUNGEN:
    check(f"Forschung '{name}' existiert in research.json", name in daten)
for name in ("Heilkunde", "Mauerbau"):
    check(f"Forschung '{name}' existiert in research.json", name in daten)

check("befund_kontrolle() meldet keinen fehlenden Namen", FW.befund_kontrolle() == [],
      str(FW.befund_kontrolle()))

# Die Fehlererkennung selbst wird mit einem erfundenen Namen geprueft.
fake = {"holz": {"forschung": "GibtsNicht", "prozent_je_stufe": 5}}
check("die Fehlererkennung findet einen Namen, der nicht in research.json steht",
      FW.fehlende_forschungsnamen(fake) == ["GibtsNicht"],
      str(FW.fehlende_forschungsnamen(fake)))


# ==========================================================================
abschnitt("2. Jeder der neun Rohstoffe: richtiger Faktor auf Stufe 0 / 1 / 3")

for rohstoff in ROHSTOFFE:
    forschung, prozent = ERWARTET[rohstoff]
    check(f"{rohstoff}: ohne Forschung Faktor 1,0",
          FW.faktor({}, rohstoff) == 1.0, str(FW.faktor({}, rohstoff)))
    soll1 = 1.0 + prozent / 100.0
    ist1 = FW.faktor({forschung: 1}, rohstoff)
    check(f"{rohstoff}: {forschung} 1 -> {soll1:.2f}",
          ist1 == soll1, f"{ist1:.4f}")
    soll3 = 1.0 + 3 * prozent / 100.0
    ist3 = FW.faktor({forschung: 3}, rohstoff)
    check(f"{rohstoff}: {forschung} 3 -> {soll3:.2f}",
          ist3 == soll3, f"{ist3:.4f}")


# ==========================================================================
abschnitt("3. Jede Produktionsforschung hebt genau ihre Rohstoffe")

check("Tierhaltung 3 hebt genau pferde, wolle, leder",
      nur_diese(ROHSTOFFE, {"Tierhaltung": 3}, {"pferde", "wolle", "leder"}),
      str(FW.faktor_alle({"Tierhaltung": 3})))
check("Minenarbeit 3 hebt genau metall und gold",
      nur_diese(ROHSTOFFE, {"Minenarbeit": 3}, {"metall", "gold"}),
      str(FW.faktor_alle({"Minenarbeit": 3})))
check("Forstwirtschaft 3 hebt genau holz",
      nur_diese(ROHSTOFFE, {"Forstwirtschaft": 3}, {"holz"}),
      str(FW.faktor_alle({"Forstwirtschaft": 3})))
check("Steinbruch 3 hebt genau stein",
      nur_diese(ROHSTOFFE, {"Steinbruch": 3}, {"stein"}),
      str(FW.faktor_alle({"Steinbruch": 3})))
check("Felderwirtschaft 3 hebt genau nahrung",
      nur_diese(ROHSTOFFE, {"Felderwirtschaft": 3}, {"nahrung"}),
      str(FW.faktor_alle({"Felderwirtschaft": 3})))
check("Goetterkunde 3 hebt genau mana",
      nur_diese(ROHSTOFFE, {GOETTERKUNDE: 3}, {"mana"}),
      str(FW.faktor_alle({GOETTERKUNDE: 3})))

# Tierhaltung und Minenarbeit heben nicht nur einen, sondern alle ihre Ziele zugleich.
tal = FW.faktor_alle({"Tierhaltung": 3})
check("Tierhaltung 3 erhoeht pferde, wolle und leder auf denselben Wert",
      tal["pferde"] == tal["wolle"] == tal["leder"] == 1.15, str(tal))
min_ = FW.faktor_alle({"Minenarbeit": 3})
check("Minenarbeit 3 erhoeht metall und gold auf denselben Wert",
      min_["metall"] == min_["gold"] == 1.15, str(min_))


# ==========================================================================
abschnitt("4. Unbekanntes aendert nichts, kein Faktor unter 1,0")

leer = FW.faktor_alle({})
check("ohne jeden Forschungsstand sind alle neun Faktoren 1,0",
      all(v == 1.0 for v in leer.values()), str(leer))

unbekannt = FW.faktor_alle({"ErfundeneForschung": 999, "landwirtschaft": 7, "bergbau": 5})
check("eine unbekannte Forschung aendert keinen einzigen Faktor",
      all(v == 1.0 for v in unbekannt.values()), str(unbekannt))
check("der veraltete Name 'bergbau' aendert nichts mehr",
      FW.faktor({"bergbau": 10}, "holz") == 1.0, str(FW.faktor({"bergbau": 10}, "holz")))
check("ein unbekannter Rohstoff bleibt bei 1,0",
      FW.faktor({"Forstwirtschaft": 5}, "kristall") == 1.0,
      str(FW.faktor({"Forstwirtschaft": 5}, "kristall")))

check("negative Stufen zaehlen als 0 (Tierhaltung -5)",
      FW.faktor({"Tierhaltung": -5}, "wolle") == 1.0,
      str(FW.faktor({"Tierhaltung": -5}, "wolle")))
check("negative Stufen zaehlen als 0 (Forstwirtschaft -100)",
      FW.faktor({"Forstwirtschaft": -100}, "holz") == 1.0,
      str(FW.faktor({"Forstwirtschaft": -100}, "holz")))
check("Heilkunde zaehlt negativ nicht (Siedler bleiben 1,0)",
      FW.siedlerfaktor({"Heilkunde": -3}) == 1.0, str(FW.siedlerfaktor({"Heilkunde": -3})))
check("Mauerbau zaehlt negativ nicht (Verteidigung bleibt 1,0)",
      FW.verteidigungsfaktor({"Mauerbau": -3}) == 1.0,
      str(FW.verteidigungsfaktor({"Mauerbau": -3})))

# Belastungsprobe: ueber alle Forschungen und Stufen 0..10 nie unter 1,0.
alle_namen = list(RESSOURCEN_FORSCHUNGEN) + ["Heilkunde", "Mauerbau"]
nie_unter_eins = True
for name in alle_namen:
    for stufe in range(0, 11):
        if FW.faktor({name: stufe}, ROHSTOFFE[0]) < 1.0:
            nie_unter_eins = False
        for r in ROHSTOFFE:
            if FW.faktor({name: stufe}, r) < 1.0:
                nie_unter_eins = False
        if FW.siedlerfaktor({name: stufe}) < 1.0 or FW.verteidigungsfaktor({name: stufe}) < 1.0:
            nie_unter_eins = False
check("kein Faktor faellt je unter 1,0 (alle Forschungen, Stufen 0..10)",
      nie_unter_eins)

check("faktor_alle liefert genau die neun Rohstoffe",
      set(FW.faktor_alle({}).keys()) == set(ROHSTOFFE), str(sorted(FW.faktor_alle({}))))
mix = {"Forstwirtschaft": 2, "Minenarbeit": 1, "Tierhaltung": 4, GOETTERKUNDE: 2}
check("faktor_alle stimmt mit faktor() je Rohstoff ueberein",
      FW.faktor_alle(mix) == {r: FW.faktor(mix, r) for r in ROHSTOFFE},
      str(FW.faktor_alle(mix)))


# ==========================================================================
abschnitt("5. Siedlerproduktion (Heilkunde) und Verteidigungswert (Mauerbau)")

check("Siedler ohne Heilkunde: 1,0", FW.siedlerfaktor({}) == 1.0,
      str(FW.siedlerfaktor({})))
check("Heilkunde 1 -> 1,10", FW.siedlerfaktor({"Heilkunde": 1}) == 1.10,
      str(FW.siedlerfaktor({"Heilkunde": 1})))
check("Heilkunde 3 -> 1,30", FW.siedlerfaktor({"Heilkunde": 3}) == 1.30,
      str(FW.siedlerfaktor({"Heilkunde": 3})))
check("eine unbekannte Forschung hebt die Siedler nicht",
      FW.siedlerfaktor({"Erfunden": 5}) == 1.0, str(FW.siedlerfaktor({"Erfunden": 5})))

check("Verteidigung ohne Mauerbau: 1,0", FW.verteidigungsfaktor({}) == 1.0,
      str(FW.verteidigungsfaktor({})))
check("Mauerbau 1 -> 1,10", FW.verteidigungsfaktor({"Mauerbau": 1}) == 1.10,
      str(FW.verteidigungsfaktor({"Mauerbau": 1})))
check("Mauerbau 3 -> 1,30", FW.verteidigungsfaktor({"Mauerbau": 3}) == 1.30,
      str(FW.verteidigungsfaktor({"Mauerbau": 3})))


# ==========================================================================
abschnitt("6. belegte_faktoren(): neun Rohstoffe plus Siedler, mit Belegstelle")

belegt = FW.belegte_faktoren()
check("belegte_faktoren() nennt alle neun Rohstoffe",
      all(r in belegt for r in ROHSTOFFE), str(sorted(belegt)))
check("belegte_faktoren() nennt zusaetzlich die Siedlerproduktion",
      FW.SIEDLER in belegt, str(sorted(belegt)))

themen = {eintrag["forschung"] for eintrag in belegt.values()}
for name in SIEBEN_THEMEN:
    check(f"das dokumentierte Thema '{name}' steht in belegte_faktoren()",
          name in themen)
check("belegte_faktoren() deckt genau die sieben dokumentierten Themen ab",
      themen == set(SIEBEN_THEMEN), str(sorted(themen)))

felder_ok = all(
    set(eintrag.keys()) == {"forschung", "prozent_je_stufe", "_belegt"}
    and isinstance(eintrag["prozent_je_stufe"], int)
    and eintrag["_belegt"].startswith("Handbuch")
    for eintrag in belegt.values()
)
check("jeder Eintrag hat genau die drei Felder und eine Handbuch-Belegstelle",
      felder_ok, str(belegt.get("mana")))

for rohstoff, (forschung, prozent) in ERWARTET.items():
    eintrag = belegt[rohstoff]
    check(f"belegte_faktoren['{rohstoff}'] nennt {forschung} mit {prozent} %",
          eintrag["forschung"] == forschung and eintrag["prozent_je_stufe"] == prozent,
          str(eintrag))
check("belegte_faktoren['siedler'] nennt Heilkunde mit 10 %",
      belegt["siedler"]["forschung"] == "Heilkunde"
      and belegt["siedler"]["prozent_je_stufe"] == 10, str(belegt["siedler"]))


# ==========================================================================
abschnitt("7. offene_luecken(): was das Handbuch nicht sagt, wird benannt")

luecken = FW.offene_luecken()
check("offene_luecken() ist ein Woerterbuch", isinstance(luecken, dict), str(type(luecken)))
check("offene_luecken() fuehrt die Forschungen ohne Rohstoffwirkung",
      "forschungen_ohne_rohstoffwirkung" in luecken, str(sorted(luecken)))
check("offene_luecken() fuehrt die Rohstoffe ohne Beleg",
      "rohstoffe_ohne_belegte_forschung" in luecken, str(sorted(luecken)))

ohne = luecken["forschungen_ohne_rohstoffwirkung"]
check("'Kriegskunst' steht bei den Forschungen ohne Rohstoffwirkung",
      "Kriegskunst" in ohne, str(sorted(ohne)))
check("keine der sechs Rohstoffforschungen steht bei den offenen Luecken",
      not (set(RESSOURCEN_FORSCHUNGEN) & set(ohne)), str(sorted(ohne)))
check("Heilkunde und Mauerbau sind als belegt-aber-kein-Rohstoff vermerkt",
      "Heilkunde" in ohne and "Mauerbau" in ohne, str(sorted(ohne)))
check("alle neun Rohstoffe haben eine belegte Forschung (keine Luecke)",
      luecken["rohstoffe_ohne_belegte_forschung"] == {},
      str(luecken["rohstoffe_ohne_belegte_forschung"]))
check("offene_luecken() deckt alle 21 Forschungen ab (6 belegt + 15 benannt)",
      len(ohne) == 15 and len(ohne) + len(RESSOURCEN_FORSCHUNGEN) == 21,
      f"{len(ohne)} offen")


sys.exit(bericht())
