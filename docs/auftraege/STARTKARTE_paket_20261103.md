# AUFTRAG STARTKARTE — Kartenwahl fuer den SPIELER beim Gruenden (starkes Modell, 03.11.2026)

Du bist der Planer UND Umsetzer eines konkreten Schritts in einem lokalen Einzelspieler-Remake
(Python 3, tkinter, JSON-Spielstand, offline, keine Netzverbindung). Auftraggeber ist Daniel.
Du kannst nichts ausfuehren - behaupte also keine Testergebnisse, sondern liefere Text, den der
Koordinator einbaut und prueft.

## GEGENSTAND (gemessen am Code vom 03.11.2026, Kopf 75f2236)

Heute bekommt der Spieler beim ersten Gruenden **keine Wahl**: die Startkarte ist fest verdrahtet.

- `src/originalkarten.py`, `START_ID = original-036`, und `startkarte(seed, eigentuemer)` gibt bei
  `eigentuemer == "spieler"` immer diese eine Karte zurueck ("Das Z", Kategorie **mittlere**,
  `typ_name` = "Das Z", `vorteil` = "Originalkarte (mittlere): Goldwert 57.0, Lederwert 60.0 / h,
  ohne Forschung"). Bots bekommen dagegen eine von NEUN Karten aus einer festen Kandidatenliste,
  deterministisch aus `sha256(seed:eigentuemer)`.
- Der Vorrat hat **127 Originalkarten**: 35 `beste`, 43 `mittlere`, 49 `schlechte`
  (`originalkarten.alle()`, Feld `kategorie`). Die private Spieler-Startkarte liegt bewusst AUSSERHALB
  des Kolonievorrats (`originalkarten.vorrat`).
- `src/main.py`, `_found_settlement()`: erster Start -> `_erste_siedlung_gruenden()`, sonst
  `_kolonie_gruenden()`. **16 Pruefdateien (22 Aufrufstellen) rufen `_found_settlement()` bzw.
  `_erste_siedlung_gruenden()` ohne Argument auf und erwarten sofort eine Siedlung** - diese Aufrufe duerfen nicht brechen.
- `_erste_siedlung_gruenden()` wuerfelt heute ein freies Weltfeld (bis 200 Versuche, kein Wasser, keine
  NPC-Fraktion), uebernimmt die Startbestaende GENAU EINMAL (verschieben, nicht kopieren), setzt die
  drei Startgebaeude (`_startgebaeude_setzen`) und laesst das Dorfzentrum offen
  (`dorfzentrum_offen = True`).
- Die **Kolonie-Gruendung hat bereits eine Auswahlmaske** (`_kolonie_gruenden`): Kartenvorrat, Nutzen,
  Preis, Mindestbestand, Weltfeld steht VOR der Zahlung fest. Das ist das Muster, an dem sich die
  Startwahl orientieren soll - aber OHNE Gebuehr (Handbuch S. 7: erster Start kostenlos).
- Fuer die Anzeige existieren bereits: `spieloekonomie.kapazitaeten(karte)`,
  `spieloekonomie.achsen(karte)`, `spieloekonomie.relativ(karte)` und
  `gelaende.karte_beschreiben(karte)`.

**Vorgabe Daniel (02.11.2026, Demo-Umfang eingefroren):** "Kernkreis + Spionage + Voelker- und
Kartenwahl am Start; alles andere kommt NACH dem ersten Demo-Upload."

## WAS DU LIEFERST

Ein Dokument, deutsch, mit genau diesen Abschnitten:

1. **Kurzfassung** - hoechstens 10 Zeilen: welcher Weg, was du NICHT entschieden hast.
2. **Entscheidungen** - Tabelle `Frage | Messlage | Moeglichkeit A (Folge) | Moeglichkeit B (Folge) |
   Empfehlung`. Diese Entscheidungen gehoeren Daniel; du empfiehlst, du entscheidest nicht. Mindestens
   diese Fragen: wie viele Kandidaten (2/3/4); aus welchen Kategorien duerfen sie kommen (nur mittlere,
   mittlere+schlechte, alle drei); bleibt `original-036` einer der Kandidaten; ist die Wahl
   wiederholbar (neu wuerfeln) oder endgueltig; gilt sie auch fuer Kolonien oder nur fuer den Start;
   wird die gewaehlte Karte im Spielstand gespeichert (Feldname!) und was passiert mit alten
   Spielstaenden ohne dieses Feld.
3. **Umsetzung** - je Schritt ein Block: `SCHRITT <n> - <Datei>`, darunter `ANKER:` mit einer
   **wortgleichen** Zeile aus dem unten gelieferten Code (so, dass sie in der Datei genau einmal
   vorkommt) und `ERSATZ:` mit dem vollstaendigen neuen Code (Einrueckung wie im Original). Neue
   Dateien als `NEUE DATEI: <pfad>` mit vollem Inhalt.
4. **Neue Pruefdatei** - vollstaendiger Inhalt, **ASCII** (ein Umlaut = SyntaxError beim Import),
   Muster `tests/harness.py` (`check(name, cond, detail)`, `abschnitt`, `bericht`). Je Entscheidung
   mindestens eine Bedingung, dazu die Grenzfaelle: keine Siedlung / eine Siedlung / Maximum erreicht,
   alter Spielstand ohne das neue Feld, Wahl ohne Argument (Rueckfall auf heute).
   **Pflicht:** eine Bedingung, die bei der HEUTIGEN, fest verdrahteten Fassung rot wird.
5. **Datenwerte** - jede Zahl, die nicht aus einer Quelle stammt, gehoert als Wert in eine JSON-Datei
   unter `data/` (nicht fest in den Code), mit einem Feld, das die Begruendung traegt (Vorschlag:
   `data/startkarte.json`).
6. **Dokumentzeilen** - je eine Zeile fuer `docs/PRUEFREGEL_ORIGINAL.md` (Register) und
   `docs/ENTWICKLUNGSPROTOKOLL.md`.
7. **Nicht beantwortet** - was du nicht belegen konntest, mit `UNBEKANNT`.

## HARTE REGELN

- **Keine Zahl ohne Quelle.** Belegt ist nur, was in den gelieferten Codeauszuegen oder im Handbuch
  steht. Erfundene Preise, Dauern oder Wahrscheinlichkeiten sind ein Fehler.
- **Der stehende Aufruf bleibt:** `_found_settlement()` ohne Argument und
  `_erste_siedlung_gruenden()` ohne Argument muessen weiterhin sofort gruenden (16 Pruefdateien, 22 Aufrufstellen).
- **Die zwei Regeln, die nie gebrochen werden:** Doerfer werden NIE eingenommen; Angriffstruppen werden
  nie am Zielort stationiert. (Hier nicht beruehrt - aber keine Beschreibung darf etwas anderes sagen.)
- **Kein Fenster, kein Netz:** alles muss ohne laufendes Spiel pruefbar sein.
- **Pruefdateien sind ASCII**, Spieltexte duerfen Umlaute tragen (UTF-8 in `src/`).
- **Keine stillen Aenderungen an bestehenden Entscheidungen:** wird eine alte Wache falsch, wird sie
  UMBENANNT und die neue Entscheidung im Docstring genannt - nicht der Code zurueckgebogen.

## GELIEFERTER CODE (wortgetreu, Stand 75f2236)

`src/originalkarten.py`:

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
```

`src/main.py`, `_found_settlement` (vollstaendig) und der Kopf von `_erste_siedlung_gruenden`:

```python
    def _found_settlement(self):
        """Eine Siedlung gruenden (Oekonomie-Paket, Schritt 9, Teil 5; Entwurf Z. 777).
        ...
        """
        if len(self.state.settlements) >= SIEDLUNGEN_MAXIMUM:
            self._log(f"Maximale Siedlungsanzahl erreicht ({SIEDLUNGEN_MAXIMUM}).")
            return
        if not self.state.settlements:
            self._erste_siedlung_gruenden()
            return
        self._kolonie_gruenden()

    def _erste_siedlung_gruenden(self):
        """Startkarte und belegte Startwerte (Handbuch S. 7: 10 Siedler, 100 Holz, 100 Stein)."""
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        size = cfg["size"]
        self.state._weltkarte_sicherstellen()      # die Startsiedlung steht auf einem Weltfeld
        if not self.state.kartenvorrat_seed:
            self.state.kartenvorrat_seed = "nebel-%d" % random.randrange(1, 10 ** 9)
        if not self.state.kartenvorrat:
            self.state.kartenvorrat_anlegen(self.state.kartenvorrat_seed)
        karte = spieloekonomie.startkarte(self.state.kartenvorrat_seed, "spieler")
        for _ in range(200):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            tile = self.state.get_tile(x, y, size)
            if not (tile and tile.terrain != "water" and not tile.npc_faction):
                continue
            ...
            sett = Settlement(name="Siedlung 1", map_id=self.state.current_map, x=x, y=y,
                              karte=karte,
                              id=siedlung_kennung("spieler", self.state.current_map, x, y))
```

`src/main.py`, die vorhandene Kolonie-Auswahl (Muster fuer die Maske):

```python
    def _kolonie_gruenden(self):
        """Die Auswahlmaske einer Neugruendung oeffnen: Kartenvorrat, Nutzen, Preis, Weltfeld."""
        karten = self.state.freie_koloniekarten()
        if not karten:
            self._log("Keine freie Koloniekarte mehr im Vorrat - es laesst sich keine Siedlung "
                      "mehr gruenden.")
            return
        felder = self.state.freie_weltfelder(6)
        if not felder:
            self._log("Kein freies Weltfeld fuer eine Gruendung gefunden.")
            return
```

## RAHMEN

- Ziel des Schritts: der Spieler waehlt beim ERSTEN Gruenden seine Startkarte aus einer kleinen,
  uebersichtlichen Auswahl und sieht je Karte Typ, Vorteil, die drei Achsen und die Bauplaetze.
- Der Schritt gehoert zum eingefrorenen Demo-Umfang (Kartenwahl am Start), ist also Vorrang vor allem
  anderen.
- Antworte auf Deutsch, mit klaren Ueberschriften, ohne Ausschmueckung. Wo du etwas nicht weisst:
  `UNBEKANNT` statt einer Vermutung.
