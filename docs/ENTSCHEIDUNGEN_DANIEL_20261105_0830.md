# Entscheidungen Daniel - 05.11.2026, 08:40 (neun Antworten in EINER Runde)

> Vorgelegt als Auswahlformular, beantwortet in zwei Blaettern derselben Runde. Wo Daniel frei
> geantwortet hat, steht seine Antwort woertlich-nah und darunter, was sie technisch bedeutet.

| Nr. | Frage | Daniels Antwort | Folge fuer die Arbeit |
|---|---|---|---|
| 1 | Bots raeumen gepluenderte Ruinen? | **Ja, mit Karren und ohne Kampf** | Bot-Logik: Ruine anlaufen, Rest einladen, keine Schlacht. Eigener Schnitt mit Wache. |
| 2 | Zweite Kampfphase im Drachenkampf? | **20 % unter halber Wache ansetzen - vorher messen** | Erst `tools/drachen_balancing.py` mit 20 % messen, Zahlen ins Balancing-Dokument, dann bauen. |
| 3 | Drache nach dem Sieg relevant halten? | **Keine Regeneration, kein Erwachen.** Woertlich-nah: "Die Spielgeschichte und die drachen bilden als feste punkte auf Ihrer jeweiligen welt eine taktik relevanz fuer ein spieler damit er zum beispiel von einer seite nicht angegriffen wird wenn er neben sich eine bereits besiegte ruine stellt und es ist eine wichtige beute, dafuer brauchen wir keinerleih weitere funktion des drachen" | Regeneration und Erwachen **entfallen**. Die Ruine wird ein **taktischer Punkt** (siehe Nr. 9) und bleibt eine **wichtige Beute**. |
| 4 | Protokoll verdichten? | **Wenn es zu voll wird, einen Teil als Historie auslagern, gut archivieren - lueckenlos, nichts verlieren, weiter alles Relevante erfassen.** | Bei der naechsten Verdichtung wird **ausgelagert statt geloescht** (Muster: `ENTWICKLUNGSPROTOKOLL_HISTORIE_BIS_20261101.md`). |
| 5 | Versteck/Cranny fuer Bot-Doerfer? | **Spaeter, eigenes Register** | Nicht jetzt. |
| 6 | Hausfarben an die Wappentinkturen angleichen? | **Ja, angleichen** | Sechs Zeilen in Chronik und `data/haeuser.json`: Farben folgen den Wappen. |
| 7 | Drachenschuppe handelbar? | **Nein - reine Trophae** | Bleibt wie gebaut (Register 207), keine Aenderung noetig. |
| 8 | Beute-Reihenfolge (Kampfregel 4)? | **b) Gold bevorzugen, Rest anteilig auffuellen** | Regel 4 wird gebaut, aber **ohne** dass Gold die ganze Ladung frisst: Gold zuerst, dann anteilig wie heute. |
| 9 | Wie wirkt die besiegte Ruine taktisch? | **Ruine sperrt ihre Seite: kein Angriff aus dieser Richtung** | Neue Mechanik: eine besiegte Ruine deckt die Himmelsrichtung, auf der sie liegt. **Braucht ein eigenes Register** (Kampfweg + Anzeige). |

## Was daraus als naechstes gebaut wird (Reihenfolge nach Risiko)

1. **Frage 6** - reine Text- und Datenarbeit, kein Kern. Sofort machbar.
2. **Frage 8** - kleine Aenderung in `kampfbericht.beute_staffel`: Gold mit Vorrang, Rest anteilig.
   Eigene Wachen (Gold zuerst, aber Holz/Stein kommen weiter mit).
3. **Frage 1** - Bot raeumt Ruinen: Bot-Logik ohne Kampf, eigener Schnitt mit Wache.
4. **Frage 2** - erst messen (20 %), dann entscheiden, dann bauen.
5. **Frage 9** - neue Taktik-Mechanik, eigenes Register, braucht Konzept und Wachen.

**Nicht mehr noetig:** Regeneration (Frage 3) und Erwachen (Frage 3) - ausdruecklich abgelehnt.
