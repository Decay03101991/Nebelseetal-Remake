RAHMEN UND VORGABEN (gelten fuer jede Aufgabe; Daniel, 31.10.2026)

1. ROLLE: Du bist PRUEFER UND ENTWERFER, nicht Erzaehler. Du urteilst ausschliesslich nach dem
   beigefuegten Material. Was dort nicht steht, ist "nicht belegbar" - du erfindest keine
   Zeilennummern, keine Seitenzahlen, keine Werte. Kein Vorwort, kein Lob, keine Zusammenfassung.
   Sprache: Deutsch.
2. NEUESTE FASSUNG IST DAS ORIGINAL. Nennt die NEUERE Fassung nur WERTE und beschreibt die AELTERE
   Fassung die MECHANIK, dann gilt: MECHANIK aus der aelteren, ZAHLEN aus der neueren Fassung. Das
   ist eine begruendete Zusammenfuehrung und ausdruecklich erlaubt - kennzeichne sie als
   "ZUSAMMENFUEHRUNG" und nenne beide Quellen mit Stelle.
3. NUR was in KEINER Fassung steht, ist VORSCHLAG. Vorschlaege werden so gekennzeichnet und mit
   einem Satz begruendet (Spielgefuehl, Balance, Einzelspieler-Tauglichkeit).
4. Daniels eigene fruehere Annahmen (z. B. Sieg bei 300 Gesamtpunkten) sind VERWERFBAR, wenn die
   Quellen etwas anderes vorgeben.
5. Einzelspieler statt Mehrspieler: das Original war ein Browsergame mit vielen Spielern. Hier gibt
   es EINEN Menschen und wenige Bots. Wo eine Regel nur wegen vieler Spieler existiert (z. B. 20
   Dimensionen als Platz fuer hunderte Welten), darf sie fuer den Einzelspieler neu gedeutet werden -
   aber so, dass sie Sinn ergibt und die Originalmechanik erkennbar bleibt.
6. Spieluhr: Faktor 180, also 1 Spielstunde = 20 echte Sekunden. Handbuch-Raten gelten pro
   SPIELSTUNDE; das Original lief in Echtzeit.
7. Belegpflicht: jede Aussage mit Datei und Zeile (bzw. Dokument + Stelle). "Nicht belegbar" ist ein
   vollwertiges Ergebnis.

AUSGABEFORMAT (allgemein)
- Tabellen genau in der vorgegebenen Spaltenzahl, hoechstens die genannte Zeilenzahl.
- Jede Zeile mit Quelle (Dokument + Stelle) oder dem Wort VORSCHLAG.
- Am Ende hoechstens drei Saetze "Was das fuer den Code bedeutet" - ohne Code zu schreiben.

AUFGABE C - SPIELBARKEIT BEI x180 UND BEWERTUNG STATT SIEG

STAND DER ENTSCHEIDUNGEN (Daniel, 31.10.2026):
  * Es gibt KEINEN Sieg wie im Original - ein Lauf endet nicht mit "gewonnen". Ein Ziel bei 300
    Gesamtpunkten ist VERWORFEN (Handbuch Seite 3: "Jeder hat bei Nebelseetal sicher seine eigenen
    Ziele" - Spielziel = Feldherr, Forscher oder Haendler).
  * Stattdessen soll ein Lauf BEWERTET werden: Auszeichnungen fuer die meisten Forschungspunkte, die
    meisten Kriegspunkte, die groesste Wirtschaftsmacht o. Ae.

VERLANGE:
1. Tabelle "Groesse | belegter Wert | Wirkung bei x180 (gerechnet) | Urteil (spielbar / zaeh /
   unspielbar)" fuer: Produktion je Gebaeude und Gelaende, Siedlerzuwachs (1/Stunde), Forschungsdauer
   (neue Stufe hoch 2 in Stunden), Ausbildungszeiten, Kriegspunkte je Einheit, Verteidigungsanlagen
   (Ausbaustufe hoch drei), Verhaeltnis Kriegs- zu Forschungspunkten. Rechne die Echtzeit bei x180 aus.
2. BEWERTUNG STATT SIEG: Entwirf ein Auszeichnungssystem, das die im Handbuch genannten Spielziele
   (Feldherr, Forscher, Haendler) abbildet. Hoechstens 6 Auszeichnungen, je mit Name, Kennzahl,
   Rechenweg aus BELEGTEN Punkten und warum sie zum Original passt. Sag ausdruecklich, wenn eine
   Kennzahl fehlt (Handelspunkte gibt es nur in der Fassung 2006).
3. WANN ENDET EIN LAUF DANN? Zwei Varianten (Zeitlimit, erreichte Auszeichnung, freies Weiterspielen
   bis alle Siedlungen verloren) mit Vor-/Nachteil und einer Empfehlung.
4. Die drei kleinsten Stellschrauben, die keine Originalzahl veraendern (Zeitfaktor, Startbedingungen,
   Kartengroesse) - mit Zahlen.

AUSGABEFORMAT
## Tabelle
| Groesse | belegter Wert | Wirkung bei x180 | Urteil |
## Bewertung statt Sieg
| Auszeichnung | Kennzahl | Rechenweg | Passung zum Original |
## Wann endet ein Lauf
## Drei Stellschrauben
## Fehlende Zahlen


==============================================================================
1  PUNKTE, SCHUTZ, SPIELZIEL (Projektauswertung Handbuch)
==============================================================================

# Originaldaten: Kampf, Aufträge, Punkte, Schutz

**Richtschnur für das Remake.** Quelle: Original-Handbuch `Nebelseetal_Spielanleitung_2009.pdf`
(Seiten 4/5, 18–23). Textfassung: `Spielanleitung_2009_Textfassung.txt`.
Ergänzend: `Spielanleitung_2005/punktesystem.php.txt`, `handel.php.txt`, `portal.php.txt`.

---

## 1. Auftragsarten (Handbuch Seite 18/19)

Einheiten werden über den Menüpunkt **Aufträge** befehligt. Ziele: eigene Siedlung,
**Portalkoordinaten**, Verbündeter, Gildenmitglied.

| Auftragsart | Ablauf |
|---|---|
| **Stationieren** | Einheiten reisen zu einer Siedlung und bleiben dort; mit Karren können Waren mitgenommen werden. In **fremden** Siedlungen nicht möglich. |
| **Spionage** | Spionagebericht mit Siedlungskarte, gelagerten Ressourcen, stationierten Einheiten, Verteidigungsanlagen und deren Zustand. Pferde können mitgegeben werden (frisches Pferd = schneller). |
| **Transportieren** | Nur mit Transporteinheiten (Handkarre, Einspänner, Zweispänner). Liefert ab und **kehrt zurück**. Kriegseinheiten können begleiten, nützen aber nichts. |
| **Handeln** | Handelskarawanen zu einem anderen Spieler, mit Kaufpreis. Der Partner bestätigt (Gold fließt automatisch) oder lehnt ab (Karawane kehrt mit Ware zurück). |
| **Angriff** | Truppen greifen eine feindliche Siedlung an. Siehe Abschnitt 2. |

