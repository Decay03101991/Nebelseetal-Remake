# Plan: starke DeepSeek-Laeufe im Projekt Nebelseetal (03.11.2026, 18:57)

## Rahmen

| Gegenstand | Wert | Beleg |
|---|---|---|
| Projektrahmen starke Laeufe | **6,00 USD** | Protokoll 18:53 (3 USD vom 11:22 + 3 USD nachgelegt) |
| Davon verbraucht | **0,00 USD** | in dieser Sitzung kein Aufruf von `deepseek-v4-pro` |
| Deckung (Kontostand) | **11,38 USD** | Daniels Ablesung 18:48 |
| Harte Tagesgrenze | **4 EUR** ueber alle Modelle und Profile | Kosten-Schutzregel, steht UEBER dem Rahmen |

Der Rahmen ist ein Ausgabenrahmen, kein Guthaben: aufladen kann nur Daniel im DeepSeek-Konto.

## Was ein Aufruf wirklich kostet (gemessen, nicht geschaetzt)

- Ein Aufruf mit `max_tokens: 48000` lieferte 14.117 Denk- und 4.398 Antwort-Token fuer **0,039 USD**
  (belegt 31.10.2026).
- Ein Tag mit vier starken Paketen plus vollem Prueflauf lag laut Anbieter-CSV bei **~1,3 USD**.
- Ein Paket = 1 Auftragsdatei + 2 bis 4 Aufrufe = **0,08 bis 0,16 USD**.
- Folge: 6 USD sind etwa **40 bis 60 starke Aufrufe**. Die fuenf offenen Denk-Pakete brauchen rund
  12 - der Rahmen ist damit komfortabel, nicht knapp.

## Einteilung (Reihenfolge nach Abhaengigkeit, nicht nach Geschmack)

| # | Paket | Warum jetzt | Aufrufe | geplant |
|---|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** | Daniels Entscheidung 18:5x: der Bot muss den Siedlerkarren bauen wie der Spieler. Ohne Warenkette (Stellmacher, Leder, Wolle, Pferde) gruendet nach `siedlerkarren_pflicht: true` KEIN Bot - das blockiert S-7 und S-9 | 3 | 0,12 USD |
| 2 | **S-7 Karawanen** | naechster Schnitt in Daniels Reihenfolge; vier Doerfer je Bot brauchen Nachschub | 4 | 0,16 USD |
| 3 | **S-9 Stil je Taktik** | baut auf S-6b/S-7 auf (was der Bot mit seinem Reichtum TUT) | 2 | 0,08 USD |
| 4 | **W-3 Kampf ueber Weltgrenzen** | Daniels Entscheidung steht (teuer mit Deckel); der Preis ist Denkarbeit, der Bau nicht | 3 | 0,12 USD |
| 5 | **V-2/V-3 Berichts-Sicht je Seite** | neue Vorgabe Daniel 19:00: Angriffs- und Verteidigungsbericht, vollstaendig ueber alle Angaben des Angegriffenen | 3 | 0,12 USD |
| 6 | **V-5 Bot-Auswertung** | Bots sollen aus Berichten schliessen, ob ein weiterer Angriff lohnt | 2 | 0,08 USD |
| 7 | **Story W-11** | nebensaechlich, laesst sich zuletzt und in einem Zug machen | 2 | 0,10 USD |
| | **Summe geplant** | | **19** | **0,78 USD** |
| | Reserve (Nachfassen, unklare Antworten) | je Nachfassen 0,04-0,08 USD | ~15 moeglich | 5,42 USD |

## Grenzen (gelten fuer jeden Lauf)

- **Nie waehrend eines Sammellaufs** - auch kein lesendes Kind (belegt 05.10.2026: `test_baseline` fiel
  dadurch aus).
- Hoechstens zwei bis drei Kinder gleichzeitig; der Laptop muss bedienbar bleiben.
- Kinder **schreiben genau eine Datei ausserhalb des Projekts** (`D:\Arbeiten\Hermes\Notizen\<THEMA>.md`),
  lesen nur, committen nie.
- Code, Register, Protokoll, Sammellauf und Commits macht die Sitzung selbst - kein Kind.
- Ein Paket ist eine Datei unter `docs/auftraege/` und muss ohne Rueckfrage ausfuehrbar sein.

## Messung und Meldung (Daniels Regel)

1. **Vor** jedem starken Lauf: Kontostand nennen (von Daniel abgelesen oder aus der Anbieter-CSV).
2. **Nach** jedem Lauf: Kosten MESSEN (`--usage-file` bzw. Anbieter-CSV), nie schaetzen; Zeile ins
   Protokoll mit Zeit, Paket, Aufrufen, Kosten.
3. **Antwortlaenge pruefen**: `reasoning_tokens` gegen `max_tokens` - 0 Zeichen Antwort heisst
   verbranntes Geld, dann `max_tokens` erhoehen.
4. **240 s ohne Streaming-Stueck** = echter Haenger; darunter weiterlaufen lassen (grosse Modelle
   brauchen Denkzeit).
5. Ist der Rahmen zu 80 % verbraucht, frage ich nach, bevor ich weiterdenken lasse.

## Was NICHT in den Rahmen gehoert

Die Sitzungsarbeit selbst (dieses Modell, `deepseek-flash`) laeuft nicht gegen den 6-USD-Rahmen; sie
kostet nach Abrechnung Bruchteile eines Cents je Takt (18:48 gemessen: 0,33 USD fuer die ganze
T-1-Runde inklusive aller Pruefungen). Der Rahmen gilt nur fuer `deepseek-v4-pro`.
