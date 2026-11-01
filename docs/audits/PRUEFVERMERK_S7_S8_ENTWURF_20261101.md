# PRÜFVERMERK zum GPT-Entwurf S-7, S-8 und Demo-Einstieg

**Stand:** 01.11.2026, 17:45. **Papier:** `archiv/eingaben/20261101_gpt_antworten/HERMES_ENTWURF_S7_S8_DEMO_ANLEITUNG_20261101.md`
(Antwort auf `AUFTRAG_GPT_S7_S8_UND_DEMO_ANLEITUNG_20261101.md`).
**Geprüfter Stand:** Commit `571c4fb` (Arbeitsbaum sauber, Register 91, Sammellauf 17:23 grün).

**Zweck:** Das Papier ist die Selbstauskunft eines externen Modells und kennzeichnet seine offenen Punkte
selbst als `UNBEKANNT`. Diese Datei beantwortet sie am echten Code — mit Datei und Zeile. Was hier als
**BELEGT** steht, ist nachgemessen; alles andere bleibt offen.

---

## 1. Die Mana-Bilanz (des Papiers Abschnitt 3.1, B-01 bis B-04)

Das Papier hielt den Mana-Haushalt für die größte Lücke und schrieb in B-12 sogar von einer
„blockierenden Demo-Bilanzlücke“, falls es keine positive Quelle gibt. **Es gibt eine — der Tempel.**

| Frage des Papiers | Befund | Beleg |
|---|---|---|
| Gibt es eine positive Mana-Quelle? | **Ja.** Der **Tempel** ist ein Produktionsgebäude mit dem Rohstoff Mana: **5 Mana/Stunde auf Nebelsee, sonst 1 Mana/Stunde** (Sumpf ausgenommen) | `data/buildings.json`, Eintrag `tempel`, Feld `rohstoff: "Mana"` und `ertrag_pro_stunde` |
| Seit wann hat jedes Dorf einen Tempel? | **Seit S-1**: Tempel, Holzfäller und Steinmetz kommen bei **jeder** Gründung kostenlos mit und suchen sich ihr Wunschgelände (Tempel zuerst Nebelsee, sonst Steppe) | `STARTGEBAEUDE_VORLIEBEN`, `_startgebaeude_setzen` (`src/main.py`), Register 86 |
| Wird Mana je Dorf oder im Reich geführt? | **Je Dorf**: `Settlement.vorraete` ist das Ortslager; Mana ist einer der neun Rohstoffe (`RESOURCES`). Die Reichsanzeige ist nur die Summe | `src/main.py`, `RESOURCES`; `ortsbestand_text` |
| Gibt es einen Forschungsbonus auf Mana? | **Ja, `+5 % je Stufe`** auf die Produktion von Mana | `data/research.json`, `wirkung_struktur: {art: produktion, ziel: mana, pro_stufe_prozent: 5}` (Gebiet Götterkunde laut `src/forschung_wirkung.py`) |
| Welche Mana-Senken gibt es? | **Drei, nicht eine:** (a) der Weltensprung mit **5.000 Mana** Festpreis, (b) **jede Portalreise** mit `MANA_GRUND 5,0 + MANA_JE_FELD 0,5 × Entfernung + MANA_JE_DIMENSION 20,0 × Z-Differenz`, (c) einzelne Ausgaben: Portal-Bau **150 Mana + 100 Gold**, Paladin **10 Mana** je Stück, vier Waren (Glas 30, Buch 40, Zaubertrank 50, Medizin 35, Trank 20) | (a) `data/welten.json` → `koordinatenwechsel.kosten_mana: 5000`, gelesen in `src/portalraum.py` (`_MANA_WECHSEL`, `wechselkosten()`); (b) `src/auftraege.py:262-291` (`kosten_der_mission`); (c) `src/bonus_system.py`, `data/units.json`, `src/main.py` (Warenliste) |
| Wo wird der Weltensprung abgebucht? | `src/portalraum.py` liefert den Preis, die Buchung läuft über den Spielkern; die Oberfläche nennt ausdrücklich „verlangt die 5.000 Mana aus einer Siedlung“ | `src/portalraum.py`, `src/main.py` (Portalansicht) |
| Ist der Preis belegt? | **Ja, wörtlich:** „Welt an ihren neuen Platz verschiebt. Sie benötigen hierfür 5.000 Mana.“ sowie „einmal binnen 24 Stunden“ — aus `portal.php` 2005 | `data/welten.json`, Abschnitt `_belegt` |

### 1.1 Gerechnete Tagesbilanz (Rechnung aus belegten Werten, keine Messung)

Ein Spieltag = 24 Spielstunden. **Nur die Tempel-Produktion gerechnet**, ohne Forschungsbonus, ohne
Reisekosten, ohne Sprung — das ist die Untergrenze des Mana-Zuflusses:

| Dorf mit Tempel auf | Mana/Stunde | Mana/Spieltag | 500 Mana erspart nach | 5.000 Mana erspart nach |
|---|---:|---:|---:|---:|
| Nebelsee | 5 | 120 | 4,2 Spieltage | 41,7 Spieltage |
| anderes Gelände | 1 | 24 | 20,8 Spieltage | 208,3 Spieltage |
| 6 Dörfer, alle Nebelsee | 30 | 720 | 0,7 Spieltage | 6,9 Spieltage |
| 6 Dörfer, alle „sonst“ | 6 | 144 | 3,5 Spieltage | 34,7 Spieltage |

