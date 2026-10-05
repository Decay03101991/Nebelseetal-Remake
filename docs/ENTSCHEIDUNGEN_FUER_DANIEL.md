# Entscheidungen für Daniel

**Zweck:** die drei offenen Entscheidungen des Remakes `D:\Arbeiten\Nebelseetal_Remake` in je rund
einer Minute beantwortbar machen. Jede Zahl nennt ihre Fundstelle (Datei + Zeile). Eigene Vorschläge
sind als **VORSCHLAG** mit Ableitung gekennzeichnet; wo das Handbuch schweigt, steht **nicht belegt**.

**Stand:** 05.10.2026, 14:02 (mit `date` geprüft).

**Status:** erzeugt vom Unteragenten, vom Koordinator an den Kernzahlen nachgeprüft — und
**beantwortet**: Daniel hat am 05.10.2026 um 14:24 entschieden (siehe „Antworten" am Ende).
Die Zahlen der Vorlage wurden stichprobenartig nachgerechnet und stimmen
(`punkte.VORSCHLAG_ZIEL_PUNKTE = 300`, `punkte.sieg_oder_niederlage()`, `spielzeit.STANDARD_FAKTOR = 180`,
`data/spielzeit.json` „belegt": false).

---

## 1. Zeitfaktor — ×180 bestätigen oder anderer Wert?

**Frage:** Soll die Spieluhr weiter ×180 laufen (1 Spielstunde = 20 echte Sekunden), oder ein anderer Wert?

**Heute eingestellt:** Faktor **180**, wählbare Stufen ×1/×20/×60/×180/×600 — `data/spielzeit.json`
Z. 2–9; `src/spielzeit.py` Z. 30–31 (`STANDARD_FAKTOR = 180.0`, `STUFEN = (1, 20, 60, 180, 600)`).

**Was die Quellen sagen:**
- Der Faktor ist **nicht belegt**: `src/spielzeit.py` Z. 16–17 („Nicht belegt — das Handbuch kennt
  keinen Zeitfaktor für eine Einzelspieler-Fassung") und `data/spielzeit.json` Z. 10 (`"belegt": false`).
  Das Handbuch kennt nur Echtzeit 1:1 (1 Spielstunde = 1 echte Stunde): `Spielanleitung_2009_Textfassung.txt` Z. 25–30.
- Herkunft des Werts: Daniel sah „keinen regelmäßigen Rohstoffeingang" — Zitat `docs/ENTWICKLUNGSPROTOKOLL.md` Z. 110.
  Vorher rechnete `tick` 1 Echtzeitsekunde = 1 Spielsekunde, also 4 Holz je **echter** Stunde
  (`src/spielzeit.py` Z. 4–7; `PROJEKT_STAND.md` Z. 71). ×180 macht daraus 12 Holz je echter Minute.
- Der Wert stammt als VORSCHLAG aus dem Entwurf: „1 Spielstunde = 20 echte Sekunden" —
  `docs/audits/entwurf_ausruestung_forschung_haus_2026-10-05.txt` Z. 102. Im Original entspricht das
  einem Speedserver 200× (`docs/PLAN_AUS_HANDBUCH.md` Z. 255); dort ist der Zeitfaktor ausdrücklich
  als offene Entscheidung Daniel vermerkt (Z. 49, 272).
- Die Handbuchformeln bleiben **unangetastet**, nur die Spieluhr läuft schneller (`src/spielzeit.py`
  Z. 9–11). Umstellbar in den Einstellungen, angewandt an genau einer Stelle (`_tick_loop`), Kopfzeile
  „Tempo ×180 · 1 Std = 20 s" (`PROJEKT_STAND.md` Z. 71).

**Optionen:**
- A) **×180 bestätigen.** Folge: Bau, Forschung und Wege sind in Sekunden bis wenigen Minuten erlebbar; kein Handbuchwert wird verändert.
- B) **anderer fester Wert** (z. B. ×60 = 1 Spielstunde je Minute; ×600 = 1 Stunde je 6 s). Folge: gleiche Wirkung, nur feiner/grober — muss vor dem nächsten `.exe`-Bau gesetzt werden.
- C) **×1 Originaltempo** als Standard. Folge: der Rohstoffeingang ist wieder praktisch unsichtbar (Daniels ursprünglicher Befund).

