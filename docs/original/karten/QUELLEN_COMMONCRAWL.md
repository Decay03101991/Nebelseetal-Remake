# Quellen: Common Crawl — Bildsuche Nebelseetal.de

Erstellt: 2026-10-04 | Werkzeug: Common Crawl Index API (index.commoncrawl.org) + Range-Download (data.commoncrawl.org)

## Ergebnis (Kurzfassung)

**Common Crawl enthaelt KEINE einzige Bilddatei von nebelseetal.de** — weder die Siedlungskarte
noch sonstige Spielbilder. In allen geprueften Indizes (2008-2026) wurden ausschliesslich
HTML/CSS/PDF/XML/JS-Records gefunden; kein Record mit MIME `image/*` und keine URL mit
Endung .jpg/.jpeg/.gif/.png/.bmp. Das deckt sich mit dem Befund des Internet Archive.

Common Crawl hat aber die **HTML-Seiten** des alten PHP-Spiels (Crawl 2009/2010) archiviert.
Diese HTML-Seiten verweisen auf die Original-Bildpfade, u. a. `bilder/screens/siedlung.jpg`.
Die Bild-Bytes selbst wurden von Common Crawl nie abgerufen/gespeichert.

## Vorgehen

1. Alle CC-Indizes aus `https://index.commoncrawl.org/collinfo.json` (128 Indizes) geladen.
2. Jeden Index abgefragt: `<cdx-api>?url=nebelseetal.de%2F*&output=json&limit=5000&matchType=domain`
   (matchType=domain deckt auch Subdomaenen wie forum./midagrad. ab).
3. Nach Bildern gefiltert: MIME beginnt mit `image/` ODER URL endet auf Bildendung.
4. Bei Treffern waeren die Bytes per HTTP-Range (`data.commoncrawl.org/<filename>`) geholt,
   entgzippt, der HTTP-Kopf vom Bildkoerper getrennt und die Magic-Bytes geprueft worden.
   -> Dieser Schritt entfiel, weil **kein** Bildtreffer existierte.

## Abdeckung pro Index

Geprueft: **86 von 128** Indizes. Nicht geprueft: 42 (siehe unten).

| Index | Ergebnis |
|---|---|
| CC-MAIN-2026-39 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-34 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-30 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-25 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-21 | 2 Treffer |
| CC-MAIN-2026-17 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-12 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-08 | 0 Treffer (keine Captures) |
| CC-MAIN-2026-04 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-51 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-47 | 2 Treffer |
| CC-MAIN-2025-43 | 2 Treffer |
| CC-MAIN-2025-38 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-33 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-30 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-26 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-21 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-18 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-13 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-08 | 0 Treffer (keine Captures) |
| CC-MAIN-2025-05 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-51 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-46 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-42 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-38 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-33 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-30 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-26 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-22 | 2 Treffer |
| CC-MAIN-2024-18 | 0 Treffer (keine Captures) |
| CC-MAIN-2024-10 | 0 Treffer (keine Captures) |
| CC-MAIN-2023-50 | 0 Treffer (keine Captures) |
| CC-MAIN-2023-40 | 0 Treffer (keine Captures) |
| CC-MAIN-2023-23 | 2 Treffer |
| CC-MAIN-2023-14 | 0 Treffer (keine Captures) |
| CC-MAIN-2023-06 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-49 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-40 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-33 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-27 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-21 | 0 Treffer (keine Captures) |
| CC-MAIN-2022-05 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-49 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-43 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-39 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-31 | 2 Treffer |
| CC-MAIN-2021-25 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-21 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-17 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-10 | 0 Treffer (keine Captures) |
| CC-MAIN-2021-04 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-50 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-45 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-40 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-34 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-29 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-24 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-16 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-10 | 0 Treffer (keine Captures) |
| CC-MAIN-2020-05 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-51 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-47 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-43 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-39 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-35 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-30 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-26 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-22 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-18 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-13 | 0 Treffer (keine Captures) |
| CC-MAIN-2019-09 | FEHLER FAILED |
| CC-MAIN-2019-04 | FEHLER FAILED |
| CC-MAIN-2018-51 | FEHLER FAILED |
| CC-MAIN-2018-47 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-43 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-39 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-34 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-30 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-26 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-22 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-17 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-13 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-09 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2018-05 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-51 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-47 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-43 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-39 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-34 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-30 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-26 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-22 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-17 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-13 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-09 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2017-04 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-50 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-44 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-40 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-36 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-30 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-26 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-22 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-18 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2016-07 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-48 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-40 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-35 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-32 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-27 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-22 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-18 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-14 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-11 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2015-06 | NICHT GEPRUEFT (IP-Block) |
| CC-MAIN-2014-52 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-49 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-42 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-41 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-35 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-23 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-15 | 0 Treffer (keine Captures) |
| CC-MAIN-2014-10 | 0 Treffer (keine Captures) |
| CC-MAIN-2013-48 | 0 Treffer (keine Captures) |
| CC-MAIN-2013-20 | 4 Treffer |
| CC-MAIN-2012 | 84 Treffer |
| CC-MAIN-2009-2010 | 74 Treffer |
| CC-MAIN-2008-2009 | 0 Treffer (keine Captures) |

