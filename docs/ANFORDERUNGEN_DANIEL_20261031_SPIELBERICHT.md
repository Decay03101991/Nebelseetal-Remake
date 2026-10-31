# Daniels Spielbericht — 31.10.2026, Slot 1 (erste echte Spielrunde nach Aufstockung)

**Was das ist.** Daniel hat Slot 1 gespielt, gespeichert und beendet; danach hat er seine Eindrücke
geschildert. Dieses Dokument hält **zuerst die gemessene Runde** fest (aus dem Spielstand, nicht aus
dem Gedächtnis), dann seine Kritik in seine Worte gefasst, dann die **Einordnung in die Reihenfolge**.

---

## 1. Die gespielte Runde — gemessen am Spielstand

Quelle: `~/.nebelseetal/savegame_slot1.json` gegen `~/.nebelseetal/archiv/SPIELBASIS_20261031_2136.json`
(SHA256 jetzt `9f00a016…`).

| Größe | vor der Runde | nach der Runde |
|---|---|---|
| Spieltag | 5 | **6** |
| Spielsekunden | 379.305 | 449.533 (**+19,5 Spielstunden**) |
| Siedlungen | 1 | 1 |
| **Bevölkerung** | 10 | **3,5** |
| **Gebäude im Ort** | 37 | **81** |
| Einheiten im Ort | 7 Handkarren | 7 Handkarren · **7 Bürgerwehr · 1 Streuner** |
| Forschung | Baukunst 3, Wagenbau 1, Forstwirtschaft 1 | + **Wagenbau 2** |
| Nachrichten | 25 | 32 (7 neu) |
| Aufträge / Angriffe | 0 | **0** |
| Vorräte | aufgestockt | praktisch unverändert (nur Produktion/Verbrauch) |

**Gebäude nach Art (81):** 13 Goldminen, 12 Jäger, 7 Erzmine, 7 Holzfäller, 5 Tempel, 5 Schmieden,
5 Häuser, 4 Steinmetz, 4 Farm, 4 Lager, 3 Pferdezucht, 2 Rinderfarm, 2 Schafszucht, 2 Bogenbauer,
2 Nähstube, 1 Bibliothek, 1 Stellmacher, 1 Diebesgilde, 1 Kriegerakademie.

**Die sieben neuen Nachrichten sind der Kern des Befunds:**

```
[forschung]  Forschung Wagenbau auf Stufe 2 abgeschlossen.
[ausbildung] Streuner nicht ausgebildet: Freie Siedler fehlen vor Ort.
[ausbildung] Siedlerkarren nicht ausgebildet: Freie Siedler fehlen vor Ort.   (2x)
[ausbildung] Handelskarawane nicht ausgebildet: Freie Siedler fehlen vor Ort.  (3x)
```

**Befund:** Daniel hat in einer Runde **44 Gebäude** gebaut und dabei die **Bevölkerung von 10 auf 3,5
Siedler** verbraucht (jedes Gebäude kostet Siedler). Danach war **keine Einheit mehr ausbildbar** —
sechs Ausbildungsversuche scheiterten an „Freie Siedler fehlen vor Ort“. Genau deshalb hat er keine
Angriffe getestet. Das ist keine Fehlbedienung, sondern eine **fehlende Vorwarnung**: die Oberfläche
sagt beim Bauen nicht, dass Siedler der Engpass sind und dass Gebäude sie dauerhaft binden.

---

## 2. Seine Kritik (seine Worte, unverändert übernommen)

> „ich hätte gerne einen balken um die menge der zu produzierenden einheiten schöner einstellen zu“
> können weil ich bisher alle einzeln machen muss auch bei z.b. 200 Bürgerwehr einheiten aufträgen.
> Wenn die ressourcen vorhanden sind und die vorraussetzungen stimmen ist es damit leichter für die
> benutzeroberfläche.„“

> „ich erkenne auf der baukarte durch die aktuellen gebäude symbole nicht sofort welches gebäude dort“
> steht und ich weiß es gibt aus der anleitung original icons für gebäude die verwendet werden können.
> ich will auch pro dorf eine schöne übersicht welche gebäude auf dieser karte aktuell errichtet
> sind. Wie viele davon und was es an produktion ausmacht.„“

> „die ressourcen icons ganz oben gefallen mir immer noch nicht obwohl wir auch originale vorgaben“
> haben.„“

> „fürs spielgefühl … ist es aktuell ein langweiliges unübersichtliches erlebnisloser vorgang von“
> allen produktionsgebäuden einfach nur möglichst schnell alle möglichen zu bauen. Die überlegung von
> welchem Gebäude ich wie viel bauen sollte damit ich meine eigenen spielziele verfolgen kann …
> kann durch übersichtliche gezielte informationen neben der karte solche gedanken unterstützen und
> triggern dafür brauchen wir ein gut durchdachtes konzept von design weil auch viele neuerungen an
> felder entstanden ist. die … entsprechen funktional komplett meinen wünschen … aber noch nicht
> designtechnisch am richtigen platz … die menüpunkte haben teils unterschiedliche formatierungen
> links.„“

