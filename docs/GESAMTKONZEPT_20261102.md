# Gesamtkonzept — Nebelseetal Remake

**Stand 02.11.2026.** Vorgabe Daniel (Konzept K-1, Abschnitt 10): Nebelseetal liefert alles Inhaltliche,
Lords Mobile ausschliesslich die Mechanik des Raums. Dieses Dokument formuliert das aus — zuerst der
Absatz, dann die Belege, dann ehrlich das, was noch fehlt. Es ist der Baustein fuer die spaetere
GitHub-Beschreibung.

Keine Zahl in diesem Dokument ist geschaetzt. Wo etwas beschlossen, aber noch nicht gebaut ist, steht
das ausdruecklich dabei.

## 1. Das Spiel in einem Absatz

Nebelseetal Remake ist ein Einzelspieler-Aufbauspiel, das zwei Vorbilder zu einem eigenen Spiel
verbindet. Alles Inhaltliche stammt aus dem Browserspiel Nebelseetal (Handbuch 2009 als Richtschnur,
die Seiten von 2005/2006 als Entwicklungsvergleich): Rohstoffe, Waren, Forschung, Gebaeude mit ihren
Funktionen, Truppen, Kampf und Beute, Dorfgruendung und die 127 Originalsiedlungskarten. Aus Lords
Mobile kommt ausschliesslich die Mechanik des Raums — das Springen auf Koordinaten und die Art, wie
Doerfer auf diesen Koordinaten liegen und angezeigt werden. Daraus entsteht eine Weltkarte, auf der man
sich bewegt, Doerfer findet, sie ausspaeht, angreift und gegebenenfalls ausraeumt, waehrend die Wirtschaft
im Hintergrund weiterlaeuft: gruenden, produzieren, forschen, ausruesten, ausbilden, bewegen, kaempfen,
punkten. Der Spieler baut gegen fuenf Bots, die dieselben Regeln benutzen — sie wirtschaften in eigenen
Doerfern, waehlen Taktiken aus ihrer Lage und greifen an, wenn sie sich stark genug fuehlen.

## 2. Der Kernkreis

| Schritt | Was der Spieler tut | Was das Spiel daraus rechnet |
|---|---|---|
| Gruenden | Siedlung auf einer Karte anlegen | Siedler, Startvorraete, Kartenprofil (`docs/original/`, 127 Karten) |
| Produzieren | Gebaeude auf passendes Gelaende setzen | Ertrag je Gebaeude und Gelände, je Stunde (`data/buildings.json`) |
| Forschen | Bibliothek bauen, Gebiete erforschen | 21 Forschungen, Voraussetzungsketten (`data/research.json`) |
| Ausruesten | Werkstatt, Rezept, Ware | 17 Waren aus 9 Rohstoffen (`data/items.json`, `data/warenrezepte.json`) |
| Ausbilden | Einheiten in der Akademie | 28 Einheiten mit belegten Preisen (`data/units.json`) |
| Bewegen | Auftraege mit Reisezeit | Entfernung, Marschdauer, Ladung (`auftraege.py`, `einheiten.py`) |
| Kaempfen | Angriff als Auftrag mit Ankunftszeitpunkt - kein Klick, kein Besetzen | Wallvorrunde, Schlacht, Bericht, danach Rueckmarsch; Beute gestaffelt (`kampf.py`, `kampfbericht.py`) |
| Punkten | — | Kriegs-, Forschungs- und Handelspunkte, Auszeichnungen (`punkte.py`) |

Die Wirtschaft laeuft ortsweise: jedes Dorf hat sein eigenes Lager, seine eigene Ernte und seine eigenen
Auftraege. Es gibt keine kuenstliche Lagerkapazitaet — gehandelt wird ueber Karawanen und Ladung.

## 3. Die Trennlinie zwischen den Vorbildern

| Bereich | Quelle | Was genau |
|---|---|---|
| Rohstoffe, Preise, Erträge | Nebelseetal 2009 | Handbuchzahlen, unveraendert; Abweichungen der 2006er Fassung stehen in `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` |
| Gebaeude und ihre Wirkung | Nebelseetal | Bauplaetze je Gelände, Ausbaustufen, Werkstaetten ohne Stufen (der Ausbau IST die Forschung) |
| Kampf | Nebelseetal | Wallstufen, Vorrunde, Zweikampf, Erschoepfung, Flucht, Beute |
| Karten | Nebelseetal | 127 Originalsiedlungskarten (10 x 10), Katalog in `data/originalkarten/` |
| Punkte | Nebelseetal | zwei Punktearten plus Handelspunkte, kein Sieg — nur Niederlage oder weiter |
| Weltkarte und Koordinaten | Lords Mobile | Springen auf X/Y, Doerfer liegen auf Feldern und werden dort angezeigt |
| Sichtbarkeit | Lords Mobile | offene Uebersicht gegen Spionagebericht, Berichte im Postfach |

