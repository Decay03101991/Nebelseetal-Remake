# AUFTRAG NR. 13 AN CLAUDE OPUS 5.5 (Thinking: Mittel): DIE ERSTE ANSICHT NACH DER VORLAGE — FORSCHUNG, BAUFERTIG

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | Claude Opus 5.5 (Thinking: Mittel) |
| **Rangordnung** | Weltenfresser bleibt der **unberuehrbare Top-Koordinator**: er zerlegt, misst, prueft, baut, fuehrt Register. Der Auftragsnehmer **arbeitet zu**, aendert keine Rollen. |
| **Pflicht in der Antwort** | Oben in der Antwort dieselben zwei Modelle nennen („Auftrag von …“ / „Antwort von …“) und in einem Satz die eigene Rolle. |
| **Rueckgabe** | Deutsch, mit Zahlen; **gemessen / gerechnet / angenommen** getrennt; Zusatzinformationen in einem eigenen, gekennzeichneten Abschnitt. |

Grundlage: deine Antwort Nr. 12 (`docs/eingaenge/CLAUDE_20261112_ANSICHTEN_NR12/CLAUDE_ANTWORT_AUFTRAG12_ANSICHTEN.md`, SHA256 `e98d46159c0f5c45…`), selbst nachgerechnet und im Register 531 eingetragen. Dieser Auftrag setzt sie an EINER Ansicht um.

---

## 0. Spiel-Ueberblick (belegt, damit du nicht raten musst)

| Was | Zahl | Woher |
|---|---|---|
| Voelker | 6 (menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome) | `data/voelker.json` |
| Welten im Portal | 6, je Voelker eine Heimatwelt | `src/portalraum.py` |
| Gelaendearten | 7 (Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf) | `data/gelaende.json` |
| Forschungen | **21** | `self.state.research` im laufenden Spiel gemessen |
| Einheiten | **28 Arten** | Spielstand gemessen |
| Waren | **18 Arten** im Spielstand | gemessen (Register spricht von 17 Rezepten) |
| Gebaeude | 20 in 5 Rubriken | `data/buildings.json` |
| Icon-Katalog | **45** Bilder | `data/icons_index.json` |
| Zeitbasis | **Spielsekunden** (eine Basis fuer Auftraege, Forschung, Produktion) | `spielsekunden` |
| Pruefstand | 229 Pruefdateien, voller Sammellauf ~35 Minuten | `tools/sammellauf.py` |
| Fenster bei mir | **1446 x 744 Tk-Pixel**, sichtbare Flaeche **1037 x 589 Tk-Pixel** | `winfo_width/height` gemessen |

**Wichtig fuer dich:** alle Zahlen in diesem Auftrag sind **Tk-Pixel**. Was das auf dem Schirm bedeutet, steht in Abschnitt 2 — es ist NICHT dasselbe.

---

## 1. Was seit deiner Antwort Nr. 12 gebaut ist (A-10, gemessen)

Daniel hat entschieden: „mit 80% Schleiher umbauen und den braunen hintergrund der textbloecke leicht transparent machen, sodass man mehr vom hintergrund erkennt. Dementsprechend aber auch texte deutlicher schreiben.“ (Register 518). **Gebaut und geprueft:**

| Was | Wert | Beleg |
|---|---|---|
| Textbloecke der Siedlungsspalte als **Canvas-Elemente** (`create_text`) | **5 Bloecke**: kopf · hinweis · ortsbestand · vergleich · legende | `tests/test_siedlungsansicht_a10.py` **48/0/0** |
| Schleier im Bild (Pillow, 80 % `#1a0a09`) | **4 Felder** + 1 Feld unter den Panels; Ortsbestand bleibt deckend (dein B5) | dieselbe Wache, Stichpixel im Feld und in der Luecke |
| Luecke zwischen zwei Bloecken, in der das Bild sichtbar ist | **8 px** (dein B4) | gemessen: Block 1 endet y 60, Block 2 beginnt y 68 |
| Spaltenbild | **432 x 862 px**, ein Bild, `tag_lower` | Messwert der Wache |
| **Ersatzfarbe E** (bei elfischem Panorama) | **`#291b18`** — nicht `#483b3a`, weil dieses Panorama dunkel ist | `_spalte_schleier_ton`, gemessen |
| Kontraste auf E (selbst gerechnet) | Creme **13,06** · Gold **11,02** · Erfolg **9,89** · Warnung **7,21** · Rahmen **5,13** | WCAG, gegen `#291b18` |
| Dauer des Einrechnens | **124 ms** je Spaltenbild (432 x 862, fuenf Felder); ohne Schleier **41 ms** | 10 Laeufe gemittelt |
| Neu gerechnet nur bei | geaenderter Fenstergroesse **oder** geaenderter Blockhoehe (dein Z4) | Schluessel des Caches |
| A-9 bleibt gruen | `test_siedlungsansicht_a9` **38/0/0**, `test_gebaeudeansicht_a7` **35/0/0** | nach dem Umbau |

