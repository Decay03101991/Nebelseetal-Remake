# Prüfvermerk — GPT-Demo-Textpaket gegen den lokalen Code

**Geprüfter Gegenstand:** `HERMES_DEMO_TEXTPAKET_SPIELERHANDBUCH_RELEASE_SPIELTEXTE_20261101.md`
(36.350 Byte, 278 Zeilen, SHA256 `be9d69afa3ede58e5ba5aafeae8c8d4cc44cf8454b6101e32a72ef5412c38148`,
abgelegt unter `archiv/eingaben/20261101_gpt_antworten/`).

**Prüfmaßstab:** der lokale Arbeitsstand `D:\Arbeiten\Nebelseetal_Remake`, Branch `main`, Kopf `b541cab`
(Code-Stand `4ed7fbb`), nicht der öffentliche GitHub-Stand `954097aa`.

**Prüfart:** jede Aussage über Spieleigenschaften gegen `data/*.json` und `src/*.py` gemessen. Urteile
wie im Projekt üblich: BELEGT, WIDERSPRUCH, NICHT BELEGT, VORSCHLAG. Die Textredaktion hat ausdrücklich
selbst nicht geprüft (Leseregel im Kopf der Antwort); dieser Vermerk holt das nach.

**Datum der Messung:** 01.11.2026, 18:15–18:35.

---

## 1. Bestätigt — Aussage stimmt mit dem heutigen Code überein

| Aussage im Textpaket | Messung | Beleg |
|---|---|---|
| 21 Forschungen | 21 Einträge | `data/research.json` (Dict mit 21 Schlüsseln) |
| 17 Waren | 17 Einträge | `data/items.json` → `waren` |
| 28 Einheitentypen | 28 Einträge | `data/units.json` → `einheiten` |
| Drei Werkstätten: Schmiede, Bogenbauer, Nähstube | alle drei vorhanden | `data/buildings.json` |
| Karren mit Ladung 40 / 100 / 250 / 1.000 / 2.500 | Handkarren 40, Einspänner 100, Zweispänner 250, Handelskarawane 1.000, Große Handelskarawane 2.500 | `data/units.json` Feld `ladung` |
| Start mit 10 Siedlern, 100 Holz, 100 Stein | so gesetzt | `src/main.py` Zeilen 1009 und 1022, Handbuch 2009 S. 7 |
| Bei Gründung kostenlos: Holzfäller, Steinmetz, Tempel | genau diese drei, mit Wunschgelände Tempel → Nebelsee/Steppe, Holzfäller → Wald, Steinmetz → Hügel/Berg | `src/main.py` `STARTGEBAEUDE_VORLIEBEN` |
| Dorfzentrum kostenlos, Platz wählt der Spieler | gesetzt über `dorfzentrum_offen` (S-2c-D, Register 90) | `src/main.py` `_dorfzentrum_setzen` |
| Dorfzentrum höchstens eines je Dorf, nicht abreißbar | `max_je_siedlung: 1`, Abriss gesperrt | `data/buildings.json`, Register 89 |
| Ohne Forschung baubar: Holzfäller, Steinmetz, Jäger, Bibliothek, Haus | genau diese fünf führen `voraussetzung: "keine (ohne Forschung baubar)"` | `data/buildings.json` |
| Alle übrigen Gebäude brauchen Baukunst Stufe 1 | Schwelle `Baukunst < 1` → Ablehnung mit Grund | `src/main.py` Zeilen 350/351 |
| Forschung braucht eine Bibliothek des jeweiligen Dorfes | so geprüft | `src/forschungspfad.py`, `data/buildings.json` (Bibliothek `max_je_siedlung: 1`) |
| 20 Weltkarten mit je 20 × 20 = 400 Feldern | 20 Dimensionen, 400 Felder je Dimension | `data/welten.json` → `dimensionen`, `belegte_regeln` |
| Midgard und Valhalla bespielbar, Startwelt Midgard | so eingetragen | `data/welten.json` → `weltkarten_spielbar`, `startwelt` |
| Weltensprung kostet 5.000 Mana | Festpreis, Buchung genau einmal | `src/portalraum.py` `_MANA_WECHSEL = 5000`, `src/main.py` `_portal_wechsel` |
| Weltensprung gesperrt, solange Aufträge unterwegs sind, auch Handel | `_unterwegs_anzahl() > 0` sperrt | `src/main.py` Zeile 5493 |
| Tempel erzeugt 5 Mana je Stunde auf Nebelsee, sonst 1 | Werte so hinterlegt | `data/buildings.json` `ertrag_pro_stunde` |
| Götterkunde steigert Mana (5 % je Stufe) | so gerechnet | `data/research.json`, `src/forschung_wirkung.py` |
| Fünf Bots: Haug, Brynhild (Menschen), Grom (Zwerg), Silra (Elf), Krank (Monster) | Namens- und Volksliste genau so | `src/botkern.py` Zeilen 54–60 |
| Auszeichnungen Feldherr, Forscher, Händler, Gesamtherrscher | so berechnet | `src/punkte.py` Zeilen 369–379 |
| Kein endgültiger Sieg, nur Niederlage oder Weiterspielen | so umgesetzt | `src/punkte.py` `spielausgang` |
| Jede Einheit verbraucht 8 Nahrung je Spieltag | Schalter aktiv, Wert 8 | `data/nahrungsverbrauch.json` |

