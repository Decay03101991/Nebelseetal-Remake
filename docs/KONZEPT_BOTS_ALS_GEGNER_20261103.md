# KONZEPT: Bots als echte Gegner (03.11.2026)

> Entwurf, NICHTS gebaut. Grundlage: Daniels Vorgabe aus der Fragenrunde 03.11.2026 und der
> gemessene Ist-Stand im Code. Dieses Papier entscheidet nichts - es schneidet die Arbeit so, dass
> jeder Schnitt einzeln pruefbar ist.

## 0. Der Auftrag, woertlich

> "ich möchte das bots wirkliche gegner darstellen, heißt sie müssen die selben mechaniken nutzen um
> zu gewinnen, heißt genau so wie der spieler karten auswählen und je nachdem welche taktik sie
> verfolgen auch dementsprechend den gebäudebau auf ihren karten vorran treiben und mit ihren
> erwirtschafteten ressourcen auch forschungsschritte durchlaufen um ihre einheiten und neue gebäude
> freizuschalten ... Auch der bot darf karren ausbilden und mit denen seinem zweitdorf wenn benötigt
> zum bau von gebäuden als starthilfe oder später als dauerhafte unterstützung immer wieder
> ressourcen schicken ... Ein bot muss wirtschaften und entscheiden."

## 1. Ist-Stand in Belegen: zwei Wirtschaften nebeneinander

Der Spieler und die Bots benutzen heute **zwei verschiedene Maschinen** fuer dieselbe Sache.

| Gegenstand | Spieler | Bot | Folge |
|---|---|---|---|
| Daten | `Settlement` (Karte, bauten, stufen, einheiten, vorraete, bevoelkerung, werkstaetten, ausbildung, forschungsauftrag) | `BotDorf` (name, karte, vorraete, ernte_seit, wall, taktik) | dem Bot fehlen Bauplaetze, Stufen, Warteschlangen |
| Ertrag | `wirtschaft.ertrag_gesamt` -> `_feld_ertraege` (aus den FELDERN der Karte) | `main.bot_dorf_ertrag` (Kartenprofil / 10) | zwei Zahlenwege fuer denselben Rohstoff |
| Ernte | `spieloekonomie.ort_tick` (Journal, Werkstatt, Ausbildung, Nahrungsverbrauch, Siedlerzuwachs) | `main.bot_doerfer_ernten` (Rate x Stunden, Deckel 20.000) | kein Verbrauch, kein Zuwachs, kein Journal |
| Bauen | `spielschicht.bauen` / `ausbauen` (Preise, Stufen, Gelände) | **gibt es nicht** | `bot.gebaut` bleibt immer 0 |
| Forschen | `forschung` + `forschungsauftrag` je Ort | **gibt es nicht** | `bot.geforscht` bleibt immer 0 |
| Truppen | `spielschicht.ausbilden` (Warteschlange, Kosten, Dauer) | `main.bot_armee_aufstellen` (kauft EINE Einheit je Aufruf) | keine Ausbildungsdauer, kein Nahrungsbedarf |
| Gruenden | `gruendung_pruefen` / `gruendung_ausfuehren` (Karte, Kosten, Siedler) | Siedlungen werden beim Start gewuerfelt (1-3), danach nie neue | Bots wachsen nicht |
| Transport | `auftraege.starten` (Karren, Ladung, Reisezeit, Kosten) | **gibt es nicht** | keine Karawanen zwischen Bot-Doerfern |
| Kartenwahl | Spieler waehlt (Register 147) | `bot_kartenwahl` -> `botkern.oekonomie_kartenwahl` (V-6) | **fertig** |
| Volksboni | Volk am Ort, wirkt (V-5) | Volk + Taktik, wirkt (V-5) | **fertig** |

**Der Kern des Problems ist also nicht der Nahrungsverbrauch.** Der ist nur das erste Symptom:
weil der Bot eine eigene, duennere Wirtschaft hat, fehlt ihm jede Stelle, an der Verbrauch, Bau,
Forschung und Ausbildung ueberhaupt stattfinden koennen.

## 2. Der eine Gedanke

**Ein Datenmodell, ein Kern.** Ein Bot-Dorf wird ein ORT wie eine Spielersiedlung und laeuft durch
dieselben Funktionen - nur die ENTSCHEIDUNGEN kommen aus `botkern`/`bottaktik` statt aus Klicks.
Dann gilt fuer den Bot automatisch:

