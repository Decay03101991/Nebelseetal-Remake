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
| Kosten | 5.000 Mana, hoechstens einmal je 24 Stunden. Der Wert steht in `data/welten.json` (`belegte_regeln.koordinatenwechsel.kosten_mana`) und wird nur gelesen. | `src/portalraum.py:19-27`, `:165-212` |
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
- **S-5 Sperre in Spielzeit** (deckt sich mit E3) und je Dorf statt global.
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
7. die Sperre (bis S-5 die belegten 24 Stunden, F-28 = C).

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
