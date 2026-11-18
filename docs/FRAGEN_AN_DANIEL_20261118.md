# Fragen an Daniel - 18.11.2026 (Sitzung 49, Abschluss)

**Warum diese Datei:** Arbeitsregel 7 (Fragen sammeln, dann EINE Runde) und Daniel 18.11.2026:
„Stell mir jetzt noch offene fragen und mit den antworten uebergeben wir dann an eine neue session“.
Jede Frage nennt Messlage, die Moeglichkeiten MIT Folge und eine Empfehlung zuerst. Die Antworten
werden hier eingetragen und gehen in die Uebergabe.

**Stand:** Kopf `825f3a5`, Register 660, Arbeitsbaum leer, voller Sammellauf 239 von 239 gruen
(12.436 Pruefungen, 1358 s). Die Belege der drei Bestandsberichte stehen in
`D:\Arbeiten\Hermes\Notizen\NEBEL_ARBEITSPLAN_STAND.md`, `NEBEL_OFFENE_ENTSCHEIDUNGEN.md` und
`NEBEL_TECHNISCHE_BAUSTELLEN.md`.

---

## 1. Womit faengt die naechste Sitzung an?

**Messlage:** von den 16 Arbeitsplan-Stuecken sind 3 gebaut (B3, B4, C4), 7 teilweise, 6 offen.
Vier Bloecke sind ohne weitere Entscheidung baubar.

| Weg | Was er bringt | Folge |
|---|---|---|
| **A (Empfehlung)** C1 zuerst: die entschiedenen **500 Mana + 100 Gold** einbauen | schliesst eine Entscheidung vom 01.11., die seit 17 Tagen nicht im Code steht (`data/welten.json` bucht 5.000) | Weltwechsel wird in einer Partie erreichbar; kostet keinen Cent |
| B Release V_0.0.4 zuerst (Tag, Release, Startseite) | macht den fertigen Stand oeffentlich | 30 Minuten, aber Design bleibt liegen |
| C A3 zuerst: Kampf gegen ein echtes BotDorf messen | alle Kampfzahlen werden beurteilbar (heute: feste Vorlage, Beute immer 16/10/12) | Messarbeit, kein Umbau |
| D B1/B2 zuerst: Bot-Kern loesen und Zielbild | groesste Baustelle, braucht vorher deine Profile/Schwierigkeit | ohne Zielbild nicht baubar |

**Antwort (Daniel, 18.11.2026):** C1 zuerst - die entschiedenen 500 Mana + 100 Gold einbauen (Wortlaut der gewaehlten Karte). Begruendung: die Entscheidung vom 01.11.2026 (Register 93) steht seit 17 Tagen nicht im Code, data/welten.json bucht weiter 5.000.

---

## 2. Bibliotheksgrenze: zwei behalten oder auf das Original stellen?

**Messlage:** `src/main.py:4113` fuehrt `BIBLIOTHEK_OBERGRENZE = 2` („hoechstens zwei je Spieler“,
Daniel 30.10.2026), die Meldung sagt „eine je Karte, eine dritte nicht“. Das Handbuch 2009 nennt
nur „eine Bibliothek je Siedlung“ und keine Gesamtgrenze.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** 2 bleibt, und die Abweichung kommt ins `ABWEICHUNGEN_2006_zu_2009.md` | deine Regel gilt weiter, die Pruefregel bleibt ehrlich (nichts wird still angeglichen) |
| B Original uebernehmen (eine je Siedlung, keine Gesamtgrenze) | mehr Bibliotheken je Partie, Forschungswege kuerzer |
| C 2 bleibt, nichts eintragen | Widerspruch zum Handbuch bleibt undokumentiert |

**Antwort (Daniel, 18.11.2026):** Zwei bleiben, und die Abweichung kommt ins ABWEICHUNGEN_2006_zu_2009.md (Wortlaut der gewaehlten Karte). Folge: BIBLIOTHEK_OBERGRENZE = 2 gilt weiter; die Abweichung wird als eigene Zeile mit Quelle, alt, neu und Grund dokumentiert - gehoert zum Pflegepunkt D2.

