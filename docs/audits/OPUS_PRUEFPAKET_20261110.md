# PRUEFPAKET: Gegenpruefung der zwoelf Gesamtaudit-Befunde am heutigen Code

## 1. Deine Rolle

Du bist **PRUEFER**, nicht Entwerfer und nicht Ausfuehrender. Du pruefst fertigen Code gegen
schriftliche Behauptungen und lieferst Zahlen mit Fundstelle. Du aenderst keine Projektdatei, du
startest nichts, du committest nichts. Du lobst nicht, du schreibst keine Einleitung.

## 2. Was du bekommst

Die zwoelf Behauptungen eines frueheren Gutachtens (31.10.2026), eine Sichtung des Koordinators vom
10.11.2026 und den **heutigen Quellcode** der betroffenen Stellen im Wortlaut - jede Stelle mit
`Datei:Zeile`.

## 2a. Woher dieser Code kommt: aus dem VEROEFFENTLICHTEN Repo, nicht von einer Platte

Du arbeitest **gegen das oeffentliche Repository**, nicht gegen den Arbeitsordner des Auftraggebers.
Alle Stellen in Abschnitt 10 sind der veroeffentlichte Blob am **gepinnten Commit `42b646c548205274a726b0fd5e7906cacfac7b94`**:

    https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/<pfad>

Willst du eine Stelle nachlesen, lade genau diese URL (der Commit steht im Pfad - damit ist der Stand
fest und aendert sich nicht, auch wenn spaeter weitergearbeitet wird). Nenne am Anfang deiner Antwort
den Commit, den du gelesen hast. Was du **nicht** tun sollst: lokale Pfade oeffnen, im Arbeitsordner
suchen, Dateien schreiben.

**Herkunft der Dateien in diesem Paket (Abruf und Vergleich am 10.11.2026):**

