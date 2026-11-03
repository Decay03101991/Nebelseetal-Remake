# Vorgaben Daniel 03.11.2026 — Welten, Bot-Hauptdorf, Raubzuege (verbindlich, noch NICHT gebaut)

Diese Datei haelt die Vorgaben woertlich-nah fest, die Daniel am 03.11.2026 im Chat gemacht hat.
Sie stehen ab jetzt ueber dem Fahrplan: was hier steht, wird gebaut; was hier nicht steht, wird nicht
erfunden. **Stand 15:57: W-1, W-4 und der Nachtrag W-5 bis W-9 sind GEBAUT** (Register 163 bis 169) -
ein Dorf entsteht in seiner Herkunftswelt, die Karte zeigt nur die Doerfer ihrer Welt, fuenf Bots
tragen je eine Fraktion, der Spieler startet in der Welt seines Volkes, und ein starker Bot raubt
jetzt auch Doerfer ANDERER Bots in derselben Welt aus. **Offen:** W-2 (Umzug eines Nebendorfs), W-3
(Preis/Sperre ueber Weltgrenzen, braucht Daniels Wort) und W-10 (Umzug, haengt an W-2).

## 1. Die vier Vorgaben

| Nr | Vorgabe (Daniel, 03.11.2026) | Was das fuer den Code heisst |
|---|---|---|
| W-1 | **Das Hauptdorf eines Bots bleibt IMMER in seiner Ursprungs- und Herkunftswelt.** | `BotDorf.dimension` des Hauptdorfs ist ab der Geburt fest und wird von KEINEM Weg geaendert (kein Transfer, kein Weltenwechsel, keine Ausnahme). Eine Wache haelt das: nach beliebig vielen Takten und Transfers ist `hauptdorf.dimension` noch die Startwelt. |
| W-2 | **Der Spieler darf mit seinem Hauptdorf die Welten wechseln — Bots nur mit ihren Nebendoerfern.** | Der Weltenwechsel (`_portal_wechsel`, heute `eigene_dimension` + 5.000 Mana) gilt fuer den Spieler unveraendert. Fuer Bots gilt: hoechstens die Doerfer mit `hauptdorf = False` duerfen die Welt wechseln; das Hauptdorf wird nie mitgenommen. |
| W-3 | **Ein Kampfauftrag von einer Welt auf eine Koordinate einer ANDEREN Welt ist so gut wie unbezahlbar — auch fuer den Spieler.** Das Springen und Koordinieren muss durch das SPIEL getriggert werden. | Der Weltenunterschied ist heute fast gratis: `auftraege.MANA_JE_DIMENSION = 20.0` Mana je Stufe (VORSCHLAG aus A2) - ein Angriff ueber eine Weltgrenze kostet damit ein paar Mana mehr als ein Angriff nebenan. Neu: ein eigener, deutlich prohibitiver Satz fuer Kampfauftraege ueber Weltgrenzen (Zahl in eine Datendatei, nicht in den Code), UND der Ausloeser ist das Spiel (Angebot/Sperre in der Oberflaeche), keine freie Koordinateneingabe. |
| W-4 | **GEBAUT (Register 169, `tests/test_bot_raubzug_bot.py` 39/0/0).** Bots, die stark genug sind (Einheiten, neue Doerfer gegruendet), beginnen Raubzuege um Ressourcen — nicht nur gegen den Spieler, auch gegeneinander. Voraussetzung: Bot und seine Welt sind spielaktiv. | Der Bot-Angriffsweg (`botkern` + `bot_angriffsplanung.waehle_ziel`) waehlt heute Ziele nur unter den SPIELER-Siedlungen. Neu: Ziele sind alle AKTIVEN Doerfer fremder Bots in derselben Welt - nach denselben Regeln (Goetterschutz, Punkteband, Wall, Beuteformel). Eine Welt, in der der Bot nicht aktiv ist, ist kein Ziel. |

## 2. Was Daniel dazu als Vorschlag offen laesst

Er sagt ausdruecklich: „gerne offen fuer kluge umsetzungsvorschlaege“. Deshalb hier die Vorschlaege
als VORSCHLAG gekennzeichnet — gebaut wird erst nach seiner Antwort:

1. **W-3 als eigene Sperre statt als Preis:** ein Kampfauftrag ueber eine Weltgrenze ist nicht
   teuer, sondern **gesperrt** und nur ueber einen vom Spiel angebotenen Weg moeglich (Portal-Auftrag
   mit Weltensprung, an eine Siedlung mit genug Mana gebunden). Vorteil: der Spieler kann sich nicht
   in einen Laufweg hineinrechnen, den niemand bezahlen kann.
2. **W-3 als Preis mit Deckel:** Kampf ueber Weltgrenzen kostet `mana_je_welt_feld` zusaetzlich
   (VORSCHLAG: Faktor 50 gegen den heutigen Satz) und ist damit praktisch nur fuer ein reiches Reich
   moeglich. Nachteil: eine Zahl, die im Spieltest niemand versteht.
