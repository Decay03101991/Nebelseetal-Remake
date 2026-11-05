# 04 Luecken und Korrekturen am Ist-Stand

## 1. Vier Aussagen der Sammlung waren falsch - hier richtiggestellt

Alle vier mit Befehl gemessen am 06.11.2026, Kopf `3c5189a`.

| Behauptung in der Sammlung | Gemessen | Beleg |
|---|---|---|
| Es gibt 20 Limbus-Dimensionen, 14 davon leer - Loeschen waere eine Datenloeschung | **sechs** Dimensionen, `d01` bis `d06`; die 14 Platzhalter `d07` bis `d20` sind am 04.11.2026 entfernt (Schnitt W-6) | `data/welten.json` Schluessel `_schnitt_w6`; Zaehlung `len(dimensionen)` = 6 |
| Die Bots greifen die Spielersiedlung nicht an (offene Luecke B3) | **sie greifen an** - die Zielwahl laeuft ueber die Siedlungen des Spielers und kaempft dort, zusaetzlich stiehlt ein duenner Bot aus dem Lager | `src/main.py:6896 bot_angriffsplanung.waehle_ziel(self.settlements, ...)`; `data/bot_diebstahl.json` `aktiv: true` (Register 161/162) |
| Ein Weltensprung waehrend laufender Auftraege ist nicht geregelt | **ist gesperrt**, mit Daniels Wortlaut im Code | `src/main.py:10857 _unterwegs_anzahl() > 0` (Daniel 01.11.2026, Anhang 2) |
| Rache fuer Krank ist neu zu bauen | das **Gedaechtnis** ist gebaut: `geschlagen_von` wird nach einer Flucht gesetzt, der Zustand `RAECHEN` greift den Schaediger an; es fehlt nur der wachsende Rachetopf | `src/bottaktik.py:345/483/566` |

**Womit die Vorsitzung daneben lag:** sie hat die Luecke B3 mit `grep "spieler"
src/bot_angriffsplanung.py` = 0 Treffer belegt. Der Parameter heisst dort `settlements` - das Wort
"spieler" muss nicht vorkommen, damit der Spieler das Ziel ist. **Lehre:** eine Zielfunktion ueber
einen Suchbegriff zu pruefen, den sie gar nicht braucht, ist kein Beleg. Beleg ist der Aufruf mit
seinen Argumenten.

**Folge:** die drei Punkte (Dimensionen, Angriff, Sprung-Sperre) fallen aus der Bewertung. Was von
B3 wirklich offen ist, ist nicht der Angriff, sondern **Reaktion auf Spielerfortschritt**
(Bot ruestet nach, wenn der Spieler davonzieht) - das steht so im Arbeitsplan und kommt aus der
Sammlung nicht.

## 2. Was die Sammlung NICHT fuellt (bleibt unsere Arbeit)

| Luecke | Warum die KI hier nicht hilft |
|---|---|
| **A1b** Spieltest-Simulation prueft vor dem Versuch | reines Werkzeugthema in unserem Baum; die KI kennt die Simulation nicht |
| **A2** Messpflicht-Tabelle (Spieltage bis Gebaeude, Forschung, Einheit, Weltwechsel, voll ausgebaut) | muss aus UNSEREN Daten gerechnet werden |
| **A3** Kampf gegen ein echtes Bot-Dorf | spielintern; ohne A3 bleiben Mauerreparatur (B-4) und Kampf nicht beurteilbar |
| **B1/B2** Bot-Kern aus `main.py` loesen, Zielbild Bots | Architekturarbeit im eigenen Code |
| **B3 (echter Rest)** Bots reagieren auf Spielerfortschritt | die KI schlaegt nur feste Armeen vor, keine Reaktion |
| **B4/B5** Drachen-Regel, Handel und Spionage als Zug | spielintern; Spionage ist heute nur ein Bericht |
| **C1** Mana-Kette (Tempel 120 Mana je Spieltag, Weltwechsel 5.000) | Zahlen liegen bei uns (Register 236) |
| **C2/C3** Forschungsdauern senken, Aufbauzeit-Zielbild | Balancing mit Messpflicht, nicht aus einem Vergleich ableitbar |
| **C4** Handelspunkte messbar | spielintern |

## 3. Was die Sammlung bestaetigt (kein Bauauftrag, nur Beleg)

Marschzeit = langsamster Trupp; Kern rechnet, Anzeige zeigt; Kampfbericht als strukturierte Daten;
Beute "Gold zuerst" (Daniels Entscheidung, 25 Prozent Vorrang); Rueckzug je Einheit mit Schwelle und
Erschoepfung; Spionage-Nachricht; Ruhm-Punkte je Gebiet; sechs Welten ueber Portal-Koordinaten;
Nachrichten und Spielstand als lokales JSON; Wall in Stufe und Zustand; drei Kampfphasen;
Goetterschutz als Punkteband.

**Nutzen dieser Bestaetigungen:** sie sind eine unabhaengige zweite Meinung ueber Mechaniken, die wir
gebaut haben - kein Grund, etwas zu aendern.
