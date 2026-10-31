# AUFTRAG: Externe Gegenprüfung des „Nebelseetal-Remake“

**Für:** ein externes KI-Modell mit Internetzugriff (ChatGPT), das die Dateien über die unten
stehenden GitHub-Pfade selbst öffnet. Kein lokaler Zugriff nötig, keine Dateien anzuhängen
(außer den zwei Dokumenten, die in Abschnitt 4 im Volltext stehen).
**Von:** Daniel Kössl · **Erstellt:** 31.10.2026 · **Sprache der Antwort:** Deutsch

---

## 0. Worum es geht

Ein deutsches Browsergame von 2005/2009 („Nebelseetal Online“) wird als **Einzelspieler-Spiel**
in Python/tkinter neu gebaut, spielbar gegen Bots, mit Spieluhr ×180. Deine Aufgabe ist **nicht**,
Code zu verbessern, sondern **Originaltreue zu prüfen**: Wo weicht das Remake von den
Originalquellen ab, wo wird eine Regel erfunden, wo fehlt eine belegte Mechanik — und wo sind die
belegten Zahlen bei Spieluhr ×180 unspielbar. Du bist die **zweite, unabhängige Meinung**; ein
anderes Modell hat dieselben Quellen schon einmal geprüft, und du sollst nicht abnicken, sondern
widersprechen, wo es etwas zu widersprechen gibt.

## 1. Die Regeln, nach denen das Projekt arbeitet (daran misst du es)

1. **NEUESTE FASSUNG IST DAS ORIGINAL.** Gibt es zu einer Mechanik zwei Fassungen, gilt die neuere.
   **ABER:** Nennt die neuere Fassung nur **Werte** und beschreibt die ältere Fassung die
   **Mechanik**, dann gilt **Mechanik aus der älteren, Zahlen aus der neueren** Fassung. Das ist eine
   begründete Zusammenführung, keine Erfindung — kennzeichne sie als `ZUSAMMENFÜHRUNG` und nenne
   beide Quellen mit Stelle.
2. **Was die Quellen nicht hergeben, ist VORSCHLAG** und muss als VORSCHLAG erkennbar sein. Es wird
   nichts erfunden und nichts „geschätzt, bis es passt“.
3. **Daniels eigene frühere Annahmen sind verwerfbar**, wenn die Quellen etwas anderes vorgeben
   (Beispiel: ein Sieg bei 300 Gesamtpunkten ist bereits **verworfen**, weil das Handbuch ausdrücklich
   sagt: „Jeder hat bei Nebelseetal sicher seine eigenen Ziele“).
4. **Einzelspieler statt Mehrspieler:** Das Original war ein Browsergame mit vielen Spielern; hier
   spielt **ein Mensch gegen wenige Bots**. Wo eine Regel nur wegen vieler Spieler existiert (z. B.
   20 Dimensionen als Platz für hunderte Welten), darf sie für den Einzelspieler **neu gedeutet**
   werden — aber so, dass sie Sinn ergibt und die Originalmechanik erkennbar bleibt.
5. **Belegpflicht:** jede Behauptung mit Datei **und** Zeile (bzw. Seite). Kannst du etwas nicht
   belegen, schreibst du „nicht belegbar“ — das ist ein vollwertiges Ergebnis.
6. **Einmal prüfen, festschreiben:** Abschnitt 5 listet 41 bereits belegte Punkte. Prüfe sie nicht
   erneut, außer du findest einen echten Widerspruch — dann sag es ausdrücklich.

## 1a. Was hier ABSICHTLICH FEHLT (wichtig für deine Antwort)

Dieser Auftrag ist **blind** gestellt: Wir halten absichtlich zurück,

* **welche Entscheidungen der Spieleigner schon getroffen hat** (Reiseformel, Dimensionen, Beute,
  Siegbedingung, Geschichte) — damit du unabhängig zu eigenen Vorschlägen kommst,
* **welche Widersprüche wir im Projekt bereits gefunden haben** und wie wir sie bewertet haben,
* **die Liste der rund 45 Punkte, die intern schon gegen die Quellen geprüft und festgeschrieben
  sind** (nur die Zahl steht unten, nicht der Inhalt),
* unsere Prioritäten und unseren Zeitplan.

**Konsequenz für dich:** Du sollst nicht bestätigen, sondern **eigene Wege zeigen**. Wo du auf
etwas stößt, das wir offenbar anders gelöst haben, ist genau das der interessante Fall — sag es
ausdrücklich, mit Quelle.

## 2. Stand der Veröffentlichung (wichtig für deine Zitate)

