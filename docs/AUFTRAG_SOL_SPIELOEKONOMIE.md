# Auftrag an ein starkes Modell: Spielökonomie, Kartenwahl und Handel (Nebelseetal-Remake)

**Erstellt:** 05.10.2026 durch den Koordinator. **Auftraggeber:** Daniel Kössl.
**Warum ein starkes Modell:** Daniel hat ausdrücklich gesagt: „benutze starke modelle um diese logik
auszubauen und auf unseren code anzuwenden … Das muss gut werden!" — hier geht es um Spielbalance und
Architektur, nicht um Textarbeit.

---

## 1. Deine Aufgabe

Entwirf die **Spielökonomie** des Remakes so, wie Daniel sie beschrieben hat (Abschnitt 2), und **wende
sie auf den vorhandenen Code an**: ein umsetzungsreifer Plan mit **echtem Code je Datei/Funktion**.

Du bist **Berater und Architekt**, nicht der Ausführende: **du änderst KEINE Projektdatei** außer der
einen Ausgabedatei (Abschnitt 6). Kein `git`, kein Commit, keine Tests ausführen (dürfen aber gelesen
werden).

## 2. Daniels Vorgabe (wörtlich, das ist die Richtschnur)

> es soll nicht darauf aufbauen, wer schneller ist gewinnt, sondern taktische handel zwischen eigenen
> siedlungen und die auswahl der richtigen karten (was schon teuer sein muss, eine neue karte
> besiedeln zu dürfen, inklusive minimum rohstoff Guthaben das man braucht um eine neue Siedlung
> gründen zu können. ) Also anfangs ist schon wichtig schnell alle verfügbaren karten mit jeweils den
> rohstoff vorteilen zu sichern die man am ende nutzt um durch handel verschiedene städte zu stärken.
> Nur auf der anfangs map soll es ausgeglichene Rohstoffe geben um theoretisch alles zu produzieren.
> In den möglichen karten von neu Gründungen soll es nur 2 oder 3 start map ähnlich ausgeglichene
> karten geben, die anderen karten sollen eher Minen und Steinmetze bevorzugen oder Farmen oder holz
> oder mischungen aus zweien und von dem dritten fast nichts. aber es muss so gebalanced sein, dass
> Rohstoffproduktion und handel die grundlage für stabile starke truppen aufbau und entwicklung sowie
> forschung bieten.

## 3. Harte Randbedingungen (nicht verhandelbar)

1. **Das Original-Handbuch 2009 ist die Richtschnur.** Alles stammt daraus oder aus belegten Quellen
   (`docs/original/`). Fehlt eine Angabe: Wert als **VORSCHLAG** kennzeichnen **mit Ableitung** —
   nichts „nach Gefühl" erfinden. Belegte Zahlen (Ertragstabelle S. 10, Preise, Siedlergrenze,
   Startwerte 100 Holz / 100 Stein / 10 Siedler) bleiben unangetastet.
2. **Sieben Geländearten** sind belegt (Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf).
   Erfinde **keine achte** — das würde eine Prüfzusage lockern und ist Daniels Entscheidung.
3. **Siedlungskarte: 8 × 7 = 56 Felder, davon genau 40 bebaubar, 16 gesperrt (nur Sumpf).**
   Das ist gerade gebaut und darf nicht wieder zerlegt werden.
4. **Mindestbesatz je Karte** (Wald 2, Berg 2, Grasland 3, Nebelsee 1) muss auch auf spezialisierten
   Karten halten — sonst ist eine Siedlung nicht spielbar. „Fast nichts" heißt also **Minimum, nicht
   Null**.
5. **Alles muss prüfbar sein.** Jede neue Regel braucht eine testbare Aussage (Zahl, Grenze,
   deterministisch aus der Saat). Kein Zufall ohne Saat.
6. **Deutsch** für alle Ausgaben (Code-Kommentare, Doku). Keine Emoji in Code oder Daten.
7. **Keine zweite Wahrheit:** Werte, die schon in `data/*.json` stehen, nicht im Code duplizieren.
8. Der vorhandene **Prüfstand bleibt grün**: der Sammellauf läuft heute mit **2665 bestanden,
   0 Fehler, 21 Befunde über 41 Dateien**. Nenne zu jeder Änderung, welche Prüfdateien mitziehen
   müssen.

## 4. Gemessener Ist-Zustand (nachlesen, nicht mir glauben)