**Empfehlung:** A) ×180 — behebt genau den gemeldeten Befund, bleibt umstellbar, tastet keine Handbuchformel an.

---

## 2. Die neun Geländeregeln — bestätigen oder ändern?

**Frage:** Soll jedes der neun Gebäude ohne belegte Geländeregel auf den vorgeschlagenen Geländearten
stehen dürfen (im Nebelsee keines von ihnen)?

**Heute eingestellt:** `data/buildings.json` — jedes der 20 Gebäude hat ein Feld `nur_auf`.
**Belegt** sind 11 Regeln (Sumpf für alle gesperrt · Bibliothek · Tempel · die Produktionsgebäude aus
der Ertragstabelle). Die **neun übrigen** sind mit `"nur_auf_belegt": false` als VORSCHLAG markiert
(Sammeltext Z. 400–405; `PROJEKT_STAND.md` Z. 76).

**Was die Quellen sagen:** Das Handbuch nennt für keines dieser neun eine Geländeregel. Belegt ist nur:
„Sümpfe sind unbebaubar" (`Spielanleitung_2009_Textfassung.txt` Z. 380–381) und die Bibliothek „nur
auf Grasland, Steppe oder Nebelseen" (Z. 403). Für die Ausbildungsgebäude nur „je eines je Siedlung"
(Z. 504–506). Für alle neun gilt daher: Gelände **nicht belegt**. Die 2005er Fassung sagt ebenfalls
kein Gelände (`Spielanleitung_2005/beschreibung.php.txt`).

Die neun Zeilen (Kennung = `id` in `data/buildings.json`):

1. **Haus** (`haus`) — VORSCHLAG: Grasland, Steppe, Wald, Hügel (Z. 374–379). Handbuch: nur „+5 Siedlergrenze je Haus" (Z. 384), kein Gelände.
2. **Lager** (`lager`) — VORSCHLAG: Grasland, Steppe, Wald, Hügel (Z. 390–395). Handbuch: Lager ist ein Siedlungsmenüpunkt, ein eigenständiges Bauwerk ist nicht belegt (Z. 389).
3. **Schmiede** (`schmiede`) — VORSCHLAG: Grasland, Steppe, Hügel, Berg (Z. 178–183). Handbuch: kein Gelände.
4. **Bogenbauer** (`bogenbauer`) — VORSCHLAG: Grasland, Steppe, Wald, Hügel (Z. 196–201). Handbuch: kein Gelände.
5. **Nähstube** (`naehstube`) — VORSCHLAG: Grasland, Steppe, Wald (Z. 213–217). Handbuch: kein Gelände.
6. **Kriegerakademie** (`kriegerakademie`) — VORSCHLAG: Grasland, Steppe, Hügel (Z. 229–233). Handbuch: nur „eines je Siedlung" (Z. 504).
7. **Diebesgilde** (`diebesgilde`) — VORSCHLAG: Grasland, Steppe, Wald (Z. 245–249). Handbuch: nur „eines je Siedlung" (Z. 504).
8. **Stellmacher** (`stellmacher`) — VORSCHLAG: Grasland, Steppe, Wald, Hügel (Z. 262–267). Handbuch: nur „eines je Siedlung" (Z. 504).
9. **Verteidigungswall** (`verteidigungswall`) — VORSCHLAG: Grasland, Steppe, Wald, Hügel, Berg (Z. 341–347). Handbuch: kein Gelände.

**Optionen:**
- A) **alle neun Vorschläge bestätigen.** Folge: der Nebelsee bleibt nur für Bibliothek und Tempel bebaubar; die Regeln greifen sofort (nur diese Datei).
- B) **einzelne ändern** (je Gebäude `nur_auf` anpassen, oder `null` = überall außer Sumpf). Folge: sofort wirksam; nach einer Datenänderung ist ein `.exe`-Neubau nötig (`PROJEKT_STAND.md` Z. 116).
- C) **alle offenen Regeln streichen** (`null`). Folge: nur die belegten Regeln bleiben — die meisten Gebäude wären fast überall baubar.

**Empfehlung:** A) alle neun bestätigen — erfüllt Daniels Vorgabe „intelligent auf alle Gebäude
angewendet", ohne einen unbelegten Wert zu erfinden.

---

## 3. Sieg- und Niederlagebedingung — heute nicht definiert

