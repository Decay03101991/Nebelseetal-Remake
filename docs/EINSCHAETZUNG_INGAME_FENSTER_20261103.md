# Einschaetzung: Ingame-Fenster und fluessige Ansichtswechsel (03.11.2026)

Daniels Fragen: (1) Koennen neue Menues und Fenster INGAME erscheinen - ueber das Hauptfenster gelegt,
Hintergrund abgedunkelt und transparent - statt als eigene Fenster auf dem Desktop? (2) Muss bei jedem
Klick die ganze Ansicht neu geladen werden, und wie aufwaendig ist das abzustellen? (3) Die Weltkarte
soll optisch anders werden (Felder und Rahmen), Groesse und Aufbau bleiben.

**Antwort in einem Satz: BEIDES IST MOEGLICH - der Weg dahin ist bei (2) ein echter Umbau, bei (1)
eine saubere, kleine Reihe von Schnitten.**

## 1. Was heute im Code steht (gemessen, nicht geschaetzt)

| Gegenstand | Befund | Beleg |
|---|---|---|
| Echte Zusatzfenster | **10** Stellen erzeugen ein `tk.Toplevel` - jedes davon ist ein eigenes Fenster auf dem Desktop | `grep -n "Toplevel(" src/main.py` |
| Ansichtswechsel | `_switch_view` -> `_render_view`; `_render_view` **zerstoert ALLE Widgets** im Inhaltsbereich (`widget.destroy()`) und baut sie neu auf, dann springt die Ansicht nach oben | `src/main.py`, `_render_view` |
| Aufrufe dieses Neuaufbaus | **46** Stellen rufen `_render_view()` direkt; 10 Stellen wechseln die Ansicht | `grep -c "_render_view()"`, `grep -c "_switch_view("` |
| Karte | die Portal-Karte zeichnet je Aufruf neu; die Objekte werden nicht wiederverwendet | `_render_portal` |
| Grafikgrundlage | tkinter (Tk 8.6) mit Canvas und Pillow im Projekt-venv | `START_SPIEL_WINDOWS.bat`, `src/gebaeude_optik.py` |

**Das ist die Ursache des Gefuehls "abgehakt":** nicht die Rechenzeit des Spiels, sondern das
Zerstoeren und Neuerzeugen von teils hunderten Widgets je Klick - inklusive Bildaufbau
(`gebaeude_optik`), Scroll-Reset und Neuzeichnen der Karte.

## 2. Frage 1 - Ingame-Fenster statt Desktop-Fenster: JA

**Technisch:** Tk kann Widgets innerhalb des Hauptfensters uebereinander legen (`place()` mit
`relx/relwidth`, `lift()`), und ein Dialog kann die Eingabe sperren (`grab_set`) - genau das, was ein
Modal leisten soll. Es braucht dafuer **kein** `Toplevel`: ein Overlay-Rahmen im Hauptfenster genuegt.

**Die Verdunkelung mit Transparenz - der einzige Stolperstein:** tkinter kennt **keine Transparenz je
Widget** (Alpha gibt es nur fuer das ganze Fenster). Zwei belegte Wege erzeugen den gewuenschten
Eindruck trotzdem:

1. **Vorgerenderte Halbtransparenz (empfohlen):** ein Bild in Fenstergroesse, das nur aus einer
   dunklen Flaeche mit Alpha besteht (Pillow: `RGBA`, `(0,0,0,140)`), als `Label` ueber den Inhalt
   gelegt. Sieht aus wie echtes Abdunkeln, das darunterliegende Fenster bleibt durchscheinend
   sichtbar. Pillow ist im Start-venv vorhanden - es braucht keinen neuen Baustein.
2. **Tk-Bordmittel ohne Bild:** ein `Canvas`-Rechteck ueber die ganze Flaeche mit `stipple` (z. B.
   `gray50`). Funktioniert ohne Pillow, ist aber ein Punktraster statt einer weichen Toenung.

Der Dialog selbst liegt dann als normaler `Frame` mit Rahmen und Schattenbild auf dieser Flaeche - und
kann trotzdem die vorhandenen Bilder aus `gebaeude_optik` nutzen (Kastenbild, Leistenbau).

**Aufwand:** klein bis mittel. Ein gemeinsamer Overlay-Baustein (oeffnen, schliessen, Hintergrund,
Eingabesperre, Escape) und danach je umgestelltem Dialog ein kurzer Schnitt. Zehn Toplevel sind ein
abzaehlbarer Vorrat, nicht ein Fass ohne Boden.

