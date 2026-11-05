## Engstelle
| Rohstoff | Tag | Wert | Beleg im Verlauf | Was zu tun ist |
|---|---|---|---|---|
| Holz | 1 | 6 | Tagesbilanz Tag 1: Holz 6; T0.18 „Holzfäller (Engpass holz)“; Tagesbilanzen Tag 4: Holz 4, Tag 8: Holz 3 | Dritten Holzfäller vor Bibliothek/Goldmine (T0.04/T0.06) bauen; alternativ Start-Holz erhöhen oder Holzimport ab Tag 0 erlauben; Bibliothek erst bei Holzpolster >60 |

## Tempo bei x180
| Beispiel | Rechnung | Urteil |
|---|---|---|
| Bau: erster Holzfäller T0.01 | 0,01 Spieltag = 0,24 Spielstunden; 0,24 × 20 Echt-Sekunden = 4,8 Echt-Sekunden nach Start | Rechnerisch korrekt, aber zu schnell für menschliches Orientieren; 1 Schritt alle 20 Spielminuten = 6,7 Echt-Sekunden |
| Forschung: Felderwirtschaft T0.04 | 0,04 Spieltag = 0,96 Spielstunden; 0,96 × 20 Echt-Sekunden = 19,2 Echt-Sekunden nach Start | In den ersten 20 Echt-Minuten (2,5 Spieltage, 180 Schritte) kann ein Mensch sinnvolle Bau-/Forschungsaufträge geben, aber kaum Bilanzen prüfen oder reagieren |

## Erste 30 Minuten
- Kein Tutorial oder geführtes Startziel, das Bau-, Forschungs- und Militär-Reihenfolge vorgibt.
- Keine sichtbare Warnung für die frühe Holz-Engstelle, obwohl Tag 1 nur Holz 6 zeigt.
- Keine Erklärung der Taktung: x180 bedeutet alle 6,7 Sekunden ein Entscheidungstakt; das ist nicht sofort verständlich.
- Keine Voraussetzungsanzeige im UI, warum Angriff/Ausbildung scheitert: „Stellmacher fehlt“, „Schmiede fehlt“ stehen nur im Fehlversuchs-Log.
- Keine Fortschrittsanzeige für die vier Auszeichnungen, damit der Spieler sein Ziel Feldherr/Forscher/Händler/Gesamtherrscher erkennt.

## Fuenf Aenderungen
| Nr | Aenderung | Zahl | Aufwand | Wirkung |
|---|---|---|---|---|
| 1 | Start-Holz von 90 auf 180 erhöhen | 180 | S | Tag-1-Holz bleibt >50 statt 6; die frühe Holzbremse und der T0.18-Engpass werden entschärft |
| 2 | Dritten Holzfäller in der Start-Baukette vor Bibliothek/Goldmine fertigstellen lassen | 3. Holzfäller | S | Holzproduktion steigt ab etwa T0.03 statt T0.18; Tagesbilanz Tag 1 Holz nicht mehr 6 |
| 3 | Nach jedem Spieltag automatisch 10 echte Sekunden pausieren | 10 s | S | Der Mensch kann die Tagesbilanz lesen, bevor der nächste Tag bei x180 weiterrennt |
| 4 | Fehlversuche ab 5 gleichen Gründen als sichtbares UI-Warnfeld zeigen | 5 | M | Spieler sieht sofort, dass Stellmacher/Schmiede/Kriegerakademie fehlen; die 85/77/36 Fehlversuche werden verständlich |
| 5 | Angriffsbefehl erst ab 2 Kämpfern und 1 Handkarren im UI erlauben; vorher fehlenden Bedarf anzeigen | 2 Kämpfer / 1 Handkarren | S | Verhindert zahlreiche unsichtbare „keine Kämpfer / keine Karren“-Fehlversuche; Spieler spart vergebliche Kommandos |

## Nicht beurteilbar
- Spielspaß und UI-Lesbarkeit, da der Lauf ohne Oberfläche gefahren wurde.
- Bot-KI, Diplomatie, Handel, Ruhmeshalle und PvP-Ersatz, weil sie im Log nicht auftauchen.
- Langzeitmotivation nach Tag 10 und spätere Einheiten/Balance (Pferde, Metallverarbeitung), da nur Endbestände sichtbar sind.
- Menschliche Reaktionszeit und Entscheidungsqualität bei x180, weil der Lauf eine feste, nicht optimale Skriptpolitik nutzt.
- Ob die Auszeichnungen mit 11 Kriegspunkten, 70 Forschungspunkten und 40 Gesamtpunkten einen attraktiven Zielverlauf bieten, da Vergleichswerte fehlen.

## Die eine Frage
Soll das x180-Frühspiel für einen Menschen gedacht sein, der alle 6,7 Sekunden einen Schritt setzt, oder soll ich die ersten 20 echten Minuten als pausiertes/tutorial-ähnliches Planungsfenster gestalten?