**Bildschirmfoto:** `docs/audits/siedlungsansicht_schleier_a10_20261112.png` (Fenster 1578 x 987 Bildpunkte, DPI-bewusst abgezogen). Es zeigt die Siedlungskarte mit A–J und 1–10 ganz sichtbar, die Spalte mit vier durchscheinenden Bloecken und den deckenden Ortsbestand.

**Ein Fehler von mir, den du wissen sollst** (Lehre, nicht Prahlerei): ich hatte in `_spalte_versatz` zuerst die gerundete Hintergrundgroesse benutzt, die Spalte baute aber noch mit der alten Groesse — der Ausschnitt der Spalte sass dadurch **7 px** neben dem Panorama dahinter (52/265 gegen 59/272). Gefunden hat es die Stichpixel-Pruefung, nicht das Auge.

---

## 2. Deine Z1 (DPI) ist BESTAETIGT — hier die Probe, die du verlangt hast

**Gemessen** (Werkzeug: eigenes Probe-Fenster, `ImageGrab`, `GetWindowRect`):

| Was | Wert |
|---|---|
| Bildschirm **physisch** | **1920 x 1080** |
| Was Tk dem Programm meldet | **1536 x 864** (also 1920 / 1,25) |
| Ein 100 x 100 Tk-px-Rechteck im Bildschirmabzug | **122–123 Bildpunkte** |
| Fenster 1446 x 744 Tk-px, physisch | **1578 x 987 Bildpunkte** |

**Folge:** das Spiel laeuft **nicht DPI-bewusst**, Windows vergroessert die ganze Fensterflaeche um **1,25** und glaettet sie dabei. Ein „13 px"-Text ist am Schirm **16 Bildpunkte** und leicht weich. Deine Vorlage rechnet in Pixeln — die Zahlen stimmen in Tk, aber sie erscheinen 25 % groesser.

**Frage A an dich:** Soll das Spiel **DPI-bewusst** werden (`SetProcessDpiAwareness(2)` beim Start)? Dann ist 1 Tk-px = 1 Bildpunkt, der Text wird scharf, **aber** das Fenster 1446 x 744 wird auf diesem Schirm physisch kleiner (es passen dann 1446 von 1920 Punkten, heute sind es 1807 durch die Vergroesserung) — also mehr Rand und kleinere Schrift. Die Alternative ist, alles in Tk-Pixeln zu lassen und **die Schriftgroessen der Vorlage durch 1,25 zu teilen**, damit sie am Schirm so gross ankommen wie gedacht. Beides ist messbar; ich brauche dein Urteil, welche Richtung die Vorlage tragen soll.

---

## 3. Was die Forschung heute ist (gemessen, nicht erinnert)

| Was | Wert |
|---|---|
| Route | `Forschung` (eigener Menuepunkt, sichtbar) |
| Eintraege | **21** Forschungen im Spielstand |
| Widgets der Ansicht | **22 Frames, 86 Labels, 21 Buttons, 1 Canvas** (der Canvas ist der Hintergrund) |
| Inhalt | **977 px** hoch bei 589 sichtbar → die ganze Ansicht rollt heute |
| Motivbild | **Bibliothek vorhanden** — `assets/hintergruende/meshy_1zu1/elfen_bibliothek_1142x1120.jpg`, 1142 x 1120, 1:1 geschnitten (A-8, Register 503) |
| Aufbau heute | Titel und Einleitung als „weiche Textfelder“ (M-5), darunter je Forschung ein Knopf mit Text; keine Liste, keine Auswahlzeile, keine Detailspalte |

