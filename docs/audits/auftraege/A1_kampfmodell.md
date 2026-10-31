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

AUFGABE A - KAMPF: WELCHE QUELLE GILT FUER WELCHEN SCHRITT, UND WIE WIRD DIE BEUTE GESTAFFELT?

Es gibt zwei Originalquellen fuer den Kampf:
  (1) HANDBUCH 2009: LE, AT, PA, RS, TP, MU, SK; Zweikampf in Kampfrunden; Sieger eines Zweikampfs
      verliert 1 Punkt AT und PA (Erschoepfung). Wallschwellen, Beute, Geraeteverlust, Punkte.
  (2) NEUERES FORUM-ORIGINAL (Material 2): Konstitution %, Kampfwert-Spanne, Ruestung, Fernkampfwert,
      Erschoepfungsschaden, Schwelle zur Kampfunfaehigkeit. Nennt WEDER Beute NOCH Geraeteverlust
      NOCH Punkte.

Im Remake folgt der Kampf heute Quelle (2) (`src/kampf.py`), Wall/Beute/Geraeteverlust/Punkte stammen
aus Quelle (1). Nach Vorgabe 2 ist das grundsaetzlich richtig - pruefe, ob es an JEDER Stelle richtig
angewandt ist.

TEIL A1: Tabelle "Kampfschritt | gilt | Quelle (Dokument + Stelle) | Art (belegt / ZUSAMMENFUEHRUNG /
VORSCHLAG)" fuer: Wallvorrunde, Mauerschaden, Fernkampf, Nahkampf/Zweikampf, Erschoepfung, Flucht,
Ausgang, Beute, Geraeteverlust, Punkte.

TEIL A2: Wo widersprechen sich die Quellen so, dass eine Zusammenfuehrung NICHT moeglich ist?
Hoechstens 6 Zeilen, je mit der kleineren Aenderung.

TEIL A3: GESTAFFELTE BEUTE (Daniels Vorgabe, noch ohne Zahlen):
  * Erster erfolgreicher Angriff, Mauer steht noch: Mauer wird beschaedigt/eingerissen, es wird WENIG
    erbeutet.
  * Mauer ist bereits (teilweise) eingerissen: deutlich MEHR Beute.
  * Keine Verteidiger mehr: der zum Angriffszeitpunkt vorhandene Bestand kann KOMPLETT mitgenommen
    werden - begrenzt durch die Karrenladung.
Belegt ist nur: "nur Transportkarren pluendern" und "Beute ist durch die Ladung begrenzt".
Verlange: eine konkrete Staffelung mit Prozentwerten und die Formel, in der sie greift (Eingaben:
Wallzustand vor dem Kampf, Wallzustand nach dem Kampf, ueberlebende Verteidiger, Karrenladung,
Ortslager). Nenne je Zahl VORSCHLAG mit halbem Satz Begruendung. Sag ausdruecklich, ob diese
Staffelung mit den Originalregeln vereinbar ist oder ihnen widerspricht.

TEIL A4: Drei Saetze, was das fuer `src/kampf.py`, `src/kampfbericht.py` und `data/` bedeutet.

AUSGABEFORMAT
## Tabelle der Schritte
| Schritt | gilt | Quelle (Dokument + Stelle) | Art |
## Widersprueche (hoechstens 6 Zeilen)
| Nr | Widerspruch | Quelle A | Quelle B | kleinere Aenderung |
## Gestaffelte Beute
| Lage | Beuteanteil | Rechenweg | VORSCHLAG-Begruendung |
## In keiner Quelle geregelt
- hoechstens 4 Punkte
## Was das fuer den Code bedeutet
1.-3.


==============================================================================
1  HANDBUCH 2009 - Kampf, Auftraege, Punkte, Schutz (Projektauswertung)
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
2  NEUERES FORUM-ORIGINAL (Volltext, Spielerfund)
==============================================================================

