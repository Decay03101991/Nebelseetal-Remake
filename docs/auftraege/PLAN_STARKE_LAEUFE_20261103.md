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

## Einteilung - bewusst breit (Vorgabe Daniel 19:1x: den Rahmen wirklich nutzen)

Rahmen **6,00 USD**, geplant sind **etwa 4,00 USD** (rund 30 Aufrufe), Rest Puffer. Jeder Schnitt bekommt
**drei Runden** statt einer: (1) Entwurf, (2) harte Gegenpruefung durch ein zweites Kind, das den Entwurf
gegen die Datendateien und Register-Eintraege prueft, (3) Nachbesserung aus den Befunden. Das kostet das
Dreifache und ist genau der Grund fuer den Rahmen: ein Entwurf ohne Gegenpruefung hat schon Fehlbefunde
geliefert.

| # | Paket | Runden | Aufrufe | geplant |
|---|---|---|---|---|
| 1 | **S-6b Warenkette fuer Bots** (Warenhaltung, Werkstattkette, Rezepte, Karrenbau) | Entwurf + Gegenpruefung + Nachbesserung | 4 | 0,45 USD |
| 2 | **V-3 Vollstaendiger Kampfbericht** (alle Angaben des Angegriffenen) | 3 | 3 | 0,35 USD |
| 3 | **V-2 Angriffs- und Verteidigungsbericht** (zwei Sichten) | 3 | 3 | 0,35 USD |
| 4 | **V-1 Angriffswarnung** (roter Rahmen, Farbe, Dauer) | 2 | 2 | 0,20 USD |
| 5 | **V-4 Postkasten** (Uebersicht, Arten, Filter, Details) | 3 | 3 | 0,35 USD |
| 6 | **V-5 Bot-Auswertung** (Bots schliessen aus Berichten) | 3 | 3 | 0,35 USD |
| 7 | **S-7 Karawanen** (Regeln, Reisekosten, Nachschub) | 3 | 3 | 0,35 USD |
| 8 | **S-9 Stil je Taktik** | 2 | 2 | 0,20 USD |
| 9 | **W-3 Kampf ueber Weltgrenzen** (Preis mit Deckel) | 3 | 3 | 0,35 USD |
| 10 | **Story W-11** (sechs Fraktionen) | 2 | 2 | 0,20 USD |
| 11 | **Querschnitt: Gesamtkonsistenz-Audit** (Kernkreis, Anzeige = Kern, Register gegen Code) | 2 | 3 | 0,35 USD |
| 12 | **Querschnitt: Pruefstrategie** (welche Wachen fehlen, Testdesign fuer die V-Schnitte) | 1 | 2 | 0,20 USD |
| | **Summe geplant** | | **33** | **3,95 USD** |
| | Puffer fuer Nachfassen (10-15 Aufrufe) | | | 2,05 USD |

**Was jetzt zusaetzlich an das starke Modell geht** (bisher als "macht die Sitzung selbst" gebucht):
Entwuerfe fuer **Datendateien** (Schluessel und Werte, nicht nur Regeln), **Testdesign** je Schnitt,
**Gegenpruefung** fremder Entwuerfe, **Doku-Entwuerfe** (Vorgabenseiten, Stand-Block-Text) und
**Codereview** meiner Diffs - jeweils als Vorschlag, den die Sitzung prueft und einbaut. Code, Register,
Protokoll, Sammellauf und Commits bleiben bei der Sitzung.

**Qualitaetsregel fuer die breitere Nutzung:** jeder Entwurf wird gegen die Datendateien geprueft, bevor
er Gesetz wird (die Uebergabe belegt: Angaben im eigenen Auftrag nachmessen, sonst folgt das Modell einer
falschen Vorgabe). Ein gruener Entwurf ohne Gegenprobe zaehlt nicht.

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