| Thema | Wo | Stand heute |
|---|---|---|
| Geländearten, Kartenmaß, Kartentypen, Gewichte, Regeln | `data/gelaende.json` | 7 Arten · 8×7 = 56/40 · 5 Kartentypen mit Gewichten · Mindestbesatz · `sperrfelder: 16` |
| Kartenerzeugung | `src/gelaende.py`, `siedlungskarte_erzeugen`, `karten_typ`, `karte_profil`, `karte_beschreiben` | zieht 40 bebaubare + 16 gesperrte Felder getrennt nach Gewicht |
| Siedlung gründen | `src/main.py`, `_found_settlement`, `neue_siedlungskarte`, `SIEDLUNGEN_MAXIMUM = 6` | **kostenlos**, keine Mindestbestände, Kartentyp zufällig |
| Transport zwischen eigenen Siedlungen | `src/main.py`, `_transport_to_settlement` | vorhanden |
| Aufträge (Transport/Stationieren/Kampf) | `src/auftraege.py` (`auftragsarten`, `starten`, `ladung_der_mission`, `SEKUNDEN_JE_FELD`) | vorhanden, „Reisezeit" ist Vorschlag |
| Wirtschaft/Ertrag | `src/wirtschaft.py` (`siedlung_ertrag`, `ertrag_gesamt`, `kapazitaet`) | Ertrag ausschließlich aus bebauten Feldern |
| Gebäude, Preise, Wirkung | `data/buildings.json`, `data/baupreise.json`, `src/gebaeude_wirkung.py`, `data/gebaeude_wirkung.json` | 20 Gebäude, Haus = 80 Holz + 50 Stein (belegt) |
| Forschung | `data/research.json`, `src/forschung.py`, `src/forschungspfad.py` | 21 Originalforschungen, Dauer = Stufe² Stunden |
| Punkte/Sieg | `src/punkte.py`, `src/main.py` (`spielausgang`, `_pruefe_spielende`) | Punkteziel 300 ist **vorläufig** (Daniels neue Vorgabe löst den Wettlauf ab) |
| Bots/Handelspreis | `src/botkern.py` (`handelspreis`, `referenzpreis_aus_beschaffung`) | Handelspreis gibt es **nur für Bots**, nicht zwischen eigenen Siedlungen |
| Reise-/Wegzeiten | `src/spielzeit.py`, `src/auftraege.py` | Zeitfaktor ×180 (1 Spielstunde = 20 echte Sekunden) |

Zusätzlich lesenswert: `docs/PROJEKT_STAND.md`, `docs/ENTWURF_SPIELZIEL_HANDEL_KARTEN.md`,
`docs/ENTWURF_WIRTSCHAFT.md`, `docs/ENTWURF_AUFTRAEGE.md`, `docs/PLAN_AUS_HANDBUCH.md`.

## 5. Was du liefern sollst (genau diese Gliederung)

**A. Das Spielziel.** Wie gewinnt man, wie verliert man, wenn es kein Wettlauf sein soll? Nenne
**eine** Empfehlung plus eine Alternative, jeweils mit Begründung und der Zahl, die sie braucht.
Behandle auch: Was passiert, wenn ein Spieler alle Karten besiedelt hat? Was, wenn er eine Siedlung
verliert?

**Wichtig (Vorgabe Daniel 05.10.2026, 16:2x):** *„Natürlich soll man nicht gewinnen wenn man nur
unvorteilhafte karten auswählt."* Das Spielziel muss also **die Qualität der Kartenwahl** tragen: wer
nur unvorteilhafte Karten besiedelt, darf **nicht** gewinnen können. Sage, woran das im Code messbar
hängt (z. B. Punkte je Siedlung aus ihrem Kartenertrag, Versorgungsgrad, Handelssaldo) — nicht als
Gefühl, sondern als prüfbare Zahl.