Das Kampfsystem
Das Kampfsystem zu verstehen ist ein bedeutender Schritt um im Nebelseetal bestehen zu können. Hier findet ihr die , durch mich vervollständigte, Erklärung aus dem Forum.
Hier ist der detaillierte neue Kampfablauf:Aktuell gelten diese Werte:
Bürgerwehr
Konstitution: 5%,
Kampfwert: 1-12
Rüstung: 0
Kämpfer
Konstitution: 15%
Kampfwert: 2-20
Rüstung: 2
Krieger
Konstitution: 25%
Kampfwert: 3-25
Rüstung: 4
Ritter
Konstitution: 50%
Kampfwert: 4-35
Rüstung: 8
Paladin
Konstitution: 70%
Kampfwert: 5-45
Rüstung: 12
Kurzbogenschütze
Konstitution: 15%
Kampfwert: 1-12
Rüstung: 0
Fernkampf: 20%
Bogenschütze
Konstitution: 25%
Kampfwert: 1-12
Rüstung: 0
Fernkampf: 30%
Langbogenschütze
Konstitution: 35%
Kampfwert: 1-12
Rüstung: 0
Fernkampf: 55%
Armbrustschütze
Konstitution: 45%
Kampfwert: 1-12
Rüstung: 2
Fernkampf: 70%
Streuner
Konstitution: 5%
Kampfwert: 2-15
Rüstung: 0
Gauner
Konstitution: 15%
Kampfwert: 2-20
Rüstung: 0
Dieb
Konstitution: 25%
Kampfwert: 2-25
Rüstung: 0
Meisterdieb
Konstitution: 35%
Kampfwert: 2-30
Rüstung: 0
Kundschafter
Konstitution: 45%
Kampfwert: 2-35
Rüstung: 2
Waldläufer
Konstitution: 55%
Kampfwert: 2-40
Rüstung: 4
Der Kampfablauf:Bevor ein Kampf stattfindet wird erst überprüft ob die Nahkampfeinheiten und die Belagerungswaffen über genug Schlagkraft verfügen die Mauer des Verteidigers zu überwinden. Wenn dieses der Fall ist kann der Kampf beginnen. Wenn nicht zieht sich der Angreifer wieder zurück.Vorrunde - FernkampfEs gibt vor der Schlacht Mauerstufe+1 Vorrunden, in der die Fernkämpfer beider Seiten, die gegnerischen Nahkampfeinheiten (Wenn keine mehr übrig sind auch die Fernkampfeinheiten) beschießen.Modifizierung des FernkampfwertesDurch die Mauer ist es für die angreifenden Schützen allerdings schwieriger die gegnerischen Einheiten zu treffen. Pro Mauerstufe ist der Fernkampfwert der angreifenden Schützen um 5% gesenkt. Die Beschädigung der Mauer wird hierbei berücksichtigt.Aber die Beschädigung durch die aktuell mitgeführten Belagerungswaffen wird erst nach der Vorrunde berechnet.Außerdem werden angreifende Nahkämpfer durch Belagerungstürme geschützt. Normale Belagerungstürme können 10 Einheiten und große Belagerungstürme 30 Einheiten schützen. Wenn diese Einheiten  beschossen werden bekommt der Fernkämpfer einen Malus von 30% auf dern Fernkampfwert.In Türmen werden immer zuerst die besten Einheiten geschützt.Die Forschung Bogenbau erhöht die Trefferchance der Schützen um 2% pro Stufe.SchadenGetroffene Einheiten erleiden Erschöpfungschaden. Je Fernkampfeinheit ist dieser Erschöpfungsschaden unterschiedlich hoch. Die Verschiedenen Einheitentypen können verschieden hohen, durch Fernkampf erlittenen Erschöpfungsschaden einstecken, bevor sie kampfunfähig werden:Erschöpfungsschaden:
Kurzbogenschützen
1 Erschöpfungsschaden pro Treffer
Bogenschützen
2 Erschöpfungsschaden pro Treffer
Langbogenschützen
3 Erschöpfungsschaden pro Treffer
Armbrustschützen
4 Erschöpfungsschaden pro Treffer
Kampfunfähigkeit bei Erschöpfung:
Bürgerwehr
1 Erschöpfungspunkt
Kämpfer
3 Erschöpfungspunkte
Krieger
5 Erschöpfungspunkte
Ritter
7 Erschöpfungspunkte
Paladin
9 Erschöpfungspunkte
Kurzbogenschützen
1 Erschöpfungspunkt
Bogenschützen
2 Erschöpfungspunkte
Langbogenschützen
3 Erschöpfungspunkte
Armbrustschützen
4 Erschöpfungspunkte
Streuner
1 Erschöpfungspunkt
Gauner
2 Erschöpfungspunkte
Dieb
3 Erschöpfungspunkte
Meisterdieb
4 Erschöpfungspunkte
Kundschafter
5 Erschöpfungspunkte
Waldläufer
6 Erschöpfungspunkte
 Wird eine Einheit Kampfunfähig, wird anhand ihrer Konstitution bestimmt, ob sie die Schlacht überlebt, oder stirbt. Sie nimmt aber in beiden Fällen nicht weiter an der Schlacht teil. Ein durch Zufall bestimmter Wert zwischen 1 und 100 muss kleiner, oder gleich der Konstitution der Einheit sein, damit sie überlebt.Nach den Vorrundenbeginnen sich die angreifenden Schützen zurückzuziehen. Die Verteidiger machen sich auf einen Nahkampf gefasst.Jede Kampfsequenz ziehen sich 20% der Fernkämpfer des Angreifers zurück, beginnend mit den stärksten Einheiten. Sollteder Angreifer die Schlacht verlieren (unentschiedene Schlachten gewinnen beide Seiten), werden die noch nicht geflohenen Fernkampfeinheiten überrannt. Unabhängig von der noch verbliebenen verteidigenden Armee, legen alle nicht zurückgezogenen Fernkämpfer eine Konstitutionsprobe ab um zu bestimmen, ob sie das Schlachtfeld lebend verlassen.Belagerung / MauerschadenAußerdem wird jetzt die Beschädigung der Mauer durch Katapulte etc. berechnet. Diese wirkt sich also nicht auf den aktuellen Kampf aus, da die Fernkämpfer schon geschossen haben. Beim nächsten Kampf allerdings (falls die Mauer nicht repariert wird) schießen die Fernkämpfer dementsprechend weniger und es muss auch weniger Schlagkraft aufgebracht werden.Der Mauerschaden wird wie folgt errechnet: Zuerst wird der Schaden ermittel die eine Belagerungswaffe macht. Bei einem Katapult wäre das zb. 2 - 13. Hier wird als Beispiel eine 9 ermittelt. Nehmen wir an der Angreifer hat eine Mauer Stufe 5 dann wird von den 9 Schaden noch 5 abgezogen(Mauerstufe). Somit macht das Katapult 4 Schaden und die Mauer hätte statt 100% nur noch 96%. So wird das für jede Belagerungswaffe getrennt gerechnet. Das heißt zb das eine kleine Ramme die max.4 Schaden macht einer Mauer Stufe 5 nichts anhaben kann.Also die Formel lautet: Schaden der Belagerungswaffe - Mauerstufe = Schaden an der MauerDie SchlachtIn der Schlacht suchen sich alle angreifenden Einheiten (die schwächsten zuerst) per Zufall eine verteidigende Nahkampfeinheit heraus und gehen mit dieser Einheit in den Nahkampf.ZweikampfDabei wird für jeden der Kontrahenten eine Zufallszahl, zwischen dem beim Kampfwert angegebenen Wert der Einheit, ermittelt. Dieser Ermittelte Wert wird um 10% pro Stufe der Forschung Schmiedekunst erhöht. Anschließend wird der Rüstungswert des Gegners, ebenfalls um 10% pro Schmiedekunststufe des Gegners erhöht, von dem Ergebnis abgezogen. Um den endgültigen Kampfwert zu erhalten wird nun noch die bisher in der Schlacht erlittene Erschöpfung der Einheit vom Wert subtrahiert.Die Einheit mit dem höheren Ergebnis gewinnt den Zweikampf, erleidet aber 2 Punkte Erschöpfung. Die Einheit die verliert muss, wie beim Fernkampf eine Konstitutionsprobe bestehen um die Schlacht zu überleben. Sie scheidet aber in jedem Fall aus der Schlacht aus.Haben beide am Zweikampf beteiligten Einheiten den selben ermittelten Kampfwert, gelten beide Einheiten als Verlierer, scheiden aus und müssen eine Konstitutionsprobe bestehen um zu überleben.Die Schlacht ist beendet, wenn entweder alle angreifenden Nahkampfeinheiten ausgeschieden sind, alle Einheiten des Verteidigers (Fern- und Nahkampfeinheiten) besiegt wurden, oder nach 10 Sequenzen kein Gewinner feststeht.


