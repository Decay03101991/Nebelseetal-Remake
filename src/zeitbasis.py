"""Eine einzige Trennung von Rechnerzeit, Laufzeit und Spielzeit.

Die monotone Uhr liefert NUR verstrichene Echtzeit waehrend eines laufenden Spiels.
UTC- und lokale ISO-Zeiten dienen NUR als Beleg und Anzeige, nie als Rechenbasis
fuer Wirtschaft oder Kampf. Spielsekunden werden ausschliesslich in GameState.tick
fortgeschrieben. Schliessen/Laden bedeutet Pause (kein heimlicher Offline-Tick).

GPT-Z01, ChatGPT externer Entwicklungsagent (28.10.2026).
"""
from __future__ import annotations

import math
import time
from datetime import datetime, timezone


def zeitmarke(jetzt: datetime | None = None) -> dict[str, str]:
    """Den einen Augenblick als UTC und als lokale Rechnerzeit beschriften."""
    utc = jetzt or datetime.now(timezone.utc)
    if utc.tzinfo is None or utc.utcoffset() is None:
        raise ValueError("Zeitmarke braucht einen zeitzonenbewussten Zeitpunkt")
    utc = utc.astimezone(timezone.utc)
    lokal = utc.astimezone()
    return {
        "zeit_utc": utc.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "zeit_lokal": lokal.isoformat(timespec="milliseconds"),
    }


class Laufzeituhr:
    """Misst vergangene echte Sekunden ohne Spruenge durch Windows-Uhrkorrekturen.

    Die Monotonie garantiert der Betriebssystemdienst. Ein defekter Test- oder
    Uhrenlieferant wird defensiv abgefangen. Kein positives Zeitlimit: eine
    laengere, echte Sitzung darf keine Produktion verlieren.
    """
    def __init__(self, lieferant=None):
        self._lieferant = lieferant or time.monotonic
        self._letzter = None
        self.neu_ankern()

    def neu_ankern(self) -> None:
        jetzt = float(self._lieferant())
        if not math.isfinite(jetzt):
            raise ValueError("Uhr lieferte keinen endlichen Zeitwert")
        self._letzter = jetzt

    def vergangen(self) -> float:
        jetzt = float(self._lieferant())
        if not math.isfinite(jetzt):
            raise ValueError("Uhr lieferte keinen endlichen Zeitwert")
        alt = self._letzter
        self._letzter = jetzt
        if alt is None or jetzt <= alt:
            return 0.0
        return jetzt - alt


class NachrichtenMitZeit(list):
    """Jede NEUE Nachricht einmal stempeln; Legacy-Nachrichten bewahren.

    Das dict wird kopiert: keine fremde Auftragsstruktur wird dabei mutiert.
    Die Liste bleibt JSON-serialisierbar und erhaelt ihre Reihenfolge.
    """
    def __init__(self, werte=(), spieluhr=None):
        # Die Zeitbasis ist zur Laufzeit gebunden und wird niemals serialisiert.
        # Geladene Altnachrichten behalten ihren urspruenglichen Inhalt.
        super().__init__(werte)
        self._spieluhr = spieluhr

    def append(self, eintrag):
        if isinstance(eintrag, dict):
            ergaenzung = {}
            if "zeit_utc" not in eintrag:
                ergaenzung.update(zeitmarke())
            if "spielzeit_sekunden" not in eintrag and self._spieluhr is not None:
                wert = float(self._spieluhr())
                if math.isfinite(wert) and wert >= 0:
                    ergaenzung["spielzeit_sekunden"] = wert
            if ergaenzung:
                eintrag = {**eintrag, **ergaenzung}
        super().append(eintrag)

    def extend(self, eintraege):
        for eintrag in eintraege:
            self.append(eintrag)


def zeitstempel_text(eintrag: dict) -> str:
    """Fuer die Nachrichtenansicht, auch ohne Zeitstempel alter Saves."""
    lokal = eintrag.get("zeit_lokal") or eintrag.get("zeit_utc")
    return f"[{lokal}] " if lokal else ""


def offene_luecken() -> dict:
    """Was die Zeitbasis absichtlich NICHT tut (kein Offline-Fortschritt, keine Systemzeit-Spruenge)."""
    return {
        "offline": "Kein Offline-Fortschritt; das Spiel ist beim Schliessen pausiert.",
        "systemzeit": "Rechnerzeit ist manipulierbar; Zeitstempel sind kein Sicherheitsnachweis.",
        "nutzerevents": "Alte Nachrichten haben keinen rueckwirkend erfindbaren Zeitstempel.",
        "kalender": "Speicherformat nutzt UTC+Offset, nicht lokale Zeit zur Fristenberechnung.",
    }
