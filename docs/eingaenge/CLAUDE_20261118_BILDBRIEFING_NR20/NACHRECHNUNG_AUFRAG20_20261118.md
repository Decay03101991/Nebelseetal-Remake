# Nachrechnung der Antwort auf Auftrag Nr. 20 (18.11.2026, Sitzung 49)

**Gegenstand:** `CLAUDE_ANTWORT_AUFTRAG20_BILDBRIEFING.md` (27.326 Byte, sha256
`d637f04ab736d4598f885ed499de345e6c73ccabc1fa4e58b9d6755edfcd6144`) - Claudes Bildbriefing fuer die
18 Dezember-Dateien.

**Regel:** jede Zahl wird nachgerechnet, BEVOR gebaut wird. Diese Datei haelt fest, was von Claudes
Befunden und Widerspruechen **bestaetigt**, was **widerlegt** und was **offen** ist. Nichts davon ist
gebaut.

**Stand der Anhaenge (hashgeprueft am 18.11.2026):** die drei Chat-Anhaenge sind **hashgleich** mit den
abgelegten Fassungen - Auftrag `.txt` (`450f829998500c6b...`), Paket `.zip` (`2c5cf6665c898d02...`),
Antwort (oben). Der Desktop ist geraeumt (14 Eintraege, kein Auftrag und keine Antwort mehr darauf).

---

## 1. Bestaetigt (eigene Messung, Datum 18.11.2026)

| Punkt | Claudes Aussage | Meine Messung | Urteil |
|---|---|---|---|
| **D1** Haltung des Drachen | `drache_weiss.png` zeigt keinen ruhenden Drachen, sondern einen aufgerichteten, bruellenden auf einem Eissockel | Bild angesehen: **aufgerichtet, Kopf hochgelegt, Maul weit offen, Fluegel ausgebreitet, Sockel aus Eiskristallen auf dunkler Platte** | **BESTAETIGT.** Mein Listentext „ruhender Drache, gleiche Haltung wie drache_weiss“ widerspricht sich selbst - das Wort „ruhend“ faellt weg (kommt aus Claudes Nr. 19) |
| **Befund 3 / D3** Bandbreite der Kachelrahmen | Ruhe 6-7 px von 64 (etwa 10 Prozent), Auswahl 6 px Kern plus Gluehen | Alpha-Spalte gemessen (mittlere Zeile, erstes deckendes Pixel bis zurueck zu durchsichtig): **Ruhe 8 px = 12,5 Prozent**, **Auswahl 10 px = 15,6 Prozent** bei 64 px | **BESTAETIGT und praezisiert** - nicht 10 Prozent, sondern 12,5 und 15,6 Prozent. „3 Prozent“ aus Nr. 19 ist damit in beiden Fassungen falsch |
| **D4** Band des Weltkartenrahmens | 3,5 Prozent = 129 px statt 3,35 Prozent | `kachelrahmen_chris.png` (400 x 400) gemessen: **Band 15 px von 400 = 3,75 Prozent** -> bei 3680 px sind das **138 px** | **DRITTE ZAHL:** weder 3,35 (Kommentar) noch 3,5 (Claude) noch 3 Prozent. Es gilt **3,75 Prozent = 138 px** |
| **D6** Zwei verschiedene Ladebilder | Das Ladeschild `LADEBILD_PNG` und der Ladehintergrund `STARTBILD_MOTIVE` sind zwei Dateien | `assets/loadingpage/Nebelseetal_Loadingpage.png` **455 x 320, RGB** (Schild); `STARTBILD_MOTIVE['anmelden']` **813 x 324**; `STARTBILD_MOTIVE['laden']` **1100 x 640** | **BESTAETIGT.** B5a/B5b ersetzen die **Hintergruende**; das Schild bleibt. Mein Listentext bei B5 spricht sonst von einer Datei zu viel |
| **Anmerkung 4** fehlende Wappen | `wappen_04`, `_10`, `_02` messen, dann haben drei Kopfbänder HEX-Werte | selbst gemessen (deckende Pixel, 160 px, 32er-Stufen): `wappen_02` (269 x 432) **#000000 13 % / #402040 7 % / #402060 7 %** (violett); `wappen_04` (313 x 424) **#200000 13 % / #600000 13 % / #a06020 6 %** (rot mit Gold); `wappen_10` (301 x 420) **#202020 14 % / #000000 13 % / #604020 6 % / #a08040 3 %** (grau-schwarz-gold) | **ERLEDIGT** - die drei Luecken sind geschlossen |
| **Anmerkung 6** Rahmen selbst messen | `kachelrahmen_chris.png` am Bild vermessen | siehe D4: Band **15 px**, Radius noch offen | **Halb erledigt** - das Band ist gemessen, der Radius nicht |

---

## 2. Nicht bestaetigt