==============================================================================
3  HANDBUCH 2009 - Kampfstellen im Wortlaut (Zeilen der Textfassung)
==============================================================================

Vorrunde
Bevor eine Schlacht beginnt müssen die Angreifenden Truppen die Verteidigungsanlagen der 
anzugreifenden Siedlung überwinden. Dies wird folgendermaßen gehandhabt:
Es wird ermittelt, ob der Angreifer mit seiner Armee den feindlichen Verteidigungswall 
überwinden kann. Dazu wird die Schlagkraft aller angreifenden Fußtruppen zusammengezählt. 
Diese Gesamtschlagkraft muss höher oder gleich dem Schwellenwert des entsprechenden 
Verteidigungswalls sein. Ab der verstärkten Palisade ist zudem eine gewisse Schlagkraft von 
Belagerungswaffen aufzubringen. Reicht die gesamte Schlagkraft des Angreifers nicht aus, um 
den Wall zu überwinden, ziehen sich die Truppen unverrichteter Dinge zurück. Der Kampf gilt 
dann als unentschieden.
Schwellenwerte der Verteidigungsanlagen:
Verteidigungswall 
(Ausbaustufe)
Schwellenwert
Fußtruppen
Schwellenwert 
Belagerungswaffen
Erdwall (1)
10
-
Steinwall (2)
40
-
Kleine Palisade (3)
90
-
Palisade (4)
160
-
Verstärkte Palisade (5)
250
500
Mauer (6)
360
600
Verstärkte Mauer (7)
490
700
Festungsmauer (8)
640
800
Verstärkte Festungsmauer (9)
810
900
Bollwerk (10)
1000
1000
Einige Belagerungswaffen richten Schaden an der Mauer an. Bei einer beschädigten Mauer 
müssen prozentual weniger Schlagkraftpunkte aufgebracht werden.
Ein Beispiel: 
Eine verstärkte Mauer deren Zustand nur noch 50% beträgt, kann mit 245 Schlagkraftpunkten 
von Fußtruppen und 350 Schlagkraftpunkten von Belagerungswaffen erstürmt werden. Also 
jeweils 50% der Schlagkraft, die normalerweise aufgebracht werden muss.
Der Schaden wird durch den Schaden der Belagerungswaffe (siehe Einheitentabelle) und der 
Ausbaustufe der Mauer ermittelt. Der Schaden wird durch Zufall bestimmt und die Ausbaustufe 
danach abgezogen. Bleibt ein positiver Wert übrig, wird er von dem Zustand der Mauer 
abgezogen.
Ein Beispiel: 
Ein Katapult (Schaden: 2-13) wird bei einem Angriff auf eine Mauer (Zustand 100%, 
Seite 21


===== Seite 22 =====
Ausbaustufe 6) mitgeführt. Bei dem Schaden wird eine 8 ermittelt. Nun wird die Ausbaustufe 
davon abgezogen. Die übrig bleibenden 2 Schadenspunkte (8-6=2) werden vom Zustand der 
Mauer abgezogen. Nach dem Kampf weist sie nur noch einen Zustand von 98% auf. Der 
Schaden wird für jede, beim Angriff mitgeführte Belagerungswaffe, einzeln ermittelt. 
Ist der Verteidigungswall überwunden, beginnt die eigentliche Schlacht.
Kampfsequenzen
Eine Schlacht läuft in Kampfsequenzen ab. In jeder Kampfsequenz, kämpfen die sich 
gegenüber stehenden Einheiten miteinander. Wenn nach 10 Kampfsequenzen noch kein Sieger 
feststeht, geht die Schlacht unentschieden aus. Der Angreifer zieht sich in dem Fall ohne Beute 
zurück.
Eine Kampfsequenz läuft folgendermaßen ab:
Zuerst schießen alle angreifenden Fernkämpfer (sofern vorhanden) auf die Fußtruppen des 
Verteidigers. Sind keine Fußtruppen des Verteidigers vorhanden werden die Verteidigenden 
Fernkampfeinheiten aufs Korn genommen.  
Gleichzeitig schießen die Verteidigenden Fernkampfeinheiten auf die Fußtruppen des 
Angreifers. Auch hier werden, falls der Angreifer keine Fußtruppen mehr hat, seine 
Fernkampfeinheiten beschossen.
(Gleichzeitig bedeutet, das Verteidiger und Angreifer ZUERST feuern und ANSCHLIEßEND die 
Verluste auf beiden Seiten berechnet werden).
Als nächstes stürmen die angreifenden Nahkampfeinheiten nacheinander zu einer zufälligen 
verteidigenden Nahkampfeinheit. Sind keine verteidigenden Nahkampfeinheiten mehr übrig 
werden die verteidigenden Fernkampfeinheiten angegriffen. Die beiden Einheiten kämpfen 
solange, bis eine der beiden tot ist, oder flieht. Die erlittenen Lebensenergieverluste des 
Siegers werden mit in die nächste Kampfsequenz übernommen. Nach alle angreifenden 
Einheiten gekämpft haben, beginnt die nächste Kampfsequenz. Die Schlacht ist vorbei, 
sobald eine der beiden Armeen keine Nahkampfeinheiten mehr hat, oder 10 Kampfsequenzen 
vorüber sind.
Zweikampf
Der Zweikampf zweier Einheiten läuft in Kampfrunden ab. Die Einheit mit dem höchsten 
Mutwert beginnt mit der ersten Runde ihren Angriff. Sind die Mutwerte der Einheiten gleich, 
beginnt die Verteidigende Einheit. Anschließend ist die jeweils andere Einheit mit Angreifen an 
der Reihe.
Der Angreifer hat, je nach Einheitentyp, eine bestimmte Chance den Gegner zu treffen. Es wird 
eine Zahl zwischen 1 und 100 ermittelt. Ist der ermittelte Wert kleiner oder gleich seiner 
Angriffsfertigkeit, trifft er den Gegner, ansonsten verfehlt er ihn und der Verteidiger ist an der 
Reihe mit Angreifen.
Wird der Verteidiger getroffen, wird anhand seiner Verteidigungsfertigkeit ermittelt, ob er den 
Schlag abwehren kann. Schafft er es, den Schlag abzuwehren, erleidet er keinerlei Schaden 
und ist seinerseits mit Angreifen an der Reihe.
Schafft der Verteidiger es nicht einen Schlag zu parieren, werden die Schadenspunkte, die der 
Angreifer verursacht, ermittelt und von der Lebensenergie des Verteidigers abgezogen. Die 
Schadenspunkte werden zufällig, innerhalb bestimmter Grenzen, ermittelt und sind bei der 
Entsprechenden Einheit vermerkt, z.B. 1-6 oder 2-8. (Siehe Einheitentabelle) 
Von den ermittelten Schadenspunkten wird der Rüstungswert des Verteidigers abgezogen. 
Sinken die Schadenspunkte dadurch auf 0 oder darunter, erleidet der getroffene trotzdem 
Seite 22


