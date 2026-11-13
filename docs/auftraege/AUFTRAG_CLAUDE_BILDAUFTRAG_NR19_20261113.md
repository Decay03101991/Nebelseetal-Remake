# AUFTRAG NR. 19 — Die Bildliste für den Dezember (Design-Briefs, ohne Rechnerzugriff)

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | **Claude Opus 5.5 (Thinking: hoch)** |
| **Rangordnung** | Weltenfresser zerlegt, misst, prüft, baut, führt das Register. Der Auftragsnehmer **arbeitet zu**. |
| **Pflicht in der Antwort** | Oben „Auftrag von …“ / „Antwort von …“ und ein Satz zur eigenen Rolle. |
| **Rückgabe** | Deutsch, mit Zahlen; **gemessen / gerechnet / angenommen** getrennt; Zusatzinformationen in eigenem Abschnitt. |

---

## 1. Was seit deiner Antwort Nr. 18 entschieden wurde

Daniel hat fünf Fragen einzeln beantwortet. **Drei davon nehmen Bilder von deiner Liste, zwei ändern die Regeln.**
Wortlaut und Folgen stehen in `BILDBEDARF_ENTSCHEIDUNGEN_20261113.txt` (Anlage 2).

| Frage | Entscheidung | Folge für die Liste |
|---|---|---|
| **F-100** | „Abzeichen ganz weg von der Weltkarte — die Fraktion erkennt man an der Burg“ | **B3 entfällt** (keine sechs Kartenabzeichen) |
| **F-104** | „Waren und Einheiten behalten ihre Icons, das bleibt fix, genau wie die Gebäude, die auf der Siedlungskarte erscheinen und produzieren“ | **B6, B7, B11 entfallen** (keine neuen Waren-, Einheiten- oder Gebäude-Icons) |
| **F-101** | „4× überall — scharf auch auf 200-%-Schirmen“ | Dateigröße = **4 × Anzeigegröße**, auch bei großen Flächen (dein Z2 ist damit überstimmt) |
| **F-103** | „Die Bilder von Meshy sind quasi die Referenz zum Spiel … benutz sie vor allem auch als Referenz dafür, was wir für Designs brauchen“ | Meshy-Lieferung = **Stilvorlage**, kein Spielinhalt |
| **F-99** | Code reparieren statt Bilder quadratisch anlegen | **gebaut**: Bilder werden jetzt eingepasst, nicht gezerrt; quadratisch bleibt trotzdem die Vorgabe für neue Bilder |

**Damit bleiben 16 Bilder übrig** (deine 105 minus B3, B6, B7, B11).

---

## 2. Deine Aufgabe

Schreibe **fertige Bildaufträge** — je Bild eine Beschreibung, die man ohne Rückfrage an ein Bildmodell
geben kann. **Sechs Teile:**

### Teil A — Das Stilblatt (eine halbe Seite)
Die gemeinsamen Regeln: Stil (episch, Nebelseetal, gemalt, keine Fotorealistik, keine Schrift im Bild),
Format je Bild, Alphakanal, quadratische Anlage, Goldrand wo Wappen, Licht und Nebel, Farbpalette der
sechs Häuser. **Was in KEINEM Bild vorkommt** — siehe Teil E.

### Teil B — Die 16 Einzelaufträge
Je Bild **alle** diese Felder:

| Feld | Inhalt |
|---|---|
| Kennung | z. B. `B2_drache_gruen` |
| Zweck | wofür im Spiel |
| Ansicht / Code | wo es erscheint (Fundstelle, soweit bekannt) |
| Anzeigegröße | px (aus der Tabelle unten) |
| **Dateigröße bei 4×** | berechnet (F-101) |
| Format | PNG RGBA / JPG q92 |
| Anzahl | 1 / 2 / 6 … |
| **Was zu sehen sein muss** | 1–2 gegenständliche Sätze, kein Adjektiv-Geschwafel |
| **Was NICHT zu sehen sein darf** | z. B. Helm und Helmzier, Schrift, Wölfe, Gesichter im Vordergrund |
| **Fertiger Prompt** | englischer Prompt für das Bildmodell, 40–80 Wörter, mit Stil, Motiv, Format, „no text“ |

Die 16 Bilder:

