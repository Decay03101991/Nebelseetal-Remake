# Modell: Portal - ein Dorf auf ein FREIES WELTFELD setzen (Spieltest 3, Note 4; F-21)

**Stand:** `ab54761`, 08.11.2026, 21:58. **Es ist KEIN Code geaendert** - dieses Dokument ist die
Vorarbeit, damit nicht geraten wird. Daniels Entscheidung F-21 lautet: erst ein Modell mit vier
Fragen, kein geratener `dorf_versetzen`.

**Nachtrag 08.11.2026, 22:35:** S-2 und S-1 sind gebaut und geprueft (Abschnitt 9). Der Satz
„kein Code geaendert“ beschreibt weiterhin den Stand 21:58 und bleibt als Beleg stehen - die
Schnitte S-3 bis S-6 sind noch offen.

## 1. Der Auftrag im Wortlaut

Daniel (Spieltest 3, Register 312): "ich kann nicht genau auswaehlen im portal welches Dorf genau wo
hinspringt ... die Auswahl wohin ich springen will sollte auch nicht per dropdown Feld sein sondern
indem ich ein freies Feld auf der entsprechenden Weltkarte auswaehle, gecheckt wird ob das Feld frei
ist und ich die Voraussetzungen habe und mich dann dort hin springen lassen."

Vier Dinge stehen darin, und alle vier fehlen heute:

1. **welches Dorf** springt - die Auswahl ist heute die Welt, nicht der Ort;
2. **wohin** - heute per Auswahlliste, nicht per Klick aufs Feld;
3. **ist das Feld frei** - es gibt im Code KEINE Flaeche, die belegte Felder kennt;
4. **Voraussetzungen** - 5.000 Mana und 24 Stunden Sperre gibt es schon, aber sie gelten fuer einen
   Weltwechsel ohne Feld.

## 2. Ist-Stand, am Code gemessen

| Gegenstand | Befund | Beleg |
|---|---|---|
| Weltensprung | `_portal_wechsel(nach_z)` prueft Mana, bucht 5.000 ab, setzt `state.eigene_dimension` und traegt die Welt in `eigene_dimensionen` ein. **Ein Dorf wird NICHT versetzt.** | `src/main.py:11842-11886` |
| Feldauswahl | `_portal_feld_waehlen(x, y)` merkt das Feld in `self.portal_auswahl` und schreibt ins Protokoll "der Dorftransfer folgt mit S-6". Gebucht wird nichts. | `src/main.py:12152-12168` |
| Klickreihenfolge | `_portal_klick` fragt in dieser Reihenfolge: Drache, fremdes Bot-Dorf, Marschlinie, sonst Feldwahl. Ein Klick aufs freie Feld landet also in der Feldwahl. | `src/main.py:12119-12138` |
| Versetzfunktion | **Es gibt kein `dorf_versetzen`.** Die Suche nach `def versetzen` und `dorf_versetzen` in `src/` ist leer. | Suche 21:57 |
| Kosten | 5.000 Mana, hoechstens einmal je 24 Stunden. Der Wert steht in `data/welten.json` (`belegte_regeln.koordinatenwechsel.kosten_mana`) und wird nur gelesen. **Seit S-5 (09.11.2026, Register 332) gilt die Wartezeit NICHT mehr** (F-28 = C); der Stundenwert bleibt als Quelle und Zeitzeugnis in `welten.json` stehen, `portalraum` liest ihn nicht mehr. | `src/portalraum.py:19-27`, `:268-300` |
| Mana-Herkunft | Abgebucht wird aus `state.resources["mana"]` - im Code die **Reichskasse** (so benannt in `src/main.py:6260`), nicht aus einer Siedlung. Die Quelle sagt aber "aus einer Siedlung". | `src/main.py:11867-11875` |
| Ort und Welt | Jede Siedlung traegt `dimension` (Vorgabe 1) und `x`/`y`. Der Sprung aendert NUR `state.eigene_dimension`; die Siedlung behaelt ihre Welt. | `src/main.py:2552-2604` (Settlement), `:11877` |
| Kennung | `Settlement.id` ist `besitzer:map_id:x:y` (`siedlung_kennung`). **Aendern sich x/y, aendert sich die Kennung** - und die Kennung ist der Schluessel in Vertraegen (`kaeufer`/`verkaeufer`), in `aktive_siedlung_id` und in den Ortsdicts des Handels. | `src/main.py:2639`, gesetzt in `:8069` |
| Unterwegs-Sperre | Der Sprung ist gesperrt, solange Auftraege laufen (`_unterwegs_anzahl() > 0`); Handelsvertraege laufen als Auftrag mit. | `src/main.py:11854-11859` |
| Sperr-Uhr | Geprueft wird mit `time.time()` (Rechnerzeit), nicht mit der Spieluhr. | `src/main.py:11869`, `:11874` |

