# Auftrag M-1 (starkes Modell): Truppenbewegungen auf der Weltkarte sichtbar machen

**Stand des Auftrags: 02.11.2026, Arbeitskopf `959e04a`.** Alle Zahlen unten sind am 02.11.2026 im
Arbeitsbaum gemessen (Befehl jeweils daneben). Was nicht gemessen ist, steht ausdruecklich als
UNBEKANNT dabei.

## Deine Rolle

Du bist **Entwerfer** (Designer + Architekt) fuer die SICHTBARKEIT von Truppenbewegungen auf der
Weltkarte. Du schreibst **keinen** Code ins Projekt. Du lieferst ein Papier, aus dem anschliessend
(a) ein Vergleichsbild mit deinen drei Fassungen gebaut und (b) der Einbau ohne Rueckfrage
umgesetzt werden kann.

**Verboten:** Projektdateien aendern ausser der einen Ausgabedatei; `git`; Tests starten; Fenster
oeffnen; Netzwerk; Zahlen schaetzen. Wenn du eine Angabe nicht hast, schreib
UNBEKANNT — von der Projektleitung zu liefern.

**Erlaubt und erwuenscht:** Kritik am Auftrag selbst. Wenn eine meiner gemessenen Angaben falsch
ist oder eine Frage gar nicht beantwortbar ist, sag das im Abschnitt F. Ein falscher Satz ueber den
Ist-Zustand kostet den ganzen Lauf.

## Die Vorgabe des Nutzers (woertlich, nicht umdeuten)

Registerpunkt 140 und Daniels Ansagen vom 02.11.2026:

- Sichtbar auf der Karte: **Startfeld, Zielfeld, die Linie dazwischen und eine GROBE Restlaufzeit.**
- Nicht sichtbar: **Truppenart, Anzahl, Karren, Ausruestung.** Daniels Wortlaut:
  „Ein einzelner handkarren erzeugt das gleiche bewegungssymbol wie eine ganze armee“.
- Die **genaue Geschwindigkeit bleibt verborgen**, damit sie die Einheit nicht verraet:
  „damit ich aufgrund der laufgeschwindigkeit nicht weiss welche einheit es wohl sein wird,
  sieht man nur die grobe Wegzeit“.
- **Ausnahme (Nachtrag):** laeuft ein Marsch auf eine **EIGENE** Siedlung zu, steht die Wegzeit
  **GENAU** da — „weil ich selbst betroffen bin und die zeiten einschaetzen kann als spieler“.
  Truppenart und Anzahl bleiben auch dann verborgen, die Geschwindigkeitsstufe wird nicht
  ausgewiesen.
- **Ein marschierender Verband ist KEIN Spionageziel.** Spionage zielt auf ein Dorf.
- Eigene Auftraege bekommen auf der Karte **dieselbe** Darstellung; ihre Einzelheiten stehen im
  Auftragsbuch/Postfach.
- Vorgehen des Nutzers fuer diesen Schritt: **die visuelle Darstellung waehrend der Bewegung
  (Symbol, Linie, Richtung/Puls, Groesse) soll das grosse Modell ENTWERFEN**, nicht nur Code
  schreiben. Erst ein kurzes Darstellungs-Papier mit zwei, drei Fassungen als Bild, dann umsetzen.

## Gemessener Ist-Zustand (das ist gebaut und bleibt)

