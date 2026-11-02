# MARSCH-Darstellung auf der Weltkarte — Entwurf (M-1)

Entwerfer-Papier zum Auftrag `docs/auftraege/MARSCH_paket_20261102.md` (Stand 02.11.2026,
Arbeitskopf `959e04a`). Dieses Papier schreibt keinen Code ins Projekt; es liefert drei baubare
Fassungen, eine Empfehlung und einen Umsetzungsplan, aus dem der Einbau ohne Rückfrage erfolgt.

Alle Ist-Zahlen unten wurden am 02.11.2026 im Arbeitsbaum gemessen. Was nicht gemessen oder nicht
belegt ist, steht ausdrücklich als UNBEKANNT (Abschnitt F).

---

## A) Drei Fassungen der Darstellung

Gemeinsame, gemessene Grundlage aller drei Fassungen (Belege im Auftrag, dort nachgemessen):

- Leinwand 400 x 400 px, Raster 20 x 20, `zelle = 20` px je Feld (`src/main.py:7044`,
  `src/portalraum.py:72`).
- tkinter.Canvas: KEINE Deckkraft. Ersatz ist in jeder Fassung ein vorgemischter, gedämpfter Ton
  und/oder eine gestrichelte Linie — nie Alpha.
- Restzeit kommt ausschließlich aus `reisezeit`/`rest_sekunden` der Auftragsliste
  (`auftraege.fortschritt`), nie aus der Rechnerzeit (`src/auftraege.py:505-544`).
- Ein Auftrag kennt nur Namen (`von`, `nach`); die Position wird über eine EINE Auflösungsfunktion
  ermittelt (siehe D).
- Verbotsregel (Daniel, Register 140): Truppenart, Anzahl, Karren, Ausrüstung und die genaue
  Geschwindigkeitsstufe sind NICHT sichtbar; „Ein einzelner handkarren erzeugt das gleiche
  bewegungssymbol wie eine ganze armee". Deshalb ist das Symbol in allen drei Fassungen bei JEDEM
  Marsch gleich groß (konstant). Gegen eine wachsende Größe: eine mit der Entfernung wachsende
  Größe hinge an `reisezeit` und gäbe damit indirekt die Geschwindigkeit preis — genau das
  verbietet die Vorgabe. Deshalb: keine Größenstaffelung, kein Unterschied nach Entfernung oder
  Truppenzahl.

Je Fassung ein Absatz und eine Zeichentabelle mit exakten Zahlen.

### A.1 — Fassung A: Punkt & Linie (laufender Punkt)

Ein gedämpfter, durchgezogener Strich verbindet Start- und Zielfeld; auf ihm wandert ein kleiner
Punkt in Marschrichtung. Am wenigsten Zeichen, am klarsten lesbar bei 20 px je Feld.

| Merkmal | Wert |
|---|---|
| Symbol (Marschpunkt) | Kreis, Durchmesser 6 px, Füllung `#F59E0B`, Rand `#7C2D12`, Linienbreite 1 |
| Startfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Zielfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Linie Start→Ziel | `#F59E0B`, Breite 2 px, durchgezogen (kein dash). Deckkraft-Ersatz: vorgemischter, dunklerer Ton für Überlagerungen, keine Alpha |
| Richtung/Bewegung | laufender Punkt; `after`-Takt 400 ms. Je Takt wird die Punktposition aus `rest_sekunden` neu berechnet: Fortschritt = vergangeneReisezeit/Gesamtreisezeit, Punkt = Start + Fortschritt·(Ziel−Start) in px. Änderung je Takt = Fortschrittsdelta · Linienlänge in px; sie darf < 1 px sein (der Punkt folgt der echten Zeit, kein künstlicher Mindestsprung) |
| Größe | konstant (Verbotsregel) — kein Wachstum mit Entfernung oder Truppenzahl |
| Restzeit | nicht auf der Leinwand. Grobe Stufe im Klick-Popup und in einer Textzeile UNTER der Karte; Stufen: unter 1 h / 1–3 h / 3–6 h / über 6 h (Grenzen siehe D, `restzeit.stufen`) |
| Eigene Siedlung als Ziel | GENAU statt grob: „2 h 15 min" (Format H h M min), sonst identische Linie und identisches Symbol. Art, Anzahl und Geschwindigkeitsstufe bleiben verborgen; einziger Unterschied ist der Text |
| am_ziel (Aktionsdauer 0 s) | Punkt sitzt exakt auf dem Zielfeld, keine Bewegung (tritt nur im Ankunftssekunden-Tick auf, da `AKTION_DAUER_SEKUNDEN = 0`) |
| Rückreise | Richtung gespiegelt (Punkt wandert Ziel→Start), Linienfarbe `#38BDF8`; sonst identisch |
| Mehrere Märsche | gleicher Start- UND Zielfeld: Versatz senkrecht zur Linie um `(lfd_nr−1)·2 px`, maximal ±4 px; nur gleiches Startfeld: kein Versatz nötig (Linien laufen auseinander) |
| Eigene Aufträge | identische Darstellung (Vorgabe); Einzelheiten stehen im Auftragsbuch/Postfach, nichts Zusätzliches auf der Karte |

