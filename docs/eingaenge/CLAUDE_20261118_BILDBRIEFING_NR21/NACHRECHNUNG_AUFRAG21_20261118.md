# Nachrechnung der Antwort auf Auftrag Nr. 21 (18.11.2026)

**Gegenstand:** `Claude_Opus_5.5_Antwort_Auftrag21_Bildbriefing_Fassung2.md` — Claudes Fassung 2 des
Bildbriefings fuer die 18 Dezember-Dateien.

**Regel:** jede Zahl wird nachgerechnet, BEVOR gebaut wird. Diese Datei haelt fest, was **bestaetigt**,
was **widerlegt** und was **offen** ist.

---

## 1. Bestaetigt (eigene Messung, 18.11.2026)

### 1.1 Der wichtigste Fund: MEINE Tabelle war falsch, seine Zuordnung richtig

Claude meldet, dass Abschnitt 3 meines Auftrags Nr. 21 („Gemessene Farben je Haus“) fuenf von sechs
Haeusern das falsche Wappen zuordnet. **Nachgemessen - er hat recht.** Die eine Quelle ist
`data/haeuser.json` (Stand 13.11.2026), nicht die Besucherseite:

| Haus | Abschnitt 3 meines Auftrags | **verbindlich (`data/haeuser.json`)** | Farben (gemessen, 32er-Stufen ab 0) |
|---|---|---|---|
| Silberbach (Menschen) | `wappen_04` | `wappen_04` (313 x 424) | **#200000 13 % / #600000 13 % / #a06020 6 %** |
| Hammerhall (Zwerge) | `wappen_05` | **`wappen_10`** (301 x 420) | **#202020 14 % / #000000 14 % / #604020 6 %** |
| Sternenwacht (Elfen) | `wappen_03` | **`assets/wappen/elfen_wappen.png`** (1024 x 1024) | **#002020 15 % / #004040 6 % / #806040 5 % / #a0a0a0 3 %** |
| Schattenfaust (Trolle) | `wappen_02` | **`wappen_08`** (315 x 428) | **#000000 18 % / #200000 12 % / #400000 7 % / #600000 7 % / #802020 6 %** |
| Knochenmoor (Ghule) | `wappen_01` | **`wappen_02`** (269 x 432) | **#000000 14 % / #402060 7 % / #202020 6 % / #402040 6 %** |
| Flickwerk (Gnome) | `wappen_06` | **`wappen_05`** (271 x 420) | **#002040 8 % / #404040 7 % / #202040 6 % / #202020 5 %** |

**Urteil:** fuenf von sechs Korrekturen stimmen. **Eine nicht:** Sternenwacht traegt NICHT `wappen_09`,
sondern `assets/wappen/elfen_wappen.png`; `wappen_09` (274 x 443, sha256 `47141319…`) ist eine andere
Datei als das Elfenwappen (1024 x 1024, sha256 `8041ec43…`).

### 1.2 Die Farbwerte sind dieselben, nur anders geschrieben