* Öffentlich auf GitHub ist ein **Stand, der laufend nachgezogen wird** (zuletzt: die Nacht vom
  30./31.10.2026). Prüfe deshalb **immer den neuesten Commit** im Repo (`main`) und nenne in deiner
  Antwort den Commit-Stand, den du gelesen hast. Alle Pfade in Abschnitt 3 sind am 31.10.2026
  geprüft und abrufbar.
* **Noch nicht veröffentlicht** (liegen nur lokal, Abschnitt 3.2): das Prüfregister, die
  Abweichungsdatei 2006/2009, zwei Entwürfe und zwei Prüfberichte. Das Prüfregister ist in
  Abschnitt 5 als Kurzliste enthalten; die anderen Papiere kannst du nicht lesen — bewerte sie
  nicht, sondern nenne sie „nicht einsehbar“, wenn eine Frage dorthin führt.
* Das Projekt selbst hat seit dem 28.10. weitergearbeitet (Menüs, Sperrmeldungen, Punkteleiste).
  Wenn du eine Stelle im Code nicht findest, liegt es daran — nicht an dir.

---

## 3. Die Dateien

### 3.1 Öffentlich (GitHub, Rohdateien)

Alle Adressen haben die Form `https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/<pfad>`.
Öffne sie **direkt als Text**, nicht über die GitHub-Oberfläche.

| Datei | Was darin steht |
|---|---|

| `docs/original/Spielanleitung_2009_Textfassung.txt` | **Die Hauptquelle:** Spielanleitung 2009 im Volltext, 1.366 Zeilen mit Seitenmarken. Zitate im Projekt nennen „Z. 1216“ = Zeile in DIESER Datei. |
| `docs/original/ORIGINAL_Kampf_und_Punkte.md` | Auswertung der Handbuchseiten 4/5 und 18–23 (Auftragsarten, Kampf, Punkte, Götterschutz). |
| `docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md` | Auswertung: Einheiten, Waren, Rohstoffe, Gebäude, Forschung. |
| `docs/original/ORIGINAL_Werte_Einheiten.md` | Einheitenwerte (LE/AT/PA/RS/TP/GS/MU/SK) aus dem Handbuch. |
| `docs/original/Spielanleitung_2005/portal.php.txt` | Vorversion 2006: Portal, Limbus, 20 Dimensionen, 20×20, 5.000 Mana, 24 h. |
| `docs/original/Spielanleitung_2005/rohstoffe.php.txt` | Vorversion 2006: Rohstofftabelle (weicht teils vom Handbuch ab). |
| `docs/original/Spielanleitung_2005/einheiten.php.txt` | Vorversion 2006: Einheiten, Ausbildungsdauer, Herstellerregel. |
| `docs/original/Spielanleitung_2005/punktesystem.php.txt` | Vorversion 2006: Punkte je Einheit und Gesamtpunktzahl. |
| `docs/original/Spielanleitung_2005/warentabelle.php.txt` | Vorversion 2006: Warenvoraussetzungen (vollständig nur dort). |
| `docs/original/Spielanleitung_2005/forschungstabelle.php.txt` | Vorversion 2006: Forschungstabelle. |
| `docs/original/Spielanleitung_2005/siedeln.php.txt` | Vorversion 2006: Siedlungen gründen, Siedlergrenze. |
| `docs/AKTUELLER_STAND.md` | Selbstauskunft des Projekts: was gebaut ist, was offen ist (Stand 28.–30.10.). |
| `docs/ENTWICKLUNGSPROTOKOLL.md` | Entwicklungsprotokoll mit Kennungen, Prüfzahlen und Kosten (das EINE Protokoll). |
| `data/buildings.json` | 20 Gebäude: Kategorien, Baupreise je Stufe, Voraussetzungen, Erträge, Wallschwellen. |
| `data/units.json` | 28 Einheiten mit allen Originalwerten, Kriegspunkten, Ladung, Gebäude, Voraussetzung. |
| `data/research.json` | 21 Forschungen mit Wirkungstext und Kosten (Handbuch 2009, Abweichungen zur Vorversion). |
| `data/resources.json` | 9 Rohstoffe, Erträge je Stunde, Startwerte, Siedlergrenze. |
| `data/gelaende.json` | Geländearten, Bebaubarkeit, Erträge je Gelände. |
| `data/warenrezepte.json` | Waren: Kosten, Dauer, Forschungsvoraussetzungen. |
| `data/gebaeude_wirkung.json` | Wirkungen der Gebäude (Siedlergrenze, Forschung, Ausbildung, Verteidigung). |
| `data/spielzeit.json` | Spieluhr: Faktor 180 (1 echte Sekunde = 180 Spielsekunden). |
| `src/kampf.py` | AKTIVES Kampfsystem (neueres Original-Forumssystem, 15 Profile, Wallvorrunde, Sequenzen). |
| `src/kampfbericht.py` | Wallvorrunde, Mauerschaden, Beute, Kampfbericht. |
| `src/auftraege.py` | Aufträge: Reisezeit, Rückkehr, Ladung, Auftragsarten, offene Lücken. |
| `src/punkte.py` | Punkte: Kriegspunkte je Einheit + Wallstufe³, Gesamt = (Krieg+Forschung)/2, Zielzahl 300 (VORSCHLAG). |
| `src/forschung.py` | Forschung: Dauer = neue Stufe² in Stunden, Kostenverdopplung, Siedlungssperre. |
| `src/wirtschaft.py` | Produktion: Erträge, Forschungsboni, Verbrauch. |
| `src/main.py` | Spielschicht und Oberfläche (7.139 Zeilen; für gezielte Fragen, nicht komplett lesen). |
| `docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md` | **Original-Hintergrundgeschichte** des Spiels (Website-Archiv 11.09.2007, drei Teile): drei Drachenbrueder, Erschaffung des Nebelseetals, Salmurs Magie, das Chaos. Grundlage der Legende. |
| `Vorausarbeit gpt chat/Fehlerregister_Nebelseetal.md` | Bekannte Fehler und Designprüfungen (u. a. Sieggrenze 300 gegen Originalpunkte). |

