"""
Nebelseetal Remake -- Wirkung der 21 Originalforschungen auf die Produktion.

Dieses Modul beantwortet genau EINE Frage: Wie veraendert eine Forschung die Ausbeute
der neun Rohstoffe, die Siedlerproduktion und den Verteidigungswert?

Belegte Werte (Handbuch 2009, Abschnitt 5 'Forschung' in
docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md):
  Felderwirtschaft  Nahrung            +10 % je Stufe
  Steinbruch        Stein              +10 % je Stufe
  Forstwirtschaft   Holz               +10 % je Stufe
  Tierhaltung       Pferde, Wolle, Leder je  +5 % je Stufe
  Minenarbeit       Metall, Gold       +5 % je Stufe
  Goetterkunde      Mana               +5 % je Stufe
  Heilkunde         Siedlerproduktion  +10 % je Stufe
  Mauerbau          Verteidigungswert  +10 % je Stufe

Alles, wovon das Handbuch schweigt, bleibt Faktor 1,0 und wird in `offene_luecken()`
begruendet. Es wird nichts erfunden.

Formel: Faktor = 1 + prozent * stufe / 100. Fehlende oder negative Stufen zaehlen als 0,
der Faktor faellt dadurch nie unter 1,0.
"""
from __future__ import annotations

from typing import Any, Dict

import spieldaten

# Die neun Rohstoffe des Originals (Handbuch Seite 9/10).
ROHSTOFFE = ("holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde")

# Ziels chluessel der Siedlerproduktion -- kein Rohstoff, aber im Handbuch belegt.
SIEDLER = "siedler"

# Belegte Wirkungen: Ziel -> (Forschungsname, Prozent je Stufe, Belegstelle).
# Reihenfolge der Tabelle folgt dem Handbuchtext, nicht dem Alphabet.
_BELEGT: Dict[str, tuple] = {
    "nahrung": ("Felderwirtschaft", 10,
                "Handbuch 2009, Abschnitt 5: 'Nahrung +10 % je Stufe'"),
    "stein":   ("Steinbruch", 10,
                "Handbuch 2009, Abschnitt 5: 'Stein +10 % je Stufe'"),
    "holz":    ("Forstwirtschaft", 10,
                "Handbuch 2009, Abschnitt 5: 'Holz +10 % je Stufe'"),
    "pferde":  ("Tierhaltung", 5,
                "Handbuch 2009, Abschnitt 5: 'Pferde, Wolle, Leder je +5 % je Stufe'"),
    "wolle":   ("Tierhaltung", 5,
                "Handbuch 2009, Abschnitt 5: 'Pferde, Wolle, Leder je +5 % je Stufe'"),
    "leder":   ("Tierhaltung", 5,
                "Handbuch 2009, Abschnitt 5: 'Pferde, Wolle, Leder je +5 % je Stufe'"),
    "metall":  ("Minenarbeit", 5,
                "Handbuch 2009, Abschnitt 5: 'Metall und Gold je +5 % je Stufe'"),
    "gold":    ("Minenarbeit", 5,
                "Handbuch 2009, Abschnitt 5: 'Metall und Gold je +5 % je Stufe'"),
    "mana":    ("G\u00f6tterkunde", 5,
                "Handbuch 2009, Abschnitt 5: 'Mana +5 % je Stufe'"),
    "siedler": ("Heilkunde", 10,
                "Handbuch 2009, Abschnitt 5: 'Siedlerproduktion +10 % je Stufe'"),
}

# Mauerbau wirkt auf den Verteidigungswert, nicht auf einen Rohstoff.
_MAUERBAU = ("Mauerbau", 10,
             "Handbuch 2009, Abschnitt 5: 'Verteidigungswert +10 % je Stufe'")

# Die sechs Forschungen mit belegter Rohstoffwirkung.
RESSOURCEN_FORSCHUNGEN = ("Felderwirtschaft", "Steinbruch", "Forstwirtschaft",
                          "Tierhaltung", "Minenarbeit", "G\u00f6tterkunde")


def _stufe(forschungsstaende: Dict[str, Any], name: str) -> int:
    """Stufe einer Forschung, nie negativ. Fehlend oder ungueltig = 0.

    Nimmt sowohl reine Zahlen als auch Objekte mit einem Attribut ``level`` an.
    """
    if not isinstance(forschungsstaende, dict):
        return 0
    roh = forschungsstaende.get(name, 0)
    if hasattr(roh, "level"):
        roh = roh.level
    if roh is None:
        return 0
    try:
        n = int(roh)
    except (TypeError, ValueError):
        return 0
    return n if n > 0 else 0


