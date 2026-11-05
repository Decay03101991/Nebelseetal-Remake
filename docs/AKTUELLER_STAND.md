# STAND 05.11.2026, 03:06 - Drachen-Nachtraege eingebaut (Register 205)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Sechs Nachrichten Daniels, sechs Aenderungen - alle geprueft.** Der Sieg gegen einen Drachen
bringt jetzt **34.000 Mana**: 4000 pauschal plus der Aufwand von drei Versuchen mit je zwei
Weltenspruengen, gerechnet aus dem ECHTEN Preis eines Sprungs (aendert der sich, zieht die
Belohnung mit - mit Wache belegt). Die Wache des Drachen bleibt **beschaedigt** stehen, ein
zweiter Angriff trifft weniger Verteidiger. Ein **Flammenzeichen** unter der Figur sagt nur,
dass schon jemand angegriffen hat, und verschwindet, wenn der Hort leer ist. **Bots** beurteilen
den Drachen mit Sicherheitsmarge, kennen Bonus und sichere Verluste, aber nicht die Wache.
Die **Ruine bleibt pluenderbar** (kein zweites Gefecht) und **sperrt danach ihre Koordinate**.
Jeder **Neubeginn** wuerfelt neue Plaetze auf denselben Welten.

**Belegt:** `tests/test_drachen_einhaengung.py` **96 bestanden, 0 Fehler** mit den Wachen
(a)-(i); Anzeige- und Bot-Texte durch die Umlaut-Wache (49/0). Voller Sammellauf: **165 von 167 gruen, 0 rot, 1450 s, 6.868 Pruefungen**
(`docs/audits/sammellauf_20261105_0310_voll.log`).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Drachen-Nachtraege (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_drachen_einhaengung.py` 96/0/0 | Testlauf |
| Voller Sammellauf (Projekt-venv) | 165 von 167 gruen, 0 rot, 1450 s, 6.868 Pruefungen | `docs/audits/sammellauf_20261105_0310_voll.log` |
| Register / Protokoll | 205 Zeilen / 331 Zeilen | `grep -cE '^\| [0-9]+ \|'`, `wc -l` |
| Guthaben (Daniel 02:48) | 5,77 USD Stand / 54,22 USD Gesamtverbrauch | Ablesung |
| Recherche | `docs/RECHERCHE_SPIELMECHANIKEN_20261105.md` (14 Vergleiche, 3 Vorschlaege) | Dokument |

## Der EINE naechste Schritt

1. **W-15 Haeuser:** Hausnamen und Wappenbeschreibungen auf die gelieferten Bilder umschreiben.
2. **Drachenschuppe als eigene Ware und Trophae** (Daniel 05.11.2026: eigene Auszeichnung,
   zaehlt am Ende nur als Trophae) - eigener Schritt mit Lagerfach und Anzeige.
3. **Die drei Recherche-Vorschlaege** pruefen (Erwartungswert im Bot-Urteil, zweite Kampfphase,
   Regeneration oder erneutes Erwachen) - erst nach Balancing-Messung, Entscheidung Daniel.
4. **Mini-Repo fuer das Protokoll** (Register 202) mit der VOLLEN Historie, lueckenlos.

Arbeitsweise unveraendert: **voller Sammellauf mit dem Projekt-venv**, Registerzeile und
Protokollzeile gehoeren zum Abschluss, Kommentarregel Variante A bei jedem neuen Code.

---
# STAND 05.11.2026, 01:52 - W-14 Teil 2 gebaut: die Drachen stehen im Spiel (Register 204)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Drachen sind verdrahtet.** W-14 Teil 1 hatte nur das Modul gebaut; jetzt haengen acht
Andockstellen daran: der Zustand (besiegte Drachen und ihre Horte im Spielstand), die Zielwahl
ueber den EINEN Angriffsweg, die Vorrunde gegen **Drachenwerte statt eines Walls** (Fusstruppen
700, Belagerung 950, unbrechbar), der **Feueratem** (8 Prozent der antretenden Fusstruppen,
eigene Berichtszeile), der Kampf gegen 204 Verteidiger, der **Beuteanteil nach Leistung** (letzter
Schlag +10 Prozent, ueber die EINE Buchstelle und begrenzt durch die Karrenladung), der eigene
**Bericht** (ohne Ueberlebende nur eigene Verluste und die Zahl der Verteidiger, kein Ausspaehen)
und die **Anzeige** als Figur je Drache, nach dem Sieg als Ruine.

**Belegt:** `tests/test_drachen_einhaengung.py` **76 bestanden, 0 Fehler** - mit allen sieben
Pflicht-Wachen der Uebergabe (Angriff unter der Schwelle kaempft nicht, Feueratem gebucht und im
Bericht, Beute genau einmal und nur der Anteil, ohne Ueberlebende keine Einheiten, kein
Ausspaehen, nach dem Sieg Ruine ohne zweiten Angriff, alter Spielstand laedt) und einer ECHTEN
Zeichnung der Portal-Ansicht. **Voller Sammellauf: 165 von 167 gruen, 0 rot, 1226 s**, 6.848 Pruefungen,
56 Befunde, kein Fehler.

**Zwei ehrliche Befunde:** der erste Entwurf liess den Drachen stehen, obwohl das Gefecht
gewonnen war - Massstab ist jetzt `kampfbericht.ausgeraeumt` (dieselbe Lesart wie W-13, weil
fliehende Verteidiger im Ort bleiben). Und der erste Sammellauf lief mit dem Hermes-Python und
meldete eine rote Datei (`test_gpt_originalkarten_historische_info`), weil dort `lxml` fehlt -
ein Geraetefehler, kein Spielfehler. Der Sammellauf gehoert mit `.venv/Scripts/python.exe`
gefahren, dann ist er gruen und rund 3 Minuten schneller.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | W-14 Teil 2 (dieser Commit) | `git log --oneline -1` |
| Neue Wache | `tests/test_drachen_einhaengung.py` 76/0/0 | Testlauf |
| Voller Sammellauf | 165 von 167 gruen, 0 rot, 1226 s, 6.848 Pruefungen | `docs/audits/sammellauf_20261105_0132_voll.log` |
| Pruefdateien / Module | 167 / 58 | `ls tests/test_*.py \| wc -l`, `ls src/*.py` |
| Register / Protokoll | 204 Zeilen / 324 Zeilen | `grep -cE '^\| [0-9]+ \|'`, `wc -l` |
| Guthaben (Daniel 01:25) | 6,13 USD Stand / 53,86 USD Gesamtverbrauch | Ablesung |

## Der EINE naechste Schritt

1. **W-15 Haeuser:** Hausnamen und Wappenbeschreibungen auf die gelieferten Bilder umschreiben.
2. **Kampfregeln 2, 4, 6** aus `cache/scratch/w13b_kampfregeln_entwurf.md` (Flucht unter 50
   Prozent, Wurf gegen 40 + 5 x Sequenz, Beute-Reihenfolge Gold zuerst, Mauerreparatur).
3. **Story-Einbau:** Chronik-Kapitel in `data/story.json` (Entwurf liegt im Scratch).

Arbeitsweise unveraendert: **voller Sammellauf mit dem Projekt-venv**, Registerzeile und
Protokollzeile gehoeren zum Abschluss, Kommentarregel Variante A bei jedem neuen Code.

**Offen bei Daniel (eine Runde am Abschluss):** welche DREI Welten die Drachen bekommen
(Vorschlag d02/d03/d05), ob die Drachenschuppe ein Lagerfach bekommt, ob der Rest des Hortes mit
dem Drachen verfallen soll (so ist es jetzt) und die Verdichtung des Protokolls.

---
# STAND 05.11.2026, 00:05 - W-13 gebaut (Gesamtsieg mit Endlosspiel), W-14 Teil 1 liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Gesamtsieg existiert jetzt im Spiel.** Daniel hat ihn am 04.11. definiert (Register 197): erreicht,
wenn jeder Bot und ALLE seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt wurden. W-13 setzt
das um: je ausgeraeumtem Dorf eine Buchung (`BotDorf.ausgeraeumt_seit`, gesetzt im EINEN Kampfweg
`GameState.kampf_am_ziel`), eine Auswertung in `punkte.gesamtsieg` und EINE Glueckwunschnachricht mit
fraktionsangepasster Geschichte aus `data/story.json` (sieben Texte, von `deepseek-v4-pro` geschrieben).
**Der Sieg beendet nichts** - `spielende` bleibt leer, die Spieluhr laeuft weiter (Endlosspiel).

**Echter Fehler dabei gefunden und behoben:** die Verluste des Verteidigers wurden bei einem Bot-Dorf NIE
gebucht. Der Block las `bot_ziel.army` - eine BERECHNETE Summe - und buchte in eine Kopie; gemessen: drei
Verluste im Bericht, Heer danach unveraendert sechs. Jetzt verteidigt die Garnison des angegriffenen
Dorfes (zweiter Teil von B-5), gebucht wird dort; ohne Dorf bucht `bot_armee_buchen`.

**W-14 Teil 1 liegt bereit, ist aber NICHT verdrahtet:** Daten, Modul und Pruefdatei fuer die Drachen (`test_drachen` 88/0/0). **Daniel hat am 05.11. die Verteidigung neu bestimmt:** deutlich mehr Einheiten - **120 Krieger + 60 Bogenschuetzen + 24 Paladine = 204** - und **statt eines Walls eigene Drachenwerte**: Schwelle Fusstruppen 700, Schwelle Belagerung 950, **unbrechbar** (Belagerung richtet keinen Wallschaden an), dazu ein **Feueratem** mit 8 % Verlusten unter den antretenden Fusstruppen. Die drei Drachenfiguren von Daniel sind freigestellt (weiss, blau, lila).

**Nachtrag 05.11.2026 (Daniel) - Drachen sind NUR Verteidiger:** keine Doerfer, ein starker Gegner mit vielen
Truppen und viel Beute. **Beuteanteil nach Leistung** (Variante A: jeder Angriff bucht seinen Anteil nach
zerstoerten Verteidigern, letzter Schlag +10 %) statt "letzter Schlag nimmt alles". **Transport wird
vorgerechnet** (`transport_bedarf`, `transport_text`), was nicht getragen wird bleibt liegen. **Epische Berichte,
aber ehrlich:** mit Ueberlebenden genaue Einheiten, ohne Ueberlebende nur eigene Verluste und die ZAHL der
Verteidiger. **Kein Ausspaehen** (`spionage_erlaubt` = False), dazu `angriffs_hinweis` und ein Satz in der Hilfe.


| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Code-Stand `9fc4138` (W-13), darauf W-14 Teil 1 und die Doku-Commits | `git log --oneline` |
| Voller Sammellauf | **163 von 165 gruen, 0 rot, 1433 s**, 6.684 Pruefungen, 55 Befunde (die zwei uebrigen sind dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261104_2327.log` |
| Neue Wachen | `test_gesamtsieg` **47/0/0**, `test_drachen` **88/0/0** | eigene Laeufe |
| Register / Protokoll | **203** / **321 Zeilen** (eine ueber Ziel - Verdichtung offen, siehe unten) | `grep -c`, `wc -l` |
| Kosten grosse Modelle (Monat) | **0,4342 USD von 1,94 USD am 04.11.** (Anbieter-CSV, 10 Anfragen); November 01.-04. insgesamt 18,0858 USD (flash 13,4376 / v4-pro 4,6482); 5,00 USD Reserve fuer `deepseek-flash` unangetastet (Ablesung 23:56: 6,56 / 53,43 USD). Eigene Textlaeufe 0,1746 USD - Schaetzpreise waren 3- bis 10-fach zu niedrig, es gilt nur die CSV |
| Veroeffentlicht | Stand von `main` als Entwicklungsschritt gepusht: `63639d5`, **ohne neue EXE** - die Testversion 0.5.0-pre.1 bleibt | `git push origin pre-release:main`, `origin/main` geprueft |
| Figuren | `assets/bilder/drache_weiss.png`, `drache_blau.png`, `drache_lila.png` (256 px + 64 px); Originale unter `archiv/eingaben/20261104_drachenbilder/` | Register 201 |

## Der EINE naechste Schritt

**W-14 Teil 2: die Drachen ins Spiel bringen.** Zu verdrahten sind (a) die Kartenanzeige - kleine
Drachenfigur statt Burg, nach dem Sieg die **Ruine** (Daniel 04.11.2026: je Spielstand und Karte; das
Ruinenbild modelliert Daniel selbst, bis dahin Platzhalter), (b) die Zielwahl im Angriffsweg, (c) der Kampf
ueber `kampf.fuehre_schlacht` mit `drachen.verteidiger`/`drachen.wall`, (d) die Beute ueber die EINE
Buchstelle `kampfbericht.beute_am_ziel` (Vorschlag: um `beute_override` erweitern), (e) der Zustand
`drachen_besiegt` in `GameState.save/load`. Der Einbauplan mit Zeilenlagen liegt in
`docs/ENTWURF_W14_TEIL2_20261105.md` - **vor dem Bau entscheidet Daniel zwei Dinge:** welche DREI Welten
`docs/ENTWURF_W14_TEIL2_20261105.md` - **vor dem Bau entscheidet Daniel nur noch EINE Sache:**
welche DREI Welten (Vorschlag d02, d03, d05). Die **Verteidigung ist entschieden** (204 Einheiten,
Drachenwerte statt Wall, Feueratem). **Arbeitsweise: der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss.**
**Offene Punkte, die nicht untergehen duerfen:** (1) Farben der Drachenfiguren - Daniel: erstmal unwichtig,
spaeter anpassen; die Chronik nennt Episheus weiss / Tardas gruen / Salmur rot, geliefert sind weiss, blau,
lila. (2) Das Protokoll steht mit **321 Zeilen** eine Zeile ueber Ziel; die Verdichtung ist ein eigener
Schritt (Vorgaengerzeilen werden nicht nachts nebenbei zusammengelegt). (4) **Eigenes Mini-Repo fuer das Entwicklungsprotokoll** ist beauftragt und auf spaeter gelegt (Register 202); (3) Zwei Skill-Abschnitte warten in
der Freigabe-Liste (`18381d56`).

# STAND 04.11.2026, 22:00 - W-12 gebaut (sechs Welten), alle sechs Welten bespielbar, fuenf Antworten eingearbeitet

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das Spiel fuehrt sechs Welten, und alle sechs sind bespielbar.** Die 14 leeren
Platzhalter-Dimensionen (d07 bis d20) sind entfernt; die sechs belegten Weltkarten (d01 Armageddon,
d02 Ragnaroek, d03 Utgard, d04 Midgard, d05 Valhalla, d06 Limbus) tragen ihre alten Kennungen, **alte
Spielstaende laden unveraendert**. Alle Textstellen, die 20 Dimensionen behaupteten, nennen jetzt sechs
Weltkarten - der Original-Stand bleibt als belegter Satz im Code, damit die Quellenlage nicht
verschwindet. **Die Frage "Limbus: Raum oder Welt?" brauchte keine Runde:** Register 98
(Daniel 01.11.2026) legt fest, dass "Limbus" Weltname bleibt und die Ebene "der magische Limbus"
heisst. **Nummernwiderspruch geradegezogen:** die Uebergabe nannte den Schnitt W-6; W-6 ist seit dem
03.11. der Nur-Lese-Blick in fremde Welten (Register 166). Der Schnitt heisst **W-12**.

**Daniel hat die fuenf offenen Fragen beantwortet** (Register 197, Wortlaut dort): Sieg ist ab jetzt
definiert (jeder Bot und alle seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt, danach
Endlosspiel und eine fraktionsangepasste Glueckwunsch-Nachricht); Drachen kommen zurueck, aber genau
einer je Karte in drei Welten, als Drachenfigur statt Burg, mit grosser Beute; Hausnamen und
Hausfarben werden uebernommen; **alle sechs Welten sind bespielbar** (sofort gebaut); die
Skill-Freigabe gilt nur fuer die Story-Schicht.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | Code-Stand `237c8ae`, darauf die Doku-Commits bis `93d104f` | `git log --oneline` |
| Limbus-Dimensionen | **6** (d01-d06), vorher 20 | `data/welten.json`, `portalraum.dim_zahl()` |
| Bespielbare Welten | **6 von 6** (vorher 2) | `data/welten.json` → `weltkarten_spielbar` |
| Register / Protokoll | **197** / **318 Zeilen** (Ziel 320, verdichtet aus 320) | `grep -c`, `wc -l` |
| Voller Sammellauf | **161 von 164 gruen, 0 rot, 1789 s**, 6.589 Pruefungen, 55 Befunde | `docs/audits/sammellauf_20261104_2123.log` |
| Einzeln nachgeholt | `test_produktionskette_ohne_cheats` **48/0/0 in 272 s** (im Lauf: Zeitlimit 420 s, kein Befund) | eigener Lauf |
| Umgestellte Pruefdateien | `test_welt` 43/0/0, `test_portalraum` 70/0/0, `test_portal_uebersicht` 61/0/0, `test_weltkarten_anzeige` 27/0/0, `test_weltbild_gelaende` 94/0/0 | Sammellauf |
| Unveraendert | 400 Felder je Weltkarte (20x20 Raster), 5.000 Mana/24 h Weltensprung, sechs Fraktionen mit Heimatwelten | `data/welten.json`, Register 164 |

## Der EINE naechste Schritt

**W-13: die Sieg-Auswertung bauen - der Gesamtsieg nach Daniels Definition.** Sieg heisst: **jeder Bot
und ALLE seine Doerfer wurden mindestens einmal laut Kampfbericht ausgeraeumt** (Register 197). Zu
bauen sind (a) eine Buchung je ausgeraeumtem Dorf im Kampfbericht-Weg (`src/kampfbericht.py`,
`src/auftraege.py`), (b) die Auswertung "sind alle Doerfer aller fuenf Bots erledigt" in `src/punkte.py`
neben E5, (c) die Glueckwunsch-Nachricht mit Fraktionsbezug, (d) **Endlosspiel danach**: der Sieg sperrt
nichts und beendet nichts. Der Storytext der Siegesnachricht ist ein EIGENER Teil (Modelllauf, Daniel
entscheidet vorher). **Arbeitsweise: der volle Sammellauf, die Registerzeile und die Protokollzeile
gehoeren zum Abschluss.** Das Protokoll wurde am 04.11. von 320 auf **318 Zeilen** verdichtet (drei
Bildcontent-Zeilen zu einer, zwei GitHub-Zeilen zu einer; Vorfassung unter
`docs/archiv/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261104.md`), **zwei Zeilen sind frei** - die
naechste Protokollzeile passt ohne neue Verdichtung.

**Danach in dieser Reihenfolge (von Daniel so entschieden):** die drei offenen Kampfregeln (2
Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit), dann **W-14 Drachen**
(eine Figur je Karte in drei Welten, Beute als VORSCHLAG 5.000 Gold, je 2.000 Holz/Stein/Nahrung und
eine Drachenschuppe, Zahlen in einer Datendatei), dann **W-15 Hausnamen und Wappenbeschreibungen**,
zuletzt der Story-Einbau aus `docs/CHRONIK_DER_WELT_20261104.md`.

# STAND 04.11.2026, 19:40 - Pre-Release 0.5.0-pre.1 veroeffentlicht, naechster Schritt W-6

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der erste Pre-Release ist draussen.** `v0.5.0-pre.1` liegt auf GitHub: Testversion
`Nebelseetal_Remake.exe` (81,8 MB, SHA256 `75c24cc5...`), Paket 81,6 MB mit EXE und vier Infodateien,
Repository oeffentlich, Besucherseite unter https://decay03101991.github.io/Nebelseetal-Remake/.
Der Start ist geprueft (Passworttor auf leerem Profil, danach Spieloberflaeche), der Anhang anonym
nachgeladen (85.516.122 Bytes, `testzip` sauber). Das Repo traegt **nur** Spielcode, Daten, Bilder und
die Veroeffentlichungsdokumente - keine Tests, keine Werkzeuge, keine Entwicklungsdokumente.
**Veroeffentlichungszweig ist `pre-release`, Entwicklung bleibt `main`; in `src`, `data`, `assets` sind
beide identisch.** Das Verfahren fuer spaetere Repo-Aenderungen steht in der Uebergabe 19:10, Abschnitt C.

**Zur Geschichte:** Die Chronik der Welt ist als Entwurf fertig (11.211 Woerter, elf Teile, Register 188),
dazu ein Gesamtbild zum Lesen mit Herkunft je Baustein und **sieben Widerspruechen** (Register 186). Der
groesste davon: das Spiel erzaehlt einen Sieg, den es nach E5 nicht gibt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf auf `main` | `6c58575` | `git log --oneline -1` |
| Veroeffentlichungszweig | `pre-release`, 595 Dateien, 76,6 MB | `git ls-tree -r pre-release` |
| Release | `v0.5.0-pre.1`, Pre-Release, Anhang 81,6 MB | GitHub-API |
| Register / Protokoll | **195** / 315 Zeilen | `grep -c`, `wc -l` |
| W-6 offen | 20 Dimensionen, 6 belegt, 14 leer | `data/welten.json` |
| Sammellauf 15:16 | 162 von 164 gruen, 0 rot, 1220 s | `docs/audits/sammellauf_20261104_1516.log` |
| Sammellauf 19:12 | **161 von 164, 1 rot** (`test_gpt_projektordnung`: `.gitignore` ohne `/archiv/`), 912 s | `docs/audits/sammellauf_20261104_1912.log` |
| Reparatur | `.gitignore` mit den Schutzregeln wiederhergestellt (Secrets, Spielstaende, `/archiv/`) plus Veroeffentlichungspakete; Datei danach gruen | Commit `6c58575` |
| Nachlauf nach der Reparatur | **162 von 164 gruen, 0 rot, 802 s** (2 dokumentiert zurueckgezogen, 6.677 Pruefungen, 55 Befunde) | `docs/audits/sammellauf_20261104_1921.log` |

## Der EINE naechste Schritt

**W-6: die 14 leeren Limbus-Dimensionen entfernen - das Spiel fuehrt sechs Welten.** `src/welt.py`
(`DIMENSIONEN`), `src/portalraum.py`, `auftraege.kosten_der_mission` (Mana je Dimensionsstufe), die
Portal-Ansicht und die Wachen `test_bot_welten`, `test_portalraum`, `test_portal_uebersicht` sind
betroffen; die sechs Fraktionen stehen in `data/welt_fraktionen.json`. **Vorher eine Entscheidung
klaeren:** Limbus ist im Handbuch der Raum, im Remake eine Welt mit Gnomen - Vorschlag: Limbus bleibt
Raum, die Gnome bewohnen feste Inseln darin. **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss.**

**Danach** die drei offenen Kampfregeln (2 Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6
Mauerreparatur mit Bauzeit), dann **C** (fliessende Ansichten); `main.py` zerlegen und Skill kuerzen
folgen nach der Story (Daniels Entscheidung).

---

# STAND 04.11.2026, 15:40 - Story 2: die fuenf Bots sprechen (Register 184)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die fuenf Nachbarn haben jetzt eine Stimme.** Der zweite Story-Teil ist gebaut: Haug, Brynhild, Grom,
Silra und Krank sagen zu Angriff, Verteidigung, Gruendung und Beute je ein bis zwei Saetze - Ton wie
Story 1 (abenteuerlich und leicht, kein Pathos). **Alle Texte stehen in `data/bot_stimmen.json`**, im
Code steht kein einziger davon (als Wache geprueft). Vier Meldungen des Spiels tragen die Stimme jetzt:
Angriff auf den Spieler, Verteidigung eines Bot-Dorfs (letzte Zeile des Kampfberichts), Dorfgruendung
eines Bots und der Raubzug Bot gegen Bot. Fehlt ein Eintrag, kommt der neutrale Satz aus der Datei -
nie ein Absturz, und der sachliche Bericht bleibt in jedem Fall stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_stimmen.py` **115/0/0** | eigener Lauf |
| Gegenprobe | Textnachschlag abgeschaltet: **43 Pruefungen rot** (115 auf 72), `src/stimmen.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Texte | 5 Bots x 4 Ereignisse x 2 Saetze = **40 Texte**, alle mit echten Umlauten | `data/bot_stimmen.json` |
| Anschluesse | `stimmen.mit_stimme` an drei Stellen (angriff, beute, gruendung), `stimmen.zeile` in `kampf_am_ziel` (verteidigung) | `src/main.py` |
| Rueckfall | unbekannter Bot, unbekanntes Ereignis, fehlende Datei = neutraler Satz bzw. leer, ohne Absturz | `tests/test_stimmen.py` Abschnitt 4 |
| Voller Sammellauf | **162 von 164 gruen, 0 rot, 6677 Pruefungen, 1220 s** (2 dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261104_1516.log` |
| Messapparat | zwei vorher rote Dateien waren Geraetefehler (lxml fehlte nach dem Laufzeitwechsel, `Tcl_Obj` in `cget`), beide repariert und einzeln gruen | Protokollzeile 16:1x |
| Pruefdateien / Register / Protokoll | **164** / **185** / **300 Zeilen** | `ls tests/test_*.py`, `grep -c`, `wc -l` |
| Modulkarte | **57 Dateien** (neu: `stimmen.py`) | `python tools/modulkarte_bauen.py` |
| Stand-Bloecke | **76** | `grep -c '^# STAND'` |

## Der EINE naechste Schritt

**W-6: die 14 leeren Limbus-Dimensionen entfernen - das Spiel fuehrt sechs Welten.** `src/welt.py`
(`DIMENSIONEN`), `src/portalraum.py`, `auftraege.kosten_der_mission` (Mana je Dimensionsstufe), die
Portal-Ansicht und die Wachen `test_bot_welten`, `test_portalraum`, `test_portal_uebersicht` sind
betroffen; die sechs Fraktionen stehen in `data/welt_fraktionen.json`. **Danach** die drei offenen
Kampfregeln (2 Fluchtformel, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit), dann **C**
(fliessende Ansichten); `main.py` zerlegen und Skill kuerzen folgen nach der Story (Daniels Entscheidung).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

**Zweiter, grosser Auftrag in eigener Sitzung: der GitHub-Neuaufbau.** Daniel hat den letzten Upload
zurueckgenommen und den Projektstand neu beurteilt; das Repository wird neu aufgebaut und als ERSTER
Pre-Release veroeffentlicht (Akte: `docs/AUFTRAG_GITHUB_PRE_RELEASE_20261104.md`, Register 185). Die
Inhaltsliste ist noch unvollstaendig - **bis dahin wird am Repo nichts geaendert.**

---

# STAND 04.11.2026, 11:15 - Story 1: das Spiel erzaehlt jetzt (Register 183)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der dritte Kernbefund der externen Pruefung ist bearbeitet: das Spiel hat eine Geschichte.**
Nach dem Laden erscheint einmalig ein Ingame-Dialog mit vier Saetzen (Weltbruch, fuenf Nachbarn,
Aufgabe), der Berater hat die Rubrik "Geschichte" mit einer Chronik, die mit dem Fortschritt von
einem auf sieben Kapitel waechst, und Sieg wie Niederlage haben eigene Texte. **Alle Texte stehen in
`data/story.json`** - im Code steht kein einziger Storytext, das ist als Wache geprueft.

Daniels Entscheidungen dazu (04.11.2026): Ton **abenteuerlich und leicht** (Variante B), EIN Intro
statt sechs Fassungen, Chronik im Berater, und in Story 2 sprechen die Bots (je ein bis zwei Saetze
fuer Angriff, Verteidigung, Gruendung, Beute).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_story.py` **38/0/0** | eigener Lauf |
| Gegenprobe | Merker abgeschaltet: **2 Pruefungen rot**, `src/story.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Texte | 4 Intro-Absaetze, 7 Chronik-Kapitel, Sieg und Niederlage - alle mit echten Umlauten | `data/story.json` |
| Chronik-Stufen | 0 Ankunft, 1 Siedlung, 2 Ware/Werkstatt, 3 Forschung, 4 Kampf, 5 zweites Dorf, 6 zweite Welt | `src/story.py: _stufe` |
| Ort des Intros | Ingame-Overlay nach dem Aufbau der Oberflaeche (kein `Toplevel`) | `main._geschichte_intro_zeigen` |
| Merker | `geschichte.json` neben dem Spielstand - Intro einmal je Installation | `story.intro_gesehen` |
| Modulkarte | 56 Dateien (neu: `story.py`) | `python tools/modulkarte_bauen.py` |
| Pruefdateien / Register | **163** / **183** | `ls tests/test_*.py`, `grep -c '^\| [0-9]'` |

## Der EINE naechste Schritt

**Story 2: die fuenf Bots sprechen.** Neue Datendatei `data/bot_stimmen.json` mit je ein bis zwei
Saetzen pro Bot und Ereignis (Angriff, Verteidigung, Gruendung, Beute, Spionage); die Meldungen des
Spiels nehmen den Text aus dieser Datei statt eines neutralen Satzes. Fertig ist der Schnitt, wenn
jede Bot-Meldung eine Stimme traegt, ein Bot ohne Eintrag weiterhin eine neutrale Meldung erzeugt
(kein Absturz) und eine Wache belegt, dass kein Text im Code steht. **Danach** die drei offenen
Kampfregeln (2, 4, 6), dann **C** (fliessende Ansichten); `main.py` zerlegen und Skill kuerzen folgen
nach der Story (Daniels Entscheidung). **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 04.11.2026, 10:45 - externe Projektpruefung verarbeitet (Register 182)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Ein fremdes Modell hat zum ersten Mal von aussen auf das Projekt geschaut** - auf Auftrag von Daniel,
mit einer Kostengrenze von 3 USD, ohne Dateizugriff (Daten nur als Text). Zwei Gutachten: Arbeitsweise
(13.791 Zeichen) und Spiel/Story/Code (10.037 Zeichen), zusammen 33.730 Token. **Der wichtigste Befund
ist gemessen und unangenehm:** 294 von 532 Commits (55 Prozent) aendern ausschliesslich Dokumente - die
Buchhaltung ist groesser als der Bau. Zweiter Befund: der Sammellauf kostet 9 bis 12 Minuten je
Code-Schnitt. Dritter: das Spiel hat kein Intro, ein Fremder findet keine Geschichte.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Gutachten | A 13.791 Zeichen, B 10.037 Zeichen, 33.730 Token, 287 s Modellzeit | `docs/PRUEFVERMERK_EXTERNE_PRUEFUNG_20261104.md` |
| Kernbefund 1 | **294 von 532 Commits aendern nur `docs/`** | `git log --pretty --name-only`, eigene Zaehlung |
| Kernbefund 2 | Sammellauf 162 Dateien, 9 bis 12 Minuten je Code-Schnitt | `docs/audits/` |
| Kernbefund 3 | kein Story-Intro im Code, nur Statuszeile und Beratertexte | `grep "Willkommen"` in `src/main.py` |
| Uebernommen | Teststufen smoke/kern/voll, Story 1 (Intro, Vorgeschichte, Siegtext), Story 2 (Bot-Stimmen, Fraktions-Kurztexte) | Pruefvermerk Abschnitt 2 |
| Abgelehnt (mit Grund) | Protokoll abschaffen, 20 Limbus-Dimensionen reduzieren, Kommentarpflicht abschaffen | Pruefvermerk Abschnitt 3 |
| Offen (Daniel entscheidet) | `main.py` zerlegen (13.479 Zeilen), Skill von 74.370 Zeichen kuerzen, Uebergabe zweiteilen | Pruefvermerk Abschnitt 5 |
| Pruefdateien / Register / Protokoll | **162** / **182** / **295 Zeilen** (Zielgroesse eingehalten) | `ls tests/test_*.py`, `grep -c '^\| [0-9]'`, `wc -l` |

## Der EINE naechste Schritt

**Teststufen fuer den Sammellauf** (der einzige Vorschlag der Pruefung, der sofort Zeit spart): eine
Stufe `smoke` fuer Dokument- und Daten-Aenderungen, `kern` fuer ein Modul und `voll` fuer Code-Schnitte,
ausgewaehlt nach den geaenderten Pfaden. Die Projektregel bleibt unangetastet: **ein Code-Schnitt gilt
nur mit vollem Lauf NACH dem letzten Fix**. Fertig ist der Schnitt, wenn es die drei Stufen gibt, eine
Wache belegt, dass `voll` weiter alle Pruefdateien faehrt, und ein Doku-Commit nachweislich unter drei
Minuten bleibt. Danach **Story 1** (Intro mit Weltbruch und Auftrag, Vorgeschichte, Siegtext).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes
Schnitts.**

---

# STAND 04.11.2026, 09:38 - S-12 und S-11: alle Felder, Kartenwahl nach Engpass (Register 180/181)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Schnitte in einem Zug, beide gemessen.** (1) **S-12:** der Huegel wird mitbelegt (Steinmetz,
dann Goldmine - beim Raecher Erzmine), und die Feldreserve fuer Haus, Bibliothek, Lager, Schmiede,
Akademie und Wall ist jetzt eine FELDLISTE statt einer Zahl. Der Unterschied ist gross: auf
`original-001` galten 19 freie Sumpffelder als erfuellte Reserve, danach fand kein Haus mehr Platz.
(2) **S-11:** die Kartenwahl waehlt nach dem ENGPASS der Taktik. Der Engpass wird gerechnet
(Bedarf eines Zyklus aus Siedlerkarren und Gruendung, geteilt durch den Ertrag der Mindestanlagen),
nicht geraten - Holz steht bei jeder Taktik vorn, Pferde sind mit vier Stueck gar kein Engpass.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wachen | `test_gesamtsieg` **47/0/0**, `test_drachen` **88/0/0** | eigene Laeufe |
| Gegenproben | Huegel-Fuellung aus **20 Pruefungen rot**; Taktik im Engpass ignoriert **5 rot**; beide Dateien per SHA256 unveraendert zurueck | eigene Laeufe |
| Voller Sammellauf | erster Lauf **157 von 162 gruen, 3 rot** (`sammellauf_20261104_0940.log`); nach dem Nachziehen der drei Wachen **160 von 162 gruen, 0 rot, 728 s**, 6.521 Pruefungen, 56 Befunde (`sammellauf_20261104_1000.log`) - die zwei nicht gruenen sind die ausgesetzten Dateien | `docs/audits/` |
| Messung 24 Spieltage | Dorfzahl **4/4/4/4/4** in beiden Schnitten; Anlagen je Dorf **63 bis 98** (vorher 52 bis 97) | `tools/bot_wirtschaft_messung.py` |
| Engpass-Paare | Pluenderer und Spaeherin holz/stein, Waechterin holz/wolle, Bastionier und Raecher holz/nahrung | `main.bot_taktik_engpass` |
| Pruefzusage S-11 | Pluenderer waehlt `original-006`, Waechterin `original-118b` bei DERSELBEN Kandidatenliste | `tests/test_s11_kartenwahl_engpass.py` |
| Bedarf eines Zyklus | 680 Holz, 550 Nahrung, 300 Stein, 150 Leder, 100 Wolle, 80 Metall, 4 Pferde | `spieloekonomie.gruendungskosten()` + `U["Siedlerkarren"]` |
| Schalter | `data/bot_wirtschaft.json`: `kartenwahl_stufe` = **engpass** (mittel/schwer/leicht bleiben waehlbar) | Datendatei |
| Pruefdateien / Register | **162** / **181** | `ls tests/test_*.py \| wc -l`, `grep -c '^\| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |
| Kampfregeln (gemessen) | **fuenf von acht stehen schon im Code** (1, 3, 5, 7, 8); offen: **2 Flucht, 4 Beute-Reihenfolge Gold zuerst, 6 Mauerreparatur mit Bauzeit** | `docs/AUDIT_KAMPFREGELN_20261104.md` |
| Offener Befund | Stein laeuft ueber (36.000 bis 61.000 je Bot), weil der Huegel nach Ertrag den Steinmetz traegt | `docs/MESSUNG_S12_ALLE_FELDER_20261104.md`, Abschnitt 3 |

## Der EINE naechste Schritt

**Das Entwicklungsprotokoll verdichten** (Daniels Antwort vom 04.11., 09:15: eigener Schritt nach
S-12, Zielgroesse unter 320 Zeilen). Verfahren nach Skill: die unveraenderte Fassung als eigene Datei
sichern und committen, die neue Fassung im Zwischenspeicher schreiben, mit
`tools/pruefe_protokoll.py --nach` pruefen (Rueckgabe 0), dann einsetzen - alle Commit-Kennungen und
Pruefzahlen bleiben erhalten. Danach die **acht Kampfregeln** in der Reihenfolge 1 bis 8
(`docs/ENTSCHEIDUNGEN_KAMPFREGELN_20261103.md`), dann **C** (Refresh fuer fuenf Ansichten).
**Der volle Sammellauf, die Registerzeile und die Protokollzeile gehoeren zum Abschluss jedes
Schnitts.**

---

# STAND 04.11.2026, 08:46 - S-8 Stufe 3: jede Bot-Taktik baut nach eigenem Plan (Register 179)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die fuenf Bots bauen nicht mehr alle dasselbe.** Bis heute setzte `bot_doerfer_bebauen` in jedem
Bot-Dorf dieselbe Zahl je Gebaeude (26 bis 30 Anlagen), unabhaengig von der Taktik - die Karte blieb
halb leer. Jetzt hat jede Taktik MINDESTZAHLEN und eine Restfeld-Regel in
`data/bot_bauplan.json` (`anlagen_bauplaene`): erst die Mindestzahlen in ihrer Zone (Phase A, in
Runden, damit eine Anlage nicht den ganzen Berg nimmt), dann die freien Felder nach Ertrag (Phase C).
Zwei Sperren halten den Plan gesund: **9 Felder bleiben fuer den Gebaeude-Bauplan frei** (Haus,
Bibliothek, Lager, Schmiede, Akademie, Diebesgilde, Bogenbauer, Wall - sonst faende `bot_dorf_bauen`
keinen Platz und es gaebe keine Forschung, keine Kaserne, keine Truppen), und **das letzte
Bibliotheksfeld** bleibt unangetastet, weil eine Bibliothek nur auf Grasland, Steppe oder Nebelsee
stehen darf.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_s8_stufe3_bauplaene.py` **98/0/0** | eigener Lauf |
| Voller Sammellauf | **159 von 161 gruen, 0 rot, 520 s**, 6.330 Pruefungen, 56 Befunde (Start 08:59; die zwei nicht gruenen sind die dauerhaft ausgesetzten Dateien) | `docs/audits/sammellauf_20261104_0900.log` |
| Gegenprobe | **40 Pruefungen rot** (Plan-Block abgeschaltet), `data/bot_bauplan.json` per SHA256 unveraendert zurueck | eigener Lauf |
| Messung 24 Spieltage | Dorfzahl **4/4/4/4/4**, Anlagen je Dorf **52 bis 97** (vorher 26 bis 30) | `tools/bot_wirtschaft_messung.py`, `s8s3_final.json` |
| Taktik-Profile | Raecher **39** Erzminen / 8 Goldminen, Spaeherin **31** Pferdezuchten, Waechterin **21** Steinmetze, Bastionier 31 Goldminen | Anlagenzahl je Dorf |
| Metall in der Kasse | **12.172 bis 55.832** (vorher 11.435 bis 16.584) | Messung |
| Daten | `anlagen_bauplaene` mit fuenf Taktiken, Restfeld-Reihenfolge je Gelaende, Holzfaeller-Deckel 6 | `data/bot_bauplan.json` |
| Belegte Ertraege | Jaeger **2 Nahrung + 2 Leder** auf Wald, Zuchten **3** auf Grasland, Farm **4 / 2** | `data/buildings.json` (gemessen, nicht getippt) |
| Nachgezogene Wachen | `test_bot_nahrung` **48/0/0**, `test_bot_dorf_als_ort` **42/0/0**, `test_bot_warenkette` **36/0/1** (BEFUND: Berg-arme Karte, 5 Bergfelder fuer 8 Anlagen) | eigene Laeufe |
| Pruefdateien / Register | **161** / **179** | `ls tests/test_*.py \| wc -l`, `grep -c '^\| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |
| Fragen dieser Sitzung | **4 gestellt, 4 entschieden** (04.11.2026, rund 09:15) - Zuordnung der Taktiken so lassen, Erzmine bleibt vorne, Protokoll nach S-12 verdichten, Metall-Abnehmer nach S-11 | `docs/FRAGEN_AN_DANIEL_20261104.md` (Abschnitt Antworten) |
| Kopf | Vorgaenger `78a6d0d`; der Commit mit diesem Block ist der neue Kopf | `git log --oneline -1` |

## Der EINE naechste Schritt

**S-12: alle Felder nutzen.** Der Bauplan fuellt heute die Gelaendearten Wald, Grasland, Berg und
Steppe; Huegel bleibt fuer die ertraglosen Gebaeude frei, Sumpf und Nebelsee tragen nichts. S-12
erweitert die Restfeld-Regel so, dass ein Bot-Dorf jedes Feld belegt, das seine Taktik sinnvoll
fuellen kann, und belegt die Pruefzusage aus dem Konzept: die Zahl der Anlagen ist von Karte zu Karte
VERSCHIEDEN (sie ist es seit heute schon - 52 bis 97 -, aber Huegel und Sumpf sind noch offen).
Danach S-11 (Kartenwahl mit Feldverstaendnis). **Der volle Sammellauf, die Registerzeile und die
Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

**Reihenfolge nach Daniels Antworten vom 04.11.2026 (rund 09:15):** S-12 -> Protokoll verdichten
(eigener Schritt, Zielgroesse unter 320 Zeilen; vorher die unveraenderte Fassung sichern und
committen) -> S-11 -> eigener Schnitt "Metall in Truppen" (Abnehmer fuer das gehortete Metall des
Raechers).

---

# STAND 03.11.2026, 23:2x - Weltkarte mit gemaltem Rahmen, Gelaendeton und Goldrand (Register 178)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Weltkarte sieht jetzt aus wie ein Kaestchen aus dem Original, nicht wie ein Farbgitter.** Um das
Gelaendekaestchen liegt der gemalte Kachelrahmen der C2-Lieferung als 9-Slice-Rahmen (Ecken fest, Kanten
gekachelt), die Felder tragen ihren Gelaendeton ohne harten schwarzen Umriss, das Gitter ist eine feine
dunkelbraune Trennlinie, und die Auswahl ist ein **Goldrand** statt eines blauen Kastens. Groesse und
Aufbau sind unveraendert: 400 x 400 px, 20 px je Feld, 10 x 10 Felder.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_weltkarte_rahmen.py` **32/0/1** | eigener Lauf |
| Gegenprobe | **6 Pruefungen rot** (Rahmen abgeschaltet, Goldrand zurueck auf Blau), `main.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Nachbarn | `test_marsch_optik` 63/0/0, `test_portal_fremdblick` 18/0/1, `test_spionage` 146/0/0, `test_weltbild_gelaende` 135/0/0, `test_portal_uebersicht` 61/0/0, `test_overlay_ingame` 42/0/1 | eigene Laeufe |
| Rahmen | vier Bildleisten, Ecke **pixelgleich** mit `kachelrahmen_ruhe.png`, Rand **16 px** | `gebaeude_optik.rahmen_kanten` |
| Gitter | **44** Linien in `#2b1a12` (vorher 400 Umrisse `#111111`) | `main.RASTER_LINIE` |
| Auswahl | `#ffcc33` (Skin-Gold) auf `#1b0d06`; der blaue Rand `#38BDF8` ist weg | `_render_portal` |
| Bild-Beleg | `C:/Users/saras/AppData/Local/hermes/cache/scratch/weltkarte_rahmen_beleg.png` (ganzer Schirm, Rahmen und Goldrand sichtbar) | eigener Lauf mit `.venv`-Python |

## Zwei Befunde vor dem Bau (gemessen, nicht geraten)

1. **Die Ressourcenleiste taugt NICHT als Rahmen.** In ihrem Band stehen acht Symbole und acht leere
   Zahlenschilde (`data/ressourcenleiste.json`, acht Felder); als Rahmen gedehnt waeren sie verzerrt.
   Daniel hat deshalb den **Kachelrahmen als 9-Slice-Rahmen** freigegeben. Ein breiter eigener
   Kartenrahmen bleibt eine Bildlieferung.
2. **Drei bestehende Wachen mussten ihren Anker verschieben**: die Zeichenflaeche sitzt jetzt in einem
   Traeger, deshalb suchen `test_portal_fremdblick`, `test_spionage` und `test_marsch_optik` sie im Baum
   statt nur unter den direkten Kindern. Die Zusagen selbst sind unveraendert (genau eine Karte, dieselben
   Tags, Restzeit-Zeile UEBER der Karte).

## Der EINE naechste Schritt

**S-8 Stufe 3: die Taktik-Bauplaene** aus `D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md`
nach `data/bot_bauplan.json` (Mindestzahlen je Taktik, Restfelder nach Ertrag), **die Zahlen mit den
ECHTEN Werten nachrechnen** (Jaeger 2/2, Zuchten 3, Farm 4/2 - der Entwurf hatte drei Annahmen falsch),
dann 24 Spieltage mit `tools/bot_wirtschaft_messung.py` messen. Danach **S-12** (alle Felder nutzen).
**Der volle Sammellauf und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 03.11.2026, 22:55 - Overlay-Basis gebaut: Dialoge liegen INGAME, kein Desktop-Fenster mehr (Register 177)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die drei haeufigsten Dialoge sind keine eigenen Fenster mehr.** Daniel (22:2x): keine Desktop-Zusatzfenster,
sondern Dialoge INGAME ueber dem Hauptfenster, Hintergrund abgedunkelt und durchscheinend. Gebaut ist die
Basis dafuer - eine Flaeche ueber dem Inhaltsbereich, ein vorgerendertes Abdunkelbild (Bildschirmabzug des
Inhalts plus Alpha-Schleier, weil Tk keine Transparenz je Widget kann), `grab_set` als Eingabesperre, Escape
und Klick daneben schliessen -, und darauf umgestellt sind **Dorf-Optionen, Truppen-Auswahl und
Spionagebericht**. Im Code stehen jetzt **7 statt 10** `Toplevel`.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_overlay_ingame.py` **42/0/1** | eigener Lauf |
| Voller Sammellauf | **157 von 159 gruen, 0 rot, 648 s** (Start 22:54), 6.189 Pruefungen, 54 Befunde; die zwei AUSGESETZT-Dateien sind dokumentiert zurueckgezogen | `docs/audits/sammellauf_20261103_2255.log` |
| Gegenprobe | **1 Pruefung rot** (Schliessen im Ansichtswechsel abgeschaltet), `main.py` per SHA256 unveraendert zurueck | eigener Lauf |
| Nachbarn | `test_spionage` 146/0/0, `test_portal_fremdblick` 18/0/1, `test_marsch_optik` 63/0/0, `test_doppelpuffer` 15/0/0, `test_baseline` 40/0/0, `test_startspiel` 62/0/1, `test_oberflaeche_original` 65/0/0 | eigene Laeufe |
| Umgestellte Dialoge | `_bot_dorf_optionen`, `_truppen_auswahl`, `_spionage_bericht_anzeigen` | `grep -n "tk.Toplevel(" src/main.py` |
| Zahlen | Deckkraft **140**, Kastenbreite **560**, Escape und Klick daneben an | `data/overlay.json` (Daniel stellt sie ohne Code) |
| Bild-Beleg | `C:/Users/saras/AppData/Local/hermes/cache/scratch/overlay_beleg.png` (Fenster 1280x820, Dialog offen, Inhalt scheint dunkel durch) | eigener Lauf mit `.venv`-Python |

## Was das Bau-Menue betrifft (Befund, nicht Wunschdenken)

Die Uebergabe nannte als ersten Dialog das **Bau-Menue**. Gemessen: es ist **kein `Toplevel`** - die
Bauauswahl liegt als Feld direkt in der Siedlungskarte (`_render_settlement_map`, Abschnitt "angebote").
Es gab dort also nichts umzustellen; an seiner Stelle ist der **Dorf-Optionen-Dialog** ingame gegangen
(der bei jedem Klick auf ein fremdes Dorf aufgeht und zur Truppen-Auswahl fuehrt).

## Der EINE naechste Schritt

**Die Weltkarte: Rahmen als Bildleiste (`main.leiste_zusammensetzen`) UND Felder mit Gelaendeton, feiner
Trennlinie und Goldrand fuer die Auswahl** - Groesse und Aufbau bleiben (Daniel 22:1x). Danach **S-8 Stufe 3**
(Taktik-Bauplaene aus `D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md` nach
`data/bot_bauplan.json`, Zahlen mit den ECHTEN Werten nachrechnen, 24 Spieltage messen). **Der volle
Sammellauf und die Protokollzeile gehoeren zum Abschluss jedes Schnitts.**

---

# STAND 03.11.2026, 22:20 - A gebaut: kein Flackern mehr beim Ansichtswechsel (Register 176)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Ansichtswechsel baut nicht mehr ab und dann auf, sondern baut NEU und tauscht erst dann.**
Damit ist das Flackern weg, das Daniel als "abgehakt" beschrieben hat - ohne dass eine der 23 Ansichten
angefasst wurde. Gemessene Ursache: `_render_view` leerte den Inhaltsbereich bei jedem Aufruf
(`widget.destroy()` je Kind) und fuellte ihn neu, an **46 Aufrufstellen**.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Neue Wache | `tests/test_doppelpuffer.py` **15/0/0** | eigener Lauf |
| Gegenprobe | **3 Pruefungen rot** (alter destroy-Zweig eingesetzt), Datei per SHA256 unveraendert zurueck | eigener Lauf |
| Bestehende Wachen | `test_baseline` 40/0/0, `test_oberflaeche_original` 65/0/0, `test_startspiel` 62/0/1 | eigene Laeufe |
| Voller Sammellauf | **156 von 158 gruen, 0 rot, 548 s** (Start 22:20), 6.146 Pruefungen | `docs/audits/sammellauf_20261103_2220.log` |

## Der Ablauf ab jetzt (Daniels Einordnung 22:2x, mit den neuen Auftraegen)

| # | Schritt | Warum hier |
|---|---|---|
| 1 | **A Doppel-Puffer** | ERLEDIGT 03.11.2026 (Register 176) - wirkt auf alle Ansichten |
| 2 | **Overlay-Basis + die drei haeufigsten Dialoge ingame** | Daniels Frage 1: keine Desktop-Fenster mehr. Zehn `Toplevel` sind der Vorrat; Bau-Menue, Truppen-Auswahl, Nachrichten zuerst |
| 3 | **Weltkarte: Rahmen als Bildleiste + Felder mit Gelaendeton und Goldrand** | Daniels Entscheidung; Groesse und Aufbau bleiben |
| 4 | **S-8 Stufe 3: Taktik-Bauplaene** in `data/bot_bauplan.json` (Mindestzahlen, Restfelder nach Ertrag) | **Entwurf liegt vor** (`D:/Arbeiten/Hermes/Notizen/S8_STUFE3_BAUPLAENE_20261103.md`, drei Annahmen berichtigt: Jaeger 2/2, Zuchten 3, Farm 4/2); Bau offen |
| 4b | **S-12 Alle Felder nutzen** (Daniel 22:2x) | der Bauplan fuellt die Karte, statt eine feste Zahl abzuarbeiten - `docs/KONZEPT_BOT_SPIELNUTZUNG_20261103.md` |
| 4c | **S-11 Kartenwahl mit Feldverstaendnis** | der Bot waehlt die Karte nach dem, was ihre Felder fuer SEINE Taktik bringen - nicht mehr Gold pauschal |
| 4d | **S-13 Abriss und Umbau fuer Bots** | der Spieler kann abreissen, der Bot heute nicht; Kernregeln und Sperren gelten mit |
| 4e | **S-14 entschieden: kein Gleichstand** | Bots behalten **drei Neugruendungen = vier Doerfer**; Ausgleich kommt aus besserem Spiel (S-11 bis S-13) |
| 4f | **S-15 Dorf aufgeben und neu gruenden** (Bot UND Spieler) | Daniel: ein Dorf vernichten und auf einer besseren Karte neu gruenden - sechs Gestaltungsfragen stehen im Konzept |
| 5 | **Die acht Kampfregeln 1 bis 8** | abgesegnet (Register 175), je Regel Wache + Sammellauf |
| 6 | **C: Refresh-Pfad fuer die fuenf haeufigsten Ansichten** | hier wird es wirklich fluessig; braucht B und die Overlay-Basis |
| 7 | V-1 bis V-5 (Berichte, Postfach), S-7 Karawanen, S-9 Stil, W-3, Story | wie gehabt |
| 8 | O-1b echte Hintergrundbilder | wartet auf Daniels Generator-Loesung (Midjourney abgebrochen) |

## Der EINE naechste Schritt

**Die Overlay-Basis bauen** (danach Bau-Menue, Truppen-Auswahl und Nachrichten darauf umstellen): ein
dunkles Alpha-Bild als Flaeche ueber dem Inhalt, darueber ein Kastenbild aus `gebaeude_optik`,
`grab_set` fuer die Eingabesperre, Escape schliesst. Der Sammellauf und die Protokollzeile gehoeren zum
Abschluss.

---

# STAND 03.11.2026, 22:1x - S-8 Stufe 2 (Feld-Prioritaeten, Erzmine 3) und die acht Kampfregeln entschieden

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-8 Stufe 2 gebaut:** `bot_doerfer_bebauen` setzt jede Anlage zuerst in ihre Zone (bevorzugtes
Gelaende) und teilt erst, wenn dort nichts mehr frei ist - so nimmt ein Holzfäller keine Steppe, die
eine Rinderfarm braucht. Die Zonen stehen als `feld_prioritaeten` in `data/bot_wirtschaft.json`
(wald/steppe/huegel/berg/grasland), hergeleitet aus den belegten Erträgen und aus Daniels
Jaeger-Vorgabe. **Erzmine auf 3** (Daniel 22:0x: mehrere Erzminen wie der Spieler, dasselbe fuer die
anderen Gebaeude - die allgemeine Erhoehung kommt mit Stufe 3).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Dorfzahl nach 24 Spieltagen | **4/4/4/4/4** (unveraendert) | `tools/bot_wirtschaft_messung.py --tage 24` |
| Metall in der Kasse | **11.435 bis 16.584** (vorher 2.494 bis 5.388) | dieselbe Messung |
| Anlagen je Dorf | 30 (26 auf der Karte ohne freies Bergfeld - die Karte bestimmt es) | dieselbe Messung |
| Wachen | `test_bot_warenkette` 35/0/0, `test_bot_dorf_als_ort` 32/0/0, `test_s8_ertrag_aus_anlagen` 21/0/0, `test_bot_kartenprofil` 40/0/0 | eigene Laeufe |
| Voller Sammellauf fuer diesen Stand | **155 von 157 gruen, 0 rot, 482 s** (Start 22:05), 6.131 Pruefungen | `docs/audits/sammellauf_20261103_2205.log` |

**Die acht Kampfregeln sind abgesegnet** (Register 175, `docs/ENTSCHEIDUNGEN_KAMPFREGELN_20261103.md`):
fusstruppen_begriff, flucht_formel, beute_verteilung, beute_reihenfolge (**Gold zuerst**),
belagerungsturm_mauerschaden (1-4 minus Wallstufe), mauer_reparatur (aktiv, **mit Bauzeit**),
vorrunde_wiederholung, geraetebeute (Zerstoerung, 10 Prozent je Sequenz, max. 50). Nah-/Fernkampf
bekommt ein eigenes Kennzeichen je Einheit, weil `einheiten.ROLLEN` beide auf `kaempfer` abbildet.

## Einschaetzung Oberflaeche (Daniel 22:1x) - liegt vor

`docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`: **beides ist moeglich.** (1) Ingame-Dialoge statt
Desktop-Fenster: JA - Overlay im Hauptfenster, Abdunkelung als vorgerendertes Alpha-Bild (Pillow ist da),
kein `Toplevel` noetig; heute stehen **10** Toplevel im Code. (2) Kein Neuaufbau je Klick: JA, in vier
Stufen - A Doppel-Puffer (klein, wirkt ueberall gegen Flackern), B Karte ohne Neuaufbau (Canvas-Objekte
einmal erzeugen, dann nur aendern), C Refresh-Pfad fuer die fuenf haeufigsten Ansichten (hier wird es
wirklich fluessig), D Rest. Ursache gemessen: `_render_view` zerstoert bei **46** Aufrufstellen alle
Widgets und baut sie neu. Weltkarte: drei Designvorschlaege im selben Dokument (Rahmen als Bildleiste,
Felder mit Gelaendeton und Goldrand, spaeter gemalte Kacheln).

## Daniels Entscheidungen zur Oberflaeche (22:2x) - jetzt der naechste Schnitt

| Frage | Entscheidung |
|---|---|
| Reihenfolge | **Oberflaeche zuerst**: A (Doppel-Puffer) **und** die Overlay-Basis mit den drei haeufigsten Dialogen - die acht Kampfregeln und S-8 Stufe 3 kommen danach |
| Weltkarte | **Rahmen als Bildleiste UND Felder mit Gelaendeton und Goldrand** (Vorschlag 3+2 zusammen) |

**Rezept fuer den naechsten Schnitt (aus `docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`):**

1. **A - Doppel-Puffer in `_render_view`:** den Inhalt in ein NEUES, noch nicht gepacktes Frame bauen
   (die Renderer lesen `self.content`), dann altes Frame zerstoeren und das neue in einem Zug einsetzen.
   Damit verschwindet das Flackern bei allen 46 Aufrufstellen, ohne dass eine Ansicht angefasst wird.
   Pruefzusage: ein Ansichtswechsel hinterlaesst nie einen leeren Inhaltsbereich (Wache ueber
   `winfo_children()` vor und nach dem Wechsel), und die Zahl der Widgets ist vor/nach gleich.
2. **Overlay-Basis:** ein Baustein `_overlay_oeffnen(titel, bauer)` - dunkle Alpha-Flaeche als Bild
   (Pillow, `(0,0,0,140)`) ueber den ganzen Inhaltsbereich, darueber ein Kastenbild aus
   `gebaeude_optik`, `grab_set` fuer die Eingabesperre, Escape schliesst. Danach die drei haeufigsten
   `Toplevel`-Dialoge darauf umstellen (Bau-Menue, Truppen-Auswahl, Nachrichten).
3. **Weltkarte:** Rahmen mit `main.leiste_zusammensetzen` (Ecken fest, Kanten dehnbar) und Felder mit
   Gelaendeton, feiner Trennlinie, Goldrand fuer die Auswahl.

**Jeder Schritt: eigene Wache, voller Sammellauf, Registerzeile, Protokollzeile.**

## Der EINE naechste Schritt

**Die Oberflaeche: A (Doppel-Puffer) und die Overlay-Basis (Daniel 22:2x).** Danach die acht Kampfregeln
in der Reihenfolge 1 bis 8 - je Regel eine Wache, der Sammellauf und die
Protokollzeile. Vorher steht nur noch **S-8 Stufe 3** (Bauplan je Taktik in `data/bot_bauplan.json`,
Mindestzahlen plus Restfelder), weil es die Erzmine-Zahl endgueltig festlegt. **Der Sammellauf gehoert
zum Abschluss jedes Schnitts, und die Protokollzeile dazu ebenfalls.**

---

# STAND 03.11.2026, 21:20 - S-8 Stufe 1: Ertrag aus den GEBAUTEN Anlagen (Register 174)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Ertrag eines Bot-Dorfes kommt jetzt aus seinen Anlagen, nicht mehr aus dem Kartenprofil.**
Gemessen war vorher: ein Dorf mit 48 Holzfällern erntete genau so viel wie eines mit 5 - jede
Bauplan-Logik war damit wirkungslos, und Daniels Vorgabe (der Bot nutzt seine Karte mit Gebaeuden
sinnvoll) konnte nicht greifen. Gerechnet wird jetzt mit DERSELBEN Kernfunktion wie beim Spieler
(`wirtschaft.ertrag_gesamt`: je Feld die Anlage und ihr Gelaende, plus Grundeinkommen und Volksfaktor) -
eine Wahrheit fuer Kern und Anzeige (F-04). Das Kartenprofil ist nur noch **Vorschau** und **Rueckfall**
fuer Doerfer ohne jede Anlage (alte Spielstaende).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `052ac0a` (S-8 Stufe 1), Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Schalter | `data/bot_wirtschaft.json`: `ertrag_weg` **von `karte` auf `anlagen`**; `karte` und `felder` bleiben als Vergleich | Datei |
| Dorfzahl nach 24 Spieltagen | **4/4/4/2/4 -> 4/4/4/4/4** (Silra von 2 auf 4) | `docs/MESSUNG_S8_ERTRAG_AUS_ANLAGEN_20261103.md` |
| Holzvorrat Silra | **471 -> 34.136** (Hauptdorf Tag 24: 151 -> 7.610) | dieselbe Messung |
| Ertrag je Dorf | statt einseitigem Profil ausgeglichen: Haug Stein 1,90 -> **12,35**, Gold 1,50 -> **6,00** | dieselbe Messung |
| Neues Messwerkzeug | `tools/bot_wirtschaft_messung.py --tage 24 [--weg karte] [--aus datei]` | Werkzeug |
| Neue Wache | `tests/test_s8_ertrag_aus_anlagen.py` **21/0/0**, Gegenprobe **6 Pruefungen rot** | eigener Lauf |
| Nachgezogene Wachen | `test_bot_kartenprofil` **40/0/0**, `test_bot_takt_kern` **27/0/1**, `test_bot_warenkette` **35/0/0** | eigene Laeufe |
| Register | **174** | `grep -c '^| [0-9]' docs/PRUEFREGEL_ORIGINAL.md` |

## Drei Befunde, die der Umbau aufgedeckt hat (alle behoben)

1. **Ohne Erzmine erntete kein Bot-Dorf Metall** - das Metall kam vorher aus dem Kartenprofil, also aus
   dem Nichts. Ein Siedlerkarren kostet **80 Metall**; damit wurde kein Karren gebaut und **kein Bot
   gruendete** (Dorfzahl fiel zuerst auf 3/3/3/2/3). Behoben: **eine Erzmine** im Bauplan
   (`data/bot_wirtschaft.json`, VORSCHLAG fuer die Zahl 1, 3 Metall/h auf Berg).
2. **`bot_karren_bauen` buchte vor der Pruefung.** Ein Dorf, das schon einen Karren hatte, verlor bei
   jedem Aufruf **200 Holz** (erst bezahlen, dann ablehnen). Reihenfolge korrigiert; die Wache belegt:
   zweiter Karren kostet jetzt nichts. **Ob dieser Fehler den frueheren Holzschwund erklaert, ist NICHT
   belegt** - im Kartenprofil-Lauf blieb die Kasse gleich, weil dort fast nie genug Metall fuer die
   Buchung im Lager war.
3. **Die Gruendung nahm das REICHSTE Dorf als Quelle** und lehnte ab, wenn dort kein Karren stand - auch
   wenn zwei andere Doerfer einen hatten (Grom blieb bei drei Doerfern). Jetzt kommen nur Doerfer MIT
   Karren als Ausgangsdorf in Frage.

## Der EINE naechste Schritt

**S-8 Stufe 2: Feld-Prioritaeten je Gebaeude** (`docs/KONZEPT_BOT_BAUPLAN_20261103.md`, Stufe 2) - in
den Daten steht je Gebaeude, welches Gelaende es bevorzugt (Holzfaeller und Jaeger Wald, Rinderfarm und
Farm Grasland, Steinmetz und Erzmine Berg) und welches nur als Notloesung zaehlt. Ohne diese Prioritaeten
belegen Holzfaeller die Steppe-Felder und die Zuchten werden nicht mehr gebaut (gemessen). Danach Stufe 3
(Bauplan je Taktik mit Mindestzahlen). **Der Sammellauf gehoert zum Abschluss jedes Schnitts, und die
Protokollzeile dazu ebenfalls.**

## Daniels Antworten aus der Runde 21:45 (in dieser Reihenfolge abarbeiten)

| Frage | Entscheidung |
|---|---|
| Die acht Kampfregeln | **Entwurf jetzt** vom starken Modell vorbereiten, Daniel segnet die Liste in EINEM Durchgang ab (Auftrag `docs/auftraege/AUFTRAG_KAMPFREGELN_20261103.md`, Ziel `D:/Arbeiten/Hermes/Notizen/KAMPFREGELN_20261103.md`) |
| Erzmine im Bot-Bauplan | **mehrere Erzminen, genau wie der Spieler - dasselbe gilt fuer die anderen Gebaeude.** Also nicht die Zahl 1 festschreiben, sondern ueber Stufe 2/3 (Feld-Prioritaeten, dann Bauplan mit Mindestzahlen und Restfeldern) so viele bauen, wie die Karte traegt |
| Obergrenze je Dorf (S-8 Stufe 3) | **alle Felder, die die Taktik sinnvoll fuellt; Restfelder mit dem besten Ertrag** (Mindestzahlen statt Obergrenzen) |
| Ort der Taktik-Bauplaene | **dieselbe Datei erweitern** (`data/bot_bauplan.json`, dort liegt schon ein Bauplan) - EINE Quelle |
| O-1b echte Hintergrundbilder | **ZURUECKGESTELLT**: Midjourney wurde abgebrochen (Daniel: zu teuer), er sucht eine Loesung. O-1a bleibt, bis der Generator geklaert ist - **kein Auftragspaket fuer einen kostenpflichtigen Dienst ohne sein Wort** |

**Der naechste Denk-Auftrag laeuft** (acht Kampfregeln); danach **S-8 Stufe 2 und 3** (Feld-Prioritaeten,
dann Bauplan je Taktik mit Mindestzahlen und Restfeldern - dort wird auch die Zahl der Erzminen
festgelegt). Ausserdem offen: Silra-Diagnose ist mit S-8 Stufe 1 erledigt (Holz 471 -> 34.136), die
Berichte V-1 bis V-5 warten auf die acht Regeln.

# STAND 03.11.2026, 19:26 - Ablauf: Hintergrundbilder als O-1 vor den Postkasten

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Daniels Befund (19:2x):** manche Hintergruende sind „verzerrt und unscharf“. Gemessen, nicht geraten:

| Gegenstand | Wert |
|---|---|
| Hintergrundbilder | **538 x 222 px** (Seitenverhaeltnis 2,42 : 1) - dieselben Dateien wie die Menuebilder |
| Zielflaeche | **980 x 760 px** (1,29 : 1) |
| Skalierung | **3,42 x** hochgezogen, dazu 2,0 px Weichzeichnen und 38 % Abdunkeln |
| Folge | ein flaches Band in einer fast quadratischen Flaeche: cover schneidet die Seiten weg, die Vergroesserung macht es weich |

Das ist dieselbe Klasse Fehler wie die Ressourcenleiste im Oktober (ein BAND als dehnbare FLAECHE behandelt). **Der Fix ist ein eigener Schnitt O-1** und kommt an diese Stelle:

| # | Schritt | Inhalt | Warum an dieser Stelle |
|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** (Teil 2) | Karrenbau im Bot-Takt, dann `siedlerkarren_pflicht: true`, Messung ueber 24 Spieltage | laeuft, Teil 1 (Warenhaltung, Ertrag aus der Karte) ist gebaut |
| 2 | **V-3 Vollstaendiger Kampfbericht** | alle Angaben des Angegriffenen; Garnison zum Angriffsmoment, Warteschlange getrennt und danach weiter | Fundament aller Berichte |
| 3 | **V-2 Angriffs- und Verteidigungsbericht** | je Seite eine Sicht, beide Wege | baut auf V-3 |
| 4 | **V-1 Angriffswarnung** | roter Rahmen (helles Rot) um das Hauptfenster waehrend der Wegzeit | klein, sofort sichtbar, W-4-Angriffe laufen schon |
| 5 | **O-1a Uebergang (ERLEDIGT 03.11.2026)** | Vergroesserung der Hintergrundbilder auf **1,25 x** begrenzt (statt 3,42 x), Rest der Flaeche in dunklem Grund (`gebaeude_optik.hintergrund_flaeche`). Bild bleibt scharf, ist aber kleiner als die Flaeche - **kein Ersatz fuer echte Bilder**, nimmt aber den unscharfen Eindruck sofort weg. Optik-Wachen 179/70/81 gruen | sofort machbar und billig gewesen |
| 6 | **V-4 Postkasten** | Uebersicht nach Art, Zeit, Betreff, Kurzfassung, Details aufklappbar | braucht V-2/V-3 (Arten und Felder) und O-1 (Hintergrund) |
| 7 | **V-5 Bot-Auswertung** | Bots lesen Berichte und schliessen daraus | braucht V-3 und V-4 |
| 8 | **S-7 Karawanen** | Transporte zwischen EIGENEN Doerfern | schreibt selbst ins Postfach |
| 9 | **S-9 Stil je Taktik** | was der Bot mit seinem Reichtum TUT | setzt S-6b und S-7 voraus |
| 9b | **O-1b echte Hintergrundbilder** | Prompts liegen fertig in `D:/Arbeiten/Hermes/Notizen/O1_BILDPROMPTS.md` (20 Motive, gemeinsamer Stilbaustein, Safe Area oben zwei Drittel, Negativ-Prompt). **Blockiert auf die Generatorfrage:** Pollinations liefert das falsche Motiv samt Wasserzeichen (belegt: Frau im Wald statt Lagerhalle, 886 x 665 statt 1600 x 1200), ComfyUI ist nicht installiert. Entscheidung noetig: lokale Installation (mehrere GB Modell) oder kostenpflichtiger Dienst | **nach hinten geschoben** (Entscheidung dieser Sitzung; Daniel 19:4x: „kann man notfalls auch nach hinten schieben“): Gameplay und Berichte wiegen schwerer, die Prompts warten ohne Verlust |
| 10 | **W-3 Kampf ueber Weltgrenzen** | teuer mit Deckel | Bau zuletzt von den Kaempfen |
| 11 | **Story (W-11)** | nur das Noetige, sechs Fraktionen | nebensaechlich, zuletzt |

**S-6b ist ERLEDIGT** (Sammellaeufe 153/155 und 154/156, 0 rot). Der naechste Schritt im Ablauf ist
**V-3 (vollstaendiger Kampfbericht)**; das Schema liegt beim starken Modell.

## Offener Befund: Bot-Doerfer sparen nicht fuer die Gruendung (gemessen 03.11.2026)

| Gegenstand | Wert |
|---|---|
| Gruendungs-Mindestbestand (Kern) | **480 Holz, 300 Stein, 250 Nahrung** (`spieloekonomie.gruendungskosten()`) |
| Silra nach 24 Spieltagen | 945 Gold, 1057 Stein, 1990 Nahrung, **189 Holz** - ein Dorf, fuenf Karren |
| Ursache | jeder Karren kostet 200 Holz; dazu Bauten und Forschung - das Dorf haelt nie 680 Holz gleichzeitig |
| Folge | Silra kann nicht gruenden, obwohl er nach Gold, Stein und Nahrung reich ist |

**Versuchte Loesung, verworfen:** eine Ruecklage in `bot_karren_bauen` (Karren nur, wenn danach noch der
Mindestbestand im Dorf liegt). Gemessen danach: Doerfer unveraendert 3/4/4/1/3, aber **Haug, Silra und
Krank bauen 0 Karren** - die Ruecklage verhindert den Karrenbau, ohne eine einzige Gruendung zu
ermoeglichen. Wieder zurueckgenommen; die Wachen sind gruen (23/0/0, 36/0/1).

**Das ist eine Wirtschaftsfrage, keine Karrenfrage** - und inzwischen gemessen:

| Versuch | Ergebnis |
|---|---|
| mehr Holzfaeller (3 -> **5**, Daniels Entscheidung 20:2x) | **keine Aenderung**: 3/4/4/1/3 Doerfer |
| Ruecklage im Karrenbau (danach muss die Gebuehr noch da sein) | **0 Karren** bei Haug, Silra, Krank - Dorfzahl unveraendert |
| 5 Holzfaeller **und** Ruecklage | genauso: 0 Karren, unveraendert |
| Holzverlauf Silra (5 Holzfaeller, 24 Tage) | Tag 3: **1** Holz, Tag 12: 53, Tag 24: 189 - nie ueber 190 |
| Wohin das Holz geht | **5 Karren** (1.000 Holz), **5 Forschungen** (Baukunst 2, Heimlichkeit 3, Wagenbau, Felderwirtschaft, Kriegskunst), **27 Anlagen** |

Der Ertrag reicht rechnerisch (20 Holz/h x 144 h = 2.880 Holz), aber Karren, Forschung und Bauten
verbrauchen ihn laufend. **Ohne eine Prioritaetsregel kommt kein Bot zur Gruendungsgebuehr** - die
Holzmenge allein loest es nicht.

**Die verbleibende Entscheidung:** soll die **Gruendung Vorrang vor Forschung und Bauen** bekommen
(dann pausieren Forschung und neue Anlagen, bis die 480 Holz beisammen sind)? Das ist der einzige
Weg, der nach dieser Messung noch wirkt - er aendert aber das Verhalten der Bot-Doerfer spuerbar.
Empfehlung: **ja, mit Deckel** - nur solange die Gruendung ansteht und die Hoechstzahl nicht erreicht ist.

# STAND 03.11.2026, 19:02 - Ablauf neu geordnet: S-6b vor S-7, Berichte vor Karawanen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Vorgaben Daniels (18:53 und 19:00) verschieben die Reihenfolge.** (a) Der Bot muss den **Siedlerkarren** bauen wie der Spieler - damit wird die Warenkette (S-6b) zur Voraussetzung jeder Bot-Gruendung, statt spaeter zu kommen. (b) **Postfach und Kampfberichte** sind ein eigener Block (V-1 bis V-5, `docs/VORGABE_POSTFACH_UND_BERICHTE_20261103.md`) und gehoeren VOR die Karawanen: S-7 und S-9 schreiben selbst Meldungen ins Postfach und sollen nicht gegen ein Format bauen, das danach umgestellt wird.

| # | Schritt | Inhalt | Warum an dieser Stelle |
|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** | Stellmacher, Leder, Wolle, Pferde beschaffbar machen; danach `siedlerkarren_pflicht` auf `true` | Daniels Entscheidung 18:53 - ohne Karren gruendet nach der Umstellung KEIN Bot; blockiert S-7, S-9 und die Ziele von W-4 |
| 2 | **V-3 Vollstaendiger Kampfbericht** | Bericht traegt alle Angaben des Angegriffenen (Wall, Garnison, Taktik, Vorraete, Beute, Verluste beider Seiten) | Fundament: ohne diesen Inhalt haben die naechsten drei Schritte nichts zu zeigen |
| 3 | **V-2 Angriffs- und Verteidigungsbericht** | je Seite eine eigene Sicht, beide Wege (Spieler->Bot, Bot->Spieler) | baut direkt auf V-3 |
| 4 | **V-1 Angriffswarnung** | roter Rahmen in hellem Rot um das Hauptfenster, solange ein Angriff auf den Spieler unterwegs ist; danach nur der Bericht | klein und sofort sichtbar; W-4-Angriffe laufen schon, der Spieler soll sie bemerken |
| 5 | **O-1a Uebergang (ERLEDIGT 03.11.2026)** | Vergroesserung der Hintergrundbilder auf 1,25 x begrenzt, Rest der Flaeche in dunklem Grund; Bild bleibt scharf statt 3,42 x aufgeblasen (`gebaeude_optik.hintergrund_flaeche`). **Kein Ersatz fuer echte Bilder**, nimmt aber den unscharfen Eindruck sofort weg | sofort machbar und billig |
| 5b | **V-4 Postkasten** | Uebersicht nach Art, Zeit, Betreff, Kurzfassung; Details aufklappbar | braucht V-2/V-3, weil erst dann feststeht, welche Arten und Felder zu zeigen sind |
| 6 | **V-5 Bot-Auswertung** | Bots lesen eingehende Berichte und schliessen daraus, ob ein weiterer Angriff lohnt | braucht V-3 (Inhalt) und V-4 (Ablage) |
| 7 | **S-7 Karawanen** | Transporte zwischen EIGENEN Doerfern, Reisekosten im Startdorf | schreibt selbst ins Postfach - jetzt in ein fertiges Format |
| 8 | **S-9 Stil je Taktik** | was der Bot mit seinem Reichtum TUT | setzt S-6b und S-7 voraus |
| 9 | **W-3 Kampf ueber Weltgrenzen** | teuer mit Deckel (Daniel 16:08) | Preis ist Denkarbeit, der Bau kommt zuletzt von den Kaempfen |
| 10 | **Story (W-11)** | nur das Noetige, den sechs Fraktionen angepasst | nebensaechlich, zuletzt |

**Der EINE naechste Schritt: S-6b** - der Bot baut den Siedlerkarren wie der Spieler. Erst messen, welche Waren und Gebaeude der Kern fuer einen Karren verlangt (`spieloekonomie.gruendungskosten()`, `warenrezepte.json`, Werkstattkette), dann die Bot-Wirtschaft nachziehen, dann `siedlerkarren_pflicht` auf `true` und ueber 24 Spieltage pruefen, dass jeder Bot vier Doerfer hat. Der Sammellauf gehoert zum Abschluss, das Protokoll traegt die Zeile dazu.

# STAND 03.11.2026, 18:47 - T-1: Ingame-Texte mit echten Umlauten (Register 171)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Alles, was der Spieler liest, traegt jetzt echte deutsche Rechtschreibung** - „wählen“ statt „waehlen“, „Gebäude“, „für“, „zurück“, „Kästchen“, „Menü“. Daniels Vorgabe (17:15) ist damit erfuellt: Knoepfe, Menues, Reiter, Dialoge, Tooltips, Meldungen, Postfach, Spiel-Log und die angezeigten Datenamen. **Kennungen, JSON-Schluessel, Dateinamen, Docstrings und Kommentare bleiben ASCII** - und Code-Bezuege in einer Meldung nennen weiter den Code-Namen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c87efcd` | `git log --oneline -1` |
| Messung VORHER | **521 Ersatzschreibweisen in 2.264 Anzeigetexten**, 42 Dateien | `tools/anzeigetexte_inventur.py` gegen `git show HEAD:src/...` |
| Messung NACHHER | **0** in 2.263 Anzeigetexten | `docs/ANZEIGETEXTE_INVENTUR.md` |
| Ersetzte Literale | **374** in 42 Dateien (Drittel 1: 90, Drittel 2: 154, `main.py`: 130) | `tools/anzeigetexte_umlaute_setzen.py` |
| Neue Wache | `tests/test_anzeigetexte_umlaute.py` **49/0/0**, Gegenprobe erzeugt eine Fundstelle | eigener Lauf |
| Voller Sammellauf | **152 von 154 gruen, 0 rot, 2 ausgesetzt, 6.047 Pruefungen, 467 s** (Start 18:35) | `docs/audits/sammellauf_t1_final.log` |
| Pruefdateien / Register | **154** / **171** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Mitgezogene Wachen | zehn: auftraege, lokale_lager, warentransport, spionage (3x), baumenue_standorttipps, speichern_robust, botkern, bottaktik, voelkerwahl, spielschicht, portal_uebersicht, portal_fremdblick, startkartenwahl, dorfuebersicht, kampf_einhaengung, ausbildung_uebersicht, bot_raubzug_bot, originalkarten_baukasse, schild_nebenfenster, spielstand_gui, spielstandarchiv | je Lauf gruen |

**Zwei Werkzeuge statt Massenersetzung:** `tools/anzeigetexte_inventur.py` misst nur, was wirklich in eine Anzeige geht (Klassen A/B/C), `tools/anzeigetexte_umlaute_setzen.py` ersetzt auf der exakten Quellspanne mit Wortkarte und schuetzt Code-Bezuege. Beide teilen sich EINE Messung (Muster F-04).

## Der EINE naechste Schritt

**S-7 Karawanen** (Daniels Reihenfolge): Transporte zwischen den EIGENEN Doerfern ueber `auftraege.starten`, Reisekosten im Startdorf. Mit vier Doerfern je Bot wird der Nachschub noetig - ein Dorf ohne Nachschub hungert. Danach **S-9** (Stil je Taktik), **W-3** (teuer mit Deckel), **S-6b** (Warenkette fuer Bots, damit der Siedlerkarren Pflicht werden kann) und zuletzt die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand ist er gruen gelaufen (467 s), und das Protokoll traegt die Zeile dazu.

# STAND 03.11.2026, 17:02 - S-6: Bots gruenden nach, vier Doerfer je Bot (Register 170)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder Bot gruendet jetzt eigene Doerfer - bis zu vier, in seiner Heimatwelt, mit eigener Karte.**
Daniels Vorgabe war „Nachgruenden, 3 Gruendungen je Bot = 4 Doerfer“. Gebucht wird mit den Zahlen des
KERNS: `spieloekonomie.gruendungskosten()` liefert Gebuehr, Startpaket und Mindestbestand, die
Forschungsregel (Wagenbau 1) kommt aus `spieloekonomie.REGELN`. Gemessen im echten Startstand: nach
**24 Spieltagen hat jeder der fuenf Bots vier Doerfer** - vorher hatte ein Bot ein bis drei, und ein
Dorf zu gruenden war ueberhaupt nicht moeglich.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `a5f0da5` plus diese Aenderung | `git log --oneline -1` |
| Daten | `data/bot_gruendung.json`: `hoechstens_doerfer` 4, `sperre_stunden` 72, `siedlerkarren_pflicht` false | Datendatei |
| Wache | `tests/test_bot_gruendung.py` **36/0/1** | eigener Lauf |
| Gegenproben | Forschungspruefung aus -> **2 Fehler**; Hoechstzahl aus -> **5 Fehler** (Bots kamen auf 7-10 Doerfer); Datei beide Male hashgleich zurueck | eigener Lauf |
| Messung im Spiel | nach 24 Spieltagen **4 Doerfer je Bot**, alle in der Heimatwelt, 4 verschiedene Karten, 11 Gruendungs-Nachrichten im Postfach | `tests/test_bot_gruendung.py` Abschnitt 4 |
| Voller Sammellauf | **151 von 153 gruen, 0 rot, 2 ausgesetzt, 5.997 Pruefungen, 469 s** (Start 17:04) |
| Neue Vorgabe Daniel (17:15) | **Ingame-Texte mit echten Umlauten** („wählen“ statt „waehlen“); Kennungen und Kommentare bleiben ASCII. Schnitt **T-1** noch offen | `docs/VORGABE_INGAME_TEXTE_20261103.md` | `docs/audits/sammellauf_20261103_1704.log` |
| Pruefdateien / Register | **153** / **170** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Die eine Abweichung, die Daniels Wort braucht:** der Kern verlangt fuer eine Gruendung einen
**Siedlerkarren**, und den kann ein Bot nicht bauen - seine Doerfer fuehren kein Leder, keine Wolle,
keine Pferde, weil die Bot-Wirtschaft keine Werkstattkette hat (gemessen). Der Schalter
`siedlerkarren_pflicht` steht deshalb auf `false`: Gebuehr und Startpaket werden voll bezahlt, die
fuenf Siedler des Karrens ziehen direkt aus dem Ausgangsdorf um. Sobald Bots eine Warenkette haben
(S-6b), wird der Schalter auf `true` gestellt - dann gilt die strenge Kernregel.

## Der EINE naechste Schritt

**T-1 zuerst: Ingame-Texte mit echten Umlauten** (Daniels Vorgabe 17:15). Erst das praezise
Inventurwerkzeug (`text=`, `insert(`, `_log(`, `messages.append` - nur was wirklich angezeigt wird),
dann Datei fuer Datei ersetzen, zuletzt `main.py`, mit einer Wache gegen die Ersatzschreibweisen. Jede
umgestellte Wache nennt die Entscheidung im Kommentar.

**Danach S-7 Karawanen**: Transporte zwischen den EIGENEN Doerfern (`auftraege.starten`, Reisekosten im
Startdorf). Mit vier Doerfern je Bot wird das noetig: ein Dorf ohne Nachschub hungert, und die
Rohstoffe liegen dort, wo die Karte sie hergibt - nicht dort, wo gebaut wird. Danach **S-9** (Stil je
Taktik), **W-3** (teuer mit Deckel, Daniels Entscheidung), **S-6b** (Warenkette fuer Bots, damit der
Siedlerkarren Pflicht werden kann) und zuletzt die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:56 - W-4: Bots rauben auch untereinander (Register 169)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Ein starker Bot kann jetzt ein Dorf eines ANDEREN Bots ausrauben.** Daniels Vorgabe war, dass Bots
mit Einheiten und eigenen Doerfern Raubzuege um Ressourcen machen - „nicht nur gegen den Spieler, auch
gegeneinander“, aber nur in einer Welt, die spielaktiv ist. Der Bot greift dafuer dieselben Stellen an
wie beim Angriff auf den Spieler: `kampf.fuehre_schlacht` kaempft, `kampfbericht.beute_am_ziel` zieht
die Beute beim Zielort ab, `bot_armee_buchen` bucht die Verluste, und das Postfach bekommt einen
Bericht. Das Dorf wechselt nie den Besitzer, Truppen bleiben nie am Zielort - die zwei Regeln gelten
unveraendert.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `1a773bc` plus diese Aenderung | `git log --oneline -1` |
| Daten (alle Zahlen VORSCHLAG) | `data/bot_raubzug.json`: `armee_schwelle` 6, `doerfer_schwelle` 1, `staerke_faktor` 1,5, `nur_eigene_welt` true | Datendatei |
| Wache | `tests/test_bot_raubzug_bot.py` **39/0/0** | eigener Lauf, `docs/audits/raubzug_einzellauf.log` |
| Gegenproben | Weltfilter abgeschaltet -> **2 Fehler**; Beute-Buchung uebersprungen -> **1 Fehler**; Datei beide Male hashgleich zurueck | eigener Lauf |
| Umgestellte Wache | `test_bot_armee_je_dorf` 21/1/1 -> **22/0/1** (sie verlangte genau EINE Verlustbuchung; seit W-4 gibt es zwei Verluststellen) | eigener Lauf |
| Nachbarproben | `test_botkern` **101/0/0**, `test_bot_diebstahl` **46/0/1**, `test_bot_welten` **44/0/1**, `test_bot_ausbildung_je_ort` **20/0/1**, `test_bot_takt_scheiben` **34/0/1**, `test_startspiel` **62/0/1**, `test_durchspiel` **65/0/2**, `test_portal_fremdblick` **18/0/1**, `test_bot_wappen` **26/0/1**, `test_gpt_frischstart` OK (6 Tests) | eigene Laeufe |
| Entscheidungen Daniel (16:08) | W-3 teuer mit Deckel; Weltaufteilung bleibt; Wappen bleiben; Karte 8 px + Name beim Darueberfahren | Nachtrag 16:08 in `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |
| Voller Sammellauf | **150 von 152 gruen, 0 rot, 2 ausgesetzt, 5.960 Pruefungen, 415 s** (Start 15:58) | `docs/audits/sammellauf_20261103_1558.log` |
| Pruefdateien / Register | **152** / **169** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Berichtigung am Vorgaengerblock | Die Uebergabe war **10.557 Byte, SHA256 `35624259…`** (15:44 nachgemessen, hashgleich archviert) - der Block vom 15:25 nennt 10.485 Byte / `c0e5fafd`; die Datei wurde nach dem Schreiben des Blocks noch ergaenzt | `sha256sum`, `stat` |

**Befund, der die naechste Sitzung betrifft:** nach der Voelkerwahl traegt jeder Bot eine eigene
Fraktion und damit eine eigene Heimatwelt (W-5/W-9) - es steht dann genau EIN Bot je Welt. Ein Raubzug
Bot gegen Bot hat damit nur dann ein Ziel, wenn zwei Bots' Doerfer in DERSELBEN Welt stehen: vor der
Voelkerwahl ist das bei Haug und Brynhild (beide menschlich, Welt 4) der Fall, danach erst wieder mit
dem Nebendorf-Umzug (W-2). Der Code kann es, die Weltaufteilung gibt ihm derzeit selten ein Ziel -
das ist eine offene Frage an Daniel, keine Luecke im Schnitt.

## Der EINE naechste Schritt

**S-6 Nachgruenden** (Daniels Reihenfolge): drei Gruendungen je Bot, damit ein Bot vier Doerfer hat -
die Voraussetzung dafuer, dass die Weltkarte je Bot mehrere Doerfer zeigt (W-7) und ein Raubzug
ueberhaupt mehrere Ziele hat. Danach **S-7** (Karawanen zwischen eigenen Doerfern), **S-9** (Stil je
Taktik), zuletzt **W-3** (braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel) und die
**Story** (W-11, nebensaechlich).

**Die Fragen der Runde sind beantwortet (Daniel, 16:08 - Nachtrag in `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md`):**
W-3 wird **teuer mit Deckel** (nicht gesperrt, eigener Schnitt spaeter), die Weltaufteilung **bleibt**
(ein Bot je Welt, W-4 greift nur wo zwei Bots eine Welt teilen), die **Wappen bleiben** in der
Reihenfolge der Fraktionen, und die Karte bleibt bei 8 px - der Burg-Name kommt erst beim
Darueberfahren (kleiner Optik-Schritt, nicht Teil von W-4).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - der Lauf zu diesem Stand ist gruen
(Zeile oben) und startete nach dem letzten Code-Eingriff.

# STAND 03.11.2026, 15:25 - S-5 komplett, Sammellauf gruen, Uebergabe geschrieben

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Tag ist abgeschlossen und gruen:** 149 von 151 Pruefdateien gruen, 0 rot, 2 ausgesetzt,
5.920 Pruefungen in 332 s. Gebaut sind heute S-13 (Bot-Takt deterministisch, Diebstahl eingeschaltet)
und die fuenf Welten-Schnitte W-1, W-5/W-9, W-8, W-6/W-7 sowie S-5 komplett (S-5b Armee in den
Doerfern, S-5c Essen je Dorf, S-5a Ausbildung ueber die Warteschlange).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `e82ce66` plus diese Doku, Arbeitsbaum leer | `git log --oneline -1` |
| Voller Sammellauf (Endstand) | **149 von 151 gruen, 0 rot, 2 ausgesetzt, 5.920 Pruefungen, 332 s** | `docs/audits/sammellauf_20261103_1516.log` |
| Pruefdateien / Register | **151** / **168** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Uebergabe | `C:\Users\saras\Desktop\UEBERGABE_NEBELSEETAL_20261103_1525.md` (10.485 Byte, SHA256 `c0e5fafd…`) | Desktop |
| Guthaben | **12,59 / 47,40 USD** (13:43 von Daniel abgelesen) | Protokoll |

## Der EINE naechste Schritt

**W-4: Bots rauben auch untereinander** (Daniels Vorgabe): starke Bots mit Einheiten und eigenen
Doerfern machen Raubzuege - gegen den Spieler UND gegen andere Bots, aber nur in einer Welt, die
spielaktiv ist. Die Voraussetzungen stehen: die Armee liegt in den Doerfern (S-5b), die Ausbildung
laeuft ueber die Warteschlange (S-5a), die Weltzuordnung ist fest (W-5/W-9). Danach S-6
(Nachgruenden), S-7 (Karawanen), S-9 (Stil je Taktik), zuletzt **W-3** (braucht Daniels Entscheidung:
gesperrt oder teuer mit Deckel) und die **Story** (W-11, nebensaechlich).

**Vier offene Fragen** stehen in der Uebergabe, Abschnitt 8 (W-3, ein Volk ohne Bot, Wappen-Zuordnung,
Burg-Groesse auf der Karte).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - und die naechste Sitzung faengt mit
`git status` und `date` an, nicht mit dem Bauen.

# STAND 03.11.2026, 17:40 - S-5 komplett: der Bot bildet aus statt zu kaufen (Register 168)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-5 ist fertig.** Die Armee steht in den Doerfern (S-5b), jedes Dorf isst fuer seine eigene
Garnison (S-5c), und der Bot **bildet jetzt aus** statt zu kaufen (S-5a): er geht denselben Weg wie
der Spieler - Forschung, Ausbildungsstaette vor Ort, Siedler, Ausruestung, Kosten aus dem Dorflager -
und die Einheit entsteht nach der Ausbildungszeit in genau dem Dorf, das sie ausgebildet hat.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fa66231` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_ausbildung_je_ort.py` **20/0/1** | eigener Lauf |
| Gegenprobe | Auftrag nicht ins Dorf geschrieben -> **1 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_bot_dorf_wirtschaft` **54/0/0**, `test_bot_nahrung` **48/0/0**, `test_bot_armee_je_dorf` **22/0/1** | eigene Laeufe |
| Nachbarproben | `test_botkern` **101/0/0**, `test_oekonomie_uhr` **65/0/0**, `test_werkstatt` **118/0/1**, `test_durchspiel` **65/0/2** | eigene Laeufe |

## Der EINE naechste Schritt

**W-4: Bots rauben auch untereinander.** Heute waehlt `bot_angriffsplanung.waehle_ziel` Ziele nur
unter den Siedlungen des Spielers; Daniel will, dass starke Bots mit Einheiten und eigenen Doerfern
Raubzuege machen - gegen den Spieler UND gegen andere Bots, aber nur in einer Welt, die spielaktiv
ist. Danach **S-6** (Nachgruenden), **S-7** (Karawanen), **S-9** (Stil je Taktik), zuletzt **W-3**
(braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel) und die **Story** (W-11).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 16:45 - S-5b/S-5c: die Armee steht in den Doerfern (Register 167)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Armee eines Bots haengt nicht mehr am Bot, sondern in seinen Doerfern — und jedes Dorf isst
fuer seine eigene Garnison.** Das ist die Voraussetzung fuer S-5a (Ausbildung je Ort): ohne diesen
Schritt haette eine Ausbildung im Dorf das Essen doppelt gezaehlt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7e1d16` plus diese Aenderung | `git log --oneline -1` |
| Wache | `tests/test_bot_armee_je_dorf.py` **21/0/1** | eigener Lauf |
| Gegenprobe | Eigenschaft liefert `{}` -> **4 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_bot_nahrung` **47/0/0**, `test_bot_bedarf` **25/0/1**, `test_bot_diebstahl` **46/0/1**, drei GPT-Wachen OK | eigene Laeufe |
| Nachbardateien | `test_botkern` **101/0/0**, `test_s7_botverhalten` **46/0/0**, `test_bot_dorf_wirtschaft` **54/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |

## Der EINE naechste Schritt

**S-5a: Ausbildung je Ort ueber die Warteschlange statt Kauf.** Der Kern hat sie schon
(`spieloekonomie.ausbildung_start`, `ausbildung_grenzen`, `Settlement.ausbildung` je Ort, und
`bot_dorf_als_ort` reicht sie durch) - der Bot umgeht sie nur. Jetzt darf er sie benutzen: die
Einheit entsteht im Dorf mit dem Einheiten-Gebaeude und steht danach im selben Dorf (S-5b ist dafuer
gebaut), gegessen wird dort (S-5c). Danach **W-4** (Bots rauben untereinander), **S-6/S-7/S-9**,
zuletzt **W-3** (braucht Daniels Entscheidung) und die **Story** (W-11, nebensaechlich).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:40 - W-6/W-7: Blick in fremde Welten, Doerfer je Welt (Register 166)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Spieler kann jetzt in fremde Welten SCHAUEN, ohne zu springen.** Ueber der Karte steht
'Ansehen:' mit der eigenen Welt und den Nummern der fuenf anderen; ein Klick zeigt deren Karte mit den
Burgen der dortigen Bots, die Kopfzeile sagt 'NUR ANSICHT', und unter der Karte steht, wie viele
Doerfer jeder Bot in dieser Welt hat. Angriff oder Spionage oeffnen sich dort NICHT - ein Auftrag
ueber die Weltgrenze ist bis zur Entscheidung W-3 gesperrt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c77f8dd` plus diese Aenderung | `git log --oneline -1` |
| Wache | `tests/test_portal_fremdblick.py` **18/0/1** | eigener Lauf |
| Gegenprobe | 'Ansehen' als echter Sprung -> **3 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Nebenbefund behoben | Gruendungen standen in Welt 1 statt in der Welt des Spielers - beide Gruendungswege setzen sie jetzt, Laden repariert unmoegliche Welten | `src/main.py` |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Story-Regel (W-11) | aus der Nebelseetal-Geschichte nur das Noetige, den sechs Fraktionen angepasst, Story nebensaechlich - eingeordnet ans ENDE der Liste | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf. Reihenfolge im
Schnitt, vom Code selbst verlangt: **erst die Armee nach `dorf.einheiten` (S-5b)**, dann ausbilden
(S-5a), dann Essen je Dorf (S-5c) - sonst isst die Armee doppelt. Danach **W-4** (Bots rauben
untereinander), **S-6/S-7/S-9**, zuletzt **W-3** (braucht Daniels Entscheidung) und die **Story**.

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 15:10 - W-8: Burgen und Wappen auf der Weltkarte (Register 165)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jedes Dorf auf der Weltkarte ist jetzt zuzuordnen.** Statt des braunen Kastens mit X traegt jedes
Dorf die **Burg seiner Fraktion** und darunter ein kleines **Wappen-Abzeichen** - Hauptdorf und
Nebendoerfer desselben Bots dasselbe Paar, der Spieler sein eigenes. Die Bilder sind Daniels
Lieferung vom 01.11., die Zuordnung steht in einer Datendatei.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `88ca781` plus diese Aenderung | `git log --oneline -1` |
| Neue Regeldaten | `data/bot_wappen.json` - je Fraktion Burg + Wappen, zwei Groessen-Regler, Urteil VORSCHLAG | Datei |
| Wache | `tests/test_bot_wappen.py` **26/0/1** | eigener Lauf |
| Gegenprobe | Zeichnen abgeschaltet -> **1 Fehler** (0 von 4 Bildern), Datei hashgleich | eigener Lauf |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Belegbilder | `docs/audits/wappen_uebersicht_20261103.png`, `portal_wappen_heimat_20261103.png`, `portal_wappen_fremdwelt_20261103.png` | eigene Aufnahmen |

## Der EINE naechste Schritt

**W-6/W-7: der Blick in fremde Welten.** Seit W-5/W-9 stehen die fuenf Bots in ihren Fuenf-Welten -
die Heimatkarte des Spielers zeigt damit nur noch seine eigenen Doerfer. Der Ueberblick ueber die
anderen Welten („der spieler ... sieht bereits die bots wenn er in die Uebersicht einer anderen welt
schaut“) und die Anzeige, wie viele Doerfer ein Bot in seiner Welt hat, fehlen noch. Danach **S-5
Ausbildung je Ort** (S-5b Armee ins Dorf zuerst), **W-4** (Bots rauben untereinander), **S-6/S-7/S-9**;
**W-3** braucht Daniels Entscheidung (gesperrt oder teuer mit Deckel).

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 14:40 - W-5/W-9: fuenf Bots, Heimatwelt je Fraktion (Register 164)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder Nutzer hat jetzt eine Herkunftswelt, und der Spieler startet in der Welt seines Volkes.**
Vorher wuerfelte die Zahl der Bots (1 bis 5) und die Startwelt war fuer jeden die feste Datenwelt
`d04`. Jetzt: fuenf Bots fest, je Fraktion genau eine Heimatwelt, Wahl des Volkes setzt die
Startwelt — ohne Midgard-Zwang im Code.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `331edd5` plus diese Aenderung | `git log --oneline -1` |
| Neue Regeldaten | `data/welt_fraktionen.json` (Fraktion -> Welt, VORSCHLAG mit Begruendung, NICHT BELEGT) | Datei |
| Wache | `tests/test_bot_welten.py` **44/0/1** | eigener Lauf |
| Gegenproben | Spielerwelt-Zeile entfernt -> **5 Fehler**; Bot-Zahl wieder gewuerfelt -> **1 Fehler**; Datei beide Male hashgleich | eigene Laeufe |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_voelkerwahl` **37/0/0**, `test_botkern` **101/0/0**, `test_durchspiel` **65/0/2** | eigene Laeufe |
| Guthaben (13:43) | **12,59 / 47,40 USD**, seit 12:24 **0,21 USD** | Protokoll |

## Der EINE naechste Schritt

**W-8: Burgen und Wappen auf die Weltkarte.** Die sechs Burgen (`assets/icons/burgen/burg_01..06.png`)
und zehn Wappen (`assets/icons/wappen/wappen_01..10.png`) liegen fertig und freigestellt; heute zeichnet
die Karte einen braunen Kasten mit X, ohne Name, ohne Nummer. Danach **W-6/W-7** (Nur-Lese-Blick in
fremde Welten, Doerfer je Welt zaehlen), dann **S-5 Ausbildung je Ort** (S-5b Armee ins Dorf zuerst,
sonst isst sie doppelt), dann **W-4** (Bots rauben untereinander), dann S-6/S-7/S-9. **W-3** (Kampf
ueber Weltgrenzen) braucht Daniels Entscheidung: gesperrt oder teuer mit Deckel.

**Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - nach diesem Stand laeuft er.

# STAND 03.11.2026, 13:52 - W-1: jedes Bot-Dorf steht nur auf seiner Weltkarte (Register 163)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots liegen jetzt in der Welt, in der sie entstanden sind — und die Karte luegt nicht mehr.**
Vorher stand jedes Bot-Dorf auf der nackten Vorgabe `dimension = 1` (Armageddon), waehrend die Heimat
des Spielers **Midgard (4)** ist; die Anzeige prueft die Welt gar nicht und zeigte fremde Doerfer auf
jeder Karte. Jetzt traegt jedes Dorf seine **Herkunftswelt**, entsteht in der Startwelt, und die Karte
zeigt nur, was auf ihr steht.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `3e9982c` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_welten.py` **19/0/1** | eigener Lauf |
| Gegenprobe | Filterzweig abgeschaltet -> **4 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Nachbardateien | `test_startspiel` **62/0/1**, `test_weltbild_gelaende` **135/0/0**, `test_spionage` **146/0/0**, `test_durchspiel` **65/0/2**, `test_bot_diebstahl` **46/0/1** - alle unveraendert gruen | eigene Laeufe |
| Guthaben (13:43, von Daniel abgelesen) | **12,59 / 47,40 USD** - seit 12:24 **0,21 USD** Verbrauch | `docs/ENTWICKLUNGSPROTOKOLL.md` |
| Offen aus Daniels Vorgaben | **W-2** Umzug eines Nebendorfs, **W-3** Preis/Sperre ueber Weltgrenzen (braucht Daniels Wort), **W-4** Bot gegen Bot | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf
(`spieloekonomie.ausbildung_start`, die der Kern schon hat und der Bot umgeht). **Reihenfolge im
Schnitt ist gemessen, nicht geraten:** erst die Armee nach `dorf.einheiten` (S-5b), dann ausbilden
(S-5a) — der Docstring von `bot_dorf_tick` sagt es selbst: 'sobald S-5 Einheiten je Ort ausbildet,
muss die Armee dort hineinwandern (sonst isst sie zweimal)'. Danach S-6 Nachgruenden, S-7 Karawanen,
S-9 Stil je Taktik. **Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts**, das Protokoll
traegt die Kennung.

# STAND 03.11.2026, 12:43 - S-13: der Bot-Takt haengt an festen Spielzeit-Punkten (Register 162)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Zeit ist jetzt eine Wahrheit — auch fuer die Bots.** Der Bot-Takt feuert nicht mehr, wenn die
Fliesskomma-Differenz reicht, sondern an FESTEN Spielstunden-Punkten: die Orte werden bis zum Punkt
gebucht, dann handelt der Bot auf genau diesem Stand. `1 x 3600 s` und `10 x 360 s` fahren dieselben
Zuege. Damit ist der Diebstahl (S-12) eingeschaltet - er war bis heute nur gebaut.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `55cd905` plus diese Aenderung | `git log --oneline -1` |
| Neue Wache | `tests/test_bot_takt_scheiben.py` **34/0/1** | eigener Lauf |
| Diebstahl-Wache | `tests/test_bot_diebstahl.py` **46/0/1** (Datei jetzt AKTIV, samt Goetterschutz) | eigener Lauf |
| Demo-Regel | `tests/test_s7_botverhalten.py` **46/0/0** | eigener Lauf |
| Gegenprobe | alte Bedingung zurueckgetauscht -> **5 Fehler**, Datei hashgleich zurueckgesetzt | eigener Lauf |
| Umgestellte Wachen | `test_gpt_fixrunde_ortslager_zeit_20261028`, `test_gpt_frischstart`, `test_gpt_bot_angriffsplanung`, `test_gpt_wall_bot_kampf` je OK (Diebstahl im `setUp` aus, Begruendung im Test) | eigene Laeufe |
| Voller Sammellauf 12:54 (ENDSTAND) | **144 von 146 gruen, 0 rot, 2 ausgesetzt, 5.786 Pruefungen, 314 s** | `docs/audits/sammellauf_20261103_1254.log` |
| Verworfen: Lauf 12:45 | **142 von 146, 2 rot** - beide rot aus EINEM Grund (der Diebstahl umging den Goetterschutz), behoben und in 12:54 gruen; nicht als roter Stand lesen | `docs/audits/sammellauf_20261103_1245.log` |
| Neue Vorgaben Daniels | `docs/VORGABEN_WELTEN_UND_BOTS_20261103.md` (Hauptdorf bleibt in seiner Welt, nur Nebendoerfer wechseln, Kampf ueber Weltgrenzen unbezahlbar, Bots rauben auch untereinander) | Chat 12:35 bis 12:40 |

## Der EINE naechste Schritt

**S-5 Ausbildung je Ort** (Daniels Reihenfolge von 12:20): Warteschlange statt Kauf
(`spielschicht.ausbilden`); damit zieht die Armee in die Doerfer und isst dort (`bot_futter_buchen`
isst heute nur im Hauptdorf, `dorf.einheiten` ist leer). Danach S-6 Nachgruenden, S-7 Karawanen, S-9
Stil je Taktik. **Der Sammellauf gehoert zum Abschluss jedes Code-Schnitts** - und das Protokoll
traegt die Kennung.

**Befunde, die dabei nicht untergehen duerfen** (gemessen 12:41, Belege in der Vorgaben-Datei):
`_bot_doerfer_im_raster` filtert NICHT nach Welt, und die sechs gelieferten Burgen
(`assets/icons/burgen/`) sind nicht auf der Karte - dort steht ein brauner Kasten mit X.

# STAND 03.11.2026, 12:25 - Sitzungsende: vier Entscheidungen, naechster Schnitt ist das Zeitmodell

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Stand ist gruen und die Richtung entschieden.** Voller Sammellauf 143 von 145 (0 rot), alle
Arbeit committet, kein Prozess offen. Die vier offenen Fragen hat Daniel beantwortet; sie gelten ab
jetzt und sind hier woertlich festgehalten.

| Nr | Frage | Antwort Daniel (woertlich) | Folge |
|---|---|---|---|
| 1 | Altname `deepseek-v4-flash` in der Config | "Ja, umstellen (Altname raus, ueberall derselbe Name)" | `auxiliary.mcp.model` = `deepseek-flash`, ueber die CLI gesetzt, Sicherung + Protokoll |
| 2 | Diebstahl-Zahlen (dünn ≤ 5, 3 %, 60/120, 12 h) | "So lassen (Schwelle 5, 3 %, 60/120, 12 h)" | `data/bot_diebstahl.json` bleibt wie es ist |
| 3 | Wie wird der Bot-Takt zeitlich deterministisch? | "Ereignis-Splitting wie beim Spieler (`spieloekonomie.tick_bis`) - groesserer Umbau, aber eine Wahrheit" | **naechster Schnitt:** Bot-Takt ueber `tick_bis` statt eigener Bucket-Logik |
| 4 | Naechster fachlicher Schnitt danach | "S-5 Ausbildung je Ort (Warteschlange statt Kauf; Armee zieht in die Doerfer und isst dort)" | nach dem Zeitmodell: S-5, dann S-6, S-7 |

## Der EINE naechste Schritt

**Bot-Takt auf `spieloekonomie.tick_bis` umstellen** (Daniels Entscheidung 3 von heute): die
Bot-Aktionen laufen dann durch DIESELBE Ereignis-Zerlegung wie die Spielersiedlungen, und
`1 × 3600 s` gegen `10 × 360 s` fuehrt zu denselben Takten. Erst danach kann `data/bot_diebstahl.json`
auf `aktiv: true` (S-12 steht fertig, Register 161) - und danach S-5 Ausbildung je Ort.

**Was dafuer zu beachten ist:** `tick_bis` arbeitet auf `orte` (dict) und `missionen` und liefert
`(orte, missionen, wissen, zeit, ereignisse)`; der Bot-Takt heute arbeitet auf `BotPlayer`-Objekten und
`self.settlements`. Die Umstellung braucht deshalb eine Uebersetzung in BEIDE Richtungen
(`bot_dorf_als_ort` / `bot_dorf_aus_ort` gibt es schon) und eine Wache, die genau die Gleichheit
`1 x 3600 == 10 x 360` fuer die Bot-Aktionen prueft - heute ist sie fuer den Spieler geprueft, nicht
fuer die Bots.

# STAND 03.11.2026, 11:45 - S-12: Diebstahl mit Bericht GEBAUT, Schalter bleibt AUS (Register 161)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Mechanik steht, die Zeit stimmt noch nicht.** Daniels Entscheidung 7 ("Ja, aber nur mit Bericht
im Postfach") ist gebaut: duenne Bots bestehlen wehrlose Orte, jeder Fall wird als Nachricht mit wer,
wann, was, wieviel ins Postfach gelegt. **Eingeschaltet ist sie nicht** - und der Grund ist gemessen,
nicht geraten.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `9865f73` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **143 von 145 gruen, 0 rot, 2 ausgesetzt, 5.742 Pruefungen, 429 s** (Start 11:43, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1143.log` |
| Pruefdateien / Register / Quelldateien | **145** / **161** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_diebstahl.py` **36/0/1** | eigener Lauf |
| Mechanik, gemessen | je Rohstoff 3 Prozent (1000/500/200 -> **30/15/6**), Deckel 60 je Rohstoff und 120 gesamt halten, Ziel nie unter 0, Bot-Hauptdorf bekommt genau die Mengen | `test_bot_diebstahl.py` |
| Bedingungen, gemessen | Garnison im Ziel -> **kein** Diebstahl; starker Bot (>5 Einheiten) -> **kein** Diebstahl; Sperre 12 h haelt, danach wieder; leerer Ort und Deckel 0 -> nichts | `test_bot_diebstahl.py` |
| Warum aus | Bot-Takt feuert je nach Tick-Zuschnitt einmal oder keinmal: **1 x 3600 s und 10 x 360 s** fuhren unterschiedlich viele Bot-Aktionen, sobald der Diebstahl das Spielerlager beruehrt (`test_gpt_fixrunde_ortslager_zeit` 98,79 gegen 105,0) | `data/bot_diebstahl.json`, Feld `warum_noch_aus` |

**Zwei Reparaturversuche, beide zurueckgenommen** (Reichsanzeige nachziehen; Takt nach ganzen
Abschnitten feuern): sie aenderten Verhalten, ohne das Problem zu loesen. Der saubere Weg ist ein
eigenes, scheiben-unabhaengiges Zeitmodell fuer Bot-Aktionen - **das ist die offene Entscheidung.**

## Der EINE naechste Schritt

**Bot-Takt auf feste Spielzeit-Punkte stellen** (statt "wenn die Fliesskomma-Differenz reicht"): jeder
Takt hat einen festen Abschnitt, 1 x 3600 s und 10 x 360 s fahren dieselben Takte. Erst damit sind
Bot-Aktionen scheiben-unabhaengig - und der Diebstahl kann eingeschaltet werden. Danach: **S-5
Ausbildung je Ort**, **S-6 Nachgruenden**, **S-7 Karawanen**.

# STAND 03.11.2026, 11:10 - S-11: der Journal-Deckel haelt (500 Zeilen je Ort, Register 160)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das `produktionsjournal` waechst nicht mehr ins Unendliche.** Daniels Entscheidung 9: 500 Zeilen je
Ort, aelteste fallen weg - fuer Spieler UND Bots, denn beide schreiben durch dieselbe Stelle. Gedeckelt
wird an Ort und Stelle, damit das Versorgungsfenster und der Spionagebericht unveraendert weiterlesen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `6aabe37` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **142 von 144 gruen, 0 rot, 2 ausgesetzt, 5.700 Pruefungen, 389 s** (Start 11:02, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1102.log` |
| Pruefdateien / Register / Quelldateien | **144** / **160** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_journal_deckel.py` **23/0/1** | eigener Lauf |
| Deckel, gemessen | 600 Zeilen -> **500** (neueste bleibt, aelteste 100 weg); 520 Stunden-Spannen durch `ort_tick` -> genau **500**, erste Zeile ab 72.000 s; unter dem Deckel aendert sich nichts | `test_journal_deckel.py` |
| Versorgungsfenster danach | **24 von 24** Stundenzeilen vorhanden, dieselben Zahlen (Holz 327,6 / Stein 296,4 / Nahrung 288,0 / Gold 216,0) | `test_journal_deckel.py` |
| Bot-Weg (`ertrag_weg = karte`) | 520 Spannen -> **500** Zeilen, letzte Zeile traegt ihren `verbrauch` | `test_journal_deckel.py` |

**Ehrliche Grenzen:** (a) gedeckelt wird nur das Journal - Vorraete und alle anderen Buecher bleiben
unberuehrt; (b) ein Deckel KLEINER als das Versorgungsfenster wuerde dem Fenster Zeilen nehmen (bei 500
nicht der Fall: 500 Zeilen = rund 20 Spieltage bei stündlichem Takt); (c) alte Spielstaende mit mehr als
500 Zeilen werden erst beim naechsten Tick gekuerzt, nicht beim Laden.

## Der EINE naechste Schritt

**Diebstahl mit Postfach-Bericht** (Daniels Entscheidung 7): duenne Bots duerfen den abwesenden Spieler
bestehlen, **jeder Fall als Nachricht ins Postfach** (wer, wann, was, wieviel) - kein stiller Verlust.
Eigener Schnitt nach S-6 im Konzept. Danach: **S-5 Ausbildung je Ort** (Warteschlange statt Kauf - damit
zieht die Armee in die Doerfer und isst dort), **S-6 Nachgruenden** (3 je Bot), **S-7 Karawanen**.

# STAND 03.11.2026, 10:26 - S-10: der BEDARF je Rohstoff, die Kartenwahl steht auf "mittel" (Register 159)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots waehlen ihre Karten jetzt nach ihrem BEDARF.** Daniels Entscheidung 4 verlangte genau das:
erst einen Bedarf je Rohstoff bauen, dann `kartenwahl_stufe` von `schwer` auf `mittel` stellen. Bis
heute kannte das Spiel nur EINEN laufenden Verbrauch - Nahrung der Garnison (8 je Einheit und Tag);
alles andere wird sofort bezahlt. Jetzt rechnet `bot_rohstoffbedarf` den Bedarf je STUNDE (dieselbe
Einheit wie die Ertraege der Karten) aus dem, was das Spiel schon fuehrt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `0e48fce` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **141 von 143 gruen, 0 rot, 2 ausgesetzt, 5.677 Pruefungen, 392 s** (Start 10:18, nach dem letzten Fix) | `docs/audits/sammellauf_20261103_1018.log` |
| Pruefdateien / Register / Quelldateien | **143** / **159** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_bedarf.py` **25/0/1** | eigener Lauf |
| Umgestellte Wachen | `test_kartenwahl_bot` **22/0/0** (Nutzen-Zweig jetzt explizit `stufe="schwer"`, neuer Abschnitt 6 fuer "mittel"), `test_bot_dorf_als_ort` **32/0/0** (Karte fuer die Zaehlung fest gesetzt) | eigene Laeufe |
| Bedarf, gemessen | 10 Einheiten = 80 Nahrung/Tag = **3,3333/h**; offener Gauner-Auftrag = **10,4167 Gold/h** + 0,0417 Siedler/h; Baukunst Stufe 1 = **2,0833 Holz/h**, Stufe 2 = 4,1667; zwei Dolche = 0,1667 Metall/h | `test_bot_bedarf.py` |
| Wirkung auf die Karte | **3 von 5 Bots** bekommen mit "mittel" eine andere Karte als mit der reinen Gold-Regel; die Mangel-Achse entscheidet (Probe: `original-108`) | `test_kartenwahl_bot.py` |

**Ehrliche Grenzen:** (a) der Bedarf ist eine **Planungsgroesse** (was das Dorf in 24 h bezahlen will),
keine Verbrauchsmessung - verbrauchte Mengen stehen weiter im `produktionsjournal`; (b) **Bauten zaehlen
nicht** mit (einmalige Ausgabe, eigene Entscheidung noetig); (c) die Aenderung wirkt nur auf die
**Kartenwahl**, nicht auf die Wirtschaft; (d) das Fenster (24 h) ist eine VORSCHLAG-Zahl in
`data/bot_bedarf.json` - das Original nennt keinen Planungshorizont.

## Der EINE naechste Schritt

**Journal-Deckel: `produktionsjournal` auf 500 Zeilen je Ort** (Daniels Entscheidung 9), Spieler UND
Bots gleich, aelteste Zeilen fallen weg, mit Wache: der Deckel greift und das Versorgungsfenster rechnet
weiter. Danach in dieser Reihenfolge: **Diebstahl mit Postfach-Bericht** (Entscheidung 7), **S-5
Ausbildung je Ort** (Warteschlange statt Kauf - damit zieht die Armee in die Doerfer und isst dort),
**S-6 Nachgruenden**, **S-7 Karawanen**.

# STAND 03.11.2026, 08:46 - S-4: die Bots FORSCHEN, ihre Taktiken trennen sich (Register 158)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus "gebaut bleibt 0" und "geforscht bleibt 0" sind echte Staende geworden.** Ein Bot-Dorf forscht
jetzt mit SEINEN Rohstoffen, durch DIESELBE Funktion wie der Spieler (`spieloekonomie.forschung_start`):
Voraussetzungskette geprueft, Preis aus dem Dorflager gebucht, Dauer aus den Spieldaten, Abschluss
genau einmal. Die Reihenfolge kommt aus dem Stil der Taktik (`data/bot_forschung.json`, Daniels
Entscheidung 2). Erst damit wird `nach_baukunst` nutzbar - Wall, Lager, Schmiede, Akademie und
Diebesgilde stehen jetzt hinter Baukunst, nicht hinter einem Verbot.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `35df468` plus diese Doku | `git log --oneline -1` |
| Voller Sammellauf | **140 von 142 gruen, 0 rot, 2 ausgesetzt, 5.653 Pruefungen, 385 s** (Start 08:38, auf dem CODE-Stand von S-4) | `docs/audits/sammellauf_20261103_0838.log` |
| Pruefdateien / Register / Quelldateien | **142** / **158** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_forschung.py` **57/0/1** | eigener Lauf |
| Umgestellte Wachen | `test_bot_bauen` **35/0/2** (S-4-Befund aufgeloest), `test_bot_takt_kern` **26/0/1** (prueft den Kern-Aufruf mit Wissensstand) | eigene Laeufe |
| Wirkung, gemessen | 120 Bot-Takte x 5 Bots (30 Spielstunden) in **2,43 s**; danach: Pluenderer Baukunst 1 / Heimlichkeit 1 / Wagenbau 1 / Felderwirtschaft 3 / Kriegskunst 2 (Lager, Schmiede, Akademie), Waechterin Baukunst 3 / Verteidigungsanlagen 3 (Wall, Bogenbauer), Bastionier Baukunst 3 / Felderwirtschaft 3 / Verteidigungsanlagen 1 (Wall, Schmiede), Spaeherin Heimlichkeit 3 (Diebesgilde, Bogenbauer), Raecher Kriegskunst 3 (Schmiede, Akademie) | Dauerspiel-Probe |
| Kosten/Dauer belegt | Stufe 1 = **50 Holz**, je Stufe das Doppelte; Dauer = Stufe zum Quadrat in Stunden; gemessen: Baukunst Stufe 1 kostet genau 50 Holz aus dem Dorflager | `spieldaten.forschungs_kosten`, `test_bot_forschung.py` |

**Ehrliche Grenzen:** (a) die Bibliothek eines Bots bleibt auf **Stufe 1** - Ausbauen ist noch nicht
gebaut, deshalb sind alle Forschungen mit "Bibliothek 2/3/5/6" gesperrt und stehen als
`nach_bibliothek` in der Datendatei; (b) die Forschung wirkt nur ueber den **Kern-Weg** des Takts
(`bot_dorf_tick` bekommt jetzt den Wissensstand) - auf dem Vorgabe-Weg `ertrag_weg = karte` rechnet
der Bot weiter mit dem Kartenprofil, dort aendert Forschung den Ertrag **nicht**; (c) die Reihenfolge
je Taktik ist eine begruendete Setzung dieser Sitzung, keine Originalregel; (d) **Ausbilden** (S-5)
fehlt weiter - die Bots haben jetzt Akademie und Gilde, aber noch keine Warteschlange.

## Der EINE naechste Schritt

**Bedarf je Rohstoff** (Daniels Entscheidung 4): den Verbrauch je Rohstoff fuehren und messen. Erst
damit darf `kartenwahl_stufe` auf `mittel` gestellt werden - heute faellt `mittel` auf die Gold-Regel
zurueck, weil das Spiel keinen Bedarfsbegriff kennt. Danach in dieser Reihenfolge: **Journal-Deckel**
500 Zeilen je Ort (Entscheidung 9), **Diebstahl mit Postfach-Bericht** (Entscheidung 7), **S-5
Ausbildung je Ort** - und damit die Voraussetzung dafuer, dass die Bot-Armee aus den Doerfern statt
aus der Kasse kommt.

# STAND 03.11.2026, 04:08 - S-3: die Bots BAUEN, ihre Siedler stehen an einem Ort (Register 156)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus "gebaut bleibt immer 0" sind echte Gebaeude geworden.** Ein Bot-Dorf baut jetzt durch
DIESELBE Funktion wie der Spieler (`spielschicht.bauen`): freies Feld, Gelaende-Eignung, Preis aus
`data/baupreise.json`, Abbuchung aus seinem eigenen Dorflager. Die Reihenfolge kommt aus dem Stil
der Taktik (`data/bot_bauplan.json`). Dazu ein Befund, der beim Bauen sofort biss: ein Bot fuehrte
Siedler an ZWEI Stellen (Rohstoff im Lager und Bevoelkerung) - jetzt nur noch in `bevoelkerung`,
und die Armee bezahlt ihre Siedler von dort.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `056e693` plus diese Aenderung (Commit folgt) | `git log --oneline -1` |
| Voller Sammellauf | **139 von 141 gruen, 0 rot, 2 ausgesetzt, 5.592 Pruefungen, 281 s** (Start 04:03, auf dem CODE-Stand dieser Aenderung) | `docs/audits/sammellauf_20261103_0403.log` |
| Pruefdateien / Register / Quelldateien | **141** / **156** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_bauen.py` **32/0/2** | eigener Lauf |
| Wirkung, gemessen | 48 Bot-Takte in **1,65 s**; jeder der fuenf Bots **15 Gebaeude** (12 Grundanlagen + 2 Haeuser + 1 Bibliothek), `dorf.gebaut` = 3, Bevoelkerung **20** (10 + 2 x 5 aus den Haeusern), Armee 4-8 aus dem Siedlerzuwachs; ein Haus kostet genau **80 Holz / 50 Stein** | `test_bot_bauen.py`, Dauerspiel-Probe |

**Ehrliche Grenzen:** (a) `nach_baukunst` (Wall, Lager, Schmiede, Akademie, Diebesgilde, Bogenbauer)
wird NICHT gebaut - die belegte Regel `regeln.ohne_forschung_baubar` nennt nur Holzaeller,
Steinmetze, Jaeger, Bibliothek und Haeuser, und Bots forschen noch nicht (S-4); (b) das **Lager**
traegt in `data/buildings.json` "keine belegt", steht aber nicht in dieser Regel - der Plan laesst
es vorsichtshalber hinter Baukunst, statt eine belegte Regel zu umgehen; (c) **Ausbauen** (Stufen)
ist noch nicht gebaut, nur Bauen; (d) die fuenf Stile unterscheiden sich beim Bauen heute nicht,
weil ihnen die Forschungsregel dieselben zwei Gebaeude laesst - das aendert S-4.

## Der EINE naechste Schritt

**S-4: die Bots FORSCHEN** - mit eigenen Rohstoffen, derselben Voraussetzungskette und derselben
Dauer wie der Spieler (`spielschicht.forschung_starten`, `forschung`-Modul, `forschungsauftrag` je
Ort). Erst damit wird `nach_baukunst` nutzbar, unterscheiden sich die Taktiken wirklich, und der
Kern-Tick bekommt seine Forschungsboni (heute geht dort ein leeres dict hinein).

Danach: **S-5** Ausbildung (Warteschlange je Ort, ersetzt den Kauf), **S-6** Nachgruenden (3 je Bot),
**S-7** Karawanen, **S-8** Reisekosten, **S-9** Stil je Taktik. **Fuer Daniel liegt genau eine
Entscheidung bereit:** `ertrag_weg` in `data/bot_wirtschaft.json` - `"karte"` (Vorgabe, B-4) oder
`"felder"` (Kern wie beim Spieler, Karte bestimmt dann nur die Bauplaetze).

# STAND 03.11.2026, 03:56 - S-2b: der Bot-Takt KANN auf dem Kern laufen - Vorgabe bleibt die Karte (Register 155)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Zwei Wirtschaften, ein Schalter.** Der Bot erntete weiter mit dem Kartenprofil mal Stunden, der
Spieler mit dem Kern aus seinen Feldern. Jetzt gibt es `ertrag_weg` in `data/bot_wirtschaft.json`:
`karte` (Vorgabe, **B-4** von Daniel) oder `felder` (derselbe Weg wie der Spieler, ueber
`spieloekonomie.ort_tick`). Der Felder-Weg ist gebaut und geprueft - **eingeschaltet ist er nicht**,
weil er eine Daniels-Entscheidung aendern wuerde.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `c9e698e` plus diese Aenderung (Commit folgt) | `git log --oneline -1` |
| Voller Sammellauf | **138 von 140 gruen, 0 rot, 2 ausgesetzt, 5.555 Pruefungen, 388 s** (Start 03:49, auf dem CODE-Stand dieser Aenderung; Protokoll- und Stand-Zeilen danach sind ohne Code) | `docs/audits/sammellauf_20261103_0349.log` |
| Pruefdateien / Register / Quelldateien | **140** / **155** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_takt_kern.py` **26/0/1** (der Befund ist die offene Entscheidung selbst) | eigener Lauf |
| Der gemessene Unterschied | Kartenprofil gegen Felder: `original-036` Holz **14,06** / Gold **5,7** gegen **12,35** / **9,0**; `original-096` **12,92** / **3,3** gegen **12,35** / **9,0**; `original-087` **12,16** / **3,6** gegen **12,35** / **4,5** (zwergisch) | `tests/test_bot_takt_kern.py` |
| Kern-Modus im echten Takt | 48 Bot-Takte in **1,3 s**, 12 Anlagen je Dorf, Siedlerzuwachs **0 -> 10**, 47 Journalzeilen je Dorf, keine Ausnahme | Dauerspiel-Probe mit umgestelltem Schalter |

**Warum der Schalter statt eines Umbaus:** mit drei Anlagen je Rohstoff liefert der Kern JEDER Karte
denselben Grundertrag (12,35/13,65/12,0/9,0 zwergisch) - die Karte bestimmte dann nur noch, was
gebaut werden KANN. Daniels Vorgabe B-4 lautet aber "die Karte bestimmt den Ertrag". Also: beide
Wege leben, die Datendatei entscheidet, kein Code. **Ein Wort von Daniel** (`"ertrag_weg": "felder"`)
schaltet um.

**Ehrliche Grenzen:** (a) der Kern bucht Nahrung nur fuer eine eigene Garnison (`dorf.einheiten`);
die Armee bleibt in `bot.army` und isst ueber `bot_futter_buchen` im Hauptdorf - bildet S-5
Einheiten je Ort aus, muss die Armee dorthin wandern, sonst isst sie zweimal; (b) die Forschung geht
als leeres dict in den Tick (S-4 fehlt), also ohne Forschungsboni; (c) Zeiten dieses Blocks aus
`date`/`stat`, nicht geschaetzt.

## Der EINE naechste Schritt

**S-3: der Bot BAUT und baut AUS - wie der Spieler.** Vorher muss ein Widerspruch aufgeloest werden,
der beim Bauen sofort beisst: ein Bot fuehrt Siedler an ZWEI Stellen - `BotDorf.bevoelkerung` (Kern,
waechst) und `vorraete["siedler"]` (Kaufweg, feste 10 aus dem Start). Die belegten Bau- und
Einheitenpreise verlangen Siedler. Vorschlag: Siedler nur noch in `bevoelkerung` fuehren, alte
Staende beim Laden uebernehmen, Kauf und Bau von dort bezahlen. Danach der Bauplan je Taktik in
`data/`.

# STAND 03.11.2026, 03:46 - S-2: die Bot-Armee isst, die Kaufbremse haelt (Register 154)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus drei fertigen Helfern ist eine Wirkung geworden.** Ein Bot-Dorf bucht seit heute den
Nahrungsverbrauch seiner Armee (dieselbe Rechnung wie beim Spieler, 8 je Einheit und Spieltag),
haelt die Kaufbremse ein (Tagesbedarf plus Reserve) und bekommt beim ersten Takt seinen Bauplan
gesetzt. Gebucht wird nur im Hauptdorf - ein Bot hat EINE Armee, nicht je Dorf eine Garnison.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `80eca7a` plus diese Aenderung (Commit folgt), Arbeitsbaum vorher leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **137 von 139 gruen, 0 rot, 2 ausgesetzt, 5.529 Pruefungen, 382 s** (Lauf 03:39, auf dem CODE-Stand dieser Aenderung; die Dokumentzeilen danach sind ohne Code) | `docs/audits/sammellauf_20261103_0339.log` |
| Pruefdateien / Register / Quelldateien | **139** / **154** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `ls src/*.py` |
| Neue Wache | `tests/test_bot_nahrung.py` **44/0/1** (der Befund ist gewollt: kein `siedler` aus der Ernte) | eigener Lauf |
| Wirkung, gemessen | 100 Einheiten = **800/Tag = 33,33 je Stunde**; Spieler (`ort_tick`) und Bot (`bot_futter_buchen`) auf denselben Verbrauch; Grenzfaelle **Soll deckt / Soll - 1 blockt / Soll + 1 deckt**; 200 Bot-Takte in **4,3 s** ohne eine unterdeckte Zeile | `tests/test_bot_nahrung.py`, Dauerspiel-Probe |

**Eigener Befund und behoben:** `bot_doerfer_bebauen` war NICHT idempotent - jeder Bot-Takt haette
drei weitere Anlagen je Rohstoff nachgelegt (nach 4 Takten 48 statt 12). Jetzt wird je Gebaeude nur
der fehlende Rest gesetzt (12 Anlagen, zweiter Aufruf 0). Eine alte Wache (`test_bot_dorf_als_ort`)
wurde rot, weil `bot_doerfer_karten_zuweisen` den Bauplan jetzt selbst setzt; sie prueft den Stand
danach und die Idempotenz - der Code wurde nicht zurueckgebogen.

**Ehrliche Grenzen (stehen auch in Register 154):** (a) der Anzeige-Weg `bot_dorf_ertrag` rechnet
weiter mit dem Kartenprofil, der Kern mit den Feldern - die Luecke schliesst erst S-2b; (b) die
Ernte liefert keinen Posten `siedler`, die belegten Preise verlangen ihn, also kauft ein Bot heute
nur aus seinem Startvorrat (loest S-5, Ausbildung je Ort); (c) das Hauptdorf isst allein, waehrend
die Kaufbremse die GANZE Kasse sieht (Nachschub ist S-7, Karawanen); (d) das
`produktionsjournal` waechst wie beim Spieler unbegrenzt (eine Zeile je Stunde und Ort).

## Der EINE naechste Schritt

**S-2b: der Takt laeuft ganz auf `ort_tick`** (Ernte, Siedlerzuwachs, Journal aus dem Kern) und
`bot_dorf_ertrag` rechnet denselben Weg wie der Kern. **Achtung, hier haengt eine Entscheidung
dran** (Frage 8.1 der Uebergabe): mit drei Anlagen je Rohstoff liefert der Kern fuer JEDE Karte
denselben Grundertrag - die Karte bestimmt dann nur, was gebaut werden KANN. Das ist eine
Aenderung gegenueber **B-4** ("die Karte bestimmt den Ertrag", Daniels Vorgabe). Vorschlag: den
Felder-Weg bauen, aber hinter einem Schalter in `data/bot_wirtschaft.json` (`ertrag_weg`), Vorgabe
zunaechst `karte` - dann entscheidet Daniel mit EINEM Wort, ohne Codeaenderung.

Danach in der Reihenfolge des Konzepts: **S-3** Bauen/Ausbauen nach Taktik, **S-4** Forschung,
**S-5** Ausbildung, **S-6** Nachgruenden (3 je Bot), **S-7** Karawanen, **S-8** Reisekosten,
**S-9** Stil je Taktik.

# STAND 03.11.2026, 02:45 - V-6: die Bot-Kartenwahl folgt jetzt einer Regel (Register 151)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**`botkern.oekonomie_kartenwahl` ist angeschlossen.** Die Funktion stand fertig im Kern und hatte
keinen Aufrufer - die Karte eines Bot-Dorfes kam allein aus der Gold-Regel. Jetzt entscheidet die
Stufe aus `data/bot_wirtschaft.json` (`kartenwahl_stufe`, heute `schwer` = hoechster Portfolio-Nutzen)
unter denselben drei reproduzierbaren Kandidaten; der Bot geht mit seinem Portfolio und seinen
Stundenertraegen hinein. Die Gold-Regel bleibt Rueckfall, damit kein Dorf ohne Karte und ohne Ertrag
bleibt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `d754624`, Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **135 von 137 gruen, 0 rot, 2 ausgesetzt, 5.448 Pruefungen, 415 s** | `docs/audits/sammellauf_20261103_0239.log` |
| Pruefdateien / Register / Quelldateien | **137** / **151** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `test_projektpfade` |
| Neue Wache | `tests/test_kartenwahl_bot.py` **19/0/0** | eigener Lauf |
| Wirkung, gemessen | 3 Doerfer in **0,03 s**; Abweichung zur Gold-Regel bei **2 von 5** Bots (Grom: 2. Dorf `original-096` statt `original-087`); dieselbe Karte als ZWEITE Wahl **1,5349** statt **3,3118** wert | `test_kartenwahl_bot.py` |

**Ehrliche Grenze:** der Pfad "mittel" der Regel braucht einen BEDARF je Rohstoff - das Spiel fuehrt
nirgends einen Verbrauch. Deshalb steht die Stufe auf `schwer`; **welche Stufe gelten soll, ist
Daniels Entscheidung** (eine Zeile in der Datendatei, kein Code).

## Der EINE naechste Schritt

**Demo-Release vorbereiten** - der eingefrorene Umfang ist gebaut: Kernkreis, Spionage, Voelker- und
Kartenwahl am Start, Volksboni mit Wirkung, Bot-Kartenwahl nach Regel. Vorher Daniels Freigabe.
Danach: Kopplung Punkte/Kanaele und Balance-Messung (beide brauchen den Teiler-Entscheid),
Marktplatz-Motiv, und Bots gruenden weiterhin NICHT nach (offener Punkt: wann und womit).

# STAND 03.11.2026, 02:30 - V-5: die Volks- und Taktikboni WIRKEN (Register 149/150)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Aus der Anzeige ist eine Wirkung geworden.** Sechs Voelker und fuenf Taktiken hatten Plus und
Minus, gerechnet hat damit nichts. Seit heute rechnen Er traege (Bot und Spieler), Reisezeit, AT,
PA, Beute, Handelserloes und Ausbaupreis mit - die Zahlen stehen in `data/boni.json`, die
Datenschicht ist `src/boni.py`, die Anzeigetexte bleiben in `data/voelker.json` (eine Wache
vergleicht beide, damit sie nicht auseinanderlaufen).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `71abeba`, Arbeitsbaum leer | `git log --oneline -1`, `git status --porcelain` |
| Voller Sammellauf | **134 von 136 gruen, 0 rot, 2 ausgesetzt, 5.429 Pruefungen, 369 s** | `docs/audits/sammellauf_20261103_0224.log` |
| Pruefdateien / Register / Quelldateien | **136** / **150** / **55** | `ls tests/test_*.py`, `grep -c '^| [0-9]'`, `test_projektpfade` 113/0/0 |
| Neue Wache | `tests/test_boni.py` **82/0/0**, Gegenprobe `aktiv: false` -> 7 Fehler | eigener Lauf |
| Guthaben | von Daniel 01:44 abgelesen: **4,63 USD**, gesamt 45,36 USD. Budget der Sitzung 3 USD (21:18), davon rechnerisch 1,82 USD offen; Kontostand NICHT neu abgelesen | `docs/ENTWICKLUNGSPROTOKOLL.md` |

**Daniels Entscheidungen (Fragenrunde 01:47-01:52):** Ueberschneidung **additiv** (5 % + 5 % =
+10 %, nicht 10,25 %); Hoehe bleibt **5 %**; Taktikbonus gilt, solange die Taktik steht, nach einem
Wechsel **48 h gesperrt**; der **Spieler** bekommt dieselben Volksboni wie ein Bot; Gnome "Ausbau
+5 %" wirkt als **-5 % Gebaeudepreise**.

**13 Wirkungen, ehrlich gezaehlt:** 12 wirken (Holz/Stein/Nahrung/Gold je Volk, Reise und PA
elfisch, AT und Handel Trolle, PA Ghule, Baukosten und AT Gnome, dazu Beute Haug, Verteidigung
Brynhild, Reise Silra, AT Krank). **Eine wirkt nicht: Groms "Ausbau +5 %"** - die Bots haben keine
Bauwirtschaft; sie steht als `ohne_anker` in der Datei und wird nicht erfunden. AT wirkt nur im
Nahkampf; bei kleinen Preisen frisst die Ganzzahl-Rundung den Rabatt (8 Stein bleibt 8).

**Eigener Befund und behoben:** `spieler_fraktion` wurde beim LADEN nie zurueckgelesen - ein
geladener Stand verlor sein Volk (und damit seit heute die Wirkung). **Vom Sammellauf gefunden:**
drei Wachen (Bot-Wirtschaft, Kartenprofil, Spionage) wurden rot, weil sie Anzeige und Kern mit dem
alten Aufruf ohne `bot` verglichen; die Zusicherung "Anzeige = Kern" bleibt, sie ist jetzt mit
demselben Bot formuliert.

## Der EINE naechste Schritt

**Demo-Release vorbereiten** - der eingefrorene Demo-Umfang ist damit gebaut: Kernkreis, Spionage,
Voelker- und Kartenwahl am Start, Volksboni mit Wirkung. Vorher Daniels Freigabe. Danach die
offenen Punkte aus der letzten Uebergabe: Anschluss `botkern.oekonomie_kartenwahl` (hat keinen
Aufrufer), Kopplung Punkte/Kanaele und Balance-Messung (beide brauchen den Teiler-Entscheid),
Marktplatz-Motiv.

# STAND 03.11.2026, 01:08 - A2: sechs Voelker, der Spieler waehlt (Register 148)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Spieler hat jetzt ein Volk.** Sechs Fraktionen stehen in `data/voelker.json`: menschlich,
zwergisch, elfisch, Trolle, Ghule, Gnome - Trolle, Ghule und Gnome ersetzen die fruehere Fraktion
"monster" (Daniel 03.11.2026). Der Spieler waehlt im Dorfzentrum VOR der Kartenwahl; die fuenf Bots
bekommen die uebrigen Voelker, jedes genau einmal. Die Wahl steht im Spielstand und bleibt als Zeile
"Dein Volk: ..." sichtbar.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `8180140` plus dieser Schritt | `git log --oneline -1` |
| Datenquelle | sechs Fraktionen mit Plus, Minus, Beschreibung und Quelle je Wert | `data/voelker.json` |
| Code liest die Datei | Datenschicht `src/voelker.py` liest `data/voelker.json`; `bottaktik` fragt dort nach (es darf selbst keine Datei oeffnen); ohne Datei alter Rueckfallsatz | `src/voelker.py`, `src/bottaktik.py` |
| Neues Modul | `src/voelker.py`, Modulkarte auf 54 Dateien nachgezogen | `docs/MODULKARTE.md` |
| Verteilung | `verteile_fraktionen` - Bots nach Namen, Voelker in Datei-Reihenfolge, keine Doppelung | ebd. |
| Wache | `tests/test_voelkerwahl.py` **37/0/0** | eigener Lauf |
| Gegenprobe | Verteilung abgeschaltet -> rot (1 Fehler), Datei danach hashgleich | eigener Lauf |
| Umgestellte Wachen | `test_s7_botverhalten` ("genau die vier Fraktionen") und `test_botkern` ("monster") tragen die neue Entscheidung im Docstring | eigene Laeufe |
| Pruefdateien / Register | **135** / **148** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **133 von 135 gruen, 0 rot, 2 ausgesetzt, 5.351 Pruefungen, 415 s** | `docs/audits/sammellauf_20261103_0118.log` |

**Ehrlich zur Wirkung:** die Boni sind eine ANZEIGE. Kein Ertrag, keine Reise und kein Kampfwert rechnet
heute mit dem Volk - das ist Auftrag V-5 und braucht Daniels Pruefung des Entwurfs.

**Ehrlich zur Wache:** die erste Fassung zaehlte fuenf Bots fest. Der Startzustand hat je nach Lage zwei
bis fuenf Bots - die Wache war damit wackelig und prueft jetzt die REGEL (jeder vorhandene Bot traegt
eine Fraktion aus der Verteilung, keine doppelt) statt einer Zahl.

## Der EINE naechste Schritt

**Volksboni verdrahten (Auftrag V-5)** - der Entwurf liegt vor und ist geprueft. Vorher braucht es
Daniels Entscheid zu den Fragen aus V-5 (Ueberschneidung Silra/Krank, Hoehe der Wirkung, Sperrzeit).
Danach: Kopplung Punkte/Kanaele (C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

**Marktplatz:** braucht ein Motiv von Daniel (Motiv 2 "Kuppelbau" ist im Handbuch als nicht entscheidbar
vermerkt).

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Mit Register 148 ist die Voelkerwahl gebaut, die Kartenwahl mit Register 147 - es fehlt nur
noch die Wirkung der Volksboni.

# STAND 03.11.2026, 00:37 - A2-Vorstufe: der Spieler waehlt seine Startkarte (Register 147)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Startkarte war fest verdrahtet, jetzt waehlt der Spieler.** Solange keine Siedlung steht und
nichts gewaehlt ist, steht im Dorfzentrum ein eigener Block "Waehle deine Startkarte": drei mittlere
Karten mit ihren drei Achsen (Holz/Stein/Agrar) und einem Knopf je Karte. Der Block ERSETZT das
Dorfzentrum nicht - Pflichtkarte und Gruendungsknopf bleiben, und der Knopf gruendet ohne Wahl mit der
Standardkarte `original-036`. Die Kandidaten sind je Startsaat reproduzierbar, alle Zahlen stehen in
`data/startkarte.json`, die Wahl landet im Spielstand (`startkarte_gewaehlt`).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fd734ae` plus dieser Schritt | `git log --oneline -1` |
| Entwurf (starkes Modell) | `deepseek-v4-pro`, 30.987 Token (23.963 Denk), 13.824 Zeichen in 194 s | `docs/design/STARTKARTE_ENTWURF_20261103.md`, `docs/audits/usage_startkarte_20261103.json` |
| Eigene Korrekturen am Entwurf | Modell nahm Objekte statt Dicts an (`alle()` liefert Dicts); die Maske war als `TODO` offen und wurde selbst gebaut | `src/originalkarten.py`, `src/main.py` |
| Wache | `tests/test_startkartenwahl.py` **28/0/0** | eigener Lauf |
| Gegenprobe | Aufruf zurueck auf `startkarte(...)` -> **26 bestanden, 2 Fehler**, Datei danach hashgleich (`983f7df0...`) | eigener Lauf |
| Mitgezogen | `test_gebaeude_icons` 56/0/0, `test_ansicht_hintergrund` 81/0/0, `test_baseline` 40/0/0 | eigene Laeufe |
| Vom Sammellauf korrigiert | der erste Anlauf ersetzte das Dorfzentrum - `test_startspiel` und `test_gpt_pflicht_starthilfe_fix04f` wurden rot; jetzt ist die Wahl ein Block, die Zaehlwachen bleiben bei 3 | `tests/test_startspiel.py` 62/0/1, `test_gpt_pflicht_starthilfe_fix04f` 9 Tests OK |
| Pruefdateien / Register | **134** / **147** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **132 von 134 gruen, 0 rot, 2 ausgesetzt, 5.307 Pruefungen, 295 s** | `docs/audits/sammellauf_20261103_0049.log` |

**Der stehende Aufruf bleibt:** `_found_settlement()` und `_erste_siedlung_gruenden()` ohne Argument
gruenden weiterhin sofort mit der Standardkarte - 16 Pruefdateien mit 22 Aufrufstellen haengen daran.

**Ebenfalls fertig, aber NICHT eingebaut: der Voelkerwahl-Entwurf.** `deepseek-v4-pro` hat auf das Paket
`docs/auftraege/VOELKER_paket_20261103.md` in 124 s einen Entwurf geliefert (17.421 Zeichen, 18.203
Token) - `docs/design/VOELKER_ENTWURF_20261103.md`. Daniel hat die sechs Fraktionen vorgegeben
(menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome; die drei neuen ERSETZEN "monster"). Offen ist
seine Entscheidung zu Plus/Minus der drei neuen Fraktionen - jede Zahl dafuer waere sonst geraten.

## Der EINE naechste Schritt

**Den Voelkerwahl-Entwurf pruefen und einbauen** (A2): Daniels Entscheid zu Plus/Minus von Trollen,
Ghulen und Gnomen einholen, dann `data/voelker.json` mit Quelle je Wert anlegen, die Fraktion in den
Spielstand bringen (heute `botkern.BOT_FRAKTIONEN` fest, 4 Fraktionen fuer 5 Bots, `menschlich` doppelt),
die Startwahl ins Startfenster neben die Kartenwahl setzen und die fuenf Bots die uebrigen Fraktionen
bekommen lassen - ohne Doppelung. Danach voller Sammellauf, Protokollzeile, ein Commit.

**Danach:** Volksboni verdrahten (Auftrag V-5 liegt vor, wartet auf Daniels Pruefung), Kopplung
Punkte/Kanaele (C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).
**Marktplatz:** braucht ein Motiv von Daniel (Motiv 2 "Kuppelbau" ist im Handbuch als nicht entscheidbar
vermerkt) - ohne Zuordnung wird dort nichts gebaut.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

# STAND 03.11.2026, 00:05 - Stufe M-6: die Forschungszeilen passen ins Fenster (Register 146)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Befund aus Register 145 ist behoben.** Die Forschungszeile wurde von links nach rechts gepackt:
Name, Stufe und Beschreibung zuerst, Forschen-Knopf und Sperrgrund danach. Bei langen Beschreibungen
schob der Text die rechte Seite aus dem Fenster - im echten Fenster (1460 x 940, Inhaltsbreite 1052 px)
brauchten 14 von 14 Zeilen zwischen 1076 und 1903 px. Jetzt wird die rechte Seite ZUERST gepackt (der
Knopf bleibt ganz rechts) und die Beschreibung bricht mit `wraplength` um; Sperrgrund und
Freischalt-Text ebenso.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `2326863` plus dieser Schritt | `git log --oneline -1` |
| Messung vorher | 14 von 14 Zeilen ueber dem Platz: 1076 bis 1903 px bei 1052 px Inhaltsbreite | eigene Messfahrt (`winfo_reqwidth` je Kind) |
| Messung nachher | 21 von 21 Zeilen ohne Ueberlauf, kein Kind liegt ausserhalb (`winfo_x + winfo_width`) | eigene Messfahrt |
| Wache | `tests/test_ansicht_hintergrund.py` **81/0/0** (vorher 74; neuer Abschnitt 9) | eigener Lauf |
| Gegenprobe | Knopf wieder `side=LEFT` -> **79 bestanden, 2 Fehler**; Datei danach hashgleich (`84d62944...`) | eigener Lauf |
| Ansicht im Fenster | Forschung, Zeilen vollstaendig lesbar | `docs/design/M6_FORSCHUNG_ZEILEN_20261102.png` |
| Pruefdateien / Register | **133** / **146** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.278 Pruefungen, 335 s** | `docs/audits/sammellauf_20261102_2356.log` |

**Ehrlich zum ersten Bild-Beleg:** `docs/design/M5_FORSCHUNG_20261102.png` zeigt den Zustand VOR der
Behebung (abgeschnittene Beschreibungen) - es ist der Beleg zum Befund. `M6_FORSCHUNG_ZEILEN_20261102.png`
zeigt denselben Bildschirm nach der Behebung.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise - weiter mit Lager/Marktplatz** (Vorgabe Daniel
02.11.2026: "dann die uebrigen Textfelder", "stueck fuer stueck"). Erledigt sind Dorfzentrum, Forschung
und die drei Ausbildungsstaetten samt Warteschlange (Register 139, 142, 144, 145). Offen: Lager/
Marktplatz, Diplomatie, Nachrichten, Portal. Fuer diese Ansichten gibt es noch KEINEN Gebaeudehintergrund;
dort ist die Reihenfolge: erst `_ansicht_hintergrund` anlegen, dann die harten `tk.Label(... bg=...)`-
Bloecke auf `_kasten_label` umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in
`tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.

**Offene Frage an Daniel dazu:** diese vier Ansichten sind fast nur Tabellen - sollen sie ueberhaupt ein
Gebaeudemotiv als Hintergrund bekommen (Empfehlung: Lager und Marktplatz ja, Diplomatie und Nachrichten
nein, Portal pruefen), oder bleiben sie reine Datenansichten mit harten Bloecken?

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 23:45 - Stufe M-5: Titel und Einleitung der Forschung liegen als weiche Felder auf dem Bild (Register 145)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Forschung war die letzte Ansicht mit Bibliotheks-Hintergrund, die noch harte Balken trug.** Titel
("Forschung") und Einleitungssatz liegen jetzt als abgerundete Felder auf dem Motiv; die Forschungszeilen
darunter bleiben ein deckender Block.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `9f2d300` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Zeilen | 2 in `main._render_research` (Titel, Einleitung) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **74/0/0** (vorher 67; neuer Abschnitt 8) | eigener Lauf |
| Gegenprobe | Titel zurueckgebaut -> **71 bestanden, 3 Fehler**; Datei danach hashgleich (`7d27229a...`) | eigener Lauf |
| Ansicht im Fenster | Forschung mit Bibliotheksmotiv | `docs/design/M5_FORSCHUNG_20261102.png` |
| Pruefdateien / Register | **133** / **145** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.276 Pruefungen, 332 s** | `docs/audits/sammellauf_20261102_2347.log` |

**BEFUND, gemessen und NICHT in diesem Schritt behoben:** die Forschungszeilen laufen ueber den rechten
Rand. In der Ansicht Forschung brauchen 14 von 14 Zeilen mehr Platz als die 1052 px Inhaltsbreite des
Fensters (1076 bis 1903 px; gemessen als Summe der `winfo_reqwidth` aller Kinder einer Zeile). Folge:
die Beschreibungen werden abgeschnitten, und bei den gesperrten Forschungen liegt der Grund-Text unter
dem "Forschen"-Knopf. Ursache ist die Pack-Reihenfolge der Zeile (die Knoepfe kommen NACH den linken
Texten), nicht die Umstellung der Textfelder. Im Bild-Beleg ist der Zustand zu sehen.

## Der EINE naechste Schritt

**Die Forschungszeilen in Ordnung bringen** (BEFUND aus Register 145): die rechte Seite einer Zeile
(Knopf, Restzeit, Sperrgrund) zuerst packen, dem Beschreibungstext eine `wraplength` geben, die sich aus
der Inhaltsbreite ergibt, und die Zeile messbar pruefen (Summe der `winfo_reqwidth` <= Inhaltsbreite,
wie in der Messfahrt dieser Sitzung). Danach voller Sammellauf, Protokollzeile, ein Commit.

**Danach weiter mit den uebrigen Textfeldern, stueckweise** - Lager/Marktplatz, Diplomatie, Nachrichten,
Portal. Fuer diese Ansichten gibt es noch KEINEN Gebaeudehintergrund; dort ist die Reihenfolge: erst
`_ansicht_hintergrund` anlegen, dann die harten `tk.Label(... bg=...)`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in `tests/test_ansicht_hintergrund.py`,
voller Sammellauf, Protokollzeile, ein Commit. **Offene Frage an Daniel:** sollen diese vier Ansichten
ueberhaupt ein Gebaeudemotiv als Hintergrund bekommen (sie sind fast nur Tabellen)?

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 23:40 - Stufe M-4: die Warteschlange der Ausbildung traegt weiche Textfelder (Register 144)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Kopf der Warteschlange und ihre zwei Hinweiszeilen liegen jetzt als abgerundete Felder auf dem
Gebaeudemotiv.** "In Arbeit: N Auftrag/Aufträge - insgesamt noch ...", der Leerfall "Keine Aufträge in
Arbeit." und die Reihenfolge-Erklaerung. Die Auftragszeilen selbst bleiben ein DECKENDER Block - sie
sind die Tabelle - und dieser Block entsteht nur noch, wenn wirklich Auftraege laufen (vorher blieb bei
leerer Schlange ein leerer Balken im Bild).

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `ee63126` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Zeilen | 3 in `main._ausbildung_warteschlange_zeichnen` (Kopf, Leerfall, Reihenfolge) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **67/0/0** (vorher 44; neuer Abschnitt 7 mit Quelltext- und GUI-Probe) | eigener Lauf |
| Gegenprobe | Kopfzeile zurueckgebaut -> **65 bestanden, 2 Fehler**; Datei danach hashgleich (`4f1fa54e...`) | eigener Lauf |
| Ansicht im Fenster | Kaserne mit zwei laufenden und einem wartenden Auftrag | `docs/design/M4_WARTESCHLANGE_20261102.png` |
| Pruefdateien / Register | **133** / **144** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.264 Pruefungen, 340 s** | `docs/audits/sammellauf_20261102_2334.log` |

**Ehrlich zum Beleg:** der erste Screenshot der Vorschau nannte eine von Hand gesetzte, erfundene
Einheiten-Kennung ("Kaempfer"). Die Zeilen nennen in Wahrheit den Anzeigenamen aus `data/units.json`
("Kämpfer"); das Bild wurde mit dem echten Namen neu aufgenommen. Kein Mangel im Spiel - ein Fehler in
meinen Vorschau-Daten.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise - weiter mit Lager/Marktplatz** (Vorgabe Daniel
02.11.2026). Die Warteschlange der Ausbildung ist erledigt (Register 144). Als naechstes: Lager und
Marktplatz, danach Diplomatie, Forschung (Restzeilen), Nachrichten und Portal. Fuer diese Ansichten gibt
es noch KEINEN Gebaeudehintergrund - dort ist die Reihenfolge: erst `_ansicht_hintergrund` anlegen (wie in
Dorfzentrum, Forschung und den drei Ausbildungsstaetten), dann die harten `tk.Label(... bg=...)`-Bloecke
auf `_kasten_label` umstellen, Tabellen deckend lassen, je Ansicht ein Eintrag in
`tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 22:55 - Stufe M-3: maximiertes Fenster in Ordnung - Leiste unverzerrt, Hintergrund bis zum Rand (Register 143)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Daniels Befund vom Desktop-Screenshot ist behoben.** Die Ressourcenleiste skaliert nicht mehr mit
der Fensterbreite: die Symbole bleiben in Originalgroesse, die zusaetzliche Breite entsteht durch
Wiederholung der gemalten Landschaft, die Hoehe bleibt 140 px. Der Gebaeudehintergrund liegt nicht
mehr fest bei 980 x 760, sondern fuellt den Inhaltsbereich und wird bei jeder Groessenaenderung in
der Zielgroesse neu gebaut.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `badba55` plus dieser Schritt | `git log --oneline -1` |
| Leiste | `rest_auffuellen: kacheln`; Skala bleibt 1,0, Hoehe 140 px, Luecken werden wiederholt | `data/ressourcenleiste.json`, `main.leiste_zusammensetzen` |
| Wache Leiste | Symbolkachel bei 2560/3440 px **pixelgleich** zum Original (Abweichung 0,00) | `tests/test_ressourcenleiste.py` **43/0/1** |
| Hintergrund | `relwidth=1/relheight=1`, `<Configure>` -> `_hintergrund_anpassen` -> `_hintergrund_bauen` (64-px-Schritte, 120 ms Ruhe) | `main._ansicht_hintergrund` |
| Wache Hintergrund | Abschnitt 6: Flaeche relativ gebunden, neues Mass 1664 x 960 baut ein Bild dieser Groesse | `tests/test_ansicht_hintergrund.py` **53/0/0** |
| Messung im maximierten Fenster | Leistenflaeche 1536 x 140, Leistenbild 1536 x 140, Hintergrundflaeche 1142 x 868 = Inhaltsbereich | eigene Messfahrt |
| Ansicht | Screenshot maximiert und Leiste bei 3832 px | `docs/design/M3_MAXIMIERT_20261102.png`, `docs/design/LEISTE_3832_NEU_20261102.png` |
| Pruefdateien / Register | **133** / **143** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.250 Pruefungen, 326 s** (23:04) | `docs/audits/sammellauf_20261102_2304.log` |
| Wache Luecken | `tests/test_leisten_luecken.py` **27/0/0** (Periode 48 px: die Luecke ist eine Wiederholung, keine Dehnung) | eigener Lauf |

**Was dabei entschieden wurde:** die P-3-Regel ("oberhalb von `skala_max` waechst das ganze Band
gleichmaessig bis `skala_hart`") ist mit Daniels Befund ueberholt. Die alten Wachen nagelten das
Wachstum fest und wurden mit Begruendung umgestellt - nicht der Code zurueckgebogen.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise** (Vorgabe Daniel 02.11.2026). Kandidaten in
dieser Reihenfolge: Warteschlange der Ausbildung (Kopfzeile und die zwei Hinweiszeilen),
Lager/Marktplatz, Diplomatie, Forschung (Restzeilen), Nachrichten und Portal.

Zu tun: je Ansicht die harten `tk.Label(... bg=self.skin["bg"])`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, Wachen nicht auf Wortlaut biegen sondern mitziehen, je Ansicht
ein Eintrag in `tests/test_ansicht_hintergrund.py`, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 22:40 - Stufe M-2: die Kastenoptik steht in Kaserne, Stellmacher und Diebesgilde (Register 142)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die drei Ausbildungsstaetten sehen aus wie Dorfzentrum und Forschung.** Titel, Einleitung,
Siedlerwarnung und der Spionage-Abschnitt liegen als abgerundete, weiche Felder auf dem
Gebaeudemotiv; zwischen den Feldern ist das Bild zu sehen. Die Tabellen (Einheiten, Warteschlange)
bleiben deckende Bloecke - genau die Trennung, die Daniel beschrieben hat.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `569fd36` plus dieser Schritt | `git log --oneline -1` |
| Umgestellte Bloecke | 8: Titel, Einleitung, "Keine Einheit", Siedlerwarnung (2 Zeilen), Spionage-Ueberschrift, Dorfzeile, Schwellen-Erklaerung | `main._render_ausbildung`, `_siedler_warnung_zeichnen`, `_spionage_abschnitt` |
| Zahlen | alle aus `data/gebaeude_motive.json` (Radius, Deckkraft, Farbe) | ebd. |
| Wache | `tests/test_ansicht_hintergrund.py` **44/0/0** (neu: Abschnitt 5 fuer alle drei Ansichten) | eigener Lauf |
| Nebengeprueft | `test_kaserne_ohne_gebaeude` 11/0/0, `test_siedler_warnung` 29/0/0, `test_gebaeude_icons` 56/0/0, `test_ausbildungsauftraege` 59/0/0 | eigene Laeufe |
| Ansicht im Fenster | Screenshot der Diebesgilde mit Feldern und sichtbarem Motiv | `docs/design/KASTEN_DIEBESGILDE_20261102.png` |
| Pruefdateien / Register | **133** / **142** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Ehrlich zur Optik:** die Felder sind abgerundet, aber sie wirken noch immer wie Balken - ein
weicher Verlauf ist bei 8 px Radius kaum zu sehen. Der naechste Feinschliff gehoert zu den uebrigen
Textfeldern; ein eigenes Darstellungs-Papier dafuer ist noch nicht geschrieben.

## Der EINE naechste Schritt

**Die uebrigen Textfelder der Ansichten, stueckweise** (Vorgabe Daniel 02.11.2026). Kandidaten in
dieser Reihenfolge: Warteschlange der Ausbildung (Kopfzeile und die zwei Hinweiszeilen),
Lager/Marktplatz, Diplomatie, Forschung (Restzeilen), Nachrichten und Portal.

Zu tun: je Ansicht die harten `tk.Label(... bg=self.skin["bg"])`-Bloecke auf `_kasten_label`
umstellen, Tabellen deckend lassen, Wachen nicht auf Wortlaut biegen sondern mitziehen, je Ansicht
ein Eintrag in `tests/test_ansicht_hintergrund.py` (Hintergrund zuerst, mindestens zwei Felder,
Text noch da), voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER, Volksboni
verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 21:45 - Stufe M-1: Truppenbewegungen sind auf der Weltkarte sichtbar (Register 141)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jeder laufende Auftrag hat jetzt eine Linie im Gelaendekaestchen.** Sichtbar ist nur das
Oeffentliche: Startfeld, Zielfeld, die Linie und die Bewegung darauf - als grobe Restzeit in einer
Zeile ueber der Karte und im Klickfenster (Vorgabe Daniel, Register 140). Truppenart, Anzahl,
Karren und die genaue Geschwindigkeit bleiben verborgen; laeuft ein Marsch auf eine EIGENE Siedlung
zu, steht die Wegzeit genau da. Entworfen hat die Darstellung das starke Modell (`deepseek-v4-pro`)
in drei Fassungen; eingebaut ist Fassung A.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `959e04a` plus dieser Schritt | `git log --oneline -1` |
| Entwurf (starkes Modell) | 278 Zeilen, drei Fassungen mit exakten Zahlen, Empfehlung A, Umsetzungsplan | `docs/design/MARSCH_ENTWURF_20261102.md`, `docs/audits/usage_m1_20261102.json` |
| Messung des Laufs | 10 Aufrufe, 757.216 Prompt-Token (656.640 aus dem Cache), 20.385 Antwort-Token, 12.585 Denk-Token | ebd. `usage_m1_20261102.json` |
| Vergleichsblatt | drei Fassungen, oben doppelt gross und unten in Originalgroesse (20 px je Feld) | `docs/design/MARSCH_VERGLEICH_20261102.png`, `tools/marsch_vergleich.py` |
| Zahlen der Anzeige | Symbol 6 px `#F59E0B`, Linie 2 px, Rueckreise `#38BDF8`, Marker hohl 8 px `#DAA520`, Takt 400 ms, Stufen 1/3/6 h, Toleranz 6 px | `data/marsch_optik.json`, `src/marsch_optik.py` |
| Zeichnen | vier Canvas-Objekte je Marsch, Tags `marsch` und `marsch_<n>`, Alte werden beim Rendern geloescht | `main._marsche_zeichnen` |
| Klick | erst Dorf, dann Marsch (6-px-Band um die Linie), dann Feld | `main._portal_klick`, `main._marsch_an` |
| Wache | `tests/test_marsch_optik.py` **63/0/0** | eigener Lauf |
| Voller Sammellauf | **131 von 133 gruen, 0 rot, 2 ausgesetzt, 5.224 Pruefungen, 357 s** (21:55) | `docs/audits/sammellauf_20261102_2155.log` |
| Pruefdateien / Register | **133** / **141** | `ls tests/test_*.py`, `grep -c '^| [0-9]'` |

**Zwei Befunde, offen benannt:** (1) `Settlement.x/y` liegt im ALTEN `MAPS`-Raster (20 nur bei
`kontinent`), dass das Portal-Raster dieselben Felder meint, ist nicht belegt - deshalb steht die
Aufloesung an einer einzigen Stelle (`main._marsch_felder`) und die Lesart ist VORSCHLAG.
(2) Bot-Doerfer tragen ihre Position erst nach `bot_doerfer_auffrischen_alle`; vorher liegt jedes
Dorf auf 0/0, und jede Wache, die ohne diesen Schritt zaehlt, prueft ein leeres Bild.

## Der EINE naechste Schritt

**Kastenoptik in Kaserne, Stellmacher und Diebesgilde** (Daniels Wahl aus der Fragenrunde 02.11.2026),
danach die uebrigen Textfelder der Ansichten - Vorgabe: stueckweise. Der Vorzustand ist gebaut und
geprueft (Register 139): das Gebaeudemotiv ist der Hintergrund, die Texte stehen in abgerundeten
Feldern davor; die drei Ausbildungsstaetten haben die Textfelder noch NICHT.

Zu tun: je Ansicht die Textbloecke auf `gebaeude_optik.kasten_bild` umstellen (wie Dorfzentrum und
Forschung), Zahlen nur aus `data/gebaeude_motive.json`, alte Wachen auf Wortlaut und Groesse
mitziehen, Pruefdatei erweitern, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026):** Kernkreis + Spionage + Voelker- und Kartenwahl
am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** uebrige Textfelder, Voelkerwahl am Start (A2), Kartenwahl fuer den
SPIELER, Volksboni verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele
(C), Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 20:59 - Stufe B-6: das Gebaeudemotiv ist der Hintergrund, Texte stehen davor (Register 139)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das gemalte Bild traegt jetzt die Ansicht - und zwar hinter dem Inhalt.** Dorfzentrum, Forschung
(Bibliothek) und die drei Ausbildungsstaetten legen das Motiv als eigene Flaeche an, die ZUERST
entsteht; die Texte liegen als abgerundete, fast deckende Felder mit warmem Braun und feinem Goldrand
darueber. Das Bild ist zurueckgenommen (38 % Abdunkelung, 2 px Weichzeichnen), damit der Text der
Vordergrund bleibt. Alle Zahlen stehen in `data/gebaeude_motive.json`.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `6bb6714`, darauf dieser Schritt | `git log --oneline -1` |
| Vergleichsblatt | drei Fassungen, Daniel hat **B** gewaehlt; danach "zu blickfangend" -> Bild zurueckgenommen | `docs/design/HINTERGRUND_VERGLEICH_20261102.png`, `tools/hintergrund_vergleich.py` |
| Flaeche | `gebaeude_optik.hintergrund_flaeche` deckt (cover, mittig beschnitten), optional weichgezeichnet/abgedunkelt | `src/gebaeude_optik.py` |
| Textfelder | `gebaeude_optik.kasten_bild` (abgerundet, Verlauf oben 248 / unten 205, Goldrand), `main._kasten_label` | ebd., `src/main.py` |
| Daten | `ansicht_hintergrund`: abdunkeln 38 %, weichzeichnen 2 px, Radius 14, Farbe 22/17/12 | `data/gebaeude_motive.json` |
| Ansichten | Dorfzentrum (`lager`), Forschung (`bibliothek`), Kaserne/Stellmacher/Diebesgilde (je Gebaeude); `_gebaeude_kopf` nur Rueckfall | `src/main.py` |
| Wache | `tests/test_ansicht_hintergrund.py` **29/0/0**; `test_gebaeude_icons` umgestellt **56/0/0** | eigene Laeufe |
| Pruefdateien / Register | **132** / **139** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Truppenbewegungen auf der Weltkarte sichtbar machen** (Vorgabe Daniel 02.11.2026, Vorbild Lords
Mobile; in der Fragenrunde ausdruecklich **vor** die Demo gesetzt). Heute zeigt das Portal-Kaestchen
Gelaende und die fremden Doerfer, aber keinen Marsch.

**Sichtbarkeitsregel (Vorgabe Daniel, Register 140) - sie ist der Kern des Schritts:**
sichtbar sind Startfeld, Zielfeld, die Linie und eine **grobe** Restlaufzeit. NICHT sichtbar sind
Truppenart, Anzahl, Karren und Ausruestung ("Ein einzelner handkarren erzeugt das gleiche
bewegungssymbol wie eine ganze armee"), und die genaue Geschwindigkeit bleibt verborgen, damit sie
die Einheit nicht verraet ("sieht man nur die grobe Wegzeit"). **Ausnahme (Nachtrag Daniel): laeuft
ein Marsch auf eine EIGENE Siedlung zu, wird die Wegzeit GENAU genannt** - "weil ich selbst betroffen
bin und die zeiten einschaetzen kann als spieler"; Truppenart und Anzahl bleiben auch dann verborgen,
die Geschwindigkeitsstufe wird nicht ausgewiesen. **Ein marschierender Verband ist kein Spionageziel**
- Spionage zielt auf ein Dorf. Eigene Auftraege bekommen auf der Karte dieselbe Darstellung; ihre
Einzelheiten stehen im Auftragsbuch/Postfach.

Zu tun: je laufendem Auftrag eine Linie im Kaestchen (eigenes Zeichen-Tag, Muster `portalbote`),
Anzeige aus `state.auftraege` gespeist (keine zweite Auftragsliste), Restzeit in groben Stufen,
Klick auf eine Linie zeigt, was oeffentlich ist (von, nach, Restzeit) - keine Truppenliste;
Pruefdatei mit Grenzfaellen (kein Auftrag = keine Linie, Ankunft = Linie weg, zwei Marsche
gleichzeitig, Uhr rueckwaerts), voller Sammellauf, Protokollzeile, ein Commit.

**Vorgehen (Vorgabe Daniel 02.11.2026): diesen Schritt plant und baut das GROSSE MODELL
(deepseek-v4-pro)** - vor allem die visuelle Darstellung waehrend der Bewegung (Symbol, Linie,
Puls/Richtung, Groesse) soll es entwerfen, nicht nur den Code schreiben. Erst ein kurzes
Darstellungs-Papier mit zwei, drei Fassungen (Bild), dann umsetzen. Kosten im Blick behalten
(hart 4 EUR/Tag ueber alle Modelle), Kontostand vorher nennen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Demo-Umfang ist eingefroren (Daniel 02.11.2026, Fragenrunde):** Kernkreis + Spionage + Voelker- und
Kartenwahl am Start. Alles andere kommt NACH dem ersten Demo-Upload.

**Danach in dieser Reihenfolge:** Kastenoptik in Kaserne/Stellmacher/Diebesgilde (Daniels Wahl), dann
die uebrigen Textfelder der Ansichten, dann Voelkerwahl am Start (A2), Kartenwahl fuer den SPIELER,
Volksboni verdrahten (A), Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C),
Balance-Messung (D), zuletzt Demo-Release (Freigabe Daniel).

# STAND 02.11.2026, 20:20 - Stufe B-5: Postfach und Spionage, gekoppelt an die Einheitenwerte (Register 138)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Es gibt jetzt ein Postfach mit Spionageberichten - und der Bericht haengt an den Einheiten.**
Wer ein fremdes Dorf ausspionieren will, schickt Kundschafter der Diebesgilde; ihre Werte
SI (Sinnesschaerfe) und HE (Heimlichkeit) ergeben den Aufklaerungswert, und der entscheidet, wie
viel der Bericht zeigt. Reicht die Aufklaerung nicht fuer den Wall, prallt der Auftrag ab: Verluste,
kein Bericht. Auf der Weltkarte stehen die fremden Doerfer jetzt als anklickbare Zeichen - ein Klick
bietet "Angriff planen" und "Spionage", beide fuehren in die Truppenauswahl.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `deeae88` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Neue Auftragsart | `spionieren` (fuenfte Art); nur fremdes Ziel, nur Spionageeinheiten, KEINE gemischte Truppe | `auftraege.py` |
| Aufklaerungswert | SI + HE je Einheit: Streuner 60, Gauner 95, Dieb 135, Meisterdieb 150, Kundschafter 175, Waldlaeufer 185; Kaempfer/Karren 0 | `spionage.aufklaerungswert`, `data/units.json` |
| Staffelung des Berichts | Truppen 25, Vorraete 50, Wall 75, Karte 100, Taktik 150 (VORSCHLAG) | `data/spionage.json` |
| Wall-Abwehr | Wallstufe x 20 x Zustand/100 (VORSCHLAG); abgewehrt = 50 % Verluste, kein Bericht | `spionage.abwehr_eines_dorfes`, `abwehr_pruefung` |
| Frist | **keine** - ein Bericht bleibt aktuell, bis ein neuer ueber dasselbe Dorf kommt (Vorgabe Daniel); er nennt seinen Stand und warnt, dass spaeter eintreffende Truppen fehlen | `data/spionage.json`, `spionage.bericht_zeilen` |
| Anzeige | Nachrichtentyp `spionage` (violett #A97BD6), Knopf "Spionagebericht oeffnen", eigener Veraltet-Hinweis | `main._render_messages`, `_spionage_bericht_anzeigen` |
| Weg im Fenster | Weltkarte (Portal-Kaestchen): fremde Doerfer als Zeichen, Klick -> Optionen -> Truppenauswahl; zweiter Einstieg Diebesgilde | `main._portal_klick`, `_bot_dorf_optionen`, `_truppen_auswahl` |
| Angriff auf ein Dorf | nimmt jetzt Wall und Wallzustand DIESES Dorfes | `main.kampf_am_ziel` (`ziel["dorf_name"]`) |
| Wache | `tests/test_spionage.py` **144/0/0**; drei Gegenproben wurden rot und die Dateien hashgleich zurueckgeschrieben | eigene Laeufe |
| Umgestellte alte Wachen | `test_auftraege` (vier -> fuenf Arten, "spionieren" war dort das Beispiel fuer eine unbekannte Art), `test_portal_uebersicht` (Klick laeuft ueber `_portal_klick`) | mit Begruendung im Kommentar |
| Voller Sammellauf | **129 von 131 gruen, 0 rot, 2 ausgesetzt, 5.131 Pruefungen, 287 s** (20:33) | `docs/audits/sammellauf_20261102_2027.log` |
| Pruefdateien / Register | **131** / **138** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Optik: die gemalten Gebaeudebilder werden der HINTERGRUND ihrer Ansicht, nicht ein Bild oben
drueber** (Vorgabe Daniel 02.11.2026, Screenshot in `docs/eingaben/20261102_Beispielansicht_Erklaerung_Hintergrund.png`).
Heute zeichnet `main._gebaeude_kopf` die Szene als 538 x 222 grosses Bild UEBER dem Inhalt
(Dorfzentrum, Bibliothek, Kaserne/Stellmacher/Diebesgilde). Richtig ist: die Szene liegt hinter dem
Inhalt und fuellt die Ansicht; die Textbloecke bleiben als kleine, DECKENDE Kaesten lesbar, dazwischen
bleibt das Bild sichtbar (Daniels Wortlaut: "kleinere textbloecke die nicht transparent sind und der
rest so transparent das moeglichst viel vom bild durchkommt"). Zu tun: eine Hintergrund-Ebene je
Ansicht, drei Fassungen als Vergleichsbild vorlegen (Vorgabe Daniel: Optik erst zeigen), Pruefdatei
fuer die Lesbarkeit der Textkaesten, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Truppenbewegungen auf der Weltkarte sichtbar machen (Vorgabe Daniel
02.11.2026, Vorbild Lords Mobile - eigene und fremde Marsche mit Richtung und Restzeit), Voelkerwahl am
Start (A2, sechs Voelker), Volksboni verdrahten (A, 13 Wirkungen), Kartenwahl fuer den SPIELER beim
Gruenden, Anschluss `botkern.oekonomie_kartenwahl`, Kopplung Punkte/Kanaele (C), Balance-Messung (D).

# STAND 02.11.2026, 19:46 - Stufe B-4: die Karte bestimmt den Ertrag (Register 137)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Jedes Bot-Dorf traegt jetzt eine Karte, und die Karte bestimmt seinen Ertrag.** Der Kartenwert wird aus
den FELDERN der Karte und den belegten Ertraegen je Gebaeude und Gelaende gerechnet - der starke Rohstoff
traegt viel, die schwaecher produzierbaren wenig oder gar nichts. Gold ist der Engpass: von 127 Karten
traegt genau eine kein Gold.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `dd3e4ed` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bot_karten_katalog`, `bot_kartenprofil`, `bot_kartenwahl`, `bot_doerfer_karten_zuweisen`, `bot_karten_uebersicht` | `src/main.py` |
| Traeger | `BotDorf.karte` (additiv; leer = alter Stand, bekommt die Karte beim ersten Bot-Takt) | ebd. |
| Kartenwahl | drei Kandidaten reproduzierbar aus Name und Dorfnummer, **Gold zuerst** (Daniel), Gleichstand ueber Gesamtwert und Kennung | `bot_kartenwahl` |
| Datendatei | `karten_aktiv`, `karten_teiler` 10 (VORSCHLAG), `karten_kandidaten` 3 | `data/bot_wirtschaft.json` |
| Gemessen | goldreichste Karte Gold 90 (original-001); **genau EINE Karte ohne Gold** (original-125); Werte je Rohstoff 0 bis 200 | Katalog + Profil |
| Wache | `tests/test_bot_kartenprofil.py` **37/0/0**; B-3-Wachen weiter gruen (52/0/0, 29/0/0, 33/0/0) | eigene Laeufe |
| Voller Sammellauf | **128 von 130 gruen, 0 rot, 2 ausgesetzt, 4.977 Pruefungen, 294 s** (19:18) | `docs/audits/sammellauf_20261102_1918.log` |
| Pruefdateien / Register | **130** / **137** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Postfach und Spionage** (Vorgabe Daniel, Vorbild Lords Mobile): der Spionageauftrag als eigene
Auftragsart, ein Bericht im Postfach, bezahlt aus Truppen, Gold und Reisezeit, und die Anzeige, die
Wallstufe, Taktik, Truppen, Items und Vorraete NUR dort zeigt. Die Schnittstellen stehen
(`bot_doerfer_uebersicht` offen, `bot_doerfer_spionagebericht` mit Karten- und Ertragsdaten); zu tun
sind der Auftrag, das Postfach und die Anzeige, eine Pruefdatei mit Grenzfaellen, ein voller
Sammellauf, eine Protokollzeile und ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Voelkerwahl am Start (A2, sechs Voelker), Anschluss von
`botkern.oekonomie_kartenwahl` an die Bot-Wahl nach Stufe, Verdrahtung der 13 Volksboni (A), Kopplung
Punkte und Kanaele (C), Balance-Messung (D).

# STAND 02.11.2026, 18:42 - Gesamtkonzept formuliert, Baustein fuer GitHub (Register 136)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Das Gesamtkonzept steht als Dokument.** Der eine Absatz aus dem Konzept (K-1, Abschnitt 10) ist zu einem
ausformulierten Papier geworden: was das Spiel ist, woraus es rechnet, was aus welchem Vorbild kommt, und
was noch fehlt - dazu ein fertiger Text fuer die spaetere GitHub-Beschreibung. Vorgabe Daniel: erst
formulieren, dann zeigen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `8c38228` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Dokument | `docs/GESAMTKONZEPT_20261102.md`, 11 Abschnitte, 9.493 Zeichen | `wc -c` |
| Kern | Inhalt aus Nebelseetal (Handbuch 2009), Raum aus Lords Mobile - nicht mehr und nicht weniger | Abschnitt 3 |
| Zahlen | 28 Einheiten, 17 Waren, 21 Forschungen, 127 Karten, 20 Dimensionen - jede mit Beleg abgezaehlt | Abschnitt 8 |
| Ehrlich offen | Kartenwahl je Gruendung, Voelkerwahl und 13 Volksboni, Spionage/Postfach, Bots gruenden nicht nach | Abschnitt 9 |
| GitHub-Text | About-Absatz plus README-Einstieg, fertig zum Einfuegen (noch NICHT veroeffentlicht) | Abschnitt 11 |
| Korrekturen Daniel (18:55) | **Doerfer werden NIE eingenommen** (nur angreifen, ausspionieren, ausraeumen); **Angriffstruppen nie am Zielort stationiert** (Angriff zu einem Zeitpunkt, dann Bericht, dann Rueckmarsch) | Abschnitte 1, 2, 4, 11; Konzept K-1 Abschnitt 10 |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.940 Pruefungen, 309 s** (18:56) | `docs/audits/sammellauf_20261102_1856.log` |
| Dokumentpruefungen | `test_textqualitaet` **325/0** (96 Dokumente), `test_projektpfade` **105/0**, `test_protokoll` 22/0/1, `test_zieluebergabe` 26/0 | eigene Laeufe |
| Pruefdateien / Register | **129** / **136** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel 02.11.2026): bei jeder Gruendung drei
Karten zur Wahl, die Karte bestimmt den maximal getragenen Rohstoff und die schwaecher produzierbaren,
Gold hat Vorrang; die Bots bilden diese Wahl ueber `botkern.oekonomie_kartenwahl` nach.** Zu tun: eine
Datendatei mit Kartenprofilen (starker, mittlere, schwacher Rohstoff), `bot_dorf_ertrag` liest das Profil
des Dorfes statt einer festen Rate, das Dorf haelt seine Karte, die Bot-Wahl bekommt ihren Aufrufer,
Pruefdatei mit Grenzfaellen, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Postfach und Spionage (die Schnittstelle steht schon), Voelkerwahl am
Start (A2, sechs Voelker), Verdrahtung der 13 Volksboni (A), Kopplung Punkte und Kanaele (C),
Balance-Messung (D).

# STAND 02.11.2026, 18:21 - Protokoll geteilt: Historie geschlossen, neues Heft ab heute (Register 135)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Vorgabe Daniel 02.11.2026: das Protokoll laeuft in einem neuen Dokument weiter.** Es gibt jetzt zwei
Hefte - eines mit der Historie bis heute, eines ab heute. Die Historie ist WORTGLEICH uebernommen (nichts
gekuerzt, nichts umgeschrieben), das aktive Heft beginnt mit dem 02.11.2026 und steht wieder weit unter
der Zielgroesse.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `d05e5c4` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Geschichtsheft | `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md` - **300 Zeilen**, geschlossen, wortgleich | `wc -l` |
| Aktives Heft | `docs/ENTWICKLUNGSPROTOKOLL.md` - **80 Zeilen** ab 02.11.2026 (KARTE-01/02, BOTDORF-01/02/03) | `wc -l` |
| Werkzeug | `tools/pruefe_protokoll.py`: 46 Commit-Kennungen, 0 unbekannt, **nichts verloren** gegen die Vor-Verdichtung | eigener Lauf |
| Wachen mitgezogen | `test_gpt_projektordnung` (ein aktives Heft + das Geschichtsheft), `test_protokoll` (Vollstaendigkeit gegen BEIDE), `test_gpt_portable_uebergabe`, `protokoll_sichern`, `projekt_ordnung_audit` | Quelltext der Wachen |
| Wache | `test_protokoll` **22/0/1**, `test_textqualitaet` **322/0** (95 Dokumente), `test_projektpfade` **105/0** | eigene Laeufe |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.940 Pruefungen, 261 s** (18:16) | `docs/audits/sammellauf_20261102_1816.log` |
| Pruefdateien / Register | **129** / **135** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Das Gesamtkonzept ausformulieren (Vorgabe Daniel 02.11.2026).** Der Absatz in
`docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 10, ist der Keim: Nebelseetal liefert Einheiten,
Kampf, Gebaeude samt ihren Funktionen, Dorfgruendung und die Karten; Lords Mobile liefert ausschliesslich
das Springen auf Koordinaten und die Anzeige der Doerfer auf diesen Koordinaten. Daraus wird der Baustein
fuer die spaetere GitHub-Beschreibung - erst formulieren, dann zeigen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel vom
02.11.2026), Postfach und Spionage (Vorbild Lords Mobile), Voelkerwahl am Start (A2, sechs Voelker),
Verdrahtung der Volksboni (A), Kopplung Punkte und Kanaele (C), Balance-Messung (D).
**Hygiene:** erledigt - das Protokoll ist geteilt (Register 135); die alte Zeile im B-3-Block
(Protokoll auslagern) ist damit abgeloest.

# STAND 02.11.2026, 18:10 - Stufe B-3: Wirtschaft je Bot-Dorf (Register 134)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Bots wirtschaften.** Jedes Bot-Dorf hat ein eigenes Lager und erwirtschaftet je Stunde drei Anlagen
je Grundrohstoff; die Kasse eines Bots ist nur noch die SUMME seiner Doerfer. Ein Spielstand von vorher
laedt ohne Fehler und verliert nichts.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `4741076` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bot_dorf_ertrag`, `bot_kasse`, `bot_kasse_setzen`, `bot_kasse_buchen`, `bot_doerfer_ernten` | `src/main.py` |
| Datendatei | `data/bot_wirtschaft.json` (Schalter, Anlagen je Dorf, Lagerdeckel 20.000) | ebd. |
| Ertrag | drei Anlagen je Grundrohstoff: **12 Holz / 12 Stein / 12 Nahrung / 9 Gold** je Stunde und Dorf (Daniel 02.11.2026) | `bot_dorf_ertrag` |
| Anzeige | Spionagebericht je Dorf mit Vorrat und Ertrag aus derselben Funktion; offene Uebersicht weiter ohne Vorrate | `bot_doerfer_spionagebericht` |
| Wache | `tests/test_bot_dorf_wirtschaft.py` **52/0/0** | eigener Lauf |
| Voller Sammellauf | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.933 Pruefungen, 276 s** (18:04-18:08) | `docs/audits/sammellauf_20261102_1804.log` |
| Pruefdateien / Register | **129** / **134** | `ls tests/test_*.py`, `grep -c` |
| Offen | Kartenprofil je Dorf (Vorgabe Daniel, Konzept Abschnitt 11), Postfach/Spionage, Voelkerwahl (A2), Boni (A), Kopplung (C), Balance (D), Protokoll 344 Zeilen auslagern | Konzept K-1 |

## Der EINE naechste Schritt

**Das Gesamtkonzept ausformulieren (Vorgabe Daniel 02.11.2026).** Der Absatz in
`docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 10, ist der Keim: Nebelseetal liefert Einheiten,
Kampf, Gebaeude samt ihren Funktionen, Dorfgruendung und die Karten; Lords Mobile liefert ausschliesslich
das Springen auf Koordinaten und die Anzeige der Doerfer auf diesen Koordinaten. Daraus wird der Baustein
fuer die spaetere GitHub-Beschreibung - erst formulieren, dann zeigen.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Kartenprofil je Bot-Dorf (Konzept Abschnitt 11, Vorgabe Daniel vom
02.11.2026), Postfach und Spionage (Vorbild Lords Mobile), Voelkerwahl am Start (A2, sechs Voelker),
Verdrahtung der Volksboni (A), Kopplung Punkte und Kanaele (C), Balance-Messung (D). **Hygiene:** das
Protokoll steht mit 344 Zeilen ueber der Zielgroesse 320 - auslagern, nicht streichen.

# STAND 02.11.2026, 16:58 - Stufe B-2: Dorf-Verhalten aus der Lage (Register 133)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Doerfer haben jetzt ein Verhalten.** Jedes Bot-Dorf bekommt eine feste Position und waehlt
sein Verhalten aus vier Lagen (Naehe, Staerke, Wall, Niederlage) - als festes Paket, mit 48 Stunden
Sperrzeit. Die Wahl ist deterministisch, nichts wird gewuerfelt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `98a9988` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Regel | `bottaktik.dorf_position`, `TAKTIK_GEWICHTE`, `dorf_taktik_bewerten/waehlen/setzen` | `src/bottaktik.py` |
| Bruecke | `GameState.bot_doerfer_auffrischen` im Bot-Takt eingehaengt | `src/main.py` |
| Anzeigegrenze | offen: Name, Position, Fraktion, Volkswerte - Taktik UND Wallstufe nur im Spionagebericht | `bot_doerfer_uebersicht` / `bot_doerfer_spionagebericht` |
| Wache | `tests/test_dorf_taktiken.py` **33/0/0** | eigener Lauf |
| Voller Sammellauf | **126 von 128 gruen, 0 rot, 2 ausgesetzt, 4.883 Pruefungen, 299 s** (16:51-16:56) | `docs/audits/sammellauf_20261102_1651.log` |
| Pruefdateien / Register | **128** / **133** | `ls tests/test_*.py`, `grep -c` |
| Offen | Wirtschaft je Dorf (B-3), Postfach/Spionage, Voelkerwahl (A2), Boni verdrahten (A) | Konzept K-1 |

## Der EINE naechste Schritt

**Stufe B-3: die Wirtschaft je Dorf.** Bisher ist der Vorrat des Bots EINE Kasse; je Dorf eigene
Vorraete, Erträge und Wall. Zu tun: eine Lesestelle fuer den Dorf-Ertrag (Kern und Anzeige aus
derselben Funktion), die Bot-Kasse als Summe der Doerfer (keine zweite Buchfuehrung), Migration
alter Spielstaende ueber die Vorgabewerte von `BotDorf`, Pruefdatei mit Grenzfaellen, voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Danach in dieser Reihenfolge:** Postfach und Spionage (Vorbild Lords Mobile, Vorgabe Daniel),
Voelkerwahl am Start (A2, sechs Voelker), Verdrahtung der Volksboni (A), Kopplung Punkte/Kanaele
(C), Balance-Messung (D). **Hygiene:** das Protokoll steht mit 334 Zeilen ueber der Zielgroesse 320
- auslagern, nicht streichen.

# STAND 02.11.2026, 17:15 - Stufe B-1: Bots tragen Doerfer (Register 132)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Die Voraussetzung fuer Dorf-Taktiken steht.** Jeder Bot traegt jetzt je Dorf einen eigenen
Datensatz (Taktik-Slot, Wall, Ausbauzaehler); die Doerfer entstehen aus den bisherigen
Siedlungsnamen, das erste ist das Hauptdorf. Ein alter Spielstand laedt ohne Ausnahme und verliert
nichts.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `74587fb` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Neu | `main.BotDorf`, `BotPlayer.doerfer`, `bot_doerfer_sicherstellen`, `bot_aus_stand` | `src/main.py` |
| Eingetragen | Kartenaufbau (`generate_map`) und Spielstand-Laden | beide Stellen im Quelltext |
| Wache | `tests/test_bot_doerfer.py` **27/0/1** (Befund = bewusster Zwischenstand) | eigener Lauf |
| Nebenbefunde | `test_s7_botverhalten` 45/0/0, `test_gpt_bot_angriffsplanung` 16/16 OK | eigene Laeufe |
| Voller Sammellauf | **125 von 127 gruen, 0 rot, 2 ausgesetzt, 4.850 Pruefungen, 284 s** (17:14-17:22) | `docs/audits/sammellauf_20261102_1714.log` |
| Pruefdateien / Register | **127** / **132** | `ls tests/test_*.py`, `grep -c` |
| Offen (bewusst) | Dorf-Vorraete sind noch NICHT fuehrend; Wirtschaft je Dorf = B-3 | Befund in der Wache |

## Der EINE naechste Schritt

**Stufe B-2: jedem Bot-Dorf eine Position auf der Karte und einen fuellbaren Taktik-Slot geben**
(Konzept `docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitte 2 und 4): die Wahlregel fuers Verhalten
aus der Lage ableiten (Naehe zum Spieler, eigene Staerke, Wallzustand, letzte Niederlage), Sperrzeit
beachten, die Wahl deterministisch aus dem Seed ziehen und die Taktik-Tabelle je Fraktion als
Datendatei anlegen. Danach B-3 (Wirtschaft je Dorf) und erst dann die Kopplung an die Volksboni.
Zu tun: Werte in `data/` (keine Literale im Code), Pruefdatei mit Grenzfaellen, voller Sammellauf,
Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Offen ausserdem:** das Protokoll steht mit 325 Zeilen ueber der Zielgroesse 320 - nach Daniels
Regel wird AUSGELAGERT (nicht gestrichen); das gehoert in den Aufraeumschritt (Punkt 9). Die Anzeige
der Doerfer im Spiel und die Voelkerwahl (Stufe A2) folgen nach B.

# STAND 02.11.2026, 16:00 - Leisten-Luecken gedeckelt (Register 131)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Punkt 3 des Ablaufplans ist erledigt.** Die Ressourcenleiste streckt ihre Luecken nicht mehr
beliebig: die Dehnung ist auf 1,35 gedeckelt, bei Bedarf waechst das ganze Band gleichmaessig
(treue Vergroesserung ohne Naht), ein Rest wird symmetrisch verteilt.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7f2a51` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1` |
| Befund vorher | Lueckendehnung **1,86** bei 2560 px, 2,81 bei 3000, **3,75** bei 3440 | eigene Messung an `leiste_zusammensetzen` |
| Werte | `luecke_max` 1,35, `skala_hart` 1,75, `rest_auffuellen` gleichmaessig | `data/ressourcenleiste.json` |
| Nachher | 1440-2320 px fuellen ganz, 2560 px Skala 1,653 (fuellt genau), 3440 px Raender 367/367 | eigene Messung, `tests/test_leisten_luecken.py` 22/0/0 |
| Umgestellte Wachen | `test_ressourcenleiste.py` **41/0/1**: Skala waechst bis `skala_hart`; Symbolfeld seitengetreu statt pixelgleich | eigener Lauf, Begruendung im Test |
| Sichtvergleich | `docs/audits/leisten_vergleich_20261102.png` (ALT/NEU, 2560 und 3440) | `tools/leisten_vergleich.py` |
| Voller Sammellauf | **124 von 126 gruen, 0 rot, 2 ausgesetzt, 4.824 Pruefungen, 541 s** (15:13-15:22) | `docs/audits/sammellauf_20261102_1513.log` |
| Pruefdateien / Register | **126** / **131** | `ls tests/test_*.py`, `grep -c` |

## Der EINE naechste Schritt

**Punkt 6: S-8-Bilanz und `weltkarten_seed` festschreiben** (Freigabe Daniels 02.11.2026, Register 93
und 94): der Weltensprung kostet **500 Mana plus 100 Gold** statt der heute gebuchten 5.000 Mana - der
belegte Originalwert 5.000 bleibt als Beleg und Konfigurationswert daneben stehen, nichts wird
geloescht -, und `weltkarten_seed` bekommt fuer die Demo einen FESTEN Wert in `data/welten.json`.
Zu tun: die eine Buchungsstelle des Sprungs umstellen (Kern UND Anzeige lesen denselben Wert), den
Belegwert unangetastet lassen, Seed setzen, je eine Pruefdatei mit Grenzfaellen (-1 / 0 / exakt Soll /
+1), voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

**Bei Daniel liegt** weiterhin Punkt 2 (Bilder im Fenster abnehmen, 10 Minuten) und die
Wappen-Zuordnung (Punkt 4). **Punkt 5** (Volksattribute und Verhaltensboni) wird seit 15:25 vom
STARKEN MODELL (deepseek-v4-pro) entworfen und umgesetzt - das GPT-Chat-Abo ist beendet, sein
Auftragspaket ist vom Desktop genommen und liegt weiter als Datei unter `docs/auftraege/`.

# STAND 02.11.2026, 13:50 - Auswahlrahmen der C2-Lieferung gezeichnet (Register 130)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Der Auswahlrahmen ist erledigt.** Auf dem gewaehlten Feld der Siedlungskarte liegt jetzt das
GELIEFERTE Bild `kachelrahmen_auswahl.png` voll deckend; der gezeichnete goldene Rahmen aus
`karten_optik_fein.auswahl_plan_fein` wird nur noch als Rueckfall gezeichnet, wenn das Bild fehlt.
Damit ist Punkt 1 des Ablaufplans aus der Uebergabe abgeschlossen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `fe4ed27` (Arbeitsbaum leer), darauf dieser Schritt | `git log --oneline -1`, `git status --porcelain` |
| Neu | Auswahlrahmen = geliefertes Bild, Bildobjekt in Durchgang 4 (zuletzt) | Register 130, `src/main.py` `_zeichne_siedlungskarte` |
| Deckkraft | Auswahl **100** Prozent (`kachelrahmen.deckkraft_auswahl_prozent`, neu), Ruhe **35** (`deckkraft_prozent`) | `data/gebaeude_motive.json`, am Bildcache gemessen |
| Wache | `tests/test_auswahlrahmen_c2.py` **17/0/0**; Gegenprobe mit abgeschaltetem Bildzweig **12/2** | eigener Lauf |
| Umgestellte Wache | `tests/test_startspiel.py` **62/0/1**: genau EIN Auswahlrahmen (Bild ODER gezeichnet), vorher 6 gezeichnete | eigener Lauf |
| Sichtvergleich | `docs/audits/auswahlrahmen_vergleich_20261102.png` (1986 x 720, drei Fassungen, echte Zeichenflaeche) | `tools/auswahlrahmen_vergleich.py` |
| Voller Sammellauf | **123 von 125 gruen, 0 rot, 2 ausgesetzt, 4.800 Pruefungen, 294 s** (13:45-13:50, auf dem ENDSTAND nach allen Dokumentzeilen) | `docs/audits/sammellauf_20261102_1345.log` |
| Pruefdateien / Register | **125** / **130** | `ls tests/test_*.py`, `grep -c` |
| Offen an Daniel | Auswahlrahmen wirkt auf dem Kontaktblatt wuchtiger als der gezeichnete - Deckkraft 100 oder z. B. 70? | `docs/FRAGEN_AN_DANIEL_20261102_1345.md` |

## Der EINE naechste Schritt

**Leisten-Luecken bei sehr breiten Fenstern schliessen** (Punkt 3 des Ablaufplans, Uebergabe
Abschnitt 4): die Landschaft wiederholt sich in der Ressourcenleiste, wenn das Fenster breiter wird.
Zu tun: mit zwei weiten Fensterbreiten messen (`main._leisten_stuecke` / `main.leiste_zusammensetzen`),
die Lueckenstuecke so bauen, dass Ecken und Symbolfelder pixelgleich bleiben und nur die Luecken
dehnen, eine Wache mit zwei Breiten ergaenzen, Sichtvergleich als Kontaktblatt unter `docs/audits/`,
danach voller Sammellauf, Protokollzeile und ein Commit.
Arbeitsweise: eine Pruefdatei je Bedingung, voller Sammellauf, Protokollzeile, ein Commit.

**Bei Daniel liegt** Punkt 2 (Bilder im Fenster abnehmen: Icons, Bauknoepfe, Hintergrund, Leiste,
10 Minuten) und die Zuordnung der Wappen zu den fuenf Bots (Punkt 4); Freigaben brauchen Punkt 5
und 6. Der Restweg bis zur Demo bleibt bei etwa 6-8 Arbeitstakten.

# STAND 02.11.2026, 11:31 - SITZUNGSENDE: Laptop-Neustart (WLAN, Tastatur)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Sitzung beendet, nicht angehalten** (WLAN bricht ab, Tastatur haengt): alle Hintergrundprozesse
sind beendet, das Spiel ist geschlossen, der Arbeitsbaum ist leer, die drei offenen
Skill-Einreihungen sind verworfen - **nichts ist ungespeichert.**
Uebergabe fuer die naechste Sitzung: `docs/UEBERGABE_20261102_1115.md` (Kopie auf dem Desktop,
hashgleich). Der Ablaufplan bis zur Demo steht dort Abschnitt 4.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `5a2f119`, Arbeitsbaum **leer** | `git status --porcelain` |
| Letzter Sammellauf | **122 von 124 gruen, 0 rot, 4.783 Pruefungen, 420 s** (10:25) | `docs/audits/sammellauf_20261102_1025.log` |
| Start | `.venv` mit Pillow 13.0.0, alte py-Kette als Rueckfall | `tests/test_start_mit_pillow.py` 10/0/0 |
| Restweg Demo | **6-8 Arbeitstakte**, davon 2 mit Daniels Freigabe | Uebergabe Abschnitt 4 |

## Der EINE naechste Schritt

**Den Auswahlrahmen der C2-Lieferung zeichnen** (Uebergabe Abschnitt 3): messen, wer zuletzt zeichnet
(`_zeichne_siedlungskarte`), den gezeichneten goldenen Rahmen nur als Rueckfall benutzen, den
gelieferten `kachelrahmen_auswahl.png` mit voller Deckkraft auf das gewaehlte Feld legen,
Sichtvergleich als Kontaktblatt unter `docs/audits/`, Wache ergaenzen, voller Sammellauf,
Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

# STAND 02.11.2026, 10:32 - Start mit Projekt-venv: Pillow da, Bilder scharf (Register 129)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `2f043dc` (Protokoll 291 Zeilen); dieser Commit bringt venv, Batch und die neue Wache | `git log --oneline -1` |
| venv | `.venv` = Astral CPython 3.11.16 + **Pillow 13.0.0**, `import tkinter, PIL` geprueft | `.venv/Scripts/python.exe -c "import PIL;print(PIL.__version__)"` |
| Start-Batch | nimmt zuerst `%~dp0.venv\Scripts\python.exe` (mit tkinter+Pillow-Pruefung), alte Kette bleibt Rueckfall | `START_SPIEL_WINDOWS.bat` |
| Im venv gemessen | Menue-Icon vorhanden, **Leistenbild vorhanden**, Hintergrund 538 x 222 | eigener Lauf, 10:22-10:32 |
| Neue Wache | `tests/test_start_mit_pillow.py` **10/0/0** (Reihenfolge im Batch, Rueckfall, venv-Import, gitignore) | eigener Lauf |
| Sammellauf | **122 von 124 gruen, 0 rot, 420 s** | `docs/audits/sammellauf_20261102_1025.log` |
| Aufgeraeumt | Python 3.15.2 unter `AppData\Local\Python` entfernt (122 MB, `py -0p` kannte es nicht) | `du -sh`, `ls` |
| Register / Pruefdateien | **129 Punkte**, **124 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Auswahlrahmen der C2-Lieferung zeichnen** - `kachelrahmen_auswahl.png` steht in
`data/gebaeude_motive.json` und wird geladen, aber der gezeichnete goldene Rahmen aus
`karten_optik_fein` liegt darueber. Zu tun: messen, wer zuletzt zeichnet (`_zeichne_siedlungskarte`),
den gezeichneten Rahmen nur als Rueckfall benutzen, den gelieferten Auswahlrahmen mit voller Deckkraft
auf das gewaehlte Feld legen, Sichtvergleich als Kontaktblatt unter `docs/audits/`, Wache in
`tests/test_gebaeude_motive.py` oder eigener Datei, voller Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`
   (jetzt mit scharfen Bildern, weil das venv Pillow hat).
2. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
3. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
4. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
5. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein `.bat` mit `%`-Pfaden und doppelten Marken ist empfindlich: Anker auf `\r\n:marke\r\n` setzen.**
  Ein `replace(':start_astral\r\n', ...)` traf zuerst das `goto :start_astral` MITTEN in der
  if-Kette und zerlegte das Batch. Erst der Anker mit fuehrendem Zeilenumbruch trifft die Marke.
  Vor dem Schreiben sichern und die Marken danach zaehlen (hier: vier Startmarken, jede mit `goto :ende`).
- **Ein venv ohne Pillow-Pruefung waere schlimmer als keins:** das Batch prueft `import tkinter, PIL`,
  bevor es dem venv traut - sonst startet ein halbfertiges venv und die Bilder fehlen wieder still.
- **`.venv` gehoert in `.gitignore` und NICHT ins Paket.** Sonst wandern 50+ MB Fremddateien ins Repo
  oder in die Demo; `git check-ignore -q .venv` ist die Wache dafuer.

# STAND 02.11.2026, 10:21 - Protokoll 291 Zeilen, Detailzeilen ausgelagert (Register 128)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `23f579f` (Verdichtung verworfen); dieser Commit loest sie strukturell | `git log --oneline -1` |
| Ergebnis | **291 Zeilen** statt 469, Ziel unter 320 erreicht - **ohne** Umformulierung | `wc -l docs/ENTWICKLUNGSPROTOKOLL.md` |
| Detaildokument | `docs/PROTOKOLL_DETAIL_2026-10.md`: 05.10. Tag 2 (87 Zeilen) und 31.10. UMSETZUNG-02 (97 Zeilen) wortgleich, 192 Zeilen | `wc -l` |
| Verlustpruefung | 46 Kennungen, **0 unbekannt**, alle Pruefzahlen der 02.11.-Sicherung vorhanden (Protokoll + Detail) | `tools/pruefe_protokoll.py` |
| Dokumentpruefungen | `test_protokoll` **16/0/1** (Zielgroessen-Befund weg), `test_textqualitaet` **307/0** (90 Dokumente), `test_projektpfade` 105/0, `test_zieluebergabe` 26/0 | eigener Lauf |
| Register / Pruefdateien | **128 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Projekt-venv mit Pillow anlegen und `START_SPIEL_WINDOWS.bat` darauf umstellen** (Daniels Entscheidung
02.11.2026, 10:2x): der Startpfad (Astral CPython 3.11.16) hat kein Pillow, deshalb fehlen
Ressourcenleiste und alle Bilder in voller Qualitaet. Zu tun: `.venv` mit derselben Python-Version
anlegen (`uv venv --python <3.11.16>`), `pillow` hinein, im Batch ZUERST `.venv\Scripts\pythonw.exe`
versuchen und die bisherige Kette als Rueckfall lassen; Waage: `python -c "import PIL"` im venv,
Startprobe aus dem Batch, `.venv` in `.gitignore` und im EXE-Bau ausgeschlossen; danach voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Offen

1. **Auswahlrahmen** der C2-Lieferung zeichnen (naechster Fachschritt danach).
2. Icons/Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. **Python 3.15.2** in `AppData\Local\Python` entfernen (Daniel hat zugestimmt).
4. Wappen den fuenf Bots; Burgen zu Weltkarten nur als Vorschlag.
5. S-8 Bilanz (Register 93), `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07; Demo wird LEER ausgeliefert. **EXE vom 01.11. 19:01** - vor einer Demo neu bauen.

## Fallstricke, in diesem Schritt belegt

- **Auslagern ist die ehrliche Verdichtung.** Ein Wortlaut, der in eine eigene Datei wandert, ist
  nicht verloren; ein Wortlaut, den ein Modell zu Stichworten verkuerzt, ist es. Wenn eine Zielgroesse
  drueckt: verschieben, nicht zusammenstreichen.
- **Die Projektpruefung vergleicht gegen die Fassung vom 05.10., nicht gegen gestern.** Wer gegen
  gestern pruefen will, braucht die eigene Sicherung - und muss Protokoll UND Detaildokument addieren,
  sonst meldet er falschen Verlust (genau das faengt das Schreibskript vorher ab).
- **Summenzeilen brauchen die Kennungen IM Text.** Wandern Zeilen in ein Detaildokument, muessen ihre
  Kennungen und Pruefzahlen in der Summenzeile mitreisen, sonst wird `test_protokoll` rot, obwohl
  nichts verloren ist.

# STAND 02.11.2026, 10:15 - Protokoll-Verdichtung verworfen, Weg ist strukturell (Register 127)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `f7be01c` (Kaserne-Fix); dieser Commit bringt nur Dokumente (Register 127) | `git log --oneline -1` |
| Versuch | Protokoll 468 -> Ziel 320 Zeilen, `deepseek-v4-pro`, abschnittsweise | Register 127 |
| Ergebnis | 287 Zeilen, alle 45 Kennungen echt, alle Pruefzahlen da - **aber Tabellenzeilen zu Stichwortketten zusammengezogen**; zwei echte Verluste (`954097a`, `777 / 300 / 21`), 44 von 86 Absatz-Anfaengen weg | `tools/pruefe_protokoll.py --nach` + eigener Vergleich gegen die 02.11.-Sicherung |
| Entscheidung | **verworfen**; `docs/ENTWICKLUNGSPROTOKOLL.md` bleibt bei 468 Zeilen, Sicherung `9445ad7` ist wieder Ist-Stand | dieser Commit |
| Verbrauch starkes Modell | 82.917 Prompt- / 77.967 Antwort-Token (rund 65.000 Denken) in drei Abschnittsaufrufen; zwei Abbrueche mit je rund 60.000 Prompt-Token; Kosten noch nicht abgelesen | `usage`-Zeilen im Lauf-Log |
| Register / Pruefdateien | **127 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |

## Der EINE naechste Schritt

**Auswahlrahmen der C2-Lieferung zeichnen** - der gelieferte `kachelrahmen_auswahl.png` liegt schon in
`data/gebaeude_motive.json` und wird geladen, aber der gezeichnete goldene Rahmen aus
`karten_optik_fein` liegt darueber, sodass die Lieferung nicht wirkt. Zu tun: messen, wer zuletzt
zeichnet (`_zeichne_siedlungskarte`), den gezeichneten Rahmen nur als Rueckfall benutzen (ohne Pillow),
den gelieferten Auswahlrahmen mit voller Deckkraft auf das gewaehlte Feld legen, Sichtvergleich als
Kontaktblatt (`docs/audits/`), Wache in `tests/test_gebaeude_motive.py` oder eigener Datei, voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Offene Entscheidungen fuer Daniel (gesammelt, EINE Runde)

1. **Pillow in die Spiel-Laufzeit?** Der Startpfad (Astral CPython 3.11.16) hat keines; `uv pip install`
   ist dort gesperrt (`externally managed`). Empfehlung: Projekt-venv mit Pillow anlegen und
   `START_SPIEL_WINDOWS.bat` darauf umstellen (dann sind Leiste, Motive und Icons scharf) - Alternative:
   alles beim Tk-Rueckfall lassen (sichtbar, aber groeber).
2. **Ressourcenleiste ohne Pillow** loesen (Kachelbau mit Tk-Mitteln) - nur noetig, wenn Punkt 1 nicht
   kommt.
3. **Protokoll-Struktur**: Detailzeilen des 05.10. und 31.10. nach `docs/PROTOKOLL_DETAIL_2026-10.md`
   auslagern, im Protokoll Summenzeile + Verweis. Das ist der einzige Weg unter 320 Zeilen, der nichts
   weglaesst.
4. **Python 3.15.2** in `AppData\Local\Python` (122 MB, vom Python-Manager ungefragt geladen) entfernen.

## Reihenfolge danach

1. Auswahlrahmen (naechster Schritt).
2. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
4. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
5. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
6. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein starkes Modell kuerzt dort, wo es am billigsten ist - nicht dort, wo es am wenigsten kostet.**
  Zeilen zusammenzuziehen ist einfach, Text zu verdichten ist Arbeit. Deshalb: die Zusage "keine Zahl
  verloren" ist NICHT die Zusage "kein Inhalt verloren". Gegenprobe muss immer der Sinn sein, nicht nur
  der Zahlenabgleich.
- **Ein 230.000-Zeichen-Auftrag mit 100.000 Zeichen Antwort passt in keinen einzelnen Aufruf.** Der
  erste Versuch endete nach 300 s Socket-Timeout, der zweite mit 0 Zeichen (Denken frisst `max_tokens`).
  Abschnittsweise arbeiten ist richtig - aber je Abschnitt mit der Regel "eine Zeile je Schritt",
  sonst entstehen Stichwortketten.
- **`vorher` heisst vorher sichern UND pruefen, wogegen man nachher vergleicht:** die Projektpruefung
  vergleicht gegen die Fassung vom 05.10., nicht gegen die von heute. Fuer echte Vollstaendigkeit
  selbst gegen die 02.11.-Sicherung vergleichen (dieser Schritt hat es getan und zwei Verluste
  gefunden, die die Projektpruefung nicht sieht).

# STAND 02.11.2026, 09:51 - Kaserne-Ansicht ohne Gebaeude abgesichert (Register 126)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `97fa2aa` (Pillow-Rueckfall); dieser Commit bringt den KeyError-Fix, Register 126 und die neue Pruefdatei | `git log --oneline -1` |
| Befund | `Kaserne` steht im Menue, sobald die Akademie auf IRGENDEINER Siedlung steht; die Ansicht liest aber die AKTIVE Siedlung - ohne Gebaeude dort `KeyError: 'guenstigste'` | nachgestellt, Wache `test_kaserne_ohne_gebaeude` |
| Fix | Fruehfall von `spieloekonomie.siedler_reserve` liefert dieselben Schluessel wie der Normalfall (`engste`, `guenstigste`, `teuerste`) | `grep -n "guenstigste" src/spieloekonomie.py` |
| Neue Pruefdatei | **11 von 11 gruen**; Gegenprobe mit dem alten Stand: **6 Fehler** inkl. `KeyError('guenstigste')`, Datei-Hash danach wieder gleich | eigener Lauf |
| Sammellauf | **121 von 123 gruen, 0 rot, 2 ausgesetzt, 4.767 Pruefungen, 407 s** (09:44-09:51) | `docs/audits/sammellauf_20261102_0944.log` |
| Register / Pruefdateien | **126 Punkte**, **123 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Irrweg | die Protokoll-Sicherung lag in `docs/` - `test_gpt_projektordnung_20261028` verlangt dort GENAU EINE aktive Protokolldatei; jetzt in `archiv/dokumentation/protokoll_alte_fassungen/`, hashgleich (`9116a9ab`) | eigener Lauf, 09:43 |
| Guthaben | Daniel 09:07: **8,25 USD** Kontostand, **41,74 USD** Gesamtverbrauch; Tagesbudget starkes Modell **3 USD** | Daniel, 09:07 |
| Offen (Freigabe) | Pillow in die Spiel-Laufzeit / Projekt-venv; Ressourcenleiste ohne Pillow; das ungenutzte Python 3.15.2 (122 MB) entfernen | eigene Messung |

## Der EINE naechste Schritt

**Das Entwicklungsprotokoll verdichten** (466 Zeilen, Regel: unter 320) - die unveraenderte Fassung
ist als `9445ad7` committed und liegt zusaetzlich in
`archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261102.md`
(hashgleich `9116a9ab`). Der starke Modellaufruf (deepseek-v4-pro) schreibt eine NEUE Datei
ausserhalb des Projekts; sie wird erst uebernommen, wenn `tools/pruefe_protokoll.py --nach <datei>`
Rueckgabe 0 liefert, alle 46 Commit-Kennungen mit `git cat-file -e` existieren und alle 205
Pruefzahlen wieder vorkommen. Danach: neue Fassung einsetzen, Zwischendatei entfernen,
Protokollzeile ueber die Verdichtung selbst, voller Sammellauf, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. **Pillow-Entscheidung** (Daniel): Projekt-venv mit Pillow und Start-Batch darauf; danach die
   Ressourcenleiste ohne Pillow als Rueckfall.
2. Icons und Hintergrund im Fenster abnehmen - drei Bilder unter `docs/audits/gebaeude_icons_fenster_*`.
3. Auswahlrahmen der C2-Lieferung; die acht Einzelsymbole aus `assets/icons/leiste/symbole/` ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
7. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein Fruehfall muss ALLE Schluessel der Funktion liefern.** Der abgekuerzte `return` in
  `siedler_reserve` sparte zwei Felder, und der Anzeigecode griff genau eines davon. Wache dafuer ist
  der Vergleich der Schluesselmengen zweier echter Faelle - nicht das Nachbauen einer Wunschliste.
- **Ein Test, der nach dem Namen einer DATEI sucht, bricht bei jeder zweiten Fassung.** Die
  Protokoll-Sicherung gehoert nach `archiv/dokumentation/protokoll_alte_fassungen/`, NICHT nach
  `docs/` (dort erlaubt `test_gpt_projektordnung_20261028` nur `ENTWICKLUNGSPROTOKOLL.md`).
- **`git rm` vor dem Kopieren pruefen:** erst Hash der Kopie vergleichen, dann entfernen - die
  Fassung steckt zusaetzlich im Commit `9445ad7`.

# STAND 02.11.2026, 09:29 - Gebaeude-Optik sichtbar auch ohne Pillow (Register 125)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `bfed4de` (Icons eingebaut); dieser Commit bringt den Pillow-Rueckfall, Register 125 und die Fensterbilder | `git log --oneline -1` |
| Befund | Startpfad (`START_SPIEL_WINDOWS.bat`, Astral CPython 3.11.16) hat **kein Pillow**: vorher `Menue-Knoepfe mit Bild: []`, `leiste_zusammensetzen -> None` | eigene Messung mit genau diesem Interpreter, 09:10 |
| Nach dem Fix | mit demselben Interpreter: Menue-Icon **20 px**, Hintergrund **538 x 222** | eigene Messung, 09:20 |
| Pruefdatei | **56 von 56 gruen** (zwei neue Wachen: Pillow fuer zwei Aufrufe abgeschaltet) | eigener Lauf |
| Sammellauf | **120 von 122 gruen, 0 rot, 2 ausgesetzt, 4.761 Pruefungen, 401 s** (09:21-09:28) | `docs/audits/sammellauf_20261102_0921.log` |
| Fensterbilder | Dorfzentrum, Bauauswahl, Forschung - echte Oberflaeche mit eigenem Testspielstand | `docs/audits/gebaeude_icons_fenster_*_20261102.png` |
| Register / Pruefdateien | **125 Punkte**, **122 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Guthaben | Daniel 09:07: **8,25 USD** Kontostand, **41,74 USD** Gesamtverbrauch; Tagesbudget fuer das starke Modell **3 USD** | Daniel, 09:07 |
| Offen (Freigabe) | Pillow in die Spiel-Laufzeit (Projekt-venv oder uv-Interpreter) und Loesung fuer die Ressourcenleiste ohne Pillow; das ungenutzte Python 3.15.2 unter `AppData\Local\Python` (122 MB) entfernen | eigene Messung |

## Der EINE naechste Schritt

**Die Kaserne-Ansicht darf ohne Gebaeude am aktiven Ort nicht abstuerzen** - der Fehler ist aelter als
dieser Schritt und beim Bau der Pruefdatei aufgefallen: `_siedler_warnung_zeichnen`
(aufgerufen aus `_render_ausbildung`) liest `reserve["guenstigste"]`, und
`spieloekonomie.siedler_reserve` liefert diesen Schluessel NICHT, wenn am aktiven Ort kein Gebaeude
steht (Fruehfall `if not bedarf: return {...}` ohne `guenstigste`). Nachgestellt: Siedlung mit
Kriegerakademie, aktive Siedlung ohne Gebaeude, Menuepunkt "Kaserne" -> `KeyError`.
Zu tun: den Schluessel im Fruehfall mitliefern (der Docstring der Funktion beschreibt die Rueckgabe,
also gehoert er in die Funktion), Wache dazu (Siedlung ohne Gebaeude -> Ansicht rendert), voller
Sammellauf, Protokollzeile, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. **Pillow-Entscheidung** (Daniel): Projekt-venv mit Pillow und Start-Batch darauf, damit Leiste und
   Bilder scharf sind; danach die Ressourcenleiste ohne Pillow als Rueckfall.
2. Icons und Hintergrund im Fenster abnehmen - die drei Bilder unter `docs/audits/` zeigen den Stand.
3. Auswahlrahmen der C2-Lieferung (der goldene gezeichnete Rahmen liegt derzeit ueber dem gelieferten);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01..G-07 vor jedem Upload; die Demo wird LEER ausgeliefert.
7. Protokoll steht bei **466 Zeilen** (Ziel unter 320) - Verdichten mit Sicherung vorher.
8. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **Ein gruener Sammellauf sagt nichts ueber den STARTWEG.** Alle 4.761 Pruefungen liefen mit dem
  Hermes-Python (Pillow vorhanden) - das Spiel startet aber mit einem anderen Interpreter ohne
  Pillow. Bei Bild-Funktionen deshalb immer einmal mit DEM Interpreter messen, den das Start-Batch
  aufruft (`py -0p` zeigt die Laufzeiten, `python.exe -c "import PIL"` die Wahrheit).
- **Rueckfall statt Absturz, aber sichtbar statt still.** Ein `None`-Ergebnis ohne Rueckfall heisst:
  das Bild FEHLT, ohne Fehlermeldung. Das ist die unangenehmste Sorte Fehler - gruen und leer.
- **`uv pip install` in die uv-Laufzeit geht nicht:** `externally managed`. Sauberer Weg ist eine
  Projekt-venv; das Aendern des Start-Batches ist Daniels Entscheidung.
- **WindowsApps-`python.exe` ist der Python-Manager, kein Python.** Ein Aufruf startet ungefragt einen
  Download (hier Python 3.15.2). Fuer Messungen immer den echten Interpreterpfad nehmen.

# STAND 02.11.2026, 08:59 - Gebaeude-Optik haengt in der Oberflaeche (Register 124)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf beim Schreiben | `0bf5d31`; dieser Commit bringt Einbau, Pruefdatei und Register 124 | `git log --oneline -1` |
| Eingebaut | Icons in der Menueleiste (20 px, `compound=tk.LEFT`), Icons an JEDEM Bauknopf der Kartenauswahl (28 px), Hintergrund 538 x 222 in Dorfzentrum, Forschung, Kaserne, Stellmacher, Diebesgilde | `tests/test_gebaeude_icons.py` |
| Zuordnung Menue -> Gebaeude | `main.MENU_GEBAEUDE` ABGELEITET: `gelaende.finde_gebaeude` (Dorfzentrum -> `lager`) + `MENUE_BEDINGUNG` (Kaserne -> `kriegerakademie`, Forschung -> `bibliothek`); Weltpunkte ohne Bild | `grep -n "MENU_GEBAEUDE" src/main.py` |
| Neue Pruefdatei | **54 von 54 gruen, 0 Fehler, 0 Befunde** | eigener Lauf |
| Gegenprobe | mit abgeschaltetem Menue-Icon **4 Fehler** (Datei wird rot), Datei-Hash danach wieder gleich | eigener Lauf, Protokoll 08:51 |
| Sammellauf | **120 von 122 gruen, 0 rot, 2 ausgesetzt, 4.759 Pruefungen, 424 s** (08:52-08:59) | `docs/audits/sammellauf_20261102_0852.log` |
| Register / Pruefdateien | **124 Punkte**, **122 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Guthaben | letzte Ablesung **8,50 USD** Kontostand, **41,49 USD** Gesamtverbrauch (Daniel, 08:09) - seither nur dieser eine Schritt | Register 117, Uebergabe 08:09 |
| EXE im Projektordner | **01.11.2026, 19:01** - enthaelt keinen der Commits ab `6585cd2` | `ls -la`, `git log -1` |
| Abnahme offen | das Aussehen im Fenster hat Daniel noch NICHT gesehen (Icons, Bauknoepfe, Hintergrund) | eigene Messung |

## Der EINE naechste Schritt

**Die Kaserne-Ansicht darf ohne Gebaeude am aktiven Ort nicht abstuerzen** - der Fehler ist aelter als
dieser Schritt und beim Bau der Pruefdatei aufgefallen: `_siedler_warnung_zeichnen`
(`src/main.py`, Aufruf in `_render_ausbildung`) liest `reserve["guenstigste"]`, und
`spieloekonomie.siedler_reserve` liefert diesen Schluessel NICHT, wenn am aktiven Ort kein Gebaeude
steht (Fruehfall: `if not bedarf: return {...}` ohne `guenstigste`). Nachgestellt: Siedlung mit
Kriegerakademie anlegen, aktive Siedlung ohne Gebaeude, Menuepunkt "Kaserne" oeffnen -> `KeyError`.
Zu tun: EINE Stelle lesen (`reserve.get("guenstigste", ("", 0))` im Anzeigecode ODER den Fruehfall in
`siedler_reserve` vollstaendig zurueckgeben - die Rueckgabe ist im Docstring beschrieben, also gehoert
der Schluessel in die Funktion), Wache in `tests/test_gebaeude_icons.py` oder eigener Datei
(Siedlung ohne Gebaeude -> Ansicht rendert), voller Sammellauf, ein Commit.
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, Protokollzeile, ein Commit.

## Reihenfolge danach

1. Icons und Hintergrund im Fenster abnehmen (Daniel) - rechnerisch und in der Pruefdatei belegt,
   im laufenden Spiel noch nicht gesehen.
2. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit
   oben); die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind weiter ungenutzt.
3. Bei sehr breiten Fenstern wiederholt sich die Landschaft in den gedehnten Leistenluecken sichtbar.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt
   "Die oeffentliche Demo wird LEER ausgeliefert", geprueft: `tools/build_public_exe.py`,
   `tests/test_demo_leer.py`).
7. **EXE ist vom 01.11. 19:01** - vor einer Demo neu bauen und startgeprueft starten.

## Fallstricke, in diesem Schritt belegt

- **`grep` auf einen Namen, den man im Kopf hat, findet nichts, was es nicht gibt.** Ich suchte
  `MENUE_ANZEIGE`, im Code steht `MENU_ANZEIGE` (mit E im Wort "Menue" haette es nicht existiert).
  Zwei Messungen (grep und `str.count`) meldeten 0 Treffer, obwohl die Zeile sichtbar war - erst der
  Zeichencode-Vergleich zeigte, dass ich den falschen Namen gesucht hatte. Bei "0 Treffer" also
  zuerst pruefen, ob der GESUCHTE Name stimmt, nicht ob der Code fehlt.
- **Ein Menuenpunkt kann ein Gebaeude sein, ohne so zu heissen.** "Dorfzentrum" ist die Anzeige von
  `lager`, "Kaserne" ist `kriegerakademie`, "Forschung" ist `bibliothek`. Die Zuordnung deshalb
  ABLEITEN (`gelaende.finde_gebaeude` + `MENUE_BEDINGUNG`), nicht als dritte Handliste tippen.
- **`tk.Button` mit `compound=tk.LEFT` braucht eine Bildreferenz im Objekt.** Der Cache in
  `_optik_bild` ist Pflicht, sonst gibt Tk das Bild frei und das Menue zeigt leere Felder.
- **Eine Ansicht, die im Menue nicht steht, ist trotzdem renderbar** (`_switch_view` kennt jede
  Route der Tabelle). Genau so kam der Kaserne-Absturz heraus: eine frische Siedlung ohne Gebaeude
  plus `_switch_view("Kaserne")`.

# STAND 02.11.2026, 01:36 - B4 gelaufen: Gebaeude-Optik als Modul (Register 123)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `5f4763b` beim Schreiben; dieser Commit bringt Modul, Pruefdatei und Bilder | `git log --oneline -1` |
| B4-Lauf | `deepseek-v4-pro`, 252 s, **1.878 Prompt- / 33.858 Antwort-Token (28.365 Denken)**; Kosten noch nicht abgerechnet | `docs/audits/usage_b4_20261102.json` |
| Geliefert | `src/gebaeude_optik.py` (ICONS, HINTERGRUENDE, `kachel()`, `hintergrund()`, `fehlende_gebaeude()`, `vorschau_blatt()`) und `tests/test_gebaeude_optik.py` | `docs/audits/BERICHT_B4_20261102.md` |
| Bilder im Projekt | **20 Menue-Icons** (256x256 RGBA) in `assets/icons/gebaeude/menue/`, **20 Hintergruende** (538x222 **RGBA**) in `.../hintergrund/`; NICHT in `archiv/` (gitignored) | eigene Kopie + Pillow-Messung |
| Pruefdatei | **179 von 179 gruen**, echte Namen und echte Bedingungen; **23 von 24 Aufrufen waren vertauscht** (namens `True`, Bedingung der Text) und meldeten 179 gruene Pruefungen ohne Wirkung | eigener Lauf |
| Modulkarte | **51 Dateien** (neu: `gebaeude_optik`) | `tools/modulkarte_bauen.py` |
| Register | **123 Punkte**, **121 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Kosten und Guthaben | letzte Ablesung **8,97 USD** (00:05); Tagesdeckel 4 EUR heute bereits ueberschritten | Register 117, Protokoll 00:10 |

## Der EINE naechste Schritt

**Die Gebaeude-Optik in die Oberflaeche einhaengen** - das Modul ist nur die Zugriffsschicht. Drei Stellen,
je mit eigener Pruefung: (1) **Baudialog und Gebaeude-Menue** zeigen je Gebaeude das gerahmte Icon
(`gebaeude_optik.kachel(id, px)`); (2) die **Gebaeudeansicht** bekommt den Hintergrund
(`gebaeude_optik.hintergrund(id, breite)`); (3) ein **Kontaktblatt** (`vorschau_blatt`) fuer Daniels
Sichtpruefung vor dem Einbau. Vorher `motiv_1..10.png` sichern (die Handbuchmotive bleiben Rueckfallsatz).
Arbeitsweise: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Icons in Menue und Baudialog, Hintergrund in der Gebaeudeansicht, Kontaktblatt fuer Daniel.
2. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind weiter ungenutzt.
3. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
4. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
5. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt
   „Die oeffentliche Demo wird LEER ausgeliefert“, geprueft: `tools/build_public_exe.py`, `tests/test_demo_leer.py`).

## Fallstricke, in dieser Sitzung belegt

- **Ein starkes Modell liefert Code, der laeuft - aber nicht Code, der prueft.** 23 von 24 `check()`-Aufrufen
  hatten Name und Bedingung vertauscht: `check(name, cond)` mit `check(cond, name)` aufgerufen meldet
  **179 gruene Pruefungen, die nichts pruefen**, weil der Text immer wahr ist. Nach jedem Modelllauf die
  Reihenfolge der Aufrufe pruefen, nicht nur das Ergebnis.
- **Nie auf gitignorte Pfade bauen.** `archiv/` ist gitignored - Bilder muessen unter `assets/` liegen, sonst
  fehlt der Demo die Grafik. Die Projektwurzel kommt aus `spieldaten.projektwurzel()`, nicht aus `__file__`.
- **Auftragsangaben selbst nachmessen.** „Hintergruende RGB“ im Auftrag war falsch (sie sind RGBA); der
  Modellcode folgte meiner Vorgabe und die Pruefdatei schlug mit 20 Fehlern zu Recht an.
- **Ein einzelner starker Aufruf kostet wenig, wenn der Auftrag eng ist:** 252 s, 35.736 Token gesamt.

# STAND 02.11.2026, 00:49 - C2-Ressourcenleiste steht im Kopf (Register 121)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `1085861` beim Schreiben; dieser Commit bringt die Leiste | `git log --oneline -1` |
| Ressourcenleiste | **im Kopf eingebaut und auf Kachelbau umgestellt**: feste Ecken und acht Symbolfelder wachsen gleichmaessig (Skala bis 1,5), nur die Luecken dehnen sich - der Balken wird breiter, die Symbole bleiben in Form; Zahlen als eigene Textebene, Positionen aus der Zusammensetzung | Register 121, 122 |
| Keine Zahl doppelt | Leiste zeigt MENGEN, Detailzeile zeigt fuer sechs Rohstoffe nur die RATE; Wolle/Leder/Pferde behalten Menge und Rate | `main.kopfzeile_fuer` |
| Messung am Fenster | **41 Canvas-Teile** (1 Bild + 8 x 5 Texte); fuenf Fensterbreiten gemessen (1000/1440/1920/2560/3440): Symbolfeld bei 2560 und 3440 **pixelgleich**, keine Verzerrung | eigener Tk-Lauf, `test_ressourcenleiste` 39/0/1 |
| Pruefdateien | neu `test_ressourcenleiste` **28/0/1**; `test_nahrungsverbrauch` mit Begruendung auf den neuen Hilfsnamen umgestellt (**53/0/0**) | eigener Lauf |
| Sammellauf | **118 von 120 gruen, 0 rot, 2 ausgesetzt**, 4.515 Pruefungen, 276 s (00:42) | `docs/audits/sammellauf_20261102_0042.log` |
| Register | **121 Punkte**, **120 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Vorschau | `docs/audits/ressourcenleiste_vorschau_20261102.png` (Zahlen sitzen mittig in den Plaketten) | Sichtpruefung |
| Kosten und Guthaben | Blockplan **1,8715 von 4,00 USD**; Guthaben **8,97 USD** (Ablesung 00:05, Protokoll 00:10) | Register 117 |

## Der EINE naechste Schritt

**Die Leiste im laufenden Fenster abnehmen und danach die GPT-Icons in Menue und Baudialog einhaengen.**
Die Leiste ist rechnerisch und im Bild geprueft, aber **noch nicht von Daniel im Spiel gesehen** - vor dem
naechsten Umbau kurz das Spiel starten, in die Uebersicht gehen und hinsehen (Zahlen mittig, Schriftgroesse
bei kleiner Fensterbreite, Warnfarbe bei fehlender Ernte). Danach der naechste Einbau: die **20 gerahmten
GPT-Icons** in Menue und Baudialog und die **20 Hintergruende (538x222)** in die Gebaeudeansicht, Quelle
`archiv/eingaben/20261101_gebaeude_designs/Nebelseetal_Gebaeude_Designs_Update/`; vorher `motiv_1..10.png`
sichern. Arbeitsweise wie hier: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Leiste im Fenster abnehmen; Schriftgroesse und Warnfarben nach Daniels Urteil nachziehen.
2. GPT-Icons in Menue und Baudialog, Hintergruende in die Gebaeudeansicht (vorher `motiv_1..10.png` sichern).
3. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben);
   die acht Einzelsymbole aus `assets/icons/leiste/symbole/` sind noch ungenutzt.
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload; die Demo wird LEER ausgeliefert (Skill-Abschnitt).

## Fallstricke, in dieser Sitzung belegt

- **Mengen und Raten nicht doppelt anzeigen.** Als die Leiste die Mengen uebernahm, zeigte die alte Textzeile
  dieselbe Zahl noch einmal; jetzt entscheidet `kopfzeile_fuer` je Rohstoff, welche Form gilt.
- **Bildmasse aus der Datendatei, nie tippen.** Alle acht Mittelpunkte und die Hoehe kommen aus
  `data/ressourcenleiste.json`; das Spiel rechnet mit einer Skala um, damit die Felder bei jeder Fensterbreite
  unter ihren Symbolen sitzen.
- **Tk-Bilder brauchen eine Referenz** (`self._leisten_bild_ref`), sonst raeumt der Garbage Collector die
  Leiste weg und es bleibt ein leerer Streifen.
- **Eine Wache, die einen alten Funktionsnamen woertlich prueft, wird mit Begruendung umgestellt** - sie sichert
  eine Zusage (eine Quelle fuer Aufbau und Anzeige), nicht den Namen.

# STAND 02.11.2026, 00:30 - C2-Kartenmotive und Kachelrahmen stehen auf der Siedlungskarte (Register 120)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `d888d8f` beim Schreiben; dieser Commit bringt den Einbau | `git log --oneline -1` |
| Kartenmotive | **20 freigestellte C2-Motive** auf der Karte, 256 px auf **44 px** verkleinert (Pillow, LANCZOS); Schalter `quelle_der_karte` in `data/gebaeude_motive.json` | Register 120, `assets/icons/gebaeude/c2/` |
| Kachelrahmen | C2-Rahmen (64 px) auf **jedem** Feld, **Deckkraft 35 Prozent** - die Zahl steht in der Datendatei, ohne Code aenderbar; voll aufgelegt war er zu dominant | `docs/audits/kartenvergleich_c2_20261102.png` (drei Fassungen) |
| Rueckfall | Gebaeude ohne Motiv zeichnet weiter den Baukoerper; die acht Handbuchmotive bleiben als Beleg in der Datendatei, nichts geloescht | `main._lade_gebaeude_motiv` liefert `None` |
| Pruefdatei | `tests/test_gebaeude_motive.py` **104/0/1** - mit Begruendung neu geschrieben (die alten Wachen nagelten drei Motive fest) | eigener Lauf |
| Sammellauf | **117 von 119 gruen, 0 rot, 2 ausgesetzt**, 4.485 Pruefungen, 274 s (00:15) | `docs/audits/sammellauf_20261102_0015.log` |
| Register | **120 Punkte**, **119 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| C2-Lieferung | 15 Mini-ZIPs, 31 Nutzbilder, Manifest 20/20 deckungsgleich, Desktop geraeumt | Register 119 |
| Kosten und Guthaben | Blockplan **1,8715 von 4,00 USD**; Guthaben **8,97 USD** / 41,02 USD Gesamtverbrauch (Ablesung Daniel 00:05) | Register 117, Protokoll 00:10 |

## Der EINE naechste Schritt

**Die Ressourcenleiste aus der C2-Lieferung oben einhaengen** - Leiste 1440x140 als Hintergrund, acht
Zahlenfelder mit den Werten als eigene, zentrierte Textebene (helle Zahl, dunkle Kontur). Reihenfolge und
Zahlenfeld-Mittelpunkte stehen woertlich in `archiv/eingaben/20261102_c2_designs/LIEFERUNG.md` (Siedler,
Nahrung, Holz, Stein, Erz, Gold, Mana, Kelch; (184,105) (342,105) (494,105) (646,105) (799,105) (957,105)
(1110,105) (1264,105) bei 1440x140, proportional skalieren). Die Werte kommen aus `kopf_zeilen_text`
bzw. der bestehenden Kopfzeilen-Rechenstelle, damit Anzeige und Kern dieselbe Quelle lesen (F-04).
Danach: GPT-Icons in Menue und Baudialog, danach die acht Ressourcensymbole der Leiste. Arbeitsweise wie
hier: Pruefdatei ergaenzen, voller Sammellauf, ein Commit.

## Reihenfolge danach

1. Ressourcenleiste oben (Teil B der C2-Lieferung) samt acht Symbolen.
2. GPT-Icons (20, gerahmt) in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht;
   vorher `motiv_1..10.png` sichern.
3. Auswahlrahmen der C2-Lieferung zeichnen (der goldene Rahmen aus `karten_optik_fein` liegt derzeit oben).
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Ein kraeftiger Kachelrahmen auf 100 Feldern zerstoert das Kartenbild.** Erst messen, dann einstellen:
  drei Fassungen rendern und vergleichen (`docs/audits/kartenvergleich_c2_20261102.png`), Deckkraft als Zahl
  in die Datendatei legen.
- **Tk gibt Bilder frei, die niemand referenziert.** Jedes skalierte Motiv und der Rahmen MUESSEN im Cache
  bleiben, sonst verschwinden sie still vom Canvas.
- **Pillow nur im Ladepfad importieren, nicht oben im Modul**: ohne Pillow (nach einem Hermes-Update) faellt
  der Code auf `tk.PhotoImage`+`subsample` zurueck, statt das Spiel unstartbar zu machen.
- **Wachen, die eine alte Zahlenlage festnageln, werden mit Begruendung umgeschrieben**, nicht der Code
  zurueckgebogen (`test_gebaeude_motive` hielt drei Motive fest).

# STAND 01.11.2026, 23:55 - Heilkunde-Bonus und Rinderfarm behoben (Register 118)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | `c565e59` beim Schreiben; dieser Commit bringt Fix und Doku | `git log --oneline -1` |
| Heilkunde-Bonus | **greift jetzt**: `siedler_zuwachs_pro_stunde` rechnet ueber `forschung_wirkung.siedlerfaktor`; gemessen **1,5 Siedler je Stunde bei Stufe 5** (vorher 1,0) | Register 118, eigener Lauf |
| Rinderfarm | **3 Nahrung + 3 Leder** auf Grasland, **1,5 + 1,5** auf Steppe (Handbuch 2009, Seite 10, woertlich) | `data/buildings.json`, Register 118 |
| Anzeige | die Gebaeudewirkungen zeigen den Zuwachs inklusive Heilkunde - Kern und Anzeige lesen dieselbe Stufenkarte (`self.state.forschungs_stufen()`) | `src/main.py`, Wachen A11/A12 |
| C2-Lieferung | **15 Mini-ZIPs, 31 Nutzbilder aufgenommen und geprueft**: 20 Kartenmotive 256x256 RGBA **freigestellt** (41-54 % Deckung), 8 Symbole 96x96, Leiste 1440x140, 2 Kachelrahmen 64x64; Manifest **20 von 20 IDs deckungsgleich** mit `data/buildings.json`; Desktop geraeumt | Register 119, `archiv/eingaben/20261102_c2_designs/` |
| Neue Pruefdatei | `tests/test_heilkunde_rinderfarm.py` **23/0/0**; `test_gpt_ne01_origwerte` **63/0/0**, `test_oekonomie_kern_10x10_nachfolger` **98/0/4** (die vier Befunde sind alt) | eigener Lauf 23:52 |
| Register | **118 Punkte**, **119 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| Sammellauf | **117 von 119 gruen, 0 rot, 2 ausgesetzt**, 4.424 Pruefungen, 456 s (23:55-00:04) - die zwei ausgesetzten sind `test_oekonomie_kern_unabhaengig` und `test_weltkarte` (dokumentiert zurueckgezogen) | `docs/audits/sammellauf_20261101_2355.log` |
| Kosten und Guthaben | unveraendert: Blockplan **1,8715 von 4,00 USD**, Guthaben **9,18 USD** (Ablesung 22:48) - heute kein starker Modelllauf mehr | Register 114, 117 |

## Der EINE naechste Schritt

**Die C2-Kartenmotive auf die Siedlungskarte bringen** - vorher entscheidet Daniel, WELCHE Fassung
gilt: die **20 freigestellten C2-Motive** (Register 119, decken alle 20 Gebaeude ab, 256x256 RGBA) oder die
**zehn handgeschnittenen Handbuchmotive** (Register 113, Daniels Zuordnung 1-10). Danach die Karte:
Motiv rund 44 px plus Gelaenderahmen (`kachelrahmen_ruhe.png`/`_auswahl.png`, 64x64) je Kachel, und die
Ressourcenleiste 1440x140 oben mit acht Zahlenfeldern (Einbauhinweise in
`archiv/eingaben/20261102_c2_designs/LIEFERUNG.md`). Arbeitsweise wie hier: Pruefdatei ergaenzen, voller
Sammellauf, ein Commit. Der Einbau aendert das sichtbare Kartenbild sichtbar - deshalb zuerst die Entscheidung.

## Reihenfolge danach

1. Kartenoptik Variante 2 in `src/main.py` (Motiv rund 44 px + Gelaenderahmen je Kachel).
2. GPT-Icons in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht
   (`archiv/eingaben/20261101_gebaeude_designs/`); vorher `motiv_1..10.png` sichern.
3. C2 pruefen, sobald Daniels ZIPs kommen (Kartenmotive, Ressourcenleiste, Kachelrahmen).
4. Wappen den fuenf Bots zuordnen; Burgen zu Weltkarten nur als gekennzeichneter Vorschlag.
5. S-8 Bilanz (500 Mana + 100 Gold, Register 93), danach `weltkarten_seed` fest (Register 94).
6. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Der alte Kleinbuchstaben-Schluessel `heilkunde` wirkt bewusst NICHT mehr.** Wer ihn wieder einbaut,
  holt den Befund aus Register 105 zurueck; Wache 7e2 in `test_oekonomie_kern_10x10_nachfolger` haelt das fest.
- **Leder haengt an Tierhaltung, nicht an Felderwirtschaft.** Eine Pruefung des Rinderfarm-Bonus mit
  Felderwirtschaft allein misst nichts - eigener Fehlversuch in dieser Sitzung, B7 fiel zuerst rot aus.
- **Datenaenderung heisst: Tests nach dem alten Literal greppen.** `grep -rn "rinderfarm" tests/` fand zwei
  Stellen; beide sind mit Begruendung umgestellt, nicht der Code zurueckgebogen.

# STAND 01.11.2026, 22:50 - B3 abgeschlossen und unabhaengig geprueft, vier GPT-Pakete entpackt und abgeglichen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | **`85c0c3b`** (B3), Doku-Commit folgt | `git log --oneline -1` |
| B3 (S-7 Bots erlebbar) | **ABGESCHLOSSEN**, nicht abgebrochen: die Sitzung `local-94abacfd` (deepseek-v4-pro) lief bis 22:45 | Register 114 |
| B3 Abnahme | `test_s7_botverhalten` **45/0/0**, die vier zuvor roten Pruefdateien wieder gruen, Sammellauf 22:35: **116/118 gruen, 0 rot, 2 ausgesetzt, 4.400 Pruefungen, 500 s** | eigener Lauf des Koordinators, `docs/audits/sammellauf_20261101_2235.log` |
| Kosten Blockplan | B1 0,5980 + B2 0,2553 + B3 **1,0182** = **1,8715 USD** von 4,00 USD | Register 114; Preis aus B1 kalibriert, Probe 0,6010 gegen 0,5980 |
| Guthaben 22:48 | **9,18 USD**, Gesamtverbrauch **40,81 USD**; Differenz zur Ablesung 21:0x = 1,21 USD, gedeckt durch B3 1,0182 + Koordination 0,19 | Register 117 |
| Tagesdeckel | rund **4,2 USD** heute – der 4-EUR-Rahmen ist praktisch erreicht | Register 117 |
| Sammellauf dieses Stands | **116/118 gruen, 0 rot, 2 ausgesetzt, 4.400 Pruefungen, 283 s** (22:56) | `docs/audits/sammellauf_20261101_2251.log` |
| Register | **117 Punkte**, **118 Pruefdateien** | `grep -cE`, `ls tests/test_*.py \| wc -l` |
| GPT-Gebaeudepakete | **vier ZIPs eingegangen**, hashgeprueft, entpackt nach `archiv/eingaben/20261101_gebaeude_designs/`; **20 Icons, 20 Hintergruende, 4 Tafeln**, Manifest-IDs **20 von 20 deckungsgleich** mit `data/buildings.json` | Register 115 |
| **Wichtigster Befund zum Einbau** | die 20 Icons sind **nicht freigestellt** (256x256, 0 % Transparenz, gemalte Szene im Goldrahmen) – sie taugen fuer **Menue und Baudialog**, **nicht** als Kartenmotive | Pillow-Messung, Sichtpruefung der Vorschau |
| Offen aus B3 | WIRKUNG der Volksattribute und Verhaltensboni nicht verdrahtet (Hook-Stellen in `kampf.py`, `spieloekonomie.py`, `auftraege.py`), Sperrzeit 1 h statt 48 h | Bericht S-7, Abschnitt 5 |

## Der EINE naechste Schritt

**Die Icons in Menue und Baudialog einhaengen, die Hintergruende in die Gebaeudeansicht** – nach den
zwei offenen Fixes (Heilkunde, Rinderfarm), die Daniel am 01.11. freigegeben hat. Kartenmotive bleiben
die zehn Handbuchmotive aus Register 113; die GPT-Icons ersetzen sie nicht.

## Reihenfolge

1. Heilkunde-Bonus auf `forschung_wirkung.siedlerfaktor` legen, Rinderfarm auf 3/1,5 (Freigabe liegt vor).
2. Zehn Handbuchmotive in `data/gebaeude_motive.json` eintragen (Daniels Zuordnung, Register 113), dann Karte.
3. Kartenoptik Variante 2 (Motiv rund 44 px + Gelaenderahmen je Kachel).
4. GPT-Icons in Menue und Baudialog, Hintergruende (538x222) in die Gebaeudeansicht.
5. Wappen den fuenf Bots zuordnen; Burgen zu Welten nur als gekennzeichneter Vorschlag.
6. S-8 Bilanz (500 Mana + 100 Gold, Register 93), `weltkarten_seed` fest (Register 94).
7. Demo-Gates G-01 bis G-07 vor jedem Upload.

## Fallstricke, in dieser Sitzung belegt

- **Ein laufender Block ist nicht am Arbeitsbaum zu erkennen.** Die Uebergabe 21:55 meldete B3 als
  abgebrochen, waehrend die Sitzung weiterlief und den Baum rot hielt. Richtig ist ein Blick auf die
  **letzte Zeile des Aufrufprotokolls** (`AppData/Local/hermes/logs/agent.log`, Sitzungskennung).
- **`data/gebaeude.json` gibt es nicht** – die Gebaeudeliste steht in `data/buildings.json`.
- **`archiv/` und `*.log` sind gitignored**: Eingabepakete und Sammellauf-Protokolle liegen auf der
  Platte, nicht in der Versionsgeschichte. Wer sie braucht, muss die Platte sichern, nicht das Repo.
- **GPT-Icons sind Buttons, keine Kulisse**: 0 % Transparenz. Fuer die Karte braucht es die
  Handbuchmotive oder eine neue Freistellung.

# STAND 01.11.2026, 21:55 - B3 abgebrochen und gesichert, Sitzungsende vorbereitet

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| Kopf | **`f5351f6`**, Arbeitsbaum **leer** | `git status --porcelain` (0 Zeilen) |
| B3 (S-7 Bot-Taktik) | **abgebrochen**, kein Bericht, kein Test, keine `usage_b3_*.json` | `ls docs/audits/BERICHT_S7_20261101.md` = nicht vorhanden |
| B3-Reste | 112 Zeilen in `src/bottaktik.py` + `src/main.py`, syntaktisch gueltig, ungeprueft; gesichert als Patch **280 Zeilen** (`eaf258ee`) und als `stash@{0}` | `archiv/unfertig/B3_unfertig_20261101.patch` |
| Kosten starkes Modell | B1 0,5980 + B2 0,2553 = **0,8533 USD**; von 4 USD bleiben rund **3,15 USD** | `usage_b1_*.json`, `usage_b2_*.json` |
| Guthaben | **10,39 USD**, Gesamtverbrauch 39,60 USD (Daniel 01.11. abgelesen) | Register 111 |
| Register | **113 Punkte**, 117 Pruefdateien | `grep -cE`, `ls tests/test_*.py` |
| Letzter belastbarer Sammellauf | 117 Dateien, 115 gruen, 0 rot, 2 ausgesetzt, 4.350 Pruefungen, 628 s (19:14) | `docs/audits/sammellauf_20261101_1914.log` |
| GPT-Gebaeudepaket | **nicht herunterladbar**: gespeicherte HTML enthaelt keine Dateien, Sandbox-Link tot; Daniel hat GPT angewiesen, **vier kleinere ZIPs** daraus zu machen | `C:/Users/saras/Desktop/Nebelseetal_Gebaeude_Design_Gesamtpaket_herunterladen.html` |

## Offene Entscheidungen, von Daniel am 01.11. beantwortet

| Thema | Entscheidung |
|---|---|
| Kartenoptik | **Variante 2**: Motiv rund 44 px plus Geländerahmen je Kachel, damit das Feld sichtbar bleibt |
| Gebaeudemotive | **alle zehn** korrigierten Motive in die Spieldaten und auf die Siedlungskarte |
| Wappen | Zuordnung zu den Bots nach Wahl von Hermes, keine Vorgabe von Daniel |
| Burgen | Zuordnung zu den Weltkarten bleibt offen (Vorschlag erlaubt, im Katalog als Vorschlag markiert) |
| B1-Befunde | **beide sofort beheben**: Heilkunde-Bonus auf `forschung_wirkung.siedlerfaktor` legen, Rinderfarm auf 3/1,5 |

# STAND 01.11.2026, 21:35 - B2 gelaufen, Katalog vollstaendig (zehn Motive, sechs Burgen, zehn Wappen)

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

| Gegenstand | Wert | Beleg |
|---|---|---|
| B1 | Wirtschaft gemessen, Werkzeug + Bericht (263 Zeilen) | Commit `a3fd069` |
| B2 | Kampf gemessen, `tools/mess_kampf.py` + Bericht (272 Zeilen), 40 Laeufe je Wallstufe 0-10 | `docs/audits/MESS_KAMPF_20261101.md` |
| B2 Kernzahlen | Schwelle gemessen == dokumentiert auf allen zehn Stufen; Beute ladungsgedeckelt; Wall 1 braucht 4 Krieger nach SK statt 1 nach AT | Bericht Abschnitte D, E, H |
| Kosten starkes Modell | B1 0,5980 + B2 0,2553 = **0,8533 USD**, von 4 USD bleiben rund 3,15 USD | `usage_b1_*.json`, `usage_b2_*.json` |
| Guthaben | **10,39 USD**, Gesamtverbrauch 39,60 USD (Differenz 1,21 USD, gedeckt) | Register 111 |
| Register | **113 Punkte** | `grep -cE` |
| Symbolkatalog | 11 Seiten: zehn Motive zugeordnet, sechs Burgen, zehn Wappen, Zuordnungsblatt | `docs/SYMBOLKATALOG_Nebelseetal_20261101.pdf` |
| B3 Paket | `docs/auftraege/B3_paket_20261101.md`, 41.579 Zeichen, S-7 Bots erlebbar | Datei |

**Offen aus B2 (Register 110):** die Auftrags-Vorpruefung zaehlt Fernkaempfer und Kundschafter mit, die
Schlacht fuer die Wallschwelle nur Nahkampf. **Offen aus B1 (Register 105):** Heilkunde-Bonus greift nie,
Rinderfarm liefert 1 statt 3 Nahrung.

## Der EINE naechste Schritt

Block **B3** starten (S-7 Bots erlebbar): Paket liegt fertig, Lauf einzeln mit `--usage-file`, fertig erst
an der `usage_*.json`, danach Kernzahlen nachrechnen, voller Sammellauf, Commit oder Ruecknahme,
Kostenzeile im Protokoll. Danach der Optik-Schnitt nach Register 112: Gebaeude kleiner auf dem Feld,
Ressourcenleiste, Motivauswahl, Burgen- und Wappenzuordnung.

---

# STAND 01.11.2026, 21:05 - B1 des starken Modells gelaufen, zwei echte Fehler gefunden

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Blockplan:** `docs/AUFTRAG_STARKES_MODELL_BLOCKPLAN_20261101.md` (B1 bis B8, rund 4,00 USD).
**B1 ist abgeschlossen**, B2 ist vorbereitet und startet als naechstes.

| Gegenstand | Wert | Beleg |
|---|---|---|
| B1 Werkzeug | `tools/mess_wirtschaft.py`, 315 Zeilen, reines ASCII, Rueckgabewert 0 | eigener Lauf |
| B1 Bericht | `docs/audits/MESS_WIRTSCHAFT_20261101.md`, 263 Zeilen, drei Kernaussagen, jede Abweichung | Datei |
| B1 Kosten | **0,5980 USD gemessen** (52 Aufrufe, 11,9 Mio Input / 11,7 Mio Cache, 103 k Output) | `docs/audits/usage_b1_20261101.json` + Preise aus dem Export |
| Sammellauf | 117 Dateien, **115 gruen, 0 rot**, 2 ausgesetzt, 4.350 Pruefungen, 695 s | `docs/audits/sammellauf_20261101_2045_b1.log` |
| Register | **108 Punkte** | `grep -cE '^\| [0-9]+ \|'` |
| Symbolkatalog | `docs/SYMBOLKATALOG_Nebelseetal_20261101.pdf`, 8 Seiten, ueber `tools/icons_katalog_pdf.py` reproduzierbar | Datei |
| Chat-Paket C1 | `docs/auftraege/C1_paket_20261101.md`, 18.810 Zeichen, noch nicht gelaufen | Datei |
| B2 Paket | `docs/auftraege/B2_paket_20261101.md`, 41.868 Zeichen | Datei |

**Zwei Befunde aus B1 (Register 105), nicht behoben:** der Heilkunde-Bonus greift im Spiel nie
(`gebaeude_wirkung` liest `heilkunde` klein), und die Rinderfarm liefert 1 statt 3 Nahrung gegen
Handbuch Seite 10. Beide brauchen Daniels Entscheidung, weil sie Spielwerte beruehren.

## Der EINE naechste Schritt

Block **B2** starten (Kampf messen): Paket liegt fertig, Lauf einzeln mit `--usage-file`, fertig erst
an der `usage_*.json`. Danach Kernzahlen selbst nachrechnen, voller Sammellauf, Commit oder
Ruecknahme, Kostenzeile im Protokoll. Parallel offen: Daniels Motivzuordnung in den Symbolkatalog
einarbeiten (Scheune, Schafzucht, Goldmine, Farm, Kriegerakademie, Erzmine, Steinbruch, Holzfaehler),
die zwei fehlenden Motive seite01_bild02 und bild03 schneiden und die automatische
Hintergrund-Entfernung aus dem Katalogwerkzeug nehmen.

---

# STAND 01.11.2026, 20:15 - Uebergabe geschrieben, Blockplan fuer das starke Modell liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**Diese Sitzung ist abgeschlossen.** Uebergabe: `docs/UEBERGABE_20261101_2010.md` (Kopie auf dem
Desktop, hashgleich), Startzeile dort Abschnitt 8.

**Blockplan fuer `deepseek-v4-pro`:** `docs/AUFTRAG_STARKES_MODELL_BLOCKPLAN_20261101.md` - acht Bloecke,
zusammen 3,55-4,50 USD, Kontostand 11,60 USD.

| Block | Inhalt | Art | Kosten |
|---|---|---|---|
| B1 | Wirtschaft messen (Ertraege, Siedler, Gold, Mana, Nahrung) | Messwerkzeug | 0,35-0,45 USD |
| B2 | Kampf messen (Wall, SK, Beute, 40 Laeufe je Stufe) | Messwerkzeug | 0,35-0,45 USD |
| B3 | S-7 Bots erlebbar (`bottaktik` anbinden) | Umbau | 0,60-0,75 USD |
| B4 | S-3 Forschungsverbund absichern | Umbau klein | 0,35-0,45 USD |
| B5 | S-4 Einheitenverlegung | Umbau | 0,50-0,65 USD |
| B6 | S-6 Dorftransfer (500 Mana + 100 Gold) | Umbau | 0,55-0,70 USD |
| B7 | Balance-Abgleich und Kette ohne Cheats | Messung + Doku | 0,45-0,55 USD |
| B8 | Demo-Reifepruefung (Gates G-01 bis G-07) | Pruefung | 0,40-0,50 USD |

**Kein Block ist gestartet** - Daniel entscheidet ueber den Start. Budget-Wache: bei 3,00 USD gemessenem
Verbrauch wird vor B7/B8 angehalten und gefragt.

## Der EINE naechste Schritt

Block **B1** starten: Paketdatei bauen (20.000-45.000 Zeichen), Zeichen/Token/USD **drucken** und Daniel
vorlegen, dann `tools/mess_wirtschaft.py` und `docs/audits/MESS_WIRTSCHAFT_<datum>.md` vom starken Modell
bauen lassen; danach Kernzahlen selbst nachrechnen, voller Sammellauf, Commit oder Ruecknahme, Kostenzeile
im Protokoll. Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

---

# STAND 01.11.2026, 19:25 - Demo wird LEER ausgeliefert, externes GitHub-Feedback aufgenommen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was seit 19:00 dazukam

**Die Demo wird leer ausgeliefert** (Register 101, Daniels Vorgabe "in der demo exe darf es keine
vorhandenen spielstaende geben sie muss leer sein"):

| Gegenstand | Wert | Beleg |
|---|---|---|
| Bau prueft das Paket | bricht ab, wenn in `data/` oder `assets/` ein Spielstand, Admin-Teststand, Passworttor oder eine Sperrdatei liegt | `tools/build_public_exe.py` `spielstaende_im_paket` |
| Demo-Speicherordner | `%LOCALAPPDATA%\Nebelseetal_Remake\Demo` - eigener, nie benutzter Ordner; der alte Testordner wird nicht mehr gelesen | `src/public_start.py` |
| Testspielstaende | **16 Dateien geloescht** (nur Teststaende, Daniels Ansage), vorher hashgeprueft in `archiv/testspielstaende_20261101.zip` (1.116.438 Byte, testzip sauber) | ZIP + `MANIFEST_SHA256.txt` |
| Zurueck im Profil | nur `tor.json` (Passworttor, kein Spielstand); veraltete `game.lock` entfernt | `ls ~/.nebelseetal/` |
| Pruefdatei | `tests/test_demo_leer.py` **28/0/0** | Lauf 19:12 |
| Nachbar | `test_public_edition_fix04j` 6 Tests OK (Wache auf den neuen Ordnernamen umgestellt) | Lauf 19:13 |
| Voller Sammellauf | **117 Dateien, 115 gruen, 0 rot, 2 ausgesetzt, 4.350 Pruefungen, 628 s** | `docs/audits/sammellauf_20261101_1914.log` |
| Auftrag 9 (Chat-Modell) | `docs/AUFTRAG_GPT_TRANSFER_S3_S4_S6_20261101.md`, 10.651 Byte, Kopie auf dem Desktop | `59002d91...` |

**Externes GitHub-Feedback vom 01.11.2026 aufgenommen** (Register 102): der Bericht prueft ausschliesslich
den OEFFENTLICHEN Stand (`main` = FIX04j, `v0.4.0-test.1`, PR #1 mit eigener Wurzel), nicht den lokalen HEAD.
Einordnung, Zuordnung zu vorhandenen Stellen und die sieben Demo-Freigabe-Gates G-01 bis G-07 stehen in
`docs/EXTERNES_FEEDBACK_GITHUB_20261101.md`; das Original liegt hashgeprueft unter
`archiv/eingaben/20261101_github_feedback/` (31.499 Byte, `dff01476...`). Es betrifft nur das Online-Repo und
ist reines Feedback: **nichts davon ist umgesetzt, kein Push, kein Release.** Zwei Punkte bleiben bei Daniel:
Lizenz fuer den eigenen Code und rechtliche Einordnung der historischen Grafiken.

## Der EINE naechste Schritt

**Das Bot-Taktikpaket gegen den Code pruefen**
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`,
47.159 Byte) und danach S-7 vorbereiten (Bots erlebbar, `bottaktik` anschliessen). Fuer das starke Chat-Modell
liegt das naechste Paket als `docs/AUFTRAG_GPT_TRANSFER_UND_DEMO_REST_20261101.md`. Danach S-3, S-4, S-6, S-7,
S-8 (Bilanz und Weltensprung 500 Mana plus 100 Gold), dann Demo-Bau mit den Gates G-01 bis G-07.
Arbeitsweise: ein Schritt = ein Commit = ein gruener voller Sammellauf.

---


# STAND 01.11.2026, 19:00 - S-5 gebaut: die Weltkarten zeigen Gelaende

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

**S-5 ist gebaut und gruen** (Register 91, Freigabe 92). Das Gelaende der Weltkarten kommt aus
`portalraum.weltbild`:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Quellen | sieben Gelaendearten und ihre `haeufigkeit` NUR aus `data/gelaende.json` (Summe 100) | `portalraum.gelaendeverteilung` |
| Raster | 10x10 Gruppen zu je 2x2 gleichartigem Gelaende = 100 Gruppen, 400 Felder | `portalraum.weltbild` |
| Verteilung | exakt 4 x haeufigkeit Felder je Art (Grasland 80, Nebelsee 28 ...) | Pruefdatei Abschnitt 3 |
| Seed | SHA-256 aus `kennung|seed`, Konfigurationswert `weltkarten_seed` in `data/welten.json` | `portalraum._seed_zahl` |
| Stabilitaet | gleicher Name und Seed = bytegleiches Raster, auch in einem frischen Interpreter | Pruefdatei Abschnitt 5 |
| Anzeige | Gelaendefarbe je Feld, Legende mit Haeufigkeiten, angewaehltes Feld mit Gelaendenamen | `main._render_portal` |
| Wirkung | KEINE Bauplatz-, Rohstoff- oder Ertragswirkung; Ernte vor/nach Weltwechsel identisch | Pruefdatei Abschnitt 9 |
| Pruefdatei | `tests/test_weltbild_gelaende.py` **135/0/0** | Lauf 18:53 |
| Voller Sammellauf | **116 Dateien, 114 gruen, 0 rot, 2 ausgesetzt, 4.349 Pruefungen, 305 s** | `docs/audits/sammellauf_20261101_1853.log` |
| Register | 91 (Status GEBAUT) und 100 (Nebenbefund) | `docs/PRUEFREGEL_ORIGINAL.md` |
| EXE | **47.981.465 Byte**, SHA256 `e361a2b3b8f1ddf062ab82041fc14a84232b79519af98e4ee2662aeab9585683`, gebaut 19:01 zu Code-Stand `b256f3b` | `stat -c %s`, `sha256sum` |
| EXE-Startbeleg | Kind-PID **15392**, Fenster `Nebelseetal Remake`, `MainWindowHandle` 86509210, nach **149 s** Responding True, danach beendet | `Get-Process`, Bildschirmaufnahme (Tor mit Passwortfeld) |

**Nebenbefund, im selben Commit behoben:** die Portalansicht gab die Nummern des Spielstands (d04 = 4)
ungefiltert als Index an das Raster - die eigene Weltkarte erschien als fremde (Bannerfarbe rot). Die neue
Pruefdatei hat es gefunden, keine bestehende Wache (Register 100).

## Der EINE naechste Schritt

**Das Bot-Taktikpaket gegen den Code pruefen**
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`,
47.159 Byte) - wie beim Textpaket jede Aussage am heutigen Stand messen, Widersprueche einzeln benennen, dann
S-7 (Bots erlebbar, `bottaktik` anschliessen) vorbereiten. Danach S-3 (Forschungsuebernahme, acht
Entscheidungen), S-4, S-6 (Dorftransfer), S-7, S-8 (Bilanz und der neue Weltensprung-Preis 500 Mana plus
100 Gold aus Register 93), dann Demo-Bau und Freigabepruefung. Arbeitsweise: ein Schritt = ein Commit =
ein gruener voller Sammellauf; offene Punkte sammeln statt einzeln fragen.

---

---

# STAND 01.11.2026, 18:40 - Fragenrunde beantwortet, S-5 FREIGEGEBEN

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was seit 17:26 dazukam

**Der GPT-Antworttext zum Demo-Paket ist geprueft, nicht uebernommen.** Pruefvermerk
`docs/audits/PRUEFVERMERK_GPT_TEXTPAKET_20261101.md` (Commit `b91186f`): 26 Angaben stimmen mit dem Code,
**sieben muessen raus**, vier fehlen. Der schwerste Befund **W-01**: das Textpaket behauptet an fuenf
Stellen, die Weltkarten zeigten Gelaende - das ist heute falsch (`portalanzeige` kennt kein Gelaende,
Register 91 steht auf NOCH NICHT GEBAUT) und wird erst mit S-5 wahr. Weitere: Spionage ist nicht
"gar nicht da" (Diebesgilde und sechs Kundschafter-Einheiten existieren), `Ragnaroeck` statt `Ragnaroek`,
Tempel auf Sumpf erzeugt 0 statt 1 Mana, Siedlerobergrenze ist belegt statt unbekannt, Limbus doppelt,
Ausbildungsdauer im Code geregelt statt unbekannt.

**Alle dreizehn offenen Fragen sind beantwortet** (`docs/FRAGEN_AN_DANIEL_20261101_1820.md`, Abschnitt
Antworten). Die Entscheidungen stehen als Register 92 bis 99.

| # | Entscheidung | Wirkung |
|---|---|---|
| 92 | **S-5 freigegeben** | Weltbild als Gelaende wird jetzt gebaut |
| 93 | **Weltensprung 500 Mana plus 100 Gold** (5.000 bleibt Originalwert) | Einbau in S-8; heute bucht der Code noch 5.000 |
| 94 | `weltkarten_seed` bekommt einen festen Wert | beim Demo-Bau nachtragen |
| 95 | "Demo" im Titel | Release-Texte |
| 96 | Handbuch erst nach S-5 | keine Veroeffentlichung vorher |
| 97 | Handbuch als eigene Datei neben dem Release | Ablage |
| 98 | Limbus bleibt Weltname, Ebene heisst "der magische Limbus" | Spielertexte |
| 99 | **Die Demo ist ein moeglichst weit umgesetztes Testspiel** | Funktionen vor Release-Texten |

## Der EINE naechste Schritt

**S-5 - das Weltbild als Gelaende** (Register 91 Vorgabe, 92 Freigabe): sieben Gelaendearten aus
`data/gelaende.json` (Feld `haeufigkeit`, Summe 100) als 2x2-Bloecke auf 20x20 = 400 Feldern, stabiler
Seed je Welt aus einem neuen Konfigurationswert `weltkarten_seed` in `data/welten.json`. Andockstellen:
`portalraum.anzeige_raster` (Feld bekommt Gelaende dazu), `main._render_portal`/`_portal_feld_waehlen`,
Farben und Namen aus `gelaende.farbe`/`gelaende.name`. Keine Orte, Doerfer, Gegner oder dauerhaften
Markierungen. Neue Pruefdatei, voller Sammellauf, Registereintrag an Punkt 91, Protokollzeile, ein Commit.

**Danach in dieser Reihenfolge:** das Bot-Taktikpaket gegen den Code pruefen
(`archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md`),
dann S-3 (Forschungsuebernahme, acht Entscheidungen), S-4, S-6 (Dorftransfer), **S-7 (Bots erlebbar,
`bottaktik` anschliessen)**, S-8 (Bilanz und der neue Weltensprung-Preis), dann Demo-Bau und
Freigabepruefung.

---

# STAND 01.11.2026, 17:26 - S-2c abgeschlossen: das Dorfzentrum ist das Lager, und den Platz bestimmt der Spieler

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-2c und S-2c-D sind fertig und gruen** - das Dorfzentrum ist Menuepunkt UND Gebaeude, die
Lagerverwaltung steht darin, und es kommt kostenlos mit jeder Gruendung, ohne dass das Spiel den Platz
vorgibt:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Gebaeude | Kennung bleibt `lager`, Anzeigename **Dorfzentrum**, `alias: ["Lager"]`, `max_je_siedlung: 1` | `data/buildings.json` |
| Alias-Erkennung | `finde_gebaeude` liest zusaetzlich den `alias` - ein Altstand mit "Lager" in `bauten` zaehlt als Dorfzentrum, ohne Migration | `src/gelaende.py` |
| Menue | `MENUE_ENTFALLEN = {"Lager"}` blendet den Punkt in der ANZEIGE aus; `MENU_ITEMS` bleibt die belegte Original-Liste (16 Eintraege); Anker fuer Stellmacher/Diebesgilde ist `MENUE_ANKER = "Dorfzentrum"` | `src/main.py` |
| EINE Lageransicht | `_render_storage(eigener_titel=False)` wird von `_render_overview` gerufen; die alte Route traegt `STILLGELEGT` | `src/main.py` |
| Platzwahl | `Settlement.dorfzentrum_offen` (Vorgabe False) wird bei jeder Gruendung gesetzt; `_dorfzentrum_setzen(feld)` setzt das Gebaeude kostenlos auf das vom Spieler gewaehlte Feld | `src/main.py` |
| Abriss | Das einzige Dorfzentrum ist gesperrt - auch unter dem alten Namen "Lager" | `_karten_abreissen` |
| Pruefdatei | `tests/test_dorfzentrum_ist_lager.py` **82/0/0** | Lauf 17:23 |
| Voller Sammellauf | **115 Dateien, 113 gruen, 0 rot, 2 ausgesetzt, 4.214 Pruefungen, 272 s** | `docs/audits/sammellauf_20261101_1723_s2cd.log` |
| Register | 90 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Daniels Entscheidung, woertlich (01.11.2026):** "kostenlos bei jeder gruendung mitgesetzt aber das setzen
lassen ist wichtig damit der spieler bestimmt welches feld seiner karte besetzt wird". Gelesen als
MITGELIEFERT, nicht automatisch gesetzt: die Gruendung setzt nur das Kennzeichen, die Siedlungskarte zeigt
den Kasten "Dorfzentrum einplanen" mit dem Knopf "Dorfzentrum hier setzen (kostenlos)". Die S-1-Regel bleibt
unberuehrt - es bleiben **drei** automatische Startgebaeude, alle 35 Wachen unveraendert gruen.

**Was das im Spiel bedeutet:** Im Menue steht kein eigener Punkt "Lager" mehr. Das Dorfzentrum zeigt oben die
Uebersicht (naechster Schritt, Siedler, Siedlungen, Auftraege, Gebaeudewirkungen) und darunter die
Lagerverwaltung des aktiven Ortes: Bestand, Waren, Einheiten und die Werkstaetten mit ihren Warteschlangen.
Nach der Gruendung wahlt der Spieler das Feld des Dorfzentrums selbst; ein zweites ist nicht baubar, das
einzige nicht abreissbar.

## Werkzeug wiederhergestellt: PyInstaller

Das Hermes-Update am 01.11. (13:59-14:52) hat die Python-Runtime getauscht; `PyInstaller` fehlte danach. Die
Pruefung `tools/build_exe.py --pruefen` lief noch, der Bau brach mit "No module named PyInstaller" ab und
liess die alte EXE unangetastet. Auf Daniels Freigabe mit `uv pip install pyinstaller` (6.22.3)
nachinstalliert. Nach dem Commit `4ed7fbb` neu gebaut: **EXE 47.974.724 Byte, SHA256 `595c48bf...`**
(17:29), **Start belegt** - Kind-PID 13892, Fenster "Nebelseetal Remake", MainWindowHandle 163907294, nach
116 s und 129 s Responding True, danach beendet. Zwischenbau 17:14 (47.972.104 Byte, `4df48ffa...`) war nur
der Werkzeugbeweis und ist ueberholt.

## Der naechste Schritt

**S-5: das Weltbild als Gelaende** (Daniel hat die Ableitung entschieden: die sieben vorhandenen
Gelaendearten mit ihren Gewichten aus `data/gelaende.json`, als 2x2-Bloecke mit stabilem Seed je Welt - siehe
Register 91). Danach S-3 (Forschungsuebernahme, Papier liegt), S-4, S-6, S-7, S-8.

**Papier eingetroffen und geprüft:** die Antwort des Chat-Modells auf Auftrag 7 (S-7/S-8/Demo-Anleitung)
liegt in `archiv/eingaben/20261101_gpt_antworten/HERMES_ENTWURF_S7_S8_DEMO_ANLEITUNG_20261101.md`; der
Gegenbefund am echten Code steht in `docs/audits/PRUEFVERMERK_S7_S8_ENTWURF_20261101.md`. **Wichtigster
Befund:** die vom Papier befürchtete "blockierende Mana-Lücke" gibt es nicht — der **Tempel** ist ein
Mana-Produzent (5/h auf Nebelsee, sonst 1/h) und kommt seit S-1 bei jeder Gründung mit. Der Weltensprung
kostet belegt 5.000 Mana (`data/welten.json`, aus portal.php 2005); 500 Mana wären für ein einzelnes Dorf
auf Normalgelände in rund 21 Spieltagen erspart, 5.000 in über 200. Mana wird außerdem bei **jeder**
Portalreise verbraucht (5 + 0,5 je Feld + 20 je Zonenstufe, `src/auftraege.py`). Der achte Bot-Zustand heißt
`FLIEHEN`, nicht `FLEHEN`. Offen bleiben: Goldpreis `G`, echte 24-Spielstunden-Messung, Bot-Ereignisquellen.

**Auftrag 7 beantwortet und abgelegt:** `AUFTRAG_GPT_S7_S8_UND_DEMO_ANLEITUNG_20261101.md` - S-7 (Bots
sichtbar ohne Kartenmarker, kein Angriff), S-8 (Bilanz Mana und Reisekosten) und der gefuehrte Start der
Demo. Die Antwort ist geprueft (siehe oben), **gebaut ist davon noch nichts**. Auf dem Desktop liegt genau diese eine Datei.

# STAND 01.11.2026, 12:20 - S-2b abgeschlossen: die Portal-Uebersicht zeigt Weltkartenliste und Gelaendekaestchen

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-2b ist fertig und gruen** - die Portalansicht traegt oben die sechs belegten Weltkarten mit Namen und
Kennzeichen, darunter das Gelaendekaestchen der aktuellen Welt mit anklickbaren Feldern:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Weltkartenliste | `portalraum.weltkarten(eigene_nummern, unterwegs)`: sechs Zeilen mit Nummer, Kennung, Name, Status (eigene Welt / fremde Welt / noch nicht bespielbar), Bannerfarbe als Wort, `waehlbar` samt Grund | `src/portalraum.py` |
| Gelaendekaestchen | 20 x 20 = 400 Felder (`portalraum.anzeige_raster`), ein Klick waehlt ein Feld (`_portal_feld_waehlen`), Auswahl steht als `portal_auswahl` in der Ansicht | `src/main.py` |
| Startwelt | **Midgard (d04 = Nummer 4)** statt des alten Vorschlags Armageddon, im Aufbau und beim Laden; Daten in `data/welten.json` (`startwelt`, `weltkarten_spielbar`) | `src/welt.py` (`startwelt_nummer()`), `GameState` |
| Sperre | Weltensprung gesperrt, solange Auftraege unterwegs sind (Hin- oder Rueckreise, auch Handel) - `auftraege.laufende()` mit der SPIELUHR, `_unterwegs_anzahl()` | Daniel, Anhang 2 („ein weltenwechsel ist fuer das dorf gar nicht moeglich solange auftraege einheiten truppen oder sonst was unterwegs ist auch handel z. b.“) |
| Pruefdatei | `tests/test_portal_uebersicht.py` **60/0/0** | Lauf 12:05 |
| Voller Sammellauf | **114 Dateien, 112 gruen, 0 rot, 2 ausgesetzt, 4.132 Pruefungen, 776 s** | `docs/audits/sammellauf_20261101_1205.log` |
| Register | 88 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Was das im Spiel bedeutet:** Das Portal oeffnet mit der Liste Armageddon, Ragnaroek, Utgard, Midgard,
Valhalla, Limbus. Eigene Weltkarten stehen gruen, fremde rot (belegte Bannerfarben aus portal.php 2005),
die vier noch nicht bespielbaren sind als solche benannt und nicht anklickbar. Bespielbar sind zuerst
Midgard (Start) und Valhalla. Unter der Liste liegt das 20 x 20-Kaestchen der aktuellen Welt; ein Klick
waehlt ein Feld an, und die Ansicht sagt ausdruecklich, dass der Dorftransfer erst mit S-6 kommt.

## Nebenbefund, behoben: Nummer und Index waren vermischt

`portalraum` rechnet mit dem Index 0..19, der Spielstand fuehrt die 1-basierte Nummer aus der Kennung
(d04 = 4). Bis S-2a standen beide unvermittelt nebeneinander: `wechsel_erlaubt(20, ...)` lehnte die
zwanzigste Weltkarte ab („Unbekannte Ausgangswelt: 20“), waehrend `_dimensionsname(20)` sie benannte und
der Knopf „20“ sie anbot; „01“ buchte auf Ragnaroek statt auf Armageddon. Die Umrechnung steht jetzt an
EINER Stelle (`nummer_von`, `kennung_von`, `index_von`, `nummer_von_index`) und ist im neuen Prueftest,
Abschnitt 4, belegt. `src/spielschicht.py` fuehrt seinen eigenen Zustand weiter absichtlich 0-basiert -
der Hinweis steht als Docstring dort, damit es niemand „vereinheitlicht“.

## Ziel nach den groben offenen Punkten: eine offizielle spielbare Demo-EXE auf GitHub

**Daniel, 01.11.2026, woertlich:** „sobald die die aktuell groben offenen punkte im spiel bearbeitet
sind möchte ich eine offiziele spielbare demo exe meines spiels auf github hochladen“.

Damit ist der Meilenstein klar und gehoert ab jetzt in jede Uebergabe:

* **Kein Zwischen-Release.** Erst wenn die groben offenen Punkte abgearbeitet sind, wird die Demo
  veroeffentlicht - gemeint sind mindestens **S-2c** (Dorfzentrum ist das Lager), **S-3** (Forschung
  ueber die Bibliothek), **S-4** (Einheitenregel), **S-5** (Weltbild 20 x 20), **S-6** (Dorftransfer),
  **S-7** (Bots sichtbar, kein Angriff) und **S-8** (Bilanz Mana und Reisekosten).
* **Offiziell heisst geprueft:** eine EXE, die startet, eine Partie ohne Absturz erlaubt und deren
  Spielstand sich speichern und laden laesst - belegt mit Sammellauf, EXE-Start und einem
  Spieltest-Verlauf, nicht behauptet.
* **Bekannte Grenze, die in die Release-Notizen gehoert:** der Remote-Stand auf GitHub ist **nicht**
  der Arbeitsstand (zuletzt `954097aa` vom 31.10.). Vor dem Hochladen wird die Reihenfolge
  festgelegt: Arbeitsstand committen, `main` aktualisieren, Version setzen, Release-Notizen
  schreiben, Demo-EXE anhaengen.
* **Teststaende sind keine Spielstaende** (Daniel, Anhang 2: „Aktuelle spielstände sind nur teststände
  zur entwicklung“). Fuer die Demo wird ein frischer Spielstart geprueft, kein alter Teststand.

## Was bewusst NICHT gebaut wurde

* **Gelaende je Feld.** Das Handbuch nennt kein Gelaende je Weltkartenfeld; das Kaestchen zeigt deshalb
  die belegten Bannerfarben und die Auswahl, keine erfundenen Gelaendearten. Gehoert zu S-5, offener Punkt.
* **Der Dorftransfer selbst.** Ein Klick merkt nur ein Feld; uebertragen, Kosten und Postfach kommen mit S-6.
* **Die Limbus-Doppelbedeutung ist weiter offen** (Weltname *und* Raum). Die Anzeige vermeidet die
  Entscheidung: die Liste heisst „Weltkarten“, der umgebende Raum wird nicht benannt.

## Der naechste Schritt

**S-2c: das Dorfzentrum ist das Lager.** Andockstellen: `_render_overview` (heute Dorfzentrum),
`_render_storage` (heute Menuepunkt „Lager“), `wirtschaft.dorf_uebersicht`, `ortsbestand_text(siedlung)`,
`data/buildings.json` -> Eintrag `lager` (`max_je_siedlung` ist heute nicht gesetzt, „ein Lager je Dorf“
muss dort durchgesetzt werden).

**Vor dem Bau zu entscheiden (steht gesammelt in der Uebergabe):** ob das Dorfzentrum als Gebaeude bei
jeder Gruendung mitgesetzt wird (dann vier Startgebaeude statt drei - S-1 und seine 35 Pruefungen ziehen
mit) oder ob es gebaut werden muss.

**Papier bereit, nicht gebaut:** `docs/design/VERBUND_FORSCHUNG_EINHEITEN_TRANSFER_20261101.md`
(46.061 Byte, SHA256 `9815fb27…`, 327 Zeilen) - Entscheidungsentwurf zu S-3 (Forschungsuebernahme),
S-4 (Einheitenpruefung, stationierte Truppen) und S-6 (Dorftransfer), mit Kennzeichnung BELEGT /
VORSCHLAG / UNBEKANNT, einem Pruefplan und acht offenen Entscheidungen in Abschnitt 7. **Selbstauskunft
eines externen Modells:** jede Zahl vor dem Einbau selbst nachpruefen.

**Desktop:** keine Kopien mehr. Die Uebergabe liegt in `docs/UEBERGABE_20261101_1105.md` und
`D:\Arbeiten\Hermes\Uebergaben\20261101_1105\`.

# STAND 01.11.2026, 09:47 - S-1 abgeschlossen: die Gruendung bringt drei Startgebaeude mit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was in dieser Sitzung gebaut wurde

**S-1 ist fertig und gruen** - der Patch aus `docs/audits/S1_ENTWURF_20261101/` ist angewendet, die
sieben roten Pruefdateien sind einzeln nachgezogen, der volle Sammellauf ist sauber:

| Gegenstand | Wert | Beleg |
|---|---|---|
| Code | `STARTGEBAEUDE_VORLIEBEN`, `_startgebaeude_setzen`, `_startgebaeude_meldung` in `src/main.py`, benutzt an beiden Gruendungswegen (`_erste_siedlung_gruenden`, `GruendungGameState.gruendung_ausfuehren`) | `git diff`, Register 86 |
| Pruefdatei | `tests/test_gruendung_startgebaeude.py` **35/0/0** | Lauf 09:24 |
| Nachgezogene Wachen | 7 Dateien, jede mit Satz und Quelle im Kommentar, keine Wache geloescht | Abschnitt unten |
| Voller Sammellauf | **112 Dateien, 111 gruen, 0 rot, 1 ausgesetzt, 4.125 Pruefungen, 598 s** | `docs/audits/sammellauf_20261101_0931.log` |
| EXE | **46.144.237 Byte**, SHA256 `b2194fc5…`, Start belegt (Kind-PID 11692, Fenster `Nebelseetal Remake`, 95 s stabil) | `sha256sum`, `Get-Process` 09:48 |
| Register | 86 | `docs/PRUEFREGEL_ORIGINAL.md` |

**Was das im Spiel bedeutet:** jede Gruendung - erstes Dorf UND jede Kolonie - setzt Holzfäller
(moeglichst Wald), Steinmetz (moeglichst Huegel oder Berg) und Tempel (moeglichst Nebelsee, sonst
Steppe) auf freie Felder, kostenlos, ohne Siedlerabzug, der Tempel ohne Baukunst. Die Meldung nennt je
Gebaeude Gelaende und Feld und sagt ausdruecklich, wenn das Wunschgelaende fehlt und ein Ersatz
genommen wurde. Startressourcen bleiben 10 Siedler / 100 Holz / 100 Stein.

## Die sieben nachgezogenen Wachen (Beleg fuer die Ruecknahme am 04:02)

Sechs der sieben haengen an EINER gemeinsamen Wache in `tools/gpt_erzeuge_startstaende.py` (sie erzeugt
den Startzustand fuer die GPT-Pruefdateien): `assert s.bevoelkerung == 10.0 and not s.bauten` ist auf
die neue Wahrheit gestellt - zehn Siedler, genau Holzfaeller, Steinmetz und Tempel, je Stufe 1.
`test_produktionskette_ohne_cheats` hatte ihre eigene Zeile und ist ebenso umgestellt. Die uebrigen
Erwartungen waren Zahlen, die auf dem leeren Aufbauzustand beruhten und offen angehoben wurden:
Holz 101 -> 105 und Stein 101 -> 103 je Stunde (Grundertrag 1/h plus Startgebaeude 4/h bzw. 2/h),
25 Stunden 125 -> 225 bzw. 175, Frischstart nach zwei Bauten 90/90 -> 94/92.

## Der naechste Schritt

**S-2b: die Portal-Uebersicht** - oben die Liste der Weltkarten mit Namen, darunter das
Gelaendekaestchen der aktuellen Welt (Daniel, Anhang 3 Frage 30). Danach **S-2c: Dorfzentrum ist das
Lager** (Lagerverwaltung im Dorfzentrum, ein Lager je Dorf - Anhang 1 Abschnitt 2, M-11).

**Erledigt in dieser Sitzung (S-2a, Register 87, Commit folgt):** der Menuepunkt Karten ist weg (die
alte Weltkarte ist stillgelegt und traegt einen Vermerk), und die Anzeige sagt Weltkarte und
Weltensprung statt Dimension - `MENU_ITEMS` hat 16 Punkte, das alte `test_weltkarte` ist als
Zeitzeugnis ausgesetzt, die neue Wache ist `tests/test_weltkarten_anzeige.py` (27/0/0).

**Vorbereitet, noch nicht gebaut:** das Papier des starken Chat-Modells zu Burgen, Wappen und
Weltbild liegt in `docs/design/ASSETS_UND_WELTBILD_20261101.md`; es gehoert zu S-5 und S-7 und ist
dort gegengeprueft einzubauen. Das Assetpaket selbst liegt in
`archiv/eingaben/20261101_burgen_wappen/` (ZIP plus zwei entpackte Kontaktboegen).

**Nebenher offen, von Daniel geliefert:** das Assetpaket `Hermes_Nebelseetal_Assets_Icons.zip`
(2 Kontaktboegen, je 1448 x 1086 px, RGBA: 6 Burgen, 10 Wappen) liegt auf dem Desktop und ist noch
nicht im Projekt. Es gehoert zu S-5 (Weltbild) und S-7 (Bots) - der Auftrag an das starke Chat-Modell
steht in `docs/AUFTRAG_GPT_WELTBILD_UND_ASSETS_20261101.md`.

# STAND 01.11.2026, 09:17 - 35 Fragen beantwortet, Fahrplan neu

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Was sich seit 03:32 geaendert hat

**Daniel hat alle offenen Fragen beantwortet** (35 Fragen in sieben Formularen). Die Antworten stehen woertlich in `docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md` (Anhang 3) und sind bindend. Die wichtigsten Aenderungen am Modell:

| Punkt | neu |
|---|---|
| Transfer | **Mana**, 500 statt 5.000; Tempel 20/h Nebelsee, 5/h sonst (VORSCHLAG) |
| Bots | **nur Koordinaten**: sechs Bots, je ein Dorf, feste Position, **kein Angriff**, keine Taktik |
| Weltkarten | **sechs belegte Namen** (Armageddon, Ragnarok, Utgard, Midgard, Valhalla, Limbus), bespielbar zuerst Midgard und Valhalla, Start in Midgard |
| Dorftransfer | **ein Dorf je Vorgang**, Einstieg per Klick aufs freie Feld |
| Spionage | Kundschafter-Auftrag, Bericht exakt, gehoert zur Kampfplanungsseite |
| Begriffe | Dimensionen heissen **Weltkarten und Weltensprung** (ab S-2 in der Anzeige) |

**Gebaut wurde in dieser Runde nichts** - Daniel wollte erst alle Antworten und dann die Uebergabe.

## Der naechste Schritt

**S-1 abschliessen.** Der Patch liegt in `docs/audits/S1_ENTWURF_20261101/`; **sieben** Pruefdateien muessen dabei einzeln nachgezogen werden (Liste in der Uebergabe 09:17, Abschnitt 4). Danach S-2 bis S-8 nach dem Fahrplan in Anhang 3.

Guthaben: **3,03 USD** (diese Sitzung hat 1,27 USD gekostet).

# STAND 01.11.2026, 03:32 - Entscheidung 1 gebaut, Bot-Taktik-Modul liegt bereit

> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen.

## Neu seit 02:48

| Paket | Register | Pruefdatei | Sammellauf |
|---|---|---|---|
| **Bot-Taktik-Modul `src/bottaktik.py`** - acht Zustaende, fuenf Taktiken, Gedaechtnis, Koordinaten, Manhattan-Abstand, sichtbare Signale. **Noch nicht von main.py benutzt** (Anschluss = S-7) | 85 | `test_bottaktik` 48/0/0 | 03:22: 111 Dateien, 110 gruen, 0 rot, 1 ausgesetzt, 4.089 Pruefungen, 357 s |
| Modulkarte neu gebaut (50 Dateien) | - | `test_projektpfade` 103/0/0 | - |

## Der naechste Schritt (unveraendert S-1)

Gruendung setzt Tempel, Holzfaeller und Steinmetz samt Startressourcen und nennt die Felder. Einzelheiten in der Uebergabe, Abschnitt 4.


> Neuester Block. Die Bloecke darunter sind aeltere Staende und bleiben stehen (nichts wird geloescht).

## Was gerade gebaut wurde (Commit folgt in dieser Sitzung, Register 84)

| Paket | Register | Pruefdatei | Sammellauf |
|---|---|---|---|
| **Entscheidung 1: jeder Angriff reist** - ein Kern `_angriff_auftrag_starten`, `_angriff_durchfuehren` entfernt, `_attack`/`_attack_map`/`_auftrag_angriff` starten Auftraege, Kampf erst bei Ankunft | 84 | `test_kampf_einhaengung` 58/0/0, `test_produktionskette_ohne_cheats` 48/0/0, `test_gpt_kampf_botbeute_echte_kasse` 7/0/0, `test_durchspiel` 65/0/2 | 02:39: 110 Dateien, 109 gruen, 0 rot, 1 ausgesetzt, 4.041 Pruefungen, 363 s |
| **Spielspannung und Bot-Taktik als Entwurf** (starkes Modell, 189 Zeilen): Spielschleifen, sieben Spannungsquellen, Zustandsautomat mit fuenf Taktiken, Gedaechtnis, sichtbare Vorzeichen, acht Widersprueche, Top 10 nach Wirkung | - | `docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md` | - |

## Der naechste Schritt

**S-1 aus dem Modell sechs Doerfer**: Gruendung setzt Tempel, Holzfischer (Wald) und Steinmetz (Huegel/Berg) und die Startressourcen 10 Siedler / 100 Holz / 100 Stein; die Meldung nennt die Felder. Andockstellen: `_erste_siedlung_gruenden`, `_kolonie_gruenden` (src/main.py), `gelaende.bau_moeglich`, `data/buildings.json` (Tempel-Ausnahme bei der Gruendungssetzung). Neue Pruefdatei; betroffen: `test_startspiel`, `test_durchspiel`, `test_originalkarten_baukasse`.

**Vor S-1 zu entscheiden (Fragen an Daniel, gesammelt):** Transferwaehrung (Mana empfohlen), Bot-Umfang (2-3 Taktiken, 1-3 Doerfer empfohlen), Goetterschutz-Dauer (so lassen und nur anzeigen empfohlen), Kartenziehung (nach dem Dorf-Umbau empfohlen). Bis zur Antwort gilt die Empfehlung, im Code als VORSCHLAG gekennzeichnet.

# STAND 01.11.2026, 01:00 — verbindlich für den Wiedereinstieg

> Dieser Block steht ÜBER den älteren Ständen. Die Angaben darunter (FIX05, FIX04j…) sind
> historisch und nicht mehr die Wahrheit. Alles hier ist gemessen, der Beleg steht daneben.

## Was in der Sitzung 31.10./01.11.2026 gebaut und committet wurde

| Paket | Commit | Register | Prüfdatei | Sammellauf |
|---|---|---|---|---|
| A-1 Mengeneingabe für Ausbildung **und** Ware (Daniels Antwort 1 = B) | `7720e99` | 79 | `test_mengeneingabe` 69/0/0 | 22:57: 107 Dateien, 106 grün, 0 rot |
| A-3 Dorfübersicht rechts der Karte + Siedler-Schalter (Antwort 2 = A, Antwort 5 = B) | `fe97182` | 80 | `test_dorfuebersicht` 24/0/1 | 23:22: 108 Dateien, 107 grün, 0 rot |
| A-6 Siedler-Reserve sichtbar und gewarnt | `df6da4d` | 81 | `test_siedler_warnung` 29/0/1 | 23:52: 109 Dateien, 108 grün, 0 rot |
| A-2 Original-Gebäudemotive auf der Karte | `97c1301` | 82 | `test_gebaeude_motive` 43/0/1 | 00:16: 110 Dateien, 109 grün, 0 rot, 4.022 Prüfungen |
| Bildquellen gesichtet (A-2/A-4) | `8835f0a` | — | — | — |
| Weltkarten-Konzept (Lords Mobile) aufgenommen und abgeglichen | `a037d5b` | — | — | — |
| A-5 Designkonzept als **Papier** vorgelegt | `b6a886f` | 83 | — | — |

Letzte EXE: `46.144.440 Byte`, SHA256 `6030147d…`, Startbeleg: Prozess 53 s stabil, Fenster mit
Titel. **Offen:** die Sichtprüfung des Passworttors (Tk liefert keinen UIA-Baum).

## Daniels Entscheidungen aus dem Formular (31.10.2026) — bindend

1. A-1 Umfang = **B**: Ausbildung **und** Ware-Herstellung. *gebaut*
2. A-3 Ort = **A**: rechte Spalte der Siedlungskarte. *gebaut*
3. A-4 = **A**: aus den Handbuchbildern schneiden. **Erledigt durch Befund:** die 244
   Handbuchbilder enthalten **keine** Rohstoff-Icons (nur Gebäudemodelle). Die einzige echte
   Quelle ist die Rohstoffleiste auf `docs/original/karten/gamestar_nebelseetal_1838855_full.jpg`
   (20–30 px, unscharf). **Neue Entscheidung nötig:** als Vorlage nachzeichnen (Empfehlung)
   oder A-4 nach der Demo schieben.
4. A-5 = am Original orientiert, benutzerfreundlich, jedes Menü und jeder Button mit genug Platz.
   **Papier liegt vor** (`docs/design/SIEDLUNG_KONZEPT_20261101.html`, Bild daneben), Abnahme offen.
5. Siedler-Mechanik = **B**: Bauten binden keine Siedler mehr. *gebaut als Schalter*
   `data/bausiedler.json` (`aktiv: false`). **Achtung, bewusste Abweichung vom Original:**
   Holzfäller, Steinmetz und Jäger kosten laut `data/baupreise.json` je 1 Siedler (Screenshot
   1838857). `aktiv: true` stellt das Original wieder her.

## Der EINE nächste Schritt: Entscheidung 1 — der Sofortangriff reist

Daniels Entscheidung (31.10.2026): „Sofortangriff **reist** wie der Auftrag; der Knopf
‚Angreifen' entfällt.“ Heute gibt es **zwei** Wege:

* `NebelseetalApp._angriff_durchfuehren` (~Z. 6215) — **ohne** Reisezeit, direkt am Ziel.
  Wird aufgerufen von `_attack(bot)` (~Z. 6472) und `_attack_map(map_id)` (~Z. 6274).
* `NebelseetalApp._auftrag_angriff(bot)` (~Z. 6502) — **mit** Reisezeit, Rückkehr und Bericht
  über `state.auftrag_starten("angreifen", …)`.

**Ziel:** nur noch der Auftragsweg. Andockstellen: `_attack`, `_attack_map` (beide auf den
Auftragsweg umstellen), ein neuer Auftragsweg für **Kartenangriffe** (`_attack_map` hat heute
kein Gegenstück in `_auftrag_*`), und `_angriff_durchfuehren` stilllegen.

**Wichtig vor dem Bauen:** drei Prüfdateien hängen heute am Sofortpfad und müssen mitwandern —
`tests/test_kampf_einhaengung.py` (prüft `_angriff_durchfuehren` als EINEN Kampfweg),
`tests/test_gpt_kampf_botbeute_echte_kasse.py` und
`tests/test_produktionskette_ohne_cheats.py`. Neue Wachen nötig: Angriff kostet Reisezeit,
Truppen sind während des Marsches nicht doppelt verfügbar, kein Pfad ohne Marsch mehr.

## Was außerdem offen ist

* **Vier unklare Gebäudemotive** (Nummern 2, 3, 4, 6 aus `D:	mp\motivbogen.png`): Daniel ordnet
  zu, dann nur `data/gebaeude_motive.json` ändern (`eingebaut: true`, `gebaeude: <id>`).
* **A-5 bauen** erst nach Abnahme des Papiers.
* Weltkarten-Konzept: Abgleich liegt in `docs/KONZEPT_ABGLEICH_20261101.md`; Reihenfolge
  vorgeschlagen (Spionage → Start-/Ziel-Schnappschuss → Portalversetzung → Frühwarnung),
  **nichts freigegeben**.

> **KORREKTUR / neuester Stand (FIX05, Stand 30.10.2026):** Die oeffentliche FIX04j-Test-EXE wurde laut bestaetigtem Nutzertest gestartet, gespeichert und geladen; aeltere Aussagen "noch keine gebaute EXE" unterhalb sind historisch ueberholt. **FIX05 ist am 30.10.2026 kontrolliert in dieses Projekt uebernommen** (11 von 12 Delta-Dateien, jede gegen ihren Manifest-Hash geprueft; `tools/originalkarten_grafiken_bauen.py` bewusst NICHT uebernommen, weil die Delta-Fassung nur ein doppeltes Backslash im Moduldocstring einfuehrt). Neu: Tempo-Einstellung liegt im privaten Laufzeitordner (`~/.nebelseetal/spielzeit_einstellung.json`) statt im PyInstaller-Buendel; Fehlerdialog bei Schreibfehlern; sechs neue Tempo-Regressionen. Neue 10x10-Originalkartenpruefung und alle offenen 25 Sichtpruefungen im `docs/quellen/CODE_UND_KARTENPRUEFUNG_FIX05.md` dokumentiert. **Windows-Neubau der EXE, vollstaendige Regression und Nutzerabnahme (Start/Speichern/Neustart/Laden) stehen noch aus** — die Uebernahme ist Code, nicht Freigabe.

> **WICHTIGER NEUERER STAND (FIX04j, 28.10.2026):** Oeffentliche Test-EXE wird getrennt vom Admin-Entwicklerbuild vorbereitet. Das Repository enthaelt **saemtliche** Admin-Module und Dokumente; nur der oeffentliche EXE-Einstieg bietet keine Admin-UI. Es liegt hier **noch kein gebauter und unter Windows abgenommener FIX04j-Release** vor. Details: `docs/RELEASE_PUBLIC_FIX04j.md`, neuester Protokollabschnitt. Aeltere Statusangaben weiter unten sind historisch und nicht automatisch gueltig.

> **Neuester isolierter GUI-Stand FIX04i (28.10.2026):** Im Adminbereich sind Ressourcen und Aktionen auf getrennten Zeilen; das Schildmotiv der vorhandenen Ladebild-PNG wird in Spieler- und Admin-Speicherfenstern als Hintergrund angezeigt, mit lesbarem Bedienfeld. Fachlogik von FIX04h bleibt erhalten. Neue und benachbarte Tests erfolgreich; **Windows- und EXE-Abnahme ausstehend.**

> **Neuester isolierter Entwicklungsstand FIX04h (28.10.2026):** Spielstandverwaltung aufgeraeumt: normale Spieler sehen nur aktive Slots und keine archivierten Fassungen; explizite Wiederherstellung nur im autorisierten Admin-Entwicklerarchiv mit klarer Slotzuordnung. Archivgroesse wird lesend angezeigt, keine automatische Loeschung. Kuenftige Beibehaltung/Begrenzung/Abschaltung des Entwicklungsarchivs **offen**. FIX04g unter Windows vom Nutzer bis Save→Archiv→Restore→Load bestaetigt; FIX04h erst unter Linux/Xvfb getestet, Windows-Neubau noch ausstehend.

> **Neuester isolierter Entwicklungsstand FIX04g (28.10.2026):** Pflicht-Starthilfe bis echte Grundproduktion, Admin-Hilfeausnahmen, private datierte Spielstandarchive, Spieler-/Admin-Slotverwaltung, manuelles Wiederherstellen. Details: `docs/ENTWICKLUNGSPROTOKOLL.md` / `docs/HERMES_UEBERGABE_AKTUELL.md`. **Nicht** als Windows-Release getestet; lokaler Windows-/GitHub-Stand kann abweichen.

# Nebelseetal Remake – EINZIGER aktueller Entwicklungsstand

**Stand:** 28.10.2026 | **Arbeitskopie:** konsolidierter GPT-Entwicklungsstand nach FIX01 und Originalkarten-Umstellung. **Nicht:** Hermes-HEAD / freigegebene Windows-Version.

## Projektstruktur

- `src/`: ein aktiver Spielcode; Einstieg `src/main.py`, Originalgrafik-Zuordnung `src/originalkarten_grafik.py`, Karten-Daten `src/originalkarten.py`.
- `assets/`: aktuell benötigte Spielgrafiken; `assets/karten/original/` die 127 unveränderten Quellbilder, `assets/karten/spielfeld/` die 127 daraus für den Spielbetrieb hergeleiteten 640×640-PNGs (nearest neighbor, keine erfundenen Landschaftssymbole).
- `data/`: Regeln und aktueller Originalkarten-Katalog (`originalkarten/katalog.json`, Grafikmanifest).
- `tests/`: aktive Tests; ältere 8×7-Tests liegen separat im Archiv und gelten **nicht** als bestanden.
- `tools/`: Bau-/Test-/Quellenwerkzeuge, z.B. `originalkarten_grafiken_bauen.py`, `build_exe.py`.
- `docs/`: ein aktuelles `ENTWICKLUNGSPROTOKOLL.md`, eine aktuelle Hermes-Übergabe, Quellen und aktueller Status.
- `archiv/`: alte Zwischenstände, Tests, Protokollfassungen, alte Übergaben, Bildstudien; **nicht veröffentlichen**.

## Aktueller Spielstand nach Systemen

| Teil | Implementiert / Bedeutung | Noch offen |
|---|---|---|
| Siedlungskarten | 127 historisch belegte Originalbilder, im Spiel als Bilder statt Zeichenvorschlag; 10×10-Daten/Index; freier Kartenvorrat | 25 automatisch klassifizierte Kartenraster visuell noch nicht abgenommen; Raster-Bild-Kongruenz manuell prüfen |
| Gelände | Originalbild zeigt Wald-Baumgruppen, Fels-/Berg- und Grasfelder, Gebäude/Wege/Koordinaten als separate Überlagerung | Unterschiede zwischen Pixelbild und automatisch erkanntem Feldtyp für die 25 ungeprüften Karten korrigieren |
| Frühere 8×7-Karten | Generator und Kartentypen im aktiven Spiel **abgeschaltet**; Quellen/Tests archiviert | Ältere Savegames nur als historische Dateien; keine automatische Migration / kein stilles Zurückkehren der alten Welt |
| Produktion / Wirtschaft | lokales Ortslager, Holz/Stein, Waren, Ausbildung, Forschung, Karren | Altprüfungen auf Originalkarten umstellen, echte Regressionen reparieren, keine kostenlosen Bot-Ressourcen |
| Bau-Menü | Bau-/Auswahlfunktionen; Screenshots `docs/nebelseetal_gamestar2.jpg` als Referenz | historische Bauoberfläche (Navigation, Kosten, Siedlerbedarf, Baufelder) noch nicht vollständig nachgebaut |
| Kampf / Mauern / Bots | Grundfunktionen, lokaler Wall/Kampf/Beute | KI-Ökonomie, Belagerung, gesamter End-to-End-Durchlauf |
| Speichern / Laden | 3 Spielerslots und Adminbereich, Schutz vor nicht-originalen Kartenständen im Ladepfad | Reale Windows-Spielstände prüfen; kein verdecktes 8×7-Upgrade; nötigenfalls getrennte manuelle Import-Routine mit Freigabe entwerfen |
| Windows EXE | Python-Spiel plus `.bat`-Buildablauf | **Keine** aktuelle auf Windows neu kompilierte/verifizierte EXE in dieser Lieferung |
| GitHub | Öffentliche Seite `Decay03101991/Nebelseetal-Remake` | Hermes nach Rückübernahme zuständig für geprüfte Commits, Protokoll- und README-Pflege; keine Zugangsdaten/Archive veröffentlichen |

## Getestet und nicht getestet

- Vor der Originalgrafik-Umstellung: 35 ausgewählte Tests, 34 erfolgreich, 1 alter Kartenansichtstest mit 11 Fehlkontrollen. Nicht als komplette Suite zählen.
- Nach der Umstellung: neuer Originalkarten-Test besteht mit **7/7**; darin Nachweis aller 127 Bilddateien, Bilddatei-Prüfsummen, GUI-PhotoImage-Smoketest und Sperren gegen Legacy-Karten.
- Separate Nachbartests wurden selektiv geprüft; nicht alle älteren Testfälle gelten für die aktuelle Datenstruktur (siehe `archiv/tests_legacy_8x7/`).
- **GPT-FIX02 (28.10.2026):** `test_startspiel.py` nun **61/0/1** (Nahrung vs. Holz-Grundrate korrekt, 100 Originalkarten-Feldtags, Baukunst->Akademie->Ausbildung). `test_durchspiel.py` **64/0/2** (Bauen/Forschung/Ausbildung/Handel/Save/Load/Portal/Werkstatt inklusive Fertigstellung). `test_gpt_wall_gui.py` **4/4**, neuer `test_gpt_originalkarten_feldklick.py` **2/2**. 24 gezielt ausgewählte Testdateien nach Korrekturen gruen; `test_gui_fehler.py` anfangs blockiert, nach Ersetzung veralteter Dialog-/Wall-/Slot-Annahmen **23/0/1**. Dies ersetzt die alten historischen Befunde NUR fuer diese geprueften Dateien, nicht fuer die Gesamtsuite.
- Keine reale Windows-EXE, keine vollständige Windows- oder Gesamtspielabnahme. Release-Status: **NEIN**.

## Next actions für den temporären Coding-Agenten

> **GELTENDER STAND 03.11.2026, 21:20 (Hermes).** Diese Ueberschrift ist der Wiedereinstiegspunkt, den
> `tools/zieluebergabe.py` liest; die Liste darunter ist **HISTORIE der GPT-Runde vom 28.10.2026** und
> **nicht mehr** der Fahrplan. Geltend: Hermes fuehrt das Projekt seit 30.10.2026 zurueck, und der
> neueste Stand steht GANZ OBEN in dieser Datei (Block **S-8 Stufe 1**, Register 174: Ertrag aus den
> gebauten Anlagen; naechster Schritt S-8 Stufe 2, Feld-Prioritaeten).
> **Fertig und committet (31.10.):** F-04 (`52b5a51`), Spielbalancing-Test (`1cd799b`), Befund Siedler/Bots
> (`4e68de8`), **Nahrungsverbrauch je Einheit** (`8db75a6`, Register 69, 52 Pruefungen, Sammellauf 20:13 mit
> 103 Dateien/102 gruen/3.756 Pruefungen), **Balancing-Test Teil 2 - Karten, Doerfer und Pech** (`bca75e1`,
> Register 71, Werkzeug `tools/balancing_karten.py`, Gates G-8/G-9).
> **Fertig seit dem letzten Stand:** **Wagenbau-Kapazitaet** (Register 73) - `data/karrenkapazitaet.json`,
> Bonus +10 % je Stufe (Deckel Stufe 10 = Faktor 2,0), EINE Rechnung `einheiten.ladung_der_gruppe`,
> Stufen aus `GameState.forschungs_stufen()`, Pruefdatei 44/0/1, Sammellauf 20:58 (104 Dateien,
> 103 gruen, 3.801 Pruefungen), EXE `aa2c48c6...`.
> **Fertig seit dem letzten Stand:** **Nahrungsnot-Sperre** (Register 70/74, Commit `e20b4c6`) und die
> **Schenkungs-Botschaft** im Nachrichtenmenue samt Aufstockung von Slot 1 (Register 77, Commit `11746b5`).
> **Daniels Spielbericht vom 31.10.2026 liegt vor** und ist der neue Fahrplan:
> `docs/ANFORDERUNGEN_DANIEL_20261031_SPIELBERICHT.md` mit sechs Paketen **A-1 bis A-6** (Register 78).
> **Reihenfolge: A-1 Mengeneingabe fuer Einheiten -> A-3 Dorfuebersicht -> A-6 Siedler-Vorwarnung beim
> Bauen -> A-2 Original-Gebaeude-Icons -> A-4 Ressourcen-Icons -> A-5 Designkonzept Siedlung.**
> **Danach (bestehend):** Sofortangriff reist -> Kampfplanungsseite -> F-03 -> F-05/F-06 -> F-07/F-13 ->
> F-11 -> P3.4/P3.6 -> P4 -> Aufraeumen -> P5 -> P1 -> F-12. **Bots spaeter** (Register 72);
> **Kartenziehung = C** entschieden, nicht gebaut (Register 75). Offen fuer die Messung:
> `tools/balancing_messung.py` uebergibt keine Forschungsstufen, G-2/G-6 mit Wagenbau neu messen.
> **Ziel:** erste spielbare DEMO als Windows-EXE auf GitHub (Kriterien in Abschnitt 4 des Spielberichts).
> Nach JEDEM Schritt verpflichtend: Registereintrag in `docs/PRUEFREGEL_ORIGINAL.md`, Protokollzeile in
> `docs/ENTWICKLUNGSPROTOKOLL.md`, Einzeltest **und** voller Sammellauf
> (`python -X utf8 tools/sammellauf.py`), neue EXE mit Startpruefung, dann EIN Commit.
> **Offene Fragen (Auswahlformular):** 7-9 beantwortet (Register 70), **Frage 10** offen (Kartenziehung:
> freie Wahl / Zufall / Wahl aus drei gezogenen Karten).

**Historisch (28.10.2026, GPT-Runde - nur noch Nachweis, kein Auftrag):**

1. Original-Raster und sichtbares Originalbild für die 25 Karten manuell Feld für Feld abnehmen; automatische Klassifikation nicht ungeprüft korrigieren.
2. Historische Wirtschafts-/Baumenü-Tests mit 10×10-Originalkarten neu aufbauen (Archiv bewahren), fehlende UI-Funktionen implementieren.
3. Bot-Ökonomie, Handel, Produktion, Kampf, Save/Load als echte Spielrunde nachweisen.
4. Unter Windows aus `EXE_NEUESTEN_STAND_BAUEN.bat` kompilieren, startetest und Releaseprüfung.
5. Hermes nach Rückkehr gegen sein reales Git-HEAD vergleichen lassen; nur nach Tests offizielles Repo aktualisieren.

**Führende Detaildokumente:** `docs/HERMES_UEBERGABE_AKTUELL.md`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`, `docs/KARTEN_NUR_ORIGINALE.md`, `docs/ENTWICKLUNGSPROTOKOLL.md`.

**Zusaetzlicher Speichertest (28.10.2026):** `tests/test_originalkarten_savegames.py` ist mit 2/2 gruen: eine neue echte Originalkarte uebersteht Save/Load und eine alte 8x7-Karte wird vor Zustandsschaeden abgewiesen.


## Letzte Entwicklungsrunde – GPT-FIX02, 28.10.2026

Die einzige aktive Spiellogik-Aenderung ist in `src/main.py`: 100 unsichtbare Felderkennungen ueber dem unveraenderten Originalkartenbild. Dazu wurden die Durchspiel-/Wall-/Starttests auf reale Spielregeln und Originalkarten angepasst und eine neue GUI-Regression ergaenzt. **24 selektierte Testdateien bestehen, darunter der reparierte GUI-Aktionstest mit 18 Ansichten/13 Aktionen.** Kein neuer Windows-Build. Keine GitHub-Aktualisierung – die erfolgt auf ausdruecklichen Wunsch Daniels erst am Ende. Alle Einzelheiten und Befunde siehe `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt GPT-FIX02.


### Ergänzende Originalkarten-Bauprüfung – GPT-FIX02b

`tests/test_gpt_originalkarten_baukasse.py`: unter Tkinter/Xvfb **4/4 erfolgreich**: Ortslager-Zahlung ohne Doppelbuchung, belegte Felder bleiben unverändert, Rohstoffmangel ohne Seiteneffekte, echtes Originalkartenbild nach Bau. Damit sind **25 ausgewählte Testdateien** grün. Die 11 alten Kartenansicht-Fehlkontrollen sind noch **nicht** vollständig ersetzt (siehe einziges Entwicklungsprotokoll). Kein neuer Windows-Build oder GitHub-Push.


## Zusatzprüfung GPT-FIX02c (28.10.2026)

Der von Daniel wieder zusammengesetzte Stand ist bytegenau identisch mit dem FIX02-Paket (1.229 Projektdateien). Zusätzlich lokales `.git` aus altem Hermes-Head, aber **kein** aktueller Windows-EXE-Build. Historische Protokoll-/Zielübergabe-Pfade in isolierter Kopie korrigiert (belegt im einzigen Entwicklungsprotokoll). Zehn zentrale Spieltestdateien nach Entpackung bestanden; die vollständige Testsuite und ein Windows-Praxistest fehlen. Neue GitHub-Fassung darf erst nach Sichtung des GitHub-Clone-Diffs, Geheimnis-/Rechtekontrolle und echter Windows-Prüfung zum Release werden.

**FIX02c Buildgate-Nachtrag:** Vorprüfskript auf vorhandenen Originalkarten-Katalogtest korrigiert; 6/6 unter Linux/Xvfb erfolgreich. Keine Windows-EXE vorhanden oder freigegeben. Drei fehlende Tests im historischen GPT-Abschluss-Teststarter bleiben offen.


### FIX04 – aktueller isolierter Entwicklungsstand vom 28.10.2026

- Kartenbild: weiterhin ausschliesslich die authentischen 127 Siedlungskarten 10x10; Originalbilder nicht veraendert.
- Siedlungs-Baumenue: Bereiche Produktion/Werkstatt/Ausbildung/Verteidigung/Sonstiges im Auswahlfeld, je Bauangebot Zweck, Ertrag, Preis, Siedler- und Forschungsbedarf sowie konkrete Sperr-/Fehlmengen. Eine einzige Baukasse und ein einziger Bauaktionsweg bleiben erhalten; Dorfwall bleibt separate Siedlungsfunktion.
- GUI-Kontrolle: neuer FIX04-Test **5/5**, Spielstarttest **61/0/1** nach korrigierter Beschriftungserwartung; weitere ausgewählte Spieltests bestanden. Vollsuite und Windows-FIX04-EXE noch offen.
- Letzter praktischer Windows-Build: FIX03 unter Python 3.11.16 (Astral), von Daniel mit funktionierendem Start, Admin und Speichern/Laden bestaetigt. Jede Codeaenderung FIX04 erfordert danach einen *neuen* Windows-Build; noch kein GitHub-Push.
- Offene Risiken: GUI bei kleiner Bildschirmaufloesung; alte Weltregionen in `main.MAPS` (nicht mit 127 Original-Siedlungskarten verwechseln), Bot-Oekonomie/Belagerungen, 25 visuelle Kartenraster und alle Tests vor Release.


### 28.10.2026 – Vorlaeufige Entwicklung FIX04d (noch nicht Windows-veroeffentlicht)

FIX04 ergaenzt das Baumenue der 127 Originalkarten um Rubriken und regelbasierte Statusanzeige. FIX04b/c enthalten Standorttipps und eine begleitende Spielerhilfe mit zehn Fragen. FIX04d ergaenzt einen nur im Admin-Teststand zulaessigen Anzeige-Override (`auto`, `anzeigen`, `ausblenden`) ohne Eingriff in den Goetterschutz. 7/7 neue Admin-Tests erfolgreich; benachbarte GUI-, Start-, Save- und Durchspieltests erfolgreich. Vollsuite, Windows-FIX04d-EXE, Botwirtschaft und 25 visuell offene Kartenraster bleiben offen. Auf GitHub ist dieser Stand noch **nicht** veroeffentlicht; bisherige FIX03-EXE ist nicht FIX04d.
