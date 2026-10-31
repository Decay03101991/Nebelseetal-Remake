# Abweichungen: Original-Seiten 2006 ↔ Handbuch 2009

**Warum diese Datei:** Die Projektregel lautet seit dem 04.10.2026: „Wo 2005er Fassung und 2009er
Handbuch abweichen, ist das vermerkt — **nicht stillschweigend angeglichen**." Daniel hat am 31.10.
die Original-Seiten des Spiels erneut geschickt; sie weichen an vielen Stellen vom Handbuch ab.
Diese Datei hält jede Abweichung fest, damit niemand später glaubt, eine der beiden Zahlen sei
„falsch" — es sind zwei Fassungen desselben Spiels.

**Quellen:** `docs/original/Spielanleitung_2005/` (Original-Seiten, Stand 2006) und
`docs/original/Spielanleitung_2009_Textfassung.txt` (Handbuch 2009, mit Zeilennummern).
**Richtschnur des Remakes ist das Handbuch 2009** (Daniel, 04.10.2026) — die 2006er Zahlen gelten
als ältere Fassung und werden nur dort genutzt, wo das Handbuch schweigt.

---

## 1. Erträge je Gebäude und Gelände

| Gebäude | 2006 (Original-Seite `rohstoffe.php`) | 2009 (Handbuch S. 10) | Urteil |
|---|---|---|---|
| Holzfäller | Wald **4** / Steppe **1** | Wald 4 / Steppe 2 | ABWEICHUNG Steppe |
| Steinmetz | Berg **4** / Hügel **1** | Berg 4 / Hügel 2 | ABWEICHUNG Hügel |
| Erzmine | Berg **3** / Hügel **1** | Berg 3 / Hügel 1,5 | ABWEICHUNG Hügel |
| Tempel | Nebelsee **8** / sonst **2** | Nebelsee 5 / sonst 1 | ABWEICHUNG beide |
| Farm | Grasland **4** / Steppe **2** | Grasland 4 / Steppe 2 | gleich |
| Goldmine | Berg **3** / Hügel **1** | Berg 3 / Hügel 1,5 | ABWEICHUNG Hügel |
| Schafszucht | Grasland **2** / Steppe **1** | Grasland 3 / Steppe 1,5 | ABWEICHUNG beide |
| Rinderfarm | Grasland **2** / Steppe **1** (nur Leder) | Grasland 3+3 / Steppe 1,5+1,5 (Nahrung **und** Leder) | ABWEICHUNG beide, 2009 gibt zusätzlich Nahrung |
| Pferdezucht | Grasland **2** / Steppe **1** | Grasland 3 / Steppe 1,5 | ABWEICHUNG beide |
| Jäger | **nur Wald** (1 Nahrung, 1 Leder) | Wald 2+2 / Steppe 1+1 | ABWEICHUNG Gelände und Menge |

## 2. Siedlergrenze — die folgenreichste Abweichung

| | 2006 | 2009 |
|---|---|---|
| Grundwert je neuer Siedlung | **5 Siedler** | **10 Siedler** |
| je Haus | +5 | +5 |
| Zuwachs | 1 Siedler/Stunde | 1 Siedler/Stunde |

**Unser Code folgt 2009** (`gebaeude_wirkung.siedlergrenze_je_siedlung`: 10 + 5 je Haus). Bleibt so.

## 3. Höchstzahl Siedlungen

| | 2006 | 2009 |
|---|---|---|
| Maximum | **10 Siedlungen** | **6 Siedlungen** (Handbuch Z. 311–312) |

**Unser Code folgt 2009** (6). Bleibt so.

## 4. Punktesystem — die Vorversion zeigt, was sich GEÄNDERT hat

2006er Seite `punktesystem.php`, wörtlich:
- **Forschungspunkte** = Summe über alle Forschungen von **Stufe × Stufe**.
- **Kriegspunkte** je ausgebildeter Militär-/Spionageeinheit: Bürgerwehr 1, Kämpfer 2, Krieger 4,
  Ritter 8, Paladin 16, Kurzbogenschütze 2, Bogenschütze 4, Langbogenschütze 8, Armbrustschütze 10,
  Streuner 1, Gauner 2, Dieb 4, Meisterdieb 8, Kundschafter 10, Waldläufer 16.
  „Solltet Ihr Einheiten verlieren, verringern sich auch Eure Kriegspunkte."
- **Handelspunkte**: je **100 Gold** Handelseinnahme 1 Punkt (20 Gold = 0,2), Verfall 1 Punkt je
  24 Stunden ohne Handelseinnahme.