3. **W-1/W-2 als Eigenschaft am Dorf:** `BotDorf.herkunftswelt` (additiv, alte Spielstaende laden
   ohne Migration) statt einer Sonderregel im Transferweg; der Transfer prueft EINE Bedingung.
4. **W-4 stufenweise:** zuerst Ziele unter den Spieler-Siedlungen UND den Bot-Doerfern derselben Welt
   (ohne neue Zahlen), danach die Staerke-Schwelle als Zahl in `data/bot_krieg.json`.

## 3. Ist-Stand, gemessen (03.11.2026, vor dem Bau)

| Punkt | Ist-Stand | Beleg |
|---|---|---|
| Bot-Hauptdorf und Welt | Jedes Bot-Dorf traegt `dimension` (Vorgabe 1). Im echten Startstand stehen **alle** Bot-Doerfer auf **Welt 1**, waehrend die Heimat des Spielers **Welt 4 (Midgard)** ist | `starter.neu_erzeugen()`; `BotDorf.dimension` |
| Weltfilter der Anzeige | **FEHLT:** `_bot_doerfer_im_raster` prueft nur `x`/`y`, nicht `dimension` — fremde Doerfer erscheinen damit auf JEDER Weltkarte | `src/main.py`, `_bot_doerfer_im_raster` |
| Dorfpositionen | Werden erst beim ersten Bot-Takt gesetzt (`bot_doerfer_auffrischen`); vorher stehen alle auf `x = y = 0` und damit auf einem Feld | eigener Lauf, `starter.neu_erzeugen()` |
| Anzeige der fremden Doerfer | Brauner Kasten mit hellem Rahmen und einem X, **ohne Name und ohne Nummer**; die sechs gelieferten Burgen (`assets/icons/burgen/burg_01..06.png`, freigestellt) sind **nicht** auf der Karte. Sie stehen nur im Ikonenkatalog | Screenshot `docs/audits/portal_karte_zoom_20261103_b.png`; `grep burgen src/` = 0 Treffer |
| Karte | 400 x 400 px fuer 20 x 20 Felder = **20 px je Feld**, Marke rund 5 px | Messung im Fenster: Canvas 400 x 400 |
| Truppenbewegung | Goldene Linie Start -> Ziel, eigenes Zeichen an beiden Enden, dazu eine Textzeile unter der Karte mit GROBER Restzeit (bei eigenem Ziel exakt); keine Truppenart, keine Anzahl | `main._marsche_zeichnen`, `marsch_optik`, Screenshot `docs/audits/portal_iststand_20261103.png` |
| Weltenunterschied im Preis | `MANA_JE_DIMENSION = 20.0` Mana je Stufe — praktisch gratis | `src/auftraege.py` |
| Transport ueber Welten | ausdruecklich **verboten** (`ValueError`: ein Weltkartenwechsel braucht eigene Portalregeln) | `spieloekonomie.transport_start` |
| Bot-Ziele | nur Spieler-Siedlungen (`bot_angriffsplanung.waehle_ziel(self.settlements, ...)`) — kein Bot gegen Bot | `main.bots_fortschreiben` |

## 4. Reihenfolge, in der das gebaut wird (VORSCHLAG)

1. **W-1/W-2 zuerst, weil es Daten sind** (Herkunftswelt am Dorf, Transfer nur fuer Nebendoerfer) -
   klein, ohne neue Zahlen, mit Wache.
2. **Der fehlende Weltfilter der Anzeige** (Befund oben) als Sofortreparatur im selben Schnitt.
3. **W-4** (Bot gegen Bot) auf dem bestehenden Angriffsweg, mit der Staerke-Schwelle in einer
   Datendatei.
4. **W-3** zuletzt, weil es die Balance beruehrt und Daniels Entscheidung braucht (gesperrt oder
   Preis mit Deckel).

Bis zu Daniels Antwort gilt der heutige Stand; keine dieser Vorgaben wird stillschweigend
mitgebaut.

## 5. Nachtrag 03.11.2026, 14:00 bis 14:07 (Chat)

| Nr | Vorgabe (Daniel, woertlich) | Stand |
|---|---|---|
| W-5 | 'jeder bot hat eine Herkunftswelt bitte und startet auch in dieser ... die gleiche zahl auf der gesamt welt befindlicher nutzer (5 bots 1 spieler und für diese 6 Welten)' | **GEBAUT** (Register 164): fuenf Bots sind fest aktiv, jeder in der Welt seiner Fraktion |
| W-6 | 'der spieler startet in der Hauptwelt und sieht bereits die bots wenn er in die Übersicht einer anderen welt schaut' | **OFFEN**: der Nur-Lese-Blick in eine fremde Weltkarte fehlt noch |
| W-7 | 'Auch soll er sehen wenn der bot sein zweites dorf gegründet hat das in seiner welt bereits 2 dörfer von ihm stehen' | **OFFEN**: haengt an W-6 und an S-6 (Nachgruenden) |
| W-8 | 'Erkennbar sind bots oder der spieler weil bots durch ihre fraktion auch ein wappen haben und auf der weltkarte sollen hauptdorf und nebendörfer die selbe burg mit dem dazugehörigen wappen tragen' | **GEBAUT** (Register 165): je Fraktion eine Burg mit Wappen aus `data/bot_wappen.json`; Haupt- und Nebendoerfer desselben Bots tragen dasselbe Paar, der Spieler sein eigenes |
| W-9 | 'Wenn ich als spieler eine fraktion wähle sollte ich auch in dieser welt starten' und 'nicht zwangsweise midgard als startwelt' | **GEBAUT** (Register 164): `data/welt_fraktionen.json`, der Spieler startet in der Welt seines Volkes; kein Midgard-Zwang im Code |
| W-10 | Die Heimatwelt eines Bots bleibt fuer immer; nur Nebendoerfer duerfen umziehen (praezisiert W-1/W-2) | **teilweise**: `herkunftswelt` steht am Dorf und bleibt stehen (Register 163); der UMZUG eines Nebendorfs ist noch nicht gebaut |