| Punkt | Claudes Aussage | Meine Messung | Urteil |
|---|---|---|---|
| **Befund 2 / D12** `burg_05` gehoert zu den Elfen, die Zuordnung sei vertauscht | `burg_05.png` ist eine Baumburg mit Blatt-Banner - das sei die Elfenburg, zugeordnet aber Schattenfaust | `burg_05` angesehen: **Baumburg, gruenes Blatt-Banner, zwei Wasserfaelle** (stimmt). Aber: die Zuordnung vom 13.11. folgt den **gemessenen Farben** - `burg_05` ist gruen/schwarz/gold (`#404020`, `#204000`, `#604020`) und passt damit zur Farbe des Hauses Schattenfaust. `burg_03` ist weiss-gold mit **achtstrahligem Stern-Banner** und liegt richtig bei Sternenwacht. Die sechs Burgen in Farbe: 01 grau/ocker, 02 sand/rot, 03 weiss-gold, **04 dunkelblau/violett (20 Prozent)**, 05 gruen/oliv, 06 eisblau/weiss | **NICHT BESTAETIGT.** Kein Farbwiderspruch, kein belegbarer Tausch. Was bleibt, ist eine **Stilfrage**: eine Baumburg fuer die Trolle. Das ist **Daniels Wort**, keine Messung - steht als offener Punkt in der Uebergabe |

---

## 3. Offen (braucht Arbeit oder Daniels Wort)

| Punkt | Was fehlt | Wer |
|---|---|---|
| **D5** | `docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md` Zeilen 40/41 und 88-90 sagen noch „16“ und „F4 offen“ | **Arbeit** (Dokument nachziehen) |
| **D7** Format der Kopfbänder | Liste sagt „JPG oder PNG“, die Zielpfade enden auf `.png` | **Arbeit**: eine Endung festlegen (Claudes Vorschlag `.jpg` q92 aus Groessengruenden ist plausibel, aber [a] - nicht gemessen) |
| **D8** Goldrahmen im Marktplatz-Kennzeichen | Der Bestand hat einen eingebauten Rahmen; meine Regel „keine Rahmen im Bild“ wuerde Chris' Zeichen veraendern | **Daniel** |
| **D9, D10** | Freisteller gegen deckend (B13), Hauptmotiv links bei allen Kopfbändern | **Arbeit**: Liste an Claudes Vorschlag anpassen (deckend, Motiv links - beides deckt sich mit dem Bestand) |
| **D11** Kopfband Flickwerk | F-105 sagt Eisblau/Weiss/Messing, die Datei `wappen_05` zeigt Marineblau `#103050` und Grau `#505050` | **Daniel** |
| **D13** | Zielname `portal_kopfband_schmiede_dorf_ghule_4508x868.png` traegt noch das alte Motiv im Namen | **Arbeit** (Name vereinheitlichen, ohne Wirkung auf das Spiel) |
| **Anmerkung 2** Alpha am Farbtyp | Meine Wache liest PNG-Farbtyp 6 als „mit Alpha“ - auch wenn alle Pixel deckend sind. Fuer `alpha: false` muss der Export Farbtyp 2 sein | **Arbeit**: Wache um den Farbtyp erweitern, Wache + Sammellauf |
| **Anmerkung 3** Seitenverhaeltnis | Die Wache prueft nur Mindestmasse; 200 x 176 bestuende „mindestens 176 x 176“ | **Arbeit**: Seitenverhaeltnis pruefen (1:1 bei B1/B2/B9/B10/B13, 64:45 bei B5, 4508:868 bei B8, je +-1 px) |
| **Anmerkung 5** Speicher-Nebenfenster | Zeigt es das Ladeschild oder den Ladehintergrund? | **Arbeit** (Code lesen, eine Stelle) |

---

## 4. Was das fuer das Briefing bedeutet

Claudes Antwort ist als **Zuarbeit brauchbar**: die drei Befunde am Bestand sind (bis auf die
Zuordnungs-Vermutung) durch eigene Messung gedeckt, die 18 Bildauftraege mit Prompt und die
Zehn-Sekunden-Pruefungen sind unmittelbar verwendbar, und die zwei Einschaetzungen zu meinen Fragen
(Drache 176 x 176 quadratisch, B5 = 4 x Anzeige) sind **sachlich richtig** begruendet.

**Vor der naechsten Fassung zu korrigieren:** „ruhend“ beim Drachen streichen (D1), Bandbreiten auf die
gemessenen Werte setzen (Ruhe 12,5 Prozent, Auswahl 15,6 Prozent, Weltkartenrahmen 3,75 Prozent),
B5 als **Hintergrund** schaerfer abgrenzen (das Schild bleibt), die drei gemessenen Wappenfarben
einsetzen, Format auf **eine** Endung festlegen, und die zwei Werkzeugluecken (Farbtyp, Seitenverhaeltnis)
vorher schliessen, damit die Abnahme stimmt.