**Zeitangaben gelten für eine Strecke.** Bei Rückkehr (z. B. Transport) dauert der Auftrag doppelt so lang.

**Auftragskosten:** eigene Siedlungen kosten Gold und Nahrung (je nach Einheiten); fremde Siedlungen
zusätzlich **Mana für das Portal**, abhängig von der Entfernung der Zielwelt. Geschwindigkeit ist in
**10-%-Schritten drosselbar**: langsamer = **weniger Gold, mehr Nahrung**, angezeigt als „Reisedauer".

---

## 2. Kampfablauf (Handbuch Seite 20–22)

### 2.1 Vorrunde — Verteidigungswall überwinden

Zuerst wird geprüft, ob der Angreifer den Wall überwinden kann. Dazu wird die **Schlagkraft (SK)
aller angreifenden Fußtruppen** summiert. Sie muss den **Schwellenwert** des Walls erreichen.
Ab der **verstärkten Palisade** ist zusätzlich Schlagkraft von **Belagerungswaffen** nötig.
Reicht sie nicht, ziehen sich die Truppen zurück — der Kampf gilt als **unentschieden**.

| Verteidigungswall (Ausbaustufe) | Schwellenwert Fußtruppen | Schwellenwert Belagerungswaffen |
|---|---|---|
| Erdwall (1) | 10 | — |
| Steinwall (2) | 40 | — |
| Kleine Palisade (3) | 90 | — |
| Palisade (4) | 160 | — |
| Verstärkte Palisade (5) | 250 | 500 |
| Mauer (6) | 360 | 600 |
| Verstärkte Mauer (7) | 490 | 700 |
| Festungsmauer (8) | 640 | 800 |
| Verstärkte Festungsmauer (9) | 810 | 900 |
| Bollwerk (10) | 1000 | 1000 |

**Mauerschaden:** Belagerungswaffen beschädigen die Mauer; eine beschädigte Mauer verlangt
**prozentual weniger Schlagkraft**. Beispiel aus dem Handbuch: eine verstärkte Mauer (Stufe 7) mit
nur noch 50 % Zustand ist mit 245 Schlagkraft Fußtruppen + 350 Schlagkraft Belagerungswaffen zu
stürmen (jeweils die Hälfte).

Schadensermittlung: **Schaden der Waffe (Zufallswert, siehe Einheitentabelle) minus Ausbaustufe der
Mauer**; bleibt ein positiver Rest, wird er vom Zustand der Mauer abgezogen.
Beispiel: Katapult (Schaden **2-13**) gegen Mauer Stufe 6, gewürfelt 8 → 8 − 6 = 2 → Zustand 100 % → **98 %**.
Der Schaden wird **für jede mitgeführte Belagerungswaffe einzeln** ermittelt.

### 2.2 Kampfsequenzen

- Eine Schlacht läuft in **Kampfsequenzen**. Nach **10 Sequenzen** ohne Sieger endet sie
  **unentschieden** — der Angreifer zieht sich **ohne Beute** zurück.
- Ablauf je Sequenz:
  1. **Fernkampf gleichzeitig**: angreifende Fernkämpfer schießen auf die **Fußtruppen** des
     Verteidigers (sind keine vorhanden, auf dessen Fernkämpfer) — gleichzeitig schießen die
     verteidigenden Fernkämpfer auf die Fußtruppen des Angreifers (analog). **Erst beide feuern,
     dann werden die Verluste beider Seiten berechnet.**
  2. **Nahkampf**: die angreifenden Nahkämpfer stürmen **nacheinander** je eine **zufällige**
     verteidigende Nahkampfeinheit (sind keine mehr da, die Fernkämpfer).
  3. Nach allen angreifenden Einheiten beginnt die nächste Sequenz.
- Ende: eine Armee hat **keine Nahkampfeinheiten** mehr, **oder** 10 Sequenzen sind vorbei.

### 2.3 Zweikampf (Einheit gegen Einheit)

- Läuft in **Kampfrunden**. Die Einheit mit dem **höheren Mutwert (MU)** beginnt; bei Gleichstand
  der Verteidiger.
- Angriff: Zufallszahl 1–100 **≤ AT** = Treffer. Sonst verfehlt, der Gegner ist dran.
- Bei Treffer: Prüfung, ob der Verteidiger mit seinem **PA** pariert. Pariert er, **kein Schaden**,
  und er ist selbst mit Angreifen dran.
- Kein Parieren: Schaden = Zufallswert im **TP-Bereich** der Einheit **minus RS** des Verteidigers.
  Sinkt der Wert dadurch auf 0 oder darunter, wird trotzdem **1 Schadenspunkt** angerichtet.
  Der Schaden geht von der **LE** ab.
- **LE unter 1** → Einheit stirbt (wird nach der Schlacht gelöscht).
  **LE unter 5** → anhand des **MU** entscheidet sich, ob sie weiterkämpft oder **flieht**.
  Geflohene Einheiten stehen dem Spieler nach der Schlacht **wieder zur Verfügung**.
  Je niedriger der MU, desto wahrscheinlicher die Flucht.
- **Erschöpfung:** der Sieger eines Zweikampfs verliert **1 Punkt AT und PA** bis zum Ende der
  Schlacht (summiert sich). Deshalb kann Übermacht schwacher Einheiten starke besiegen.

### 2.4 Ausgang der Schlacht

- Sind **alle verteidigenden Einheiten tot oder geflohen**, gewinnt der **Angreifer**. Führt er
  **Transportkarren** mit, beginnen diese die Siedlung zu **plündern**.
- Sind **alle angreifenden Fußtruppen tot oder geflohen**, gewinnt der **Verteidiger**.
- Der **Verlierer** verliert einen Teil seiner Karren und Belagerungswaffen; wie viele, hängt von der
  Dauer ab. Jede Einheit hat **40 % Fluchtchance**, die pro Kampfsequenz um **5 %** steigt.
- **Unentschieden:** alle Karren und Belagerungswaffen bleiben erhalten.

---

## 3. Punktesystem (Handbuch Seite 3–5)

| Punktart | Berechnung |
|---|---|
| **Forschungspunkte** | Summe aller Forschungsstufen **hoch drei**. Beispiel: Felderwirtschaft 1 = 1, Kriegskunst 4 = 64, Minenarbeit 2 = 8 → **73** |
| **Kriegspunkte** | je Einheit ein fester Punktewert (siehe Liste unten) **plus** Verteidigungsanlagen: **Ausbaustufe³**. Beispiel: Palisade Stufe 4 = **64** |
| **Gesamtpunktzahl** | **(Kriegspunkte + Forschungspunkte) / 2** |
| **Rufpunkte** | für aktive Spielteilnahme; gehen **nicht** in die Gesamtpunktzahl ein, sind gegen Boni (z. B. Extraressourcen) eintauschbar. Bei Punktgleichheit entscheidet der **höhere Ruf**, danach das **frühere Anmeldedatum**. |

