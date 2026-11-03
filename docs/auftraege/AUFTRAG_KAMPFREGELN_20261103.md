NEBELSEETAL REMAKE - AUFTRAG KAMPFREGELN (Regelentwurf, keine Umsetzung)
Stand: 03.11.2026, 21:45. Auftraggeber: Daniel. Bearbeiter: starkes Modell (deepseek-v4-pro).

WAS ICH BRAUCHE
Nebelseetal ist ein Remake des gleichnamigen Browserspiels (Aufbau- und Kriegsspiel, Einzelspieler
gegen fuenf Bots, Spieluhr laeuft schneller als die Rechnerzeit). Das Kampfsystem ist gebaut und
laeuft; acht Einzelfragen sind im Code als `unsicher: true` markiert, weil das Originalhandbuch sie
nicht ausdruecklich regelt. Daniel will zu JEDEM der acht Punkte EINE Regel mit Begruendung
vorgeschlagen bekommen und segnet die Liste dann in einem Durchgang ab.

DU LIEFERST REGELN, KEINEN CODE. Keine Dateiaenderung, kein Patch, keine Umsetzungsanleitung mit
Code. Jede Zahl ist ein VORSCHLAG, keine belegte Originalregel, und muss als solche gekennzeichnet
sein. Wo das Handbuch etwas belegt, hat das Handbuch Vorrang vor jeder Analogie.

WAS IM ORIGINAL BELEGT IST (Handbuch 2009, Seiten 20-22; Auszuege woertlich)
- Vorrunde: Zuerst wird geprueft, ob der Angreifer den Wall ueberwinden kann. Dazu wird die
  Schlagkraft (SK) aller angreifenden Fusstruppen summiert. Sie muss den Schwellenwert des Walls
  erreichen. Ab der verstaerkten Palisade ist zusaetzlich Schlagkraft von Belagerungswaffen noetig.
  Reicht sie nicht, ziehen sich die Truppen zurueck - der Kampf gilt als unentschieden.
  Schwellen (Wallstufe 1-10), Fusstruppen / Belagerungswaffen:
  1 Erdwall 10 / -, 2 Steinwall 40 / -, 3 Kleine Palisade 90 / -, 4 Palisade 160 / -,
  5 Verstaerkte Palisade 250 / 500, 6 Mauer 360 / 600, 7 Verstaerkte Mauer 490 / 700,
  8 Festungsmauer 640 / 800, 9 Verstaerkte Festungsmauer 810 / 900, 10 Bollwerk 1000 / 1000.
- Mauerschaden: eine beschaedigte Mauer verlangt PROZENTUAL weniger Schlagkraft. Beispiel: Stufe 7
  mit 50 Prozent Zustand ist mit 245 Fusstruppen-SK + 350 Belagerungs-SK zu stuermen (je die Haelfte).
  Schadensermittlung: Schaden der Waffe (Zufallswert) minus Ausbaustufe der Mauer; bleibt ein
  positiver Rest, wird er vom Zustand abgezogen. Beispiel: Katapult (Schaden 2-13) gegen Mauer
  Stufe 6, gewuerfelt 8 -> 8 - 6 = 2 -> Zustand 100 -> 98 Prozent. Fuer JEDE mitgefuehrte
  Belagerungswaffe einzeln.
- Kampfsequenzen: Nach 10 Sequenzen ohne Sieger endet die Schlacht unentschieden, der Angreifer
  zieht sich OHNE Beute zurueck. Je Sequenz: Fernkampf beider Seiten gleichzeitig (Angreifer auf die
  Fusstruppen des Verteidigers, sind keine da auf dessen Fernkaempfer), dann werden die Verluste
  beider Seiten berechnet; danach Nahkampf, jede angreifende Einheit greift nacheinander eine
  ZUFAELLIGE verteidigende Nahkampfeinheit an. Ende: eine Armee hat keine Nahkampfeinheiten mehr
  oder 10 Sequenzen sind vorbei.
- Zweikampf: hoeherer Mutwert (MU) beginnt, bei Gleichstand der Verteidiger. Treffer mit Zufall 1-100
  kleiner/gleich AT, sonst verfehlt; Parieren mit PA; Schaden = Zufallswert im TP-Bereich minus RS,
  mindestens 1 Punkt, geht von der LE ab. LE unter 1 = tot; LE unter 5 = anhand des MU entscheidet
  sich, ob die Einheit weiterkaempft oder flieht; geflohene Einheiten stehen nach der Schlacht
  wieder zur Verfuegung, je niedriger der MU desto wahrscheinlicher die Flucht. Der Sieger eines
  Zweikampfs verliert 1 Punkt AT und PA bis zum Schluss (Erschoepfung, summiert sich).
- Ausgang: alle verteidigenden Einheiten tot oder geflohen -> Angreifer gewinnt und beginnt mit
  Transportkarren zu pluendern. Alle angreifenden Fusstruppen tot oder geflohen -> Verteidiger
  gewinnt. Der Verlierer verliert einen Teil seiner Karren und Belagerungswaffen; wie viele, haengt
  von der Dauer ab. Jede Einheit hat 40 Prozent Fluchtchance, die pro Kampfsequenz um 5 Prozent
  steigt. Bei Unentschieden bleiben alle Karren und Belagerungswaffen erhalten.
- Das Handbuch regelt NICHT: wie Beute auf die Rohstoffe verteilt wird, in welcher Reihenfolge
  Ressourcen genommen werden, ob Geraete (Karren, Belagerungswaffen) erbeutet werden koennen, wer
  die Mauer repariert und wann, und ob eine Vorrunde nach einer beschaedigten Mauer wiederholt wird.

