# Entwicklungsprotokoll — Nebelseetal Remake (ab 02.11.2026)

**Wozu:** Daniel schreibt das Entstehen des Spiels mit. Kurz und mit Beleg: die wichtigsten Schritte und ihre Kennungen — kein Tagebuch.
**Regeln für dieses Protokoll:**
- Nach jedem groben Schritt eine Zeile — immer hinten anhängen.
- Genau eine Zeile je grobem Schritt (das hält es übersichtlich).
- Fehler und Irrwege gehören hinein.
- Sicherungen stehen nicht hier (die gehören nach `docs/SICHERUNGEN.md`).
- Kosten nur gemessen, nie geschätzt.
- Zielgröße: deutlich unter 320 Zeilen. Wird sie überschritten, wird verdichtet — vorher die unveränderte Fassung sichern und committen.

**Zwei Hefte (Vorgabe Daniel 02.11.2026).** Dieses Heft führt ab dem 02.11.2026 weiter. Die gesamte
Historie bis zum 01.11.2026 steht unverändert in `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md`;
ältere Fassungen liegen zusätzlich in `docs/` und in `archiv/dokumentation/protokoll_alte_fassungen/`.
Nichts ist gelöscht, nichts verdichtet, nichts umgeschrieben.

## Vorgeschichte
Die Zeit vor dem 02.11.2026 — Vorgeschichte, Tag 1 bis zum 31.10.2026 und die ausgelagerten
Detailzeilen (`docs/PROTOKOLL_DETAIL_2026-10.md`) — steht im Historienheft
`docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md`. Auch die Zeilen des 02.11.2026 VOR der Sektion
HERMES-KARTE-01 (10:21 Protokollverdichtung, 10:32 Projekt-venv) stehen dort noch, weil sie zur letzten
Sektion des alten Hefts gehoeren. Hier geht es mit der Sektion HERMES-KARTE-01 weiter.