**Kriegspunkte je Einheit (wörtlich aus dem Handbuch):**
Bürgerwehr 1 · Kämpfer 2 · Krieger 4 · Ritter 8 · Paladin 16 ·
Kurzbogenschütze 2 · Bogenschütze 4 · Langbogenschütze 8 · Armbrustschütze 10 ·
Belagerungsturm 2 · Ramme 3 · Großer Belagerungsturm 4 · Große Ramme 5 · Balliste 6 · Katapult 7 ·
Großes Katapult 8 · Streuner 1 · Gauner 2 · Dieb 4 · Meisterdieb 8 · Kundschafter 10 ·
Waldläufer 16 · Handkarren 1 · Einspänner 2 · Zweispänner 3.
(Handelskarawanen, Siedlerkarren und Sammlerkarren haben **„Punktewert: -"**, geben also **keine** Kriegspunkte.)

Beispiel aus dem Handbuch: 10 Paladine + 12 Bogenschützen = 10·16 + 12·4 = **208 Kriegspunkte**.

---

## 4. Götterschutz (Handbuch Seite 5)

- Neue Spieler sind die **ersten sieben Tage** geschützt und **nicht angreifbar**.
- Der Schutz endet **früher**, sobald der Spieler seinen **ersten Kriegspunkt** erhält — also bereits
  beim Ausbau von Verteidigungsanlagen oder bei der ersten Militär-/Spionageeinheit.
- **Bis 299 Punkte: eingeschränkter Götterschutz.** Angriff nur auf Spieler im Bereich
  **eigene Punktzahl ± 20 %**. Über die Grenze von 299 Punkten hinweg ist **kein** Angriff möglich
  (in keine Richtung). Ein Spieler mit 299 Punkten kann nur 240–299 angreifen und ist für alle
  oberhalb 299 nicht angreifbar.
- **Ab 300 Punkten: kein Schutz** mehr.
- Geschützte Spieler erscheinen in Ruhmeshalle und Portal **grün** und mit einem **grünen Punkt**.

---

## 5. Weitere belegte Spieldaten

| Regel | Wert |
|---|---|
| Startwerte | 10 Siedler, 100 Holz, 100 Steine |
| Maximale Siedlungen | 6 |
| Siedlungsnamen | Karte wird zufällig zugewiesen; nie zweimal dieselbe gleichzeitig |
| Schriftverkehr | Nachrichten leuchten auf; Bestätigungen über erfüllte Aufträge laufen dort ein |
| Gildenwertung | nur Gilden mit **mehr als zwei** Mitgliedern werden gewertet |
| Rangfolge bei Punktgleichheit | höherer Ruf, danach früheres Anmeldedatum |
| Bauplätze | Gebäude auf der Siedlungskarte platzieren; Mauszeiger zeigt Eignung; Abriss bringt nichts zurück |
| Echtzeit | Produktion, Bewegung, Forschung laufen in Echtzeit ab, nicht in Runden |
| Bibliothek | nur auf Grasland, Steppe oder Nebelsee; **eine je Siedlung** |
| Ausbildungsgebäude | Kriegerakademie, Diebesgilde, Stellmacher — je **eines** je Siedlung |
| Werkstätten | Schmiede, Bogner, Nähstube — **mehrfach** möglich, fertigen parallel |


==============================================================================
2  HANDBUCH 2009 - Spielziel im Wortlaut (Seite 3)
==============================================================================

===== Seite 3 =====
Grundlegendes
In diesem Abschnitt der Anleitung werden grundlegende Dinge, wie das Spielziel, der 
Bildschirmaufbau oder das Punktesystem erklärt. 
Spielziel
Jeder hat bei Nebelseetal sicher seine eigenen Ziele. Großer Feldherr, friedlicher Forscher oder 
einflussreicher Händler, das alles ist möglich. Der Weg zu jedem dieser Ziele führt jedoch über 
die Rohstoffe, die Du für so gut wie alles im Nebelseetal benötigst. Der direkteste Weg an 
Rohstoffe zu kommen ist, sie mit speziellen Gebäuden zu erwirtschaften. Später kommen dann 
noch die Möglichkeiten Raub und Handel hinzu. 
Um viele Rohstoffe zu bekommen musst Du viele Gebäude bauen. Mit den Rohstoffen kannst 
Du dann forschen, um z.B. Deine Rohstoffproduktion zu steigern, oder neue Rohstoffe zu 
ermöglichen (z.B. Wolle oder Gold). Wenn Du genug zusammengetragen hast, kannst Du 
zusätzliche Siedlungen gründen (bis maximal 6 Siedlungen) und somit noch mehr Rohstoffe 
ansammeln.
Bildschirmaufbau
Am linken Bildschirmrand befindet sich das Hauptmenü. Von hier aus gelangst Du in die 
verschiedenen Hauptbereiche des Spiels. Außerdem werden hier die neusten fünf Nachrichten, 
die Du erhalten hast und Deine Punkte angezeigt. Über das Dropdownfeld, über dem Menü 
kannst Du zwischen Deinen Siedlungsübersichtseiten und der Spielübersichtsseite wechseln.
Am oberen Bildschirmrand befindet sich die Ressourcenleiste. Wenn Du Dich in einem 
Unterbereich einer Deiner Siedlungen befindest, werden hier die Ressourcen selbiger 
angezeigt. In der Hauptübersicht und in allen anderen Bereichen, die keiner bestimmten 
Siedlung zugeordnet sind, stehen hier die Gesamtressourcen aus allen Siedlungen.
In der Mitte des Bildschirms befindet sich der Hauptanzeigebereich. Hier werden die Inhalte 
der verschiedenen Spielbereiche angezeigt. 
In manchen Bereichen, wie z.B. der Siedlungsübersicht, wird am rechten Bildschirmrand ein 
weiteres Menü eingeblendet. Über dieses gelangt man in weitere Unterbereiche des Spiels.
Hauptmenü
Hier eine kurze Erläuterung zu den einzelnen Hauptmenüpunkten, eine genaue Beschreibung 
findest Du in den Entsprechenden Abschnitten dieser Anleitung:
Übersicht
Über diesen Menüpunkt kommst Du direkt auf die Spielübersichtsseite, auf der Du auch direkt 
nach dem Einloggen landest.
Portal
Alle Welten in Nebelseetal, liegen im magischen Limbus, der sich in 20 Dimensionen aufteilt. 
Diese sind über magische Portale miteinander verbunden. Im Portalbereich siehst Du die 
Position Deiner Welt und die der Welten anderer Spieler im Limbus. Je weiter eine andere 
Spielwelt von Deiner Welt entfernt liegt, desto mehr Mana kostet es, das Portal zu öffnen, um 
Einheiten zu diesem Spieler zu entsenden.
Seite 3


===== Seite 4 =====
Diplomatie
Im Diplomatiebereich kannst Du einer Gilde beitreten, eine eigene Gilde Gründen und


==============================================================================
3  HANDBUCH 2009 - Punkte im Wortlaut (Seite 4/5)
==============================================================================

Im Diplomatiebereich kannst Du einer Gilde beitreten, eine eigene Gilde Gründen und 
verwalten, verbündete Spieler (Buddyliste) suchen und Dein Herrscherprofil (Spielerprofil) 
anlegen. 
Einstellungen
Hier kannst Du Dein Passwort ändern, den Newsletter bestellen/abbestellen, einen anderen 
Spielskin wählen, in den Urlaubsmodus wechseln und, falls gewünscht, Deinen Account 
löschen. Letzteres kann nicht rückgängig gemacht werden!
Ruhmeshalle
In diesem Bereich kannst Du sehen wie Stark andere Spieler sind und wo Du dich unter ihnen 
platzierst.
Gildenhalle
In der Gildenhalle sind alle Gilden nach ihrer Stärke aufgelistet. Die Gildenstärke ergibt sich aus 
den Punkten ihrer Mitglieder. Es werden nur Gilden mit mehr als zwei Mitgliedern gewertet.
Voraussetzungen
Um Einheiten auszubilden, Gebäude zu bauen, Waren zu produzieren und Forschungen zu 
betreiben muss Dein Volk bestimmte Voraussetzungen, wie Gebäudestufen oder 
Forschungsstufen erfüllen. Welche Voraussetzungen das sind und ob Dein Volk sie schon erfüllt 
hat kannst Du in diesem Bereich einsehen.
Nachrichten
Im Nachrichtenmenü siehst Du alle Nachrichten, die an Dich gesendet wurden und Du 
bekommst hierher die Bestätigungsmeldungen, wenn Einheiten von Dir Deine Aufträge erfüllt 
haben. Wenn Du eine Neue Nachricht erhalten hast, leuchtet der Nachrichtenbutton auf.
Forum
Über diesen Link gelangst Du ins Nebelseetal-Forum.
IRC-Chat
Über diesen Link gelangst Du direkt in den Nebelseetal IRC-Chanel.
Logout
Wenn Du Deine Spielzüge getätigt hast, kannst Du dich hier ausloggen.
Punktesystem
Um in der Ruhmeshalle, in der alle Spieler aufgeführt werden, weit oben zu stehen, musst Du 
möglichst viele Gesamtpunkte erreichen. In Nebelseetal-Online gibt es drei verschiedene Arten 
von Punkten: 
Forschungspunkte
Diese Punkte geben Deinen aktuellen Forschungsstand an. Für jede Forschung die Du erlangt 
hast, wird die Forschungsstufe hoch drei genommen. Die so gewonnenen Werte, werden 
anschließend addiert und ergeben Deine Forschungspunkteanzahl.
Ein Beispiel:
Felderwirtschaft Stufe 1 = 1 Punkt (1*1*1=1)
Kriegskunst Stufe 4 = 64 Punkte (4*4*4=64)
Minenarbeit Stufe 2 = 8 Punkte (2*2*2=8)
Gesamtforschungspunkte = 73 (1+64+8=73)
Seite 4


===== Seite 5 =====
Kriegspunkte
Für jede Militär- und Spionageeinheit die Du ausbildest, bekommst Du Kriegspunkte. Wie viele 
Punkte hängt von der entsprechenden Einheit ab:
•
Bürgerwehr: 1 Punkt 
•


==============================================================================
4  VORVERSION 2006 - Punktesystem inkl. Handelspunkte
==============================================================================

Punktesystem
|
Punktesystem
|
In Nebelseetal-Online gibt es 3 verschiedene Arten von Punkten:
Forschungspunkte
Diese Punkte geben Euren aktuellen Forschungsstand an. Für jede Forschung die Ihr
erlangt habt, wird die Stufe mit sich selbst multipliziert. Diese Werte werden
anschließend addiert und ergeben Eure Forschungspunkteanzahl.
Ein Beispiel:
Felderwirtschaft Stufe 1 = 1 Punkt (1*1=1)
Kriegskunst Stufe 4 = 16 Punkt (4*4=16)
Minenarbeit Stufe 2 = 4 Punkt (2*2=4)
Gesamtforschungspunkte = 21 (1+16+4=21)
Kriegspunkte
Für jede Militär- und Spionageeinheit die Ihr ausbildet, bekommt Ihr Kriegspunkte.
Wieviele Punkte hängt von der entsprechenden Einheit ab:
Bürgerwehr: 1 Punkt
Kämpfer: 2 Punkte
Krieger: 4 Punkte
Ritter: 8 Punkte
Paladin: 16 Punkte
Kurzbogenschütze: 2 Punkte
Bogenschütze: 4 Punkte
Langbogenschütze: 8 Punkte
Armbrustschütze: 10 Punkte
Streuner: 1 Punkte
Gauner: 2 Punkte
Dieb: 4 Punkte
Meisterdieb: 8 Punkte
Kundschafter: 10 Punkte
Waldläufer: 16 Punkte
Solltet Ihr Einheiten verlieren, verringern sich auch Eure Kriegspunkte, um den entsprechenden Wert!
Handelspunkte
Handelspunkte bekommt Ihr, wenn Ihr über das Handelssystem Waren gegen Gold eintauscht.
Für je 100 Gold, die Ihr durch Handel erwirtschaftet, bekommt ihr einen Handelspunkt. Kleinere
Beträge werden mit eingerechnet. Wenn Ihr also etwas für 20 Gold verkauft bekommt Ihr 0,2 Punkte.
Wenn Ihr 24 Stunden keine Handelseinkünfte hattet, verliert ihr einen Handelspunkt.
Ein Beispiel:
Ihr verkauft 100 Schwerter für 300 Gold. Dafür bekommt ihr drei (300:100=3) Handelspunkte. Wenn Ihr nun 24 Stunden
lang nichts mehr verkauft wird euch ein Handelspunkt abgezogen. Nach weiteren 24 Stunden ein weiterer.
Dies bedeutet, das Ihr nach drei Tagen alle drei Handelspunkte wieder verlohren habt.
Ihr könnt dies verhindern in dem Ihr aktiv weiter handelt. Wenn Ihr, nachdem
Ihr die drei Punkte aus dem Beispiel oben bekommen habt, einen weiteren Handel abschließt,
bleiben eure Handelspunkte weitere 24 Stunden erhalten. Erst wenn nach dem letzten, abgeschlossenen Handel
24 Stunden vergangen sind, reduzieren sich eure Handelspunkte. Wenn Ihr also täglich mindestens einen
Handel mit einem anderen Spieler abschließt, verliert ihr keine Punkte.
Alle drei Punktearten fließen zu je einem Drittel in Eure Gesamtpunktezahl ein.
Diese geben Euren Platz in der Gesamtwertung an.


==============================================================================
5  PUNKTE-CODE (src/punkte.py, Konstanten und Rechenwege)
==============================================================================

"""
Nebelseetal Remake — Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026).

Belegte Originalregeln (Handbuch 2009, Seiten 3-6, nachgeprueft in
``docs/original/ORIGINAL_Kampf_und_Punkte.md``):

  * Forschungspunkte = Summe aller Forschungsstufen **hoch drei**
    ("Fuer jede Forschung die Du erlangt hast, wird die Forschungsstufe hoch drei genommen.
     Die so gewonnenen Werte werden anschliessend addiert." — Handbuch S. 3).
  * Kriegspunkte = fester Punktewert je Einheit (Handbuch S. 5)
    **plus** Verteidigungsanlagen: **Ausbaustufe hoch drei**
    ("Palisade (Ausbaustufe 4) = 64 Kriegspunkte (4*4*4=64)" — Handbuch S. 5).
  * Gesamtpunktzahl = **(Kriegspunkte + Forschungspunkte) / 2**
    ("Die Gesamtpunktzahl besteht aus der Summe von den Kriegs- und Forschungspunkten.
     Das Ergebnis wird dann durch zwei geteilt." — Handbuch S. 5/6).
  * Rufpunkte gehen **nicht** in die Gesamtpunktzahl ein; sie entscheiden nur bei
    Punktgleichheit (hoeherer Ruf zuerst, danach frueheres Anmeldedatum — Handbuch S. 6).
  * Goetterschutz: neue Spieler sind die **ersten sieben Tage** geschuetzt und nicht
    angreifbar (Handbuch S. 6). Der Schutz endet frueher mit dem ersten Kriegspunkt — das
    bildet dieser Baustein NICHT ab (Vorschlag, siehe unten).

NICHT belegt — als VORSCHLAG gekennzeichnet (siehe ``vorschlaege()``):
  * die Rundung der Gesamtpunktzahl bei ungerader Summe,
  * eine Sieg- und eine Niederlagebedingung (das Handbuch nennt **keine**),
  * der Startzeitpunkt des Goetterschutzes.

Das Modul rechnet nur, zeichnet nichts und aendert keine andere Datei.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import einheiten as _einheiten

# --------------------------------------------------------------------------
# Belegte Konstanten
# --------------------------------------------------------------------------

# Handbuch S. 6: "die ersten sieben Tage".
GOETTERSCHUTZ_TAGE = 7
SEKUNDEN_JE_TAG = 86400

# VORSCHLAG: Zielpunktzahl fuer den Sieg. Das Handbuch nennt keine Siegbedingung; 300 ist die
# belegte Schutzgrenze (Handbuch S. 6 "Spieler ueber 300 Punkten befinden sich ausserhalb des
# Goetterschutzes") und darum ein sichtbarer Meilenstein.
VORSCHLAG_ZIEL_PUNKTE = 300


# --------------------------------------------------------------------------
# Kleine Griffe
# --------------------------------------------------------------------------

def _stufe(wert) -> int:
    """Eine nicht-negative Ausbaustufe; alles Unbrauchbare gilt als 0."""
    try:
        return max(0, int(wert))
    except (TypeError, ValueError):
        return 0



[...]



# --------------------------------------------------------------------------
# 2. Kriegspunkte
# --------------------------------------------------------------------------

def kriegspunkte(einheiten: Optional[dict], wall_stufe: int) -> int:
    """Punkte aus Einheiten (fester Wert je Einheit) plus Wall (Stufe hoch drei).

    ``einheiten`` bildet Einheitenname -> Anzahl ab. Einheiten ohne Punktewert
    (Handelskarawanen, Siedlerkarren — Handbuch: "Punktewert: -") zaehlen 0.
    """
    summe = 0
    for name, anzahl in (einheiten or {}).items():
        summe += _ke_einheit(name) * _anzahl(anzahl)
    summe += _stufe(wall_stufe) ** 3
    return summe


# --------------------------------------------------------------------------
# 3. Gesamtpunktzahl
# --------------------------------------------------------------------------

def gesamtpunkte(forschungsstaende: Optional[dict], einheiten: Optional[dict],
                 wall_stufe: int) -> int:
    """(Kriegspunkte + Forschungspunkte) / 2 (Handbuch S. 5/6).

    VORSCHLAG: Das Handbuch nennt keine Rundung. Bei ungerader Summe wird
    **abgerundet** (``// 2``); der Rest 0.5 faellt weg. Begruendung in ``vorschlaege()``.
    """
    fp = forschungspunkte(forschungsstaende)
    kp = kriegspunkte(einheiten, wall_stufe)
    return (fp + kp) // 2


# --------------------------------------------------------------------------
# 4. Rufpunkte
# --------------------------------------------------------------------------


==============================================================================
6  ERTRAEGE, STARTWERTE, SIEDLER (data/resources.json und Handbuch)
==============================================================================

{
 "versionsvermerk": "Zwei Fassungen belegt: archivierte Spielanleitung 2005 (HTML) und Handbuch 2009 (Textfassung). Sie weichen bei mehreren Ertraegen und bei der Siedlergrenze ab. Primaerwerte = 2009; Abweichungen sind je Rohstoff in 'abweichung' bzw. unter 'siedler' vermerkt.",
 "gebaeude_ohne_forschung": [
  "Holzfäller",
  "Steinmetz",
  "Jäger",
  "Bibliothek",
  "Haus"
 ],
 "regeln": {
  "gelände": "Jedes produzierende Gebäude erzeugt auf 2 verschiedenen Geländearten unterschiedliche Mengen. Ausnahme: der Jäger (in der 2005er Fassung nur Wald, 2009 auch Steppe).",
  "sumpf": "Sümpfe sind unbebaubar und für Siedlungen wertlos.",
  "zuwachs": "Der Wert in Klammern ist die Produktionsmenge pro Stunde; der Rohstoffzuwachs pro Stunde steht im Spiel in Klammern hinter dem Bestand, ein Balken zeigt, wann die nächste Einheit dazukommt.",
  "echtzeit": "Produktion läuft in Echtzeit (Beispiel Handbuch: 4 Holz/Stunde = alle 15 Minuten 1 Einheit Holz).",
  "abriss": "Ein Abriss bringt keine Rohstoffe zurück.",
  "bibliothek": "Bibliothek nur auf Grasland, Steppe oder Nebelsee, eine je Siedlung."
 },
 "siedler": {
  "produktion_pro_stunde": 1,
  "grenze_neue_siedlung": {
   "handbuch_2009": 10,
   "fassung_2005": 5
  },
  "erhoehung_pro_haus": 5,
  "abweichung": "Siedlergrenze einer neuen Siedlung: Handbuch 2009 = 10 Siedler, 2005er Fassung = 5 Siedler. Erhöhung pro Haus in beiden Fassungen +5."
 },
 "startwerte": {
  "siedler": 10,
  "holz": 100,
  "steine": 100,
  "_anmerkung": "Startwerte laut Handbuch 2009 Seite 7 (10 Siedler, 100 Holz, 100 Steine) und ORIGINAL_Kampf_und_Punkte.md Abschnitt 5."
 },
 "max_siedlungen": 6,
 "rohstoffe": [
  {
   "id": "holz",
   "name": "Holz",
   "erzeugendes_gebaeude": [
    "Holzfäller"
   ],
   "ertrag_pro_stunde": {
    "Wald": 4,
    "Steppe": 2
   },
   "ertrag_2005": {
    "Wald": 4,
    "Steppe": 1
   },
   "abweichung": "Steppe: 2005 = 1, Handbuch 2009 = 2. Wald in beiden Fassungen 4."
  },
  {
   "id": "stein",
   "name": "Stein",
   "erzeugendes_gebaeude": [
    "Steinmetz"
   ],
   "ertrag_pro_stunde": {
    "Berg": 4,
    "Hügel": 2
   },
   "ertrag_2005": {
    "Berg": 4,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 2. Berg in beiden Fassungen 4."
  },
  {
   "id": "metall",
   "name": "Metall",
   "erzeugendes_gebaeude": [
    "Erzmine"
   ],
   "ertrag_pro_stunde": {
    "Berg": 3,
    "Hügel": 1.5
   },
   "ertrag_2005": {
    "Berg": 3,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 1,5. Berg in beiden Fassungen 3."
  },
  {
   "id": "mana",
   "name": "Mana",
   "erzeugendes_gebaeude": [
    "Tempel"
   ],
   "ertrag_pro_stunde": {
    "Nebelsee": 5,
    "alle Gelände außer Sumpf": 1
   },
   "ertrag_2005": {
    "Nebelsee": 8,
    "alle Gelände außer Sumpf": 2
   },
   "abweichung": "Nebelsee: 2005 = 8, Handbuch 2009 = 5. Übriges Gelände (außer Sumpf): 2005 = 2, Handbuch 2009 = 1."
  },
  {
   "id": "nahrung",
   "name": "Nahrung",
   "erzeugendes_gebaeude": [
    "Farm",
    "Jäger",
    "Rinderfarm (siehe Leder, Anmerkung)"
   ],
   "ertrag_pro_stunde": {
    "Grasland": 4,
    "Steppe": 2
   },
   "ertrag_2005": {
    "Grasland": 4,
    "Steppe": 2
   },
   "abweichung": null,
   "weitere_erzeuger": {
    "Jäger": {
     "ertrag_pro_stunde": {
      "Wald": 2,
      "Steppe": 1
     },
     "ertrag_2005": {
      "Wald": 1
     },
     "abweichung": "Jäger: Handbuch 2009 nennt zusätzlich Steppe (1 Nahrung), 2005 nur Wald (1 Nahrung); Wald: 2005 = 1, 2009 = 2."
    }
   }
  },
  {
   "id": "gold",
   "name": "Gold",
   "erzeugendes_gebaeude": [
    "Goldmine"
   ],
   "ertrag_pro_stunde": {
    "Berg": 3,
    "Hügel": 1.5
   },
   "ertrag_2005": {
    "Berg": 3,
    "Hügel": 1
   },
   "abweichung": "Hügel: 2005 = 1, Handbuch 2009 = 1,5. Berg in beiden Fassungen 3.",
   "anmerkung": "Schreibweise 2005: 'Goldmiene', Handbuch 2009: 'Goldmine'."
  },
  {
   "id": "wolle",
   "name": "Wolle",
   "erzeugendes_gebaeude": [
    "S

Diese führen beispielsweise in die Kriegerakademie in der Einheiten ausgebildet werden 
können, oder in die Bibliothek in der Du neue Wissensgebiete erforschen kannst. Diese Buttons 
und die dazu gehörigen Bereiche, werden in den entsprechenden Abschnitten dieser Anleitung 
näher erläutert.
Seite 9


===== Seite 10 =====
Rohstoffproduktion und Gebäude:
Gebäude
Rohstoff Produktion
Holzfäller
Holz
Wald (4), Steppe (2)
Steinmetz
Stein
Berg (4), Hügel (2)
Erzmine
Metall
Berg (3), Hügel (1,5)
Tempel
Mana
Nebelsee (5), alle außer Sumpf (1)
Farm
Nahrung
Grasland (4), Steppe (2)
Goldmine
Gold
Berg (3), Hügel (1,5)
Schafszucht
Wolle
Grasland (3), Steppe (1,5)
Rinderfarm
Leder
Grasland (3 Nahrung, 3 Leder),
Steppe (1,5 Nahrung, 1,5 Leder)
Pferdezucht
Pferde
Grasland (3), Steppe (1,5)
Jäger
Nahrung, 
Leder
Wald (2 Nahrung, 2 Leder), 
Steppe (1 Nahrung, 1 Leder)
Seite 10


===== Seite 11 =====
Jedes Gebäude produziert auf 2 verschiedenen Geländearten unterschiedliche Mengen an 
Rohstoffen. Wie viele Ressourcen pro Stunde produziert werden, kannst Du aus der Tabelle 
oben entnehmen. Der Wert in Klammern geben die Produktionsmenge pro Stunde an. Sümpfe 
sind unbebaubar und somit für Eure Siedlungen völlig wertlos. 
Deine Siedlung bekommt, außer den Rohstoffen, noch einen neuen Siedler pro Stunde, bis ihre 
Siedlergrenze erreicht ist. Diese Grenze liegt in jeder neuen Siedlung bei 10 Siedlern. Wenn Du 
in Deiner Siedlung Häuser errichtest, erhöht sich der Grenzwert um 5 Siedler pro Haus. Wann 
Du den nächsten Siedler bekommst, kannst Du in der Siedlungsübersicht, unter der 
Rohstoffzuwachstabelle sehen. 
Neben den schon genannten Rohstoffe produzierenden Gebäuden, gibt es noch die 
Produktions- und Ausbildungsstätten. Diese werden in späteren Abschnitten dieser Anleitung 
genauer beschrieben.
Seite 11


==============================================================================
7  FORSCHUNG: DAUER UND KOSTEN (Handbuch-Wortlaut)
==============================================================================

Forschungen sind wichtige Voraussetzungen, für Einheiten, Waffen, Gebäude und weitere 
Forschungsmöglichkeiten. Manche von ihnen erhöhen die Produktivität Deiner Siedlungen, 
andere ermöglichen den Bau neuer Gebäude und Einheiten oder steigern die Effektivität Deiner 
Kampfeinheiten. 
Um Forschung zu betreiben musst Du in Deiner Siedlung zunächst eine Bibliothek bauen. Dies 
kannst Du über den Button „Bauen“ im Siedlungsmenü tun. 
Hast Du genügend Ressourcen gesammelt, klicke in der Siedlungsübersicht auf „Bauen“ und 
wähle die Bibliothek aus. Sie kann nur auf Grasland, Steppe oder Nebelseen errichtet werden. 
In jeder Siedlung kann nur eine einzige Bibliothek gebaut werden. 
Verfügt Deine Siedlung über eine Bibliothek, erscheint im Siedlungsmenü der Button 
„Forschung“. Über diesen gelangst Du in den Forschungsbereich. In Diesem kannst Du, 
solange Deine Gelehrten nicht mit Studien beschäftigt sind, die Bibliothek ausbauen, oder 
einen Forschungsauftrag erteilen. 
Ausbauen der Bibliothek
Das Ausbauen der Bibliothek erfolgt in Stufen. Mit jeder Stufe, die Deine Bibliothek ausgebaut 
wird, stehen Dir weitere Forschungsmöglichkeiten in ihr offen. Welche Voraussetzungen Du für 
die Forschungen benötigst kannst Du unter „Voraussetzungen“ im Hauptmenü erfahren. Wenn 
Du genügend Ressourcen gesammelt hast, klicke im Forschungsbereich auf den Button 
„Bibliothek ausbauen“, um die Stufe der Bibliothek um 1 zu erhöhen. Der Ausbau wird mit 
jeder Stufe teurer. 
Forschung
Um Forschungsaufträge an Deine Gelehrten zu erteilen, suche Dir im Forschungsbereich die 
entsprechende Forschung aus und klicke dort auf „Forschen“. Die benötigten Ressourcen 
werden sofort zum experimentieren in die Bibliothek geschafft und Deine Gelehrten beginnen 
mit ihren Studien. 
Auch die Entwicklung Deiner Forschungsmöglichkeiten wird in Stufen angegeben und erhöht 
sich pro Forschungsauftrag um 1. Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in 
Stunden. Während dieser Zeit kannst Du in der Siedlung, in der geforscht wird, weder die 
Bibliothek ausbauen, noch einen weiteren Forschungsauftrag erteilen. 
Solltest Du Dich, aus welchem Grund auch immer, dazu entschließen die laufende Forschung 
abzubrechen, sind sowohl die investierte Zeit, als auch die eingesetzten Ressourcen verloren. 
Ein Beispiel: 
Du möchtest Deine Kenntnisse in der „Baukunst“ von Stufe 2 auf Stufe 3 anheben. Du hast 
bereits die nötigen Ressourcen gesammelt und in der Bibliothek sitzen Deine Gelehrten faul 
herum und erfreuen sich an Rauschkraut, Wein und diskutieren über philosophische Fragen... 
Sobald Du nun auf „Baukunst erforschen“ klickst, werden die für die Forschung benötigten 
Ressourcen von Deinem Siedlungsbestand abgezogen. Die Gelehrten machen sich sofort daran 
die Komplexität der „Baukunst“ zu erforschen. 
Seite 12


===== Seite 13 =====
Da Du diese auf die Stufe 3 anheben möchtest, wird das 9 Stunden in Anspruch nehmen. (3 * 
3 = 9) Während dieser Zeit, ist in der Siedlung, in der geforscht wird, der gesamte 
Forschungsbereich blockiert. Du kannst dort lediglich noch den Fortschritt der Studien 
beobachten, oder Deine Gelehrten anweisen, ihre Studien einzustellen. Solltest Du Dich zu 
Letzterem entscheiden, klicke auf den Button „Forschung abbrechen“. 
Nach einer erneuten Sicherheitsabfrage stellen Deine Gelehrten ihre Arbeit ein. In diesem Fall 
kannst Du, sofort wieder uneingeschränkt auf den Forschungsbereich zugreifen, allerdings sind 
die eingesetzten Ressourcen für die abgebrochene Forschung verloren. 
WICHTIG: Während der gesamten Studienzeit bleibt die Stufe Deiner Forschung noch auf 
ihrem alten Wert! Erst wenn die Forschungszeit vollständig abgelaufen ist und Du erneut den 
Forschungsbereich besuchst, um das Ergebnis deiner Gelehrten zu begutachten, erhöht sich 
die Stufe des Forschungsprojekts um 1. 
Die Rohstoffkosten die zum Forschen aufgebracht werden müssen, verdoppeln sich pro Stufe. 
Das bedeutet, wenn Du für eine Forschung Stufe1 50Holz benötigst, benötigst Du für Stufe2 
100Holz, für Stufe3 200Holz, für Stufe4 400Holz usw. 
Seite 13


==============================================================================
8  GEBAEUDE, WALLSCHWELLEN, AUSBILDUNGSGEBAEUDE
==============================================================================

# Gebäude, Aufbau und Freischaltung im Original (ausgelesen 30.10.2026)

**Quelle:** `docs/original/Spielanleitung_2009_Textfassung.txt` — Seiten 9–14 (Zeilen 330–460 im
Textsatz; die Datei markiert jede Seite mit `===== Seite N =====`). Wörtliche Zitate sind in
Anführungszeichen, Seitenzahl in Klammern.
**Zweck:** Daniel: „kannst du mal schauen, wie das mit dem Gebäudeaufbau und dem Freischalten
nacheinander im Originalspiel aufgebaut war" … „es gibt Abschnitte die einzelne Gebäude und deren
Funktion erklären … daraus können wir viel schließen."

---

## 1. Die Reihenfolge ist im Original NICHT eine Gebäudekette, sondern eine Freischaltung über die Bibliothek

Der Aufbau in der Anleitung, Seite für Seite:

| Seite | Inhalt |
|---|---|
| 9 | Die Siedlungsseite hat **Buttons, die in Bereiche führen** — „beispielsweise in die Kriegerakademie in der Einheiten ausgebildet werden können, oder in die Bibliothek in der Du neue Wissensgebiete erforschen kannst" |
| 10 | Tabelle **Rohstoffproduktion**: jedes Gebäude, welches Gelände, wie viel Ertrag pro Stunde |
| 11 | Regel: jedes Gebäude produziert auf **zwei** Geländearten unterschiedlich viel; **Sümpfe sind unbebaubar**; **1 neuer Siedler pro Stunde**, Grenze **10 je neuer Siedlung, +5 je Haus** |
| 12 | **Forschung**: Bibliothek bauen → Button „Forschung" erscheint; Ausbau in Stufen; Dauer und Kosten |
| 13 | Beispiel Baukunst 2→3 = 9 Stunden; Kosten verdoppeln sich je Stufe; während der Studien ist der Forschungsbereich **der Siedlung** blockiert |
| 14 | **Waren**: erst Waffen/Rüstungen produzieren (Schmiede, Bogenbauer, Näherei), dann Militäreinheiten |

**Kern der Freischaltung (Seite 12, wörtlich):**
1. „Um Forschung zu betreiben musst Du in Deiner Siedlung zunächst eine **Bibliothek** bauen. Dies
   kannst Du über den Button **„Bauen"** im **Siedlungsmenü** tun."
2. „Sie kann nur auf **Grasland, Steppe oder Nebelseen** errichtet werden. **In jeder Siedlung kann
   nur eine einzige Bibliothek gebaut werden.**"
3. „Verfügt Deine Siedlung über eine Bibliothek, **erscheint im Siedlungsmenü der Button
   „Forschung"**."
4. „Mit jeder Stufe, die Deine Bibliothek ausgebaut wird, stehen Dir **weitere
   Forschungsmöglichkeiten** in ihr offen."
5. „Welche Voraussetzungen Du für die Forschungen benötigst, kannst Du unter **„Voraussetzungen"**
   im Hauptmenü erfahren."

Damit ist Daniels Wunsch („Forschung erst als Menüpunkt, wenn eine Bibliothek steht") **original
belegt** — es ist im Original kein Sonderfall, sondern die normale Siedlungslogik. Das haben wir am
30.10. so gebaut.

## 2. Was die Forschungen freischalten (Seite 12)

„Forschungen sind wichtige Voraussetzungen, **für Einheiten, Waffen, Gebäude und weitere
Forschungsmöglichkeiten**. Manche erhöhen die Produktivität Deiner Siedlungen, andere ermöglichen
**den Bau neuer Gebäude und Einheiten** oder steigern die Effektivität Deiner Kampfeinheiten."

→ Die Freischaltung läuft also **über Forschungsstufen**, nicht über eine feste Gebäudereihenfolge.
Für uns heißt das: `data/units.json` (`voraussetzung`) und `data/buildings.json`
(`voraussetzung`) sind die richtige Stelle — und `research.json` (Feld `voraussetzung`, z. B.
„Bibliothek 1") die Bedingung darüber.

## 3. Harte Zahlen aus dem Abschnitt (alle wörtlich belegt)

| Regel | Wert | Seite |
|---|---|---|
| Forschungsdauer | **neue Stufe² in Stunden** („Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in Stunden") | 12 |
| Forschungsstufe steigt | **erst nach Ablauf** der Zeit („Während der gesamten Studienzeit bleibt die Stufe … auf ihrem alten Wert") | 13 |
| Kosten je Forschungsstufe | **verdoppeln sich** (Stufe 1 = 50 Holz → 100 → 200 → 400 …) | 13 |
| Blockade | während der Studien in **dieser Siedlung** kein Ausbau und kein zweiter Auftrag | 12/13 |
| Abbruch | investierte Zeit **und** Rohstoffe sind verloren | 12 |
| Bibliothek-Ausbau | mit jeder Stufe teurer, jede Stufe schaltet Forschungen frei | 12 |
| Siedlergrenze | 10 je neuer Siedlung, **+5 je Haus**, 1 Siedler/Stunde Zuwachs | 11 |
| Gelände | jedes Produktionsgebäude hat **zwei** bevorzugte Geländearten, **Sumpf unbebaubar** | 10/11 |

## 4. Erträge je Gebäude und Gelände (Seite 10, wörtlich)

| Gebäude | Rohstoff | Wald | Steppe | Berg | Hügel | Grasland | Nebelsee | sonst |
|---|---|---|---|---|---|---|---|---|
| Holzfäller | Holz | 4 | 2 | – | – | – | – | – |
| Steinmetz | Stein | – | – | 4 | 2 | – | – | – |
| Erzmine | Metall | – | – | 3 | 1,5 | – | – | – |
| Tempel | Mana | – | – | – | – | – | 5 | alle außer Sumpf 1 |
| Farm | Nahrung | – | 2 | – | – | 4 | – | – |
| Goldmine | Gold | – | – | 3 | 1,5 | – | – | – |
| Schafszucht | Wolle | – | 1,5 | – | – | 3 | – | – |
| Rinderfarm | Leder (+Nahrung) | – | 1,5 / 1,5 | – | – | 3 / 3 | – | – |
| Pferdezucht | Pferde | – | 1,5 | – | – | 3 | – | – |
| Jäger | Nahrung, Leder | 2 / 2 | 1 / 1 | – | – | – | – | – |

## 5. Gegen den Code gehalten (was schon stimmt — nicht neu prüfen)

| Punkt | Befund |
|---|---|
| Forschungsdauer Stufe² | **stimmt schon**: `src/forschung.dauer_stunden()` = Stufe², über `spieldaten.forschungsdauer_stunden` |
| Kostenverdopplung | **stimmt schon**: `src/forschung.py` Kopf nennt „Stufe 1 = 50 Holz, dann 100, 200, 400, 800 …" |
| Bibliothek nur Grasland/Steppe/Nebelsee | **stimmt schon**: `data/buildings.json`, `nur_auf` = genau diese drei, mit Belegvermerk `_belegt_nur_auf` |
| Eine Bibliothek je Siedlung | **stimmt schon**: `max_je_siedlung` = 1, durchgesetzt in `bauen_auf_karte` |
| Forschung erst ab Bibliothek | **am 30.10. gebaut**: Menüpunkt erscheint nur mit Bibliothek |
| Siedlergrenze 10 + 5 je Haus | **stimmt schon**: `gebaeude_wirkung.siedlergrenze_je_siedlung` |
| Sumpf unbebaubar | **stimmt schon**: Geländeregeln (Projektregel seit 05.10.) |

## 6. Widerspruch, den Daniel entscheiden muss

Daniels Vorgabe „höchstens **zwei** Bibliotheken je Spieler, eine dritte nicht" ist **strenger als
das Original**: das Handbuch begrenzt nur **je Siedlung** auf eine Bibliothek und setzt **keine**
Gesamtgrenze über das Spiel. Im Code steht seine Grenze (`BIBLIOTHEK_OBERGRENZE = 2`) und ist dort
als seine Entscheidung kommentiert. **Zu entscheiden:** Original folgen (Grenze fällt, je Siedlung
eine) oder Daniels Grenze behalten.

## 7. Was daraus für den Aufbau folgt (nah am Original)

1. **Siedlungsmenü führt die Bereiche** als Buttons: Dorfzentrum/Übersicht, Bauen (Produktion und
   Verteidigung), Lager, und — sobald gebaut — Kriegerakademie, Stellmacher, Diebesgilde,
   Bibliothek/Forschung. Genau das ist am 30.10. entstanden.
2. **Der Sprung „neue Einheiten" läuft über Forschung**, nicht über Gebäudeketten: Einheit X wird
   freigeschaltet, wenn ihre Forschung die Stufe erreicht (`data/units.json`, `voraussetzung`).
3. **Waren zuerst, dann Truppen** (Seite 14): Schmiede/Bogenbauer/Näherei liefern Waffen und
   Rüstungen, die Ausbildung verbraucht sie. In unserem Code prüft `ausbildung_start` die
   Ausrüstung vor Ort — stimmt mit dem Original.