> „Zum spielablauf habe ich aktuell nichts zu bemängeln aber da ich mit den möglichkeiten bei der“
> truppen produktion unzufrieden war habe ich auch keine angriffe getestet.„“

---

## 3. Daraus die Arbeitspakete (mit Beleglage und Reihenfolge)

| # | Paket | Inhalt | Warum jetzt |
|---|---|---|---|
| **A-1** | **Einheitenmenge in einem Auftrag** | Statt 200 Einzelklicks: Zahlfeld + „−/+“-Schritt + Schieberegler, Vorschau „200 × Bürgerwehr = Kosten/Nahrung/Siedler/Ausrüstung; davon bezahlbar: N“, Kern `spieloekonomie.ausbildung_start(anzahl=N)` (Warteschlange bleibt EIN Auftrag je Werkstatt, Plätze je Stück), Meldung nennt die tatsächlich gestartete Menge | Klein, sofort spürbar; ohne das ist keine Armee machbar (Daniels Punkt 1) |
| **A-2** | **Gebäude-Icons auf der Siedlungskarte** | Original-Icons aus dem Handbuch statt Platzhalter; je Gebäudeart ein erkennbares Zeichen, Ausbaustufe klein sichtbar | Daniels Punkt 2a — er erkennt seine eigene Stadt nicht |
| **A-3** | **Dorfübersicht: was steht da, wie viel, was bringt es** | Eine Tabelle je Siedlung: Gebäudeart · Anzahl · Ausbaustufen · Stundenertrag · Siedler belegt · Anteil am Ortsertrag; darunter Summenzeile. Quelle: bebaute Felder + `data/buildings.json` (dieselbe Rechnung wie `wirtschaft`) | Daniels Punkt 2b — das ist der Hebel für „welches Gebäude wie viel baue ich“ |
| **A-4** | **Ressourcen-Icons oben** | Originalvorlagen aus dem Handbuch (die 7 Icon-Sheets liegen in `assets/`; 9 Rohstoffe zuschneiden wie die Einheiten) statt Emoji | Daniels Punkt 3 |
| **A-5** | **Designkonzept Siedlung** | Ein durchdachtes Layout: Karte in der Mitte, **rechts ein „Berater“-Panel** mit gezielten Kennzahlen (Engpass, Ertrag je Rohstoff, Siedlerreserve, offene Bedingungen), links **einheitlich formatierte Menüpunkte**; „was fehlt mir für mein Ziel“ statt „baue alles“ | Daniels Kernkritik (Spielgefühl). **Das ist ein Konzeptauftrag, keine Kleinigkeit** — erst Papier, dann bauen |
| **A-6** | **Siedler-Vorwarnung beim Bauen** | Beim Bauen zeigt die Oberfläche, wie viele Siedler das Gebäude dauerhaft bindet und wie viele frei bleiben; Warnung, wenn die Reserve unter die Ausbildungsgrenze fällt | Befund aus Abschnitt 1 (10 → 3,5 Siedler, sechs Fehlversuche) |

**Reihenfolge, die ich vorschlage:** **A-1 → A-3 → A-6 → A-2 → A-4 → A-5.** Begründung: A-1 macht
Armeen überhaupt erst möglich (und damit den Kampf testbar), A-3 und A-6 beantworten die Frage „wie“
viel baue ich„ mit Zahlen aus den Daten, A-2/A-4 sind Optik mit Originalvorlagen, A-5 ist der große“
Designwurf und sollte auf dem dann stehenden Fundament sitzen — sonst gestaltet man zweimal.

**Nicht vergessen (bestehende Punkte bleiben davor oder dahinter):** Sperre bei Nahrungsnot ist
gebaut; offen bleiben Sofortangriff reist, Kampfplanungsseite, F-03/F-05/F-06/F-07/F-11/F-13,
P3.4/P3.6, P4/P5/P1, F-12. **Bots: vertagt** (Register 72). **Kartenziehung: Entscheidung C, noch
nicht gebaut** (Register 75).

---

## 4. Was „erste spielbare DEMO für Windows auf GitHub“ braucht

1. **A-1** (ohne Mengenwahl keine Armee → kein Kampf testbar),
2. **A-3 + A-6** (sonst wiederholt sich genau diese Runde: alles zubauen, Siedler weg, nichts geht mehr),
3. **A-5 in einer ersten Fassung** (einheitliche Menüzeile links + Berater-Panel rechts),
4. die offenen Funktionspunkte, die Spielstand oder Kampf berühren: Sofortangriff reist, F-03 (Portal),
5. ein sauberer Durchlauf **ohne Admin-Aufstockung** als Abnahmekriterium: Startkarte → 2. Siedlung →
   erste Armee → erster Angriff → Speichern/Laden,
6. `main` bleibt unberührt; Veröffentlichung auf dem Stand-Branch (Entscheidung 12).
