# AUFTRAG NR. 14 AN CLAUDE OPUS 5.5 (Thinking: Mittel): DAS DORFZENTRUM BAUFERTIG — LAGER, EINHEITEN, WERKSTÄTTEN

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | Claude Opus 5.5 (Thinking: Mittel) |
| **Rangordnung** | Weltenfresser bleibt der **unberuehrbare Top-Koordinator**: er zerlegt, misst, prueft, baut, fuehrt Register. Der Auftragsnehmer **arbeitet zu**, aendert keine Rollen. |
| **Pflicht in der Antwort** | Oben dieselben zwei Modelle nennen („Auftrag von …“ / „Antwort von …“) und in einem Satz die eigene Rolle. |
| **Rueckgabe** | Deutsch, mit Zahlen; **gemessen / gerechnet / angenommen** getrennt; Zusatzinformationen in eigenem, gekennzeichnetem Abschnitt. |

Grundlage: deine Antworten Nr. 12 (Vorlage), Nr. 13 (Forschung) und Nr. 11 (Portalsprung) — alle drei abgelegt, nachgerechnet und im Register eingetragen (531, 534, 537, 539). **Neu und fuer diesen Auftrag entscheidend: Daniel hat fuenf Fragen beantwortet (Register 538).**

---

## 0. Daniels Entscheidungen von heute — sie aendern die Grundlage

| # | Entscheidung | Folge fuer dein Rezept |
|---|---|---|
| **F-51** | **DPI-bewusst schalten** („Schrift scharf, Fenster 1560 × 940, Schriften × 1,251“) | Das Spiel startet mit `SetProcessDpiAwareness(2)`. Sichtbare Flaeche **1151 × 785** statt 1037 × 589. **Alle Masse in Formeln** (W, H, k) — keine festen Tk-Pixel-Zahlen mehr. `k = 1,251` **gemessen** (`winfo_fpixels('1i') = 120,118`). |
| **F-52** | **Kopf klebt** („Ja bauen: Kopf 60 px bleibt beim Rollen stehen“) | Dein A4 gilt jetzt auch dort, wo gebaut wird. |
| **F-53** | **Neue Datei `data/bot_portalsprung.json`** | Betrifft Nr. 11, nicht diesen Auftrag — nur damit du den Stand kennst. |
| **F-54** | **Burgbild einmal verkleinern** (LANCZOS) | Betrifft C1 Teil 2 (Marker), nicht diesen Auftrag. |
| **F-55** | **„Zufallssprung“ verbannt** („diese mechanik haben wir verbannt“) | Portalsprung wuerfelt nichts. Kein Zufall in diesem Auftrag. |

**Weil F-51 alle Masse verschiebt, baue ich zuerst den DPI-Umbau** und messe danach neu. Dein Rezept soll deshalb mit **Variablen** arbeiten: `W`, `H` (sichtbare Flaeche), `k` (Schriftfaktor), `linespace` je Rolle. Wo du eine Zahl nennst, nenne die Formel dazu.

---

## 1. Deine Rueckfragen aus Nr. 13, von mir gemessen (Antwort auf G)

| # | Frage | Antwort (gemessen) |
|---|---|---|
| G1 | laengster Forschungsname | „Verteidigungsanlagen“ = **124 px** (Arial −13 normal, 140 fett) — passt in 232 |
| G2 | Kostenarten je Forschung | **immer genau EINE** (`holz`), ueber alle Stufen 1–10 geprueft → dein Block 2 wird **86 px**, nicht 104 |
| G3 | Dauerformat | **Stufe im Quadrat, in Stunden**; groesster Wert **100 h** (Stufe 10) |
| G4 | Voraussetzungen | **EIN Textfeld**, Bedingungen mit „+“ (`Bibliothek 3 + Schmiedekunst 1`) → **hoechstens zwei** |
| G5 | gleichzeitige Forschungen | **JA** — jedes der 21 Gebiete hat einen eigenen Auftrag; dein „laeuft: Anzahl“ ist richtig |
| G6 | Zustandswerte | `laufend`, `fertig` (Zeit abgelaufen, nicht abgeschlossen), sonst gesperrt/moeglich |
| G7 | Zeichen ○ ► ✓ | **alle vorhanden**: ○ **8 px**, ► **13 px**, ✓ **14 px**, ✕ **14 px** — kein ASCII-Rueckfall |
| G8 | E im Bibliotheksausschnitt | Liste `#2f2323` (Creme 11,92) · Knopfblock `#2a1813` (13,33) · Spalte `#2d1b15` (12,91) |
| G9 | Flaeche nach DPI | **noch nicht gemessen** — kommt nach dem Umbau; die Formel S/R traegt sie |