## 3. Frage 2 - kein Neuaufbau bei jedem Klick: JA, in vier Stufen

**Warum es heute so ist:** `_render_view` ist der EINE Weg, eine Ansicht zu zeigen, und er baut immer
alles neu. Ein Klick auf "bauen" loest eine Aktion aus und danach denselben Totalaufbau.

**Stufen, von billig nach teuer (jede einzeln spielbar und pruefbar):**

| # | Massnahme | Wirkung | Aufwand |
|---|---|---|---|
| A | **Doppel-Puffer:** neue Ansicht unsichtbar aufbauen, dann in EINEM Zug tauschen (statt zerstoeren und dann fuellen) | kein Flackern, kein Zwischenzustand; die Wartezeit bleibt, das Flackern verschwindet | klein (ein Umbau von `_render_view`, betrifft alle 46 Aufrufe auf einen Schlag) |
| B | **Karte ohne Neuaufbau:** Canvas-Objekte EINMAL erzeugen, danach nur `itemconfig`/`coords` (belegter Standardweg gegen langsamer werdende Canvas) | Klicks auf der Karte werden sofort; die Karte ist die Ansicht mit den meisten Objekten | mittel, aber in sich geschlossen (`_render_portal`) |
| C | **Refresh-Pfad fuer die fuenf haeufigsten Ansichten** (Dorfuebersicht, Karte, Kaserne, Forschung, Lager): Widgets wiederverwenden und nur Werte setzen (`config`) statt neu bauen | das Gefuehl "abgehakt" verschwindet dort, wo es am meisten stoert | mittel bis gross (je Ansicht ein eigener Pflegeweg) |
| D | **Teil-Renderer** fuer die restlichen Ansichten | gleichmaessig fluessig ueberall | gross (54 Ansichten) |

**Ehrliche Grenze:** A wirkt sofort und ueberall, kostet aber nur das Flackern. C ist der Punkt, an dem
sich das Spiel wirklich fluessig anfuehlt - dort muss je Ansicht entschieden werden, was sich aendert
und was stehen bleibt. D ist Fleissarbeit und lohnt erst, wenn A bis C belegt sind.

**Recherche-Befund (kurz):** der Standard gegen Flackern in Tk ist genau dieser Weg - Widgets
wiederverwenden (`config`) statt zerstoeren, den Aufbau vor dem Anzeigen abschliessen
(`update_idletasks`), und auf dem Canvas Objekte einmal erzeugen und danach nur aendern. Kein
Alternativ-Framework noetig; ein Wechsel auf ein anderes Toolkit waere ein Neubau der Oberflaeche und
steht in keinem Verhaeltnis.

## 4. Weltkarte optisch (Groesse und Aufbau bleiben)

Drei Vorschlaege, alle ohne Aenderung der Spiellogik:

1. **Gemalte Kacheln statt Farbflaechen:** die vorhandenen Kartenmotive aus `assets/` als Kacheln je
   Gelaendeart, mit weichen Kanten - nah an der Originaloptik, wirkt sofort "gemacht".
2. **Feines Raster mit Geländefarben und Lichtkante:** keine harten Rechtecke mehr, sondern eine
   Flaeche mit Gelaendeton, feiner Trennlinie und dunkler Rahmenleiste; die Auswahl bekommt einen
   Goldrand statt eines blauen Kastens.
3. **Rahmen als Bildleiste:** der vorhandene Leistenbau (`main.leiste_zusammensetzen`) um die Karte -
   Ecken fest, Kanten dehnbar. Das ist die billigste Variante, weil das Werkzeug schon da ist.

Empfehlung: 3 als Rahmen (sofort), 2 fuer die Felder (ein Schnitt), 1 spaeter als eigene Bildlieferung.

## 5. Vorschlag zur Reihenfolge

1. **A (Doppel-Puffer)** - ein Schnitt, wirkt auf alle Ansichten, klein.
2. **Overlay-Basis + die drei haeufigsten Dialoge ingame** - dein Wunsch aus Frage 1, sichtbar.
3. **B (Karte ohne Neuaufbau)** zusammen mit dem neuen Karten-Design.
4. **C (Refresh fuer die fuenf haeufigsten Ansichten)** - hier wird es fluessig.
5. Der Rest (D) nach Bedarf, wenn Daniel es im Spiel noch als hakelig empfindet.

Jeder Schritt: eigene Wache, Sammellauf, Registerzeile. Kein Schritt aendert Spiellogik oder Zahlen -
es geht ausschliesslich um die Oberflaeche.
