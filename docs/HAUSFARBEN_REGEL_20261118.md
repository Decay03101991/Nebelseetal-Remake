# Hausfarben: Wappen, Burg und Geschichte — die eine Regel (18.11.2026)

**Daniels Wort (18.11.2026, 22:4x):** „ja die farben dürfen sich an den burgen orientieren aber achte darauf
das es mit der geschichte stimmig ist und unser gesamt designkonzept stimmig ist“.

Dieses Blatt hält fest, was gemessen ist, wo es sich widerspricht und welche **eine** Regel daraus folgt.

## 1. Gemessen (deckende Pixel, 160 px Kante, 32er-Stufen ab 0)

| Haus | Volk | Wappen (`data/haeuser.json`) | Farben des Wappens | Farben der Burg |
|---|---|---|---|---|
| Silberbach | Menschen | `wappen_04` | **#200000 / #600000 / Gold #a06020** | `burg_02`: #e0c0a0, #c0a080, **#600000**, #404020 |
| Hammerhall | Zwerge | `wappen_10` | **#202020 / #000000 / #604020** | `burg_01`: #404040, #202020, #c0a0a0, #c0a080 |
| Sternenwacht | Elfen | `elfen_wappen.png` | **#002020 / #004040 / Silber #a0a0a0 / Gold #806040** | `burg_03`: #e0e0e0, #e0e0c0, #808080 |
| Schattenfaust | Trolle | `wappen_08` | **#000000 / #200000 / #400000 / #600000 / #802020** | `burg_05`: **#202000, #404020, #204000** (grün/oliv), #402000 |
| Knochenmoor | Ghule | `wappen_02` | **#000000 / #402060 / #402040** (violett) | `burg_04`: #202040, #404060, #000020 |
| Flickwerk | Gnome | `wappen_05` | **#002040 / #404040 / #202040** (marineblau/grau) | `burg_06`: #e0e0e0, **#80a0c0, #4060a0, #204060** (eisblau) |

## 2. Wo es sich widerspricht — zwei Häuser, nicht sechs

Die Chronik nennt je Haus „Die Farben des Hauses sind …“. Gegen diese Sätze gemessen:

| Haus | Chronik sagt | Wappen | Burg | Urteil |
|---|---|---|---|---|
| Silberbach | Rot und Gold | rot/gold | rot + warmes Beige | **stimmig** |
| Hammerhall | Grau, Schwarz und Gold | grau/schwarz/gold | grau/schwarz/warm | **stimmig** |
| Sternenwacht | Weiß, Silber, Gold und Tannengrün | silber/weiß, Goldakzente, tannengrün | weiß/silber | **stimmig** (Tannengrün fehlt der Burg, ist aber kein Widerspruch) |
| Knochenmoor | Violett und Schwarz | violett/schwarz | dunkelblauviolett | **stimmig** |
| **Schattenfaust** | **Rot, Schwarz und Gold** | rot/schwarz/gold | **grün/oliv** | **WIDERSPRUCH** |
| **Flickwerk** | **Grau, Schwarz und Gold** | marineblau/grau | **eisblau/weiß** | **WIDERSPRUCH** |

## 3. Die Regel, die beides zusammenhält

**Heraldik und Szene sind zwei Ebenen, keine zwei Wahrheiten.**

- **Heraldik** (Wappen, Banner, Fahnen, Wappenrock, alles was das HAUS bezeichnet) trägt die Farben der
  **Chronik**. Sie stehen in `data/haeuser.json` und sind der Text, den Daniel freigegeben hat — sie bleiben
  unverändert.
- **Szene** (Burg, Landschaft, Baustoff, Licht) trägt die Farben der **gelieferten Burg**. Eine Basaltfeste
  mit Moos und Grün steht in einem grünen Land — das sagt nichts über ihr Banner.
- **Beides zusammen** in einem Bild: die Szene gibt den Grundton, die Heraldik setzt den Akzent (Banner,
  Wappen, Vorhang). So bleibt die Geschichte wahr („Die Farben des Hauses sind Rot, Schwarz und Gold“) und
  das Bild folgt der Burg.

Daraus folgt für das Dezember-Paket, je Datei:

| Datei | Grundton | Akzent |
|---|---|---|
| `kopfband_trolle` (B8) | **grün/oliv** der Burg `burg_05` | rot-schwarzes Banner, goldene Akzente |
| `kopfband_gnome` (B8) | **eisblau/weiß** der Burg `burg_06` | marineblaues Tuch (`wappen_05`, D11) — und **nur hier** Marineblau |
| die übrigen vier Kopfbänder | Burgfarben des Hauses | Wappenfarben als Banner |
| B1, B2, B9, B10, B12, B13 | unverändert nach den Regeln des Bildbriefings | — |

## 4. Was das für die Anzeige im Spiel bedeutet (offen, nicht gebaut)

`data/haeuser.json` führt heute **nur** die Wappenfarben (`farben`). Wenn die Anzeige künftig auch die Burg
zeigen soll, braucht sie ein zweites Feld (z. B. `farben_burg`, gemessen wie oben) — das ist ein eigener
Schnitt mit eigener Wache, **nicht** Teil dieses Blattes. Bis dahin gilt: die Anzeige zeigt die Heraldik.

## 5. Stand

- Die Chronik bleibt **unverändert** (Daniel 18.11.2026: „achte darauf das es mit der geschichte stimmig
  ist“).
- Das Bildbriefing (Auftrag Nr. 22, Zeichner-Fassung) bekommt diese Regel als **eigenen Abschnitt** —
  sonst zeichnet jemand die Trolle rot und die Gnomen eisblau nach der Burg und die Banner verschwinden.
