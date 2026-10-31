# Anforderungen Daniel — Gebäude-Menüs, Ausbildung, Bibliothek, Kampf (30.10.2026)

**Stand der Umsetzung (30.10.2026, nachts):**
**ERLEDIGT:** A1 (Stellmacher-Menü ab Gebäude), A2 (Karren im Stellmacher), A3 (Truppen in der
Kriegerakademie), A4 (eigene Ansicht je Gebäude: Stellmacher, Diebesgilde, Kaserne),
A6 (Karren nicht mehr in der Truppenausbildung), B1 (Forschung erst ab Bibliothek),
B2/B3 (letzte Bibliothek nicht abreißbar), zwei Navigationsebenen wie im Original,
Menüpunkt „Voraussetzungen", „Eure Punkte" dauerhaft in der Leiste.
**OFFEN:** A5 (Forschungsstufen erweitern die Auswahl — die Sperre wird schon erklärt, die
Freischaltung selbst ist über `data/units.json` vorhanden, aber nicht im Spiel durchgespielt),
A7 (ein Hersteller je Karte — im Code durchgesetzt, Handbuch bestätigt „eine Bibliothek je
Siedlung", für die übrigen Gebäude offen), B4 (Original: eine Bibliothek **je Siedlung**, keine
Gesamtgrenze — Daniels Zwei-Grenze ist strenger und bleibt als seine Entscheidung stehen),
C1–C7 (Kampf, Portal, Wegzeiten, Planungsplattform: unverändert offen).