## HERMES-KARTE-01 - 02.11.2026 - Auswahlrahmen der C2-Lieferung gezeichnet (Register 130)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 13:20 bis 13:35 | **Auswahlrahmen: geliefertes C2-Bild liegt jetzt auf dem gewaehlten Feld, gezeichneter Goldrahmen nur noch Rueckfall (Register 130)** | `main._zeichne_siedlungskarte` Durchgang 4 zeichnet ein BILDobjekt (`_lade_kachelrahmen(auswahl, zelle)`) statt `karten_optik_fein.auswahl_plan_fein`; der Plan bleibt Rueckfall, wenn das Bild fehlt. Deckkraft neu als Zahl in der Datendatei (`kachelrahmen.deckkraft_auswahl_prozent` 100, gelesen als `main.AUSWAHL_DECKRAFT`); `_lade_motivdaten` liefert dafuer vier statt drei Werte. Wache `tests/test_auswahlrahmen_c2.py` **17/0/0**, Gegenprobe mit abgeschaltetem Bildzweig **12 bestanden, 2 Fehler**; `tests/test_gebaeude_motive` **104/0/1**, `tests/test_startspiel` **62/0/1** (Erwartung von 6 gezeichneten Objekten auf genau EINEN Auswahlrahmen umgestellt, Begruendung im Test) |
| 13:36 bis 13:41 | **Voller Sammellauf nach dem Schritt** | `tools/sammellauf.py`: **123 von 125 gruen, 0 rot, 2 ausgesetzt, 4.800 Pruefungen, 298 s**; Log `docs/audits/sammellauf_20261102_1336.log` (Datei 1 nennt Startzeit und 125 Dateien) |
| 13:30 | **Sichtvergleich als Kontaktblatt** | `docs/audits/auswahlrahmen_vergleich_20261102.png` (1986 x 720): drei Fassungen DESSELBEN Renderers auf Feld 12 - ohne Auswahl, bisher gezeichneter Goldrahmen, neuer gelieferter Rahmen. Aufgenommen als Bildschirmfoto der echten Zeichenflaeche (Pillow `ImageGrab`, je Fassung ein eigenes Fenster); Werkzeug `tools/auswahlrahmen_vergleich.py`. Eigener Befund: der gelieferte Rahmen ist deutlich wuchtiger als der gezeichnete und deckt die Feldraender ab - deshalb ist die Deckkraft ein Regler in der Datendatei (offene Frage an Daniel, `docs/FRAGEN_AN_DANIEL_20261102_1345.md`) |
| 13:45 bis 13:50 | **Voller Sammellauf auf dem ENDSTAND** (nach Registerzeile 130, Protokollzeile und Stand-Block) | `tools/sammellauf.py`: **123 von 125 gruen, 0 rot, 2 ausgesetzt, 4.800 Pruefungen, 294 s**; Log `docs/audits/sammellauf_20261102_1345.log`. Der Lauf davor (13:36, 298 s) war auf dem Code-Stand VOR den Dokumentzeilen und brachte dasselbe Ergebnis - beide Laeufe stehen im Log-Ordner |
| 13:54 | **Gegenprobe mit dem START-Interpreter** (Lehre 02.11.2026: ein gruener Sammellauf sagt nichts ueber den Startweg) | `.venv/Scripts/python.exe` (Pillow 13.0.0) zeichnet die Karte ebenfalls mit GENAU EINEM Auswahlbild (64 px), `main.AUSWAHL_DECKRAFT` 100, `main.RAHMEN_DECKRAFT` 35 - gleicher Code, gleiches Ergebnis wie unter dem Hermes-Python |
| 14:59 | **Guthaben (von Daniel abgelesen): DeepSeek 6,93 USD, Gesamtverbrauch 43,06 USD** | Zweite Quelle gegengerechnet: Ablesung 09:07 war 8,25 / 41,74 USD - Differenz **-1,32 USD Kontostand** und **+1,32 USD Gesamtverbrauch** passen zueinander (keine Aufladung dazwischen). Tagesbudget starkes Modell 3 USD; heute kein starker Modellaufruf, alle Arbeit lokal |
| 15:05 | **Auftrag V-5 fuer das GPT-Chat-Abo als Paket abgelegt** (`docs/auftraege/AUFTRAG_GPTCHAT_20261102_VOLKSATTRIBUTE.md` + `.zip`) | Gegenstand: Umsetzungsentwurf fuer die 13 nicht verdrahteten Wirkungen (8 Volksattribute-Zeilen aus 4 Fraktionen plus 5 Taktikboni; `bottaktik.VOLKSATTRIBUTE`, `TAKTIKEN[bot][bonus]`, `verhaltensbonus_aktiv` ohne Aufrufer). Paket 0,13 MB (Grenze 8 MB), enthaelt bottaktik, botkern, einheiten, kampf, kampfbericht, gebaeude_wirkung, forschung_wirkung, auftraege, spieloekonomie, test_s7_botverhalten, Register und Abweichungen 2006/2009; `testzip` geprueft. Zwei Kopien hashgleich auf dem Desktop |
| 15:00 | **Fragenrunde beantwortet (Auswahlformular)** | Auswahlrahmen bleibt bei **100 Prozent** (Eintrag in `data/gebaeude_motive.json` und in `docs/FRAGEN_AN_DANIEL_20261102_1345.md` nachgetragen); naechster Arbeitsschritt Punkt 3 (Leisten-Luecken); **Punkt 5 freigegeben** (Volksattribute und Verhaltensboni verdrahten) und **Punkt 6 freigegeben** (500 Mana + 100 Gold, `weltkarten_seed` fest); die 9 aelteren gestagten Skill-Eintraege werden EINZELN geprueft und vorgelegt |