- **„Alle drei Punktearten fließen zu je einem Drittel in Eure Gesamtpunktezahl ein."**

**Das Handbuch 2009 rechnet anders** (S. 5/6): **Gesamtpunktzahl = (Kriegspunkte + Forschungspunkte)
/ 2** — also nur zwei Punktarten, keine Handelspunkte, halbiert statt gedrittelt.

**Unser Code folgt 2009** (`src/punkte.gesamtpunkte`, `// 2`, mit Begründung an der Stelle). Das ist
**keine Lücke**, sondern die neuere Fassung. Die **Kriegspunkte-Tabelle ist in `data/units.json`
bereits vollständig und stimmt in allen 15 Werten** mit der 2006er Tabelle überein (geprüft 31.10.).

**Was daraus offen bleibt:** ob Handelspunkte im Remake eine Rolle spielen sollen (Daniels
Entscheidung — das Handbuch 2009 kennt sie im Punktestand nicht mehr; das Handelssystem selbst ist
belegt). Erst danach lohnt ein Einbau.

## 5. Ausbildung: die Gebäudestufe macht schneller

2006er Seite `einheiten.php`, wörtlich: „Diese Gebäude werden stufenweise ausgebaut. **Je höher die
Stufe, desto schneller werden die entsprechenden Einheiten ausgebildet.**" Ebenso: „In jeder Eurer
Siedlungen kann jeweils **nur eine** Kriegerakademie, eine Diebesgilde und ein Stellmacher errichtet
werden" und „Sobald Ihr eines dieser Gebäude errichtet habt, **erscheint im Siedlungsmenü der Button**
Stellmacher, Diebesgilde bzw. Kriegerakademie."
**Bedeutung:** Das bestätigt unabhängig, was am 30.10. gebaut wurde (Menüpunkt erst mit dem Gebäude,
ein Hersteller je Siedlung). **Offen:** unsere Ausbildungszeit ist eine feste Pilotregel
(`pilot_ausbildung_minuten`); die Stufenabhängigkeit fehlt.

## 6. Weitere kleine Abweichungen

| Thema | 2006 | 2009 |
|---|---|---|
| Siedeln | über Menüpunkt **„Aufträge" → „Neue Siedlung gründen"** | eigener Menüpunkt **„Siedeln"** |
| Siedlungsmenü | „Siedlungsübersicht, Gebäude bauen, Gebäude abreißen, Lager, Aufträge" | zusätzlich Umbenennen, Siedeln, Siedlung aufgeben |
| Auswahl der Siedlung | „Auge hinter dem Siedlungsnamen", Auswahlfeld **unter** dem Menü | Klick auf den Namen oder Dropdown **über** dem Menü |
| Weltnamen | Armageddon, Ragnarök, Utgard, Midgard, Valhalla, Limbus (als Welten) | Limbus mit **20 Dimensionen** |
| Waren-Voraussetzungen | vollständige Tabelle (Waffentechnik 1/3/5/8, Rüstungsbau 3/5/7, Nähkunst 1/2/4/6, Magiekunde 2) | Handbuch nennt die Stufen nicht in dieser Form |
| Produktionstakt | „4 Holz pro Stunde → alle **15 Minuten** 1 Holz" | keine Aussage zum Takt |

**Die Waren-Tabelle aus 2006 ist die einzige vollständige Quelle für Warenvoraussetzungen** —
Messer (keine), Dolch (Waffentechnik 1), Kurzschwert (3), Schwert (5), Zweihänder (8),
Kettenhemd (Rüstungsbau 3), Plattenrüstung (5), Magischer Paladinharnisch (Rüstungsbau 7 +
Magiekunde 2), Kurzbogen (Waffentechnik 2), Bogen (4), Langbogen (6), Armbrust (8),
Wollumhang (keine), Lederrüstung (Nähkunst 1 + Rüstungsbau 2), Diebesumhang (Nähkunst 2),
Fellumhang (Nähkunst 4), Fellrüstung (Nähkunst 6).

---

## Was daraus folgt (Vorschlag, nicht ausgeführt)

1. **Nichts umstellen, was heute 2009 folgt** (Siedlergrenze 10, 6 Siedlungen) — die Abweichung ist
   jetzt dokumentiert, nicht geglättet.
2. **Handelspunkte und die Drittel-Regel** prüfen und Daniel vorlegen (verändert die Siegbedingung).
3. **Warenvoraussetzungen** aus der 2006er Tabelle gegen `data/warenrezepte.json` halten.
4. **Ausbildungszeit** an die Gebäudestufe koppeln (2006 belegt die Richtung, nicht die Zahl).
