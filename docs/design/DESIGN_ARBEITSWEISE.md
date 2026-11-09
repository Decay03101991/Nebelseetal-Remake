# Designarbeit im Nebelseetal-Remake - Ablauf und Ablage

**Stand:** 09.11.2026, 01:45. Diese Datei regelt, wie Design-Lieferungen (Daniel, Opus 5.5,
Dritte) ins Projekt kommen, wo sie liegen und was davon ins Spiel darf. Sie ersetzt keine
Projektregel, sondern ordnet den Designweg in den bestehenden Ablauf ein.

## 1. Wo was liegt

| Ebene | Ort | Was liegt dort | Im Repo? | In der EXE? |
|---|---|---|---|---|
| Eingang | Desktop (Symbol auf `D:\Desktop`) | die unveränderte Lieferung | nein | nein |
| Rohpaket | `archiv/design/<JJJJMMTT>_<thema>/paket.zip` | die ZIP, byte-gleich | nein (gitignoriert) | nein |
| Entpackt | `.../entpackt/` | der Inhalt, unverändert und unbenannt | nein | nein |
| Referenzbilder | `archiv/design/referenzbilder_<datum>/` | Rohbilder und Stilvorlagen | nein | nein |
| Fertige Assets | `assets/...` | geschnittene, größenoptimierte Dateien | ja | ja |
| Dokumente | `docs/design/*.md` | Prüfungen, Modelle, Entwürfe | ja | nein |
| Belege | `SHA256SUMS.txt` je Ordner | Hash jeder Datei | nein | nein |

**Bilder kommen nur dann in einen spielrelevanten Ordner, wenn sie im Spiel genutzt werden**
(Daniel, 09.11.2026). Das gilt für Referenzbilder wie für Designvorlagen: eine Stilvorlage ist
kein Bestandteil des Spiels. Bis zur Nutzung liegen alle Bilder in
`archiv/design/<JJJJMMTT>_<thema>/` oder `archiv/design/referenzbilder_<datum>/`; erst mit dem
Einbau wandert die gebrauchte Datei nach `assets/...` und bekommt dort eine Zeile in der README,
wo sie eingesetzt wird. Damit wächst weder der Ordner noch die EXE mit Vorräten.
**Aufgehoben** ist damit die ältere Fassung (Entscheidung 06.11.2026: der Ordner wächst mit der
Designentwicklung).

## 2. Der Ablauf in sieben Schritten

Jede Lieferung läuft gleich, egal von wem sie kommt:

1. **Abholen.** Liegt auf dem Desktop etwas, das zum Design gehört, wird es **nicht** geöffnet und
   **nicht** bearbeitet, sondern als Ganzes übernommen.
2. **Hash vor dem Räumen.** `sha256sum` auf Quelle und Kopie; erst wenn beide gleich sind, wird der
   Desktop geräumt. Räumen heißt **verschieben, nicht vernichten**.
3. **Ablegen.** `archiv/design/<JJJJMMTT>_<thema>/` mit `paket.zip`, `entpackt/` und
   `SHA256SUMS.txt`; dazu eine Zeile in `archiv/design/README.md`. Nichts umbenennen.
4. **Lesen und prüfen.** Zuerst die LIES-MICH-Datei des Pakets, dann das Hauptdokument. **Jede
   Zahlenangabe gegen die Datendateien halten** (`data/*.json`), nicht gegen den Vortrag des
   Pakets. Widersprüche gehören mit Belegstelle in `docs/design/DESIGN_PRUEFUNG_<datum>.md`.
5. **Urteil.** Je Punkt: übernehmbar, nicht übernehmbar oder offen - **mit Grund**. Was
   spielersichtbar ist, entscheidet Daniel; ich lege ihm die Punkte als Fragen vor (einzeln, je drei
   Vorschläge, der empfohlene zuerst).
6. **Umsetzen.** Nur geschnittene Assets nach `assets/`; **eine Quelle je Wert** (Farben und Maße in
   `data/*.json` oder im Skin, keine zweite Farbtabelle im Code). Originale Daniels werden nie
   verändert, im Spiel stehen nur skalierte Kopien.
