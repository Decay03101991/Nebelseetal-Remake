"""
Robustes Speichern (Paket W8) - atomar, geprueft, mit Sicherung und Wiederherstellung.

Warum ein eigenes Modul:
  Der Spielstand wird derzeit direkt in die Zieldatei geschrieben (``json.dump`` auf den
  Endpfad). Bricht der Vorgang mittendrin ab - Stromausfall, voller Datentraeger, ein Fehler
  beim Serialisieren -, ist die EINZIGE Spielstandsdatei beschaedigt und damit verloren.

Dieses Modul loest das mit dem ueblichen Muster:
  1. Zuerst in eine Zwischendatei ``<pfad>.tmp`` schreiben, mit ``flush`` + ``os.fsync``.
  2. Die Zwischendatei wieder EINLESEN und mit den Daten vergleichen (jeder Schreibvorgang
     wird geprueft - ein Schreibvorgang, den niemand zurueckliest, ist nur eine Behauptung).
  3. Erst dann ``os.replace`` - das ist auf demselben Dateisystem ein atomarer Umsprung.
     Es gibt also entweder den alten ODER den neuen Spielstand, niemals einen halben.

Alle Funktionen sind ehrlich: sie werfen nicht, sie melden (ja/nein, Meldung). Schlaegt
etwas fehl, bleibt die alte Datei unangetastet.

Regeln dieses Moduls:
  * nur Standardbibliothek (json, os, time)
  * importiert NICHT ``main.py`` (keine GUI, keine Spielabhaengigkeit)
  * reiner ASCII-Quelltext; deutsche Texte nur in Meldungen
  * kein tkinter, kein Netz, kein Zugriff auf fremde Dateien

Oeffentliche Schnittstelle:
  speichere(daten, pfad) -> (bool, str)
  lade(pfad) -> (daten|None, str)
  sichere_kopie(pfad) -> (bool, str)
  pruefe_datei(pfad) -> dict
  wiederherstellen(pfad) -> (bool, str)
  aufraeumen(pfad) -> list
  offene_luecken() -> dict
"""
from __future__ import annotations

import json
import os
import time

ENDUNG_TMP = ".tmp"
ENDUNG_BAK = ".bak"


# ---------------------------------------------------------------- interne Helfer

def _lies_text(pfad: str):
    """Liest eine Datei als Text. Gibt (text, None) oder (None, fehler) zurueck. Wirft nie."""
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return f.read(), None
    except OSError as e:
        return None, f"Datei nicht lesbar ({type(e).__name__}): {e}"
    except Exception as e:                                  # defensiv, wirklich nie werfen
        return None, f"Datei nicht lesbar ({type(e).__name__}): {e}"


def _lies_json(pfad: str):
    """Liest eine Datei als JSON. Gibt (daten, None) oder (None, fehler) zurueck. Wirft nie."""
    text, fehler = _lies_text(pfad)
    if text is None:
        return None, fehler
    try:
        return json.loads(text), None
    except ValueError as e:
        return None, f"JSON beschaedigt ({type(e).__name__}): {e}"


def _serialisiere(daten):
    """Wandelt ein dict in JSON-Text. Gibt (text, None) oder (None, fehler) zurueck. Wirft nie.

    Wichtig: Schlaegt die Serialisierung fehl, wurde die ALTE Datei noch nicht angefasst -
    genau das ist der Sinn.
    """
    try:
        return json.dumps(daten, indent=2, ensure_ascii=False), None
    except Exception as e:
        return None, f"Serialisierung fehlgeschlagen ({type(e).__name__}): {e}"


def _entferne_quiet(pfad: str) -> None:
    """Fehlgeschlagene Zwischendatei archivieren statt vernichten.

    Schlaegt das Archivieren fehl, bleibt der Rest am bisherigen Ort und kann
    beim naechsten Start erneut geprueft werden. Nie einen echten Slot anfassen.
    """
    if not os.path.isfile(pfad) or not pfad.endswith(ENDUNG_TMP):
        return
    try:
        import spielstand_archiv
        spielstand_archiv.archiviere(pfad, "abgebrochen", "Fehlgeschlagener Speicherversuch")
    except OSError:
        pass


# ---------------------------------------------------------------- Schreiben