---

## 2. Widersprüche — müssen vor jeder Veröffentlichung korrigiert werden

### W-01 (schwer) Die Weltkarten zeigen noch gar kein Gelände

Der Text behauptet an vier Stellen, die Weltkarten zeigten ausschließlich Gelände: H-11, H-15, R-09,
G-01 und G-03.

Am Code ist das **falsch**. `portalraum.anzeige_raster(z, radius=10)` liefert je Feld nur
`x, y, z, eigen, status, farbe` — die Farbe ist die Bannerfarbe der Dimension, kein Gelände. Das Gelände
je Weltkartenfeld ist Registerpunkt 91 und dort ausdrücklich als **NOCH NICHT GEBAUT** vermerkt (Stand
17:26: „NOCH NICHT GEBAUT“). Es ist Schritt S-5, also der nächste Schnitt, aber er existiert heute nicht.

Folge: Die Aussage wird erst nach S-5 wahr. Bis dahin ist sie eine Zusage über eine nicht vorhandene
Funktion. Der Satz muss entweder entfallen oder auf den Stand nach S-5 warten.

### W-02 (mittel) Spionage ist nicht „gar nicht da“

H-15 und R-08 behaupten, Spionage gebe es in der Demo nicht. Das ist zu kurz:

* Die **Diebesgilde** ist baubar (Baukunst, `max_je_siedlung: 1`) und bildet laut
  `data/buildings.json` sechs Einheiten aus: Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, Waldläufer.
* **Heimlichkeit** ist eine der 21 Forschungen und laut `data/research.json` die Grundlage, um Spione
  auszubilden.
* Was fehlt, sind **Spionageaktionen** — im Code findet sich keine Startfunktion für Aufklärung oder
  Diebstahl.

Richtige Formulierung: Spionageaktionen fehlen, Spionage-Einheiten und die Gilde sind vorhanden.

### W-03 (klein) Schreibweise Ragnaroeck

Der Text schreibt „Ragnaroeck“. Die Daten führen `Ragnaroek` (`data/welten.json` → `welten_belegt`).
Die Wörterliste L-01 verlangt einen Namen für alle Bereiche; also die Datenschreibweise übernehmen.

### W-04 (klein) Tempel auf Sumpf erzeugt 0 Mana, nicht 1

H-11 sagt „sonst 1 Mana je Spielstunde“. Der Ertrag lautet `{"Nebelsee": 5, "alle Gelände außer Sumpf": 1}`
— auf Sumpf also 0. Entweder Sumpf ausdrücklich nennen oder „auf den übrigen Feldern außer Sumpf 1“
schreiben.

### W-05 (klein) Die Siedlerobergrenze ist belegt, nicht unbekannt

H-17 führt sie als `UNBEKANNT — Hermes prüft`. Sie steht in `data/gebaeude_wirkung.json` mit
Handbuch-Beleg (S. 11): 10 Siedler je Siedlung, +5 je Haus, und bei sechs Dörfern ein Deckel von 360.
Der Vorbehalt ist unnötig und macht das Handbuch schwächer als es sein müsste.