**Frage:** Wann ist die Partie gewonnen, wann verloren?

**Heute eingestellt:** `main.is_defeated()` (`src/main.py` Z. 590–591) ist **unerreichbar**: es verlangt,
dass der Kontinent nicht mehr aktiv ist, aber `destroy_map` schützt den Kontinent ausdrücklich
(Z. 579–582). Beleg: `docs/PLAN_Einzelspieler.md` Z. 53.

**Was die Quellen sagen:**
- **Das Handbuch nennt keine Sieg- oder Niederlagebedingung.** Das „Spielziel" ist ausdrücklich offen:
  „Jeder hat bei Nebelseetal sicher seine eigenen Ziele" (`Spielanleitung_2009_Textfassung.txt` Z. 46–54;
  ebenso `Nebelseetal_Spielanleitung_2009.pdf` Z. 37–41). Es gibt keinen Abschnitt „Spielende", „Sieg"
  oder „Niederlage" — weder 2009 noch in der 2005er Fassung (`Spielanleitung_2005/beschreibung.php.txt`).
- Belegt sind **Punkte** und **Ruhmeshalle** (Rangliste: „wie stark andere Spieler sind", Z. 97–99):
  Forschungspunkte = Summe der Stufen³, Kriegspunkte = Einheitenwerte + Wallstufe³,
  **Gesamtpunktzahl = (Krieg + Forschung) / 2** (`ORIGINAL_Kampf_und_Punkte.md` Z. 104–121).
- Eine **feindliche Siedlung wird nicht zerstört**, nur geplündert: „beginnen diese die Siedlung zu
  plündern" (Z. 1332). Eine eigene Siedlung kann man freiwillig **aufgeben** — dann sind alle Einheiten,
  Waren und Gebäude verloren (Z. 320–325). Ein „Verlust aller Siedlungen" ist im Handbuch **nicht** als
  Niederlage definiert (**nicht belegt**).
- Der Code enthält bereits einen als VORSCHLAG gekennzeichneten Ansatz: `src/punkte.py` Z. 213–242 —
  Niederlage bei „keine Siedlung und keine Einheit", Sieg bei erreichter Zielpunktzahl, Vorgabe **300**
  (`VORSCHLAG_ZIEL_PUNKTE`, Z. 46). Auch der Plan fragt: „Sieg über alle vier Nebenwelten + Punktzahl,
  oder reine Punktwertung?" (`PLAN_AUS_HANDBUCH.md` Z. 277); der Entwurf nennt dasselbe
  (`entwurf_ausruestung_forschung_haus_2026-10-05.txt` Z. 119).

**Optionen (alle VORSCHLAG — abgeleitet aus belegten Punktearten und dem Siedlungsverlust):**
- A) **Punkteziel.** Sieg, sobald `(Kriegs- + Forschungspunkte) / 2` eine Schwelle erreicht (Code-Vorgabe
  300); Niederlage, wenn keine Siedlung **und** keine Einheit mehr übrig sind. Ableitung: beide Größen
  sind belegt, und „alle Siedlungen aufgeben" löscht alles (Handbuch Z. 320–325). Folge: sofort spielbar,
  die Partie bekommt ein Ende; die Schwelle 300 ist willkürlich und sollte Daniel bestätigen.
- B) **Nebenwelten + Punkte.** Sieg erst nach Erreichen/„Eroberung" aller Nebenwelten **und** Punktziel —
  wörtlich eine der beiden Plan-Alternativen (`PLAN_AUS_HANDBUCH.md` Z. 277). Folge: längeres,
  „imperiales" Spiel; braucht aber eine Kontinent-/Welt-Mechanik, die heute fehlt.
- C) **kein Ende.** Reine Punkte-Rangliste wie das Original, das kein Spielende kennt. Folge: kein Bruch
  mit dem Original, aber genau der heute unbefriedigende Zustand.

**Empfehlung:** A) Punkteziel mit bestätigter Schwelle — der einzige Vorschlag, der heute schon im Code
steht, aus belegten Punkten abgeleitet ist und der Partie ein Ende gibt.

---

## Antwort bitte so:

Zeitfaktor: [ ] ×180  [ ] anderer Wert: ______

Geländeregeln (neun): [ ] alle bestätigen  [ ] einzelne ändern (welche? ____________________)