## 3. Widersprueche und Luecken (jeder mit Beleg, keiner behoben)

**W-1 Die Kennung haengt an den Koordinaten.** Ein Umzug auf ein anderes Feld aendert `Settlement.id`.
Alles, was die Kennung gespeichert hat (laufende Vertraege, `aktive_siedlung_id`, die Ortsdicts eines
Handelsabschlusses), zeigt danach ins Leere. Die Unterwegs-Sperre deckt das nur teilweise: sie sperrt
laufende Auftraege, aber nicht gespeicherte Kennungen in Anzeige und Spielstand. **Das ist die
technisch teuerste Stelle des Schnitts.**

**W-2 Es gibt keine Flaeche, die belegte Felder kennt.** Keine Funktion liefert "Feld X/Y auf Welt Z
ist frei". Bot-Doerfer haben feste Positionen (`bottaktik.dorf_position`, gelesen in
`_bot_doerfer_im_raster`), eigene Siedlungen tragen `x`/`y` - eine gemeinsame Belegungskarte gibt es
nicht. Die Frage "ist das Feld frei?" ist damit heute nicht beantwortbar, und ein "frei" ohne Pruefung
waere geraten.

**W-3 Zwei Koordinatenraeume.** `Settlement.x/y` gehoert zur ALTEN Siedlungskarte (`MAPS`-Groessen,
`src/main.py:3498-3504`: kontinent 20, wald 8, berge 8, suempfe 7, portalreich 10), das Portal
zeichnet ein 20 x 20-Raster.
Dass beide dasselbe Feld meinen, ist im Code NICHT belegt - so steht es schon in
`docs/design/MARSCH_ENTWURF_20261102.md` Abschnitt F. Gemessen ist dort sogar ein Widerspruch: die
Entfernung eines Auftrags rechnet `abs(ort.x - dorf.x) + abs(ort.y - dorf.y)` und mischt damit beide
Raeume. **Solange das offen ist, kann "Feld 7/12 auf Welt 3" nicht eindeutig auf eine Siedlung
zeigen.**

**W-4 Der Sprung versetzt kein Dorf.** `state.eigene_dimension` wechselt, `Settlement.dimension`
bleibt. Beim NAECHSTEN Laden zieht die Reparatur (`:8076-8082`) einen Ort nur dann in die aktive Welt,
wenn seine Welt unmoeglich ist - sonst bleibt er in der alten. Das heisst: heute springt die ANSICHT,
nicht das Dorf.

**W-5 Die Kosten kommen aus der Reichskasse, nicht aus einer Siedlung.** Der Quellentext
("Verschiebungsritual ... aus einer Siedlung") und der Code (`state.resources["mana"]`, im Code
Reichskasse genannt) sagen Verschiedenes. Fuer den Umzug ist das die Frage, WESSEN Mana bezahlt wird.

**W-6 Die Sperre laeuft auf der Rechnerzeit.** `time.time()` statt `state.spielsekunden`; das ist
genau der Punkt E3 (Entscheidung 308), vier Stellen im Portal und eine beim Laden.

