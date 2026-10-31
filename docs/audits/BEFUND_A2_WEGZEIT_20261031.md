## Formel  
Dauer eine Strecke = 2 · Entfernung / Geschwindigkeit Spielstunden.  
Belegt: aktiver Code `reisezeit_sekunden = Entfernung / Geschwindigkeit * 7200` (`src/auftraege.py`, Konstante `SEKUNDEN_JE_FELD = 7200.0`); 7200 s = 2 h.  
Rückweg: doppelte Dauer (Handbuch 2009, Seite 19: „dauert der Auftrag doppelt so lange“).  
Spieluhr x180: 1 Spielstunde = 20 Echtsekunden (Vorgabe Daniel, 31.10.2026, Abschnitt 6).  
Prüfung: 32 Felder, GS 5 ⇒ 12,8 Spielstunden = 256 Echtsekunden (4 min 16 s) pro Strecke, 512 s gesamt. Das gibt dem Verteidiger ausreichend Vorwarnzeit und ist für Einzelspieler erträglich. Faktor 2 wird beibehalten.

## Kostentabelle
| Groesse | Wert | belegt/VORSCHLAG | Quelle/Herleitung |
|---|---|---|---|
| Gold je Einheit und Strecke | 0,1 Gold pro Feld und GS-Punkt pro Einheit. Beispiel: GS 10, 16 Felder → 16 Gold. | VORSCHLAG | Handbuch 2009 Seite 20 nennt nur „verschiedene Mengen an Gold … je nach Einheiten“ und „weniger Gold bei Drosselung“; keine konkreten Zahlen. Ableitung im Verhältnis zu Produktionsraten Goldmine 3/1,5 pro Stunde (data/resources.json). |
| Nahrung je Einheit und Strecke | 0,1 Nahrung pro Feld geteilt durch GS je Einheit. Beispiel: GS 10, 16 Felder → 0,16 Nahrung. | VORSCHLAG | Handbuch 2009 Seite 20 nennt nur „steigt dabei der Bedarf an Nahrung“ bei Drosselung; keine Zahlen. Ableitung im Verhältnis zu Farm 4/Jäger 2 pro Stunde (data/resources.json). |
| Mana je Entsendung | 5 Mana + 0,5 Mana pro Feld Entfernung, unabhängig von der Einheitenzahl. Zusätzlich +20 Mana je Z-Differenz (Dimensionswechsel). | VORSCHLAG | Vorversion 2006, Abschnitt Portal: Mana hängt von Entfernung ab, Dimensionswechsel kostet viel Mana. Konkrete Auftrags-Mana-Kosten nicht belegt; Verschiebungsritual belegt 5.000 Mana. |

## Sechs Beispielreisen
| Distanz | GS | Spielstunden | Echtzeit bei x180 | Rueckweg gesamt |
|---|---|---|---|---|
| 6 | 5 | 2,4 h (2 h 24 min) | 48 s | 4,8 h (96 s) |
| 6 | 35 | ~0,343 h (20 min 34 s) | ~6,9 s | ~0,686 h (41 min 9 s / 13,7 s) |
| 16 | 5 | 6,4 h (6 h 24 min) | 128 s | 12,8 h (256 s) |
| 16 | 35 | ~0,914 h (54 min 51 s) | ~18,3 s | ~1,829 h (109 min 43 s / 36,6 s) |
| 32 | 5 | 12,8 h (12 h 48 min) | 256 s | 25,6 h (512 s) |
| 32 | 35 | ~1,829 h (1 h 49 min 43 s) | ~36,6 s | ~3,657 h (219 min 26 s / 73,1 s) |

Quelle: Formel aus `src/auftraege.py` (`SEKUNDEN_JE_FELD = 7200`), Rückweg-Handbuch 2009 Seite 19, Spieluhr x180 Vorgabe. GS-Werte aus `data/units.json`.

## Drosselung um 10 %
Beispiel: 16 Felder, GS 10 (z. B. Kämpfer), eine Strecke. Drosselung = Geschwindigkeit auf 90 % reduziert (Handbuch 2009, Seite 20: „in 10%-Schritten drosseln“).

