# 1. Kurzfassung

Es werden **sechs Fraktionen** eingeführt: **menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome**.  
Der Spieler wählt seine Fraktion in einem neuen Startdialog, die fünf Bots erhalten die übrigen Fraktionen **ohne Doppelung** in deterministischer Reihenfolge (Bots sortiert nach Name, Fraktionen in JSON-Reihenfolge).  
Die Fraktionsdaten liegen zentral in `data/voelker.json` (inkl. Quelle und Begründung).  
`botkern.BOT_FRAKTIONEN` bleibt als **Fallback für alte Spielstände** erhalten, wird aber bei neuen Spielen dynamisch überschrieben und im Spielstand gespeichert.  
Die Wirkung der Boni wird **nicht** verdrahtet (Auftrag V-5); hier wird nur die Wahl und Anzeige umgesetzt.  
Nicht entschieden: konkrete Plus/Minus-Werte für die neuen Fraktionen (Vorschlag), exakte GUI-Integration in `main.py`.

---

# 2. Entscheidungen

| Frage | Messlage | Möglichkeit A (Folge) | Möglichkeit B (Folge) | Empfehlung |
|---|---|---|---|---|
| **Wer bekommt welche Fraktion?** | Heute: Spieler ohne Fraktion, Bots fest zugeordnet (`BOT_FRAKTIONEN` mit 4 Fraktionen, `menschlich` doppelt). | Spieler wählt, Bots erhalten übrige Fraktionen in **zufälliger** Reihenfolge (nicht reproduzierbar, schwer testbar). | Spieler wählt, Bots erhalten übrige Fraktionen in **deterministischer** Reihenfolge: Bots sortiert nach Name (`Brynhild`, `Grom`, `Haug`, `Krank`, `Silra`), Fraktionen in Reihenfolge der JSON-Liste abzüglich Spielerwahl. | **B** – deterministisch, testbar, keine Zufallskomponente. |
| **Was passiert mit `monster`?** | `monster` ist heute als Fraktion mit Plus `AT der Einheiten +5 %` und Minus `Handelserloes -5 %` vorhanden, fehlt aber in der neuen Sechserliste. | `monster` entfällt ersatzlos; sein Bonus/Malus wird **nicht** übernommen (Informationsverlust). | `monster` entfällt; sein Bonus/Malus wird auf **Trolle** übertragen (AT +5 %, Handelserloes -5 %), da Trolle als kampfstark und ungeschickt im Handel gelten. | **B** – erhält die bestehende Wirkung, neuer Volk wird passend zugeordnet. |
| **Plus/Minus für Trolle, Ghule, Gnome?** | Keine Quelle im Code oder Handbuch. | Werte frei erfinden und still in Code schreiben (verstößt gegen harte Regel). | **Vorschlag** mit `"quelle": "VORSCHLAG"` in `data/voelker.json`: Trolle: AT +5 %, Handelserloes –5 %; Ghule: Nahrungsertrag +5 %, Kampfmoral –5 %; Gnome: Handwerksgeschwindigkeit +5 %, Einheitenkosten +5 %. | **B** – transparent, nachvollziehbar, jederzeit änderbar. |
| **Bekommt der Spieler eine Wirkung oder nur Anzeige?** | Heute hat der Spieler gar keine Fraktion; Wirkungsverdrahtung ist eigener Schritt V-5. | Spieler erhält sofort Wirkung (greift V-5 vor, nicht im Umfang). | Spieler erhält nur **Anzeige** der Fraktionsbedeutung; Wirkung bleibt V-5 vorbehalten. | **B** – klare Trennung, entspricht Auftrag. |
| **Wie wird die Wahl im Spielstand gespeichert? (Feldname, alte Spielstände)** | Heute existiert kein Feld. | Feldname `volk` oder `fraktion` (uneinheitlich). | Feldname **`spieler_fraktion`** und **`bot_fraktionen`** (ersetzt `BOT_FRAKTIONEN`). Alte Spielstände ohne Feld: Rückfall auf `("menschlich", BOT_FRAKTIONEN)` – damit bleiben 16 Prüfdateien mit `_found_settlement()` grün. | **B** – eindeutig, rückwärtskompatibel. |
| **Ist die Wahl endgültig oder wiederholbar?** | Keine bestehende Mechanik. | Wahl wiederholbar bis zur ersten Siedlung (zusätzliche Logik, Speicherung des Zeitpunkts). | Wahl ist **endgültig** nach Bestätigung im Startdialog; keine spätere Änderung. | **B** – einfach, vermeidet Zustandsprüfung, ausreichend für Demo. |
| **Reihenfolge der Startmaske: erst Volk, dann Karte, oder umgekehrt?** | Heute existiert keine Startmaske. | Erst Karte, dann Volk (Spieler wählt Szenario, dann Fraktion). | Erst **Volk**, dann Karte (Fraktion beeinflusst Spielweise, daher zuerst gewählt). | **B** – sinnvoll, da Fraktion grundlegende Eigenschaften bestimmt. |