WAS DER CODE HEUTE TUT (Ist-Stand, damit deine Regeln dazu passen)
- Es gibt EINE Schlachtfunktion (`kampf.fuehre_schlacht`); sie setzt Vorrunde, Sequenzen und
  Zweikampf nach den belegten Regeln oben um.
- Der Wall hat je Stufe einen ZUSTAND von 0 bis 100 Prozent (Start 100). Die Vorrunde rechnet die
  Schwellen mit dem Zustand anteilig - das ist der belegte Prozentsatz-Satz oben.
- Beute: eine Staffel, die Daniel vorgegeben hat - 100 Prozent, wenn kein Verteidiger mehr steht;
  60 Prozent, wenn der Wall schon bei 0 Prozent war; 30 Prozent, wenn der Wall beschaedigt war;
  10 Prozent beim ersten erfolgreichen Angriff auf einen heilen Wall. Zusaetzlich begrenzt durch die
  Gesamtladung der mitgefuehrten Transportkarren (Handkarren 40, Einspaenner 100, Zweispaenner 250,
  Grosser Karren 1000, Ochsenkarren 2500; Forschung Wagenbau erhoeht die Ladung). Verteilt wird
  anteilig nach vorhandener Vorratsmenge je Rohstoff. Kein Karren = keine Beute.
- Flucht: im Zweikampf gibt es die Regel LE unter 5 plus MU; eine eigene Ausloese-Bedingung fuer
  die GANZE Armee fehlt.
- Belagerungswaffen haben einen Schadensbereich (Katapult 2-13) und ziehen den Wert minus
  Wallstufe vom Zustand ab, je Waffe einzeln - so wie im Handbuch.

DIE ACHT PUNKTE (in dieser Reihenfolge abarbeiten)
1. fusstruppen_begriff - welche Einheiten zaehlen als Fusstruppen (fuer die Vorrunden-Schlagkraft
   und fuer das Kampfende)?
2. flucht_formel - wann flieht eine Armee als Ganzes (Ausgang flucht)?
3. beute_verteilung - wie wird die Beute auf Angreifer und Verteidiger verteilt?
4. beute_reihenfolge - in welcher Reihenfolge werden Ressourcen genommen, wenn die Ladung nicht fuer
   alles reicht?
5. belagerungsturm_mauerschaden - wie viel Schaden macht ein Belagerungsturm an der Mauer (Abgrenzung
   zum belegten Waffenschaden)?
6. mauer_reparatur - wer repariert die Mauer, wann, womit, zu welchem Preis?
7. vorrunde_wiederholung - wird die Vorrunde in einer spaeteren Sequenz oder bei einem spaeteren
   Angriff wiederholt, und mit welchem Wallzustand?
8. geraetebeute - koennen Karren und Belagerungswaffen erbeutet oder zerstoert werden?

WENN DU ETWAS ENTWERFEN ODER ERFINDEN MUSST (Vorgabe Daniel 03.11.2026)
- Fehlt im Projekt eine belegte Quelle, dann erkundige dich GEZIELT nach bekannten, aehnlichen
  Systemen (vergleichbare Aufbau- und Browserspiele, Open-Source-Projekte, gaengige Kampfsimulationen):
  zwei bis drei Quellen mit Namen.
- Sag zu jeder Quelle, WARUM gerade sie taugt und was du daraus uebernimmst: "System X macht das so,
  weil ...; uebertragen auf Nebelseetal heisst das ...".
- Gezielt, nicht breit: keine Linklisten, keine Marktuebersicht.
- Deine Uebertragung ist ein VORSCHLAG, keine belegte Originalregel. Die Rangfolge bleibt:
  Handbuch 2009 vor Seiten 2006 vor Analogie.
- Ohne Netzzugang: offen sagen, dass du dich nicht erkundigen konntest - keine Quelle erfinden.

FORMAT DER ANTWORT (genau so, deutsch, Markdown, keine Emojis)
Fuer JEDEN der acht Punkte ein Block:

### <Nummer>. <punktname> - <Kurzfassung der Regel in einem Satz>

**Regel (Vorschlag, wortwoertlich so umsetzbar):** <drei bis acht Saetze, mit allen Zahlen und
Bedingungen; so formuliert, dass ein Programmierer sie ohne Rueckfrage umsetzen kann.>

**Begruendung:** <zwei bis vier Saetze: warum diese Regel, was sie im Spiel bewirkt, welchen Fehler
sie verhindert.>

**Quellenlage:** BELEGT (Handbuchstelle nennen) / TEILBELEGT (was ist belegt, was nicht) /
NICHT BELEGT - VORSCHLAG. Bei Analogie: welches System, warum uebertragbar.

**Zahlen:** <jede Zahl mit Begruendung und, wo moeglich, einer Herleitung aus vorhandenen Werten
(Wallschwellen, Waffenschaden, Ladungen, AT/PA/TP/RS/LE/MU). Keine Zahl ohne Begruendung.>

**Folgen fuer den Code:** <welche Felder des Kampfberichts dadurch sicher werden, welcher Test den
Fall pruefen muesste, und was sich fuer Spieler UND Bots aendert.>

**Restrisiko:** <was auch mit dieser Regel offen bleibt, in einem Satz.>

ZUM SCHLUSS
- Eine Tabelle mit allen acht Punkten: Punkt | Regel in einem Satz | Quellenlage | sicher/unsicher.
- Ein Absatz "Was ich NICHT empfehle" mit zwei bis drei Regeln, die naheliegen, aber dem Spiel
  schaden wuerden (mit Grund).
- Ein Absatz "Widersprueche zum Ist-Stand": wo deine Regel eine heute gebaute Regel aendert, sag es
  ausdruecklich - Daniel entscheidet, nicht du.