===== Seite 23 =====
einen Schadenspunkt. Der Schaden wird von den Lebenspunkten der Einheit abgezogen.
Sinkt die Lebensenergie einer Einheit unter 1, stirbt sie. Sinkt die Lebensenergie unter 5, wird 
anhand ihres Mut-Wertes entschieden, ob sie weiterhin im Kampf geschehen bleibt, oder 
Flieht. Geflohene Einheiten stehen dem Angreifenden/Verteidigenden Spieler nach der Schlacht 
wieder zur Verfügung, Tote Einheiten werden nach der Schlacht gelöscht. Je geringer der 
Mutwert der Einheit, desto höher die Wahrscheinlichkeit, das sie flieht.
Erschöpfung
Der Sieger eines Zweikampfes, wird durch den anstrengenden Kampf müde. Seine Angriffs- 
und Abwehrfähigkeit sinkt bis zum Ende der Schlacht um einen Punkt, bei mehreren 
Zweikämpfen summiert sich die Erschöpfung natürlich.
So ist es möglich, auch starke Einheiten mir der entsprechenden Übermacht an schwachen 
Einheiten, zu besiegen.
Ausgang der Schlacht
Sind alle verteidigenden Einheiten tot oder geflohen gewinnt der Angreifer die Schlacht. Falls 
er Transportkarren in seiner Angriffstruppe mitführt, beginnen diese die Siedlung zu plündern. 
Sind alle angreifenden Fußtruppen tot oder geflohen, gewinnt der Verteidiger die Schlacht.
Der Verlierer verliert einen Teil seiner stationierten bzw. mitgeschickten Karren und 
Belagerungswaffen. Wie viele, hängt von der Dauer der Schlacht ab. Jede Einheit hat eine 
Fluchtchance von 40%. Jede Kampfsequenz, die die Schlacht dauert erhöht sich diese Chance 
um 5%. 
Geht die Schlacht unentschieden aus, bleiben alle Karren und Belagerungswaffen erhalten.