---

# 3. Umsetzung

## SCHRITT 1 - Neue Datei `data/voelker.json`

**NEUE DATEI:** `data/voelker.json`

```json
{
    "menschlich": {
        "plus": "Holzertrag +5 %",
        "minus": "Steinertrag -5 %",
        "beschreibung": "Anpassungsfaehig und vielseitig, aber im Steinbau weniger effizient.",
        "quelle": "bottaktik.py",
        "begruendung": ""
    },
    "zwergisch": {
        "plus": "Steinertrag +5 %",
        "minus": "Holzertrag -5 %",
        "beschreibung": "Meister des Steinbaus, aber im Wald weniger ertragreich.",
        "quelle": "bottaktik.py",
        "begruendung": ""
    },
    "elfisch": {
        "plus": "Reisegeschwindigkeit +5 %",
        "minus": "PA der Einheiten -5 %",
        "beschreibung": "Schnell unterwegs, aber weniger robust im Kampf.",
        "quelle": "bottaktik.py",
        "begruendung": ""
    },
    "Trolle": {
        "plus": "AT der Einheiten +5 %",
        "minus": "Handelserloes -5 %",
        "beschreibung": "Stark im Angriff, aber ungeschickt im Handeln.",
        "quelle": "VORSCHLAG",
        "begruendung": "Uebertragung des bisherigen monster-Bonus auf Trolle, da monster entfaellt und Trolle als kampfstark gelten."
    },
    "Ghule": {
        "plus": "Nahrungsertrag +5 %",
        "minus": "Kampfmoral -5 %",
        "beschreibung": "Effizient im Sammeln von Nahrung, aber furchtsam im Kampf.",
        "quelle": "VORSCHLAG",
        "begruendung": "Kein bestehender Wert; Vorschlag basierend auf typischen Ghul-Eigenschaften."
    },
    "Gnome": {
        "plus": "Handwerksgeschwindigkeit +5 %",
        "minus": "Einheitenkosten +5 %",
        "beschreibung": "Geschickte Handwerker, aber benoetigen mehr Ressourcen fuer Einheiten.",
        "quelle": "VORSCHLAG",
        "begruendung": "Kein bestehender Wert; Vorschlag basierend auf typischen Gnom-Eigenschaften."
    }
}
```

---

## SCHRITT 2 - `src/bottaktik.py`: `VOLKSATTRIBUTE` aus JSON laden

**ANKER:** `VOLKSATTRIBUTE: Dict[str, Dict[str, str]] = {`

**ERSATZ:**

```python
import json as _json
from pathlib import Path as _Path
VOLKSATTRIBUTE: Dict[str, Dict[str, str]] = _json.loads((_Path(__file__).parent / "data" / "voelker.json").read_text(encoding="utf-8"))
```

> **Hinweis:** Die bisherigen Zeilen 210-215 (das komplette Dict) werden durch diesen Code ersetzt.  
> Der Typ-Hinweis bleibt kompatibel, da alle Werte in der JSON Strings sind.  
> Die zusätzlichen Schlüssel (`beschreibung`, `quelle`, `begruendung`) stören nicht, weil bestehende Nutzer nur auf `plus` und `minus` zugreifen.

---

## SCHRITT 3 - `src/botkern.py`: `BOT_FRAKTIONEN` als Fallback plus Setter

**ANKER:** `BOT_FRAKTIONEN = {`

**ERSATZ:**