| Gegenstand | Messwert | Beleg |
|---|---|---|
| Sichtbare Karte | Das **Portal-Kaestchen**; `_render_maps`/`_draw_map`/`_on_map_click` sind STILLGELEGT (tote Ansicht, dort ist nichts einzubauen) | `src/main.py:6977` (`_render_portal`), Register 93 |
| Rasterweite | 20 x 20 Felder | `src/portalraum.py:72` (`_achsen`), `feld_zahl()` |
| Zellgroesse | `zelle = max(4, 400 // kante)` → bei 20 Feldern **20 px je Feld**, Leinwand 400 x 400 px | `src/main.py:7044` |
| Fremde Doerfer (heute) | Quadrat mit zwei Diagonalen, Halbmass `halb = max(3.0, zelle*0.24)` = **4,8 px**, Fuellung `#B45309`, Rand/Linien `#FFE8C2`, Linienbreite 2 | `src/main.py:7057-7067` |
| Canvas-Tag der Doerfer | `portalbote` — eine Pruefdatei zaehlt Objekte mit diesem Tag | `src/main.py:7063`, `tests/test_spionage.py:536` |
| Klick | `<Button-1>` auf der Leinwand → `_portal_klick(ereignis.x // zelle, ereignis.y // zelle, kante)`; fremdes Dorf → `_bot_dorf_optionen`, sonst `_portal_feld_waehlen` | `src/main.py:6946`, `:7088` |
| Auftragsliste | GENAU EINE Liste `state.auftraege`; Felder je Eintrag: `art, einheiten, von, nach, ziel, fremd, entfernung, geschwindigkeit, reisezeit, start, ankunft, aktion_dauer, rueckkehr, fracht, ladung, kosten, beute, aufklaerung, warnungen, status, rueckgut, gold_verdient, abgeliefert, angewendet` | `src/auftraege.py:319` (`starten`), `:429-478` (Eintrag) |
| Phasen und Restzeit | `_status(eintrag, jetzt)` liefert `hinreise` / `am_ziel` / `rueckreise` / `abgeschlossen` **plus Restssekunden**; `laufende(liste, jetzt)` filtert die abgeschlossenen weg; `fortschritt(...)` setzt den Merker `status` | `src/auftraege.py:502`, `:547`, `:516` |
| Spieluhr | `state.spielsekunden` ist die EINE Zeitbasis der Auftraege (nicht `time.time()`) | `src/main.py:6934` (`_unterwegs_anzahl`) |
| Startposition eigener Siedlungen | `Settlement.x` / `.y` sind Weltfelder; beim Gruenden aus dem **vom Spieler gewaehlten** Weltfeld gesetzt | `src/main.py:736-741`, `:3102`, `freie_weltfelder` `:3001` |
| Zielposition fremder Doerfer | `BotDorf.x` / `.y`, fest aus Name + laufender Nummer (kein Zufall aus der Uhr); gesammelt von `_bot_doerfer_im_raster(kante)` | `src/bottaktik.py:88` (`dorf_position`), `src/main.py:8235` |
| Reihenfolge der Meldungen an den Auftragskern | `auftraege.starten(...)` bekommt `von`/`nach` als **Namen**, nicht als Koordinaten | `src/auftraege.py:319` |
| Zeichenmittel | `tkinter.Canvas`; KEINE Transparenz, keine laufende Animation ausser `after(...)`; Pillow ist im Start-Interpreter vorhanden (Python 3.11.16, Pillow 13.0.0), darf aber keine Pflicht werden | `src/main.py`, `.venv/Scripts/python.exe -c 'import PIL'` |
| Start- und Pruefinterpreter | Spiel: `.venv` Python 3.11.16 + Pillow 13.0.0; Sammellauf: Hermes-Python 3.14 | `tests/test_start_mit_pillow.py` |

## Was offen ist — und was du darueber entscheiden sollst

1. **Zwei Koordinatenraeume.** Das Portal zeichnet ein 20 x 20-Raster **je Dimension**
   (`portalraum`), die eigenen Siedlungen tragen `Settlement.x/y` auf der ALTEN Karte
   (`MAPS[...]['size']`: `kontinent` 20, `wald` 8, `berge` 8, `suempfe` 7, `portalreich` 10 —
   `src/main.py:1454-1460`). **Ob beide dasselbe Feld meinen, ist NICHT belegt.** Entscheide eine
   Lesart, begruende sie und sorge dafuer, dass eine spaetere Korrektur nur EINE Funktion trifft,
   nicht die halbe Ansicht.
2. **Der Auftrag kennt nur Namen** (`von`, `nach`). Die Position muss also ueber den Namen
   aufgeloest werden. Was passiert, wenn ein Name (alte Spielstaende, umbenannte Siedlung) nicht
   aufloest? Entscheide: unsichtbar lassen mit Hinweis, oder Linie zum Kartenrand?
3. **20 px je Feld sind klein.** Wieviel Symbol, wieviel Linie, wieviel Text ist bei 20 px
   lesbar? Nenne die Grenze in Zahlen und sage, was du deshalb WEGLAESST.

## Aufgabe

### A) Drei Fassungen der Darstellung (A, B, C)

Je Fassung ein kurzer Absatz **und** eine Zeichentabelle mit exakten Zahlen. Pflichtangaben je
Fassung — ohne diese Zahlen ist die Fassung nicht baubar und gilt als nicht geliefert:

- **Symbol** am Marschpunkt: Form (Kreis/Dreieck/Raute/Pfeil ...), Groesse in px bei `zelle = 20`,
  Fuellung und Rand als `#RRGGBB`, Linienbreite.
- **Linie** Start → Ziel: Farbe `#RRGGBB`, Breite px, durchgezogen/gestrichelt (bei tkinter:
  `dash=(a, b)`), Deckkraft gibt es NICHT — wie loest du das stattdessen?
