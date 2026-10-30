# Kartenregel – nur Originale (verbindlich ab 28.10.2026)

## Was aktiv ist

- **127 Originalvarianten**, IDs exakt aus `data/originalkarten/katalog.json` (inkl. Variantenkennung, nicht automatisch eine lückenlose fortlaufende Zahlenreihe!).
- `src/originalkarten.py`: Daten und Kartenauswahl; jede Karte hat `originalkarte_id`, 10×10-Raster und 100 Feldtypen.
- `assets/karten/original/{beste,mittlere,schlechte}/`: unveränderte authentische Kartenbilder samt Quellenhash.
- `assets/karten/spielfeld/original-*.png`: 640×640 nearest-neighbor-Versionen derselben Gesamtbilder, ohne neue künstlich gezeichnete Wald-/Gebirgsformen.
- `src/originalkarten_grafik.py`: liest die Grafik eines vorhandenen Original-IDs, validiert 10×10 und liefert einen realen Bildpfad. Fehlt etwas: sichtbarer Fehler, **kein** stilles Zurückfallen auf generierte Karten.
- `src/main.py::_zeichne_siedlungskarte`: Hintergrund = Originalgrafik, darüber Wege/Gebäude/Wall/Auswahl/Koordinaten; `karten_optik_fein` weiterhin für diese **Overlays**, nicht mehr als Geländehintergrund.
- `src/gelaende.py::siedlungskarte_erzeugen`: bei Kompatibilitätsaufruf ohne Altparameter ausschließlich originale Spieler-Startkarte; alte `mass`/`typ_id` werden abgelehnt. `src/spieloekonomie.py::feste_karte` ist deaktiviert.
- Savegame-Ladeweg: historischer Kartentyp ohne `originalkarte_id` oder mit anderem Format wird vor Zustandsänderung abgewiesen. Alte Dateien nicht löschen.

## Was nicht mehr aktiv ist

- 8×7-Generator und die errechneten Kartenprofile aus alten 'waldreich/weideland/bergreich'-Typen.
- Fantasie-Gelände-Renderer `karten_optik_fein.gelaende_plan_fein` für die Siedlungskarte. Die Funktion kann als historische UI-Hilfe im Code vorhanden sein, wird aber nicht mehr aufgerufen.
- 17 veraltete Testdateien mit 8×7-/künstlichen Testfixtures: `archiv/tests_legacy_8x7/`; müssen in richtige Originalkarten-Tests überführt werden.
- `data/gelaende.json` enthält weiterhin die belegten Geländeregeln, aber keine alten Kartentypen oder Kartenmaße als aktive Quelle. Archiv der alten Daten: `archiv/legacy_karten_8x7/`.

## Grenzen / Qualitätskontrolle

**Das echte Bild ist Referenz; die technischen Feldtypen wurden bei 25 Karten noch nicht manuell bestätigt.** Für Holzfäller/Bergbau/Wege muss das jeweilige Feld im Bild mit `spielraster[i]` übereinstimmen. Daher nicht behaupten, dass jede automatisch abgeleitete Klassifikation bereits belegt ist. Am besten eine visuelle 10×10-Korrekturmaske und Tests pro korrigierter Karte etablieren, ohne Originalbild zu verändern.

Die Weltkarte/20×20-Weltkoordinaten sind eine andere Spielebene und nicht die frühere 8×7-Siedlungskarte. Nicht ohne eine eigene Originalquelle austauschen.

## Reproduktion der Grafik

`py -m pip install Pillow` (nur fürs Quellbild-Werkzeug), dann `py tools\originalkarten_grafiken_bauen.py`. Das Spiel selbst benötigt weiterhin **keine** Pillow-Abhängigkeit; Windows `tk.PhotoImage` liest die erzeugten PNGs. Der EXE-Build nimmt `assets/` und `data/` mit.

Die Bauten sind weiterhin zeichnerische Overlays; ein vollständiger grafischer Nachbau des historischen Baumenüs (`docs/nebelseetal_gamestar2.jpg`) ist **noch offen**.