==============================================================================
4  AKTIVER CODE - Profile und Ablauf (Auszug src/kampf.py)
==============================================================================

STAND = "2026-10-28.GPT-NE01.wissenswertes"

# (Konstitution %, Kampfwert-Min, Kampfwert-Max, Rüstung, Fernkampfchance %, 
#  Erschöpfung durch Treffer, Schwelle zur Kampfunfähigkeit)
# Basis aus 'Das Kampfsystem.odt'; Kampfwert-Spannen nach dem neueren
# 'WeitereWerteKampfsystem.odt' (Tabelle Einheitenwerte, S. 5/6).
# Konflikt Handbuch 2009 (LE/AT/PA) gegen dieses Forum-Original: Registerpunkt 40 in
# docs/PRUEFREGEL_ORIGINAL.md und docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md §3.1.
# (Der frueher hier genannte Ort docs/GPT_NE01_*.md existiert nicht - geprueft 31.10.2026.)
PROFILE = {
    "Bürgerwehr": (5, 1, 12, 0, None, 0, 1),
    "Kämpfer": (15, 4, 22, 2, None, 0, 3),
    "Krieger": (25, 7, 29, 4, None, 0, 5),
    "Ritter": (50, 9, 43, 8, None, 0, 7),
    "Paladin": (70, 17, 57, 12, None, 0, 9),
    "Kurzbogenschütze": (15, 1, 12, 0, 20, 1, 1),
    "Bogenschütze": (25, 1, 12, 0, 30, 2, 2),
    "Langbogenschütze": (35, 1, 12, 0, 55, 3, 3),
    "Armbrustschütze": (45, 3, 14, 2, 70, 4, 4),
    "Streuner": (5, 2, 15, 0, None, 0, 1),
    "Gauner": (15, 2, 20, 0, None, 0, 2),
    "Dieb": (25, 2, 25, 0, None, 0, 3),
    "Meisterdieb": (35, 2, 30, 0, None, 0, 4),
    "Kundschafter": (45, 4, 37, 2, None, 0, 5),
    "Waldläufer": (55, 6, 44, 4, None, 0, 6),
}