---

## 3. Klebender Kopf 60 px fuer die Siedlungskarte?

**Messlage:** im Plan zu V_0.0.5 steht „Kopf 60 px, klebend (A4) - offen, Entscheidung Daniel“.
F-52 hat am 12.11. generell „JA“ gesagt; offen ist, ob die Siedlungskarte ihn JETZT bekommt.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** ja, die Siedlungskarte bekommt ihn jetzt | ein Baustein von V_0.0.5 wird fertig; Kopf bleibt beim Rollen stehen |
| B erst, wenn Geruest A in allen Ansichten steht | eine Runde spaeter, dafuer einheitlich |
| C kein Klebe-Kopf | bleibt wie heute |

**Antwort (Daniel, 18.11.2026):** Ja, die Siedlungskarte bekommt ihn jetzt (Wortlaut der gewaehlten Karte). Folge: der 60-px-Kopf bleibt beim Rollen stehen, F-52 wird damit fuer die Siedlung umgesetzt; einer der fuenf V_0.0.5-Bausteine ist danach fertig.

---

## 4. Chronik: die sechs Wappenbeschreibungen nachziehen?

**Messlage:** `docs/CHRONIK_DER_WELT_20261104.md` Teil 5 beschreibt Motive, die auf den heutigen
Wappenbildern nicht zu sehen sind. Die neuen Wappen (F-90) sind noch nicht da.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** nachziehen, sobald die sechs neuen Wappen geliefert sind | Chronik und Bilder passen dann zusammen; bis dahin bleibt der Text als Zeitzeugnis |
| B jetzt schon auf die heutigen Bilder umschreiben | Text passt fuer ein paar Wochen, dann wieder nicht |
| C lassen | Widerspruch bleibt stehen |

**Antwort (Daniel, 18.11.2026):** Ja, nachziehen sobald die sechs neuen Wappen geliefert sind (Wortlaut der gewaehlten Karte). Bis dahin bleibt der Chronik-Text als Zeitzeugnis stehen; keine Umschreibung auf die heutigen Bilder.

---

## 5. Weltkarten-Konzept (Lords-Mobile-Abgleich): freigeben oder liegen lassen?

**Messlage:** der Abgleich liegt fertig in `docs/KONZEPT_ABGLEICH_20261101.md`; vier Schritte sind
vorgeschlagen (Spionage, Start-/Ziel-Schnappschuss, Portalversetzung, Fruehwarnung). **Nichts
freigegeben**, seit 01.11. keine Freigabe belegbar.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** liegen lassen bis nach dem Release | die naechsten Schritte bleiben ueberschaubar |
| B jetzt freigeben, in der vorgeschlagenen Reihenfolge | neue Baustelle neben C1/Release |
| C verwerfen | Konzept bleibt als Beleg liegen |

**Antwort (Daniel, 18.11.2026):** Jetzt freigeben, in der vorgeschlagenen Reihenfolge: Spionage -> Start-/Ziel-Schnappschuss -> Portalversetzung -> Fruehwarnung (Wortlaut der gewaehlten Karte). Folge: das Konzept ist damit FREIGEGEBEN (nicht mehr Vorschlag) - die vier Schritte werden als eigenes Arbeitspaket in der freigegebenen Reihenfolge gefahren, jeder Schritt mit Wache, Registerzeile und Sammellauf; sie werden NICHT zwischen C1 und den Release gemischt.

---

## 6. Die sechs neuen Wappen: welche Bildquelle?