## HERMES-KARTE-02 - 02.11.2026 - Leisten-Luecken gedeckelt, Band waechst gleichmaessig (Register 131)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 15:15 | **Befund am Code gemessen, bevor gebaut wurde** | `leiste_zusammensetzen` mit der alten Regel: Lueckendehnung 1,00 bei 1440 und 1920 px, 1,17 bei 2240, **1,86 bei 2560, 2,81 bei 3000, 3,75 bei 3440** (Skala blieb auf `skala_max` 1,5). Bildmodell-Befund am gerenderten 3440er Streifen: langgezogene Reflexe und harte Naehte, genau wie von Daniel beschrieben |
| 15:35 | **Grenzen als Zahlen in die Datendatei, Verdrahtung geaendert (Register 131)** | `data/ressourcenleiste.json`: `luecke_max` 1,35, `skala_hart` 1,75, `rest_auffuellen` gleichmaessig (mit `_lueckendehnung` als Begruendung). `main.leiste_zusammensetzen`: Luecken gedeckelt, bei Bedarf gleichmaessige Vergroesserung des ganzen Bandes, Breiten vorab gerechnet und Rest symmetrisch verteilt |
| 15:50 | **Zwei alte Wachen mit Begruendung umgestellt, neue Wache gebaut** | `tests/test_ressourcenleiste.py` **41/0/1**: die Zusicherung Skala bleibt auf `skala_max` nagelte die Ursache fest und ist ersetzt durch Skala waechst bis `skala_hart`; pixelgleich bei 2560 und 3440 ist ersetzt durch seitengetreu (Abweichung < 2 Prozent, gegen die Originalkachel gemessen). Neu `tests/test_leisten_luecken.py` **22/0/0** mit Gegenprobe: mit `luecke_max` 99 misst dieselbe Pruefung 3,76 und wird rot |
| 15:55 | **Sichtvergleich** | `docs/audits/leisten_vergleich_20261102.png`: ALT und NEU bei 2560 und 3440 px, gerendert vom echten Renderer (`tools/leisten_vergleich.py`). Neu ist bei 2560 schaerfer und ohne Naht; bei 3440 stehen die Raender 367/367, beide Enden sind vollstaendig (Ausschnittpruefung der Ecken) |
| 15:22 | **Voller Sammellauf auf dem Endstand** (mit der neuen Wache und den zwei umgestellten Zusicherungen) | `tools/sammellauf.py`: **124 von 126 gruen, 0 rot, 2 ausgesetzt, 4.824 Pruefungen, 541 s**; Log `docs/audits/sammellauf_20261102_1513.log`. Die zwei ausgesetzten sind die bekannten dokumentiert zurueckgezogenen Dateien (`test_oekonomie_kern_unabhaengig`, `test_weltkarte`) |
| 15:45 | **Starker Modellaufruf V-5 (deepseek-v4-pro) - Entwurf liegt vor, Kosten noch nicht abgelesen** | Aufruf mit 247.535 Zeichen Kontext (9 Kernmodule, `gebaeude_wirkung.json`, Auftragstext), Streaming, Laufzeit **416 s**, Antwort **26.154 Zeichen**. Nutzung laut Antwort: **77.689 Prompt-** und **26.899 Antwort-Token** (davon 18.266 Denk-Token), 104.588 gesamt. Kosten NICHT geschaetzt - naechste Guthabenablesung Daniels ergibt den Wert. Inhalt: zentrale Funktion `bottaktik.modifikatoren(bot, jetzt)`, Prozentwerte in einer neuen `data/bot_boni.json`, multiplikative Ueberschneidung (1,05 x 1,05 = 1,1025), Verankerung an Erträgen, Reise, Beute, Handel, Kampf; Grom-Ausbau bleibt wirkungslos (keine Bot-Bauwirtschaft) |
| 16:05 | **Konzept K-1 zu Dorf-Taktiken und Volksboni als Datei abgelegt (Entwurf, nichts gebaut)** | `docs/KONZEPT_DORF_TAKTIKEN_20261102.md`: Daniels Vorschlag zu Ende gedacht - jedes Dorf gibt EINEN Punkt (1 Prozent), der entweder die Staerke des Volkes hebt (Deckel +5, also hoechstens +10 Prozent) oder die Schiwerte ausgleicht (bis 0 Prozent); Taktik-Pakete je Fraktion als Datentabelle; fuenf Invarianten als Wachen; fuenf offene Entscheidungen mit Empfehlung. Gemessener Befund dazu: die Bots haben heute KEINE Doerfer (BotPlayer.settlements leer, Kommentar main.py nennt die eigene Ortsstruktur als spaetere Stufe), deshalb Stufenplan A bis D in Abschnitt 5 |
| 16:25 | **Konzept K-1 erweitert: Voelkerwahl am Start, dritter Kanal fremde Boni** | Daniels Praezisierung (02.11.2026): der Spieler waehlt zu Spielbeginn sein Volk, das HAUPTDORF traegt nur dessen +5/-5 und gibt KEINEN Punkt, jedes weitere Dorf gibt einen; die Bots bekommen die uebrigen Voelker. Dazu ein dritter Kanal: ein Dorf kann sich bis 5 Prozent eines FREMDEN Volkes holen. Ins Konzept als Abschnitt 8 nachgetragen, samt Balance-Regel (ein Budget ueber drei Kanaele, hoechstens 10 Prozentpunkte Wirkung, fremde Boni stapeln nicht) und dem gemessenen Code-Befund (`botkern.BOT_FRAKTIONEN` fest, vier Fraktionen fuer fuenf Bots, Boni bisher nur fuer Bots) |