| Datei | Abruf-URL (gepinnter Commit) | SHA256 (Repo = Arbeitskopie) | bytegleich |
|---|---|---|---|
| `src/auftraege.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/auftraege.py | `c53a21b81dfced3e...` | nur Zeilenenden (inhaltlich gleich) |
| `src/forschung.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/forschung.py | `2216acb93ae28593...` | ja |
| `src/kampf.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/kampf.py | `c74bbac70c4bf40f...` | ja |
| `src/main.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/main.py | `7aefce30d2de9769...` | ja |
| `src/punkte.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/punkte.py | `834aec887ece1e85...` | ja |
| `src/spielzeit.py` | https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/42b646c548205274a726b0fd5e7906cacfac7b94/src/spielzeit.py | `2c8af3c2e9aed204...` | ja |


## 3. Was du NICHT beurteilen sollst

- Keinen Abgleich gegen das Original-Handbuch (das war der Auftrag des alten Gutachtens, die
  Handbuchauszuege liegen diesem Paket absichtlich NICHT bei).
- Keine Gestaltungs- oder Geschmacksfragen.
- Keine Aussagen ueber Stellen, die hier nicht abgedruckt sind - schreibe stattdessen
  `UNBEKANNT: Stelle nicht im Paket` und nenne, welche Datei du braeuchtest.

## 4. Pflicht-Ausgabeformat (genau diese Reihenfolge, hoechstens 220 Zeilen)

**A. Tabelle der zwoelf Behauptungen** - Spalten:
`Nr | Urteil | Fundstelle (Datei:Zeile) | Gemessener Wert im Code | Was zu tun ist | Aufwand S/M/L`
Urteile nur aus diesem Vokabular:
`BESTAETIGT` (der Code tut heute noch, was die Behauptung sagt) ·
`UEBERHOLT` (der Code ist inzwischen anders - Beweis mit heutiger Fundstelle) ·
`TEILWEISE` (ein Teil stimmt, ein Teil nicht - beide Teile belegen) ·
`UNBEKANNT` (Stelle nicht im Paket).

**B. Rechnung Spieluhr x180** - die sechs Punkte aus der Rechenpflicht, je mit Formel und Zahl.

**C. Die drei schwersten offenen Punkte** - je drei Saetze, mit der Zahl, die es entscheidet.

**D. Was ich nicht wissen kann** - was dir an Material fehlt, um sicher zu urteilen.

## 5. Harte Regeln

- Jede Zeile traegt eine Fundstelle aus DIESEM Paket (Datei und Zeile).
- Keine Zahlen aus dem Gedaechtnis: jede Zahl steht im abgedruckten Code oder ist aus ihm gerechnet.
- Kein Pseudocode fuer Umbauten; hoechstens drei Zeilen Kernidee je Vorschlag.
- Wo die Behauptung und der Code auseinandergehen, gewinnt der Code - und du nennst BEIDE Stellen.

---

## 6. Messlage (Stand, aus Werkzeugen)

| Groesse | Wert |
|---|---|
| Stand (Commit, Datum) | `42b646c 2026-11-10` |
| Register belegt bis | 368 |
| Module in `src/` | 64 |
| Zeilen in `src/` | 39025 |
| Letzter Sammellauf | 217 von 217 gruen, 0 rot, 2 ausgesetzt, 9409 Pruefungen |
| EXE im Projekt | `Nebelseetal_Pre_Release_V_0.0.3.exe`, 83341753 Byte, SHA256 `a7035101...` |


## 7. Die zwoelf Behauptungen des Gutachtens vom 31.10.2026

| 1 | Ressourcenbestand (Reich/Ortskasse) | DOPPELT: eine zweite Kasse neben der fuehrenden |
| 2 | Kampfsystem | DOPPELT: zwei Kampfsysteme, Entscheidung E1 offen |
| 3 | Bauvoraussetzungen (Baukunst) | WIDERSPRUCH: sechs Gebaeude ohne Forschungspruefung |
| 4 | Tageswechsel/Goetterschutz | WIDERSPRUCH: Tageszaehlung mit `if` statt `divmod` |
| 5 | Auftragskosten und Drosselung | FEHLT: Konstante da, aber nicht angeschlossen |
| 6 | Ausbildungsgeschwindigkeit | FEHLT: Ausbildungszeit nicht an Gebaeudestufe gekoppelt |
| 7 | Menuepunkt Voraussetzungen | FEHLT: zeigt nicht alle Bedingungen |
| 8 | Bibliotheks-Obergrenze | WIDERSPRUCH: Code 2, Original 1 je Siedlung |
| 9 | Spieluhr x180 | UNBELEGT: belegte Dauern werden extrem verkuerzt |
| 10 | Siegbedingung 300 Punkte | WIDERSPRUCH: Wallstufe 8 erreicht 300 Punkte leicht |
| 11 | Beuteanteil 50 Prozent | UNBELEGT: Handbuch beziffert keinen Anteil |
| 12 | Siedlergrenze, Siedlungsmax, Startwerte | IN ORDNUNG: belegte 2009-Werte uebernommen |

## 8. Sichtung des Koordinators vom 10.11.2026 (kein Urteil - pruefen!)

Diese Zeilen sind eine SICHTUNG des Koordinators am 10.11.2026 (grep/ast, nicht nachgerechnet).
Sie sind **kein Urteil**: bestaetige oder widerlege jede Zeile am Code.

| Nr | Was am heutigen Code auffaellt | Fundstelle |
|---|---|---|
| 2 | `src/kampf_alt_handbuch_2009.py` existiert NICHT mehr; `src/kampf.py` nennt sie nur noch als fruehere Fassung. Eine Wache verlangt ausdruecklich, dass es nur EINE Schlacht-Implementierung gibt | `src/kampf.py:5`, `tests/test_gpt_kampf_forum_neu.py:83,87` |
| 4 | Die Tageszaehlung nutzt bereits `divmod` gegen EINE Tageslaenge, und der Goetterschutz prueft `tag > goetterschutz_tage()` | `src/main.py:7910-7923` |
| 5 | `SEKUNDEN_JE_FELD` ist 7200.0 (nicht 3600) und WIRD benutzt (Reisezeit-Formel); die Drosselung nennt sich selbst "nicht angeschlossen" | `src/auftraege.py:66,159,176,717-719` |
| 10 | `VORSCHLAG_ZIEL_PUNKTE` gibt es nicht mehr. Es gibt `ZIEL_PUNKTE_VERWORFEN = 300` - Daniel hat am 31.10.2026 entschieden, dass das Original KEINEN Sieg kennt (E5) | `src/punkte.py:45-50` |
| 8 | `BIBLIOTHEK_OBERGRENZE = 2` steht unveraendert | `src/main.py:3652` |
| 9 | `STANDARD_FAKTOR = 180.0` steht unveraendert | `src/spielzeit.py:34` |
| 11 | `BEUTE_ANTEIL_PROZENT = 50` steht, das Modul nennt ihn ausdruecklich VORSCHLAG | `src/auftraege.py:84,727` |
| 3 | Eine Pruefung namens `bau_zulassen` gibt es nicht; `Baukunst` steht als `voraussetzung` in den Gebaeudedaten und wird im Forschungsweg gelesen - ob `bauen_auf_karte` sie erzwingt, ist OFFEN | `src/forschungspfad.py:15,275`, `data/buildings.json` |

## 9. Rechenpflicht (fuer Abschnitt B deiner Antwort)

Rechne mit den Zahlen, die im Code stehen (nicht aus dem Kopf), und zeige je Zeile die Formel:

1. **Forschung:** Dauer bis Stufe n = n^2 Stunden (Beleg im Code). Bei Spieluhr 180: wie lange dauert
   Stufe 10 in ECHTZEIT? Wie lange Stufe 20?
2. **Reise:** `SEKUNDEN_JE_FELD` bei Spieluhr 180: wie viele echte Sekunden sind ein Feld? Zehn Felder?
3. **Ausbildung:** Grunddauer aus `pilot_ausbildung_minuten` bei Spieluhr 180 in Echtzeit.
4. **Siedlerzuwachs:** steht im Code als Zuwachs je Stunde - rechne auf echte Sekunden um.
5. **Punkte:** Wallstufe 8 = 8^3 = 512 Kriegspunkte; Gesamtpunktzahl = (Krieg + Forschung) / 2.
   Wie viele Forschungsstufen (Summe der Stufen^3) braucht man, um mit Wallstufe 8 ueber 300 zu kommen?
6. **Urteil je Zeile:** Ist die Dauer bei x180 fuer einen Einzelspieler spielbar, trivial oder
   unspielbar? Nenne die Zahl, die dein Urteil traegt.

## 10. Der heutige Code im Wortlaut (geschnitten aus dem Repo-Blob am gepinnten Commit)



### src/main.py:4656-4674 - `ortsdeckung`

```python
    def ortsdeckung(self, siedlung: Settlement, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn auch der Reichsbestand mitzahlen darf. Leer = gedeckt.

        Geprüft wird gegen die zwei Quellen, aus denen `verbrauche_am_ort` wirklich zahlt: das
        LOKALE Lager des Ortes und den Reichsbestand (Übergang). So wird nie halb gebucht.
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = float(siedlung.bevoelkerung)
                if not self._lokale_kasse_aktiv():
                    haben += float(self.population)
            else:
                haben = float(siedlung.vorraete.get(r, 0.0))
                if not self._lokale_kasse_aktiv() and r in self.resources:
                    haben += float(self.resources[r].amount)
            if haben + 1e-9 < float(v):
                fehlt[r] = round(float(v) - haben, 2)
        return fehlt
```

### src/main.py:4676-4707 - `verbrauche_am_ort`

```python
    def verbrauche_am_ort(self, siedlung: Settlement, kosten: dict) -> Tuple[bool, str]:
        """Kosten aus dem LOKALEN Lager EINES Ortes bezahlen. Liefert ``(ok, Meldung)``.

        Ökonomie-Paket, Schritt 9, Teil 3 (Entwurf Z. 779-780: „Kosten aus BP gegen gewählten Ort
        prüfen; mittels verbrauchen buchen; Siedler aus dessen bevoelkerung"). Führend ist das
        lokale Lager des Ortes; erst wenn es nicht reicht, zahlt der **Reichsbestand** dazu.
        Gebucht wird ausschließlich nach erfolgreicher Vorprüfung — eine Ablehnung ändert NICHTS.

        ÜBERGANG, ehrlich benannt (Entwurf Z. 787): alte Spielstände tragen ihre Rohstoffe noch im
        Reichsbestand (`GameState.resources`). Bis auch sie in Ortslagern führen, ist der
        Reichsbestand die zweite Kasse — gezogen wird nur der fehlende Betrag, nie mehr. Die
        Zielform („Globale resources … im Neumodus aus Anzeigen ableiten") erreicht der spätere
        Teil, indem dieser Zuschuss entfällt.
        """
        fehlt = self.ortsdeckung(siedlung, kosten)
        if fehlt:
            return False, "es fehlt " + ", ".join(f"{r} ({w:.2f})" for r, w in sorted(fehlt.items()))
        for stoff, menge in (kosten or {}).items():
            if stoff == "siedler":
                aus_ort = min(float(siedlung.bevoelkerung), float(menge))
                siedlung.bevoelkerung = float(siedlung.bevoelkerung) - aus_ort
                rest = float(menge) - aus_ort
                if rest > 0 and not self._lokale_kasse_aktiv():
                    self.population = max(0.0, float(self.population) - rest)
                continue
            aus_ort = min(float(siedlung.vorraete.get(stoff, 0.0)), float(menge))
            siedlung.vorraete[stoff] = round(float(siedlung.vorraete.get(stoff, 0.0)) - aus_ort, 2)
            rest = float(menge) - aus_ort
            if rest > 0 and not self._lokale_kasse_aktiv() and stoff in self.resources:
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - rest, 2)
        self._reichsanzeige_aus_orten()
        return True, ""