**B. Kartenvorrat (die Auswahl der Karten).**
* Die **Startkarte** ist ausgeglichen: jeder der neun Rohstoffe muss theoretisch produzierbar sein.
* Danach ein **fester Vorrat** für Neugründungen: **2–3 ausgeglichene** Karten, die übrigen
  **spezialisiert** (Minen/Steinmetze · Farmen · Holz · und Mischungen aus zwei, beim dritten „fast
  nichts").
* Für **jede** Karte: vollständige `gewichte`-Tabelle über alle sieben Geländearten (Summe egal,
  Verhältnisse zählen), der daraus folgende **Vorteil in Zahlen** (Ertrag/h je Rohstoff) und die
  Prüfung, dass der **Mindestbesatz** und die **40/16-Aufteilung** halten.
* Sage, **wie viele** Karten/Siedlungen es geben soll und warum.

**C. Gründung einer neuen Siedlung.** Preis in Rohstoffen und Siedlern, **Mindest-Rohstoffguthaben**
vor der Gründung, Voraussetzungen (Forschung, freie Karte), und was passiert, wenn mehrere Spieler
dieselbe Karte wollen. Alle Zahlen als VORSCHLAG **mit Ableitung** aus den belegten Preisen
(Haus 80/50) und der Ertragstabelle. Rechne vor, wie lange ein Spieler auf eine Neugründung spart
(bei ×180).

**D. Handel zwischen eigenen Siedlungen.** Das ist der Kern. Entwirf: Warenpreise je Siedlung
(abhängig von ihrer Karte), Transportweg/Reisezeit (vorhandene Formel nutzen), Verluste/Risiko,
und warum Handel **besser** ist, als einfach alles selbst zu produzieren. Nenne die konkreten
Formeln und wo sie hingehören (`src/`-Modul, neue Datei oder bestehende erweitern).

**E. Balance-Nachweis.** Rechne an **einem** durchgerechneten Beispiel (Start → zweite Siedlung →
Handel → erste Ware → erste Einheit → erste Forschung) vor, dass die Zeiten und Mengen zusammenpassen
(mit ×180). Zeige, dass Truppenaufbau, Ausbau und Forschung aus Produktion **und** Handel getragen
werden — und wo es kippen würde.

**F. Umsetzungsplan.** Nummerierte, **einzeln prüfbare** Schritte. Je Schritt: betroffene Datei +
Funktion, die genaue Änderung **als Code** (vollständige Funktion oder präziser Diff), die neue
Prüfaussage und die Prüfdatei, die mitziehen muss. Reihenfolge so, dass der Prüfstand zwischen den
Schritten grün sein kann.

**G. Risiken und offene Punkte.** Was könnte Alt-Spielstände brechen? Was ist am neuen Entwurf
angreifbar? Welche Zahlen muss Daniel selbst entscheiden?

**H. Bots: die Schwierigkeit muss die Ökonomie kennen (Vorgabe Daniel 05.10.2026, 16:2x).**
Wörtlich: *„Schwierigere Bots müssen das wissen und danach handeln."* Entwirf je **Schwierigkeitsstufe**
(**leicht / mittel / schwer** — drei genügen, Vorgabe Daniel 05.10.2026) konkret:
* Wie ein Bot **Karten bewertet** (welche Kennzahl, aus welchen Daten — z. B. `karte_profil`,
  `wirtschaft.kapazitaet`) und danach **wählt oder ablehnt**.
* Wie ein Bot **Neugründungen** plant (Reihenfolge der Karten, Sparen auf den Gründungspreis) und ab
  welcher Stufe er das überhaupt tut.
* Wie ein Bot **handelt** (mit wem, zu welchem Preis, wann er Vorräte hortet oder verkauft) — nenne
  die Formeln und die Stellschrauben je Stufe.
* Wie ein Bot einen Spieler **bestraft, der nur unvorteilhafte Karten besiedelt** (z. B. schnelleres
  Vordringen auf die guten Karten, Preisdruck im Handel).
* Welche vorhandenen Bausteine dafür schon da sind (`src/botkern.py`: `handelspreis`,
  `referenzpreis_aus_beschaffung`, Temperament; `docs/ENTWURF_AUFTRAEGE.md`) und was fehlt.
* Jede Stufe braucht **prüfbare** Aussagen (z. B. „ab Stufe schwer siedelt der Bot innerhalb der
  ersten N Spielstunden auf der besten freien Karte") — keine Beschreibungen ohne Messgröße.

## 6. Ausgabe (genau eine Datei, sonst nichts ändern)

Schreibe deine Antwort nach:

```
D:\Arbeiten\Nebelseetal_Remake\docs\audits\entwurf_spieloekonomie_sol_2026-10-05.txt
```

Regeln für die Datei:
* Deutsche Sprache, klare Überschriften A–G, Tabellen wo Zahlen stehen.
* **Höchstens 1.200 Zeilen.** Lieber dicht und konkret als lang.
* Jede Zahl mit Herkunft: `[BELEGT: Quelle]` oder `[VORSCHLAG: Ableitung]`.
* Codeblöcke klar als Python kennzeichnen und mit Datei + Funktion überschreiben.
* **Keine** anderen Dateien anfassen, nichts löschen, nicht committen.

## 7. Was du NICHT tun sollst

* Keine achte Geländeart erfinden. Keine Bilddeutung. Keine Originaldateien umsortieren.
* Keine bestehende Prüfzusage lockern (z. B. „sieben Geländearten" in `tests/test_gelaende.py`).
* Keine Netz-Einträge, keine Multiplayer-Ideen — Einzelspieler bleibt Einzelspieler.
* Nicht behaupten, du hättest etwas gemessen, was du nicht gemessen hast.
