# BEFUND Dorfzentrum — die Belegbilder sind veraltet, und die Spalte rollt seit `5e40828`

**Sitzung 43, 13.11.2026, 08:04–08:21.** Rein messend: es wurde **nichts** am Dorfzentrum umgebaut
(Übergabe 0340, Abschnitt 0: „währenddessen NUR lesen und dokumentieren“). Die Übergabe bittet in
Abschnitt 6 um **F-86 — Sichtprüfung der drei Belegbilder**. Diese Prüfung ist jetzt vorbereitet, und
dabei sind zwei Dinge herausgekommen, die eine Sichtprüfung allein nicht zeigen würde.

---

## 1. Die drei Belegbilder zeigen einen Zustand, den es nicht mehr gibt

| Bild | Zeitstempel | Nächster Code-Commit danach |
|---|---|---|
| `docs/audits/dorfzentrum_20261113_01xx.png` | 13.11. 01:41 | `1d11e51` 01:47 (Dorfzentrum-Ansicht), `5e40828` 02:41 (sieben Regressionen) |
| `docs/audits/dorfzentrum_werkstaetten_20261113.png` | 13.11. 01:46 | dito |
| `docs/audits/dorfzentrum_einheiten_20261113.png` | 13.11. 01:46 | dito |

Alle drei entstanden **vor** dem Commit der Ansicht selbst (01:47) und **vor** der Regressionen-Runde
(02:41). Belegt am Bild selbst: im alten Einheiten-Bild ist die **rechte Bestandsspalte am Fensterrand
abgeschnitten** (nur „Be…“ sichtbar) — genau der Fehler, der in `5e40828` als „Einheitentabelle 1 px
hoch / zu schmal“ behoben wurde. Wer diese drei Bilder beurteilt, beurteilt einen überholten Stand.

**Neue Belegbilder (echtes Fenster, heutiger Stand, 9 Stück):**

| Datei | Inhalt |
|---|---|
| `docs/audits/dorfzentrum_<reiter>_fenster_0815.png` | das ganze Fenster, 1560 × 940 (Lager / Werkstätten / Einheiten) |
| `docs/audits/dorfzentrum_<reiter>_spalte_sicht_0815.png` | die linke Spalte **so weit sie sichtbar ist** (448 × 764) |
| `docs/audits/dorfzentrum_<reiter>_arbeitsflaeche_0815.png` | die Arbeitsfläche allein (638 × 723) |

`<reiter>` ist `lager`, `werkstaetten` oder `einheiten`. Fenster: 1560 × 940 (die Größe, die `main.py`
Zeile 8773 auf diesem Schirm wählt), DPI-Faktor 1,251. Die Spalte in **voller** Höhe (448 × 1149) wird
absichtlich **nicht** abgelegt: der Bildschirm ist 1080 px hoch, der untere Teil eines solchen Abzugs
wäre fremder Desktop, kein Beleg.

---

## 2. Befund A: die linke Spalte rollt — der Block „Hinweis“ liegt außerhalb des Fensters

**Messung** (`probe_generisch.py`, HEAD `9e6e480`, 1560 × 940):

```
leinwand 448x764  yview (0.0, 0.665)      <- nur 66,5 % der Spalte sind sichtbar
spalte   448x1149                          <- die Spalte ist 1149 px hoch
   kopf       y=   0    89 hoch   sichtbar
   naechster  y=  99    62 hoch   sichtbar
   ort        y= 171    72 hoch   sichtbar
   aktionen   y= 253    89 hoch   sichtbar
   auswahl    y= 352   699 hoch   sichtbar   <- fast leer, nur das Lage-Band darin
   hinweis    y=1061    78 hoch   AUSSERHALB des Sichtfensters
```

Der Block **„Hinweis“ (der ausführliche Text des nächsten Schritts) ist ohne Scrollen nicht zu sehen**,
und der Block **„Auswahl“ ist 699 px hoch, obwohl nur das Lage-Band darin steht**. Die Übergabe 0340
behauptet in Abschnitt 2 das Gegenteil: „Blockhöhen 56 / 57 / 72 / 62 / 216 / 78 + 6 Lücken à 8 = **589
= Fensterhöhe genau**, die Spalte rollt nicht“. Das war zum Zeitpunkt der Übergabe schon falsch.

## 3. Befund B: Ursache ist die Regressionen-Runde `5e40828` (02:41) — Gegenprobe im Worktree

| | `9a8fbc2` (vor der Runde, 01:59) | `9e6e480` (HEAD, 03:22) |
|---|---|---|
| `leinwand.yview()` | **(0.0, 1.0)** — paßt genau | **(0.0, 0.665)** — rollt |
| Spalte | 448 × 764 | 448 × 1149 |
| Blockhöhen | 64 / 62 / 72 / 64 / 364 / 78 | 89 / 62 / 72 / 89 / **699** / 78 |
| `hinweis`-Block | y=676, sichtbar | y=1061, unsichtbar |
| `_dz_block_hoehen` beim Bau notiert | 64 / 62 / 72 / 64 / 364 / 78 — **richtig** | 1 / 1 / 1 / 1 / 699 / 1 — **falsch** |

**Ursache, belegt:** `5e40828` hat in `_dz_rest_verteilen` das `self.content.update_idletasks()`
entfernt (richtig — es vermaß das ganze Fenster, Register 576). Damit fehlt aber die Rechnung, die den
Rahmen zuvor auf Maß gebracht hat: `winfo_reqheight()` eines **Frames mit gepackten Kindern** liefert
**1**, solange die Geometrie noch nicht gerechnet ist. `_dz_rest_verteilen` summiert genau diese
Werte, bekommt 5 × 1 statt 5 × echter Höhe und gibt Block 5 den Rest von fast der ganzen Spalte:
764 − 5 − 48 = **699**. Die Spalte wird damit 1149 hoch und rollt.