def _einheiten(aufstellung: Optional[dict], seite: str) -> list:
    result = []
    for name, anzahl in (aufstellung or {}).items():
        if name not in PROFILE:
            continue  # Karren/Belagerung sind keine Kämpfer
        try:
            n = int(anzahl)
        except (ValueError, TypeError, OverflowError):
            continue
        if n <= 0:
            continue
        kon, lo, hi, ruestung, fern, schaden, schwelle = PROFILE[name]
        for _ in range(n):
            result.append({"name": name, "seite": seite, "kon": kon, "lo": lo,
                           "hi": hi, "ruestung": ruestung, "fern": fern,
                           "fern_schaden": schaden, "schwelle": schwelle,
                           "erschoepfung": 0, "tot": False, "inaktiv": False,
                           "rueckzug": False})
    return result

[...]

        return fertig("unentschieden")

    # Wallvoraussetzung vor der Schlacht; SK und Intervalle bleiben Originaldaten.
    if stufe:
        wall = spieldaten.wallstufen()[stufe - 1]
        # Neu gefundenes Originalforum: die Fußtruppen-Schwelle wird von
        # NAHKAMPFeinheiten überwunden. Fernkämpfer zählen nicht dazu;
        # sonst könnten reine Bogenschützen ohne Sturmtruppen Wall 1 öffnen.
        foot_sk = sum(E.schlagkraft(u["name"]) for u in _nah(A))
        siege_sk = sum(E.schlagkraft(n) * int(k) for n, k in belagerung.items())
        faktor = zustand / 100.0
        if foot_sk < float(wall["schwellenwert_fussttruppen"]) * faktor:
            logs.append("Fußtruppen: Schwelle nicht erreicht; die Truppen ziehen sich zurueck; kein Kampf")
            return fertig("unentschieden")
        schwelle_bel = wall.get("schwellenwert_belagerungswaffen")
        if schwelle_bel is not None and siege_sk < float(schwelle_bel) * faktor:
            logs.append("Belagerungs-Schlagkraft zu gering: Schwelle nicht erreicht; die Truppen ziehen sich zurueck; kein Kampf")
            return fertig("unentschieden")

    result["vorrunde_bestanden"] = True
    result["kampf_stattgefunden"] = True