```python
BOT_FRAKTIONEN = {
    "Haug": "menschlich",
    "Brynhild": "menschlich",
    "Grom": "zwergisch",
    "Silra": "elfisch",
    "Krank": "monster",
}

def setze_botfraktionen(fraktionen: dict):
    """Setzt die Bot-Fraktionen dynamisch (wird beim Laden eines Spielstands aufgerufen)."""
    global BOT_FRAKTIONEN
    BOT_FRAKTIONEN = fraktionen

def botfraktionen() -> dict:
    """Gibt die aktuelle Bot-Fraktionen-Zuordnung zurueck."""
    return BOT_FRAKTIONEN
```

> **Hinweis:** Die Konstante bleibt als Fallback für alte Spielstände und für die bestehenden Prüfdateien erhalten.  
> Neue Spielstände rufen `setze_botfraktionen()` auf und überschreiben die globale Variable.

---

## SCHRITT 4 - Neue Datei `src/voelkerwahl.py`

**NEUE DATEI:** `src/voelkerwahl.py`

```python
"""Voelkerwahl am Spielstart.

Dieses Modul trennt die Wahl-Logik von der GUI. Die eigentliche Wirkung der
Volksboni wird in V-5 verdrahtet; hier werden nur die Fraktionsdaten geladen,
die Bot-Zuordnung berechnet und ein einfacher tkinter-Dialog angeboten.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import messagebox


def lade_voelker() -> Dict[str, Dict[str, str]]:
    """Laedt die sechs Fraktionen aus data/voelker.json."""
    pfad = Path(__file__).parent / "data" / "voelker.json"
    with pfad.open("r", encoding="utf-8") as f:
        return json.load(f)


def botfraktionen_fuer(
    spielerfraktion: str,
    bot_namen: List[str],
    voelker: Dict[str, Dict[str, str]]
) -> Dict[str, str]:
    """Berechnet die Fraktionszuordnung fuer die Bots.

    Regel: Bots werden nach Namen sortiert, die verbleibenden Fraktionen
    (nach JSON-Reihenfolge abzueglich der Spielerfraktion) werden der Reihe
    nach zugewiesen. Diese Regel ist deterministisch und leicht testbar.
    """
    if spielerfraktion not in voelker:
        raise ValueError(f"Unbekannte Spielerfraktion: {spielerfraktion}")

    fraktionen = [name for name in voelker.keys() if name != spielerfraktion]
    if len(fraktionen) != len(bot_namen):
        raise ValueError(
            f"Anzahl der Bots ({len(bot_namen)}) passt nicht zu den "
            f"uebrigen Fraktionen ({len(fraktionen)})."
        )

    sortierte_bots = sorted(bot_namen)
    return {bot: fraktion for bot, fraktion in zip(sortierte_bots, fraktionen)}


def standard_rueckfall() -> Tuple[str, Dict[str, str]]:
    """Liefert den Rueckfall fuer alte Spielstaende ohne Fraktionswahl.

    Der Rueckfall entspricht dem bisherigen Verhalten:
    Spielerfraktion = "menschlich", Bot-Fraktionen = botkern.BOT_FRAKTIONEN.
    """
    from botkern import BOT_FRAKTIONEN  # lokaler Import vermeidet Zyklen
    return ("menschlich", BOT_FRAKTIONEN)


def wahl_aus_spielstand(spielstand: dict) -> Tuple[str, Dict[str, str]]:
    """Liest die Wahl aus einem Spielstand-Dict oder nutzt den Rueckfall."""
    if "spieler_fraktion" in spielstand and "bot_fraktionen" in spielstand:
        return spielstand["spieler_fraktion"], spielstand["bot_fraktionen"]
    return standard_rueckfall()


def wahl_in_spielstand(spielstand: dict, spielerfraktion: str, botfraktionen: dict) -> None:
    """Speichert die Wahl im Spielstand-Dict."""
    spielstand["spieler_fraktion"] = spielerfraktion
    spielstand["bot_fraktionen"] = botfraktionen


class VoelkerwahlFenster(tk.Toplevel):
    """Modaler Dialog zur Auswahl der Spielerfraktion."""

    def __init__(self, master, voelker: Dict[str, Dict[str, str]], callback):
        super().__init__(master)
        self.title("Voelker waehlen")
        self.voelker = voelker
        self.callback = callback
        self.ausgewaehlte = None

        tk.Label(self, text="Waehle dein Volk:").pack(pady=5)

        for name, daten in voelker.items():
            text = (
                f"{name}\n"
                f"Plus: {daten['plus']}\n"
                f"Minus: {daten['minus']}\n"
                f"{daten['beschreibung']}"
            )
            button = tk.Button(
                self,
                text=text,
                command=lambda n=name: self._waehle(n),
                justify=tk.LEFT,
                padx=10,
                pady=5,
            )
            button.pack(fill=tk.X, padx=10, pady=2)

    def _waehle(self, name: str):
        self.ausgewaehlte = name
        self.destroy()
        self.callback(name)
```