| Größe | Ohne Drosselung | Mit 10-%-Drosselung | Änderung | Quelle/Herleitung |
|---|---|---|---|---|
| Dauer (Spielstunden) | 3,2 h | ~3,556 h | +11,1 % | Formel aus `src/auftraege.py`; Drosselung qualitativ belegt Handbuch 2009 S. 20. |
| Echtzeit bei x180 | 64 s | ~71,1 s | +7,1 s | Umrechnung: 1 Spielstunde = 20 s (Vorgabe). |
| Goldkosten (je Einheit) | 16 Gold | 14,4 Gold | −10 % | Vorschlag aus Kostentabelle; qualitativ belegt: „weniger Gold“ (Handbuch 2009, S. 20). |
| Nahrung (je Einheit) | 0,16 Nahrung | ~0,178 Nahrung | +11,1 % | Vorschlag aus Kostentabelle; qualitativ belegt: „steigt … Bedarf an Nahrung“ (Handbuch 2009, S. 20). |

## Dimensionen als Laendereien
**Ausgangslage:** 20 Dimensionen à 20 × 20 Felder, Koordinaten (X, Y, Z), Portalaktivierung kostet Mana, Dimensionsdurchdringung besonders teuer (Vorversion 2006, Abschnitt Portal).  

**Variante A – Alle 20 Dimensionen als dünn besiedelte Landesteile:** Jede Dimension bleibt ein Landesteil, erhält aber nur 1–3 aktive Welten (Bot-Siedlungen oder mögliche Spielersiedlungen). Reisen innerhalb einer Dimension normal, zwischen Dimensionen nur per Portal mit Manakosten. Vorteil: Originalstruktur mit 20 Dimensionen und Mana für Z-Wechsel bleibt vollständig erkennbar. Nachteil: Sehr viel leerer Raum, für Einzelspieler kaum zu füllen, Bot-Dichte dünn, Mana-Kosten wirken unverhältnismäßig.

**Variante B – Reduzierte Landesteile:** Die 20 Dimensionen werden zu 3–5 thematischen Landesteilen (z. B. Waldland, Bergland, Wüste, Nebelsee) zusammengezogen. Jeder Landesteil hat ein eigenes Raster und ist per Portal verbunden. Vorteil: Überschaubar, gut für Einzelspieler, Bots konzentriert. Nachteil: Die 20-Dimensionen-Optik und die damit verbundene Mana-Staffelung gehen verloren.

**Empfehlung:** Zwischenlösung: Die 20 Dimensionen als Hintergrund behalten, aber nur 5–7 für den Spieler aktiv freischalten (Rest „versiegelt“ oder spätere Erweiterung). Das Portal wird zum Tor zwischen den aktiven Landesteilen: Reisen innerhalb eines Landesteils normal, zwischen Landesteilen nur per Portal mit Manakosten. Mana-Kosten bleiben entfernungsabhängig inklusive Z-Differenz (Vorschlag: 5 + 0,5 Mana pro Feld + 20 Mana je Z-Differenz). Handel und Kopfgeld laufen über das Portal zu Bot-Siedlungen in anderen Landesteilen; Kopfgeld wird als Belohnung für Angriffe auf Bot-Siedlungen interpretiert (in Quellen nicht näher beschrieben, daher Vorschlag). So bleibt die Originalmechanik (Portal, Mana, Dimensionen) erkennbar, der aktive Raum ist für Einzelspieler angemessen.

## Drei offene Punkte
1. Konkrete Gold- und Nahrungskostensätze für die 28 Einheiten fehlen in den Quellen; die vorgeschlagene Kostenformel (0,1 Gold pro Feld/GS, 0,1 Nahrung pro Feld/GS) ist reine Balance-Annahme.  
2. Bot-Verhalten und Kopfgeldmechanik sind in Handbuch und Vorversion nicht beschrieben; Reaktionen auf Angriffe und Belohnungssystem für Bot-Siedlungen bleiben offen.  
3. Die genaue Mana-Kostenfunktion für Portalreisen (insbesondere zwischen aktiven Landesteilen/Dimensionen) und die Balance zur Mana-Produktion (5/Stunde auf Nebelsee, 1/Stunde sonst, `data/resources.json`) im Einzelspieler sind offen.

Was das für den Code bedeutet: Die vorgeschlagenen Kostensätze (Gold, Nahrung, Mana) müssen als anpassbare Konstanten im Auftragsmodul ergänzt werden, damit sie ohne Eingriff in die Kernlogik nachjustierbar sind. Die Drosselung muss die Geschwindigkeit vor der Reisezeitberechnung mit dem Faktor 0,9 multiplizieren und Gold/Nahrung entsprechend der belegten qualitativen Richtung anpassen. Die Dimensions-/Ländereienlogik ist als Konfiguration (aktive Dimensionen, Mana-Zuschläge) umzusetzen, nicht als fest kodierte 20-Dimensionen-Annahme.