Fehlgeschlagene Abfragen (Serverfehler/Timeout): CC-MAIN-2018-51, CC-MAIN-2019-04, CC-MAIN-2019-09

## Nicht geprueft

Diese Indizes konnten nicht abgefragt werden, weil `index.commoncrawl.org` die Verbindung
nach der grossen Anfrageserie voruebergehend sperrte (IP-Block, "Could not connect ... after 21s").
`https://data.commoncrawl.org` (WARC-Host) blieb erreichbar. Es handelt sich ausschliesslich um
Indizes aus 2015-2018, in denen die Domain bereits geparkt/abgeschaltet war:

CC-MAIN-2018-47, CC-MAIN-2018-43, CC-MAIN-2018-39, CC-MAIN-2018-34, CC-MAIN-2018-30, CC-MAIN-2018-26, CC-MAIN-2018-22, CC-MAIN-2018-17, CC-MAIN-2018-13, CC-MAIN-2018-09, CC-MAIN-2018-05, CC-MAIN-2017-51, CC-MAIN-2017-47, CC-MAIN-2017-43, CC-MAIN-2017-39, CC-MAIN-2017-34, CC-MAIN-2017-30, CC-MAIN-2017-26, CC-MAIN-2017-22, CC-MAIN-2017-17, CC-MAIN-2017-13, CC-MAIN-2017-09, CC-MAIN-2017-04, CC-MAIN-2016-50, CC-MAIN-2016-44, CC-MAIN-2016-40, CC-MAIN-2016-36, CC-MAIN-2016-30, CC-MAIN-2016-26, CC-MAIN-2016-22, CC-MAIN-2016-18, CC-MAIN-2016-07, CC-MAIN-2015-48, CC-MAIN-2015-40, CC-MAIN-2015-35, CC-MAIN-2015-32, CC-MAIN-2015-27, CC-MAIN-2015-22, CC-MAIN-2015-18, CC-MAIN-2015-14, CC-MAIN-2015-11, CC-MAIN-2015-06

## Was Common Crawl stattdessen enthaelt

Crawl **CC-MAIN-2009-2010** (= `crawl-002`, 2010) hat die HTML-Seiten des alten Spiels:
index.php, anleitung.php, anmeldung.php, login.php, regeln.php, screens.php, wallpaper.php,
hintergrundgeschichte.php, links.php, ruhmeshalle.php sowie das Forum unter forum.nebelseetal.de.

Die Seite `screens.php` (Original-URL http://www.nebelseetal.de/screens.php, CC-Zeitstempel
20100310002533) verweist im HTML auf genau diese Bilddateien:

- `bilder/screens/siedlung.jpg`
- `bilder/screens/lager.jpg`
- `bilder/screens/portal.jpg`
- `bilder/screens/profil.jpg`
- `bilder/screens/thumb_siedlung.jpg`
- `bilder/screens/thumb_lager.jpg`
- `bilder/screens/thumb_portal.jpg`
- `bilder/screens/thumb_profil.jpg`

`wallpaper.php` verweist auf `bilder/wallpaper/wallpaper.jpg`, `wallpaper_wide.jpg`, `thumb1.jpg`, `thumb2.jpg`.
Diese Bilddateien sind **nicht** im Common-Crawl-Index vorhanden (nie gecrawlt).

### Beleg-Records (WARC/ARC-Koordinaten)

| Original-URL | CC-Index | ARC/WARC-Datei | Offset | Laenge | CC-Zeitstempel |
|---|---|---|---|---|---|
| http://www.nebelseetal.de/screens.php | CC-MAIN-2009-2010 | crawl-002/2010/04/02/23/1270218670229_23.arc.gz | 92879327 | 2549 | 20100310002533 |
| http://www.nebelseetal.de/wallpaper.php | CC-MAIN-2009-2010 | crawl-002/2010/04/02/23/1270218670229_23.arc.gz | 92881876 | 2338 | 20100310002504 |
| http://www.nebelseetal.de/index.php | CC-MAIN-2009-2010 | crawl-002/2010/09/24/35/1285397931522_35.arc.gz | 66849249 | 3072 | 20100903185349 |

Die aus diesen Records extrahierten HTML-Seiten liegen als Beleg in:
`docs/original/karten/commoncrawl/`

## Klare Negativ-Aussage

- Siedlungskarte (`bilder/screens/siedlung.jpg`): **NICHT in Common Crawl**.
- lager.jpg / portal.jpg / profil.jpg: **NICHT in Common Crawl**.
- wallpaper.jpg / wallpaper_wide.jpg: **NICHT in Common Crawl**.
- Ueberhaupt keine Bilddatei der Domain in Common Crawl (128 Indizes, 86 geprueft).