```

### src/main.py:4709-4727 - `reichsdeckung`

```python
    def reichsdeckung(self, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn das GANZE Reich zahlt (alle Ortslager + Reichsbestand). Leer = gedeckt.

        Für **globale** Aktionen, die zu keiner einzelnen Siedlung gehören (z. B. der Kartenwechsel
        auf der Weltkarte, Handbuch S. 19).
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = sum(float(s.bevoelkerung) for s in self.settlements)
                if not self._lokale_kasse_aktiv():
                    haben += float(self.population)
            else:
                haben = sum(float(s.vorraete.get(r, 0.0)) for s in self.settlements)
                if not self._lokale_kasse_aktiv() and r in self.resources:
                    haben += float(self.resources[r].amount)
            if haben + 1e-9 < float(v):
                fehlt[r] = round(float(v) - haben, 2)
        return fehlt
```

### src/main.py:4729-4763 - `verbrauche_reichsweit`

```python
    def verbrauche_reichsweit(self, kosten: dict) -> Tuple[bool, str]:
        """Kosten für eine GLOBALE Aktion aus dem ganzen Reich bezahlen. ``(ok, Meldung)``.

        Erst der Reichsbestand, dann die Ortslager (nach Kennung, damit es wiederholbar bleibt).
        Nach erfolgreicher Vorprüfung; eine Ablehnung ändert nichts.
        """
        fehlt = self.reichsdeckung(kosten)
        if fehlt:
            return False, "es fehlt " + ", ".join(f"{r} ({w:.2f})" for r, w in sorted(fehlt.items()))
        for stoff, menge in (kosten or {}).items():
            rest = float(menge)
            if stoff == "siedler":
                if not self._lokale_kasse_aktiv():
                    nimm = min(rest, float(self.population))
                    self.population = max(0.0, float(self.population) - nimm)
                    rest -= nimm
                for s in sorted(self.settlements, key=lambda x: x.id):
                    if rest <= 1e-9:
                        break
                    nimm = min(rest, float(s.bevoelkerung))
                    s.bevoelkerung = float(s.bevoelkerung) - nimm
                    rest -= nimm
                continue
            if not self._lokale_kasse_aktiv() and stoff in self.resources:
                nimm = min(rest, float(self.resources[stoff].amount))
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - nimm, 2)
                rest -= nimm
            for s in sorted(self.settlements, key=lambda x: x.id):
                if rest <= 1e-9:
                    break
                nimm = min(rest, float(s.vorraete.get(stoff, 0.0)))
                s.vorraete[stoff] = round(float(s.vorraete.get(stoff, 0.0)) - nimm, 2)
                rest -= nimm
        self._reichsanzeige_aus_orten()
        return True, ""
