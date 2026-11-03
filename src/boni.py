# -*- coding: ascii -*-
"""Die Wirkung der Volks- und Taktikboni: Datenschicht und Rechnung (V-5, 03.11.2026).

Warum ein eigenes Modul: die Prozentwerte gehoeren in eine Datendatei (`data/boni.json`), und
`bottaktik.py` darf keine Datei oeffnen (eigene Wache). Also liest DIESES Modul die Datei, und
`bottaktik.modifikatoren` fragt hier nach - wie schon bei `voelker.py`.

Die Rechnung ist ADDITIV (Entscheidung Daniel 03.11.2026, Fragenrunde V-5): treffen ein Volk und
eine Taktik dieselbe Groesse (Silra Reise, Krank AT), werden die Prozente addiert und dann EINMAL
angewandt. 5 % + 5 % ergibt +10 %, nicht +10,25 %. Die Forschung rechnet weiter multiplikativ
(`bonus_system`), das bleibt unberuehrt.

Eine Wahrheit je Groesse: die ZAHLEN stehen nur hier (aus `data/boni.json`), die ANZEIGETEXTE nur in
`data/voelker.json`. `tests/test_boni.py` prueft, dass beide dieselben Voelker und dieselben
Prozentsaetze tragen.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Dict, Optional

DATEI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "boni.json")

# Ohne lesbare Datei wirkt NICHTS (Faktor 1,0). Das ist die ehrliche Vorgabe: lieber keine Wirkung
# als eine geratene Zahl.
RUECKFALL: Dict[str, object] = {"aktiv": False, "ueberschneidung": "additiv",
                                "sperrzeit_stunden": 0, "groessen": {}, "voelker": {}, "taktiken": {}}


def lade(pfad: str = None) -> dict:
    """Die Rohdaten der Datendatei - bei Fehler der leere Rueckfall (kein Erfinden).

    Das Ergebnis wird EINMAL gelesen und gemerkt (`_lade_gecacht`): die Datei aendert sich waehrend
    einer Partie nicht, und der Ertrag wird je Dorf und Stunde oft gerechnet. Wer sie liest, darf
    das Dict NICHT veraendern - alle oeffentlichen Funktionen geben Kopien oder neue Dicts zurueck.
    """
    return _lade_gecacht(pfad or DATEI)


@lru_cache(maxsize=8)
def _lade_gecacht(ziel: str) -> dict:
    """Die eigentliche Leseoperation, einmal je Pfad (siehe `lade`)."""
    try:
        with open(ziel, encoding="utf-8") as f:
            daten = json.load(f)
        return daten if isinstance(daten, dict) else dict(RUECKFALL)
    except (OSError, ValueError):
        return dict(RUECKFALL)


def aktiv(pfad: str = None) -> bool:
    """Ist die Wirkung eingeschaltet? (Schalter in der Datendatei, ohne Code zu aendern)"""
    return bool(lade(pfad).get("aktiv"))


def ueberschneidung(pfad: str = None) -> str:
    """Wie zwei Quellen auf dieselbe Groesse wirken: heute nur 'additiv' (Daniel 03.11.2026)."""
    return str(lade(pfad).get("ueberschneidung") or "additiv").strip().lower()


def sperrzeit_sekunden(pfad: str = None) -> float:
    """Sperrzeit des Taktikboni nach einem Taktikwechsel, in Sekunden (0 = keine Sperre)."""
    try:
        stunden = float(lade(pfad).get("sperrzeit_stunden") or 0)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, stunden) * 3600.0


def groessen(pfad: str = None) -> Dict[str, dict]:
    """Die Tabelle der Groessen (Art, Rohstoff, Anzeigetext) - Kopie, niemand aendert die Quelle."""
    roh = lade(pfad).get("groessen") or {}
    return {str(k): dict(v) for k, v in roh.items() if isinstance(v, dict)}


def _werte_liste(quelle: str, name: str, pfad: str = None) -> Dict[str, float]:
    """Summierte Prozente je Groesse fuer Volk ODER Taktik (additiv, doppelte Groessen addieren).

    Liefert {Groesse: Prozent}. Unbekannter Name oder kaputter Eintrag ergibt {} - keine Zahl, die
    niemand belegen kann.
    """
    tabelle = lade(pfad).get(quelle) or {}
    eintraege = tabelle.get(str(name)) if isinstance(tabelle, dict) else None
    ergebnis: Dict[str, float] = {}
    for e in (eintraege or []):
        if not isinstance(e, dict):
            continue
        groesse = str(e.get("groesse") or "").strip()
        if not groesse:
            continue
        try:
            prozent = float(e.get("prozent"))
        except (TypeError, ValueError):
            continue
        ergebnis[groesse] = ergebnis.get(groesse, 0.0) + prozent
    return ergebnis


def volk_werte(kennung: str, pfad: str = None) -> Dict[str, float]:
    """Die Prozente eines Volkes je Groesse (leer bei unbekanntem Volk)."""
    return _werte_liste("voelker", kennung, pfad)


def taktik_werte(name: str, pfad: str = None) -> Dict[str, float]:
    """Die Prozente einer Taktik je Groesse (leer bei unbekannter Taktik)."""
    return _werte_liste("taktiken", name, pfad)


def modifikatoren(fraktion: str = "", taktik: str = "", taktik_bonus_aktiv: bool = True,
                  pfad: str = None) -> Dict[str, float]:
    """Die summierten Prozente je Groesse aus Volk und (aktiver) Taktik - ADDIERT.

    `taktik_bonus_aktiv` kommt aus der Sperrzeit/der Taktik des Bots (`bottaktik`); ist er False,
    zaehlt nur das Volk. Ist die Wirkung abgeschaltet (`aktiv` false) oder die Datei kaputt, kommt
    ein leeres Dict - dann rechnet niemand mit einem Bonus.
    """
    if not aktiv(pfad):
        return {}
    ergebnis = dict(volk_werte(fraktion, pfad)) if fraktion else {}
    if taktik and taktik_bonus_aktiv:
        for groesse, prozent in taktik_werte(taktik, pfad).items():
            ergebnis[groesse] = ergebnis.get(groesse, 0.0) + prozent
    return {g: p for g, p in ergebnis.items() if p}


def faktor(prozent: float) -> float:
    """Ein Prozentwert als Faktor: 5 -> 1,05; -5 -> 0,95. Untergrenze 0 (nie negativ)."""
    try:
        return max(0.0, 1.0 + float(prozent) / 100.0)
    except (TypeError, ValueError):
        return 1.0


def faktoren(werte: Optional[dict], pfad: str = None) -> Dict[str, float]:
    """{Groesse: Prozent} als {Groesse: Faktor} (1,0 = keine Wirkung, fehlende Groessen fehlen)."""
    return {str(g): faktor(p) for g, p in (werte or {}).items()}


def ertragsfaktor(fraktion: str = "", rohstoff: str = "", pfad: str = None) -> float:
    """Ertragsfaktor EINES Rohstoffs aus dem Volk (Taktiken wirken nicht auf Ertraege).

    Bei abgeschalteter Wirkung (`aktiv: false`) kommt 1,0 - der Schalter gilt auch hier, nicht nur
    in `modifikatoren`.
    """
    roh = str(rohstoff or "").strip().lower()
    if not roh or not aktiv(pfad):
        return 1.0
    return faktor(volk_werte(fraktion, pfad).get(f"ertrag_{roh}", 0.0))


def reisezeitfaktor(fraktion: str = "", taktik: str = "", taktik_bonus_aktiv: bool = True,
                    pfad: str = None) -> float:
    """Faktor auf die REISEZEIT (nicht auf die Geschwindigkeit): +5 % schneller = 1/1,05.

    So bleibt die Anzeige dieselbe Groesse wie die Rechnung: die Zeit wird geteilt, nicht die
    Geschwindigkeit erfunden.
    """
    prozent = modifikatoren(fraktion, taktik, taktik_bonus_aktiv, pfad).get("reise", 0.0)
    schnell = faktor(prozent)
    return 1.0 / schnell if schnell > 0 else 1.0


def kampf_werte(werte: Optional[dict]) -> Dict[str, float]:
    """AT und PA als Prozente fuer den Kampf aus einem Modifikatoren-Dict.
    Zwei Groessen, eine Rechnung: "verteidigung" (Brynhilds Taktikbonus) zaehlt zur PA des
    Verteidigers - sie ist im Handbuch dieselbe Kennzahl, nur anders benannt. "beute" bleibt
    daneben stehen, weil der Kampf sie getrennt braucht.
    """
    werte = werte or {}

    def _z(schluessel: str) -> float:
        try:
            return float(werte.get(schluessel) or 0.0)
        except (TypeError, ValueError):
            return 0.0

    return {"at": _z("at"), "pa": _z("pa") + _z("verteidigung"), "beute": _z("beute")}


def preis_faktor(fraktion: str = "", pfad: str = None) -> float:
    """Faktor auf GEBAEUDEPREISE aus dem Volk (Gnome: -5 % = 0,95). 1,0 heisst kein Rabatt.

    Daniel 03.11.2026: "Ausbau +5 %" der Gnome wirkt als 5 % guenstigerer Ausbau. Bei den Bots
    aendert das nichts - sie bauen nicht (siehe `groessen()["ausbau"]`).
    """
    return faktor(modifikatoren(fraktion, pfad=pfad).get("baukosten", 0.0))