### 3.2 Nur lokal vorhanden (nicht abrufbar — nur zur Kenntnis)


| Datei | Was darin steht |
|---|---|

| `docs/PRUEFREGEL_ORIGINAL.md` | **Prüfregister mit 40 belegten Punkten** (Seite/Zeile je Punkt). In diesem Auftrag als Kurzliste in Abschnitt 5 enthalten, damit nichts doppelt geprüft wird. |
| `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` | Alle messbaren Abweichungen Vorversion 2006 gegen Handbuch 2009, mit Regel „Balance 2009, Struktur beide“. |
| `docs/original/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md` | Handbuch S. 9–14: Freischaltung über Forschungsstufen, Dauer Stufe², Kostenverdopplung, Ertragstabelle. |
| `docs/ENTWURF_WEGZEIT_KAMPF_WELT_20261031.md` | Entwurf des starken Modells für Wegzeit, Kampfablauf, Weltlage (195 Zeilen) — VORSCHLAG, teils widerlegt. |
| `docs/ENTWURF_AUSBILDUNG_HERSTELLER_20261030.md` | Entwurf Ausbildung und Hersteller (311 Zeilen) — VORSCHLAG. |
| `docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md` | Prüfbericht dieses Entwurfs gegen Handbuch und Code (6 falsche Aussagen belegt, Entscheidungen E1–E5). |
| `docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md` | Landkarte der ZWEI Bewegungssysteme im Code (zwei Formeln, zwei Beuteregeln). |


---

## 4. Drei Originaldokumente im Volltext

Die ersten beiden liegen im Projekt nur als `.odt` vor (ChatGPT kann das Format nicht lesen). Deshalb
stehen sie hier wörtlich. **Sie sind eine Originalquelle und widersprechen dem Handbuch in mehreren
Punkten** — genau das ist eine deiner Fragen (Aufgabe A). Das dritte ist die Original-Geschichte.

### 4.1 „Das Kampfsystem“ (neueres Original-Forumssystem, Spielerfund)

```text
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
```

### 4.2 „Wissenswertes“ (Punktesystem, Rohstoffproduktion, Einheitenwerte)

