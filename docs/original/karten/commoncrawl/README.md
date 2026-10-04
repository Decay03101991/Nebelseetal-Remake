# Common Crawl — Funde für Nebelseetal.de

**In diesem Ordner liegen KEINE Bilder** — Common Crawl hat keine einzige Bilddatei
der Domain archiviert (Details: `../QUELLEN_COMMONCRAWL.md`).

Stattdessen als Beleg abgelegt: die von Common Crawl gespeicherten **HTML-Seiten**
des alten Spiels (Crawl `CC-MAIN-2009-2010`), aus denen hervorgeht, welche Bilddateien
die Seite damals einband (u. a. `bilder/screens/siedlung.jpg`).

| Datei | Original-URL | ARC-Datei / Offset / Länge | CC-Zeitstempel |
|---|---|---|---|
| `cc_2009_CRAWL_CC-MAIN-2009-2010_www.nebelseetal.de_screens.php.html` | http://www.nebelseetal.de/screens.php | `crawl-002/2010/04/02/23/1270218670229_23.arc.gz` @ 92879327, 2549 | 20100310002533 |
| `cc_2009_CRAWL_CC-MAIN-2009-2010_www.nebelseetal.de_wallpaper.php.html` | http://www.nebelseetal.de/wallpaper.php | `crawl-002/2010/04/02/23/1270218670229_23.arc.gz` @ 92881876, 2338 | 20100310002504 |
| `cc_2009_CRAWL_CC-MAIN-2009-2010_www.nebelseetal.de_index.php.html` | http://www.nebelseetal.de/index.php | `crawl-002/2010/09/24/35/1285397931522_35.arc.gz` @ 66849249, 3072 | 20100903185349 |
| `cc_2009_CRAWL_CC-MAIN-2009-2010_forum.nebelseetal.de_index.php.html` | http://forum.nebelseetal.de/index.php | `crawl-002/2010/09/24/26/1285388250075_26.arc.gz` @ 55157984, 5122 | 20100906012047 |

Abruf erfolgte per HTTP-Range von `https://data.commoncrawl.org/<ARC-Datei>`, entgzippt,
ARC-Kopf abgetrennt. **Kein Bildinhalt abgelegt, weil kein Bildtreffer existierte.**