## HERMES-BOTDORF-01 - 02.11.2026 - Stufe B-1: Bots tragen Doerfer (Register 132)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 16:40 | **Befund vor dem Bau** | `BotPlayer` fuehrt nur `settlements` als NAMEN (Kartenaufbau: `n_sett = random.randint(1, 3)`), einen gemeinsamen Vorrat und EINEN Wall; `grep -n dorf src/botkern.py` findet nichts. Im Code steht ausdruecklich, dass die eigene Ortsstruktur je Bot-Siedlung spaeter kommt |
| 16:55 | **Traeger und Migration gebaut (Register 132)** | `main.BotDorf` + `BotPlayer.doerfer`; `bot_doerfer_sicherstellen` (Namen -> Doerfer, erstes = Hauptdorf, Wall/Zaehler uebernommen, idempotent); `bot_aus_stand` fuer das Laden (dict -> Objekt). Eingetragen im Kartenaufbau UND im Spielstand-Laden |
| 17:05 | **Wache gebaut und gruen** | `tests/test_bot_doerfer.py` **27/0/1**; zusaetzlich `test_s7_botverhalten` **45/0/0** und `test_gpt_bot_angriffsplanung` **16/16 OK** (unittest-Stil) unveraendert gruen |
| 17:05 | **Zwischenstand offen benannt** | Die Dorf-Vorraete sind NICHT fuehrend; die Wirtschaft je Dorf (B-3) und die Taktikwahl (B-2) folgen. Der Befund steht in der Wache selbst, damit niemand den halben Weg fuer den ganzen haelt |
| 17:22 | **Voller Sammellauf auf dem Endstand (B-1)** | `tools/sammellauf.py`: **125 von 127 gruen, 0 rot, 2 ausgesetzt, 4.850 Pruefungen, 284 s**; Log `docs/audits/sammellauf_20261102_1714.log`. Protokoll steht damit bei 326 Zeilen ueber der Zielgroesse 320 - Auslagerung (nicht Streichung) ist als Aufraeumschritt notiert |

## HERMES-BOTDORF-02 - 02.11.2026 - Stufe B-2: Dorf-Verhalten aus der Lage (Register 133)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 16:39 | **Regel gebaut (bottaktik)** | `dorf_position`, `TAKTIK_GEWICHTE` (acht Verhalten, vier Lagen), `dorf_taktik_bewerten`, `dorf_taktik_waehlen`, `dorf_taktik_setzen`; Sperrzeit 48 h als VORSCHLAG, alle Gewichte VORSCHLAG mit Begruendung im Code |
| 16:50 | **Bruecke in main.GameState** | `bot_doerfer_auffrischen` (Lage aus vorhandenen Werten, Wahl je Dorf, eingehaengt im Bot-Takt), `bot_doerfer_auffrischen_alle`, `bot_doerfer_uebersicht`, `bot_doerfer_spionagebericht` |
| 16:50 | **Eigener Fehler gefunden und korrigiert** | Die erste Fassung der offenen Uebersicht enthielt die WALLSTUFE. Daniels Vorgabe: Wallstufe ist ein Kampfdatum, sichtbar nur im Spionagebericht. Grenze verschoben, Wache prueft jetzt beide Seiten (offen: Name/Position/Fraktion/Volkswerte; Bericht: Wall, Taktik, Truppen, Vorraete) |
| 16:51 | **Wache** | `tests/test_dorf_taktiken.py` **33/0/0**; ASCII-Pruefung 0 Nicht-ASCII-Bytes nach dem Uebersetzen zweier Umlaute |
| 16:56 | **Voller Sammellauf auf dem Endstand (B-2)** | `tools/sammellauf.py`: **126 von 128 gruen, 0 rot, 2 ausgesetzt, 4.883 Pruefungen, 299 s**; Log `docs/audits/sammellauf_20261102_1651.log`. Die Uhrzeiten der Zeilen darueber sind aus Datei-Zeitstempeln (`stat`) nachgetragen - die zuerst geschriebenen waren geschaetzt (16:39 bottaktik, 16:50 main, 16:51 Wache) |