==============================================================================
5  BEUTE IM CODE HEUTE (src/kampfbericht.py Z. 200-243)
==============================================================================

# ------------------------------------------------------------------------------ 3. Beute

def beute(einheiten_des_siegers: Dict[str, int],
          vorraete: Dict[str, float],
          rng: Optional[random.Random] = None) -> Dict[str, int]:
    """Was die Karren des Siegers tragen koennen (Handbuch Seite 22/23).

    Nur Transporteinheiten (Karren) tragen; Belagerungswaffen und Kaempfer tragen nichts.
    Die Beute ist ehrlich begrenzt: sie ueberschreitet weder die Gesamtkapazitaet der Karren
    noch den vorhandenen Vorrat je Rohstoff.

    ANNAHME zur Verteilung: Das Handbuch begrenzt die Beute auf die Karrenladung, nennt aber
    keine Aufteilung auf die Rohstoffe. Hier wird anteilig nach Vorratsmenge verladen
    (dieselbe Regel wie in `kampf.py.ergebnis['beute']`). `rng` wird angenommen, aber nicht
    gebraucht - die Aufteilung ist bewusst nachvollziehbar und nicht zufaellig.
    """
    del rng  # bewusst ungenutzt: die Verteilung ist nicht im Handbuch geregelt -> anteilig

    kapazitaet = 0
    for name, anzahl in (einheiten_des_siegers or {}).items():
        kapazitaet += E.kapazitaet(name, max(0, _als_int(anzahl)))

    vorhanden: Dict[str, int] = {}
    for stoff, menge in (vorraete or {}).items():
        m = int(max(0.0, _als_zahl(menge)))
        if m > 0:
            vorhanden[stoff] = m

    gesamt = sum(vorhanden.values())
    if kapazitaet <= 0 or gesamt <= 0:
        return {}

    genommen: Dict[str, int] = {}
    restplatz = kapazitaet
    for stoff in sorted(vorhanden):
        if restplatz <= 0:
            break
        anteil = vorhanden[stoff] / gesamt
        nimm = min(int(anteil * kapazitaet), vorhanden[stoff], restplatz)
        if nimm > 0:
            genommen[stoff] = nimm
            restplatz -= nimm
    return genommen


==============================================================================
6  WALLSCHWELLEN, PUNKTE, FREISCHALTUNG (Projektauswertung)
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