- derselbe Ertrag (aus den Kartenfeldern), dieselben Preise, dieselben Bauplaetze,
- derselbe Nahrungsverbrauch (8 je Einheit und Tag), derselbe Siedlerdeckel,
- dieselbe Forschungsvoraussetzung, dieselbe Ausbildungsdauer,
- dieselben Reisekosten, dieselben Karren und Ladungen,
- dieselbe Gruendungsregel.

Das ist keine neue Mechanik, sondern das **Abschaffen einer zweiten**. Alles, was der Bot dann tut,
ist schon geprueft - es kommt nur aus einer anderen Quelle.

## 3. Die Schnitte

Reihenfolge so gewaehlt, dass nach jedem Schnitt etwas Sichtbares und Pruefbares dasteht.

| Schnitt | Inhalt | Groesse | Abhaengig von |
|---|---|---|---|
| **S-1 Datenmodell** | `BotDorf` bekommt die Felder eines Ortes (bauten, stufen, einheiten, bevoelkerung, werkstaetten, ausbildung, forschungsauftrag, waren, journal) - entweder durch Umstellung auf `Settlement` oder durch Angleich der Felder. Alte Spielstaende laden verlustfrei. | L | - |
| **S-2 Ein Kern** | Bot-Ernte laeuft ueber `spieloekonomie.ort_tick` (gleiche Funktion wie beim Spieler); `main.bot_dorf_ertrag` und `bot_doerfer_ernten` werden zu Anzeige-Rueckfall oder entfallen. **Erst hier** greift der Nahrungsverbrauch, den Daniel 03.11.2026 verlangt hat. | L | S-1 |
| **S-3 Bauen** | Der Bot baut und baut aus: Bauplaetze aus der Karte, Preise aus `baupreise`, Stufen wie beim Spieler. Die REIHENFOLGE kommt aus der Taktik (Ausbauplan je Taktik in einer Datendatei, z. B. "Waechterin: Wall zuerst"). | M | S-1, S-2 |
| **S-4 Forschen** | Der Bot forscht mit seinen eigenen Ressourcen, mit derselben Voraussetzungskette - und schaltet damit Einheiten und Gebaeude frei. | M | S-1, S-2 |
| **S-5 Ausbildung** | Statt `bot_armee_aufstellen` (Kauf) eine Ausbildungs-Warteschlange wie beim Spieler; die **Kaufbremse** aus Daniels Antwort (Futterdeckung + Reserve) sitzt davor. | M | S-2 |
| **S-6 Gruenden** | Der Bot gruendet nach: Kosten, Siedler, Karte (Kartenwahl ist fertig). **Daniel 03.11.2026: vorerst 3 Gruendungen je Bot = 4 Doerfer** (1 Startdorf + 3); mehr spaeter ausdruecklich erlaubt, dann nur eine Zahl in `data/bot_wirtschaft.json` (`gruendungen_je_bot`). Offen bleibt das WANN (Siedler frei? Vorrat voll? Taktik "wachsen"?). | M | S-1, S-3 |
| **S-7 Karawanen** | Der Bot schickt Karren zwischen seinen Doerfern - mit `auftraege.starten` (dieselbe Funktion wie der Spieler), inklusive Reisezeit und Reisekosten. Regel noetig: nur bei Mangel im Zieldorf UND Ueberschuss im Quelldorf. | M | S-2, S-6 |
| **S-8 Reisekosten** | Auch Bots zahlen Reisekosten aus dem STARTDORF (Daniel 03.11.2026). **Beim Spieler ist das bereits so** (gemessen: `auftrag_starten` bucht `kosten` von `quelle.vorraete` ab, Zeilen 3426-3440) - fuer Bots fehlt die Stelle, weil ihre Marsche keine Auftraege sind. | S | S-7 |
| **S-9 Stil** | Was der Bot mit seinem Reichtum TUT, bleibt Taktik: "Pluenderer" baut Karren und Beutezuege, "Bastionier" Wall und Ausbau, "Waechterin" Verteidigung, "Spaeherin" Kundschafter, "Raecher" Angriff. Je Taktik eine Gewichtung in `data/` - keine Zahl im Code. | M | S-3 bis S-7 |

**S-1 und S-2 sind der schwere Teil** (Risiko: 5.400+ Pruefungen, Spielstaende, Anzeigen). Ab S-3
ist jeder Schritt klein und einzeln sichtbar: ein Bot, der einen Holzfaeller baut, ist ein Bild und
eine Zahl.

