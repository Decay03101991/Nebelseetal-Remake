# 1. Kurzfassung

Empfehlung: Der Spieler wählt beim ersten Gründen **eine** von **drei** Startkarten aus der Kategorie `mittlere`; `original-036` ist garantiert enthalten. Die Wahl ist **endgültig**, wird im Spielstand unter `startkarte_gewaehlt` gespeichert und gilt **nur für die erste Siedlung**, nicht für Kolonien. Die Kernlogik wird in `src/originalkarten.py` gekapselt; `_found_settlement` startet die Wahl nur, wenn noch keine Siedlung und noch keine Startkarte gewählt wurde. `_erste_siedlung_gruenden` nutzt die gewählte Karte oder fällt auf `original-036` zurück. Die konkrete GUI-Einbindung bleibt offen, da der vorhandene UI-Code nicht geliefert wurde.

# 2. Entscheidungen

| Frage | Messlage | Möglichkeit A (Folge) | Möglichkeit B (Folge) | Empfehlung |
|---|---|---|---|---|
| Wie viele Kandidaten? | Eingefrorener Demo-Umfang verlangt „kleine, übersichtliche Auswahl“; keine Zahl vorgegeben. | 2 Kandidaten (sehr übersichtlich, weniger Abwechslung) | **3 Kandidaten** (übersichtlich, genug Optionen) | 4 Kandidaten (mehr Auswahl, unübersichtlicher) | **3** |
| Aus welchen Kategorien dürfen sie kommen? | Heutige Startkarte ist `mittlere`; Bots erhalten gemischte Liste. | **nur mittlere** (balanciert, analog heute) | mittlere + schlechte (mehr Varianz, riskanter) | alle drei (volle Freiheit, aber `beste` könnte zu stark sein) | **nur mittlere** |
| Bleibt `original-036` einer der Kandidaten? | Heute fest verdrahtete Startkarte; Kontinuität sinnvoll. | **Ja, garantiert** (Standardkarte bleibt Option) | Nein, zufällig aus Kategorie (kann ausgeschlossen sein) | – | **Ja** |
| Ist die Wahl wiederholbar oder endgültig? | Erster Start ist kostenlos; keine Wiederholungskosten definiert. | Wiederholbar vor Bestätigung (z. B. neu würfeln) | **Endgültig** (einmal gewählt, gespeichert) | – | **Endgültig** |
| Gilt sie auch für Kolonien oder nur für den Start? | `_kolonie_gruenden` hat bereits eigene Auswahlmaske mit Vorrat und Preis. | **Nur für den Start** (erste Siedlung) | Auch für Kolonien (müsste bestehende Maske ersetzen, großer Aufwand) | – | **Nur Start** |
| Wird die gewählte Karte gespeichert? Feldname und Altlast? | JSON-Spielstand existiert; alte Spielstände haben kein solches Feld. | **Ja**, Feld `startkarte_gewaehlt` (String ID); alte Spielstände ohne Feld → Rückfall auf `original-036` | Nein, nur temporär im RAM (Wahl geht bei Neustart verloren) | – | **Feld `startkarte_gewaehlt` + Rückfall** |
| Wie werden die Kandidaten bestimmt? | Für Bots gibt es feste Liste; für Spieler keine Quelle. | **Zufällig aus `mittlere`, deterministisch pro Seed, garantiert `original-036`** | Feste, handverlesene Liste von 3 mittleren Karten (inkl. `original-036`) | – | **Deterministisch aus `mittlere`** |

# 3. Umsetzung

Die Umsetzung folgt den Empfehlungen aus Abschnitt 2.  
**Falls Daniel anders entscheidet, sind die betroffenen Schritte anzupassen.**

---

### SCHRITT 1 - `src/originalkarten.py`

**ANKER:**  
`def startkarte(seed, eigentuemer):`

