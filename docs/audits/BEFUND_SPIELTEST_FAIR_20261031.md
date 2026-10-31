## Engstelle
| Rohstoff | Tag | Wert | Beleg im Verlauf | Was zu tun ist |
|---|---|---|---|---|
| Holz | 6 | 4 | Tagesbilanz Tag 6: Holz fällt von 76 auf 4; nach T5.99 kein Bau mehr, nur noch Forschung | Holzproduktion erhöhen, z. B. dritter Holzfäller oder Start-/Baukosten von Holz entschärfen; Baureihenfolge strecken |

## Tempo bei x180
| Beispiel | Rechnung | Urteil |
|---|---|---|
| Bau: erster Holzfäller bei T0.01 | 0.01 Spieltag = 0.24 Spielstunden = 14.4 Spielminuten; 14.4/180 = 0.08 echte Minuten = 4.8 Sekunden | Der Mensch kann bauen, aber wird nach ~5 Sekunden zur nächsten Aktion getrieben; Rohstofffolgen sind in der Zeit nicht lesbar. |
| Forschung: Felderwirtschaft bei T0.04 | 0.04 Spieltag = 0.96 Spielstunden; 0.96 × 20 Sekunden = 19.2 echte Sekunden | Forschung wirkt wie ein Automatismus; die Bedeutung der ersten Forschung geht im Takt unter. |
| Erste 20 Echtminuten | 20 / 8 = 2.5 Spieltage; ein Aktionstakt von 20 Spielminuten dauert 6.7 Echtsekunden | Ein Mensch kann Handlungen ausführen, aber nicht sinnvoll planen oder Feedback verarbeiten; für den Einstieg zu schnell. |

## Erste 30 Minuten
- Es fehlt ein Tutorial/Questpfad, der die erste Baupriorität (Holzfäller, Farm, Goldmine) und deren Reihenfolge erklärt.
- Es fehlt eine sichtbare Kampfvorbereitung, dass der erste Angriff mindestens eine Einheit und einen Karren braucht.
- Es fehlt eine Engpassanzeige, die rechtzeitig vor Holzstillstand warnt, statt erst bei 4 Holz an Tag 6.
- Es fehlt verständliches Feedback, warum trotz Kriegerakademie und Gold keine Ausbildung stattfindet.
- Es fehlt eine Pausen-/Tempokontrolle, damit die ersten 30 Echtminuten (= 3.75 Spieltage) nicht einfach durchlaufen.

## Fuenf Aenderungen
| Nr | Aenderung | Zahl | Aufwand | Wirkung |
|---|---|---|---|---|
| 1 | Start-Holz von 90 auf 250 erhöhen | 90 → 250 | S | Entschärft die Holzengstelle Tag 6; der Spieler kann die ersten 12 Gebäude ohne gefühlten Stillstand bauen. |
| 2 | Automatisch 1 Krieger ausbilden, sobald Kriegerakademie steht und Gold ≥ 100; erzwingt Tag-2-Angriff auf Wallstufe 1 | 1 Krieger / Gold ≥ 100 | M | Kein 10-Tage-Lauf ohne Kampf; Kriegspunkte und Beute können entstehen. |
| 3 | Stellmacher spätestens T1.50 in die Baufolge aufnehmen | T1.50 | S | Karren sind vorhanden; Angriff scheitert nicht wie im Lauf an fehlender Transportkapazität. |
| 4 | Standardtempo für die ersten 10 Spieltage von x180 auf x60 senken; x180 optional für Tests | x60 | L | 1 Spieltag dauert 24 echte Minuten; in den ersten 20 Minuten vergehen nur 0.83 Spieltage, Planung wird möglich. |
| 5 | Holz-Ampel ab Tag 0 mit Baustopp bei Holz < 20 und Hinweis „Holzfäller erweitern“ | Holz < 20 | M | Der Spieler sieht den Engpass vor dem Kollaps bei Tag 6 und wird nicht durch Stillstand vertrieben. |

## Nicht beurteilbar
- Ob das UI/Handling Spaß macht oder abschreckt: Der Lauf ist ohne Oberfläche gefahren.
- Ob Kampfbalance, Beutestaffel oder Truppenverluste stimmen: Es ist kein Kampf zustande gekommen.
- Ob die Ausbildung und das spätere Wirtschafts-/Militärspiel tragen: Nur 10 Tage, 0 Einheiten, 0 Kämpfe.
- Ob Bots, Handel oder Kriegsinteraktion funktionieren: Es gibt keine Bot-Interaktion im Log.
- Ob x180 für einen echten Menschen langfristig spielbar ist: Der Log zeigt nur Automatik, keine echte Reaktionszeit.

## Die eine Frage
Warum wurde im Lauf trotz Kriegerakademie und Gold ab Tag 1 nie eine Einheit ausgebildet: fehlt eine Voraussetzung im Spiel (z. B. Metall/Siedler/Karren) oder war die Ausbildungsbedingung der Simulationspolitik schlicht zu schwach?