## HERMES-BOTDORF-03 - 02.11.2026 - Stufe B-3: Wirtschaft je Bot-Dorf (Register 134)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 17:34 | **Uebergabe gelesen, Stand bestaetigt** | Arbeitsbaum leer, Kopf `4741076`, 128 Pruefdateien, Register 133, Protokoll 334 Zeilen, kein Prozess im Projekt (nur das Gateway) |
| 17:37 | **Datendatei und Regel gebaut (B-3, erste Fassung)** | `data/bot_wirtschaft.json`; `bot_wirtschaft_einstellungen`, `bot_dorf_ertrag`, `bot_kasse`, `bot_kasse_setzen`, `bot_kasse_buchen`, `bot_doerfer_ernten`; `BotPlayer.vorraete` als Eigenschaft ohne eigenes Feld; Ernte im Bot-Takt vor dem Zug |
| 17:53 | **Zwei echte Fehler gefunden und behoben** | Der Beute-Pfad schrieb per `clear()/update()` in eine KOPIE der Eigenschaft - die Beute kam aus dem Nichts (Fund durch `test_gpt_kampf_botbeute_echte_kasse`) - und `test_durchspiel` setzte die Bot-Kasse per Index (still verloren); beide auf `bot_kasse_setzen` umgestellt, zwei Wachen per `ast` ergaenzt |
| 17:57 | **Eigener Messfehler: falscher Interpreter** | Erster voller Lauf mit dem `.venv`-Python war untauglich: `test_gpt_originalkarten_historische_info` faellt dort an fehlendem `lxml` aus (kein Spielfehler). Der Sammellauf gehoert auf `python` 3.14, so wie in den Sitzungen davor |
| 18:01 | **Guthaben (von Daniel abgelesen)** | DeepSeek **6,48 USD**, gesamt 43,51 USD (15:34: 6,83 / 43,16) - Verbrauch dieser Sitzung bisher **0,35 USD** |
| 18:03 | **Entscheidung Daniel: drei Anlagen je Grundrohstoff** | Statt einer Anlage (4/4/4/3 je Stunde und Dorf) jetzt drei (12/12/12/9); die Zahl steht in `data/bot_wirtschaft.json`, nicht im Code. Erster Versuch las die Anlagenliste als Schleife falsch (Ertrag 0) - die Wache meldete es sofort rot, behoben |
| 18:08 | **Wache** | `tests/test_bot_dorf_wirtschaft.py` **52/0/0**, ASCII geprueft (kein Byte ueber 127) |
| 18:08 | **Voller Sammellauf auf dem Endstand (B-3)** | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.933 Pruefungen, 276 s**, Log `docs/audits/sammellauf_20261102_1804.log` |
| 18:10 | **Neue Vorgabe Daniel notiert (noch nicht gebaut)** | Je Gruendung drei Karten zur Wahl; die Karte bestimmt den maximal getragenen Rohstoff und die schwaecher produzierbaren, Gold hat Vorrang, wirklich stark ist man nur mit den besten Karten; die Bots muessen diese Wahl nachbilden. Steht in `docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 11 |

## HERMES-PROTOKOLL-01 - 02.11.2026 - Protokoll geteilt: Geschichtsheft geschlossen, neues Heft begonnen (Register 135)
| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 18:13 | **Zweites Heft angelegt (Vorgabe Daniel 02.11.2026)** | Die Historie bis 01.11.2026 steht unverändert in `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md` (geschlossen), dieses Heft führt ab 02.11.2026 weiter. Die Wachen wurden mitgezogen: `test_gpt_projektordnung_20261028` erlaubt genau EIN aktives Heft plus das Geschichtsheft, `test_protokoll` und `tools/pruefe_protokoll.py` vergleichen die Vollständigkeit gegen beide Hefte zusammen, `tools/protokoll_sichern.py` sichert beide beiden Heften |
| 18:16 | **Voller Sammellauf nach der Teilung** | **127 von 129 gruen, 0 rot, 2 ausgesetzt, 4.940 Pruefungen, 261 s**, Log `docs/audits/sammellauf_20261102_1816.log`; Werkzeug `tools/pruefe_protokoll.py` 46 Kennungen, 0 unbekannt, nichts verloren |
| 18:20 | **Registerzeile 135 nachgetragen** | Teilung des Protokolls mit allen mitgezogenen Wachen und dem Lauf-Beleg; das aktive Heft steht bei 80 Zeilen, die Zielgroesse 320 ist damit wieder eingehalten |