```

### src/main.py:7861-7942 - `tick`

```python
    def tick(self, dt_seconds: float):
        # Die monotone Laufzeituhr kann bei defektem Lieferanten oder einem
        # ungueltigen Tempo keine NaN/Inf-Spielsekunden erzeugen duerfen.
        dt_seconds = float(dt_seconds)
        if not math.isfinite(dt_seconds) or dt_seconds < 0:
            raise ValueError("Spielzeit muss endlich und nichtnegativ sein")
        # Ökonomie-Paket, Schritt 9, Teil 6b: EINE Uhr JE ORT — der Kern rechnet.
        #
        # `spieloekonomie.ort_tick` erntet (aus DERSELBEN Quelle wie die Anzeige,
        # `wirtschaft.ertrag_gesamt`), schreibt den Siedlerzuwachs bis zur Grenze des Ortes fort,
        # holt fertige Werkstattwaren ins LAGER DES ORTES und bucht abgeschlossene Ausbildungen
        # genau einmal. Vorher buchte `tick` die Ernte SELBST — und `ort_tick` tut dasselbe:
        # nebeneinander hätte das JEDE ERNTE VERDOPPELT. Deshalb steht hier jetzt nur der Kern.
        #
        # Die Gesamtsicht (Reich = Übergangsbestand + Summe der Ortslager) wird um genau die
        # Zuwächse nachgeführt, die die Orte WIRKLICH bekommen haben — berechnet aus dem
        # Unterschied vor/nach dem Kern, nicht aus einer zweiten Ertragsformel. Eine zweite
        # Rechnung wäre eine zweite Wahrheit.
        _ab = float(getattr(self, "spielsekunden", 0.0))
        _bis = _ab + dt_seconds
        # Teil 6c: was in diesem Takt WIRKLICH fertig wurde (Ware im Ortslager, ausgebildete
        # Einheit). Die Oberfläche braucht das, um neu zu zeichnen — sonst bliebe die fertige Ware
        # unsichtbar, bis der Spieler die Ansicht wechselt.
        eingetroffen: List[str] = []
        # Teil 6 (Rest): auch die FORSCHUNG laeuft auf dieser Uhr. `forschung_abschluss` hebt die
        # Stufe im WISSEN (global) und loescht den Auftrag im ORT — genau einmal.
        _wissen = {k: int(v.level) for k, v in self.research.items()}
        # Oekonomie-Paket, Schritt 10 Teil 2 (Entwurf Z. 645-648): die ORTSSEITE faehrt jetzt ueber
        # die EREIGNISUHR. `tick_bis` zerlegt den Takt in genau die Spannen, die die Ereignisse
        # vorgeben (Ausbildungsende, Forschungsende, fertige Werkstattware) — ein grosser Takt ist
        # damit GENAU so viel wie viele kleine. Vorher lief EINE Spanne [ab, bis]: eine Forschung,
        # die mitten im Takt fertig wurde, wirkte erst am Spannenende auf die Produktion (belegt in
        # tests/test_oekonomie_uhr.py, 13i: 4.000000 statt 4.372222 Holz).
        _abschnitt = _ab                                                   # Beginn des naechsten Abschnitts
        for _punkt in bot_takt_punkte(_ab, _bis):                          # S-13: je festem Bot-Punkt
            _wissen = self._orte_abschnitt(_abschnitt, _punkt, _wissen, eingetroffen)  # Orte bis dorthin
            self.bots_fortschreiben(_punkt)                                # DANN handelt der Bot - auf DIESEM Stand
            _abschnitt = _punkt                                            # naechster Abschnitt beginnt hier
        # Der Rest des Takts (auch ein Takt von 0 s: dann wird nur Faelliges gebucht).
        _wissen = self._orte_abschnitt(_abschnitt, _bis, _wissen, eingetroffen)
        # FIX 2+3: Tag fortschreiben (86400s = 1 Spieltag) + Götterschutz nach sieben Tagen bzw.
        # beim ersten Kriegspunkt beenden (Handbuch S. 6, KORREKTUR 05.10.2026 — vorher Tag 3).
        # Siedlergrenze und Siedlerzuwachs kommen aus den Haeusern der Siedlungskarten (W4b-5):
        # 10 Siedler je Siedlung, +5 je Haus, 1 neuer Siedler je Stunde (Handbuch Seite 11),
        # mit Heilkunde +10 % je Stufe. Vorher stand hier ein erfundener Zuwachs von 30 je Stunde.
        # Teil 6b: der ZUWACHS wird nicht mehr hier gerechnet — er entsteht in `ort_tick` je Ort
        # (bis zu dessen eigener Grenze) und wird oben als Unterschied in die Gesamtsicht gebucht.
        # Hier bleibt nur die GESAMTGRENZE für die Anzeige, damit keine zweite Zuwachsformel läuft.
        self.max_population = gebaeude_wirkung.bevoelkerungsgrenze(self.settlements)
        self._day_accum = getattr(self, "_day_accum", 0.0) + dt_seconds
        tage, self._day_accum = divmod(self._day_accum, zeitbasis.SEKUNDEN_JE_TAG)  # EINE Tageslaenge (R3-1)
        self.day += int(tage)
        if self.noob_protection:
            # Götterschutz (Handbuch S. 6, Z. 215-217; KORREKTUR 05.10.2026): neue Spieler sind die
            # ersten SIEBEN Tage geschützt, der Schutz endet früher mit dem ERSTEN Kriegspunkt.
            # Vorher stand hier ein fester Tag 3 — belegter Widerspruch gegen das Handbuch
            # (archiv/analysen/audits/handbuch_abgleich_2026-10-05.txt, Punkt 1). `self.day` startet bei 1,
            # also sind „die ersten sieben Tage“ day 1..7 und der Schutz endet ab day 8.
            krieg = self.punktestand()["krieg"]
            if self.day > punkte.goetterschutz_tage() or krieg > 0:
                self.noob_protection = False
                grund = ("erster Kriegspunkt" if krieg > 0
                         else f"{punkte.goetterschutz_tage()} Tage vorbei")
                self.messages.append({
                    "text": f"Götterschutz beendet ({grund}) - die Welt ist jetzt gefährlich!",
                    "type": "system"})
        # W3: fertige Waren aus den Werkstatt-Warteschlangen ins Lager buchen (genau einmal).
        self.werkstatt_fortschreiben(self.spielsekunden)
        # W7: Auftraege weiterlaufen lassen (Ankunft buchen, Heimkehrer gutschreiben).
        self.auftraege_fortschreiben(self.spielsekunden)
        # S1 (06.11.2026): abgelaufene Nachrichten aus dem Postfach nehmen; ungelesene
        # Verlustberichte verschieben ihre Frist, Militaerberichte laufen nie ab
        # (Daniel, Entscheidung 4). Fristen und Typen stehen in data/nachrichten.json.
        postfach.ablauf_buchen(self.messages, self.spielsekunden)
        # S2 (06.11.2026): laufende Mauerreparaturen steigen stueckweise (Zustand folgt der Uhr).
        self.mauer_reparatur_weiter(self.spielsekunden)
        self.last_tick = time.time()
        # Teil 6c: was in diesem Takt fertig wurde, geht an den Aufrufer ZURÜCK — die Oberfläche
        # zeichnet daraufhin neu (`NebelseetalApp._tick_loop`). `GameState` kennt keine Ansicht.
        for _was in eingetroffen[:4]:
            self._log(f"Fertig: {_was}")
        return eingetroffen