Nebelseetal selbst hatte keine begehbare Weltkarte mit Koordinaten. Genau diese Luecke fuellt der
Lords-Mobile-Teil — er bringt keine Inhalte mit, nur den Raum, in dem die Inhalte liegen.

## 4. Der Raum

- Die Welt ist ein Raster (Standard 20 x 20), die Spielerdimensionen sind durchnummeriert (`data/welten.json`: 20 Dimensionen, 6 belegte Welten).
- Jedes Bot-Dorf hat eine feste Position, abgeleitet aus Name und Nummer — nichts wird gewuerfelt (`bottaktik.dorf_position`).
- **Offen sichtbar** beim Ueberfahren: Position, Schild, Fraktion, Dorfname und die bekannten Volkswerte.
- **Nur ueber einen Spionagebericht**: Wallstufe und Wallzustand, aktive Taktik, stationierte Truppen, Items und Vorraete. Der Bericht ist die Entscheidungsgrundlage fuers Pluendern.
- Berichte und Meldungen landen im Postfach; der Spieler springt per Koordinate zum Dorf.

**Zwei Regeln, die nie gebrochen werden (Vorgabe Daniel 02.11.2026):**

1. **Doerfer werden NIE eingenommen.** Ein Dorf wird angegriffen, ausspioniert und gegebenenfalls
   ausgeraeumt — es wechselt nie den Besitzer, es wird nie besetzt, und in einem fremden Dorf steht
   keine Garnison.
2. **Angriffstruppen werden nie am Zielort stationiert.** Der Angriff trifft zu einem Zeitpunkt ein; von
   da an gibt es den Angriffsbericht, und die Truppen sind auf ihrem Rueckweg. Stationieren gibt es nur
   ins EIGENE Dorf — in fremden Siedlungen ist es nicht erlaubt (Handbuch 2009, Seite 19; im Code
   `auftraege.py`, Auftragsart `stationieren`).

## 5. Die Wirtschaft

- **Ortslager statt Reichskasse:** Ernte, Siedlerzuwachs und Ausbildungen bucht `spieloekonomie.ort_tick` je Dorf; die Gesamtsicht ist die Summe der Orte, nie eine zweite Kasse.
- **Ertrag aus Gelaende:** ein Gebaeude bringt je nach Gelände unterschiedlich viel (Holzfaeller 4 auf Wald, 2 auf Steppe — Handbuch 2009).
- **Siedler sind der harte Deckel:** 10 Grundsiedler plus 5 je Haus, hoechstens 6 Siedlungen je Reich.
- **Bots wirtschaften seit dem 02.11.2026 selbst:** jedes Bot-Dorf erzeugt je Stunde 12 Holz, 12 Stein, 12 Nahrung und 9 Gold (drei Anlagen je Grundrohstoff auf bestem Gelände, `data/bot_wirtschaft.json`) und haelt sein eigenes Lager.
- **Beschlossen, noch nicht gebaut:** bei jeder Gruendung drei Karten zur Wahl; die gewaehlte Karte bestimmt den maximal getragenen Rohstoff und die dort schwaecher produzierbaren, Gold hat Vorrang (`docs/KONZEPT_DORF_TAKTIKEN_20261102.md`, Abschnitt 11).

## 6. Die Bots

- Fuenf Gegner mit eigener Fraktion, Aggression und Handelsneigung (`botkern.BOT_NAMEN`, `BOT_FRAKTIONEN`).
- Jeder Bot traegt ein bis drei Doerfer; das erste ist das Hauptdorf und traegt die Volksbasis, ohne Taktik-Punkt.
- Jedes Dorf waehlt aus vier Lagen (Naehe zum Spieler, Staerke, Wallzustand, letzte Niederlage) ein Verhalten als festes Paket, mit 48 Stunden Sperrzeit — deterministisch, nicht gewuerfelt (`bottaktik`).
- Bots kaufen Einheiten aus ihren eigenen Vorraeten zu den belegten Preisen, handeln ueber Karawanen und greifen nur an, wenn die Punktegrenze es erlaubt (Goetterschutz, Band plus/minus 20 Prozent).
- **Beschlossen, noch nicht gebaut:** Voelkerwahl am Start (sechs Voelker, der Spieler waehlt, die Bots bekommen die uebrigen) und die Verdrahtung der 13 Volksboni.