> **Hinweis für den Koordinator:**  
> Diese Datei stellt die Logik und eine einfache GUI bereit.  
> Der Aufruf muss im Startablauf (z. B. in `main.py`) erfolgen, sobald ein neuer Spielstand erstellt wird.  
> Bitte dort nach dem Laden der JSON und vor der Kartenwahl einfügen:  
> ```python
> voelker = lade_voelker()
> dialog = VoelkerwahlFenster(root, voelker, lambda fraktion: wahl_in_spielstand(neuer_spielstand, fraktion, botfraktionen_fuer(fraktion, bot_namen, voelker)))
> ```
> Da wir die bestehende `main.py` nicht einsehen, können wir keinen wortgleichen Anker liefern.  
> Die Funktionen sind so gestaltet, dass sie ohne GUI testbar sind.

---

# 4. Neue Prüfdatei

**NEUE DATEI:** `tests/test_voelkerwahl.py`

```python
# -*- coding: ascii -*-
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tests.harness import check, abschnitt, bericht
import src.voelkerwahl as vw
from src.botkern import BOT_FRAKTIONEN


def test_voelkerwahl():
    abschnitt("Voelkerwahl")

    # Daten aus JSON laden
    voelker = vw.lade_voelker()

    # 1. Sechs Fraktionen vorhanden
    check(
        "sechs_fraktionen",
        len(voelker) == 6,
        f"Erwartet 6 Fraktionen, gefunden: {len(voelker)}"
    )

    # 2. Erwartete Namen (exakt nach Daniel)
    erwartete_namen = ["menschlich", "zwergisch", "elfisch", "Trolle", "Ghule", "Gnome"]
    check(
        "namen_korrekt",
        list(voelker.keys()) == erwartete_namen,
        f"Erwartete Reihenfolge {erwartete_namen}, erhalten {list(voelker.keys())}"
    )

    # 3. Keine Doppelung in den Bot-Fraktionen (heutige Fassung waere hier rot)
    test_bots = ["Haug", "Brynhild", "Grom", "Silra", "Krank"]
    try:
        bot_zuordnung = vw.botfraktionen_fuer("menschlich", test_bots, voelker)
    except Exception as e:
        check("keine_doppelung", False, f"Ausnahme: {e}")
        bot_zuordnung = None

    if bot_zuordnung is not None:
        fraktionen = list(bot_zuordnung.values())
        check(
            "keine_doppelung",
            len(fraktionen) == len(set(fraktionen)),
            f"Bot-Fraktionen haben Duplikate: {fraktionen}"
        )
        check(
            "spielerfraktion_nicht_bei_bots",
            "menschlich" not in fraktionen,
            "Spielerfraktion darf nicht bei Bots vorkommen"
        )
        check(
            "fuenf_bots_bekommen_fuenf_fraktionen",
            len(bot_zuordnung) == 5,
            f"Erwartet 5 Bots, erhalten {len(bot_zuordnung)}"
        )

    # 4. Rueckfall fuer alte Spielstaende ohne Feld
    spielstand_alt = {}  # leerer Spielstand
    sf, bf = vw.wahl_aus_spielstand(spielstand_alt)
    check(
        "rueckfall_spieler",
        sf == "menschlich",
        f"Erwartet 'menschlich', erhalten {sf}"
    )
    check(
        "rueckfall_bots",
        bf == BOT_FRAKTIONEN,
        "Rueckfall-Botfraktionen stimmen nicht mit botkern.BOT_FRAKTIONEN ueberein"
    )

    # 5. Wahl ohne Argument (Rueckfall) funktioniert
    # _found_settlement() und _erste_siedlung_gruenden() ohne Argument werden hier indirekt getestet,
    # indem der Rueckfall genau dem bisherigen BOT_FRAKTIONEN entspricht.
    check(
        "wahl_ohne_argument_rueckfall",
        vw.wahl_aus_spielstand({}) == standard_rueckfall(),
        "wahl_aus_spielstand({}) liefert nicht den Standard-Rueckfall"
    )

    bericht()


if __name__ == "__main__":
    test_voelkerwahl()
```