**Zweck:** Daniels Ansagen im Wortlaut festhalten, bevor gebaut wird. Jeder Punkt hat eine Kennung,
einen Beleg („Daniel, 30.10.2026") und eine Spalte „Beleglage", damit niemand später raten muss,
was Vorgabe war und was gemessen ist.
**Regel:** Was hier als „offen" steht, wird aus den Originaldokumenten (`docs/original/`) geklärt —
nicht erfunden.

---

## A. Gebäude werden Menüpunkte (Oberflächen-Struktur)

| Kennung | Anforderung (Daniel) | Beleglage |
|---|---|---|
| A1 | Sobald ein **Stellmacher** auf der Karte steht, erscheint **links im Menü** ein Menüpunkt „Stellmacher". | Vorgabe Daniel. Heute gibt es diesen Menüpunkt nicht. |
| A2 | Im Stellmacher-Menü werden **Karren produziert** — wenn Pferde bzw. die nötigen Rohstoffe vorhanden sind. | Vorgabe Daniel; Kosten je Karren stehen belegt in `data/units.json` (Handkarren: holz 100, metall 15, leder 15, wolle 15, siedler 1; Siedlerkarren zusätzlich Wagenbau 1). |
| A3 | **Truppen** werden in der **Kriegerakademie** ausgebildet — „genau wie in den Spielunterlagen beschrieben". | Vorgabe Daniel; `data/units.json` Feld `gebaeude` führt die Ausbildungsstätte je Einheit. |
| A4 | Dasselbe Muster gilt für **jedes** Ausbildungs-/Herstellergebäude (Bogenmacher, Diebesgilde, …): sobald gebaut, eigener Menüpunkt, die Angelegenheiten des Gebäudes passieren **dort**. | Vorgabe Daniel. |
| A5 | **Neu freigeschaltete Forschungsstufen erweitern die Auswahl** der Einheiten, die man bauen darf — im gleichen Stil. | Vorgabe Daniel; Voraussetzungen stehen in `data/units.json` (`voraussetzung`). |
| A6 | Handkarren und Siedlerkarren gehören **ausschließlich** in den Stellmacher, nicht in eine allgemeine Truppenausbildung. „Weil man zuvor ja noch gar keine produzieren kann." | Vorgabe Daniel (Korrektur seiner ersten Formulierung). |
| A7 | Je **ein** Stellmacher / Bogenmacher / Item-Hersteller pro Karte genügt; **mehrere** machen nur bei Farm und Pferdezucht Sinn (Produktionserhöhung). | Vorgabe Daniel, Kennzeichnung „glaube ich". **Gegen das Handbuch prüfen**, bevor festgeschrieben. |

## B. Bibliothek und Forschung

| Kennung | Anforderung (Daniel) | Beleglage |
|---|---|---|
| B1 | Der Menüpunkt **Forschung existiert erst**, wenn eine **Bibliothek** errichtet wurde. | Vorgabe Daniel. |
| B2 | Es muss **immer mindestens eine Bibliothek** stehen — „man darf die letzte nicht abreißen, da die Bibliothek essenziell ist". | Vorgabe Daniel. |
| B3 | Man darf eine **zweite woanders** bauen und **dann die erste abreißen** — aber nie die letzte. | Vorgabe Daniel. |
| B4 | **Offen:** gilt die Regel „mindestens eine Bibliothek" **pro Karte** oder **pro Spieler insgesamt**? | Aus den Originaldaten klären (`docs/original/`), nicht raten. |

## C. Kampf, Gegner, Planung

| Kennung | Anforderung (Daniel) | Beleglage |
|---|---|---|
| C1 | Daniel will **mit ausgebildeten Truppen selbst kämpfen**, um die Abläufe zu sehen und zu erkennen, wo optimiert werden muss. | Vorgabe Daniel. |
| C2 | Ein Kampf ist derzeit **nicht sinnvoll eingerichtet**: Gegner lassen sich weder **auswählen** noch **finden**. | Befund Daniel; deckt sich mit dem Spielstand (0 Einheiten, keine Bot-Kontakte). |
| C3 | Das **Portal** funktioniert noch nicht so, dass es diese Wege eröffnet. | Befund Daniel; im Spielstand: „Zu wenig Mana in einer Siedlung: 5000 benötigt, 0.0 vorhanden" (Portal kostet 5000 Mana, belegt in der Spielanleitung 2005). |
| C4 | Die **Lage der 6 Karten/Siedlungen** ist ungeklärt: wie wird entschieden, wo sie liegen, und daraus folgen die **Wegzeiten** der Gegner zu meinen Dörfern. | Offen. Belegt ist: **6 Siedlungen** (Handbuch Z. 58/311-312), Karten vergibt das Original **per Zufall** (Z. 313); Weltmodell X/Y/Z, 20 Dimensionen à 400 Felder, eigene Welt grün / fremde rot (`docs/original/Spielanleitung_2005/portal.php.txt`). Was daraus für Wegzeiten folgt: **nicht belegt, zu klären**. |
| C5 | **Wegzeiten müssen in Echtzeit sichtbar sein**, während Truppen unterwegs sind — inklusive **wohin**. | Vorgabe Daniel. Heute existiert `movements` im Spielstand, aber leer; eine Anzeige fehlt. |
| C6 | Es braucht eine **übersichtliche Plattform zum Planen** von Angriffen und Kriegen. | Vorgabe Daniel. |
| C7 | Grundlage: „mit dem bereits vorhandenen Wissen sollten wir das gut hinkriegen" — die Originaldokumente liefern die Hinweise, an denen wir uns halten. | Daniel; Quellen liegen in `docs/original/`. |

---

## Vorschlag zur Reihenfolge (Koordinator, 30.10.2026)

1. **A1–A6 + B1–B3 zuerst** — reine Oberflächen- und Sperrlogik auf vorhandenen Daten. Sichtbarer
   Fortschritt, kein neues Weltmodell nötig. Voraussetzung: Entwurf
   `docs/ENTWURF_AUSBILDUNG_HERSTELLER_20261030.md` (starkes Modell) ist da.
2. **A7 + B4** gegen das Handbuch klären (ein Hersteller je Karte, Bibliothek pro Karte oder Spieler).
3. **C4** (Lage der Karten und Wegzeiten) aus den Originaldaten klären — das ist die Grundlage für C5/C6.
   Ohne C4 keine ehrliche Wegzeit.
4. **C5 + C6** (Anzeige und Planungsplattform), **dann** C1–C3 (echter Kampf gegen auffindbare Gegner).

## Was ausdrücklich NICHT passiert

- Keine Wegzeit und keine Gegnerposition wird erfunden. Fehlt eine Angabe in den Originaldokumenten,
  wird sie auf `null` gesetzt und begründet — wie es die Projektregel seit dem 04.10.2026 verlangt.