## 4. Was NICHT belegt ist (wird nicht erfunden)

- Ob im Original ein Dorf MIT seinen Bauten umzieht, oder ob es am Ziel neu aufgebaut wird. Die
  Portal-Anleitung nennt "Koordinatenwechsel/Verschiebungsritual" und den Preis, nicht den Umfang.
- Ob ein Ziel auf einem Bot-Feld zulaessig ist (die Quelle schweigt).
- Ob Truppen, Garnison und Waren mitreisen oder zurueckbleiben.
- Ob die Sperre je DORF oder je SPIELER gilt (heute ist es eine globale Uhr, `state.letzter_wechsel`).

## 5. Die vier Fragen an Daniel (jede einzeln, mit drei Vorschlaegen)

**F-25: Was kostet der Umzug ausser den 5.000 Mana?**
- A (Empfehlung): nur die 5.000 Mana und die 24-Stunden-Sperre - kein Gold, keine Waren. Begruendung:
  der Betrag steht belegt in `data/welten.json`, alles Weitere waere erfunden.
- B: zusaetzlich Gold nach Entfernung innerhalb der Welt (Vorschlagsformel `welt.portalkosten`, NICHT
  belegt - sie ist im Code ausdruecklich als Vorschlag gekennzeichnet).
- C: zusaetzlich ein Anteil der Bauten (ein Umzug "kostet" 10 Prozent des Bauwerts, keine Quelle).

**F-26: Darf das Ziel auf einem Feld mit einem Bot-Dorf liegen?**
- A (Empfehlung): nein - ein belegtes Feld wird abgelehnt, mit klarer Meldung. Ein Bot-Dorf ist ein
  fremder Ort; zwei Orte auf einem Feld sind eine zweite Wahrheit.
- B: ja, aber nur mit Hinweis und ohne Kampf (Nachbarschaft).
- C: ja, und der Umzug auf ein Bot-Feld loest einen Angriff aus.

**F-27: Was reist mit - Bauten, Garnison, Karawanen?**
- A (Empfehlung): ALLES reist mit, das Dorf bleibt dasselbe (Bauten, Stufen, Garnison, Waren,
  Karawanen) - es aendert nur seine Koordinaten. Das haelt "ein Dorf ist ein Ort" ein und ist die
  kleinste Aenderung am Spielstand.
- B: nur Bevoelkerung und Waren; Bauten muessen am Ziel neu gebaut werden (harter Umzug).
- C: Garnison und unterwegs befindliche Einheiten bleiben zurueck (waere eine zweite Armee - und
  widerspricht der bestehenden Unterwegs-Sperre).

**F-28: Wie lange und wofuer gilt die Sperre danach?**
- A (Empfehlung): 24 Stunden fuer den NAECHSTEN Umzug desselben Dorfes, gemessen in SPIELZEIT (das
  behebt gleich W-6); die Sperre gilt je Dorf, nicht fuer den ganzen Spieler.
- B: 24 Stunden fuer den ganzen Spieler (wie heute global), aber in Spielzeit.
- C: keine Sperre mehr, nur die Mana-Kosten.

## 6. Antworten (Daniel, 08.11.2026, 22:05 bis 22:10, einzeln im Chat)

| Nummer | Frage | Antwort | Folge fuer den Bau |
|---|---|---|---|
| F-25 | Kosten ausser den 5.000 Mana | **A - nur die 5.000 Mana (und die Sperre)** | keine zweite Preistafel; Gold, Waren und Bauanteil kommen nicht vor. Der Sperr-Teil ist durch F-28 = C ueberholt. |
| F-26 | Bot-Feld als Ziel | **A - nein, belegtes Feld wird abgelehnt** | die Belegungskarte (S-1) muss eigene Doerfer UND Bot-Doerfer kennen; die Meldung nennt den Grund |
| F-27 | Was reist mit | **A - alles** | Bauten, Stufen, Garnison, Waren, Karawanen bleiben am Ort; der Umzug aendert nur die Koordinaten |
| F-28 | Sperre danach | **C - keine Sperre mehr, nur die Mana-Kosten** | `portalraum.wechsel_erlaubt` verliert die 24-Stunden-Pruefung; die Kosten bleiben die Bremse |

