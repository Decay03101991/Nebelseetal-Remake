# Wirtschafts-Entwurf (astra, Einsatz 3) — Vorschlag zur Abnahme

**Einsatz 3 des Plans.** Modell `gpt-6-astra`, 4 m 12 s, Rohantwort in
`docs/audits/astra_wirtschaft_antwort.txt`. Alles hier ist **VORSCHLAG**, kein Originalwert —
das Handbuch nennt Erträge, aber **keine Preise und keine Ausbildungsdauern**.

---

## Die Kernzahl: das Handbuch-Tempo ist unspielbar

astra hat die belegten Formeln durchgerechnet (Kosten 50 Holz × 2^(n−1), Dauer n² Stunden)
und stellt sie einem gestauchten Modell gegenüber:

| Forschungsstufe | Handbuch (belegt) | Vorschlag (spielbar) |
|---|---|---|
| 1 | 50 Holz / **1 Stunde** | 10 Holz / 3 Minuten |
| 3 | 200 Holz / **9 Stunden** | 30 Holz / 27 Minuten |
| 5 | 800 Holz / **25 Stunden** | 50 Holz / 75 Minuten |
| 10 | 25.600 Holz / **100 Stunden** | 100 Holz / 5 Stunden |
| Summe 1–10 | 51.150 Holz / **385 Stunden** | 550 Holz / ~19 Stunden |

**Urteil von astra:** Die Verdopplung belohnt Warten und Massenproduktion; quadratische Zeiten
können Spezialisierung tragen — aber nur mit verkleinertem Zeitmaßstab und Warteschlange.

**Meine Einschätzung:** Das Original war ein Browsergame über Monate, und es hatte **Speedserver**
— Zeitbeschleunigung ist also im Original selbst angelegt, nicht meine Erfindung. Der saubere Weg:
die **Handbuchformeln bleiben die Regel**, und ein **Zeitfaktor** (wie der Speedserver) staucht sie.
Dann ist nichts erfunden, nur beschleunigt — und die Zahl ist ehrlich benannt.

## Weitere Vorschläge (alle abgeleitet, nicht gewürfelt)

- **Spieltag = 2 Echtzeitstunden** (zwölffache Produktion und Siedlerzuwachs); Forschung und
  Ausbildung behalten eigene Echtzeitdauern.
- **Baupreise**: abgeleitet aus dem Ertrag der Gebäude — eine „Referenz-Produzentenstunde" ist
  4 Holz oder 4 Stein (Normertrag eines guten Standorts); Basisproduktion bekommt 3 Arbeitsstunden
  Budget, Spezialproduktion 6, Werkstätten 10, Ausbildungsstätten 14.
- **Bauzeit**: je Gebäude 3 Minuten, mit **gemeinsamer Bauwarteschlange** (Ausbau wird zur
  Entscheidung statt zum Sofortklick).
- **Startkarte**: 40 nutzbare Bauplätze mit allen nötigen Geländearten.
- **Ausbildungsdauern** (Auswahl): Kurzbogenschütze 15, Armbrustschütze 45, Streuner 5,
  Waldläufer 55, Handkarren 5, Katapult 50 Minuten — gestaffelt nach Einheitentyp.
- **Pacing-Ziele**: nach 1 Stunde 8 Gebäude, 0 Einheiten, Baukunst 1; nach 1 Spieltag 24 Gebäude,
  1 Bürgerwehr + 1 Handkarren, ~13 Punkte; nach 3 Spieltagen 40 Gebäude, 6 Bürgerwehren,
  2 Kurzbogenschützen, 2 Handkarren, ~96 Punkte.
- **Die drei Engpässe**: Gold (416 Minuten Ansparzeit je Kämpfer bei einfacher Goldmine →
  deshalb zuerst Bürgerwehr statt Goldtruppen), Versorgung (125 Minuten Nahrung/Leder je
  Bürgerwehr → Lieferketten verbreitern statt Ausbildung beschleunigen), Forschung
  (270 Minuten für das letzte Meilensteinprofil).

**Ehrlicher Vorbehalt von astra selbst:** diese Meilensteine sind **Ziele**, keine durch eine
Ablaufsimulation belegten Erreichbarkeitsgarantien. Ich prüfe sie später im echten Spiel.

## Was ich dafür von Daniel brauche

1. **Zeitfaktor**: Spieltag = 2 Echtzeitstunden in Ordnung? (Alternativ: langsamer, näher am
   Original.)
2. **Forschungstempo**: Handbuchformeln **mit Zeitfaktor** (mein Vorschlag) oder die gestauchten
   Zahlen direkt?
3. **Baupreise**: aus dem Ertrag abgeleitete Preise übernehmen?
4. **Bauzeit 3 Minuten + Warteschlange**: einverstanden?

Ohne diese vier Antworten baue ich die Wirtschaft nicht — die Zahlen würden sonst von mir kommen,
und genau das soll nicht passieren.
