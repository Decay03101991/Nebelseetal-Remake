# Originalreferenz: Gebaeude-Baumenue (Gamestar2)

**Bild:** [`docs/nebelseetal_gamestar2.jpg`](nebelseetal_gamestar2.jpg), bei Daniel im oeffentlichen GitHub dokumentiert. Historische Spielansicht, **keine** Aufnahme der heutigen Tkinter-Anwendung.

## Konkreter Bildbefund

Das Bild zeigt oben eine Ressourcenzeile und die aktive Siedlung, links Navigation, rechts die Auswahl **Siedlungsuebersicht / Produktion / Verteidigung**. Im Mittelteil „Produktionsgebaeude bauen“, eine Gebaeudeauswahl mit **Holzfaeller**, **Steinmetz**, **Jaeger** und **Haus**, je **Beschreibung, Baukosten in Holz/Stein, Siedlerbedarf bzw. Bauaktion**. Das Original zeigt auch Verweise auf Nachrichten und Forschung/Kriegspunkte.

## Abgleich mit Quellcode

- `src/main.py` enthaelt `bauen_auf_karte` (Feld-/Forschungspruefung), `baukosten` (JSON-Preise), `_karten_bauen` und den Siedlungskarten-Renderer. Funktionen **existieren im Code**.
- Der aktuelle GUI-Einstieg ist die Siedlungskarte mit Feldwahl und Bauaktionen und das Dorfzentrum; die komplette Original-Bauseite (Rubriken, gleichzeitige Kosten und Werkplaetze, Originalanordnung) ist damit **nicht nachgewiesen**.
- Baupreise im Code sind teils **Remake-Vorschlaege**, nicht belegte historische Originalwerte. Nie stillschweigend als Originalwerte ausgeben.
- Eine **wortgetreue Umsetzung der Screenshot-Oberflaeche** ist nicht automatisch richtig: Preisregeln und Spielmechanik zuerst mit Handbuch/Originalquellen vergleichen.

## Verbindliche Aufgaben fuer die naechste GUI-Runde

1. Siedlung auswaehlen → Gebaeudeliste nach Rohstoffproduktion, Wohnen, Industrie, Verteidigung.
2. Je Eintrag **Name, Zweck, Ertrag, Baukosten, Siedlerbedarf, Baukunst-/Technologievoraussetzung, Geländeeignung** aus denselben aktiven Regeldaten ableiten.
3. Baubar/gesperrt begruenden; Standort-/Feldwahl deutlich machen; ein einziger Buchungspfad ueber `_karten_bauen`, keine zweite Kasse oder Schattenpreise.
4. Originalreferenz als Vergleich in Tests/Designprotokoll verwenden: Holzfaeller / Steinmetz / Jaeger / Haus, Kopfzeile, Siedlung und Kategorie-Navigation.
5. Unter Windows mit Maus, Tastatur und kleineren Aufloesungen manuell pruefen; UI nur freigeben, wenn sie sich wirklich bedienen laesst.

**Diese Runde hat bewusst keine neue historische GUI behauptet oder den Screenshot als Spielflaeche verwendet.**