## W-11 — Story und Lore: eigenes Konzept, Fraktionen zuerst (Daniel 03.11.2026, 15:30)

**Woertlich:**
> „Für die Loore bzw Geschichte zum Spiel gilt ab sofort: Nur noch benötigte informationen aus der
> Nebelseetal geschichte und die thematik Nebel See Tal zu nehmen aber die geschichte den jetzt
> vorhandenen Fraktionen und den attributen dieser Fraktionen bzw Völker anzupassen. Das ist aber nur
> Story und nebensächlich und wird bitte dementsprechend eingeordnet in den ablauf. Mittlerweile haben
> wir denke ich bereits unser ganz eigenes Spielkonzept und sollten es auch als solches Entwickeln.
> Mach mir zur story dann gerne vorschläge usw wenn es an der reihe ist.“

**Was daraus gilt:**

| Nr | Regel |
|---|---|
| S-1 | Aus der Nebelseetal-Geschichte und dem Thema „Nebelsee-Tal“ wird nur genommen, was NOETIG ist - keine Uebernahme des alten Rahmens um seiner selbst willen. |
| S-2 | Die Geschichte wird den SECHS vorhandenen Fraktionen (menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome) und ihren belegten Attributen angepasst - nicht umgekehrt. |
| S-3 | Story ist NEBENSACHLICH: sie kommt nach Mechanik, Welten, Bots und Wirtschaft, nicht davor und nicht dazwischen. |
| S-4 | Das Spiel ist unser EIGENES Konzept; es wird als solches entwickelt und beschrieben, nicht als Nachbau des Originals. Originaltreue gilt weiter fuer MECHANIK und ZAHLEN (Pruefregel), nicht fuer die Erzaehlung. |
| S-5 | Beim Erzaehlen sind Vorschlaege erwuenscht (Daniel 03.11.2026) - sie werden als VORSCHLAG vorgelegt, nicht stillschweigend gesetzt. |

**Einordnung im Ablauf:** Story steht am ENDE der Arbeitsliste, nach S-5 bis S-9 und W-3/W-4. Wenn
Daniel sie aufruft, kommen zuerst Vorschlaege (Fraktionen als Traeger der Handlung, Nebelsee-Tal als
Schauplatz, sechs Welten als Kapitel), dann erst Text.

## Nachtrag 03.11.2026, 16:08 — Daniels Antworten (eine Runde, vier Fragen)

| Nr | Frage | Antwort Daniel (woertlich-nah) | Folge |
|---|---|---|---|
| W-3 | Kampf ueber Weltgrenzen: gesperrt oder teuer mit Deckel? | **Teuer mit Deckel** — nicht gesperrt | Kampfauftraege ueber eine Weltgrenze bleiben moeglich und bekommen einen eigenen, prohibitiven Satz (VORSCHLAG im Dokument: Faktor 50 gegen `auftraege.MANA_JE_DIMENSION = 20.0`, Zahl in eine Datendatei, nicht in den Code). Der Ausloeser bleibt das Spiel (Angebot in der Oberflaeche), keine freie Koordinateneingabe. **Noch NICHT gebaut** — eigener Schnitt nach S-6/S-7/S-9 |
| W-4 | Raubzuege Bot gegen Bot haben derzeit kein Ziel (ein Bot je Welt). Aendern? | **Bleibt so** — Folge der Vorgabe „5 Bots, 6 Welten“ | Keine Aenderung der Weltzuordnung. Der Mechanismus bleibt gebaut und greift, sobald zwei Bots' Doerfer in derselben Welt stehen (vor der Voelkerwahl Haug/Brynhild, spaeter ueber W-2) |
| W-8 | Wappen-Zuordnung: soll eine bestimmte Burg zu einem bestimmten Volk? | **So lassen** (Reihenfolge der Fraktionen) | `data/bot_wappen.json` bleibt unveraendert |
| W-8 | Burg und Wappen auf der Karte sind 8 px: groessere Felder oder Name beim Darueberfahren? | **So lassen (8 px), Name erst beim Darueberfahren** | Kein Kartenumbau. Der Name beim Darueberfahren ist ein kleiner UI-Schritt und steht als naechster Optik-Punkt offen (nicht Teil von W-4) |