## 7. Punkte und Ende

Es gibt **keinen Sieg** (E5). `punkte.spielausgang` kennt nur Niederlage oder weiter; bewertet wird ueber
Auszeichnungen (Feldherr, Forscher, Haendler, Gesamtherrscher) und Handelspunkte. Die Niederlage tritt
ein, wenn die eigene Existenz wegbricht — nicht durch eine Punktzahl.

## 8. Umfang in Zahlen (gemessen am 02.11.2026)

| Gegenstand | Wert | Beleg |
|---|---|---|
| Einheiten | 28 | `data/units.json` |
| Waren | 17 aus 9 Rohstoffen | `data/items.json`, `data/warenrezepte.json` |
| Forschungen | 21 | `data/research.json` |
| Originalsiedlungskarten | 127 (35 beste, 43 mittlere, 49 schlechte) | `assets/karten/original/`, `data/originalkarten/` |
| Dimensionen / belegte Welten | 20 / 6 | `data/welten.json` |
| Spieluhr | Faktor 180 (einstellbar; nicht belegt, Vorschlag) | `data/spielzeit.json` |
| Pruefstand | 129 Pruefdateien, 4.940 Pruefungen, 0 rot | `docs/audits/sammellauf_20261102_1816.log` |

## 9. Was noch fehlt (ehrlich)

1. **Kartenwahl je Gruendung** — Vorgabe vom 02.11.2026, Konzept Abschnitt 11.
2. **Voelkerwahl am Start und die Volksboni** — beschlossen, 13 Wirkungen noch nicht verdrahtet.
3. **Spionage und Postfach** — die Schnittstelle steht (`bot_doerfer_spionagebericht`), Aufrufer und Anzeige fehlen.
4. **Bots gruenden nicht nach** — sie tragen die Doerfer, die der Kartenaufbau anlegt.
5. **Kein Mehrspieler, kein Server, kein Konto** — und das bleibt so: lokales Einzelspieler-Spiel.

## 10. Technik

Python mit tkinter, ohne Netzverbindung, ohne Installation (portabel startbar), Spielstand als JSON,
Bilder und Daten im Projektordner. Keine laufenden Kosten, keine Konten, keine Telemetrie.

## 11. Der GitHub-Text (fertig zum Einfuegen)

**Kurzbeschreibung (About, rund 340 Zeichen):**

> Ein Einzelspieler-Aufbauspiel, das die Tiefe von Nebelseetal mit der Raum-Mechanik von Lords Mobile
> verbindet: Gruenden, Wirtschaften, Forschen, Ausruesten, Ausbilden und Kaempfen auf einer Weltkarte
> aus Koordinaten — gegen fuenf Bots, die nach denselben Regeln spielen. Python und tkinter, offline,
> portabel, ohne Konto.

**Erweiterte Beschreibung (Einstieg fuer die README):**

> **Worum es geht.** Du gruendest Doerfer, baust Gebaeude auf passendes Gelaende, forschst, stellst
> Waren her und bildest Truppen aus — mit den Zahlen und Regeln des Originals Nebelseetal (Handbuch
> 2009). Was Nebelseetal nicht hatte, kommt aus Lords Mobile: die begehbare Weltkarte mit Koordinaten,
> auf der Doerfer liegen und angesprungen werden.
>
> **Wie du spielst.** Jedes Dorf hat sein eigenes Lager und seine eigene Ernte. Auftraege reisen mit
> echter Reisezeit; gekaempft wird nicht per Klick, sondern als Marsch mit Wallvorrunde, Schlacht und
> gestaffelter Beute. Was du ueber ein fremdes Dorf weisst, haengt davon ab, ob du spionierst: offen
> siehst du Position, Fraktion und Volkswerte, alles andere nur im Spionagebericht.
>
> **Gegen wen.** Fuenf Bots wirtschaften in eigenen Doerfern, waehlen Taktiken aus ihrer Lage und
> greifen an, wenn sie sich stark fuehlen — nach denselben Regeln wie du.
>
> **Was es nicht ist.** Kein Eroberungsspiel: Doerfer werden ausgespaeht, angegriffen und ausgeraeumt,
> aber nie eingenommen — die Truppen ziehen wieder ab. Und: kein Browsergame, kein Server, keine
> Anmeldung, keine Kosten. Ein lokales Spiel, das sich wie ein Browserspiel von damals anfuehlt.
