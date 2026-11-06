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

**15 Dateien, 3,3 MB:** 6 Fraktionsbilder (Elfen, Gnome ×2, Ghule ×2, Menschen ×3, Zwerge ×3 als
Panoramen und Hintergründe), Burgen auf der Weltkarte, Gebäude- und Ressourcen-Icons,
Ressourcenbalken und drei Stilbilder Nebelseetal.

**Offen (keine Entscheidung ohne Daniel):** `tools/build_exe.py` gibt `assets` als Ganzes an
PyInstaller (`--add-data assets;assets`). Mit diesem Ordner wächst die EXE um 3,3 MB, obwohl die
Bilder reine Vorlagen sind. Vorschlag: beim nächsten EXE-Bau eine Ausnahmeliste für
`assets/referenzbilder` einführen - eigener kleiner Schnitt, kein Release vor S4 (F-9).
