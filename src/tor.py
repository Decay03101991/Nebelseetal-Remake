"""
Passworttor fuer das Nebelseetal-Remake (Schritt 8 in `docs/WEG_ZUR_EXE.md`).

Zweck: Das Spiel soll nur mit dem von **Daniel selbst gesetzten** Passwort starten. Das Passwort
kommt **niemals** in einen Chat und wird **nirgends im Klartext** gespeichert — abgelegt wird nur
ein gesalzener Pruefwert (PBKDF2-HMAC-SHA256).

  * Erststart: Passwort zweimal eingeben -> Pruefwert nach ``~/.nebelseetal/tor.json``.
  * Jeder weitere Start: Passwort eingeben, Pruefwert vergleichen.
  * Nach je drei Fehlversuchen waechst die Wartezeit (5 s, 15 s, 60 s) — VORSCHLAG, in dieser Datei
    aenderbar.
  * Aendern: altes Passwort noetig. Zuruecksetzen: Tor-Datei loeschen (der Spielstand bleibt).

Ehrliche Grenze: Ein Tor in einer lokalen EXE haelt Gelegenheitsspieler auf. Wer die Dateien lesen
kann, kann sie auch veraendern — ohne Server ist mehr nicht moeglich, und einen Server will dieses
Spiel ausdruecklich nicht.

Dieses Modul zeichnet nichts (keine tkinter-Abhaengigkeit) und ist damit fensterlos pruefbar.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Any, Dict, Optional, Tuple

# Ablageort ausserhalb des Projektordners: so ueberlebt das Tor jeden Neubau der EXE.
ORDNER = os.path.join(os.path.expanduser("~"), ".nebelseetal")
STANDARD_PFAD = os.path.join(ORDNER, "tor.json")

# Pruefwert-Einstellungen. PBKDF2-HMAC-SHA256 mit Zufallssalz und vielen Runden: das Passwort
# selbst steht nirgends, und aus dem Pruefwert laesst sich das Passwort nicht zurueckrechnen.
RUNDEN = 200_000
SALZ_BYTES = 16
MIN_LAENGE = 4            # VORSCHLAG: das Handbuch kennt kein Passwort, es ist unsere eigene Wahl
WARTEZEITEN = (0, 5, 15, 60)   # Stufe 0..3: keine / 5 s / 15 s / 60 s (Wartezeit nach je 3 Fehlversuchen)

VERSION = 1


# --------------------------------------------------------------------------
# Hilfsgriffe
# --------------------------------------------------------------------------

def _pruefwert(passwort: str, salz_hex: str, runden: int) -> str:
    """Der gesalzene Pruefwert zu einem Passwort (Hex)."""
    return hashlib.pbkdf2_hmac(
        "sha256", passwort.encode("utf-8"), bytes.fromhex(salz_hex), int(runden)).hex()


def _lade(pfad: str) -> Optional[Dict[str, Any]]:
    """Die Tor-Datei lesen — None, wenn es keine (oder eine kaputte) gibt."""
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(daten, dict) or "pruefwert" not in daten or "salz" not in daten:
        return None
    return daten


def _schreibe(pfad: str, daten: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=2, ensure_ascii=False)
        return True, f"Tor gespeichert: {pfad}"
    except OSError as fehler:
        return False, f"Tor konnte nicht gespeichert werden: {fehler}"


# --------------------------------------------------------------------------
# Zustand
# --------------------------------------------------------------------------

def hat_passwort(pfad: str = STANDARD_PFAD) -> bool:
    """Ist ein Passwort gesetzt? (Erststart = nein)."""
    return _lade(pfad) is not None


def tor_pfad(pfad: str = STANDARD_PFAD) -> str:
    """Der Ablageort — fuer den Hinweis im Tor-Fenster."""
    return pfad


def fehlversuche(pfad: str = STANDARD_PFAD) -> int:
    daten = _lade(pfad)
    return int(daten.get("fehlversuche", 0)) if daten else 0


def wartezeit_sekunden(anzahl_fehlversuche: int) -> int:
    """Wie lange nach dieser Anzahl Fehlversuche gewartet wird (0 = keine Wartezeit).

    Die ersten beiden Fehlversuche sind frei (Tippfehler sollen nicht bestrafen); danach waechst
    die Wartezeit nach JEDEN WEITEREN DREI Fehlversuchen: 5 s, dann 15 s, dann 60 s.
    """
    i = max(0, int(anzahl_fehlversuche))
    if i < 3:
        return 0
    stufe = (i - 3) // 3 + 1          # 3,4,5 -> 1 · 6,7,8 -> 2 · ab 9 -> 3
    return WARTEZEITEN[stufe] if stufe < len(WARTEZEITEN) else WARTEZEITEN[-1]


def gesperrt_bis(pfad: str = STANDARD_PFAD) -> float:
    """Zeitpunkt, bis zu dem nach zu vielen Fehlversuchen gewartet wird (0 = frei)."""
    daten = _lade(pfad)
    return float(daten.get("gesperrt_bis", 0.0)) if daten else 0.0


def restwartezeit(pfad: str = STANDARD_PFAD, jetzt: Optional[float] = None) -> float:
    """Verbleibende Wartezeit in Sekunden (0, wenn frei)."""
    jetzt = time.time() if jetzt is None else jetzt
    return max(0.0, gesperrt_bis(pfad) - jetzt)


# --------------------------------------------------------------------------
# Passwort setzen, pruefen, aendern, zuruecksetzen
# --------------------------------------------------------------------------

def passwort_pruefen_regeln(passwort: str, wiederholung: str) -> Tuple[bool, str]:
    """Die Regeln fuer ein neues Passwort — (ok, Meldung)."""
    if not passwort:
        return False, "Das Passwort darf nicht leer sein."
    if len(passwort) < MIN_LAENGE:
        return False, f"Das Passwort muss mindestens {MIN_LAENGE} Zeichen haben."
    if passwort != wiederholung:
        return False, "Die beiden Eingaben stimmen nicht überein."
    return True, "Passwort angenommen."


def setze_passwort(passwort: str, wiederholung: str, pfad: str = STANDARD_PFAD) -> Tuple[bool, str]:
    """Setzt das Passwort beim ersten Start (oder nach einem Zuruecksetzen).

    Gespeichert wird nur Salz, Rundenzahl und Pruefwert — niemals das Passwort selbst.
    """
    ok, meldung = passwort_pruefen_regeln(passwort, wiederholung)
    if not ok:
        return False, meldung
    salz = secrets.token_hex(SALZ_BYTES)
    daten = {
        "version": VERSION,
        "verfahren": f"PBKDF2-HMAC-SHA256, {RUNDEN} Runden, Salz {SALZ_BYTES} Byte",
        "salz": salz,
        "runden": RUNDEN,
        "pruefwert": _pruefwert(passwort, salz, RUNDEN),
        "gesetzt": time.strftime("%d.%m.%Y %H:%M"),
        "fehlversuche": 0,
        "gesperrt_bis": 0.0,
        "hinweis": ("Ohne diese Datei verlangt das Spiel beim naechsten Start ein NEUES Passwort. "
                    "Der Spielstand bleibt dabei erhalten."),
    }
    return _schreibe(pfad, daten)


def pruefe_passwort(passwort: str, pfad: str = STANDARD_PFAD,
                    jetzt: Optional[float] = None) -> Tuple[bool, str]:
    """Prueft das Passwort und fuehrt die Fehlversuche mit (Wartezeit nach je drei Fehlern).

    Rueckgabe: (Zugang ja/nein, Meldung). Bei Erfolg werden die Fehlversuche zurueckgesetzt.
    """
    jetzt = time.time() if jetzt is None else jetzt
    daten = _lade(pfad)
    if daten is None:
        return False, "Es ist kein Passwort gesetzt — bitte zuerst eines festlegen."

    rest = max(0.0, float(daten.get("gesperrt_bis", 0.0)) - jetzt)
    if rest > 0:
        return False, f"Zu viele Fehlversuche. Bitte {int(rest) + 1} Sekunden warten."

    salz = daten["salz"]
    runden = int(daten.get("runden", RUNDEN))
    kandidat = _pruefwert(passwort, salz, runden)
    if hmac.compare_digest(kandidat, str(daten["pruefwert"])):
        daten["fehlversuche"] = 0
        daten["gesperrt_bis"] = 0.0
        _schreibe(pfad, daten)
        return True, "Zugang gewaehrt."

    versuche = int(daten.get("fehlversuche", 0)) + 1
    daten["fehlversuche"] = versuche
    wartezeit = wartezeit_sekunden(versuche)
    if wartezeit:
        daten["gesperrt_bis"] = jetzt + wartezeit
    _schreibe(pfad, daten)
    if wartezeit:
        return False, f"Falsches Passwort ({versuche} Fehlversuche). {wartezeit} Sekunden warten."
    return False, f"Falsches Passwort ({versuche} Fehlversuche)."


def aendere_passwort(alt: str, neu: str, wiederholung: str,
                     pfad: str = STANDARD_PFAD) -> Tuple[bool, str]:
    """Aendert das Passwort — nur mit dem alten Passwort."""
    if not hat_passwort(pfad):
        return False, "Es ist kein Passwort gesetzt — bitte zuerst eines festlegen."
    ok, meldung = pruefe_passwort(alt, pfad)
    if not ok:
        return False, f"Das alte Passwort stimmt nicht ({meldung})"
    return setze_passwort(neu, wiederholung, pfad)


def zuruecksetzen(pfad: str = STANDARD_PFAD) -> Tuple[bool, str]:
    """Loescht die Tor-Datei. Das Spiel verlangt dann beim naechsten Start ein neues Passwort.

    Der Spielstand liegt in einer anderen Datei und bleibt erhalten.
    """
    if not os.path.exists(pfad):
        return False, "Es gibt keine Tor-Datei zum Zuruecksetzen."
    try:
        os.remove(pfad)
    except OSError as fehler:
        return False, f"Tor-Datei liess sich nicht loeschen: {fehler}"
    return True, ("Tor zurueckgesetzt — beim naechsten Start wird ein neues Passwort festgelegt. "
                  "Der Spielstand bleibt erhalten.")


def uebersicht(pfad: str = STANDARD_PFAD) -> Dict[str, Any]:
    """Kurzbericht fuer Anzeige und Pruefung (ohne jeden Hinweis auf das Passwort)."""
    daten = _lade(pfad) or {}
    return {
        "gesetzt": hat_passwort(pfad),
        "pfad": pfad,
        "verfahren": daten.get("verfahren"),
        "gesetzt_am": daten.get("gesetzt"),
        "fehlversuche": int(daten.get("fehlversuche", 0)),
        "restwartezeit": round(restwartezeit(pfad), 1),
    }