**ERSATZ:**  
```python
def startkarte(seed, eigentuemer):
    """Spieler: feste versorgbare Karte; Bots: deterministische Auswahl anderer Originale."""
    if eigentuemer == "spieler":
        ident = START_ID
    else:
        kandidaten = ["original-005", "original-015", "original-019", "original-030",
                      "original-034", "original-036", "original-037", "original-051", "original-052"]
        n = int(hashlib.sha256(f"{seed}:{eigentuemer}".encode("utf-8")).hexdigest()[:12],16)
        ident = kandidaten[n % len(kandidaten)]
    return karte(ident, seed=f"{seed}:start:{eigentuemer}")


def startkarte_kandidaten(seed):
    """Liefert die Auswahlkandidaten fuer die Startkartenwahl des Spielers."""
    cfg = _startkarte_konfig()
    anzahl = int(cfg["anzahl_kandidaten"])
    kategorien = cfg["kategorien"]
    standard_id = cfg["standard_karte"]
    alle_mittlere = [k for k in alle() if k.kategorie in kategorien and k.id != standard_id]
    sortierte = sorted(alle_mittlere,
                       key=lambda k: hashlib.sha256(f"{seed}:{k.id}".encode()).hexdigest())
    auswahl_ids = [standard_id] + [k.id for k in sortierte[:anzahl - 1]]
    return [karte(id, seed=f"{seed}:startkandidat:{id}") for id in auswahl_ids]


def startkarte_auswahl_erforderlich(settlements_count, maximum, gewaehlt_id):
    """True, wenn die Startkartenwahl vor der ersten Siedlung gezeigt werden muss."""
    if settlements_count >= maximum:
        return False
    if settlements_count > 0:
        return False
    return not gewaehlt_id


def startkarte_gewaehlt(gewaehlt_id, seed):
    """Karte fuer den Spieler anhand der gewaehlten ID, sonst Standardkarte."""
    if gewaehlt_id:
        return karte(gewaehlt_id, seed=f"{seed}:start:spieler")
    return startkarte(seed, "spieler")


def _startkarte_konfig():
    import json
    from pathlib import Path
    pfad = Path(__file__).resolve().parent.parent / "data" / "startkarte.json"
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)
```

---

### SCHRITT 2 - `src/main.py`

**ANKER:**  
`        if not self.state.settlements:`

**ERSATZ:**  
```python
        if not self.state.settlements:
            if not hasattr(self.state, "startkarte_gewaehlt") or not self.state.startkarte_gewaehlt:
                self._startkarten_wahl_starten()
                return
            self._erste_siedlung_gruenden()
            return
        self._kolonie_gruenden()
```

---

### SCHRITT 3 - `src/main.py`

**ANKER:**  
`        karte = spieloekonomie.startkarte(self.state.kartenvorrat_seed, "spieler")`

**ERSATZ:**  
```python
        if hasattr(self.state, "startkarte_gewaehlt") and self.state.startkarte_gewaehlt:
            karte = spieloekonomie.karte(self.state.startkarte_gewaehlt,
                                        seed=f"{self.state.kartenvorrat_seed}:start:spieler")
        else:
            karte = spieloekonomie.startkarte(self.state.kartenvorrat_seed, "spieler")
```

---

### SCHRITT 4 - `src/main.py`

**ANKER:**  
`    def _kolonie_gruenden(self):`

**ERSATZ:**  
```python
    def _startkarten_wahl_starten(self):
        """Startkarten-Auswahlmaske oeffnen und nach Wahl die erste Siedlung gruenden."""
        kandidaten = spieloekonomie.startkarte_kandidaten(self.state.kartenvorrat_seed)
        # Die Anzeige der Kandidaten und die Auswahl werden analog zu _kolonie_gruenden
        # umgesetzt, aber ohne Gebuehr. Nach Bestaetigung wird startkarte_gewaehlt gesetzt
        # und _erste_siedlung_gruenden aufgerufen.
        def _auswahl_bestaetigen(gewaehlte_id):
            self.state.startkarte_gewaehlt = gewaehlte_id
            self._erste_siedlung_gruenden()
        # TODO: Maske mit _auswahl_bestaetigen als Callback implementieren.
        pass

    def _kolonie_gruenden(self):
```

