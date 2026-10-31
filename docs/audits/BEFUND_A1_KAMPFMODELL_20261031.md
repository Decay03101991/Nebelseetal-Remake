## Tabelle der Schritte
| Schritt | gilt | Quelle (Dokument + Stelle) | Art |
|---|---|---|---|
| Wallvorrunde | Angriff nur, wenn Nahkampf-Schlagkraft und ggf. Belagerungs-Schlagkraft die Schwellenwerte erreichen; reine Fernkämpfer zählen nicht. | Material 2, Forum-Original, Abschnitt „Bevor ein Kampf stattfindet...“ (Nahkampf); Material 1, Handbuch 2009, Abschnitt 2.1 Tabelle Schwellenwerte | ZUSAMMENFUEHRUNG |
| Mauerschaden | Schaden je Belagerungswaffe minus Mauerstufe; Berechnung nach der Fernkampf-Vorrunde; wirkt erst beim nächsten Kampf; prozentuale Schwellenreduktion. | Material 2, Forum-Original, Abschnitt „Belagerung / Mauerschaden“; Material 1, Handbuch 2009, Abschnitt 2.1 | ZUSAMMENFUEHRUNG |
| Fernkampf | Nur Vorrunde: Mauerstufe+1 Vorrunden, Fernkämpfer beider Seiten; Modifikationen (Mauer, Türme, Bogenbau) und Erschöpfungsschaden; Rückzug 20 % je Sequenz, stärkste zuerst. | Material 2, Forum-Original, Abschnitte „Vorrunde - Fernkampf“ bis „Nach den Vorrunden...“ | belegt |
| Nahkampf/Zweikampf | Angreifer wählt zufällig verteidigende Nahkampfeinheit; Zufallswert im Kampfwertbereich, +10 % je Schmiedekunststufe, -Rüstung, -Erschöpfung; höherer gewinnt; Verlierer scheidet aus und Konstitutionsprobe. | Material 2, Forum-Original, Abschnitte „Die Schlacht“ und „Zweikampf“ | belegt |
| Erschoepfung | Sieger eines Zweikampfs erleidet 2 Erschöpfungspunkte; Fernkampftreffer verursachen Erschöpfungsschaden; Erschöpfung senkt den Kampfwert; Kampfunfähigkeit bei Schwelle. | Material 2, Forum-Original, Abschnitte „Erschöpfungsschaden“ und „Zweikampf“ | belegt |
| Flucht | Keine Flucht im Handbuch-Sinn; nur Konstitutionsprobe überlebt/stirbt bei Kampfunfähigkeit; Rückzug nur für Angriffs-Fernkämpfer. | Material 2, Forum-Original, Abschnitt „Wird eine Einheit Kampfunfähig...“ und „Nach den Vorrunden...“ | belegt |
| Ausgang | Ende, wenn alle angreifenden Nahkämpfer ausgeschieden, alle Verteidiger (Fern+Nah) besiegt oder 10 Sequenzen ohne Sieger; unentschieden ohne Beute/Verlust. | Material 2, Forum-Original, letzter Absatz; Material 1, Handbuch 2009, Abschnitt 2.4 | ZUSAMMENFUEHRUNG |
| Beute | Nur Transportkarren plündern; Beute durch Karrenladung begrenzt. | Material 1, Handbuch 2009, Abschnitt 2.4: „Falls er Transportkarren... plündern“; Material 5, Code-Kommentar: „Beute ist durch die Ladung begrenzt“ | belegt |
| Geraeteverlust | Verlierer verliert Teil seiner Karren und Belagerungswaffen; Fluchtchance 40 %, +5 % je Sequenz; unentschieden: keine Verluste. | Material 1, Handbuch 2009, Abschnitt 2.4 | belegt |
| Punkte | Kriegspunkte je Einheit fester Wert, Verteidigungsanlagen Stufe³, Gesamt=(Krieg+Forschung)/2. | Material 1, Handbuch 2009, Abschnitt 3 | belegt |