```

### src/main.py:2722-2773 - `bauen_auf_karte`

```python
def bauen_auf_karte(siedlung: "Settlement", gebaeude_key: str, feld: int,
                   forschungsstaende: Optional[dict] = None,
                   nur_pruefen: bool = False) -> tuple:
    """
    Setzt ein Gebäude auf ein Feld der Siedlungskarte.

    Rückgabe: (ja/nein, Meldung). Prüft zuerst die Eignung (Handbuch S. 7/8: beim Bauen wird
    die Eignung des Geländes angezeigt), dann ob das Feld frei ist, und zuletzt die belegte
    Obergrenze je Siedlung (Kriegerakademie, Diebesgilde, Stellmacher und Bibliothek: je
    höchstens eines — data/buildings.json, Feld 'max_je_siedlung').

    Das neue Feld bekommt die Ausbaustufe 1 (W4b-5).
    """
    if siedlung.karte is None:
        return False, "Diese Siedlung hat noch keine Karte."
    if not (0 <= feld < len(siedlung.karte["raster"])):
        return False, f"Feld {feld} liegt nicht auf der Karte."
    if str(feld) in siedlung.bauten:
        return False, (f"Feld {feld} ist bereits belegt "
                       f"({siedlung.bauten[str(feld)]}).")
    art = siedlung.karte["raster"][feld]
    erlaubt, warum = gelaende.bau_moeglich(gebaeude_key, art)
    if not erlaubt:
        return False, warum

    kennung = gelaende.finde_gebaeude(gebaeude_key) or gebaeude_key
    eintrag = gelaende.alle_gebaeude().get(kennung) or {}
    # Handbuch, Abschnitt Siedlungs-Baumenue: genau fuenf Gebaeude sind ohne Forschung baubar.
    # Alle uebrigen erfordern Kenntnisse in Baukunst. S-4 (03.11.2026): dieselbe Regel steht
    # jetzt EINMAL in `gebaeude_forschung_erlaubt` - der Spieler hier und der Bot in
    # `bot_dorf_bauen` fragen dieselbe Funktion, statt die Liste ein zweites Mal zu fuehren.
    frei, warum_forschung = gebaeude_forschung_erlaubt(kennung, forschungsstaende)
    if not frei:
        return False, warum_forschung
    grenze = eintrag.get("max_je_siedlung")
    if isinstance(grenze, int) and grenze > 0:
        schon_da = gebaeude_wirkung.gebaeude_stufe(siedlung, kennung) > 0
        if schon_da and grenze <= 1:
            _zusatz = (" Eine zweite Bibliothek ist auf einer anderen Siedlung erlaubt "
                       "(höchstens zwei je Spieler, eine je Karte)."
                       if str(kennung) == "bibliothek" else "")
            return False, (f"{eintrag.get('name', kennung)} gibt es höchstens {grenze}× "
                           f"je Siedlung (belegte Originalregel) — hier steht schon "
                           f"eines. Stattdessen ausbauen." + _zusatz)

    # Das Feld merkt sich die Ausbaustufe 1 (W4b-5); gespeichert wird der uebergebene
    # Gebaeudeschluessel wie bisher — alle Leser (gelaende, wirtschaft, gebaeude_wirkung)
    # verstehen Kennung UND Anzeigename.
    if not nur_pruefen:
        siedlung.bauten[str(feld)] = gebaeude_key
        siedlung.stufen[str(feld)] = 1
    return True, f"{warum} (Feld {feld})"
