## Engstelle
| Rohstoff | Tag | Wert | Beleg im Verlauf | Was zu tun ist |
|---|---|---|---|---|
| Holz | 4 | 4 | Tagesbilanz Tag 4: Holz 4; Fehlversuche u.a. „Zu wenig für den Ausbau von Kriegerakademie: es fehlen 47/34/56 holz“, „haus: es fehlen 72 holz“ | Holzfäller früher ausbauen, Holzbauten strecken, Baukunst-Forschung vorziehen |

## Tempo bei x180
| Beispiel | Rechnung | Urteil |
|---|---|---|
| Bau erster Holzfäller T0.01 | 0,01 Spieltage × 8 echte Minuten/Spieltag = 0,08 min = 4,8 s | Sehr schnell; erstes Gebäude nach <5 s |
| Forschung Felderwirtschaft T0.04 | 0,04 Spieltage × 8 echte Minuten/Spieltag = 0,32 min = 19,2 s | Sehr schnell; erste Forschung nach <20 s |

Erste 20 echte Minuten = 2,5 Spieltage. Bis dahin stehen laut Verlauf bereits viele Gebäude, die erste Forschung und die erste Ausbildung. Ein Mensch kann also sinnvoll bauen und forschen. Allerdings taktet die Simulation alle 20 Spielminuten = 6,7 echte Sekunden; mit GUI wäre das für einen Menschen sehr hektisch.

## Erste 30 Minuten
- Ein Tutorial oder eine geführte Startsequenz fehlt, die die ersten Bauten (Holzfäller, Farm, Goldmine, Steinmetz) vorgibt.
- Eine Zielanzeige fehlt: Es gibt keine Siegbedingung, und die Gesamtpunkte bleiben niedrig.
- Voraussetzungen für Ausbildung und Angriff sind vor dem Klick nicht sichtbar; der Lauf erzeugt 238 Ausbildungs- und 236 Angriffs-Fehlversuche.
- Eine Engpasswarnung für Holz fehlt; der Bestand fällt auf 4, ohne dass die einfache Politik rechtzeitig gegensteuert.
- Wirkungslose Bau-/Ausbau-Buttons bleiben aktiv; 874 Befehle scheitern an Max-Stufe oder „alle Gebäude stehen“.

## Fuenf Aenderungen
| Nr | Aenderung | Zahl | Aufwand | Wirkung |
|---|---|---|---|---|
| 1 | Start-Holz von 90 auf 150 erhöhen | +60 Holz | S | Überbrückt den frühen Holzmangel; Hausbau und Kriegerakademie-Ausbau scheitern seltener |
| 2 | Angriff erst ab 4 Soldaten und 1 Handkarren freischalten | 4/1; 236 Fehlversuche | S | Vermeidet 236 Fehlversuche und zeigt dem Spieler die Angriffsvoraussetzung |
| 3 | Ausbildungsvoraussetzungen vor dem Klick anzeigen | 238 Fehlversuche (84+77+77) | S | Spieler erkennt, dass Handkarren Stellmacher und Kämpfer/Bürgerwehr Kriegerakademie brauchen |
| 4 | Bau-/Ausbau-Buttons bei Max-Stufe oder „alle Gebäude stehen“ deaktivieren | 874 Fehlversuche (356+414+104) | S | Entfernt wirkungslose Befehle und reduziert Frust |
| 5 | Warenfertigung Kurzschwert/Lederrüstung erst mit Schmiede/Nähstube anzeigen | 55 Fehlversuche (36+19) | S | Erklärt den Produktionsweg und vermeidet Fehlversuche |

## Nicht beurteilbar
- Ob das Spiel Spaß macht: Der Lauf ist reine Spiellogik ohne Oberfläche und ohne menschliche Klick- und Denkzeiten.
- Ob das x180-Tempo mit einer echten GUI bedienbar ist: Die Schrittfrequenz beträgt 6,7 Sekunden, aber GUI-Bedienzeit ist nicht getestet.
- Kampfbalance: Nur zwei Angriffe auf Wallstufe 1, keine Verluste, keine höheren Wallstufen oder Bot-Verhalten belegt.
- Langzeitwirtschaft ab Tag 8: Metall, Wolle und Leder bleiben ungenutzt; Handelspunkte fehlen im Verlauf.
- Ob das Mana-System funktioniert oder relevante Abnehmer hat: Mana bleibt im gesamten Lauf 0.

## Die eine Frage
Was ist das geplante Ziel für den Einzelspieler-Modus, wenn der Lauf bei Spieltag 8 mit 19 Gesamtpunkten endet und keine Siegbedingung existiert – ist das der gewünschte Sitzungsumfang oder fehlen dafür Inhalte?