```text
Wissenswertes
Punktesystem         Rohstoffproduktion/Gebäude         Einheitenwerte     
Hier werde ich einiges Aufschreiben wovon ich denke das es wichtig zu wissen ist. Diverse Auflistungen etc.Diese Dinge muss man sich dann nicht umständlich im Forum suchen oder in der veralteten Anleitung nachlesen. Hier seit ihr sicher das es auf dem aktuellen Stand ist. Außerdem könnt ihr euch hier eine Liste runterladen in der alle Werte übersichtlich draufstehen:
- Tabelle aller Gebäude, Forschungen, Einheiten etc. mit Kosten
 

PunktesystemUm in der Ruhmeshalle, in der alle Spieler aufgeführt werden, weit oben zu stehen, musst Du möglichst viele Gesamtpunkte erreichen. In Nebelseetal-Online gibt es zwei verschiedene Arten von Punkten:ForschungspunkteDiese Punkte geben Deinen aktuellen Forschungsstand an. Für jede Forschung die Du erlangt hast, wird die Forschungsstufe hoch drei genommen. Die so gewonnenen Werte, werden anschließend addiert und ergeben Deine Forschungspunkteanzahl.Ein Beispiel:Felderwirtschaft Stufe 1 = 1 Punkt (1*1*1=1)Kriegskunst Stufe 4 = 64 Punkte (4*4*4=64)Minenarbeit Stufe 2 = 8 Punkte (2*2*2=8)Gesamtforschungspunkte = 73 (1+64+8=73)KriegspunkteFür jede Militär- und Spionageeinheit die Du ausbildest, bekommst Du Kriegspunkte. Wie viele Punkte hängt von der entsprechenden Einheit ab:
Punkte

Bürgerwehr
1

Kämpfer
2

Krieger
4

Ritter
8

Paladin
16

Kurzbogenschütze
2

Bogenschütze
4

Langbogenschütze
8

Armbrustschütze
10

Streuner
1

Gauner
2

Dieb
4

Meisterdieb
8

Kundschafter
10

Waldläufer
16

Handkarren
1

Einspänner
2

Zweispänner
3

Handelskarawane
-

gr.Handelskarawane
-

Siedlerkarren
-

Belagerungsturm
2

Ramme
3

gr.Belagerungsturm
4

gr.Ramme
5

Balliste
6

Katapult
7

gr.Katapult
8
Ein Beispiel:30 Bürgerwehr + 10 Paladine + 12 Bogenschützen = 30*1 + 10*16 + 12*4 = 238GesamtpunktzahlDie Gesamtpunktzahl besteht aus der Summe von den Kriegs- und Forschungspunkten. Das Ergebnis wird dann durch zwei geteilt. Die Gesamtpunktzahl kann man in der Ruhmeshalle sehen, die Kriegs- und Forschungspunkte kann man dort nicht erkennen, sie werden Dir nur für Deinen Account unter dem Hauptmenü angezeigt.Ein Beispiel:(150 Forschungspunkte + 200 Kriegspunkte) : 2 = 175 Gesamtpunkte
Wissenswertes
Punktesystem         Rohstoffproduktion/Gebäude         Einheitenwerte     
Hier werde ich einiges Aufschreiben wovon ich denke das es wichtig zu wissen ist. Diverse Auflistungen etc.Diese Dinge muss man sich dann nicht umständlich im Forum suchen oder in der veralteten Anleitung nachlesen. Hier seit ihr sicher das es auf dem aktuellen Stand ist. Außerdem könnt ihr euch hier eine Liste runterladen in der alle Werte übersichtlich draufstehen:
- Tabelle aller Gebäude, Forschungen, Einheiten etc. mit Kosten
 

Rohstoffproduktion und Gebäude:
Gebäude
Rohstoff
Produktion

Holzfäller
Holz
Wald (4), Steppe (2)

Steinmetz
Stein
Berg (4), Hügel (2)

Jäger
Nahrung und Leder
Wald (2 Nahrung, 2 Leder), Steppe(1 Nahrung, 1 Leder)

Farm
Nahrung
Grasland (4), Steppe (2)

Pferdezucht
Pferde
Grasland (3), Steppe (1,5)

Rinderfarm
Leder und Nahrung
Grasland (3Leder, 1 Nahrung), Steppe (1,5 Leder, 0,5 Nahrung)

Schafszucht
Wolle
Grasland (3), Steppe (1,5)

Erzmine
Metall
Berg (3), Hügel (1,5)

Goldmine
Gold
Berg (3), Hügel (1,5)

Tempel
Mana
Nebelsee (8), alle außer Sumpf (2)
Jedes Gebäude produziert auf 2 verschiedenen Geländearten unterschiedliche Mengen an Rohstoffen. Wie viele Ressourcen pro Stunde produziert werden, kannst Du aus der Tabelle oben entnehmen. Der Wert in Klammern gibt die Produktionsmenge pro Stunde an. Sümpfe sind unbebaubar und somit für Eure Siedlungen völlig wertlos. Deine Siedlung bekommt, außer den Rohstoffen, noch einen neuen Siedler pro Stunde, bis ihre Siedlergrenze erreicht ist. Diese Grenze liegt in jeder neuen Siedlung bei 5 Siedlern. Wenn Du in Deiner Siedlung Häuser errichtest, erhöht sich der Grenzwert um 5 Siedler pro Haus. Wann Du den nächsten Siedler bekommst, kannst Du in der Siedlungsübersicht, unter der Rohstoffzuwachstabelle sehen.Zu der o.g. Produktion wird dann noch der Forschungsbonus gerechnet. Beachtet das sich die Produktion eines Jägers nicht durch Forschung beeinflussen läßt! Keine Forschung erhöht die Produktion des Jägers! Er ist also nur am Anfang interessant.Genauso verhält es sich mit der Nahrungsproduktion der Rinderfarmen. Diese wird niemals durch Forschung beeinflusst. Sie sind also niemals eine Alternative zu den Farmen, falls man denkt diese nicht zu benötigen.
Wissenswertes
Punktesystem         Rohstoffproduktion/Gebäude         Einheitenwerte     
Hier werde ich einiges Aufschreiben wovon ich denke das es wichtig zu wissen ist. Diverse Auflistungen etc.Diese Dinge muss man sich dann nicht umständlich im Forum suchen oder in der veralteten Anleitung nachlesen. Hier seit ihr sicher das es auf dem aktuellen Stand ist. Außerdem könnt ihr euch hier eine Liste runterladen in der alle Werte übersichtlich draufstehen:
- Tabelle aller Gebäude, Forschungen, Einheiten etc. mit Kosten
 

Einheitenwerte
Kostitution
Kampfwert
Rüstung
Fernkampf
Erschöpfung
Geschwindigkeit(GS)
Schlagkraft(SK)

Bürgerwehr
5,00%
1 – 12
0
-
1
5
1

Kämpfer
15,00%
4 – 22
2
-
3
10
2

Krieger
25,00%
7 – 29
4
-
5
25
3

Ritter
50,00%
9 – 43
8
-
7
20
4

Paladin
70,00%
17 – 57
12
-
9
20
5

Streuner
5,00%
2 – 15
0
-
1
10
2

Gauner
15,00%
2 – 20
0
-
2
15
3

Dieb
25,00%
2 – 25
0
-
3
20
5

Meisterdieb
35,00%
2 – 30
0
-
4
25
7

Kundschafter
45,00%
4 – 37
2
-
5
30
9

Waldläufer
55,00%
6 – 44
4
-
6
35
11

Kurzbogenschütze
15,00%
1 – 12
0
20,00%
1, auch Erschöpfungsschaden
5
1

Bogenschütze
25,00%
1 – 12
0
30,00%
2, auch Erschöpfungsschaden
5
2

Langbogenschütze
35,00%
1 – 12
0
55,00%
3, auch Erschöpfungsschaden
5
4

Armbrustschütze
45,00%
3 – 14
2
70,00%
4, auch Erschöpfungsschaden
5
5
Schützt soviele Einheiten vor Fernkämpfern (-30% Angriff)
Mauerschaden

Belagerungsturm
10
0
15
35

Ramme
0 – 4
15
25

gr.Belagerungsturm
30
0
15
45

gr.Ramme
0 – 8
15
35

Balliste
1 – 10
15
25

Katapult
2 – 13
15
45

gr.Katapult
5 – 18
15
55

Handkarren
10

Einspänner
25

Zweispänner
30

Handelskarawane
25

gr.Handelskarawane
30

Siedlerkarren
20
Zu den oben genannten Werten wird noch der Bonus durch Forschungen wie Waffentechnik und Bogenbau dazugerechnet.
```

