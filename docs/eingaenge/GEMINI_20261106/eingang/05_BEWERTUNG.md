# 05 Bewertung - was uebernehmen, was teilweise, was entscheidet Daniel

**Stand:** 06.11.2026, Kopf `3c5189a`. **Nichts hiervon ist gebaut.** Diese Tabelle ist die
Vorlage fuer EINE Entscheidungsrunde (`docs/FRAGEN_AN_DANIEL_20261106_GEMINI.md`).
Spalte "Messzahl heute" ist gemessen, Spalte "Effekt" ist die erwartete Wirkung - keine Zusage.

## A. Uebernehmen empfohlen (Vorschlag der Sitzung)

| Nr. | Stueck | Messzahl heute | Erwarteter Effekt | Aufwand | Zahlen von Daniel? |
|---|---|---|---|---|---|
| B-3 | Postfach: Filter, Archiv, Ablauf | 29 Fuellstellen, 0 Archivfunktionen | lange Partien bleiben lesbar; Berichte verschwinden nicht im Stapel | S | nein (keine Spielzahl) |
| B-8 | Ruhm-Fortschrittsbalken | 4 Auszeichnungen, 0 Balken | der naechste Rang ist sichtbar, ohne neue Zahl im Spiel | S | nein |
| B-4 | Mauerreparatur (Prozent-Wall) | 0 Wallschaden in den Laeufen; Luecke `kampfbericht.py:566` | der Wall ist nicht mehr reines Verbrauchsgut | M | **ja** (Kosten, Dauer, Deckel) |
| B-5 | Verwundetenheilung | Heilung existiert nicht (`Heilkunde` = Siedler +10 Prozent) | Verluste schmerzen, sind aber nicht endgueltig; Aufbau wird NICHT kuerzer | M | **ja** (Quote, Kosten, Dauer) |
| B-1 | Diplomatie mit Gunst und Vertraegen | 2 Kennzahlen je Bot, 0 Vertraege | neue Spielentscheidung statt zwei Knoepfen | L | **ja** (Gunstwerte, Vertragskosten) |
| B-2 | Proaktive Diplomatie-Events | 35 Overlay-Stellen, 0 Ereignisse mit Antwort | aus Berichten werden Entscheidungen | M | **ja** (Forderungen, Fristen) |

## B. Teilweise - erst nach dem jeweiligen Vorgaenger

| Nr. | Stueck | Messzahl heute | Bedingung |
|---|---|---|---|
| T-1 | Rachetopf mit wachsender Armee | Gedaechtnis `geschlagen_von` da, Topf fehlt | Teil von B2 (Bot-Zielbild); Groesse entscheidet Daniel |
| B-6 | Etappen-Reise ueber das Portal | 0 Treffer "etappe"; eine Strecke je Reise | **verlaengert** Reisen - A2-Messpflicht und Daniels Leitlinie 237 muessen vorher erfuellt sein |
| B-7 | Siedlungsumzug | 0 Umzugsfunktionen | braucht Daniels Zielbild (Siedler, Portalkosten, Kartenregel) |
| B-9 | Nachrichten-Uebersicht begrenzen | kein Limit im Code | gehoert zu B-3, kein eigenes Stueck |
| B-10 | `pathlib` und Type Hints | 14 von 60 Modulen mit `pathlib`, 767 Rueckgabetypen | Aufraeumschnitt ohne Spielwirkung, nur wenn Daniel ihn will |

## C. Faellt weg - die Frage ist im Code schon beantwortet

| Gegenstand | Beleg |
|---|---|
| 20 Dimensionen gegen 6 Welten | 6 Dimensionen, `_schnitt_w6` (04.11.2026) |
| Bots greifen die Spielersiedlung an (B3) | `main.py:6896` plus Diebstahl (Register 161/162) |
| Sprung-Sperre bei laufenden Auftraegen | `main.py:10857` (Daniel 01.11.2026) |
| Preisfrage "Transporte abfangen" | von Daniel am 05.11.2026 abgelehnt |

## D. Was Daniel entscheiden muss (eine Runde, neun Punkte)

1. **Reihenfolge:** welches der sechs Stuecke aus A zuerst? Vorschlag der Sitzung: B-3, dann B-8
   (beide klein, reine Anzeige), dann B-4 und B-5 (brauchen Zahlen), dann B-1 und B-2 als eine
   Diplomatie-Runde.
2. **Mauerreparatur:** Kosten, Dauer, Deckel - und ob sie nur in der eigenen Siedlung wirkt.
3. **Verwundetenheilung:** wie viel Prozent der Verluste heilbar, zu welchem Preis, ueber welche Zeit.
4. **Diplomatie:** Gunstskala, drei Vertragsarten mit Mindestgunst und Kosten, Folge eines Bruchs.
5. **Diplomatie-Events:** welche Nachbarn fordern was, mit welcher Frist und welcher Folge.
6. **Rachetopf (T-1):** waechst die Rache je Angriff, je Verlust oder je Spieltag - und ab wann greift
   der Bot zurueck?
7. **Etappen-Reise (B-6):** soll Reisen laenger dauern? Wenn ja, wie viel Aufbauzeit darf das kosten?
8. **Siedlungsumzug (B-7):** gewuenscht oder nicht? Wenn ja, Preis und Bedingung.
9. **Aufraeumschnitt (B-10):** `pathlib` und Type Hints jetzt nachziehen oder nur fuer neuen Code?

## E. Was diese Sitzung NICHT getan hat

- **kein Code geaendert** (Dokumente, Sammlung und Ablage)
- **kein Modellauf** (die 4,00 USD sind unangetastet)
- **nichts aus der Sammlung eingebaut**, auch nicht die zwei kleinen Anzeigen B-3 und B-8