### A.2 — Fassung B: Pfeil (Richtung über die Spitze)

Dieselbe Linie, aber der Marschpunkt ist eine Pfeilspitze, die immer in Laufrichtung zeigt. Die
Richtung ist auch ohne Bewegung sofort ablesbar.

| Merkmal | Wert |
|---|---|
| Symbol (Marschpunkt) | Pfeilspitze (Dreieck), Spitze 6 px lang / 6 px breit, Füllung `#EF4444`, Rand `#000000`, Linienbreite 1; Drehung in Laufrichtung |
| Startfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Zielfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Linie Start→Ziel | `#EF4444`, Breite 2 px, gestrichelt `dash=(4,3)`. Deckkraft-Ersatz: gestrichelte Linie senkt das visuelle Gewicht, keine Alpha |
| Richtung/Bewegung | Pfeilspitze zeigt in Laufrichtung; Position wird je `after`-Takt 400 ms aus `rest_sekunden` neu berechnet (wie A.1). Änderung je Takt = Fortschrittsdelta · Linienlänge in px |
| Größe | konstant (Verbotsregel) |
| Restzeit | wie A.1: grobe Stufe im Popup und unter der Karte; Stufen unter 1 h / 1–3 h / 3–6 h / über 6 h |
| Eigene Siedlung als Ziel | GENAU („2 h 15 min"), sonst identisch; Art/Anzahl/Geschwindigkeitsstufe bleiben verborgen |
| am_ziel (Aktionsdauer 0 s) | Pfeilspitze steht auf dem Zielfeld, Spitze zum Ziel gerichtet, keine Bewegung |
| Rückreise | Richtung gespiegelt (Spitze zeigt zum Start), Linienfarbe `#38BDF8` |
| Mehrere Märsche | gleicher Start- UND Zielfeld: Versatz senkrecht zur Linie um `(lfd_nr−1)·2 px`, maximal ±4 px |
| Eigene Aufträge | identische Darstellung (Vorgabe); Einzelheiten im Auftragsbuch/Postfach |

### A.3 — Fassung C: Puls & Ameisenstraße

Die Linie „marschiert" als wandernde Strichmarkierung, der Punkt pulsiert. Die Bewegungsrichtung
kommt aus dem wandernden Strich (dashoffset), die Lebendigkeit aus dem Puls.

| Merkmal | Wert |
|---|---|
| Symbol (Marschpunkt) | Kreis, Durchmesser 8 px (Radius 4), Füllung `#22C55E`, Rand `#052E16`, Linienbreite 1; Radius pulsiert je Takt 4 px ↔ 5 px (Änderung ±1 px) |
| Startfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Zielfeld | hohles Quadrat (nur Rand), Kante 8 px, Farbe `#DAA520`, Linienbreite 1 |
| Linie Start→Ziel | `#22C55E`, Breite 3 px, gestrichelt `dash=(6,4)` mit laufendem `dashoffset`. Deckkraft-Ersatz: gestrichelt + wandernd, keine Alpha |
| Richtung/Bewegung | Ameisenstraße: `after`-Takt 200 ms, `dashoffset` wandert je Takt um 2 px in Laufrichtung; zusätzlich Puls des Punktes (Radius 4↔5 px, Takt 400 ms) |
| Größe | konstant (Verbotsregel) |
| Restzeit | wie A.1: grobe Stufe im Popup und unter der Karte; Stufen unter 1 h / 1–3 h / 3–6 h / über 6 h |
| Eigene Siedlung als Ziel | GENAU („2 h 15 min"), sonst identisch; Art/Anzahl/Geschwindigkeitsstufe bleiben verborgen |
| am_ziel (Aktionsdauer 0 s) | Punkt auf dem Zielfeld, Puls und Strichwanderung angehalten |
| Rückreise | Richtung gespiegelt (dashoffset wandert rückwärts, Punkt wandert Ziel→Start), Linienfarbe `#38BDF8` |
| Mehrere Märsche | gleicher Start- UND Zielfeld: Versatz senkrecht zur Linie um `(lfd_nr−1)·2 px`, maximal ±4 px |
| Eigene Aufträge | identische Darstellung (Vorgabe); Einzelheiten im Auftragsbuch/Postfach |

---

## B) Vergleichstabelle der drei Fassungen

| Zeile | A (Punkt & Linie) | B (Pfeil) | C (Puls & Ameisenstraße) |
|---|---|---|---|
| Lesbarkeit bei 20 px | gut: 2-px-Linie + 6-px-Punkt, wenig Zeichen | mittel: 6-px-Pfeilspitze klar, gestrichelte Linie unruhiger | mittel: 3-px-Linie auffällig, Puls lenkt ab |
| Erfüllt die Verbotsregel (keine Truppenart, keine Anzahl erkennbar) | ja: Symbolgröße konstant, keine Zusatzform | ja: Symbolgröße konstant, keine Zusatzform | ja: Symbolgröße konstant, keine Zusatzform |
| Verrät die Grafik die Geschwindigkeit? | Nein. Position folgt der echten Restzeit, nicht der Geschwindigkeit; die Größe ist konstant und der Takt fest 400 ms, unabhängig vom Marsch | Nein. Pfeilspitze ist starr, Takt fest 400 ms, Größe konstant | Nein. Takt fest 200/400 ms, Pulsamplitude fest ±1 px, unabhängig vom Marsch |
| Zahl der Canvas-Objekte je Marsch (Zählwache) | 4 (Linie, Start, Ziel, Punkt) | 4 (Linie, Start, Ziel, Pfeilspitze) | 4 (Linie, Start, Ziel, Punkt) |
| Verhalten bei 5 Märschen gleichzeitig | sauber: 5 dünne Linien + 5 Punkte, Versatz nur bei gleichem Start/Ziel | unruhig: 5 gestrichelte Linien + 5 Pfeile überlagern sich stärker | am unruhigsten: wandernde Striche + Puls; Versatz dringend nötig |
| Aufwand | S | S | M (dashoffset-Animation zusätzlich) |
| Rückwärtskompatibilität (alte Spielstände ohne Koordinaten) | gleich: nicht auflösbarer Name = unsichtbar mit Hinweis (Abschnitt E) | gleich | gleich |

Zählwache konkret: eine Prüfdatei zählt für den Sammel-Tag `marsch` genau `4 · Anzahl_laufender_Märsche`
Objekte und je Marsch (eigener Tag `marsch_<index>`) genau 4 — jede Abweichung verrät eine
unbeabsichtigte Zusatzzeichnung.

---

## C) Empfehlung

Empfohlen wird Fassung A (Punkt & Linie). Begründung: bei 20 px je Feld ist die durchgezogene
2-px-Linie mit 6-px-Punkt am klarsten lesbar, der Objektaufwand ist am geringsten (4 je Marsch),
und der laufende Punkt zeigt die Richtung am eindeutigsten, ohne dass eine Animation die
Kartenfläche unruhig macht. Später verbessern würde ich an A nur die Farbwahl (kontrast-/farbblind-
sichere Palette) und — falls je eine größere Kartenansicht kommt — eine mitwachsende Linienbreite,
niemals aber eine größenveränderliche Symbolgröße.

---

## D) Umsetzungsplan (Einbau ohne Rückfrage)

### D.1 Neue Funktionen

Ort: eine reine Funktion gehört in ein NEUES Modul `src/marsch_optik.py` (ohne tkinter, ohne
main-Import, testbar wie `bottaktik.py`); die Auflösung und das Zeichnen gehören nach `src/main.py`,
weil sie Spielstand und Canvas brauchen.

`src/marsch_optik.py`:

- `optik() -> dict` — lädt `data/marsch_optik.json` (EINE Datenquelle; keine Zahl im Code).
- `restzeit_text(rest_sekunden: float, genau: bool = False) -> str` — grobe Stufe oder GENAU-Text
  („H h M min"). Grenzen aus `restzeit.stufen`, Format aus `restzeit.genau_format`.

`src/main.py` (App):

- `_marsch_felder(eintrag: dict) -> tuple` — liefert `(start_pos, ziel_pos)` je None-able. DAS ist
  die EINE Korrekturstelle für die Frage der zwei Koordinatenräume (siehe F): jede spätere
  Korrektur trifft nur diese Funktion. Auflösung: `nach`/`ziel.dorf_name`+`ziel.bot_name` über
  `_bot_doerfer_im_raster(20)` → `(dorf.x, dorf.y)`; `von` über die Siedlungsliste → `(s.x, s.y)`.
- `_marsche_zeichnen(zeichenflaeche, zelle, kante)` — zeichnet alle laufenden Märsche nach den
  Zahlen aus `marsch_optik.optik()`; ruft `auftraege.fortschritt(self.state.auftraege,
  self.state.spielsekunden)` und zeichnet nur Einträge mit `status != "abgeschlossen"`.

### D.2 Daten: `data/marsch_optik.json` (vollständig, Fassung A)

```json
{
  "fassung": "A",
  "symbol": {"form": "kreis", "durchmesser_px": 6, "fuellung": "#F59E0B",
             "rand": "#7C2D12", "linienbreite": 1},
  "start_marker": {"form": "quadrat_hohl", "kante_px": 8, "farbe": "#DAA520", "linienbreite": 1},
  "ziel_marker": {"form": "quadrat_hohl", "kante_px": 8, "farbe": "#DAA520", "linienbreite": 1},
  "linie": {"farbe_hin": "#F59E0B", "farbe_rueck": "#38BDF8", "breite_px": 2,
            "muster": "durchgezogen", "dash": null,
            "deckkraft_ersatz": "vorgemischter gedaempfter Ton, keine Alpha"},
  "bewegung": {"art": "laufender_punkt", "takt_ms": 400,
               "aenderung": "position je Takt aus rest_sekunden, Fortschrittsdelta mal Linienlaenge in px"},
  "groesse": "konstant",
  "restzeit": {
    "ort": "popup_und_label_unter_der_karte",
    "stufen": [
      {"bis_sekunden": 3600, "text": "unter 1 h"},
      {"bis_sekunden": 10800, "text": "1-3 h"},
      {"bis_sekunden": 21600, "text": "3-6 h"},
      {"bis_sekunden": null, "text": "ueber 6 h"}
    ],
    "eigenes_ziel_genau": true,
    "genau_format": "H h M min"
  },
  "rueckreise": {"farbe": "#38BDF8", "richtung_gespiegelt": true},
  "mehrere": {"versatz_px": 2, "max_versatz_px": 4, "achse": "senkrecht zur Linie"},
  "klick": {"toleranz_px": 6, "reihenfolge": ["dorf", "marsch", "feld"]}
}
```

Für Fassung B/C ändern sich nur die Werte (Form/Farbe/dash/Takt) — die Struktur bleibt identisch,
damit der Einbau auf Fassungswechsel vorbereitet ist.

### D.3 Canvas-Tags

- Eigener Tag je Marsch: `marsch_<index>` (Index in der laufenden Liste) — zum gezielten Löschen
  und Neuzeichnen EINES Marsches.
- Ein Sammel-Tag `marsch` auf allen Marsch-Objekten — für die Zählwache und das Löschen ALLER
  Märsche in einem Rutsch.

Warum zwei: das Löschen eines einzelnen Marsches (Ankunft/Rückkehr) und das vollständige Neuzeichnen
bei jedem `_render_view` brauchen verschiedene Granularität; die Prüfdatei zählt über den Sammel-Tag.

### D.4 Klick

`_portal_klick` prüft in dieser Reihenfolge: (1) fremdes Dorf über `_bot_dorf_an` (Feld-genau, wie
heute) — bleibt unverändert, damit das Dorf-Öffnen nicht bricht; (2) Marsch über die kürzeste
Punkt-zu-Strecke-Distanz zum Liniensegment mit Toleranz 6 px (Linie ist 2 px dünn, die Trefferfläche
ist das 6-px-Band um das Segment); (3) sonst `_portal_feld_waehlen`. Damit hat ein Klick auf ein
Dorf immer Vorrang vor der Marschlinie, die darüberliegt.

### D.5 Popup/Klickinhalt (nur Öffentliches)

Von → Nach, grobe Restzeit (Stufe) bzw. GENAU („2 h 15 min"), wenn das aktuelle Ziel eine eigene
Siedlung ist. Keine Truppenart, keine Anzahl, keine Geschwindigkeit, keine Karren, keine
Ausrüstung.

### D.6 Zeichnungsreihenfolge

Nach den Dörfern (darüber): die Marschlinien liegen über dem Gelände und über den Dorfzeichen,
damit sie sichtbar sind; der Klick-Vorrang des Dorfes (D.4) stellt sicher, dass das Überlagern
kein Öffnen verhindert.

### D.7 abgeschlossen

Entschieden wird im Zeichner `_marsche_zeichnen`: es wird nur gezeichnet, was `fortschritt` als
`hinreise`/`am_ziel`/`rueckreise` liefert; `abgeschlossen` erscheint nicht (Linie weg). Kein
separater Löschlauf nötig, weil bei jedem `_render_view` alle Marsch-Objekte neu gezeichnet werden.

---

## E) Grenzfälle (erwartetes Verhalten)

- kein Auftrag → keine Linie, keine Marker, keine Textzeile.
- Ankunft → `am_ziel` (nur im Ankunftssekunden-Tick bei Aktionsdauer 0): Punkt auf dem Zielfeld.
- Rückkehr/abgeschlossen → Linie, Marker und Punkt verschwinden (D.7).
- zwei Märsche gleichzeitig → zwei Linien + zwei Punkte; gleiches Start/Ziel-Feld → Versatz (A).
- Spieluhr steht (kein Fortschritt) → `rest_sekunden` unverändert, Punkt bleibt stehen.
- Uhr rückwärts → `rest_sekunden` kann wieder wachsen; `_status` liefert keine negativen Werte,
  der Marsch kann in eine frühere Phase zurückfallen und erscheint dann erneut (hin/reverse).
  Die Anzeige zeigt immer die aus `rest_sekunden` berechnete Stufe, nie eine negative Zahl.
- Zielname nicht auflösbar → Marsch UNSICHTBAR lassen mit Hinweis in der Statuszeile/Log
  („Ziel 'X' nicht auf der Karte auflösbar"); KEINE Linie zum Kartenrand (die Richtung wäre
  erfunden).
- Marsch über die Kartengrenze hinaus → Start/Ziel außerhalb 0..19 werden nicht gezeichnet
  (unsichtbar mit Hinweis); keine Projektion, kein Umbrechen.
- Marsch in eine andere Dimension → wird nicht gezeichnet (das Portal-Kästchen zeigt nur die
  aktuelle Dimension); Hinweis im Log.
- Auftrag mit `am_ziel` und Aktionsdauer 0 → siehe Ankunft oben; praktisch tritt `am_ziel` nur
  für genau einen Tick auf.

---

## F) Was du nicht wissen kannst — und Kritik am Auftrag

- Zwei Koordinatenräume (Auftrag, Punkt 1): die eigene Siedlung trägt `Settlement.x/y` auf der
  ALTEN Karte (`MAPS`-`size`: kontinent 20, wald/berge 8, sümpfe 7, portalreich 10,
  `src/main.py:1454-1460`); das Portal zeichnet ein 20-x-20-Raster (`portalraum._achsen`). Dass
  beide dasselbe Feld meinen, ist im Code NICHT belegt — die beiden Systeme sind getrennte
  Konzepte (Limbus-Weltkarte vs. alte Siedlungskarte). Gemessen ist sogar ein Widerspruch:
  `spionage_starten` (`src/main.py:2176`) und `_truppen_auswahl` (`src/main.py:8387`) rechnen die
  `entfernung` als `abs(ort.x − dorf.x) + abs(ort.y − dorf.y)` und mischen damit Siedlungs-x/y
  (alte Karte) mit `BotDorf.x/y` (20-x-20, `bottaktik.dorf_position`). Die gespeicherte
  `entfernung`/`reisezeit` eines Auftrags kann dadurch auf einer anderen Rastergröße beruhen als
  der gezeichneten Linie. Für die Zeichnung unschädlich (sie nutzt Namen und `rest_sekunden`),
  für die Reisezeitdauer aber dieselbe offene Frage. Meine Lesart: Das 20-x-20-Portal ist der EINE
  Anzeigeraum; `Settlement.x/y` ist KEINE Portal-Koordinate, bis die Projektleitung das Gegenteil
  belegt. Deshalb ist die Position einer eigenen Siedlung im Portal derzeit UNBEKANNT — von der
  Projektleitung zu liefern. Die Auflösung steht isoliert in `_marsch_felder` (D.1), sodass eine
  spätere Festlegung genau EINE Funktion trifft.
- Damit ist auch der MARSCH-START bei eigenen Aufträgen (von = eigene Siedlung) derzeit nicht
  auflösbar; die Zielfelder fremder Dörfer (`BotDorf.x/y`) sind es. Die Fassungen funktionieren
  also heute nur, sobald die Projektleitung die Portal-Koordinate der eigenen Siedlung liefert.
- `fortschritt` (`src/auftraege.py:539`) kappt `rest_sekunden` auf `max(0.0, rest)` — die
  „Restzeit negativ"-Frage aus dem Auftrag tritt deshalb nicht als negative Zahl auf, sondern als
  Rückfall in eine frühere Phase bei rückwärtslaufender Uhr (E). Das ist gemessen, keine Erfindung.
- Die Prüfdatei `tests/test_spionage.py` zählt Dorf-Objekte über den Tag `portalbote`; die neuen
  Marsch-Tags (`marsch`, `marsch_<index>`) sind neu und kollidieren nicht mit bestehenden Tags.
- Nicht gemessen und daher UNBEKANNT: ob zwei Bot-Dörfer denselben Namen tragen können (dann ist
  `ziel.dorf_name`+`ziel.bot_name` der einzige eindeutige Schlüssel — die Auflösung ist darauf
  ausgelegt, aber nicht mit echten Daten geprüft); und ob es Spielstände gibt, in denen
  `Settlement.x/y` außerhalb 0..19 liegt (dann greift „nicht auflösbar").
- Kritik am Auftrag: Die Angabe „`_render_maps`/`_draw_map`/`_on_map_click` sind stillgelegt" ist
  gemessen korrekt (die lebende Ansicht ist `_render_portal`, `src/main.py:6977`). Die
  Pflichtangabe „Deckkraft gibt es nicht — wie löst du das stattdessen?" ist damit beantwortbar
  (vorgemischter Ton / gestrichelt), aber der Auftrag unterschätzt, dass bei 20 px je Feld JEDE
  Zusatzmarke (Start-, Ziel-Marker) bereits mit dem Dorfzeichen konkurriert; deshalb sind beide
  Marker bewusst hohl und 8 px klein gewählt.
