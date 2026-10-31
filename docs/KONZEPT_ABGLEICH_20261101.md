# Abgleich: Weltkartenmechanik-Konzept (01.11.2026) gegen den Code

**Eingang:** `docs/eingaenge/20261101_Lords_Mobile_Weltkartenmechanik.txt`
(SHA256 `9e06b2078ad343ca19b33e116f2f8a417b29ac648554da00d74fb68e3575ca35`, 325 Zeilen).
Das Dokument sagt selbst: keine verbindlichen Auftraege, Hermes entscheidet. Hier steht nur, was
**schon da** ist, was **fehlt** und was **im Weg steht** — gebaut wird erst nach Daniels Wort.

## 1. Was bereits existiert (gemessen im Code)

| Konzeptpunkt | Stand im Code | Beleg |
|---|---|---|
| Siedlung hat eine Weltposition | **vorhanden**: `Settlement.map_id`, `.x`, `.y` | `src/main.py` ~Z. 217-219 |
| Marschzeit aus Entfernung und Tempo | **vorhanden**: `auftraege.reisezeit_sekunden` | `src/auftraege.py` Z. 146, Formel Entfernung / Geschwindigkeit × `SEKUNDEN_JE_FELD` |
| Tempo der Gruppe | **vorhanden**: langsamste Einheit bestimmt das Tempo (`tempo_der_gruppe`) | `auftraege.py` Z. 118 |
| Missionsarten | **vorhanden**: stationieren, transportieren, handeln, angreifen | `auftraege.auftragsarten()` |
| Missionskosten (Gold, Nahrung, Mana) | **vorhanden**: `kosten_der_mission`, Saetze als VORSCHLAG gekennzeichnet | `auftraege.py` Z. 267 |
| Missionsstatus und Ankunft | **vorhanden**: `fortschritt`, `angekommen`, `_status` | `auftraege.py` Z. 440-510 |
| Bericht aus echten Ereignisdaten | **vorhanden**: `bericht()` und `spieldaten_anwenden()` | `auftraege.py` Z. 514-598 |
| Ladung und Fracht je Karren | **vorhanden** (mit Wagenbau-Bonus, Register 73) | `ladung_der_mission` |
| Buchung im LOKALEN Lager | **vorhanden** (Ortslager fuehrend seit Teil 3a) | `verbrauche_am_ort`, `ortsdeckung` |
| Portal zwischen Dimensionen | **vorhanden**: eigener Baustein `portalraum.py`, Dimensionen in `welt.py` | `portalraum`, `welt` |
| Karten mit Feldern und Koordinaten | **vorhanden**: Siedlungskarte A-H / 1-8, Weltkarte mit Feldern | `karten_optik_fein`, `welt_optik_fein` |

**Damit sind von den elf vorgeschlagenen Tests bereits abgedeckt:** C (Marschzeit aus Entfernung),
H (lokales Lager gegen Anzeige, in der Praxis durch Ortslager und Kopfzeile), I (atomare Ablehnung,
seit A-1 auch fuer Mengen), J (mehrere Siedlungen mit eigenem Startort).

## 2. Was fehlt (ehrlich, mit Aufwand)

