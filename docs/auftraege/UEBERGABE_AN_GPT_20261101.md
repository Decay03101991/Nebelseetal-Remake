# ÜBERGABE AN DICH (ChatGPT) — Aufgaben für heute, 01.11.2026

Diese Übergabe ist zum Kopieren gedacht. Sie sagt dir, was du heute liefern sollst, in welcher
Reihenfolge, und unter welchen Bedingungen. Das eigentliche Aufgabenblatt ist **Auftrag C2**; diese
Seite ist der Rahmen darum.

---

## 1. Worum es geht

Wir bauen „Nebelseetal Remake“ — ein Remake des Browserspiels „Nebelseetal Online“ (2005–2009) als
lokale Anwendung. Du bist der Gestalter: du lieferst Bilder, keine Regeln. Jede Zahl im Spiel stammt
aus dem Originalhandbuch oder aus einer ausdrücklichen Entscheidung von Daniel; beides kann ich dir
auf Nachfrage nennen.

---

## 2. Was du schon geliefert hast — und was daraus geworden ist

**Geliefert am 01.11.:** 20 Gebäude-Illustrationen, 20 Menü-Hintergründe, 4 Original-Entwurfstafeln,
`asset_manifest.json`, `Gebäude_Designs_Update.md` — in vier ZIPs, je unter 8 MB. Das hat
funktioniert und war gut.

**Geprüft und übernommen:**

- Die **20 IDs** deines Manifests stimmen **eins zu eins** mit den 20 Gebäuden im Spielcode überein.
  Kein Eintrag fehlt, keiner zu viel. Das ist der Grund, warum wir mit dir weiterarbeiten.
- Die **20 Menü-Hintergründe** (je 538 × 222 px) sind für die Gebäudeansicht brauchbar.
- Die **20 Icons** sind schön und werden im Menü und im Baudialog verwendet — aber sie sind
  **gerahmte Buttons mit gemalter Umgebung** (256 × 256 px, keine Transparenz). Auf dem Spielfeld
  verdecken sie das Gelände. Darum braucht es heute die freigestellten Kartenmotive (Teil A von C2).

**Eine Lehre aus einem früheren Textpaket:** darin standen sieben Widersprüche zu den tatsächlichen
Spielwerten. Seitdem gilt: **keine Zahl ohne Quelle.** Wenn du eine brauchst und sie steht nicht in
deinem Auftrag, fragst du — du schätzt nicht.

---

## 3. Was heute ansteht

### Zuerst: Auftrag C2 (liegt als eigenes Dokument bei)

Vier Teile, rund 31 Bilder:

| Teil | Inhalt | Anzahl |
|---|---|---|
| A | **Freigestellte Kartenmotive** je Gebäude — ohne Rahmen, ohne Szene, transparent, bei 44 px erkennbar | 20 |
| B | **Ressourcenleiste** — ein Entwurf plus 8 freigestellte Symbole (Gold, Holz, Stein, Erz, Nahrung, Mana, Siedler, Punkte) | 9 |
| C | **Kachelrahmen** 64 × 64 px, als 9-Slice, einmal Ruhe und einmal Auswahl | 2 |
| D | **Manifest und Lieferschein** | 2 |

**Das ist der Hauptauftrag für heute.** Er ist wichtiger als alles andere auf dieser Seite.

### Danach, wenn du Zeit hast: Auftrag C1 (liegt ebenfalls bei)

Die Demo-Begleittexte (Spielerhandbuch, FAQ, README, bekannte Grenzen). C1 wurde vorbereitet, aber
noch nie gefahren. Nimm ihn **erst nach C2** — die Bilder sind der Engpass im Spiel, die Texte nicht.

---

## 4. Lieferregeln (gelten für alle Lieferungen, ohne Ausnahme)

1. **Höchstens 8 MB je ZIP.** Das Gesamtpaket beim ersten Versuch war 22,6 MB und nicht
   herunterladbar. Vier ZIPs unter 8 MB waren kein Problem. Bleib dabei.
2. **Dateien direkt anhängen**, keine Download-Links, keine HTML-Seiten. Eine gespeicherte
   Chat-Seite enthält keine Bilder (`blob:`-Verweise verfallen).
3. **Dateinamen exakt wie im Auftrag.** Die Namen sind IDs im Spielcode; Abweichungen kosten uns Handarbeit.
4. **Ein Manifest je Lieferung**, ein Eintrag je Bild mit ID, Pfad, Pixelmaß und Zweck.
5. **Am Ende deiner Antwort eine kurze Liste:** welche ZIPs mit welcher Größe und welchem Inhalt,
   und was du **nicht** geliefert hast. Keine langen Erklärungen.
6. **Was du nicht kannst, sagst du.** Du ersetzt nichts durch etwas anderes und erfindest keinen Ersatz.

---

## 5. Was du nicht liefern sollst

- **Keine Spielregeln, Zahlen, Tabellen oder Balancing-Vorschläge.** Die kommen aus dem Original.
- **Keine** Wappen, Burgen oder Einheitenbilder — die sind vorhanden und abgestimmt.
- **Keine** Menü-Hintergründe — die 20 vorhandenen bleiben.
- **Keine Python-Dateien** und keine Zuordnungs-Skripte. Zwei Wahrheiten über Dateizuordnungen
  hatten wir schon einmal; das räumen wir nicht wieder auf.
- **Keine ZIPs über 8 MB**, keine Sammelpakete, keine Startseiten mit Links.

---

## 6. Reihenfolge für heute

1. **C2, Teil A** (Kartenmotive) — das ist der Engpass. Wenn nur ein Teil fertig wird, dann dieser.
2. **C2, Teil B und C** (Ressourcenleiste, Kachelrahmen).
3. **C2, Teil D** (Manifest, Lieferschein) — ohne ihn können wir nichts einbauen.
4. **C1** (Begleittexte), nur wenn C2 vollständig geliefert ist.

Wenn du bei einem Teil hängst: liefer die anderen fertig und benenne den offenen Teil mit einem
Satz Grund. Ein halbes Paket mit klarer Ansage ist brauchbar; ein volles Paket mit erfundenen
Bestandteilen ist es nicht.