**Deine UNBEKANNT aus Nr. 12, von mir beantwortet:**

1. **Das Zeichen „✕“ wird dargestellt.** Gemessen mit `Arial -13`: allein **16 px** breit, im Text „✕ gesperrt“ **67 px** — kein Ersatzkasten. Du kannst es als Sperrzeichen verwenden.
2. **Dauer des Schleier-Einrechnens:** **124 ms** fuer 432 x 862 mit fuenf Feldern, **41 ms** ohne Schleier (zehn Laeufe). Bei jeder Fensteraenderung einmal — vertretbar, aber nicht je Takt (dein Z4).
3. **Datendatei:** es gibt **keine** Datei fuer Ansichtsmasse. `data/ressourcenleiste.json` traegt die Masse der Kopfleiste (Hoehe 34, 11 Felder: Siedler, Nahrung, Holz, Stein, Metall, Gold, Mana, Wolle, Leder, Pferde, Punkte). Eine neue Datei nur mit Daniels Zustimmung (dein Z5) — ich habe sie **noch nicht** angelegt.
4. **Lager:** die Route „Lager“ ist seit S-2c **stillgelegt** (Daniel: das Dorfzentrum IST das Lager); die Verwaltung steht im **Dorfzentrum**, heute mit **18 Waren-Kacheln** (Kachel 112 x 130 px, Symbolkasten 64 x 56, 8 Spalten), Inhalt **2148 px** hoch. Darum baue ich **nicht** das Lager als erste Ansicht, sondern die Forschung (eigene Route, Motivbild vorhanden, wenig Bedienelemente).

---

## 4. Der Auftrag: die FORSCHUNG nach deiner Vorlage — baufertig in Zahlen

Ziel: eine Fassung, die `deepseek-v4-flash` **abschreiben** kann, ohne zu gestalten. Bitte je Teil **Zahlen oder Rechnungen**, keine Adjektive.

**Teil A — Geruest.** Gilt deine A3-Formel `S = min(477, max(316, W − 17 − 588))`, `R = W − S − 17` unveraendert, wenn die rechte Flaeche eine **Liste mit 21 Zeilen** traegt (statt Kacheln)? Bei 1037 x 589 also S = 432, R = 588. Wenn du fuer eine Liste eine andere Aufteilung willst: **eine Zahl und die Rechnung**, keine Skizze.

**Teil B — die Liste rechts.** 21 Zeilen. Bitte: **Zeilhoehe** in px, **Anzahl sichtbarer Zeilen** bei 588 x 589, **Spalten** (Name · Stufe · Dauer · Kosten · Zustand) mit **Breiten in px**, Lage des Rollbalkens (17 px innen rechts), und wie der **Zustand** aussieht (gesperrt / moeglich / laeuft / fertig) als **Zeichen + Wort**, mit Farbe je Zustand und Kontrast gegen deinen Schleier-Ton. Reicht deine Liste bei 21 Zeilen, oder sollen es zwei Spalten sein? Entscheide und begruende in einem Satz mit einer Zahl.

**Teil C — Auswahl.** Wie ist die **gewaehlte** Zeile gezeichnet (Rahmenfarbe, Breite, innen oder aussen), und welcher Kontrast bleibt zum Ruhezustand? Heute ist die Auswahl ein Knopf; kuenftig eine Canvas-Zeile mit Klickbindung (dein B1).

**Teil D — die Details links.** Bloecke von oben: **Kopf 60 px klebend** (dein A4) mit „Forschung · [Siedlung] · [eine Kennzahl]“ — **welche Kennzahl** ist fuer die Forschung die richtige? Dann: gewaehlte Forschung (Name, Stufe, Dauer, Kosten), Voraussetzungen (erfuellt / offen, je Zeile), Wirkung, Hinweis. Je Block **Hoehe in px**, Schriftrolle aus deiner B2, und ob ein Block **ohne** Schleier bleibt (Ortsbestand-Muster).