7. **Beleg.** Protokollzeile und Registerzeile wie bei jedem anderen Schritt, mit Prüfzahl,
   Gegenprobe und Sammellauf.

## 3. Regeln, die aus Daniels Vorgaben stammen

- **Logo** (Herr Däubner): immer auf dunklem Grund, nie verzerren, umfärben oder beschneiden; die
  Urheberzeile bleibt sichtbar.
- **Burgbilder und Drachenfiguren sind Daniels Grafiken** - Originale unangetastet.
- **Die 125 Siedlungskarten** für den Dörferausbau bleiben, wie sie sind.
- **Keine Ausbaustufen designen** - weder für Burgen noch für Gebäude oder Felder.
- **Malstil** ist der der Stilreferenzen: gemalt, warmes Licht vorn, kühler Nebel hinten.
- **Nebelsee:** auf der Siedlungskarte bebaubar (Tempel liefert Mana). **Auf der Weltkarte KEINE Sperre:** das Gelaende ist dort reine Anzeige, ein Dorf darf auch auf Nebelsee und Sumpf landen (Daniel 09.11.2026, Register 329; bestaetigt die Entscheidung vom 01.11.2026). Nebelsee und Sumpf duerfen im Design als Deko gemalt werden, ohne eine Regel zu tragen.

## 4. Was am 09.11.2026 eingeplant wurde

Die erste Lieferung (`20261109_designvorschlag_01`, Opus 5.5) liegt im Archiv und ist geprüft:
`docs/design/DESIGN_PRUEFUNG_20261109.md`. Sie schlägt eine **isometrische** Weltkarte
(128 x 64 px je Kachel) vor. Die heutige Portalkarte ist ein **flaches 20 x 20-Quadrat** mit
Geländefarben. Das ist keine Farbänderung, sondern ein Umbau des Zeichners - er wird als eigener
Schnitt geplant (`D-2` im Prüfdokument), nicht nebenbei gemacht.

**Reihenfolge der Designarbeit** (Vorschlag, Daniel entscheidet):

| Nr | Schritt | Fertig, wenn |
|---|---|---|
| D-1 | Abgleich des Pakets mit den Projektdokumenten, Widersprüche notiert | Prüfdokument liegt, jeder Punkt hat ein Urteil |
| D-2 | Entscheidung: flaches Raster behalten oder isometrisch umbauen | Daniels Wort steht im Protokoll |
| D-3 | Testkarte 20 x 20 mit den sieben Geländearten und Tannen | sieht aus wie die Stilprobe, Belastungstest im Fenster |
| D-4 | Burgen auf der Weltkarte je Fraktion (skalierte Kopien) | drei blaue Fraktionen sind im kleinsten Zoom unterscheidbar, Freigabe Daniel |
| D-5 | Portal mit Burgen und den belegten Bannern (grün/rot) | Übersicht und Detail stehen, Freigabe Daniel |
| D-6 | Drachen auf der Weltkarte, Ruine für den Sieg | drei Drachen an ihren Feldern, Ruinenbild beauftragt |
| D-7 | Fehlende Fraktionsbilder (Trolle zuerst) | jede Fraktion hat Panorama, Szene und Medaillon |
| D-8 | Logo in Ladeseite, Portal und Startmenü | überall auf dunklem Grund, Freigabe Daniel |

D-1 und D-2 sind Vorarbeit ohne Code und **beide erledigt**:

- **D-1 (09.11.2026):** Nachtrag im Prüfdokument — Selbstkorrektur an W-D1, W-D6 bis W-D9, Bildersumme
  (24 von 35 Bilddateien des Pakets sind pixelgleich mit vorhandenem Material).
- **D-2 (09.11.2026, Daniel):** erst eine **flache** Testkarte mit gemalten Kacheln (D-3);
  isometrisch nur, wenn der Stil flach nicht trägt (Register 328). Die isometrische Stilprobe ist
  damit zurückgestellt, nicht abgelehnt.

**Kein Designschritt ändert Spielregeln.** Wo ein Design eine Regel berührt (etwa ob ein Gelände auf
der Weltkarte sperrt), entscheidet Daniel, nicht das Paket — so am 09.11.2026 geschehen: **keine
Geländesperre**, das Gelände bleibt reine Anzeige (Register 329).