- **Richtung / Bewegung**: Wie sieht man, dass es vorwaerts geht? Pulsieren (`after`-Takt in ms,
  welche Groesse aendert sich, um wieviel px), laufender Punkt auf der Linie, Pfeilspitze,
  Verjuengung zum Ziel hin? Nenne den Takt und die Aenderung exakt.
- **Groesse**: bleibt das Symbol bei jedem Marsch gleich (Verbotsregel: Handkarren sieht aus wie
  Armee) oder darf es mit der Entfernung wachsen? Begruende die Entscheidung gegen die Vorgabe.
- **Restzeit**: Wo steht die grobe Zeit (im Kaestchen? im Tooltip/Popup? als Zahl am Symbol?) und
  in welchen Stufen (z. B. „unter 1 h“, „1-3 h“, „3-6 h“, „ueber 6 h“ — die Stufen sind dein
  Vorschlag, die Rechnung muss aus `reisezeit`/`rest_sekunden` kommen, nicht aus der Uhrzeit).
- **Eigene Siedlung als Ziel**: wie wird die GENAU-Zeit dargestellt, ohne dass Art und Anzahl
  sichtbar werden? Was ist anders als bei einem fremden Ziel?
- **Ruhezustand am Ziel** (`am_ziel`, Aktionsdauer 0 s → kommt praktisch nicht vor) und
  **Rueckreise**: andere Farbe, gespiegelte Richtung, beides?
- **Mehrere Maersche gleichzeitig**: 2, 3, 5 — was passiert bei ueberlappenden Linien, gleichem
  Start- oder Zielfeld? Nenne den Versatz in px.
- **Eigene Auftraege**: gleiche Darstellung (Vorgabe) — was unterscheidet sie im Bild, wenn
  ueberhaupt etwas?

### B) Vergleichstabelle der drei Fassungen

Zeilen: Lesbarkeit bei 20 px · Erfuellt die Verbotsregel (keine Truppenart, keine Anzahl
erkennbar) · Verraet die Grafik die Geschwindigkeit? (ausdrueckliche Nein-Aussage mit Begruendung)
· Zahl der Canvas-Objekte je Marsch (Zaehlwachen!) · Verhalten bei 5 Maerschen gleichzeitig ·
Aufwand S/M/L · Rueckwaertskompatibilitaet (alte Spielstaende ohne Koordinaten).

### C) Empfehlung

Eine Fassung, ein Satz Begruendung, und ein Satz, was du an ihr spaeter noch verbessern wuerdest.

### D) Umsetzungsplan (damit der Einbau ohne Rueckfrage geht)

- Neue Funktion(en): Name, Signatur, Ort (`src/main.py` oder eigenes Modul — begruende).
- Daten: Vorschlag `data/marsch_optik.json` mit allen Zahlen aus A (Feldnamen und Werte
  ausschreiben); der Code soll ALLES daraus lesen, keine Zahl im Code.
- Canvas-Tags: eigener Tag je Marsch (Muster: bestehendes `portalbote`) **plus** ein Sammel-Tag;
  warum zwei.
- Klick: Wie erkennt `_portal_klick` einen Marsch, ohne das Dorf-Oeffnen zu brechen? Reihenfolge
  der Pruefungen, Toleranz in px (die Linie ist duenn — Trefferflaeche?).
- Popup/Klickinhalt: was genau steht da (nur Oeffentliches: von, nach, Restzeit in grober Stufe)?
- Wo wird gezeichnet (nach den Doerfern? darueber?) und warum.
- Was passiert bei `abgeschlossen`: Linie weg — wo wird das entschieden?

### E) Grenzfaelle (Liste mit erwartetem Verhalten)

kein Auftrag = keine Linie · Ankunft/Rueckkehr = Linie verschwindet · zwei Maersche gleichzeitig ·
Spieluhr steht (kein Fortschritt) und **Uhr rueckwaerts** (Restzeit negativ — was zeigt die
Anzeige?) · Zielname nicht aufloesbar · Marsch ueber die Kartengrenze hinaus · Marsch in eine
andere Dimension · Auftrag mit `am_ziel` und Aktionsdauer 0.

### F) Was du nicht wissen kannst

Alles, was du nicht gemessen hast, gehoert hierher — ausdruecklich auch Kritik an diesem Auftrag.
Keine Zahl erfinden.

## Form und Ausgabe

- Sprache Deutsch, Tabellen, Abschnitte **A bis F**, **hoechstens 400 Zeilen**, keine Emojis.
- **Genau EIN Ausgabepfad:** `docs/design/MARSCH_ENTWURF_20261102.md`. Keine andere Datei
  anfassen, nichts loeschen, nicht committen.
- Am Ende deiner Antwort **nur** die Zeile: `FERTIG <Zeilenzahl>`.
