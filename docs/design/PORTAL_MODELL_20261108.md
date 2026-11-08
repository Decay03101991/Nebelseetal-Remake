# Modell: Portal - ein Dorf auf ein FREIES WELTFELD setzen (Spieltest 3, Note 4; F-21)

**Stand:** `ab54761`, 08.11.2026, 21:58. **Es ist KEIN Code geaendert** - dieses Dokument ist die
Vorarbeit, damit nicht geraten wird. Daniels Entscheidung F-21 lautet: erst ein Modell mit vier
Fragen, kein geratener `dorf_versetzen`.

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

## 6. Schnitte, wenn die vier Antworten da sind

- **S-1 Belegungskarte (Kern).** Eine Funktion im Kern, die je Welt die belegten Felder liefert
  (eigene Siedlungen aus `x/y`, Bot-Doerfer aus `dorf_position`) und "frei" beantwortet. Wache: zwei
  Doerfer auf einem Feld werden erkannt, ein freies Feld wird als frei gemeldet.
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