**Messlage:** die sechs Pollinations-Versuche hast du am 13.11. abgelehnt („dafuer brauchen wir die
richtige KI“). Guthaben heute: **1,99 USD** (Gesamtkosten 78,00 USD). F-92 hat „kostenlose Proben
zuerst“ entschieden.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** erst Cl.audes Bildbriefing (Nr. 20) abwarten, dann mit diesem Briefing kostenlos bei Pollinations probieren | kein Geld, bessere Proben als beim ersten Versuch |
| B bezahltes Modell, nach Aufladen | bessere Qualitaet, kostet Guthaben |
| C du lieferst die Bilder selbst | kein Modellrisiko, dauert |

**Antwort (Daniel, 18.11.2026):** Bezahltes Bildmodell nach dem Aufladen (Wortlaut der gewaehlten Karte). Folge: die sechs Wappen sind bis zum Aufladen BLOCKIERT (Restguthaben 1,86 USD); der Auftrag/Briefing kommt weiter von Claude (Nr. 20), die Ausfuehrung erst nach dem Aufladen. Noch offen und nicht erfunden: WELCHES bezahlte Modell (Kandidaten und Preis je Bild stehen nicht in den Unterlagen - UNBEKANNT, wird beim Aufladen entschieden).

---

## 7. F-72/C7 (Regel 2 um gekennzeichnete Startwerte) und F-70 (Portalsprung): wann?

**Messlage:** F-72 ist freigegeben, aber nicht gebaut; du willst es „in einer eigenen Sitzung - nicht
zwischen zwei Bauauftraegen“. F-70 ist mit F-95 zurueckgestellt, der Bauauftrag Nr. 11 liegt fertig.

| Weg | Folge |
|---|---|
| **A (Empfehlung)** beide nach dem Release, je in eigener Sitzung | keine Vermischung mit Bauauftraegen |
| B F-72 jetzt, F-70 spaeter | eine Sitzung ohne Bauauftrag dazwischen |
| C beide verwerfen | die Akten bleiben als Beleg |

**Antwort (Daniel, 18.11.2026):** Beide nach dem Release, je in eigener Sitzung (Wortlaut der gewaehlten Karte). Folge: F-72/C7 und F-70 bekommen je einen eigenen Termin NACH dem Release V_0.0.4/V_0.0.5; das fertige Bau-Rezept fuer F-70 (Auftrag Nr. 11) bleibt liegen.

---

## Was KEINE Antwort braucht (wird in der naechsten Sitzung erledigt)

- Registerzeilen 594/595 nachtragen (Kette-Luecke 543-649 bleibt als Kopfzeile dokumentiert).
- `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` pflegen (seit 05.11. unveraendert) - gehoert zu D2.
- Demo aus dem heutigen Stand bauen und `--pruefen` fahren; CI-Workflow auf den erzeugten Dateinamen ziehen.
- Bildschirmfoto der Startseite: **das brauchst du** (Platzhalter in `index.html:149`).

---

## Nachtrag 18.11.2026, 18:40: ein Widerspruch, den C1 sichtbar gemacht hat

**Wortlaut der beiden Aussagen:** Register 93 (01.11.2026, 18:24) sagt „500 Mana plus Gold, 100 Gold“. F-25 = A (Fragenrunde 07.11.2026) sagt „nur die 5.000 Mana, kein Gold, keine Waren“ - F-25 ist also juenger, ging aber in der Frage noch von 5.000 Mana aus.

**Wie C1 es behandelt:** Daniels neuestes Wort vom 18.11.2026 (Antwort 1, „C1 zuerst - 500 Mana + 100 Gold einbauen“) gilt; der Goldanteil ist gebaut, der Docstring von `wechsel_erlaubt` nennt den Grund. Der Teil von F-25, der weiter eingehalten ist: es gibt **keine zweite Preistafel** - beide Preise kommen aus `data/welten.json`, Block `koordinatenwechsel.spielwert`.

**Was du pruefen muesstest, falls du es anders meinst:** sag ein Wort, dann wird der Goldanteil auf 0 gesetzt (eine Zeile in der Datendatei, der Manapreis bleibt 500) - die Wachen pruefen den Spielwert aus der Datendatei, nicht eine Zahl im Code. Beleg: Register 664.