### 4.3 Die Original-Hintergrundgeschichte des Spiels (Website, Capture 11.09.2007)

**Das ist die Grundlage für die Legende (Aufgabe D).** Drei Drachenbrüder, die Erschaffung des
Nebelseetals, Salmurs Magiegeschenk und das daraus folgende Chaos. Wörtlich aus dem Website-Archiv.

```text
# Original-Hintergrundgeschichte (Website-Archiv, 11.09.2007)

**Warum diese Datei:** Daniel (31.10.2026): „Die Geschichte soll trotzdem möglichst aus originalen
Spieldaten kommen. Überall stehen kleine Texte … vielleicht findest du was in der Spielanleitung, das
sich zu einer Geschichte ausarbeiten lässt und das Interesse und die Aufmerksamkeit von Spielern halten
kann."

Kleine Fundstellen, die sich zu einer Geschichte ausarbeiten lassen, gibt es — aber nicht in der
Spielanleitung (die ist ein technisches Handbuch). Die **Hintergrundgeschichte des Spiels** steht auf
der alten Website, archiviert bei web.archive.org (Capture **11.09.2007**), in **drei Teilen**.

**Regel für jede Weiterarbeit:** dieser Text ist ORIGINAL — er wird wörtlich zitiert, nicht umgedichtet.
Neue Erzählteile werden daneben gestellt und als NEU gekennzeichnet. Nichts wird stillschweigend
verändert.

**Rohdateien:** `docs/original/website/hintergrundgeschichte.php`, `…geschichte2.php`, `…geschichte3.php`

---

## Teil 1 — Die Götter und das Nebelseetal

*Quelle: `docs/original/website/hintergrundgeschichte.php` (web.archive.org, 11.09.2007)*

Epheus der Weiße, Herr des Wachstums und der Heilung

Tardas der Grüne, Herr der Maßlosigkeit und der List

Salmur der Rote, Herr des Hasses und der Furcht

Diese drei Brüder, göttliche Drachenwesen mit Fähigkeiten jenseits der Vorstellung schufen vor Äonen von Zeiten das Nebelseetal.

Eine friedliche Welt in der viele Menschenvölker miteinander Handel trieben und ihre Schöpfer verehrten.

Eine Zeit in der die Göttlichen selbst noch auf der Welt wandelten und sie nach ihrer Vorstellung formten bis alles perfekt war.

Doch dann, als alles getan war, gab es einen unter ihnen der Unzufrieden wurde...

Epheus erfreute sich das alles so wunderbar friedlich wuchs und gedieh.

Tardas gab sich in seinem Garten den Gelüsten, der Völlerei und des Spaßes hin.

Aber Salmur wollte mehr. Ihm reichte es nicht etwas geschaffen zu haben und sich nun daran zu ergötzen. Er wollte weiterhin die Welt gestalten und diese mitbestimmen.

Jedoch, da alles perfekt war und es nichts mehr zu verbessern gab, musste er sich eine neue Aufgabe suchen.

Und so schenkte er dem Nebelseetal die Magie. Eine mächtige Kraft, die bisher nur den Göttlichen selbst zugänglich war. Die Bewohner des Nebelseetals versuchten diese zu beherrschen, doch sie scheiterten, da ihnen die Weisheit fehlte, die magischen Kräfte zu begreifen.

Und so kam es das die Welt in ihren Grundfesten erschüttert wurde. Die magische Energie brachte Chaos, denn viele versuchten sich an ihr, aber kaum einer mochte sie zu bändigen.

---

## Teil 2 — Salmur und das Chaos

*Quelle: `docs/original/website/hintergrundgeschichte2.php` (web.archive.org, 11.09.2007)*

Zwar hatte Salmur dieses nicht gewollt, jedoch fand er langsam gefallen an dieser Entwicklung. Er ergötzte sich an dem Chaos im Nebelseetal. Kriege zerrütteten das Land und durch die Magie wurden ganze Kontinente verwüstet.

Epheus weinte als er dieses sah, jedoch konnte er der Magie die durch Salmur entfaltet wurde keinen Einhalt gebieten.

Tardas weilte derweil immer noch in seiner Abgeschiedenheit und hatte sich gänzlich seinen Wohlergehen hingegeben. Er bekam von alledem nichts mit, denn Epheus vermochte ihn nicht zu finden.

Das Nebelseetal verfiel immer mehr dem Chaos und so kam es das die von den Drachen erschaffene Welt durch die magischen Ströme, welche durch Salmur entfacht worden waren, zerrissen wurde. Ganze Kontinente wurden von der Magie verschlungen, Hunderttausende starben, die Realitäten verschwammen und splitteten sich zu vielen Welten auf, welche nun, nur noch durch magische Korridore miteinander verbunden waren.

Nach tausenden von Jahren glätteten sich die magischen Ströme wieder, doch war das einstige Nebelseetal nicht mehr wieder zu erkennen.

Früher war alles eine Welt gewesen, doch nun ist alles zerrissen. Viele einzelne Welten sind entstanden, Welten auf denen sich die Überlebenden eine neue Heimat aufbauen. Auch die Bewohner haben sich verändert. Viele sind über die Jahrhunderte mit der Magie verschmolzen und haben sich zu neuen, manchmal gar seltsamen Völkern verwandelt. Menschen, Feen, Echsenwesen, Zwerge, Gnome, Elben, Orks... unzählige verschiedene Formen von Zivilisationen sind entstanden.

---

## Teil 3 — Die Ströme kommen zur Ruhe

*Quelle: `docs/original/website/hintergrundgeschichte3.php` (web.archive.org, 11.09.2007)*

Die magischen Ströme sind zur Ruhe gekommen, jedoch führen sie immer noch zu wunderlichen Dingen. Die Landschaft der Welten verändert sich ständig. Wo eben noch ein Bergmassiv aufragt, ist am nächsten Morgen vielleicht ein dichter Wald, oder ein stinkender Sumpf. Die neuen Völker lernten bald mit diesen magischen Gegebenheiten zu leben und diese sogar unterbewusst zu beeinflussen. Sobald sie sich an einem Ort versammeln um dort einen neuen Lebensraum für sich zu schaffen und zu siedeln, hören die Veränderungen in der unmittelbaren Nähe auf.

Auf jedem einzelnen Bruchstück der alten Welt, die nun im magischen Raum, dem Limbus, verstreut liegen, entstand ein magisches Portal. Eine Öffnung, zu den mystischen Korridoren, die die neuen Welten mit einender verbinden. Durch diese Durchgänge ist es den verstreuten Völkern möglich andere Welten zu besuchen, um miteinander in Kontakt zu treten...

Doch was ist aus den göttlichen Drachen geworden, welche einst die alte Welt erschufen?

Sie weilen immer noch in den Weiten des Limbus:

Salmur hat immer noch Freude sich alles anzusehen. Er nimmt es mit Wohl wollen hin das etwas neues entstanden ist, was er erschaffen hat.

Epheus jedoch weint immer noch und ab und zu fallen seine Tränen auf die Welten des Nebelseetals und lassen magische Nebelseen entstehen aus denen magische Energien strömen.

Tardas kehrte aus seiner Abgeschiedenheit zurück, um sich wieder seinen Teil an der Welt zu sichern.

Ein neues Zeitalter hat begonnen, in dem neue Herrscher sich aufmachen ihr Volk zu hoher Kultur und Macht zu führen...

```

