"""Private Spielstandarchive: eindeutig, zeitgestempelt, ohne unbemerktes Loeschen.

Zielordner: <aktueller Spielstandordner>/archiv/spielstaende/, nicht im GitHub-Code.
Ueberschreiben ist eine AUSNAHME: bestehender Slot wird wirklich ersetzt; keine
neue Historienkopie im Archiv. Die bestehende .bak-Sicherung von speichern.py
bleibt aus Gruenden der Datenintegritaet davon unberuehrt.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

BEREICHE = {"spieler", "admin", "testbereinigung", "abgebrochen"}


def archivwurzel(speicherordner: str) -> Path:
    return Path(speicherordner).resolve() / "archiv" / "spielstaende"


def ordner_anlegen(speicherordner: str) -> Path:
    wurzel = archivwurzel(speicherordner)
    for relativ in ("spieler/slot_1", "spieler/slot_2", "spieler/slot_3",
                    "admin", "testbereinigung", "abgebrochen"):
        (wurzel / relativ).mkdir(parents=True, exist_ok=True)
    return wurzel


def _zielgruppe(pfad: Path, bereich: str) -> Path:
    if bereich not in BEREICHE:
        raise ValueError("Unbekannter Archivbereich")
    import re
    name = pfad.name
    match = re.fullmatch(r"savegame_slot([123])\.json", name)
    if bereich == "spieler":
        if not match:
            raise ValueError("Kein normaler Spielerslot")
        return Path("spieler") / ("slot_" + match.group(1))
    if bereich == "admin" and name != "admin_teststand.json":
        raise ValueError("Kein Admin-Teststand")
    return Path(bereich)


def archiviere(pfad: str, bereich: str, grund: str) -> tuple[bool, str]:
    """Verschiebt eine vorhandene Datei samt ggf. .bak in ein Ereignisverzeichnis.

    Keine Datei wird vor der Sicherstellung des Zielverzeichnisses entfernt.
    Das Ereignis bekommt lokales Datum, Uhrzeit und Kollisionskennung. Ein Fehler
    wird zurueckgemeldet; es findet NIE ein unbemerktes Delete statt.
    """
    quelle = Path(pfad).resolve()
    if not quelle.is_file() or quelle.is_symlink():
        return False, "Spielstandsdatei fehlt oder ist kein regulaerer Dateipfad."
    try:
        gruppe = _zielgruppe(quelle, bereich)
        basis = ordner_anlegen(str(quelle.parent)) / gruppe
        zeit = datetime.now().astimezone()
        ereignis = basis / (zeit.strftime("%Y-%m-%d_%H-%M-%S_%f") + "_" + uuid4().hex[:8])
        ereignis.mkdir(parents=False, exist_ok=False)
        ziel = ereignis / quelle.name
        os.replace(str(quelle), str(ziel))
        # Eine .bak gehoert zum selben Archiv-Ereignis, darf aber bei Fehler nicht
        # den bereits archivierten Hauptstand wieder beschaedigen.
        backup = Path(str(quelle) + ".bak")
        if backup.is_file() and not backup.is_symlink():
            try:
                os.replace(str(backup), str(ereignis / backup.name))
            except OSError:
                pass  # Backup bleibt am Originalort statt unbemerkt zu verschwinden.
        info = {"zeitpunkt": zeit.isoformat(timespec="seconds"),
                "quelle": quelle.name, "bereich": bereich, "grund": grund,
                "wiederherstellbar": True}
        try:
            (ereignis / "ARCHIV_INFO.json").write_text(
                json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass  # Name und Nutzdaten sind auch ohne Info vorhanden.
        return True, str(ziel)
    except (OSError, ValueError) as exc:
        return False, f"Archivieren fehlgeschlagen: {exc}"


def archivierte_staende(speicherordner: str, bereich: str, slot: int | None = None) -> list[Path]:
    """Liste ohne Nebenwirkungen: neueste zuerst, nur die bekannten Namen."""
    wurzel = archivwurzel(speicherordner)
    if bereich == "spieler":
        if type(slot) is not int or slot not in (1, 2, 3):
            return []
        gruppe, name = Path("spieler") / f"slot_{slot}", f"savegame_slot{slot}.json"
    elif bereich == "admin":
        gruppe, name = Path("admin"), "admin_teststand.json"
    else:
        return []
    verzeichnis = wurzel / gruppe
    if not verzeichnis.exists():
        return []
    return sorted((p / name for p in verzeichnis.iterdir()
                   if p.is_dir() and (p / name).is_file()), reverse=True)


def wiederherstellen(archivdatei: str, zielpfad: str, *, ueberschreiben: bool = False) -> tuple[bool, str]:
    """Aus dem Archiv KOPIEREN (Original bleibt). Kein implizites Ueberschreiben."""
    import shutil
    import tempfile
    quelle, ziel = Path(archivdatei).resolve(), Path(zielpfad).resolve()
    wurzel = archivwurzel(str(ziel.parent))
    try:
        if not quelle.is_file() or quelle.is_symlink() or quelle.name != ziel.name:
            return False, "Archivdatei ist nicht zulaessig."
        if not quelle.is_relative_to(wurzel):
            return False, "Datei liegt ausserhalb des privaten Spielstandarchivs."
        if ziel.exists() and not ueberschreiben:
            return False, "Zielslot ist belegt. Erst explizit freigeben."
        # Gueltigkeit vor dem Uebernehmen kontrollieren.
        with quelle.open("r", encoding="utf-8") as f:
            inhalt = json.load(f)
        if not isinstance(inhalt, dict):
            return False, "Archiv enthaelt keinen Spielstand."
        if ziel.name == "admin_teststand.json" and not inhalt.get("admin_teststand"):
            return False, "Kein Admin-Teststand."
        if ziel.name.startswith("savegame_slot") and inhalt.get("admin_teststand"):
            return False, "Adminstand gehoert nicht in Spielerslots."
        # Auch Wiederherstellung ist eine absichtliche Ueberschreibung, keine Archivflut.
        fd, tmp = tempfile.mkstemp(prefix=".restore_", dir=str(ziel.parent))
        try:
            with os.fdopen(fd, "wb") as dest, quelle.open("rb") as src:
                shutil.copyfileobj(src, dest)
                dest.flush(); os.fsync(dest.fileno())
            os.replace(tmp, ziel)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        return True, "Spielstand aus Archiv wiederhergestellt."
    except (OSError, ValueError, UnicodeError) as exc:
        return False, f"Wiederherstellung fehlgeschlagen: {exc}"


def archiv_groesse(speicherordner: str) -> tuple[int, int]:
    """Lesende Groessenkontrolle fuer Entwickler: (Dateianzahl, Bytes).

    Keine Loeschfunktion und kein Eingriff in gespeicherte Staende. Symlinks
    werden nicht verfolgt. Vor einem spaeteren Release braucht das Archiv eine
    explizite Aufbewahrungsstrategie statt unbegrenzten Wachstums.
    """
    wurzel = archivwurzel(speicherordner)
    if not wurzel.is_dir():
        return 0, 0
    dateien, gesamt = 0, 0
    for verzeichnis, _unterordner, namen in os.walk(wurzel, followlinks=False):
        for name in namen:
            datei = Path(verzeichnis) / name
            try:
                if datei.is_symlink() or not datei.is_file():
                    continue
                dateien += 1
                gesamt += datei.stat().st_size
            except OSError:
                continue
    return dateien, gesamt