---

### SCHRITT 5 - `data/startkarte.json`

**NEUE DATEI:** `data/startkarte.json`  
```json
{
  "anzahl_kandidaten": 3,
  "kategorien": ["mittlere"],
  "standard_karte": "original-036",
  "speicherfeld": "startkarte_gewaehlt",
  "wahl_endgueltig": true,
  "begruendung": "Startkartenwahl im eingefrorenen Demo-Umfang: uebersichtliche Auswahl aus mittleren Karten, Standardkarte als Option erhalten, Wahl wird im Spielstand gespeichert."
}
```

# 4. Neue Prüfdatei

**Datei:** `tests/test_startkartenwahl.py`  
**Vollständiger Inhalt (ASCII):**

```python
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tests.harness import check, abschnitt, bericht
import originalkarten


def main():
    abschnitt("Startkarten-Konfiguration")

    config_path = os.path.join(os.path.dirname(__file__), "..", "data", "startkarte.json")
    check("data/startkarte.json existiert", os.path.exists(config_path), "Datei fehlt")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            start_cfg = json.load(f)
        check("anzahl_kandidaten ist int > 0",
              isinstance(start_cfg.get("anzahl_kandidaten"), int) and start_cfg["anzahl_kandidaten"] > 0,
              "anzahl_kandidaten fehlt oder ungueltig")
        check("kategorien ist nicht-leere Liste",
              isinstance(start_cfg.get("kategorien"), list) and len(start_cfg["kategorien"]) > 0,
              "kategorien fehlt oder leer")
        check("standard_karte ist String",
              isinstance(start_cfg.get("standard_karte"), str) and start_cfg["standard_karte"],
              "standard_karte fehlt")
        check("speicherfeld ist String",
              isinstance(start_cfg.get("speicherfeld"), str) and start_cfg["speicherfeld"],
              "speicherfeld fehlt")
        check("wahl_endgueltig ist bool",
              isinstance(start_cfg.get("wahl_endgueltig"), bool),
              "wahl_endgueltig fehlt oder nicht bool")
        check("wahl_endgueltig ist true",
              start_cfg.get("wahl_endgueltig", False) is True,
              "Erwartet endgueltige Wahl")
    else:
        start_cfg = {"anzahl_kandidaten": 1, "kategorien": ["mittlere"], "standard_karte": "original-036"}

    abschnitt("Kandidatenliste")
    check("startkarte_kandidaten existiert",
          hasattr(originalkarten, "startkarte_kandidaten"),
          "Funktion startkarte_kandidaten fehlt")
    if hasattr(originalkarten, "startkarte_kandidaten"):
        kandidaten = originalkarten.startkarte_kandidaten("testseed")
        check("Kandidatenanzahl wie konfiguriert",
              len(kandidaten) == start_cfg.get("anzahl_kandidaten", 3),
              "Erwartet %s, erhalten %d" % (start_cfg.get("anzahl_kandidaten", 3), len(kandidaten)))
        check("Standardkarte enthalten",
              any(k.id == start_cfg["standard_karte"] for k in kandidaten),
              "Standardkarte nicht in Kandidatenliste")
        check("Alle Kandidaten in erlaubter Kategorie",
              all(k.kategorie in start_cfg["kategorien"] for k in kandidaten),
              "Mindestens eine Karte hat eine unerlaubte Kategorie")

    abschnitt("Auswahl erforderlich")
    check("startkarte_auswahl_erforderlich existiert",
          hasattr(originalkarten, "startkarte_auswahl_erforderlich"),
          "Funktion startkarte_auswahl_erforderlich fehlt")
    if hasattr(originalkarten, "startkarte_auswahl_erforderlich"):
        check("keine Siedlung und kein gewaehlt -> True",
              originalkarten.startkarte_auswahl_erforderlich(0, 999, None) is True,
              "Erwartet True bei 0 Siedlungen und keiner Auswahl")
        check("eine Siedlung -> False",
              originalkarten.startkarte_auswahl_erforderlich(1, 999, None) is False,
              "Erwartet False bei bestehender Siedlung")
        check("Maximum erreicht -> False",
              originalkarten.startkarte_auswahl_erforderlich(999, 999, None) is False,
              "Erwartet False bei Erreichen des Maximums")
        check("alter Spielstand ohne Feld -> True",
              originalkarten.startkarte_auswahl_erforderlich(0, 999, "") is True,
              "Erwartet True bei leerem gewaehlt")

    abschnitt("Rueckfall ohne Auswahl")
    check("startkarte_gewaehlt existiert",
          hasattr(originalkarten, "startkarte_gewaehlt"),
          "Funktion startkarte_gewaehlt fehlt")
    if hasattr(originalkarten, "startkarte_gewaehlt"):
        check("startkarte_gewaehlt(None) liefert Standardkarte",
              originalkarten.startkarte_gewaehlt(None, "testseed").id == start_cfg["standard_karte"],
              "Erwartet Standardkarte")
        check("startkarte_gewaehlt mit ID liefert diese Karte",
              originalkarten.startkarte_gewaehlt("original-005", "testseed").id == "original-005",
              "Erwartet Karte mit ID original-005")
        check("startkarte fuer Spieler liefert weiterhin Standardkarte",
              originalkarten.startkarte("testseed", "spieler").id == start_cfg["standard_karte"],
              "Erwartet Standardkarte fuer Spieler")

    bericht()


if __name__ == "__main__":
    main()
```