---

## 5. Was intern schon geprüft ist

Rund 45 Punkte sind intern gegen Handbuch 2009 bzw. die 2006er Seiten geprüft und festgeschrieben.
**Die inhaltliche Liste liegt bewusst NICHT in diesem Auftrag** (siehe Abschnitt 1a): du sollst
unabhängig prüfen, nicht bestätigen. Wenn du auf einen echten Widerspruch stößt, nenne ihn mit
Quelle — wir gleichen dann ab.

(Liste absichtlich nicht enthalten - siehe Abschnitt 1a.)

---

## 6. Deine vier Aufgaben (jeweils: Optionen, nicht Bestätigung)

Für jede Aufgabe gilt: **rechne, und liefere OPTIONEN.** Zu jeder Option: Vor- und Nachteil,
Aufwand (S/M/L), Wirkung auf das Spielgefühl bei Spieluhr ×180, und ob sie einer Quelle
widerspricht. Wenn dir Information fehlt, um eine Option zu beurteilen: **sag es** — das ist ein
Ergebnis, keine Lücke im Vortrag.

### Aufgabe A — Kampf: zwei Quellen, eine Wirklichkeit

Es gibt zwei Originalquellen für den Kampf: das **Handbuch 2009** (LE, AT, PA, MU, RS, TP;
Zweikampf in Kampfrunden; Erschöpfung −1 AT/PA; Wallschwellen; Beute; Geräteverlust; Punkte) und
das **neuere Forumssystem** (Konstitution %, Kampfwert-Spanne, Rüstung, Fernkampfwert,
Erschöpfungsschaden, Schwelle zur Kampfunfähigkeit) — letzteres nennt **weder Beute noch
Geräteverlust noch Punkte**.