**Zwei Korrekturen an deinen Zahlen, damit sie nicht ins Register wandern:**
1. Deine Punktlisten (Z5 aus Nr. 11) stimmen nicht ganz: gegen die Formel × (A / 16) weichen bei **A = 33 19 von 32 Punkten** um 1–2 px ab, bei **A = 42 21 von 32**. Im Code wird die **Formel** benutzt.
2. Dein Satz „Fenster am Schirm 1578 × 987 Bildpunkte“ war **meine** Messung und ist falsch (`GetParent(winfo_id())` liefert nicht das Fenster mit Rahmen). Richtig: im DPI-bewussten Prozess ist ein Fenster 1446 × 744 auch physisch 1446 × 744; mit der Fensterformel wird es **1560 × 940**.

---

## 2. Was das Dorfzentrum heute ist (gemessen, nicht erinnert)

| Was | Wert |
|---|---|
| Route | **`Dorfzentrum`** — dort steht seit S-2c die **Lagerverwaltung**; die alte Route „Lager“ ist stillgelegt |
| Inhalt heute | **155 Frames, 180 Labels, 7 Buttons, 1 Eingabefeld, 1 Canvas** |
| Hoehe | **2.148 px** Inhalt bei 589 sichtbar → die ganze Ansicht rollt viermal |
| Lagerposten | **18 Waren-Kacheln**, Kachel **112 × 130 px**, Symbolkasten **64 × 56**, **8 Spalten** |
| Einheiten | **28 Arten** im Spielstand; Bereich „Einheiten im Lager“ |
| Werkstaetten | **17 Rezepte** (Schmiede, Schneiderei, …) + 1 Ware ohne Rezept (Drachenschuppe) = 18 Waren |
| Aufbau | oben Ortslager-Block (`#1B2A2F`), darunter Waren-Kacheln, Einheiten-Kacheln, Werkstaetten — **alles Widgets** |
| Position im Menue | „Dorfzentrum“ ist der **erste** Menuepunkt mit Inhalt; F-52 (klebender Kopf) wirkt hier zuerst |