def speichere(daten: dict, pfad: str) -> tuple:
    """Schreibt ``daten`` atomar und geprueft nach ``pfad``.

    Ablauf: nach ``<pfad>.tmp`` schreiben (flush + os.fsync), zuruecklesen und vergleichen,
    dann mit ``os.replace`` auf den Endpfad umsetzen, den Endpfad nochmals zuruecklesen.
    Gibt (Wahrheitswert, Meldung) zurueck und laesst bei jedem Fehler die alte Datei stehen.
    """
    if not isinstance(daten, dict):
        return False, "Die Daten muessen ein dict (Woerterbuch) sein."

    text, fehler = _serialisiere(daten)
    if text is None:
        return False, fehler

    tmp = pfad + ENDUNG_TMP

    # 1. Zwischendatei schreiben und auf den Datentraeger zwingen
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        _entferne_quiet(tmp)
        return False, f"Zwischendatei nicht schreibbar ({type(e).__name__}): {e}"

    # 2. Zuruecklesen und vergleichen - kein ungepruefter Schreibvorgang
    zurueck, fehler2 = _lies_json(tmp)
    if zurueck is None:
        _entferne_quiet(tmp)
        return False, f"Zwischendatei nicht lesbar: {fehler2}"
    if zurueck != daten:
        _entferne_quiet(tmp)
        return False, "Zwischendatei stimmt nicht mit den Daten ueberein."

    # 3. Atomarer Umsprung auf den Endpfad
    try:
        os.replace(tmp, pfad)
    except OSError as e:
        _entferne_quiet(tmp)
        return False, f"Ersetzen fehlgeschlagen ({type(e).__name__}): {e}"

    # 4. Endpfad nochmals zuruecklesen
    endgueltig, fehler3 = _lies_json(pfad)
    if endgueltig is None:
        return False, f"Datei nach dem Ersetzen nicht lesbar: {fehler3}"
    if endgueltig != daten:
        return False, "Datei stimmt nach dem Ersetzen nicht mit den Daten ueberein."

    return True, f"Gespeichert: {os.path.basename(pfad)} ({len(text)} Zeichen)"


# ---------------------------------------------------------------- Lesen

def lade(pfad: str) -> tuple:
    """Liest und parst eine Datei. Wirft NIE.

    Gibt (daten, "in Ordnung") zurueck, sonst (None, Grund). Eine fehlende oder beschaedigte
    Datei wird ehrlich gemeldet - die Anwendung kann entscheiden, ob sie eine Sicherung nutzt.
    """
    try:
        if not os.path.exists(pfad):
            return None, f"Datei fehlt: {pfad}"
        text, fehler = _lies_text(pfad)
        if text is None:
            return None, fehler
        return json.loads(text), "in Ordnung"
    except Exception as e:
        return None, f"Laden fehlgeschlagen ({type(e).__name__}): {e}"


# ---------------------------------------------------------------- Sicherung

def sichere_kopie(pfad: str) -> tuple:
    """Legt eine Sicherung ``<pfad>.bak`` an - VOR dem Ueberschreiben.

    Gibt (Wahrheitswert, Meldung) zurueck. Ohne vorhandene Datei gibt es nichts zu sichern.
    Die Sicherung wird durch Zuruecklesen geprueft.
    """
    if not os.path.exists(pfad):
        return False, "Keine Datei zum Sichern vorhanden."
    bak = pfad + ENDUNG_BAK
    try:
        with open(pfad, "rb") as q:
            inhalt = q.read()
        with open(bak, "wb") as z:
            z.write(inhalt)
            z.flush()
            os.fsync(z.fileno())
        with open(bak, "rb") as q:
            zurueck = q.read()
    except Exception as e:
        _entferne_quiet(bak)
        return False, f"Sicherung fehlgeschlagen ({type(e).__name__}): {e}"
    if zurueck != inhalt:
        _entferne_quiet(bak)
        return False, "Sicherung stimmt nicht mit der Datei ueberein."
    return True, f"Sicherung angelegt: {os.path.basename(bak)} ({len(inhalt)} Byte)"


def wiederherstellen(pfad: str) -> tuple:
    """Stellt ``pfad`` aus der Sicherung ``<pfad>.bak`` wieder her.

    Schreibt zuerst eine gepruefte Zwischendatei und setzt sie atomar um, damit auch die
    Wiederherstellung nie eine halbe Datei hinterlaesst. Gibt (Wahrheitswert, Meldung) zurueck.
    """
    bak = pfad + ENDUNG_BAK
    if not os.path.exists(bak):
        return False, "Keine Sicherung vorhanden."
    tmp = pfad + ENDUNG_TMP
    try:
        with open(bak, "rb") as q:
            inhalt = q.read()
        with open(tmp, "wb") as z:
            z.write(inhalt)
            z.flush()
            os.fsync(z.fileno())
        with open(tmp, "rb") as q:
            zurueck = q.read()
        if zurueck != inhalt:
            _entferne_quiet(tmp)
            return False, "Wiederherstellung nicht ueberpruefbar."
        os.replace(tmp, pfad)
    except Exception as e:
        _entferne_quiet(tmp)
        return False, f"Wiederherstellung fehlgeschlagen ({type(e).__name__}): {e}"
    daten, fehler = _lies_json(pfad)
    if daten is None:
        return False, f"Wiederhergestellte Datei nicht lesbar: {fehler}"
    return True, f"Wiederhergestellt aus {os.path.basename(bak)}."


# ---------------------------------------------------------------- Pruefen