Claude misst 32er-Stufen **ab der Stufenmitte** (#101010…), ich ab **0** (#000000…) — je Kanal 16
auseinander. Beide Zahlenfolgen bezeichnen dieselben Farben: aus meinem #200000/#600000 wird bei ihm
#301010/#701010. **Bestaetigt**, und seine Kennzeichnung der Quelle ist sauber.

### 1.3 D-a: die Leisten-Endstuecke sind 8 : 17, nicht 64 : 34

`data/bildpaket_dezember.json` fuehrt `leiste_ende_links`/`_rechts` mit `datei: [64, 136]` → **64 : 136 =
8 : 17**; die Anzeige 16 x 34 ist ebenfalls 8 : 17. Meine Zeile „64:34 bei den beiden Leisten-Endstuecken“
war falsch (64 : 34 ist das Verhaeltnis der **Mitte** 256 : 136). **Bestaetigt, mein Fehler.**

### 1.4 Eckenradius 7,5 Prozent: als DATENWERT belegt, nicht am Bild gemessen

`data/gebaeude_motive.json` fuehrt `kachelrahmen.weltkarte_rand: 14` und `kachelrahmen.weltkarte_ecke: 30`
(400er-Kaestchen) → Radius **30/400 = 7,5 %**. Das ist ein gepflegter Datenwert, keine Pixelmessung -
Claude sagt das selbst richtig. **Aber:** `weltkarte_rand: 14` (3,5 %) widerspricht meiner Pixelmessung
**15 px = 3,75 %**; es gilt die Messung (15 px), der Radius bleibt 7,5 % (30 px).

### 1.5 Toleranzen: seine Begruendung ist besser als mein Vorschlag

Ich hatte ±1 px fuer alle Dateien vorgeschlagen. Sein Einwand ist sachlich richtig: bei den kleinen
Dateien (176, 256, 384 px) laesst ±1 px eine 177 x 176-Datei durch, die beim Einpassen eine Spalte
verliert. **Uebernommen:** 0 px bei B1, B2, B10, B12, B13; ±1 px bei den hochgerechneten B5, B8, B9.

---

## 2. Nicht bestaetigt

| Punkt | Claudes Aussage | Meine Messung | Urteil |
|---|---|---|---|
| Wappen der Elfen | `wappen_09` | `assets/wappen/elfen_wappen.png` (1024 x 1024); `wappen_09` ist 274 x 443 und eine **andere** Datei | **WIDERLEGT** - im Briefing gilt `elfen_wappen.png` |

---

## 3. Offen (Daniel entscheidet)

| Punkt | Lage | Meine Empfehlung |
|---|---|---|
| **D8** Goldrahmen im Marktplatz-Kennzeichen | Bestand hat einen Rahmen von rund 3 px (Gold #b8a270, Lichtkante #eee6b6, dunkle Seite #a27239) | **Rahmen bleibt** (Teil der gelieferten Zeichnung, passt zum Auswahlrahmen) |
| **D11** Farbe Kopfband Flickwerk | Wappen `wappen_05` Marineblau **#002040/#103050**, Burg `burg_06` eisblau (HEX unbekannt), F-105 nennt Eisblau/Weiss/Messing | **Marineblau des Wappens** |
| **D-c** Burg gegen Wappen bei TROLLE und GNOME | Trolle: Wappen rot (**#400000/#600000**), Burg `burg_05` gruen/oliv; Gnome: Wappen marineblau, Burg eisblau. Regel vom 05.11. sagt „Farbe folgt dem Bild“ - ohne zu sagen, welchem | **Das Wappen gilt** (so steht es in `data/haeuser.json`: Trolle „Rot, Schwarz und Gold“, Gnome „Grau, Schwarz und Gold“) |

---

## 4. Folge, die niemand bestellt hat: zwei Dokumente zeigten die falschen Wappen

Beim Nachrechnen aufgefallen und berichtigt:

- **`index.html`** (die Besucherseite) zeigte fuenf von sechs Wappen falsch - Bild **und** Text
  (`wappen_05` bei Hammerhall, `wappen_03` bei Sternenwacht, `wappen_02` bei Schattenfaust, `wappen_01`
  bei Knochenmoor, `wappen_06` bei Flickwerk).
- **`FRAKTIONEN_WELTEN.md`** trug dieselbe alte Zuordnung.

Beide folgen jetzt `data/haeuser.json` (Bilder und Kurzbeschreibungen). **`CHRONIK_DER_WELT.md` war
bereits richtig** - ihre Farbangaben stimmen mit `data/haeuser.json` in allen sechs Haeusern ueberein.

---

## 5. Was das fuer das Briefing bedeutet

Claudes Fassung 2 ist **brauchbar und sauber gekennzeichnet** (gemessen / gerechnet / angenommen je
Zeile). Zu uebernehmen: die 18 Dateien mit fuenf Feldern, die Farbtabelle nach `data/haeuser.json`, die
Seitenverhaeltnisse mit 0 px / ±1 px, der Alpha-Test am Farbtyp, die drei gemeldeten Widersprueche
(D-a uebernommen, D-b bestaetigt, D-c offen) und seine Zusatzhinweise Z1 bis Z3 (Radius ueber die
Innenoeffnung messen, Nahtlosigkeit der Leiste in Pixel pruefen, zweite Wache mit Pillow).

**Zu berichtigen vor der Zeichner-Fassung:** Sternenwacht = `elfen_wappen.png`; sonst nichts.