# 5. Datenwerte

Alle Werte, die nicht aus dem gelieferten Code oder Handbuch stammen, liegen in `data/startkarte.json`:

```json
{
  "anzahl_kandidaten": 3,
  "kategorien": ["mittlere"],
  "standard_karte": "original-036",
  "speicherfeld": "startkarte_gewaehlt",
  "wahl_endgueltig": true,
  "begruendung": "Startkartenwahl im eingefrorenen Demo-Umfang: uebersichtliche Auswahl aus mittleren Karten, Standardkarte als Option erhalten, Wahl wird im Spielstand gespeichert."
}
```

# 6. Dokumentzeilen

**Für `docs/PRUEFREGEL_ORIGINAL.md`:**  
`Startkartenwahl: tests/test_startkartenwahl.py; prueft Konfiguration, Kandidaten, Auswahlgrenzfaelle und Rueckfall auf Standardkarte.`

**Für `docs/ENTWICKLUNGSPROTOKOLL.md`:**  
`03.11.2026: Startkartenwahl beim ersten Gruenden vorbereitet: Funktionen in originalkarten.py ergaenzt, _found_settlement startet Auswahl nur bei fehlender Siedlung und fehlender Startkarte, _erste_siedlung_gruenden nutzt gewaehlte Karte, neue data/startkarte.json.`

# 7. Nicht beantwortet

- **UNBEKANNT:** Genaue Implementierung der GUI-Auswahlmaske in `_kolonie_gruenden` (Anzeige der Karten, Callback-Mechanismus). Die neue Methode `_startkarten_wahl_starten` enthält nur einen Platzhalter; die UI muss vom Koordinator analog zu `_kolonie_gruenden` ergänzt werden.
- **UNBEKANNT:** Struktur des State-Objekts und Serialisierungslogik. Es wurde angenommen, dass ein neues Attribut `startkarte_gewaehlt` automatisch gespeichert wird. Falls nicht, muss die `to_dict`/`from_dict`-Methode der State-Klasse angepasst werden.
- **UNBEKANNT:** Ob das Modul `spieloekonomie` die neuen Funktionen `startkarte_kandidaten`, `startkarte_gewaehlt` und `startkarte_auswahl_erforderlich` automatisch re-exportiert. Falls nicht, müssen entsprechende Imports in `spieloekonomie` ergänzt werden.