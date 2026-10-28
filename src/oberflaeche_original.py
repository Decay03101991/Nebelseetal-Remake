"""
Nebelseetal Remake - Menue-Vergleich (Paket W7, 04.10.2026).

Stellt das WOERTLICH belegte Original-Menue (Datenblatt `data/menue_original.json`,
Quelle: archiv/analysen/audits/astra_gamestar_antwort.txt, Screenshot 1838855) gegen das Menue
des laufenden Spiels. Das laufende Menue steht als `MENU_ITEMS` in `src/main.py`;
dieses Modul LIEST `main.py` als TEXT und importiert es NICHT (main ist eine
Fensteranwendung).

Belegte Fassung des Originals:
  Uebersicht, Portal, Diplomatie, Einstellungen, Ruhmeshalle, Gildenhalle,
  Voraussetzungen, Nachrichten, Neuigkeiten, Anleitung, Schlachtsimulator,
  Forum, Chat, Spieler werben, Logout.
Dazu oben die Rohstoffleiste, links "Eure Punkte: Forschung / Krieg / Gesamt",
unten "Laufende Auftraege:".

Offline-Regel: Forum, Chat, Spieler werben und Logout sind Netz-/Mehrspieler-
funktionen. Sie bleiben dokumentiert, gehoeren aber NICHT in das ausgelieferte
Einzelspieler-Spiel (`offline_menue()` laesst genau diese vier weg).

Das Modul rechnet/liest nur und aendert keine andere Datei. Nur Standardbibliothek,
keine Fensterbibliothek, kein Netz.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# --------------------------------------------------------------------------
# Pfade (relativ zu dieser Datei, damit das Ergebnis ortsunabhaengig ist)
# --------------------------------------------------------------------------

_HIER = Path(__file__).resolve().parent
_WURZEL = _HIER.parent
_DATENDATEI = _WURZEL / "data" / "menue_original.json"
_MAIN_DATEI = _HIER / "main.py"


# --------------------------------------------------------------------------
# Griffe auf das Datenblatt
# --------------------------------------------------------------------------

def _daten() -> dict:
    """Das Datenblatt `data/menue_original.json` als Verzeichnis."""
    with open(_DATENDATEI, "r", encoding="utf-8") as f:
        return json.load(f)


def netz_eintraege() -> list:
    """Die vier Netz-/Mehrspieler-Eintraege, die NICHT ins Einzelspieler-Spiel kommen."""
    return list(_daten().get("netz_eintraege", []))


# --------------------------------------------------------------------------
# 1. Das Original-Menue
# --------------------------------------------------------------------------

def original_menue() -> list:
    """Alle belegten Originaleintraege in belegter Reihenfolge.

    Jeder Eintrag ist ein Verzeichnis mit `name`, `reihenfolge`, `quelle` und dem
    Kennzeichen `offline` (True = gehoert ins Offline-Remake).
    """
    return [dict(e) for e in _daten().get("eintraege", [])]


def offline_menue() -> list:
    """Nur die Eintraege, die ins OFFLINE-Einzelspieler-Remake gehoeren (Namen, in Reihenfolge).

    Genau die vier Netz-Eintraege (Forum, Chat, Spieler werben, Logout) fallen weg.
    """
    return [e["name"] for e in original_menue() if e.get("offline")]


# --------------------------------------------------------------------------
# 2. Das Menue des laufenden Spiels (main.py als TEXT, nicht importiert!)
# --------------------------------------------------------------------------

def _menue_aus_text(text: str) -> list:
    """Liest die Namen der Liste `MENU_ITEMS` aus einem Quelltext heraus."""
    treffer = re.search(r"MENU_ITEMS\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not treffer:
        return []
    return re.findall(r"\"([^\"]+)\"", treffer.group(1))


def aktuelles_menue() -> list:
    """Die Namen aus `MENU_ITEMS` in `src/main.py`, gelesen als TEXT (kein Import)."""
    text = _MAIN_DATEI.read_text(encoding="utf-8")
    return _menue_aus_text(text)


# --------------------------------------------------------------------------
# 3. Abweichungen
# --------------------------------------------------------------------------

def fehlend() -> list:
    """Was das Offline-Soll hat, dem Spiel aber fehlt (Soll - Ist)."""
    ist = set(aktuelles_menue())
    return [name for name in offline_menue() if name not in ist]


def zusaetzlich() -> list:
    """Was das Spiel zusaetzlich fuehrt, das Offline-Soll aber nicht kennt (Ist - Soll)."""
    soll = set(offline_menue())
    return [name for name in aktuelles_menue() if name not in soll]


def reihenfolge_abweichungen() -> list:
    """Eintraege, die in beiden Listen vorkommen, aber unterschiedlich weit oben stehen.

    Verglichen werden nur die gemeinsamen Namen; ihre Stelle wird innerhalb der
    gemeinsamen Namen gezaehlt (1 = ganz oben). Jede Abweichung ist ein Verzeichnis
    mit `name`, `soll_stelle` und `ist_stelle`.
    """
    soll = offline_menue()
    ist = aktuelles_menue()
    gemeinsam = [name for name in soll if name in ist]
    soll_stelle = {name: i + 1 for i, name in enumerate(gemeinsam)}
    ist_gemeinsam = [name for name in ist if name in soll]
    ist_stelle = {name: i + 1 for i, name in enumerate(ist_gemeinsam)}

    abweichungen = []
    for name in gemeinsam:
        if soll_stelle[name] != ist_stelle[name]:
            abweichungen.append({
                "name": name,
                "soll_stelle": soll_stelle[name],
                "ist_stelle": ist_stelle[name],
            })
    return abweichungen


# --------------------------------------------------------------------------
# 4. Punktezeile und Auftragszeile (links/unten im Original)
# --------------------------------------------------------------------------

def punktezeile() -> dict:
    """Der belegte linke Statusblock: 'Eure Punkte' mit Forschung/Krieg/Gesamt und darunter
    'Laufende Auftraege:'."""
    return dict(_daten().get("punktezeile", {}))


# --------------------------------------------------------------------------
# 5. Lesbarer Bericht
# --------------------------------------------------------------------------

def abweichungsbericht() -> str:
    """Ein lesbarer deutscher Text: Original gegen Spiel, mit allen Abweichungen."""
    original = original_menue()
    offline = offline_menue()
    ist = aktuelles_menue()
    netz = netz_eintraege()

    fehlt = fehlend()
    zuviel = zusaetzlich()
    reihenfolge = reihenfolge_abweichungen()
    punkte = punktezeile()

    zeilen = []
    zeilen.append("Abweichungsbericht: Original-Menue gegen das Spiel")
    zeilen.append("=" * 50)
    zeilen.append(f"Original belegt: {len(original)} Eintraege.")
    zeilen.append(f"Davon offline spielbar: {len(offline)} (Netz-Eintraege weggelassen: "
                  + ", ".join(netz) + ").")
    zeilen.append(f"Das Spiel fuehrt: {len(ist)} Eintraege.")
    zeilen.append("")
    zeilen.append(f"Fehlt dem Spiel ({len(fehlt)}): "
                  + (", ".join(fehlt) if fehlt else "nichts"))
    zeilen.append(f"Zusaetzlich im Spiel ({len(zuviel)}): "
                  + (", ".join(zuviel) if zuviel else "nichts"))
    zeilen.append(f"Reihenfolge-Abweichungen ({len(reihenfolge)}):")
    if reihenfolge:
        for eintrag in reihenfolge:
            zeilen.append(f"  - {eintrag['name']}: soll Stelle {eintrag['soll_stelle']}, "
                          f"ist Stelle {eintrag['ist_stelle']}")
    else:
        zeilen.append("  keine")
    zeilen.append("")
    zeilen.append(f"Punktezeile: {punkte.get('titel', '?')} - "
                  + " / ".join(punkte.get("zeilen", [])))
    zeilen.append(f"Darunter: {punkte.get('darunter', '?')}")
    return "\n".join(zeilen)
