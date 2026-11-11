"""Wo liegen die Originalquellen? Seit Register 407 (11.11.2026) NICHT mehr im Repo.

Daniels Entscheidung (11.11.2026, Register 407): Handbuch, Handbuchbilder, Website-Grafiken,
Zeitschriftenmaterial und die historischen Kartenvorlagen sind aus dem OEFFENTLICHEN Stand genommen
und liegen lokal unter `archiv/originalquellen_20261111/` (gitignoriert, also nicht im Repo).

Die Pruefdateien suchen eine Datei darum ZUERST im Repo, DANN in dieser Ablage. Fehlt beides, ist die
Provenienz nicht pruefbar - das wird als BEFUND gemeldet, nicht als Fehler: der Stand ist dadurch nicht
kaputt, nur weniger belegt.

ASCII-only, wie alle Pruefdateien (ein Umlaut waere beim Import ein Syntaxfehler).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ABLAGE = REPO / "archiv" / "originalquellen_20261111"

# Wo ein Pfad aus dem Repo in der Ablage liegt (laengster Praefix zuerst pruefen).
UMZUG = (
    ("docs/original/", ""),
    ("assets/karten/original/", "karten_original/"),
    ("docs/nebelseetal_gamestar", ""),
)


def finde(relativ: str):
    """Der Pfad der Originaldatei oder None. Erst im Repo, dann in der lokalen Ablage."""
    text = str(relativ).replace("\\", "/")
    direkt = REPO / text
    if direkt.is_file():
        return direkt
    for alt, neu in UMZUG:
        if text.startswith(alt):
            rest = text[len(alt):]
            kandidat = ABLAGE / (neu + rest)
            if kandidat.is_file():
                return kandidat
    return None


def fehlt_hinweis(anzahl: int) -> str:
    """Ein Satz fuer die Schlusszeile, wenn Originale weder im Repo noch in der Ablage liegen."""
    return (f"{anzahl} Originaldateien weder im Repo noch in {ABLAGE.name} gefunden - "
            f"Provenienz nicht geprueft (Entscheidung Register 407)")