## Widersprueche
| Nr | Widerspruch | Quelle A | Quelle B | kleinere Aenderung |
|---|---|---|---|---|
| 1 | Fernkampf: Handbuch: in jeder Kampfsequenz gleichzeitig; Forum: nur Vorrunden vor der Schlacht, danach Rückzug. | Material 1, Abschnitt 2.2 | Material 2, Abschnitt „Vorrunde - Fernkampf“ | Handbuch-Fernkampf verwerfen, Forum-Vorrunde übernehmen. |
| 2 | Zweikampf: Handbuch: AT/PA/RS/TP/MU-Runden mit LE; Forum: einzelner Kampfwert-Wurf, Rüstung, Verlierer scheidet aus. | Material 1, Abschnitt 2.3 | Material 2, Abschnitt „Zweikampf“ | Handbuch-Zweikampf vollständig ersetzen. |
| 3 | Erschöpfung: Handbuch: Sieger -1 AT/PA; Forum: Sieger -2 Erschöpfungspunkte, wirkt auf Kampfwert; Fernkampf verursacht Erschöpfung. | Material 1, Abschnitt 2.3 | Material 2, Abschnitt „Erschöpfungsschaden“ | Handbuch-Erschöpfung ersetzen. |
| 4 | Flucht: Handbuch: LE<5 und Mut entscheidet Flucht, Rückkehr; Forum: Kampfunfähigkeit, Konstitutionsprobe, kein Wiedereintritt. | Material 1, Abschnitt 2.3 | Material 2, Abschnitt „Wird eine Einheit Kampfunfähig...“ | Handbuch-Fluchtregel ersetzen. |
| 5 | Wallbedingung: Handbuch: „Fußtruppen“; Forum: „Nahkampfeinheiten“. | Material 1, Abschnitt 2.1 | Material 2, Abschnitt „Bevor ein Kampf...“ | „Fußtruppen“ als Nahkampf interpretieren; Fernkämpfer zählen nicht. |

## Gestaffelte Beute
| Lage | Beuteanteil | Rechenweg | VORSCHLAG-Begründung |
|---|---|---|---|
| Keine Verteidiger mehr | 100 % | `min(Karrenladung, Ortslager)` | Nur dieser Fall ist original belegt: Sieg, Karren plündern; Ladung begrenzt. |
| Mauer gebrochen (vorher 0 %) | 60 % | `0,6 * min(Karrenladung, Ortslager)` | Optionaler Vorschlag: Trümmer verzögern die Plünderung. |
| Mauer beschädigt (vorher <100 %) | 30 % | `0,3 * min(Karrenladung, Ortslager)` | Optionaler Vorschlag: Durchbruch noch nicht vollständig, Zeitverlust. |
| Mauer heil (vorher 100 %) | 10 % | `0,1 * min(Karrenladung, Ortslager)` | Optionaler Vorschlag: Überraschungsangriff, nur schnelle Plünderung. |

Diese Staffelung (10/30/60/100) ist ein reiner **VORSCHLAG** und **widerspricht den Originalregeln**: Nach Material 1 (Abschnitt 2.4) gewinnt der Angreifer nur, wenn alle verteidigenden Einheiten tot oder geflohen sind, also sind immer keine Verteidiger mehr; der Mauerzustand ist im Original kein Faktor für die Beute. Die mit dem Original vereinbare Regel lautet: **100 % des Ortslagers, begrenzt durch die Karrenladung**, sobald der Angreifer siegt und Karren mitführt.

## In keiner Quelle geregelt
- Die Prozentwerte 10/30/60/100 der Beutestaffelung sind in keiner beigefügten Quelle belegt (VORSCHLAG).
- Die konkreten Kampfwert-Spannen im Code (Material 4, PROFILE) weichen von Material 2 ab und sind durch keine beigefügte Originalquelle gedeckt.
- Die Schadensspannen der Belagerungswaffen (außer Katapult 2-13) fehlen im beigefügten Material vollständig.
- Die Ladungskapazität der Transportkarren ist nicht beziffert; nur die Begrenzung als Prinzip ist belegt.

## Was das fuer den Code bedeutet
1. In `src/kampf.py` müssen die Einheitenwerte und die Kampfmechanik verbindlich aus Material 2 stammen; abweichende Kampfwert-Spannen im PROFILE-Block sind zu korrigieren oder als VORSCHLAG zu kennzeichnen.
2. In `src/kampfbericht.py` ist die gestaffelte Beute (Material 5, Z. 200-243) zu entfernen oder deutlich als nicht originale Hausregel zu kennzeichnen; stattdessen nur `min(Karrenladung, Ortslager)`.
3. In `data/` sind alle Einheitenwerte, die in Material 2 gelistet sind, aus dieser Quelle zu übernehmen; fehlende Belagerungswaffen- und Karrenwerte sind aus Handbuch 2009 zu ergänzen oder als nicht belegbar zu markieren.