```

### src/main.py:3652-3652 - `BIBLIOTHEK_OBERGRENZE`

```python
BIBLIOTHEK_OBERGRENZE = 2
```

### src/main.py:2632-2632 - `SIEDLUNGEN_MAXIMUM`

```python
SIEDLUNGEN_MAXIMUM = 6
```

### src/main.py:3759-3762 - `MENU_ANZEIGE`

```python
MENU_ANZEIGE = {
    "Gilde": "Gildenhalle",
    "Kampfsimulator": "Schlachtsimulator",
}
```

### src/kampf.py:172-438 - `fuehre_schlacht`

```python
def fuehre_schlacht(angreifer: Dict[str, int], verteidiger: Dict[str, int],
                    wall_stufe: int = 0, wall_zustand: float = 100.0,
                    angreifer_karren: Optional[Dict[str, int]] = None,
                    verteidiger_karren: Optional[Dict[str, int]] = None,
                    vorraete: Optional[Dict[str, float]] = None,
                    rng: Optional[random.Random] = None,
                    forschung_angreifer: Optional[dict] = None,
                    forschung_verteidiger: Optional[dict] = None,
                    boni_angreifer: Optional[dict] = None,
                    boni_verteidiger: Optional[dict] = None,
                    schwellen: Optional[tuple] = None,
                    zweite_phase: Optional[dict] = None) -> Dict[str, Any]:
    """Führt reproduzierbar eine Schlacht nach der späteren Originalbeschreibung aus.

    Nicht im Dokument geregelte Gerätelager- und Beutemechanik bleibt aus dem
    älteren Handbuch erhalten; siehe GPT-KA01 Quell-/Abweichungsregister.

    V-5 (03.11.2026): `boni_angreifer`/`boni_verteidiger` sind Prozentwerte je Seite, wie sie
    `bottaktik.modifikatoren` bzw. `boni.kampf_werte` liefern: ``{"at": 5.0, "pa": -5.0}`` bzw. mit
    "beute". AT skaliert den NAHKAMPF-Wurf, PA die Ruestung, "beute" die nutzbare Karrenladung.
    Ohne Angabe rechnet die Schlacht exakt wie bisher (Faktor 1,0) - der Zufall bleibt unberuehrt,
    weil weiter dieselben `randint`-Grenzen gezogen werden.

    `zweite_phase` ist Daniels Entscheidung zur Frage 2 (05.11.2026): faellt die Wache des
    Verteidigers UNTER DIE HAELFTE, schlaegt der Feueratem ein ZWEITES Mal zu - mit dem Anteil
    aus dem Dict (`atem_prozent`, bezogen auf die angetretenen Nahkaempfer des Angreifers) und
    nur EINMAL je Gefecht (`unter_anteil`, Vorgabe 0,5). Ohne Angabe oder mit `aktiv=False`
    rechnet die Schlacht wortgleich wie vorher.
    """
    if rng is None:
        rng = random.Random()

    def _prozent(quelle, schluessel: str) -> float:
        """Ein Prozentwert aus einem Boni-Dict - 0,0 bei fehlendem oder kaputtem Wert."""
        if not isinstance(quelle, dict):
            return 0.0
        try:
            return float(quelle.get(schluessel) or 0.0)
        except (TypeError, ValueError):
            return 0.0

    at_a, pa_a = 1.0 + _prozent(boni_angreifer, "at") / 100.0, 1.0 + _prozent(boni_angreifer, "pa") / 100.0
    at_v, pa_v = 1.0 + _prozent(boni_verteidiger, "at") / 100.0, 1.0 + _prozent(boni_verteidiger, "pa") / 100.0
    beute_faktor = 1.0 + _prozent(boni_angreifer, "beute") / 100.0
    stufe = max(0, min(10, int(wall_stufe)))
    zustand = max(0.0, min(100.0, float(wall_zustand)))
    A, V = _einheiten(angreifer, "Angreifer"), _einheiten(verteidiger, "Verteidiger")
    a_wissen = forschung_angreifer or {}
    v_wissen = forschung_verteidiger or {}
    geraet = dict(angreifer_karren or {})
    for n, k in (angreifer or {}).items():
        if E.rolle(n) == "belagerung":
            # Beide Aufrufkonventionen sind erlaubt: Gerät kann im Angreifer-
            # Dict ODER separat übergeben werden. Kein doppeltes Belagerungsgerät.
            geraet.setdefault(n, max(0, int(k)))
    belagerung = {n: k for n, k in geraet.items() if E.rolle(n) == "belagerung"}
    logs = [f"Kampfmodell {STAND}; Wall Stufe {stufe} Zustand {zustand:.1f}%"]
    unsicher = ["Forschungsstand nicht übergeben: Wert 0 statt fiktiver Bot-Forschung"] if (
        forschung_angreifer is None or forschung_verteidiger is None) else []
    result = {"stand": STAND, "ausgang": "unentschieden",
              "kampf_stattgefunden": False, "vorrunde_bestanden": False,
              "sequenzen": [],
              "verluste_angreifer": {}, "verluste_verteidiger": {},
              "geflohen": [], "mauer_zustand": zustand, "beute": {},
              "bericht": "", "unsicher": unsicher}
    def fertig(ausgang):
        result["ausgang"] = ausgang
        result["verluste_angreifer"] = dict(Counter(u["name"] for u in A if u["tot"]))
        result["verluste_verteidiger"] = dict(Counter(u["name"] for u in V if u["tot"]))
        result["geflohen"] = [f"{u['name']} (Angreifer)" for u in A if u["rueckzug"]]
        result["bericht"] = "\n".join(logs)
        return result

    # Ohne Nahkampfeinheiten darf es weder automatischen Sieg noch Beute geben.
    # Ein reiner Fernkampftrupp darf schiessen, erobert aber nichts im Nahkampf.
    if not A:
        logs.append("Keine eigenen Kampfeinheiten: kein Kampf, keine Beute")
        return fertig("unentschieden")

    # Wallvoraussetzung vor der Schlacht; SK und Intervalle bleiben Originaldaten.
    if stufe:
        wall = spieldaten.wallstufen()[stufe - 1]
        # Neu gefundenes Originalforum: die Fußtruppen-Schwelle wird von
        # NAHKAMPFeinheiten überwunden. Fernkämpfer zählen nicht dazu;
        # sonst könnten reine Bogenschützen ohne Sturmtruppen Wall 1 öffnen.
        foot_sk = sum(E.schlagkraft(u["name"]) for u in _nah(A))
        siege_sk = sum(E.schlagkraft(n) * int(k) for n, k in belagerung.items())
        faktor = zustand / 100.0
        if foot_sk < float(wall["schwellenwert_fussttruppen"]) * faktor:
            logs.append("Fußtruppen: Schwelle nicht erreicht; die Truppen ziehen sich zurück; kein Kampf")
            return fertig("unentschieden")
        schwelle_bel = wall.get("schwellenwert_belagerungswaffen")
        if schwelle_bel is not None and siege_sk < float(schwelle_bel) * faktor:
            logs.append("Belagerungs-Schlagkraft zu gering: Schwelle nicht erreicht; die Truppen ziehen sich zurück; kein Kampf")
            return fertig("unentschieden")
    # W-14 Teil 2 (05.11.2026): der Drache hat KEINEN Wall. Statt der Wallstufe gelten seine
    # beiden eigenen Schwellen (Schuppen). Die Rechnung ist wortgleich die der Wallvorrunde -
    # dieselbe Schlagkraft, dieselbe Reihenfolge, dieselbe Folge (Rückzug, kein Kampf).
    elif schwellen:
        foot_sk = sum(E.schlagkraft(u["name"]) for u in _nah(A))
        siege_sk = sum(E.schlagkraft(n) * int(k) for n, k in belagerung.items())
        try:
            grenze_fuss, grenze_bel = int(schwellen[0]), int(schwellen[1])
        except (TypeError, ValueError, IndexError):
            grenze_fuss, grenze_bel = 0, 0
        logs.append("Drachenschuppen: Fußtruppen %d gegen %d, Belagerung %d gegen %d"
                    % (foot_sk, grenze_fuss, siege_sk, grenze_bel))
        if foot_sk < grenze_fuss:
            logs.append("Fußtruppen: Schwelle nicht erreicht; die Truppen ziehen sich zurück; kein Kampf")
            return fertig("unentschieden")
        if siege_sk < grenze_bel:
            logs.append("Belagerungs-Schlagkraft zu gering: Schwelle nicht erreicht; die Truppen ziehen sich zurück; kein Kampf")
            return fertig("unentschieden")

    result["vorrunde_bestanden"] = True
    result["kampf_stattgefunden"] = True

    # Schutz in Türmen: jeweils beste 10/30 Nahkämpfer des Angreifers.
    schutz = 10 * int(belagerung.get("Belagerungsturm", 0)) + \
             30 * int(belagerung.get("Großer Belagerungsturm", 0))
    geschuetzt = {id(u) for u in sorted(_nah(A),
                 key=lambda u: (u["hi"], u["kon"]), reverse=True)[:max(0, schutz)]}

    # Mauerstufe + 1 echte Vorrunden – selbst ohne Mauer genau eine.
    # Beide Seiten treffen Entscheidungen vor Verrechnung der Rundenerschöpfung.
    for runde in range(stufe + 1):
        schuesse = []
        for schuetze_seite, gegner, wissen, abzug in (
            (A, V, a_wissen, 0.05 * stufe * (zustand / 100.0)),
            (V, A, v_wissen, 0.0),
        ):
            for schuetze in _fern(schuetze_seite):
                ziele = _nah(gegner) or _fern(gegner)
                if not ziele:
                    continue
                ziel = rng.choice(ziele)
                chance = schuetze["fern"] / 100.0 + \
                         0.02 * _forschungsstufe(wissen, "Bogenbau") - abzug
                if schuetze_seite is V and id(ziel) in geschuetzt:
                    chance -= 0.30
                chance = max(0.0, min(1.0, chance))
                if rng.random() < chance:
                    schuesse.append((ziel, schuetze["fern_schaden"]))
        for ziel, schaden in schuesse:
            ziel["erschoepfung"] += schaden
        zeilen = [f"Fernkampf-Vorrunde {runde + 1}/{stufe + 1}: {len(schuesse)} Treffer"]
        for u in A + V:
            _ausgeschieden(u, rng, zeilen)
        logs.extend(zeilen)
        result["sequenzen"].append("\n".join(zeilen))

    # Mauerschaden erst NACH sämtlichen Schussvorrunden: beeinflusst nächsten Kampf.
    mauerschaden = 0
    for name, menge in (belagerung.items() if stufe else ()):
        minimum, maximum = E.mauer_schaden(name)
        for _ in range(max(0, int(menge))):
            if maximum > 0:
                mauerschaden += max(0, rng.randint(minimum, maximum) - stufe)
    result["mauer_zustand"] = max(0.0, zustand - mauerschaden)
    logs.append(f"Mauerschaden nach Fernkampf: {mauerschaden}; Zustand {result['mauer_zustand']:.1f}%")

    ursprung_fern = len(_fern(A))
    rueckzug_je_runde = math.ceil(ursprung_fern * 0.2)
    # Zweite Atemphase (Frage 2, 05.11.2026): VOR dem Nahkampf vorbereiten. Gezaehlt wird die
    # Wache, die jetzt noch steht - faellt sie unter den Anteil, brennt der Atem ein zweites Mal.
    zp_aktiv = bool(isinstance(zweite_phase, dict) and zweite_phase.get("aktiv", True))
    try:
        zp_prozent = float((zweite_phase or {}).get("atem_prozent") or 0.0)
        zp_anteil = float((zweite_phase or {}).get("unter_anteil") or 0.5)
    except (TypeError, ValueError):
        zp_prozent, zp_anteil = 0.0, 0.5
    zp_aktiv = zp_aktiv and zp_prozent > 0
    zp_wache_start = len(_alle(V))                                        # Wache beim Antreten
    zp_fusstruppen = len([u for u in A if u["fern"] is None])             # Nahkaempfer beim Antreten
    zp_gefeuert = False                                                   # nur EINMAL je Gefecht
    if zp_aktiv:                                                          # nur bei eingeschalteter Phase
        result["zweite_phase"] = {"atem_prozent": zp_prozent, "unter_anteil": zp_anteil,
                                  "ausgeloest": False, "verluste": 0}
    nahkampf_sequenzen = 0
    for seq in range(1, 11):
        if not _nah(A) or not _alle(V):
            break
        nahkampf_sequenzen = seq
        protokoll = [f"Nahkampf-Sequenz {seq}"]
        # 20 % der ursprünglich vorhandenen angreifenden Schützen ziehen
        # sich je Sequenz zurück, die stärksten zuerst.
        for u in sorted(_fern(A), key=lambda x: (x["fern"], x["kon"]), reverse=True)[:rueckzug_je_runde]:
            u["rueckzug"] = True
            protokoll.append(f"{u['name']} zieht sich zurück")
        for kaempfer in sorted(_nah(A), key=lambda u: (u["hi"], u["kon"])):
            if not _aktiv(kaempfer):
                continue
            ziele = _nah(V) or _fern(V)
            if not ziele:
                break
            ziel = rng.choice(ziele)
            a_wurf = rng.randint(kaempfer["lo"], kaempfer["hi"])
            v_wurf = rng.randint(ziel["lo"], ziel["hi"])
            a_kampf = (a_wurf * at_a * (1 + 0.10 * _forschungsstufe(a_wissen, "Schmiedekunst"))
                       - ziel["ruestung"] * pa_v * (1 + 0.10 * _forschungsstufe(v_wissen, "Schmiedekunst"))
                       - kaempfer["erschoepfung"])
            v_kampf = (v_wurf * at_v * (1 + 0.10 * _forschungsstufe(v_wissen, "Schmiedekunst"))
                       - kaempfer["ruestung"] * pa_a * (1 + 0.10 * _forschungsstufe(a_wissen, "Schmiedekunst"))
                       - ziel["erschoepfung"])
            protokoll.append(f"{kaempfer['name']} {a_kampf:.2f} gegen {ziel['name']} {v_kampf:.2f}")
            loser = [ziel] if a_kampf > v_kampf else ([kaempfer] if a_kampf < v_kampf
                                                       else [kaempfer, ziel])
            for u in loser:
                u["erschoepfung"] = max(u["erschoepfung"], u["schwelle"])
                _ausgeschieden(u, rng, protokoll)
            if len(loser) == 1:
                sieger = kaempfer if loser[0] is ziel else ziel
                if _aktiv(sieger):
                    sieger["erschoepfung"] += 2
                    _ausgeschieden(sieger, rng, protokoll)
        result["sequenzen"].append("\n".join(protokoll))
        logs.extend(protokoll)
        # Zweite Atemphase: die Wache ist unter ihren Anteil gefallen (Frage 2, 05.11.2026).
        if zp_aktiv and not zp_gefeuert and zp_wache_start > 0 \
                and len(_alle(V)) * 2 < zp_wache_start:                   # UNTER der Haelfte
            zp_gefeuert = True                                            # nur einmal je Gefecht
            zp_verluste = max(0, int(round(zp_fusstruppen * zp_prozent / 100.0)))
            getroffen = []                                                # wen der Atem trifft
            for u in sorted(_nah(A), key=lambda x: (x["hi"], x["kon"])):   # die schwaechsten zuerst
                if len(getroffen) >= zp_verluste:
                    break
                u["inaktiv"] = True                                       # kampfunfaehig
                u["tot"] = True                                           # gefallen
                getroffen.append(u["name"])
            zeile = ("Zweiter Feueratem: die Wache steht unter %d von %d - %d Nahkämpfer fallen"
                     % (int(zp_wache_start * zp_anteil), zp_wache_start, len(getroffen)))
            logs.append(zeile)                                            # im Bericht sichtbar
            result["sequenzen"].append(zeile)                             # eigene Sequenz
            result["zweite_phase"].update({"ausgeloest": True, "verluste": len(getroffen)})
        if not _alle(V) or not _nah(A):
            break

    if not _alle(V) and not _nah(A):
        # Kein Sieger, wenn beide Nahkampfseiten gleichzeitig ausscheiden.
        ausgang = "unentschieden"
    elif not _alle(V) and _alle(A):
        ausgang = "angreifer"
    elif not _nah(A):
        ausgang = "verteidiger"
    else:
        ausgang = "unentschieden"
    # Nicht zurückgezogene Schützen werden bei Niederlage überrannt und
    # müssen wie im Forumstext die Konstitutionsprobe bestehen.
    if ausgang == "verteidiger":
        for u in _fern(A):
            u["inaktiv"] = True
            u["tot"] = rng.randint(1, 100) > u["kon"]
            logs.append(f"{u['name']} überrannt: {'gefallen' if u['tot'] else 'entkommen'}")

    if ausgang == "angreifer":
        result["beute"] = _beute(geraet, vorraete, beute_faktor)
        ent, verl = _sieggeraete(verteidiger_karren, nahkampf_sequenzen, rng)
        if verteidiger_karren:
            result["geraete_erhalten_verteidiger"] = ent
            result["geraete_verloren_verteidiger"] = verl
    elif ausgang == "verteidiger":
        ent, verl = _sieggeraete(geraet, nahkampf_sequenzen, rng)
        if geraet:
            result["geraete_erhalten"] = ent
            result["geraete_verloren"] = verl
    logs.append(f"Ausgang: {ausgang}; Nahkampf-Sequenzen: {nahkampf_sequenzen}")
    return fertig(ausgang)