**Lesart für die Preisentscheidung (F-01 des Papiers):** 5.000 Mana ist bei einem einzelnen Dorf auf
Normalgelände praktisch unerreichbar (über 200 Spieltage), bei sechs Dörfern auf Nebelsee dagegen in knapp
einer Woche. **500 Mana** ist auch für ein einzelnes Dorf auf Normalgelände in rund drei Wochen erreichbar
und auf Nebelsee in gut vier Tagen. Die Zahlen sind Quotienten aus belegten Stundenwerten — die echte
Messung mit laufenden Ticks steht noch aus (offener Punkt 3).

---

## 2. Die Reiseformeln (des Papiers Abschnitt 3.3, B-05 und B-14 bis B-16)

| Frage des Papiers | Befund | Beleg |
|---|---|---|
| Rechenfunktionen | `reisezeit_sekunden(entfernung, geschwindigkeit)`, `tempo_der_gruppe(bestand)` = **langsamste mitgeführte Einheit**, `kosten_der_mission(...)`, `ladung_der_mission(...)` | `src/auftraege.py:111-191, 267-291` |
| Hin- und Rückweg | **Die Rückkehr dauert so lange wie eine Strecke**, zusammen das Doppelte — steht als Kommentar mit Quellenangabe im Modul | `src/auftraege.py` (Kopfkommentar, „BELEGT … Handbuch S. 19“) |
| Kostenarten | Gold, **Nahrung und Mana** — Mana auch bei jeder Portalreise, nicht nur beim Sprung | `kosten_der_mission`, Rückgabe `{gold, nahrung, mana}` |
| Rundung | `round(..., 2)` auf die drei Kostenarten | ebenda |
| Zeitbasis | Spieluhr (`state.spielsekunden`), nicht Rechnerzeit | `auftraege.fortschritt(..., jetzt)`; die Portalansicht rechnet die Sperre in Spielstunden |

Das Papier hatte hier nur **Übungsformeln mit erfundenen Zahlen** geliefert (B-14 bis B-16) und
ausdrücklich gesagt, Hermes müsse die echten Formeln bestimmen. **Das ist damit erledigt:** die echten
Funktionen stehen fest, die Übungszahlen des Papiers werden **nicht** übernommen.

---

## 3. Der Zustandsname (des Papiers Teil 5, letzter Absatz)

Das Papier fragte, ob der achte Zustand `FLEHEN` oder `FLIEHEN` heißt. **Er heißt `FLIEHEN`**
(„Rueckzug nach Niederlage“), die Auftrags-Fassung von Auftrag 6 hatte `FLEHEN` falsch geschrieben.

Beleg: `src/bottaktik.py:22` — `MARSCHIEREN, RAUBERN, FLIEHEN, RAECHEN = "MARSCHIEREN", "RAUBERN", "FLIEHEN", "RAECHEN"`;
Beschriftung in Zeile 28, Zeitkonstante `RUHE_ZEIT_FLIEHEN = 24 * 3600` in Zeile 43.
**Folge:** Kein Text wird geändert (der Code ist richtig), aber jede Meldung und jedes spätere Papier
schreibt `FLIEHEN`.

---

## 4. Was das Papier richtig gesehen hat (übernommen, ohne Gegenbefund)

* **Keine Bot-Markierung auf der Weltkarte** — deckt sich mit Daniels Vorgabe und mit dem Stand von S-2b.
* **Kein Angriff in S-7** — deckt sich mit `docs/AKTUELLER_STAND.md`.
* **Meldungen nur nach echtem, gespeichertem Zustandswechsel, mit Deduplizierung und Tagesgrenze** — der
  vorhandene Nachrichtenweg ist `state.messages` mit `nachrichten_farbe`; eine zweite Ablage gibt es nicht
  und wird nicht gebaut.
* **Eine Buchungsstelle** für den Weltensprung — `portalraum.wechselkosten()` liefert den Preis, gebucht
  wird im Spielkern; die Anzeige liest nur.
* **`random.Random` mit stabilem, aus SHA-256 abgeleitetem Seed, nie `hash()`** — dieselbe Regel gilt schon
  im Projekt (`botkern`, `bottaktik`, `s1`-Platzwahl arbeitet bewusst ohne Zufall).
* **Hilfe aus echten Spielstandsdaten, Knöpfe navigieren nur** — die Karte „Dein nächster Schritt“ existiert
  (`main.naechster_schritt`, `src/spielerhilfe.py`).

## 5. Was ausdrücklich offen bleibt (nicht gebaut, nicht entschieden)

1. **Goldpreis `G` des Weltensprungs** (Daniels Vorschlag „500 Mana plus ein wenig Gold“) — Zahl fehlt,
   Entscheidung Daniel.
2. **Echte 24-Spielstunden-Messung** mit laufenden Ticks für 1, 2 und 6 Dörfer (die Tabelle oben ist eine
   Rechnung aus Stundenwerten, keine Messung).
3. **Bot-Ereignisquellen** für E-02 bis E-12 des Papiers: welche davon heute wirklich liefern, ist je
   Kennung zu prüfen; das Papier hat sie selbst als „bis dahin deaktiviert“ markiert.
4. **Erste zehn Echtzeitminuten bis zur ersten Eigenversorgung**: braucht einen frischen Durchlauf ohne
   Cheats mit getrennter Protokollierung von Spielzeit und Rechnerzeit.
5. **`bottaktik` ist weiterhin nicht angeschlossen** — der Anschluss ist S-7 und noch nicht gebaut.

---

**Fazit:** Das Papier ist als Regelwerk brauchbar, seine Zahlen sind aber **Vorschläge**, keine Messungen.
Der wichtigste eigene Befund gegen das Papier: die angenommene „blockierende Mana-Lücke“ existiert nicht,
weil der Tempel seit S-1 in jedem Dorf steht und Mana produziert. Für die Preisentscheidung liegt damit
eine belastbare Rechnung vor; die Messung mit laufenden Ticks bleibt der nächste Schritt.