**Verlangt:** (1) Tabelle „Kampfschritt | gilt | Quelle | Art (belegt / Zusammenführung /
Vorschlag)“ für Wallvorrunde, Mauerschaden, Fernkampf, Nahkampf, Erschöpfung, Flucht, Ausgang,
Beute, Geräteverlust, Punkte. (2) **Drei Wege**, wie man die beiden Quellen zu EINEM System
zusammenführt — je mit Vor-/Nachteil, Aufwand und dem, was dabei verloren geht. (3) Deine
Empfehlung mit einem Satz Begründung. (4) **Wie würdest du die Beute staffeln**, wenn der erste
Angriff eine Mauer einreißt und erst spätere Angriffe wirklich ernten? Nenne Prozentwerte und die
Formel, mit der sie greifen (Eingaben: Wallzustand vor dem Kampf, überlebende Verteidiger,
Karrenladung, Ortslager).

### Aufgabe B — Wegzeit und Kosten: die fehlende Formel

Belegt: GS = Reisegeschwindigkeit; Zeitangaben gelten für **eine Strecke**, Rückkehr dauert doppelt;
Geschwindigkeit ist in 10-%-Schritten drosselbar (langsamer = weniger Gold, mehr Nahrung); Aufträge
zu fremden Siedlungen kosten zusätzlich **Mana nach Entfernung**; ein Weltwechsel kostet 5.000 Mana,
einmal je 24 h; 20 Dimensionen, je 20×20 Felder. **Eine Zahlenformel nennt keine Quelle** — die
Einheiten bringen GS-Werte von 5 bis 35 mit.

**Verlangt:** (1) **Drei Formeln zur Auswahl** (Dauer als Funktion von Distanz und GS), je mit
durchgerechneten Reisen über 6, 16 und 32 Felder für GS 5 und GS 35 — Spielstunden **und** Echtzeit
bei ×180 — plus Vor-/Nachteil. (2) Welche Formel du nimmst und warum. (3) Eine Kostentabelle
(Gold, Nahrung, Mana je Einheit und Strecke), soweit belegbar, sonst als Vorschlag. (4) Die
**Portal-Regel für ein Einzelspieler-Spiel**: wie werden aus den 20 Dimensionen sinnvolle Orte, was
ist das Portal dann noch, welche Mana-Kosten bleiben sinnvoll — zwei Varianten mit Empfehlung.

### Aufgabe C — Spielbarkeit bei ×180 und was am Ende eines Laufs steht