## 4. Was nach welchem Schnitt sichtbar ist

- nach S-2: Bot-Doerfer haben ein Journal, einen Siedlerzuwachs und **Nahrungsverbrauch**; eine
  hungrige Armee ist im Bericht als `unterdeckung` zu sehen (Daniels Frage 2).
- nach S-3: im Spionagebericht stehen Gebaeude und Stufen eines Bot-Dorfes - die Pluenderung wird
  dadurch planbar.
- nach S-5: Bots haben dieselben Einheiten wie der Spieler, weil sie sie ausbilden muessen.
- nach S-6: die Bot-Doerferzahl waechst sichtbar auf der Weltkarte.
- nach S-7: Karawanen laufen zwischen Bot-Doerfern und sind als Truppenbewegung zu sehen (verborgen
  bleibt Art und Anzahl, Register 140).

## 5. Daniels Antworten von heute (festgehalten, gelten ab jetzt)

1. **Bots nutzen dieselben Mechaniken wie der Spieler** (Karten, Bau nach Taktik, Forschung,
   Ausbildung, Gruenden, Handel, Karawanen zwischen eigenen Doerfern). Ziel: echte Gegner.
2. **Nahrung 1:1** wie beim Spieler (8 je Einheit und Tag, alle Einheiten des Bots), bei
   Unterdeckung **keine Desertion**, aber **Kaufstopp**: der Bot stellt nichts Neues auf, solange
   die Unterdeckung laeuft.
3. **Kaufbremse** zusaetzlich: aufgestellt wird nur, solange die Nahrung im Lager den Tagesbedarf
   der Armee **plus Reserve** deckt (Reserve = `tagesbedarf x reserve_stunden / versorgung_stunden`).
4. **Reisekosten auch fuer Bots**, abgebucht im Dorf, in dem die Reise beginnt - beim Spieler
   ist das bereits so (`auftrag_starten` bucht von `quelle.vorraete`).
5. **Fundament zuerst:** S-1/S-2 werden vor der Sofortmassnahme gebaut (kein Doppelbau).
6. **Start wie der Spieler:** ein Dorf, 10 Siedler, 100 Holz/Stein, leere Armee, eine Karte.
7. **Alle Bots gleich stark**, Unterschied nur ueber die Taktik.
8. **Hoechstens 4 Doerfer je Bot** (1 Startdorf + 3 Gruendungen); mehr spaeter, dann nur eine
   Zahl in der Datendatei.

## 6. Drei Entscheidungen, die S-1/S-2 blockieren

1. **Startbedingungen der Bots:** heute gewuerfelt (1-3 Doerfer, Vorschlagsvorraete, leere Armee).
   Sollen Bots wie der Spieler mit 10 Siedlern, 100 Holz/Stein, EINEM Dorf und einer Karte starten -
   oder mit Vorsprung (mehr Doerfer, mehr Vorrat), damit sie frueh gefaehrlich sind?
2. **Eine Stufe fuer alle oder je Bot?** `data/spieloekonomie.json` kennt leicht/mittel/schwer.
   Heute rechnen alle Bots gleich (Kartenwahl "schwer"). Sollen die fuenf Bots unterschiedlich
   schwierig sein (z. B. Haug leicht, Krank schwer)?
3. **Zeitbudget je Bot-Takt:** ein vollstaendiger `ort_tick` je Bot-Dorf kostet Rechenzeit. Wie
   viele Bot-Doerfer darf ein Reich haben (Spieler: hoechstens 6), und wie oft darf der Bot
   wirtschaften (heute ein Takt, in dem EINE Einheit gekauft wird)?

## 7. Was NICHT dazugehoert (Grenzen)

- **Keine Eroberung, keine Garnison in fremden Doerfern** - die zwei Regeln aus dem Gesamtkonzept
  Abschnitt 4 bleiben unangetastet.
- **Kein neuer Zahlenwert ohne Quelle.** Alles, was ein Bot entscheiden soll, steht als Gewicht in
  `data/` mit Begruendung.
- **Kein Umbau der Ordnerstruktur**, keine neuen Abhaengigkeiten.
- **Der Spieler bleibt Massstab, nicht Zielscheibe:** die Bots duerfen nicht dadurch "besser"
  werden, dass sie Regeln umgehen (z. B. doppelte Ernte), sondern nur dadurch, dass sie dieselben
  Regeln nutzen.