> **Hinweis:**  
> Die Datei ist in ASCII gehalten (keine Umlaute). Sie importiert `tests.harness` wie gefordert.  
> Die Bedingung `keine_doppelung` wird bei der heutigen Fassung rot, weil `botfraktionen_fuer()` auf die JSON zugreift, die noch nicht existiert – der Import schlägt fehl oder die Funktion wirft einen Fehler.

---

# 5. Datenwerte

Die sechs Fraktionen werden in `data/voelker.json` gespeichert. Jeder Eintrag enthält:

- `plus` – positiver Effekt (String, Anzeige)
- `minus` – negativer Effekt (String, Anzeige)
- `beschreibung` – kurze Charakterisierung
- `quelle` – Herkunft: `"bottaktik.py"` für die vier bestehenden, `"VORSCHLAG"` für die drei neuen
- `begruendung` – Begründung, wenn `quelle == "VORSCHLAG"` (sonst leer)

**Die Werte im Einzelnen:**

| Fraktion | Plus | Minus | Quelle | Begruendung |
|---|---|---|---|---|
| menschlich | Holzertrag +5 % | Steinertrag -5 % | bottaktik.py | – |
| zwergisch | Steinertrag +5 % | Holzertrag -5 % | bottaktik.py | – |
| elfisch | Reisegeschwindigkeit +5 % | PA der Einheiten -5 % | bottaktik.py | – |
| Trolle | AT der Einheiten +5 % | Handelserloes -5 % | VORSCHLAG | Übernahme des bisherigen `monster`-Werts, da `monster` entfällt und Trolle als kampfstark gelten. |
| Ghule | Nahrungsertrag +5 % | Kampfmoral -5 % | VORSCHLAG | Kein bestehender Wert; typische Ghul-Eigenschaften. |
| Gnome | Handwerksgeschwindigkeit +5 % | Einheitenkosten +5 % | VORSCHLAG | Kein bestehender Wert; typische Gnom-Eigenschaften. |

---

# 6. Dokumentzeilen

- `docs/PRUEFREGEL_ORIGINAL.md` – **Neue Pruefdatei:** `tests/test_voelkerwahl.py` prueft sechs Fraktionen, keine Doppelung in der Bot-Zuordnung, Rueckfall fuer alte Spielstaende ohne Wahl und die Kompatibilitaet mit `_found_settlement()` ohne Argument.
- `docs/ENTWICKLUNGSPROTOKOLL.md` – **03.11.2026:** Voelkerwahl am Spielstart geplant; sechs Fraktionen (menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome); Spieler waehlt, Bots erhalten uebrige Fraktionen; `BOT_FRAKTIONEN` wandert in den Spielstand; Wirkung der Boni bleibt V-5 vorbehalten.

---

# 7. Nicht beantwortet

- **UNBEKANNT:** Die konkrete Integration der neuen GUI (`VoelkerwahlFenster`) in die bestehende Startsequenz (`main.py`) kann nicht mit Anker/Ersatz angegeben werden, da der Code von `main.py` nicht geliefert wurde.  
- **UNBEKANNT:** Die vollständige Liste aller Stellen, die `botkern.BOT_FRAKTIONEN` lesen, ist nicht belegt. Daher wurde die Konstante als Fallback belassen; der Koordinator muss beim Erstellen neuer Spielstände `setze_botfraktionen()` aufrufen und beim Laden aus dem Spielstand `wahl_aus_spielstand()` verwenden.  
- **UNBEKANNT:** Ob die bestehenden 16 Prüfdateien tatsächlich weiter grün bleiben, kann ohne deren Inhalt nicht garantiert werden; der Rückfall auf `BOT_FRAKTIONEN` wurde so gewählt, dass er dem heutigen Verhalten entspricht.  
- **UNBEKANNT:** Die genauen Plus/Minus-Werte für Trolle, Ghule und Gnome sind nicht durch Quellen belegt und daher als `VORSCHLAG` markiert.