Das Handbuch nennt **keine Siegbedingung** („Jeder hat bei Nebelseetal sicher seine eigenen Ziele“ —
Feldherr, Forscher, Händler). Belegt sind dagegen die Raten: Produktion je Gebäude und Gelände,
1 Siedler/Stunde, Forschungsdauer = neue Stufe² in Stunden, Kriegspunkte je Einheit,
Verteidigungsanlagen = Ausbaustufe³, Gesamtpunkte = (Krieg + Forschung) / 2.

**Verlangt:** (1) Tabelle „Größe | belegter Wert | Wirkung bei ×180 (gerechnet) | Urteil (spielbar /
zäh / unspielbar)“. (2) **Drei Modelle für das Ende eines Laufs** (z. B. Auszeichnungen, Rangliste,
Auswertung nach N Spieltagen, freies Weiterspielen) mit Vor-/Nachteil und Aufwand. (3) Für dein
Lieblingsmodell: **welche Kennzahlen** werden daraus abgeleitet, und aus welchen belegten Werten
kommen sie? (4) Was dir an Information fehlt, um das zu entscheiden.

### Aufgabe D — Antrieb ohne Mitspieler und eine Geschichte aus Originaltexten

Im Mehrspieler-Spiel ist der Antrieb automatisch da: andere Spieler, mit denen man sich messen kann.
Hier spielt **ein Mensch gegen wenige Bots** — das Spiel muss den Antrieb **selbst erzeugen**. Dazu
will der Spieleigner eine kleine Geschichte/Legende als Lobpreisung des alten Browsergames; Material
dafür ist die mitgelieferte Original-Hintergrundgeschichte.

**Verlangt:** (1) Höchstens sechs Punkte „was im Original den Antrieb erzeugte“ (mit Mechanik-Bezug).
(2) **Fünf Antriebs-Quellen** für den Einzelspieler, die auf **bestehenden** Mechaniken aufsetzen —
je mit „wodurch entsteht der Vergleich/Maßstab ohne echte Mitspieler“ und Aufwand S/M/L.
(3) Wo dieser Ersatz **nicht** trägt (höchstens drei Punkte). (4) Ein **Legenden-Gerüst in höchstens
250 Wörtern**, ausschließlich aus belegten Originalbausteinen, getrennt in „belegt verwendet“ und
„neu erfunden“. (5) **Die eine Frage**, die der Spieleigner zuerst beantworten muss.

---

## 7. Ausgabeformat (halte es genau ein)

1. **Kopf, 3 Sätze:** Was du geprüft hast, wo du Übereinstimmung siehst, was dein wichtigster
   Einwand ist.
2. **Befundtabelle, höchstens 15 Zeilen:**

   | Nr | Bereich | Befund | Beleg im Remake (Datei:Zeile) | Beleg in der Quelle (Dokument + Stelle) | Urteil | Empfehlung | Aufwand |
   |---|---|---|---|---|---|---|---|

   Urteile nur aus: **WIDERSPRUCH · FEHLT · ERFUNDEN · DOPPELT · UNBELEGT · IN ORDNUNG**.
   „ERFUNDEN“ heißt: im Remake steht eine Regel oder Zahl, für die es in den Quellen keinen Beleg
   gibt und die nicht als VORSCHLAG gekennzeichnet ist. Höchstens zwei Zeilen „IN ORDNUNG“.
3. **Die drei Aufgaben A, B, C** jeweils als eigener Abschnitt mit der verlangten Tabelle/Rechnung.
4. **Was du nicht prüfen konntest:** höchstens 5 Zeilen mit Grund.
5. **Die drei wichtigsten Maßnahmen**, je ein Satz, nach Wirkung sortiert.

Kein Vorwort, kein Lob, keine Zusammenfassung des Projekts, keine Code-Verbesserungsvorschläge
außerhalb der drei Aufgaben.

---

## 8. Was du NICHT tun sollst

* keine Zeilennummern, Seitenzahlen oder Werte erfinden — im Zweifel „nicht belegbar“,
* keine Regel aus einem anderen Spiel oder aus Browsergame-Allgemeinwissen ergänzen,
* keine Punkte aus Abschnitt 5 erneut aufrollen,
* keine Dateien bewerten, die du nicht öffnen kannst (Abschnitt 3.2),
* keine Änderungen am Code verlangen, die eine Originalzahl ersetzen — erst Beleg, dann Vorschlag.

---

## 9. Was mit deiner Antwort passiert

Daniel liest sie selbst und gibt sie an die Sitzung zurück, die das Remake baut. Befunde mit
Datei:Zeile werden zu Prüfungen im Projekt (`tests/`), belegte Widersprüche zu Änderungen,
VORSCHLÄGE zu Entscheidungen, die Daniel trifft. Deine Antwort ist damit **Arbeitspapier, keine
Freigabe**: nichts wird gebaut, was nicht durch eine Quelle oder Daniels Entscheidung gedeckt ist.