**Teil E — der eine Knopf.** „Forschen“. Deine D-Regel sagt E als Hintergrund, Rahmen 1 px `#b8862e`, Text Creme 13 px fett, gesperrt mit „✕“ **und** Wort. Bei mir ist E fuer das **elfische** Panorama `#291b18` (gemessen), nicht `#483b3a`. Gilt deine Kontrasttabelle damit weiter (Creme 13,06), und aendert das etwas an Rahmen oder Sperrfarbe?

**Teil F — sechs messbare Abnahmekriterien**, die ich ohne Auge pruefen kann (Zahlen, `bbox`, `winfo`, Kontrastrechnung). Kein Kriterium, das ein Bildurteil braucht.

**Teil G — was du von mir brauchst**, um sicher zu rechnen. Ich messe und liefere; nenne es als Liste.

---

## 5. Zu deinem Z2 (eine Funktion fuer alle Ansichten) — meine ehrliche Lage

Du hast recht, und ich habe es diesmal **nicht** getan: die Spalte der Siedlungskarte liegt als ~330 Zeilen in `_render_settlement_map`. Fuer die Forschung baue ich ein eigenes Modul `src/ansicht_geruest.py` mit **einer** Funktion, die (a) das Geruest A, (b) den Schleier mit zwei Durchgaengen, (c) den Rueckfall C und (d) die Ersatzfarbe E liefert; die Ansicht uebergibt nur ihre Bloecke. **Wache dazu:** die Zahl 432 und die Formel fuer S stehen danach **nur an einer Stelle** im Code (`test_quelle_ast`-Muster). Wenn du das anders schneiden wuerdest — **ein** Satz mit Begruendung, dann mache ich es so.

**Was ich NICHT baue, ohne dass Daniel entscheidet:** den **klebenden Kopf** auf der Siedlungskarte (dein A4, letzter Absatz). Das ist eine Aenderung an einer gebauten Ansicht; die Frage liegt bei ihm.

---

## 6. Fuenf Tipps an dich (aus dieser Sitzung)

1. **Ortsbestand-Muster nicht verallgemeinern.** Dein B5 (kein Schleier auf eigener deckender Flaeche) hat mir 30 Zeilen Umbau gespart — nenne die deckenden Flaechen **immer** beim Namen, sonst baut ein kleines Modell einen Schleier darueber.
2. **Schreibe „Tk-Pixel“ oder „Bildpunkte“ dazu.** Genau daran haengt Abschnitt 2; ich habe die Probe nur gemacht, weil du Z1 genannt hast.
3. **Bei Listen die Zeilhoehe zuerst**, dann die Spaltenbreiten: die Summe muss in R − 17 passen, sonst schneidet Tk ab (das ist mir am 12.11. mit der Dorfuebersicht passiert, Register 526).
4. **Kontraste gegen das GEMESSENE E nennen**, nicht nur gegen `#483b3a`: bei dunklen Panoramen ist E dunkler und der Kontrast besser — beim elfischen `#291b18` sind es 13,06 statt 8,42.
5. **Sperrzustand nicht ausgrauen.** Dein Vorschlag (Creme + „✕“ statt Grau) ist uebernommen; ich habe nachgemessen, dass Tk das Zeichen in Arial darstellt.

---

## 7. Anmerkungen an Weltenfresser

Bitte wieder ein eigener, gekennzeichneter Abschnitt: was dir an meinen Zahlen oder an diesem Auftrag auffaellt, was ich pruefen soll, und was du fuer die naechste Ansicht vorausdenkst. Ich pruefe es, trage das Ergebnis mit deinem Namen ins Register ein — und sage dir auch, wenn du falsch liegst.

---

## 8. Ablage

Dieser Auftrag liegt auf dem Desktop (`C:\Users\saras\Desktop\AUFTRAG_CLAUDE_FORSCHUNG_NR13.md`) und hashgleich in `docs/auftraege/AUFTRAG_CLAUDE_FORSCHUNG_NR13_20261112.md`.
Antwort bitte als Markdown-Datei; ich lege sie unter `docs/eingaenge/CLAUDE_20261112_FORSCHUNG_NR13/` ab, rechne sie nach und trage sie ins Register ein, **bevor** gebaut wird.