def _faktor(prozent: int, stufe: int) -> float:
    return 1.0 + prozent * stufe / 100.0


def faktor(forschungsstaende: Dict[str, Any], rohstoff: str) -> float:
    """Produktionsfaktor fuer einen Rohstoff.

    1,0 ohne belegte Forschung; Stufe n einer Forschung mit p Prozent je Stufe
    ergibt 1 + p*n/100. Unbekannter Rohstoff oder unbekannte Forschung bleibt 1,0.
    """
    eintrag = _BELEGT.get(rohstoff)
    if eintrag is None:
        return 1.0
    name, prozent = eintrag[0], eintrag[1]
    return _faktor(prozent, _stufe(forschungsstaende, name))


def faktor_alle(forschungsstaende: Dict[str, Any]) -> Dict[str, float]:
    """Produktionsfaktor aller neun Rohstoffe."""
    return {r: faktor(forschungsstaende, r) for r in ROHSTOFFE}


def siedlerfaktor(forschungsstaende: Dict[str, Any]) -> float:
    """Faktor der Siedlerproduktion aus Heilkunde (+10 % je Stufe)."""
    name, prozent = _BELEGT[SIEDLER][0], _BELEGT[SIEDLER][1]
    return _faktor(prozent, _stufe(forschungsstaende, name))


def verteidigungsfaktor(forschungsstaende: Dict[str, Any]) -> float:
    """Faktor des Verteidigungswerts aus Mauerbau (+10 % je Stufe)."""
    name, prozent = _MAUERBAU[0], _MAUERBAU[1]
    return _faktor(prozent, _stufe(forschungsstaende, name))


def belegte_faktoren() -> Dict[str, Dict[str, Any]]:
    """Belegte Wirkungen: Ziel -> {forschung, prozent_je_stufe, _belegt}.

    Enthaelt die neun Rohstoffe und zusaetzlich den Schluessel ``siedler``
    (Heilkunde). Jeder Eintrag nennt die Handbuchstelle, aus der er stammt.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for ziel, (name, prozent, beleg) in _BELEGT.items():
        out[ziel] = {"forschung": name, "prozent_je_stufe": prozent, "_belegt": beleg}
    return out


def fehlende_forschungsnamen(faktoren: Dict[str, Dict[str, Any]]) -> list:
    """Namen aus einem ``belegte_faktoren()``-artigen Wortschatz, die in
    data/research.json fehlen. So wird ein Tippfehler sofort sichtbar, statt
    still als Faktor 1,0 durchzurutschen.
    """
    daten = spieldaten.forschungen()
    namen = {e["forschung"] for e in faktoren.values() if e.get("forschung")}
    return sorted(n for n in namen if n not in daten)


def befund_kontrolle() -> list:
    """Namen in ``belegte_faktoren()``, die NICHT in data/research.json stehen."""
    return fehlende_forschungsnamen(belegte_faktoren())


def offene_luecken() -> Dict[str, Any]:
    """Was das Handbuch NICHT sagt -- ehrlich benannt statt erfunden.

    * ``forschungen_ohne_rohstoffwirkung``: jede der 21 Forschungen, die keinen der
      neun Rohstoffe hebt, mit Begruendung.
    * ``rohstoffe_ohne_belegte_forschung``: Rohstoffe ohne Beleg (hier leer, da alle
      neun belegt sind).
    """
    daten = spieldaten.forschungen()
    ohne: Dict[str, str] = {}
    for name in daten:
        if name in RESSOURCEN_FORSCHUNGEN:
            continue
        if name == "Heilkunde":
            grund = "erhoeht die Siedlerproduktion (belegt), aber keinen der neun Rohstoffe"
        elif name == "Mauerbau":
            grund = "erhoeht den Verteidigungswert (belegt), aber keinen der neun Rohstoffe"
        else:
            grund = "Handbuch nennt keine Rohstoffwirkung; Faktor bleibt 1,0"
        ohne[name] = grund
    rohstoffe_ohne = {r: "kein Eintrag in belegte_faktoren()" for r in ROHSTOFFE if r not in _BELEGT}
    return {
        "forschungen_ohne_rohstoffwirkung": ohne,
        "rohstoffe_ohne_belegte_forschung": rohstoffe_ohne,
        "hinweis": ("Nur die sechs Forschungen aus Handbuch Abschnitt 5 mit Prozentangabe "
                    "heben Rohstoffe; alles andere bleibt 1,0."),
    }