**Abweichung von der Quelle, ausdruecklich notiert:** die 24-Stunden-Sperre steht BELEGT in
`src/portalraum.py` (Kopf, Z. 19-27: "hoechstens einmal je 24 Stunden"). Mit F-28 = C faellt sie weg -
das ist Daniels Entscheidung als Spielleiter, keine stille Aenderung. Folge: der Spieler kann mit
genug Mana mehrfach am Tag springen; die Reichskasse ist damit die einzige Bremse.

## 7. Damit bleibt EINE technische Frage offen (nicht an Daniel, sondern an den Code)

W-3 (zwei Koordinatenraeume) ist mit den vier Antworten NICHT entschieden. Vorschlag fuer den Bau,
weil er den Bestand nicht anfasst: **`Settlement` bekommt `welt_x`/`welt_y` (Portalraum, 20 x 20) als
EIGENE Felder**, `x`/`y` bleiben die Siedlungskarte. Der Umzug schreibt nur `welt_x`/`welt_y` und
`dimension`. Vorteil: die Kennung `besitzer:map_id:x:y` bleibt stabil (W-1 entschaerft), alte
Spielstaende laden unveraendert (fehlende Felder = 0/0, sichtbar als "noch nicht im Portal
verortet"), und `_ort_feld` bleibt die EINE Aufloesestelle. Nachteil: ein Dorf hat dann zwei
Positionen, und die Anzeige muss klar sagen, welche sie zeigt.

## 8. Schnitte, wenn die vier Antworten da sind

- **S-1 Belegungskarte (Kern).** Eine Funktion im Kern, die je Welt die belegten Felder liefert
  (eigene Siedlungen aus `welt_x`/`welt_y`, Bot-Doerfer aus `dorf_position`) und "frei" beantwortet.
  Wache: zwei Doerfer auf einem Feld werden erkannt, ein freies Feld wird als frei gemeldet.
- **S-2 Koordinatenraum klaeren (VOR dem Umbau).** Eine Entscheidung, welcher Raum gilt, und die
  Aufloesung an EINER Stelle (`_ort_feld`), damit W-3 nicht in den Umzug einwandert.
- **S-3 `dorf_versetzen` im Kern.** Eine Buchstelle: pruefen (Ziel frei, Mana, Sperre, nichts
  unterwegs), dann genau einmal abbuchen und die Koordinaten setzen; die Kennung wird NEU gebildet und
  alle Fundstellen ziehen nach (W-1).
- **S-4 Portal-Ansicht: Karte statt Auswahlliste.** Klick aufs Feld, freie Felder sichtbar, belegte
  gesperrt mit Grund; der Sprung-Knopf nennt Dorf, Zielfeld und Preis.
- **S-5 Sperre weg (F-28 = C).** `wechsel_erlaubt` prueft nur noch Weltkarte und Mana; der
  Zeitstempel `letzter_wechsel` bleibt als Aufzeichnung. Die Schnittbeschreibung "Sperre in
  Spielzeit und je Dorf" ist mit Daniels Antwort F-28 = C ueberholt.
- **S-6 Wachen und Sammellauf.** Neue Wache fuer Kern und Fenster, Gegenprobe auf dem Altstand, voller
  Sammellauf, Registerzeile.

**Reihenfolge:** F-25 bis F-28 beantworten, dann S-2 (Klaerung) und S-1 (Kern), dann S-3 bis S-6.
S-3 ohne S-2 waere geraten - genau das will F-21 verhindern.

## 9. Gebaut am 08.11.2026, 22:15 bis 22:35: S-2 (Klaerung) und S-1 (Kern)

### 9.1 S-2 - der Koordinatenraum ist entschieden

`Settlement` traegt zwei EIGENE Felder `welt_x`/`welt_y` fuer den PORTALRAUM (0..19 je Weltkarte).
`x`/`y` bleiben unveraendert die Siedlungskarte. Ein Ort hat damit zwei Positionen, und welche
gilt, sagt die eine Aufloesestelle `_ort_feld` (`src/main.py`): zuerst `welt_x`/`welt_y`, sonst
`x`/`y`.

**Abweichung vom Vorschlag in Abschnitt 7, ausdruecklich festgehalten:** dort stand „fehlende
Felder = 0/0“. Das ist falsch gedacht - `0/0` ist im 20 x 20-Raster ein GUELTIGES Feld, ein Dorf
dort waere von einem nicht verorteten Dorf nicht zu unterscheiden. Der Vorgabewert ist deshalb
`None` („noch nicht im Portal verortet“). Folgen:

- alte Spielstaende laden unveraendert (fehlende Felder werden `None`, keine Migration);
- `siedlung_kennung(besitzer, map_id, x, y)` bleibt unberuehrt - die Kennung haengt weiter an
  Besitzer, Karte und `x`/`y`, also entschaerft S-2 den Widerspruch W-1;
- eine Portalposition AUSSERHALB des Rasters wird nicht durch `x`/`y` ersetzt (kein Mischen der
  beiden Raeume, W-3);
- geschrieben wird das Feld erst vom Umzug (`dorf_versetzen`, Schnitt S-3). Bis dahin ist jedes
  Dorf „noch nicht im Portal verortet“, und die Anzeige verhaelt sich wie bisher.

### 9.2 S-1 - die Belegungskarte im Kern

`src/portalraum.py` fragt jetzt „ist dieses Feld frei?“ und liest dabei KEINEN Spielstand;
hereingereicht werden nur die belegten Felder:

| Funktion | Aufgabe |
|---|---|
| `feld_eintrag(art, name, welt, x, y)` | ein belegter Ort als Eintrag; wirft `ValueError`, wenn Welt oder Feld nicht im Raster liegen (kein stilles Fallenlassen) |
| `belegungs_karte(eintraege)` | `(Welt-Index, x, y) -> Liste der Eintraege`; zwei Orte auf einem Feld bleiben BEIDE erhalten |
| `feld_status(welt, x, y, eintraege, ausschluss=None)` | Antwort `frei` / `belegt` / `ausserhalb` mit deutschem Grund, `belegt_von` und Weltnamen |
| `feld_name(welt)` | Anzeigename einer Weltkarte nach Index (fuer die Meldung) |

Drei Zusagen, die darin stecken: gezaehlt wird je (Welt, x, y) - **zwei Welten mit demselben Feld
kollidieren nicht**; `ausschluss` ist der Name des Dorfes, das selbst springen will, damit es sich
nicht selbst blockiert (ein zweiter Ort auf dem Feld blockiert trotzdem); Bot-Doerfer belegen ihr
Feld ueber ihre feste Position aus `bottaktik.dorf_position`, ohne Zufall aus der Uhr.

**Noch NICHT gebaut:** `dorf_versetzen` (S-3), die Karte in der Portalansicht (S-4), die Sperre in
Spielzeit (S-5) und die Verdrahtung in `main.py` - die Belegungskarte wird heute von keiner
Anzeige und keiner Buchstelle benutzt. Sie ist der Kern, auf den S-3 und S-4 aufsetzen.

### 9.3 S-3 - die Buchstelle (`_dorf_versetzen`), gebaut 23:15

`NebelseetalApp._dorf_versetzen(name, x, y, welt_nummer=0)` in `src/main.py` ist die EINE
Buchstelle; `_portal_belegte_felder()` uebersetzt den Spielstand in Felder (eigene Siedlungen aus
`welt_x`/`welt_y`, Bot-Doerfer aus ihrer festen Position). Geprueft wird in dieser Ordnung, und
jede Ablehnung nennt ihren Grund im Postfach:

1. die Siedlung gibt es;
2. nichts ist unterwegs (Daniel 01.11.2026, Anhang 2);
3. die Weltkarte ist bekannt;
4. das Dorf steht noch nicht auf diesem Feld (sonst waere es eine Buchung fuer nichts);
5. das Feld ist frei - auch ein Bot-Dorf blockiert (F-26 = A);
6. die Reichskasse traegt die 5.000 Mana (F-25 = A: keine zweite Preistafel);
7. die Sperre (bis S-5 die belegten 24 Stunden, F-28 = C). **Seit S-5 entfallen** - siehe 9.5.

Gebucht wird genau einmal: Mana minus Festpreis, `welt_x`/`welt_y`, `dimension` des Dorfes und die
gezeigte Welt (`eigene_dimension`, `eigene_dimensionen`). Bauten, Stufen, Garnison, Waren und
Karawanen werden NICHT angefasst und reisen damit mit (F-27 = A).

**W-1 ist damit erledigt, nicht nur entschaerft.** Abschnitt 8 verlangte fuer S-3 noch, die Kennung
neu zu bilden und alle Fundstellen nachzuziehen. Das ist mit S-2 ueberholt: `Settlement.id` haengt
an `besitzer:map_id:x:y`, und der Umzug setzt nur `welt_x`/`welt_y` und `dimension`. Kennung,
`aktive_siedlung_id`, Vertragsschluessel und Ortsdicts bleiben deshalb gueltig; es wird nichts
nachgezogen. Der teuerste Punkt des Schnitts faellt weg.

**Offen und benannt:** (a) S-4 muss den Knopf der Ansicht auf `_dorf_versetzen` legen; solange
daneben `_portal_wechsel` steht, gibt es ZWEI Buchstellen mit je 5.000 Mana, und ein Klick darf
nicht beide ausloesen. (b) S-5 nimmt die 24-Stunden-Pruefung aus `wechsel_erlaubt` (F-28 = C) -
vorher wird gemessen, welche Wachen daran haengen (`test_portalraum`, `test_durchspiel`,
`test_e2e_wege`, `test_weltkarten_anzeige`, `spielschicht`).

### 9.4 S-4 - die Ansicht: Feld anklicken, Dorf waehlen, springen (gebaut 23:33)

Daniels Antwort **A** vom 08.11.2026: der Knopf „Weltensprung“ in der Weltkartenliste ist WEG - er
hat dieselben 5.000 Mana abgebucht, ohne ein Dorf zu versetzen. Der Umzug ist der EINZIGE Weg.

Die Ansicht hat jetzt unter der Karte einen Block **Dorf versetzen**:

| Teil | Was er tut |
|---|---|
| Dorf-Wahl | ein Knopf je eigener Siedlung (Name + Weltkarte), merkt `portal_dorf` - bucht nichts |
| Feldklick | merkt `portal_auswahl`; geprueft wird jetzt gegen die ANGESEHENE Weltkarte (`_portal_blick`), vorher gegen die eigene |
| Zeile | nennt Feld, Gelaende, Weltkarte und den STATUS mit Grund („ist frei“ / „ist belegt: X“ / „liegt ausserhalb“) |
| Knopf | „<Dorf> hierher versetzen (5.000 Mana)“; gesperrt mit Grund (kein Feld, Feld nicht frei, Mana zu knapp, Auftraege unterwegs) |

`_portal_dorf_springen` bucht NICHT selbst - es ruft `_dorf_versetzen` (S-3) und leert danach die
Feldauswahl (sonst haengt der Goldrand an einem inzwischen belegten Feld).

**Fund beim Bau, behoben:** die Karte zeichnete die EIGENEN Doerfer auf `Settlement.x`/`y` - also
auf der SIEDLUNGSKARTE. Ein versetztes Dorf waere an seinem alten Platz gezeichnet worden. Jetzt
geht es ueber `_ort_feld`, die eine Aufloesestelle (Portalposition `welt_x`/`welt_y`, Altstand
`x`/`y`).

**S-4b ist erledigt (09.11.2026, 03:35, Register 331):** `_portal_wechsel` ist ENTFERNT, und
die vier Wachen sind auf die Buchstelle `_dorf_versetzen` umgestellt, nicht geloescht
(`test_durchspiel`, `test_e2e_wege` Kette 12, `test_portal_uebersicht`, `test_weltkarten_anzeige`);
dazu `test_portal_ansicht_umzug` und `test_portal_fremdblick`, die vorher nur den fehlenden Aufruf
prueften. Keine Funktion aus `portalraum` faellt mit der Methode weg (`wechsel_erlaubt` und
`nach_wechsel` werden von `_dorf_versetzen` und `spielschicht` weiter gebraucht).
**Noch offen:** S-6 (Wachen, voller Lauf, EXE).

### 9.5 S-5 - keine Wartezeit mehr (gebaut 09.11.2026, 08:07, Register 332)

Daniels Antwort **F-28 = C** vom 08.11.2026 („keine Sperre mehr, nur die Mana-Kosten“): die belegte
24-Stunden-Regel faellt weg. Der Stundenwert `hoechstens_je_stunden` steht weiterhin in
`data/welten.json` - er ist Quelle und Zeitzeugnis - aber `portalraum` liest ihn nicht mehr
(`_STUNDEN_SPERRE` geloescht, damit es keine zweite Wahrheit gibt).

| Stelle | vorher | jetzt |
|---|---|---|
| `portalraum.wechsel_erlaubt` | `(von_z, nach_z, mana, letzter_wechsel, jetzt)`, prueft die Restzeit | `(von_z, nach_z, mana)`, prueft nur bekannte Weltkarte und Mana |
| `portalraum.beschreibung()` | „hoechstens einmal je 24 Stunden moeglich“ | „hat keine Wartezeit (Entscheidung F-28 = C)“ |
| `portalraum.nach_wechsel` | „neuer Sperr-Zeitstempel“ | „der Zeitstempel des Wechsels“ - Aufzeichnung, sperrt nicht |
| `main._sperre_text` (Restzeit) | „noch X h“ / „abgelaufen“ | heisst `_letzter_wechsel_text`: „noch nie gewechselt“ / „vor wenigen Minuten“ / „vor X h“ (auch ein Zeitstempel aus der Zukunft wird benannt) |
| Portalzeile der Ansicht | „Sperre: …“ | „zuletzt gewechselt: …“ |
| `spielschicht.portalwechsel` | reichte Zeitstempel und Uhr durch | ruft `wechsel_erlaubt` mit drei Werten; `jetzt` bleibt fuer `nach_wechsel` und die Meldung |

**Die Wachen sind umgedreht, nicht geloescht.** Sechs Dateien forderten die Sperre; jede prueft jetzt
das Gegenteil mit demselben Aufruf: `test_portalraum` (72/0/0: `inspect.signature` = genau drei Werte,
ein Altaufruf mit Zeitstempel muss `TypeError` werfen, `_STUNDEN_SPERRE` darf nicht mehr existieren,
die Beschreibung nennt „keine Wartezeit“), `test_dorf_versetzen` (38/0/0: der zweite Umzug gelingt
sofort, wieder GENAU ein Festpreis, die Position ist neu), `test_e2e_wege` (132/0/1, Kette 12:
derselbe Wechsel von gerade eben ist mit genug Mana erlaubt; der zweite Umzug im Spiel scheitert am
Mana, nicht an einer Wartezeit), `test_spielschicht` (145/0/1), `test_portal_uebersicht` (62/0/0),
`test_weltkarten_anzeige` (27/0/0).

**Der Zeitstempel bleibt im Spielstand** (`state.letzter_wechsel`, geschrieben von `nach_wechsel`),
weil die Ansicht damit sagen kann, wann zuletzt gereist wurde - er sperrt nichts.

## 10. Daniels Antworten zur Gestaltung (09.11.2026, 09:33, fuenf Fragen in EINER Runde)

S-5 und S-6 waren gebaut, dann standen fuenf Fragen aus der Uebergabe 07:35 offen. Sie wurden
zusammen gestellt (fuenf Blaetter einer Runde, je drei Vorschlaege, Empfehlung zuerst; freie Antwort
moeglich) und um **09:33** beantwortet (gemessen am Werkzeug-Protokoll, nicht geschaetzt). Wortlaut der
Antworten:

| Nummer | Frage | Antwort (Wortlaut) | Folge |
|---|---|---|---|
| F-29 | Stil: flach gemalt bleiben, oder isometrisch umbauen? | **„Beide Fassungen als Bild sehen, dann entscheiden“** | Ein Vergleichsblatt liegt vor: `archiv/design/20261109_vergleich_stil/vergleich_flach_vs_isometrisch_20261109.png` (2000 x 1160, flach 20 px, flach 48 px und der Kartenausschnitt der Stilprobe A nebeneinander). **D-4 wartet auf seine Wahl** - kein Einbau vorher. |
| F-30 | Kantenlaenge der Portalkarte | **„20 px je Feld belassen“** | Keine Aenderung: `_portal_zelle` rechnet heute 20 px je Feld, 400 x 400 px. D-4 malt mit `kante=20` (gemessen 0,462 s kalt, 0,00013 s warm). Kein Rollbalken. |
| F-31 | Tannen oder runde Laubbaeume | **„Tannen“** | Keine Aenderung: `weltkarte_malerei` malt Tannen (D-3, Register 330). Das Designpaket beschreibt runde Laubbaeume - dieser Punkt ist damit abgelehnt. |
| F-32 | `spielschicht.portalwechsel` ohne Aufrufer in `src/` | **„Behalten und ausdruecklich als Spielschicht-Funktion dokumentieren“** | Bleibt. Offen ist die ausdrueckliche Dokumentation (ein Satz im Docstring plus ein Absatz in der Modulkarte); sie geht mit der naechsten `src/`-Aenderung in EINEN Commit, damit kein Sammellauf fuer eine Textzeile allein laeuft. |
| F-33 | `letzter_wechsel` im Spielstand | **„Bleibt als reine Aufzeichnung im Spielstand“** | So ist S-5 gebaut (Register 332): `nach_wechsel` schreibt den Stempel, die Portalzeile zeigt „zuletzt gewechselt“, nichts sperrt. Keine Aenderung. |
| F-34 | Stil und Kante, nachdem er das Vergleichsblatt gesehen hat (09.11.2026, 09:44) | **„Nummer 2 Flach und 48 px je Feld gefällt mir am besten nur etwas heller bitte wie bei Nummer 3“** | **F-29 und F-30 sind damit beantwortet und F-30 ist ueberholt:** flach gemalt bleibt, die Kante ist **48 px je Feld** (960 x 960 px - die Ansicht braucht einen Rollbalken, das ist D-4), und der Ton wird heller wie die isometrische Probe A. Gebaut in `weltkarte_malerei`: `HELLIGKEIT = 1.20` und `SCHATTEN_ALPHA = 20` statt 42, EINE Stelle (`_einheitslicht`) fuer Kacheln und ganze Karten; gemessene mittlere Helligkeit 85 -> 102 von 255. |

**F-29 hat Daniel am 09.11.2026 um 09:44 mit F-34 beantwortet** (flach, 48 px, heller wie Probe A) -
siehe die Zeile darueber. Damit ist aus dieser Runde nichts mehr offen ausser der kleinen
Dokumentationsaufgabe zu F-32.