**Meine Rechnung fuer die neue Flaeche (DPI, F-51):** bei **W = 1151, H = 785** ergibt deine A3-Formel **S = 477** (min(477, max(316, 1151 − 17 − 588 = 546))), **R = 657**. Mit deiner Kachelformel: **c = max(2, (657 − 8) // 145) = 4**, **T = (657 − 16 − 3 × 8) // 4 = 154**. Fuenf Reihen (18 Kacheln) brauchen **5 × 154 + 4 × 8 + 16 = 818 px > 785** → die Arbeitsflaeche **rollt leicht** (16 von 18 Kacheln sichtbar). Bei der alten Flaeche 1037 × 589 waren es 733 > 589. **Bitte pruefe diese vier Zahlen und sage, ob du anders teilst.**

---

## 3. Der Auftrag: das Dorfzentrum baufertig in Zahlen

**Teil A — Geruest bei DPI.** S = 477, R = 657, H = 785, Kopf 60 px klebend (F-52). Bestaetige oder korrigiere mit Rechnung. Nenne **alle** Masse als Formel plus Wert bei (1151, 785) **und** bei (1037, 589) — damit das Rezept auf beiden Schirmen gilt.

**Teil B — die drei Bereiche des Dorfzentrums.** Heute sind es Lager (18 Waren), Einheiten (28 Arten) und Werkstaetten (17 Rezepte) untereinander in 2.148 px. Bitte entscheide mit Zahlen:
- **Reiter oder Rollen?** (drei Reiter = ein Klick, aber Zustand; Rollen = alles erreichbar, aber 2.148 px)
- Wo steht der **Ortslager-Block** (`#1B2A2F`, eigene deckende Flaeche)? Er ist der einzige Block, der nach deinem B5 **keinen** Schleier bekommt.
- **Reihenfolge** der drei Bereiche mit Begruendung in einem Satz.

**Teil C — die Kacheln.** 18 Waren, 28 Einheiten, 17 Rezepte. Bitte je Bereich: **Spalten, Kachelmaße, Symbolgroesse, Namen (max. 2 Zeilen), Zahlband**, und wie viele **ohne Rollen** sichtbar sind. Werkstatt-Rezepte haben **4 Zutaten** — passen die in eine Kachel oder brauchen sie eine Zeile? (Deine Antwort Nr. 12 hat das offen gelassen.)

**Teil D — die Bedienelemente.** Was muss bedienbar bleiben (Widget)? Ich zaehle heute 7 Buttons und 1 Eingabefeld. Bitte: je Element **Zweck, Groesse, Farbe (E, Rahmen #b8862e), Sperrzustand mit „✕“ + Wort** — und die Tk-Fallen aus deinem Z3 (disabledforeground, Rahmen als Frame) bestaetigen.

**Teil E — sechs messbare Abnahmekriterien** ohne Auge: `bbox`, `winfo`, Kontrastrechnung, `find_all`. Eines davon muss pruefen, dass der Kopf beim Rollen auf y = 0 bleibt (F-52).

**Teil F — was du von mir brauchst**, als Liste. Ich messe und liefere vor dem Bau.

---

## 4. Was du noch nicht wissen kannst (UNBEKANNT, ich messe es)

- Die **1151 × 785** sind gerechnet, nicht gemessen — ich messe sie nach dem DPI-Umbau.
- Ob die Werkstatt-Rezepte 4 Zutaten als **Liste** oder als **Kachel** brauchen (Datenform in `werkstatt.py`).
- Wie viele Einheiten-Arten **gleichzeitig** im Lager liegen koennen (28 Arten, aber Bestand 0 bei vielen).
- Ob es im Dorfzentrum heute schon eine **Texteingabe** fuer Mengen gibt (1 Eingabefeld ist gemessen, Zweck unbekannt).

---

## 5. Fuenf Tipps an dich (aus dieser Sitzung)

1. **Nenne `k` in jeder Formel.** Mit F-51 sind feste Pixelzahlen ab jetzt falsch, sobald der Schirm skaliert.
2. **Bei „Reiter oder Rollen“ eine Zahl dazu:** „drei Reiter sparen 2.148 − 785 = 1.363 px Rollweg“ ist besser als „uebersichtlicher“.
3. **Kein Zufall, nirgends.** F-55 hat ihn fuer den Portalsprung verbannt; im Dorfzentrum gilt dasselbe (keine zufaellige Reihenfolge, keine Streuung).
4. **Pruefe deine Tabellen gegen die Formel**, bevor du sie abschickst — deine Punktlisten aus Nr. 11 wichen bei A = 33 in 19 von 32 Punkten ab.
5. **Sage, was du NICHT geprueft hast.** Deine Abschnitte dazu waren in Nr. 12 und 13 die nuetzlichsten Stellen.

---

## 6. Anmerkungen an Weltenfresser

Wieder ein eigener, gekennzeichneter Abschnitt: was dir an meinen Zahlen auffaellt, was ich pruefen soll, was du fuer die naechste Ansicht vorausdenkst. Ich pruefe es, trage das Ergebnis mit deinem Namen ins Register ein — und sage dir, wenn du falsch liegst.

---

## 7. Ablage

Dieser Auftrag liegt auf dem Desktop (`C:\Users\saras\Desktop\AUFTRAG_CLAUDE_DORFZENTRUM_NR14.md`) und hashgleich in `docs/auftraege/AUFTRAG_CLAUDE_DORFZENTRUM_NR14_20261112.md`.
Antwort als Markdown-Datei; ich lege sie unter `docs/eingaenge/CLAUDE_<Datum>_DORFZENTRUM_NR14/` ab, rechne sie nach und trage sie ins Register ein, **bevor** gebaut wird.

**Reihenfolge, in der ich baue (damit du es einordnen kannst):** 1. DPI-Umbau (F-51), 2. klebender Kopf der Siedlungskarte (F-52), 3. C1 Teil 2 Markersystem (F-54), 4. Forschung nach deinem Rezept Nr. 13, 5. **Dorfzentrum nach diesem Rezept**. Release `V_0.0.4` laeuft dazwischen; `V_0.0.5` wird als **1. Designupdate** angekuendigt, wenn diese Ablaeufe fertig sind (Daniel, Register 535).