def pruefe_datei(pfad: str) -> dict:
    """Prueft eine Datei ohne sie zu veraendern.

    Rueckgabe: {'existiert', 'groesse', 'lesbar', 'json_ok', 'stand'}.
    'stand' ist eine lesbare Zustandszeile (deutsche Kurzbewertung; bei vorhandener Datei
    mit dem Zeitpunkt der letzten Aenderung). Es wird NIE geworfen.
    """
    ergebnis = {"existiert": False, "groesse": 0, "lesbar": False, "json_ok": False,
                "stand": "Datei fehlt"}
    if not os.path.exists(pfad):
        return ergebnis
    ergebnis["existiert"] = True
    try:
        ergebnis["groesse"] = os.path.getsize(pfad)
    except OSError:
        ergebnis["groesse"] = 0

    text, fehler = _lies_text(pfad)
    if text is None:
        ergebnis["stand"] = f"Datei nicht lesbar: {fehler}"
        return ergebnis
    ergebnis["lesbar"] = True

    try:
        json.loads(text)
        ergebnis["json_ok"] = True
    except ValueError:
        ergebnis["json_ok"] = False

    try:
        zeit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(pfad)))
    except OSError:
        zeit = "unbekannt"

    if ergebnis["json_ok"]:
        ergebnis["stand"] = f"in Ordnung (Stand {zeit})"
    else:
        ergebnis["stand"] = f"JSON beschaedigt (Stand {zeit})"
    return ergebnis


# ---------------------------------------------------------------- Aufraeumen

def aufraeumen(pfad: str) -> list:
    """Archiviert liegengebliebene Zwischendateien zum Zielpfad und meldet sie.

    Archiviert werden nur Dateien, die mit dem Namen der Zieldatei beginnen und auf ``.tmp``
    enden (z. B. ``savegame.json.tmp`` aus einem abgebrochenen Lauf). Die Zieldatei selbst
    und die Sicherung ``.bak`` bleiben unberuehrt. Rueckgabe: Liste der archivierten Ursprungsnamen.
    """
    entfernt: list = []
    ordner = os.path.dirname(os.path.abspath(pfad))
    basis = os.path.basename(pfad)
    try:
        namen = os.listdir(ordner)
    except OSError:
        return entfernt
    for name in namen:
        if name.startswith(basis + ".") and name.endswith(ENDUNG_TMP):
            voll = os.path.join(ordner, name)
            try:
                import spielstand_archiv
                ok, _ = spielstand_archiv.archiviere(
                    voll, "abgebrochen", "Zwischendatei nach abgebrochenem Speichervorgang")
                if ok:
                    entfernt.append(voll)
            except OSError:
                pass
    return entfernt


# ---------------------------------------------------------------- Ehrliche Luecken

def offene_luecken() -> dict:
    """Was dieses Modul NICHT kann - ehrlich benannt, statt es zu verschweigen.

    Rueckgabe: dict Schluessel -> Begruendung. Diese Punkte sind keine Fehler, sondern die
    Grenzen des Verfahrens; sie gehoeren in den Bericht, damit ein gruener Lauf nicht
    faelschlich 'alles perfekt' bedeutet.
    """
    return {
        "verzeichnis_sync": (
            "Nach os.replace wird der Verzeichniseintrag nicht gesondert synchronisiert "
            "(kein fsync auf den Ordner). Auf den meisten Systemen genuegt der Datei-fsync; "
            "auf wenigen Dateisystemen bleibt ein kleines Restrisiko beim Stromausfall."),
        "netzlaufwerk": (
            "os.replace ist nur INNERHALB eines Dateisystems atomar. Liegen .tmp und Ziel auf "
            "verschiedenen Laufwerken, schlaegt das Ersetzen ehrlich fehl statt still zu kopieren."),
        "sperren": (
            "Es gibt keine Dateisperre gegen zwei gleichzeitige Schreiber. Das letzte os.replace "
            "gewinnt; fuer ein Einzelspieler-Spiel ist das ausreichend, fuer Mehrfachzugriff nicht."),
        "pruefsumme": (
            "Die Rueckpruefung vergleicht die GEPARSTEN Daten, nicht eine Pruefsumme der Rohbytes. "
            "Ein inhaltlich gleicher, aber anders formatierter Text gilt damit als gueltig."),
        "verschluesselung": (
            "Die Datei wird im Klartext geschrieben. Ein Passwortschutz der Spielstandsdatei "
            "gehoert zum Passworttor, nicht hierher."),
    }


if __name__ == "__main__":                                   # kleine Selbstprobe
    import sys
    if len(sys.argv) > 1:
        print(f"Pruefung {sys.argv[1]}: {pruefe_datei(sys.argv[1])}")
    else:
        print("speichern: robustes Speichern (W8). Benutzung ueber speichere/lade/...")
        print(f"Offene Luecken: {len(offene_luecken())}")