Die Doktrin im Code („die Anforderungshöhe eines Labels steht ohne Update“) gilt für **Labels** —
nicht für **Frames**. Das ist der Unterschied, der hier fehlt.

**Warum keine Wache das gefunden hat:** `test_dorfzentrum_masse` (119/0/1) und
`test_dorfzentrum_ansicht` (44/0/1) vergleichen Zahlen zwischen Quelltext und `dorfzentrum.masse(...)`;
keine von beiden liest `winfo_height()` eines gebauten Blocks oder `yview()`. Es ist genau der
Fallstrick 1 der Übergabe („eine Wache, die Zahlen im Quelltext vergleicht, sieht keine Geometrie“) —
ein zweites Mal.

---

## 4. Befund C: zwei Maße stimmen nicht mit der Übergabe überein (offen, nicht repariert)

| Was | Übergabe 0340 | gemessen (HEAD) | Bewertung |
|---|---|---|---|
| Kachelhöhe | 206 × **83** | 206 × **82** (`dorfzentrum.masse` liefert 82) | 1 px; vermutlich die Rahmenkante. Nicht angefaßt. |
| Arbeitsfläche | R = **658** | Inhalt **638** breit, `req` 658 | 20 px fehlen; die dritte Kachelspalte (206 × 3 + 2 × 10 = 638) paßt gerade noch, der Text der dritten Spalte liegt am Rand |
| Block „Aktionen“ | — | `reqwidth` **1229** bei 448 verfügbar | der Text will 1229 px; er wird beschnitten. In `9a8fbc2` genauso (kein neuer Fehler), aber sichtbar |

Diese drei Punkte sind **nicht** angefaßt: sie gehören zu F-86 (Aussehen) und sind mit dem Spaltenfehler
zusammen zu entscheiden.

---

## 5. Was für die Sichtprüfung (F-86) jetzt vorliegt

1. Bilder, die den heutigen Stand zeigen — je Reiter das ganze Fenster, die sichtbare Spalte und die
   Arbeitsfläche (Abschnitt 1).
2. Ein gemessener Fehler, der das Urteil „zu eng“ schon vorwegnimmt: der Hinweis-Block ist weg
   (Abschnitt 2 und 3) — **das ist Nacharbeit, unabhängig vom Geschmack.**
3. Drei kleinere Maßabweichungen (Abschnitt 4), die zusammen mit dem Spaltenfehler zu entscheiden sind.

**Vorschlag zur Reihenfolge:**

1. Spaltenfehler reparieren (F-89): `_dz_rest_verteilen` darf sich nicht auf die `reqheight` von
   Frames verlassen. Zwei Wege, beide klein:
   - **(a) ohne Umbau:** die sechs Blöcke in ein `grid` legen und Zeile 5 `weight=1` geben — dann rechnet
     Tk den Rest selbst, nach dem Aufbau, ohne jede Handmessung. Das entfernt die Fehlerklasse.
   - **(b) mit minimalem Eingriff:** `_dz_rest_verteilen` an ein `<Configure>` der Spalte hängen und
     beim **zweiten** Durchlauf rechnen (dann stehen die echten Höhen der Nachbarn).
2. Danach F-86 mit den neuen Bildern beurteilen (Kacheln 82 statt 83, R 638 statt 658, Aktionen-Text).
3. Erst dann F-78 (Wappen) — oder parallel, weil es `src/` nicht berührt.

**Nicht getan:** kein Umbau, kein Commit in `src/`, kein Testlauf als Beleg für eine Änderung — es gibt
keine.

---

## 6. Belege und Nachvollziehen

```bash
# Messung Kopf gegen Vorzustand (beide Zahlenreihen ueber derselben Probe)
python -X utf8 probe_generisch.py D:/Arbeiten/Nebelseetal_Remake 1560x940
python -X utf8 probe_generisch.py <worktree auf 9a8fbc2> 1560x940

# Bilder (echtes Fenster, DPI-bewusst, Bildausschnitt 1:1)
python -X utf8 belegbilder_dorfzentrum2.py 0815
```

Die beiden Werkzeuge liegen im Scratch-Ordner der Sitzung
(`C:\Users\saras\AppData\Local\hermes\cache\scratch\`); sie ändern nichts am Spiel. Die Gegenprobe auf
`9a8fbc2` lief in einem **temporären** Worktree und ist mit einer Zeile wiederholbar:

```bash
git worktree add <beliebiger Ordner> 9a8fbc2     # danach: git worktree remove <Ordner>
```

Der Worktree wurde nach der Messung wieder entfernt (der Scratch-Ordner räumt sich, ein dort
liegender Worktree würde als toter Eintrag zurückbleiben).

**Fallstrick beim Fotografieren (neu, teuer):** `winfo_fpixels("1i") / 96` ergibt im
DPI-bewussten Prozeß **1,251** — dort sind Tk-Koordinaten aber schon physisch, das Bild wird also um
25 % verschoben und zeigt fremden Fensterinhalt. Richtig ist der Faktor **1,0**, sobald
`main.dpi_bewusst_machen()` gelaufen ist; die Probe aus `pruefstand-konventionen.md` 3d
(`grab.width / winfo_screenwidth()`) liefert ihn von selbst.
