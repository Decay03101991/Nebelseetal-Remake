## Engstelle
| Rohstoff | Tag | Wert | Beleg im Verlauf | Was zu tun ist |
|---|---|---|---|---|
| Holz | 1 | 6 | Tagesbilanz Tag 1 Holz 6; „T0.18 Holzfäller (Engpass holz)“ | Holzfäller vor teuren Gebäuden sichern; Start-Holz prüfen. |

## Tempo bei x180
| Beispiel | Rechnung | Urteil |
|---|---|---|
| Bau: erster Holzfäller fertig T0.01 | 0,01 Spieltag × 8 echte Minuten = 0,08 echte Minuten (4,8 s) | Erste Bauten sind sofort sichtbar; x180 ist schnell, aber es passiert konkret etwas. |
| Forschung: Waffentechnik fertig T1.62 | 1,62 Spieltage × 8 echte Minuten = 12,96 echte Minuten | Forschung ist spürbar länger; 20 echte Minuten = 2,5 Spieltage, daher sinnvolles Handeln (Bauen, Forschen, erster Angriff Tag 2) ist möglich. |

## Erste 30 Minuten
1. Es fehlt eine sichtbare Ziel-/Rollenwahl mit den vier Auszeichnungen und ihrer Punkteformel, damit der Spieler weiß, ob er Krieg, Forschung oder Handel anstrebt.
2. Es fehlt eine Voraussetzungsanzeige für Einheiten und Waren; der Lauf erzeugt 516 Kurzschwert-Fehlversuche, weil Waffentechnik Stufe 3 fehlt.
3. Es fehlt eine Frühwarnung für den Holzengpass; Tag 1 endet mit nur 6 Holz.
4. Es fehlt eine Erklärung, dass Beute ohne Handkarren leer bleibt; die Angriffe Tag 2/3 bringen Beute {}.
5. Es fehlt eine Fortschrittsanzeige für maximale Gebäudestufen; 723 Fehlversuche „Bibliothek Stufe 5 erreicht“ belegen blinde Klicks.

## Fuenf Aenderungen
| Nr | Aenderung | Zahl | Aufwand | Wirkung |
|---|---|---|---|---|
| 1 | Start-Holz erhöhen | 90 -> 150 | S | Entschärft den Tag-1-Holzengpass (Verlauf: 6 Holz). |
| 2 | Parallele Forschung ab Bibliothek Stufe 2 erlauben | 1 -> 2 gleichzeitige Forschungen | M | Waffentechnik, Nähen und Rüstungsbau können gleichzeitig laufen; Kämpfer früher als Tag 8.28. |
| 3 | Stellmacher in der Baukette vorziehen | T1.19 -> T0.75 | M | Handkarren kann vor Tag 2.0 fertig sein; erste Angriffe bringen Beute statt {}. |
| 4 | Nicht verfügbare Aktionen sperren/ausgrauen | 516 Kurzschwert- + 491 Kämpfer-Fehlversuche -> 0 | M | Spieler sieht fehlende Ware/Forschung sofort; keine wiederholten Frust-Klicks. |
| 5 | Mana-Produktion korrigieren | Tag 12 Mana 0 -> 288 (1/h) | S | Mana wird als Ressource nutzbar; aktuell bleibt es 12 Spieltage lang 0. |

## Nicht beurteilbar
- Ob das Spiel mit Oberfläche für Menschen genauso läuft; die Simulation zeigt nur Logik.
- Ob die Bot-Gegner fair oder spannend sind; im Verlauf steht nur „Ausgang angreifer, Vorrunde bestanden: True“.
- Ob Beute und Karrensperre als Hausregel Spaß machen; es fehlt die Wahrnehmung im Spiel.
- Ob Handel eine sinnvolle Rolle spielt; der Lauf enthält keine Handelsaktionen.
- Ob Mana, Goetterschutz und Ruhmeshalle funktionieren und motivieren; Mana bleibt 0, Goetterschutz wird nur einmal False.
- Ob die Auszeichnungen ohne Sieg langfristig motivieren; 12 Tage sind nur eine frühe Phase.

## Die eine Frage
Willst du, dass der erste Kämpfer vor dem ersten Angriff (Tag 2) verfügbar ist, oder ist die Waffentechnik-Stufe-3-plus-Lederrüstung-Hürde als bewusste Verzögerung gewollt?