| Luecke | Aufwand | Anmerkung |
|---|---|---|
| **Versetzung einer Siedlung** (gezielt, zufaellig, Portal) | mittel bis gross | Nur der Admin-Bereich kennt heute ein Verschieben (`admin_werkzeuge`); im Spiel gibt es keinen Weg. Die Position steckt schon in `Settlement`, die Innensicht (Bauten, Stufen, Lager, Warteschlangen) haengt NICHT an x/y — ein Versatz ist damit grundsaetzlich ohne Datenverlust moeglich. |
| **Spionage als Missionsart** | klein bis mittel | `auftraege.auftragsarten()` kennt vier Arten; Spionage kommt als fuenfte hinzu und nutzt Reisezeit, Kosten und Bericht mit. Bericht muss **datiert und eingefroren** sein (das Konzept verlangt es, und die Lehre aus der Schenkungs-Pruefung sagt dasselbe). |
| **Regel, wenn der Startort waehrend eines Marsches springt** | klein | Das Konzept laesst es offen. Vorschlag: Marsch behaelt seinen Startpunkt als **Schnappschuss**; die Rueckkehr geht an die AKTUELLE Position der Siedlung. Keine verlorenen Truppen, keine Doppelbuchung. |
| **Regel, wenn das Ziel waehrend des Anmarsches springt** | klein | Vorschlag: Angriff trifft das Feld, nicht die Siedlung — ist das Feld leer, kommt der Bericht „Ziel verzogen“, Truppen kehren um. |
| **Fruehwarnung** (herannahende Feinde) | mittel | Braucht einen Sichtradius und eine Anzeige; heute nicht vorhanden. |
| **Forschung, die Spionage verbessert** | klein | Andockstelle `forschung_wirkung`; das Handbuch nennt Spionageforschung — vor dem Bau in `docs/original` nachsehen, nicht raten. |

## 3. Wo das Konzept dem Projekt widerspricht

1. **KORRIGIERT am 01.11.2026 — meine erste Fassung war falsch.** Ich hatte geschrieben, ein
   Versetzen der Siedlung gebe es im Original nicht. `portalraum.py` führt aber den **belegten
   Koordinatenwechsel** (5.000 Mana, höchstens 1× je 24 Stunden, von EINER Siedlung; Quelle
   Portal-Anleitung 2005 und Handbuch 2009 S. 80–83). Es gibt das Ritual also, es ist nur nicht
   im Spiel erreichbar. Abweichung vom Original wäre ein **frei wählbares Springen ohne Ritual**
   — nicht das Ritual selbst. Details im Modell `docs/KONZEPT_SECHS_DOERFER_20261101.md`.
   Unverändert gilt: belegt ist ein **Portal zwischen den Welten**
   (`portalraum.py`, Handbuch); ein frei waehlbares Springen auf der Karte ist eine
   **Lords-Mobile-Mechanik**, keine Nebelseetal-Regel. Wenn Daniel sie will, ist sie eine
   bewusste Remake-Abweichung — wie schon bei der Siedler-Bindung (Register 80) und dort
   ausdruecklich als Abweichung gekennzeichnet. Sie darf nicht als „originalgetreu“ verkauft
   werden.
2. **Keine Zahl aus Lords Mobile uebernehmen.** Das Dokument sagt es selbst. Das Projekt hat eine
   harte Regel: keine Zahl ohne Quelle. Alle Werte (Abklingzeit, Manakosten, Sichtradius) waeren
   VORSCHLAG und muessten im Spieltest balanciert werden.
3. **Echtzeit ist im Remake Spielzeit.** Märsche laufen auf der Spieluhr (`spielsekunden`), nicht
   auf der Rechneruhr — und muessen Speichern/Laden ueberstehen (Test G). Das ist im Kern schon so
   geloest (`tick_bis`), muss aber fuer jede neue Missionsart geprueft werden.

## 4. Empfohlene Reihenfolge (nur Vorschlag, nicht freigegeben)

1. **Spionage als fuenfte Missionsart** — kleinster Schritt, nutzt alles Vorhandene, bringt sofort
   Spieltiefe und ist die Voraussetzung fuer „aufklaeren, dann angreifen“.
2. **Ziel- und Startort-Schnappschuss** in Missionen (Test E und F) — verhindert die instabilen
   Zielreferenzen, bevor irgendetwas springt.
3. **Portalversetzung** statt freiem Springen: dieselbe Mechanik wie das vorhandene Portal, mit
   Mana- und Forschungsbedingung. Das haelt die Abweichung klein und begruendbar.
4. **Fruehwarnung** zuletzt — sie braucht Sichtradius und Balancierung.

## 5. Was hier NICHT passiert ist

Nichts davon ist gebaut. Kein Wert wurde erfunden, keine Zeile Code angefasst. Der Abgleich ist
Lesearbeit am vorhandenen Stand; die Entscheidung ueber die Umsetzung liegt bei Daniel.
