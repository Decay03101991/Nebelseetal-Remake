# Referenzbilder (Daniel, 06.11.2026)

Hier liegen die **brauchbaren** Bildvorlagen, die Daniel aus dem früheren Bildcontent
aussortiert, bearbeitet und selbst benannt hat. Der Dateiname sagt, was das Bild zeigt - die
Namen sind die Wahrheit und werden NICHT geändert oder umsortiert.

**Herkunft:** Desktopordner `Nebelseetal_Referenzbilder`, am 06.11.2026 hierher gelegt, an die
Stelle der drei entfernten Ordner. Die drei alten Sammlungen
(`hintergrund_content_20261104`, `hintergrund_content_20261106`,
`hintergrund_content_20261106_fraktionen`, zusammen 32 MB) hat Daniel am 06.11.2026 ausdrücklich
zum Entfernen freigegeben ("dürfen komplett aus dem System und aus den Nebelseetal Ordnern und aus
dem Github entfernt werden"). Sie sind mit `git rm` entfernt; die letzte Fassung steht weiter in der
Git-Historie (Commit vor `11d41ab`), ist also wiederholbar, ohne dass sie im Baum liegt.

## Das Logo ist FERTIG (06.11.2026)

`Logo_Nebelseetal_20261106.png` ist kein Referenzbild, sondern das **fertige Logo des Spiels**:
3500 x 3500, freigestellt (73 % transparent), Banner mit dem Schriftzug NEBELSEETAL.
**Entworfen hat es Herr Chris Fred Däubner für Daniel Kössl.** Es steht unter seinem Urheberrecht:
keine Weiterverwendung ohne seine Erlaubnis. Für die Besucherseite liegen web-optimierte Fassungen
unter `assets/bilder/logo_nebelseetal_klein.png` (1.294 KB) und `.webp` (309 KB, 1600 x 754).

**15 Referenzbilder, 3,3 MB** (dazu das fertige Logo, 6,6 MB): 6 Fraktionsbilder (Elfen, Gnome ×2, Ghule ×2, Menschen ×3, Zwerge ×3 als
Panoramen und Hintergründe), Burgen auf der Weltkarte, Gebäude- und Ressourcen-Icons,
Ressourcenbalken und drei Stilbilder Nebelseetal.

**Offen (keine Entscheidung ohne Daniel):** `tools/build_exe.py` gibt `assets` als Ganzes an
PyInstaller (`--add-data assets;assets`). Mit diesem Ordner wächst die EXE um 3,3 MB, obwohl die
Bilder reine Vorlagen sind. Vorschlag: beim nächsten EXE-Bau eine Ausnahmeliste für
`assets/referenzbilder` einführen - eigener kleiner Schnitt, kein Release vor S4 (F-9).

## Dieser Ordner WÄCHST - und die Bilder sind teils Spiel, teils Stil

**Entscheidung Daniel 06.11.2026 (Register 285, Punkt 3):** der Ordner wächst mit der
Designentwicklung deutlich; es kommen laufend neue Bilder dazu. Die Bilder werden **teils ingame
genutzt** (Hintergründe, Panoramen, Menübilder), **teils dienen sie nur als Stilreferenz** - deshalb
tragen sie meist `ReferenzBild` im Namen und nicht den Namen einer Ansicht. Wer ein Bild ingame
einsetzt, trägt es an der Stelle ein, wo es gebraucht wird, und lässt die Datei hier liegen; es wird
nichts umbenannt, verschoben oder umsortiert (Namen sind die Wahrheit).

**Die Bilder kommen mit in die EXE** (Daniel 06.11.2026, dieselbe Entscheidung: 3,3 MB sind egal) -
es gibt KEINE Ausnahmeliste beim Bauen. Beim ersten Startbild-Schnitt genutzt:
`ReferenzBild_Fraktionen_Elfen_Waldlandreich_im_Nebelseetal_Hintergrundbild.jpg` (Anmeldung) und
`ReferenzBild_Fraktionen_Menschen_arbeiten_im_Nebelseetal_mit_Ritter_Hintergrundbild.jpg` (Ladebild).
