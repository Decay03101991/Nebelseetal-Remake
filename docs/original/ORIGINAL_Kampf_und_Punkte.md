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