```

### src/auftraege.py:66-66 - `SEKUNDEN_JE_FELD`

```python
SEKUNDEN_JE_FELD = 7200.0
```

### src/auftraege.py:72-72 - `DROSSELUNG_SCHRITTE_PROZENT`

```python
DROSSELUNG_SCHRITTE_PROZENT = 10
```

### src/auftraege.py:79-79 - `AKTION_DAUER_SEKUNDEN`

```python
AKTION_DAUER_SEKUNDEN = 0.0
```

### src/auftraege.py:84-84 - `BEUTE_ANTEIL_PROZENT`

```python
BEUTE_ANTEIL_PROZENT = 50
```

### src/spielzeit.py:34-34 - `STANDARD_FAKTOR`

```python
STANDARD_FAKTOR = 180.0
```

### src/punkte.py:50-50 - `ZIEL_PUNKTE_VERWORFEN`

```python
ZIEL_PUNKTE_VERWORFEN = 300
```

### src/punkte.py:98-108 - `kriegspunkte`

```python
def kriegspunkte(einheiten: Optional[dict], wall_stufe: int) -> int:
    """Punkte aus Einheiten (fester Wert je Einheit) plus Wall (Stufe hoch drei).

    ``einheiten`` bildet Einheitenname -> Anzahl ab. Einheiten ohne Punktewert
    (Handelskarawanen, Siedlerkarren — Handbuch: "Punktewert: -") zaehlen 0.
    """
    summe = 0
    for name, anzahl in (einheiten or {}).items():
        summe += _ke_einheit(name) * _anzahl(anzahl)
    summe += _stufe(wall_stufe) ** 3
    return summe
```

### src/punkte.py:190-192 - `goetterschutz_tage`

```python
def goetterschutz_tage() -> int:
    """Die belegten sieben Tage Schutz (Handbuch S. 6)."""
    return GOETTERSCHUTZ_TAGE
```

### src/forschung.py:41-49 - `dauer_stunden`

```python
def dauer_stunden(stufe: int) -> int:
    """Forschungsdauer fuer das Erreichen von `stufe`: Stufe zum Quadrat, in Stunden.

    Delegiert an die Originalregel in `spieldaten`. Fuer Stufen unter 1 gibt es nichts zu
    erforschen -> 0 Stunden.
    """
    if stufe < 1:
        return 0
    return spieldaten.forschungsdauer_stunden(stufe)
```