### W-06 (klein) Limbus ist doppelt belegt

H-11 reiht Limbus als gleichrangige Weltkarte neben Midgard und Valhalla. Limbus ist aber zugleich der
Name der magischen Ebene, in die alle Welten eingebettet sind (`data/welten.json` `_belegt`). Die
Doppelbelegung ist im Register als offener Punkt geführt. Im Spielertext sollte Limbus deshalb nicht als
Reiseziel in einer Reihe mit den anderen stehen, solange das nicht entschieden ist.

### W-07 (klein) Ausbildungsdauer ist nicht unbekannt

H-03 nennt die Wartezeit bis zur ersten Einheit `UNBEKANNT`. Sie ist im Code geregelt: 20 Minuten je
Gebäudestufe (`AUSBILDUNG_STUFENFAKTOR`, als VORSCHLAG gekennzeichnet). Der Text darf sie als Vorschlag
nennen, statt sie für unbekannt zu erklären.

---

## 3. Was der Text auslässt und was Spieler verwirren würde

| Lücke | Sachstand | Beleg |
|---|---|---|
| **24-Stunden-Sperre nach einem Weltensprung** | nach jedem Sprung bucht der Code „24 Stunden gesperrt“ und setzt `letzter_wechsel` | `src/main.py` `_portal_wechsel`, Meldungstext |
| **Wagenbau ist Voraussetzung, nicht nur Bonus** | Einspänner ab Stufe 3, Zweispänner 7, Handelskarawane 2, Große Handelskarawane 6, Siedlerkarren 1 | `data/units.json` → `voraussetzung` je Karren |
| **Diebesgilde und Kundschafter-Einheiten** | siehe W-02 | `data/buildings.json` |
| **Bibliothek nur auf Grasland, Steppe oder Nebelsee** | so hinterlegt | `data/buildings.json` `wirkung` |

---

## 4. Was am heutigen Stand offen bleibt — nicht durch Textprüfung lösbar

1. **Weltensprung-Preis.** Der Code bucht 5.000 Mana (belegt aus `portal.php` 2005 als Koordinatenwechsel).
   Daniels eigener Vorschlag war 500 plus ein wenig Gold; die Entscheidung fällt in S-8. Der Text muss
   diesen Preis als veränderlich kennzeichnen, nicht als fest.
2. **Gelände auf den Weltkarten** — erst nach S-5 wahr (W-01).
3. **Veröffentlichte EXE, Dateiname, SHA256, Version, Datum.** Heute existiert nur der lokale Build
   (47.974.724 Byte, `595c48bf…`, Start belegt über PID 13892) — nicht veröffentlicht.
4. **Speichern- und Laden-Bedienweg.** Im Text als unbekannt geführt; das ist korrekt und bleibt offen,
   bis die EXE frisch durchgeklickt wurde.
5. **Siedlerobergrenze** ist belegt (W-05) — kein offener Punkt mehr.
6. **Rechtsstatus zum Original.** Die Danksagung ist redaktionell sauber; eine Aussage über Rechte bleibt
   bei Daniel.

---

## 5. Urteil

Das Textpaket ist als **Entwurf brauchbar**: Aufbau, Ton, Wörterliste und die Dreiteilung
„abgelehnt → Grund → nächster Schritt“ passen zum Projekt, und die große Mehrheit der Zahlen stimmt mit
dem Code überein.

**Veröffentlichung bleibt gesperrt**, bis drei Dinge erledigt sind:

1. W-01 ist behoben — entweder nach dem Bau von S-5 oder durch Streichen der Gelände-Aussage.
2. W-02 bis W-07 sind eingearbeitet (Textänderungen, kein Code).
3. Der Preis für den Weltensprung ist in S-8 entschieden und die veröffentlichte EXE mit Prüfsumme liegt
   vor.

Der Einbau der Spieltexte S-01 bis S-25 in die Oberfläche ist ein eigener Schritt und gehört nicht in
diesen Prüfvermerk.