Sieg/Niederlage: [ ] A Punkteziel (Schwelle ____)  [ ] B Nebenwelten + Punkte  [ ] C kein Ende

---

## Belege — wirklich gelesen

- `data/spielzeit.json` Z. 2–12 (Faktor 180, Stufen, `belegt: false`) · `src/spielzeit.py` Z. 16–46 (`STANDARD_FAKTOR=180`, Vorgabe/Belegstand).
- `data/buildings.json` Z. 178–397 (`nur_auf` je Gebäude) und Z. 400–405 (Sammeltext `_gelaenderegeln_vorschlag`).
- `src/main.py` Z. 590–591 (`is_defeated()`), Z. 579–582 (`destroy_map`, Kontinent-Schutz).
- `src/punkte.py` Z. 46 (`VORSCHLAG_ZIEL_PUNKTE = 300`), Z. 213–242 (`sieg_oder_niederlage`), Punkteformeln.
- `docs/PROJEKT_STAND.md` Z. 63, 71 (Zeitfaktor), 76 (Geländeregeln), 102–107, 116, 425–433 (offene Punkte).
- `docs/ENTWICKLUNGSPROTOKOLL.md` Z. 110 (Schritt 28, Befund und wörtliches Zitat).
- `docs/PLAN_AUS_HANDBUCH.md` Z. 46–49, 255, 270–277 (Speedserver 200× ↔ Zeitfaktor, offene Entscheidungen).
- `docs/PLAN_Einzelspieler.md` Z. 53 („`is_defeated()` ist unerreichbar").
- `docs/audits/entwurf_ausruestung_forschung_haus_2026-10-05.txt` Z. 102 (Zeitfaktor 1:20), Z. 119 (Sieg/Niederlage).
- `docs/original/Spielanleitung_2009_Textfassung.txt` Z. 46–59 (Spielziel), 97–99 (Ruhmeshalle), 279–281, 320–325
  (Siedlung aufgeben), 337–373 (Ertragstabelle), 377–386 (Sumpf/Grenze), 400–404 (Bibliothek), 504–506
  (Ausbildungsgebäude), 1273–1334 (Kampf/Plündern).
- `docs/original/ORIGINAL_Kampf_und_Punkte.md` Z. 104–121 (Punkte), Z. 125–153 (Schutz/Siedlungen).
- `docs/original/Nebelseetal_Spielanleitung_2009.pdf` Z. 1–60 (Anfang, u. a. Spielziel Z. 37–41 — entspricht der Textfassung).
- `docs/original/Spielanleitung_2005/beschreibung.php.txt` + `.../punktesystem.php.txt` (2005er Fassung: kein Spielende).
- `docs/original/00_QUELLEN.md` (Herkunft/Stand der Originaldateien).

**Grenzen:** Der PDF-Volltext ist nicht durchsuchbar (Binärdatei); die zitierbare Prüfung lief über die
Textfassung `Spielanleitung_2009_Textfassung.txt` (laut `00_QUELLEN.md` dieselbe Anleitung). Keine weitere
`ORIGINAL_*.md` enthält eine Sieg-/Niederlage- oder Geländeregel-Angabe.

---

## Antworten (Daniel, 05.10.2026, 14:24 — festgehalten vom Koordinator)

| Frage | Daniels Entscheidung | Zustand |
|---|---|---|
| 1 Zeitfaktor | **×180 so lassen** (1 Spielstunde = 20 Sekunden) | nichts zu ändern, Wert steht so |
| 2 Die neun Geländeregeln | **alle neun so lassen** | in `data/buildings.json` als `_bestaetigt` eingetragen |
| 3 Sieg-/Niederlagebedingung | **Vorschläge abwarten** — diese Vorlage zuerst vorlegen | **offen**, siehe unten |

Zusätzlich an dem Tag entschieden (nicht Teil dieser Vorlage): die **Lichtfarbe** wird getrennt (Wald
bekommt `#6A7E6C`, aus seiner Grundfarbe gerechnet) und das **Kartenmaß** wird **8×7 = 56 Felder,
davon 40 bebaubar**.

**Noch vorzulegen:** die drei Optionen zu Sieg/Niederlage aus Abschnitt 3 — Empfehlung des Autors ist
A) Punkteziel (Schwelle im Code heute 300, `src/punkte.py`).