| # | Was | Anzeige | Datei bei 4× |
|---|---|---|---|
| B1 | Ruine auf der Weltkarte (Feld eines besiegten Drachen) | 19–44 px | 176 × 176 |
| B2a | Drache **grün** (Tardas der Grüne) | 19–44 px | 176 × 176 |
| B2b | Drache **rot** (Salmur der Rote) | 19–44 px | 176 × 176 |
| B5a | Startbild „Anmelden“ | 1024 × 720 | 4096 × 2880 |
| B5b | Startbild „Laden“ | 1024 × 720 | 4096 × 2880 |
| B8 | Kopfband je Volk — **sechs Stück** | bis 1127 px breit, ≤ 200 hoch | 4508 × 800 |
| B9 | Goldrahmen der Weltkarte | 400–920 px | 3680 × 3680 |
| B10a | Kachelrahmen „Ruhe“ | 57–64 px | 256 × 256 |
| B10b | Kachelrahmen „Auswahl“ | 57–64 px | 256 × 256 |
| B12 | Ressourcenleiste: Mitte (kachelbar), Ende links, Ende rechts | 64 × 34 / 16 × 34 | 256 × 136 / 64 × 136 |
| B13 | Marktplatz-Kennzeichen | 96 × 96 | 384 × 384 |

### Teil C — Die sechs Kopfbänder (B8) im Einzelnen
Für jedes der sechs Häuser ein Kopfband-Motiv. **Grundlage ist die Chronik, Teil 5** (Anlage 3), dort
stehen die Motive wörtlich. Je Haus: Name, Farben, Wappen-Motiv, Herrschaftssitz, was auf dem Band zu
sehen sein soll (Dorfstreifen, ruhig, ohne Schrift), und der fertige Prompt.

Zum Maßstab: Die Meshy-Lieferung der **Waldelfen** (Anlage 4, `elfen_wappen.png`, 1024 × 1024,
freigestellt) zeigt, welcher Stil gemeint ist — gemalt, ruhig, mit klarer Silhouette, Gold als Akzent.

### Teil D — Reihenfolge und Bündelung
In welcher Reihenfolge die 16 entstehen sollen, damit der Stil zusammenpasst, und welche sich zu einem
Blatt bündeln lassen (ein Auftrag, mehrere Bilder darauf, später geschnitten). Nenne je Bündel: welche
Bilder, wie viele, welches Seitenverhältnis das Blatt braucht.

### Teil E — Was in keinem Bild vorkommt
- **keine Wölfe** — es gibt keine solche Fraktion (Daniel, 13.11.2026)
- **kein Helm und keine Helmzier** auf Wappen (Chronik, Teil 5, bei allen sechs Häusern)
- **keine Schrift, keine Zahlen, kein Logo** im Bild
- **keine Emoji-Optik**, kein Cartoon, keine Fotorealistik
- **keine Gesichter von Menschen** als Hauptmotiv (Porträts sind ausgeschlossen)
- nichts, was eine echte Person zeigt

### Teil F — Was offen bleibt
Liste die Punkte, die du **nicht** entscheiden kannst, mit dem Grund. Bekannt offen:
- **B4** (Einzelansicht der Gebäude, 1142 × 1120): F-104 nennt nur die Gebäude, die auf der
  Siedlungskarte erscheinen und produzieren — die Einzelansicht-Hintergründe sind etwas anderes. **Nicht
  in die 16 rechnen**, aber sag, ob du sie für nötig hältst.

---

## 3. Antwortformat

1. Kopf zurück.
2. **Teil A** Stilblatt.
3. **Teil B** die 16 Aufträge als Tabelle oder je Bild ein Block — **vollständig, alle Felder**.
4. **Teil C** sechs Kopfbänder.
5. **Teil D** Reihenfolge und Bündel.
6. **Teil E** Verbotsliste (darf knapp sein, wenn oben schon klar).
7. **Teil F** offene Punkte.
8. **Fünf Zeilen Zusammenfassung**: wie viele Aufträge, wie viele Bündel, was zuerst, was du nicht beurteilen kannst.

---

## 4. Anlagen

| # | Datei | Inhalt |
|---|---|---|
| 1 | `AUFTRAG_CLAUDE_BILDauftrag_NR19.txt` (diese Datei) | Der Auftrag |
| 2 | `BILDBEDARF_ENTSCHEIDUNGEN_20261113.txt` | Daniels fünf Entscheidungen im Wortlaut und die Restliste |
| 3 | `CHRONIK_DER_WELT_20261104.txt` | Die Chronik — **Teil 5 (Zeile ~202–287)** beschreibt die sechs Häuser mit Wappen, Farben und Sitzen; Teil 3 die drei Drachen |
| 4 | `elfen_wappen.png` | Meshy-Stilvorlage (Waldelfen), 1024 × 1024, freigestellt |
| 5 | `BILDBESTAND_MESSUNG_20261113.txt` | 370 Bilddateien mit Maßen, Alpha und erster Fundstelle — zum Nachschlagen, welche Maße heute üblich sind |

## 5. Was du NICHT tust

keine Datei im Spiel ändern, nichts löschen, keine Bilder erzeugen (kein Guthaben), keine Mechanik-Zahlen
vorschlagen, keine Priorität „alles ist 1“, keine Wölfe.
