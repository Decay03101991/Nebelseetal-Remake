"""Baut den Auftrag fuer die EXTERNE Gegenpruefung (ChatGPT, Abo - keine Kostenbremse noetig).

Daniel (31.10.2026): "leg mir den prompt fuer das grosse model einmal als kopie auf den desktop
... ich will eine andere ki das ganze nochmal komplett extern pruefen lassen. er braucht einfach
nur die pfade zu den daten auf github da er nicht lokal auf daten zugreifen kann."

Deshalb enthaelt der Auftrag:
  * nur OEFFENTLICHE GitHub-Pfade (am 31.10.2026 per API geprueft: HTTP 200),
  * die zwei Originaldokumente, die als .odt vorliegen, im VOLLTEXT (ChatGPT kann .odt nicht lesen),
  * das Pruefregister in Kurzform (was NICHT erneut zu pruefen ist),
  * drei klar umrissene Aufgaben mit festem Ausgabeformat,
  * die Liste der Dateien, die es NOCH NICHT auf GitHub gibt (lokal, Stand 31.10.).

Ergebnis:
  docs/audits/AUFTRAG_EXTERNE_PRUEFUNG_20261031.md
  C:\\Users\\saras\\Desktop\\AUFTRAG_EXTERNE_PRUEFUNG_20261031.md   (Kopie fuer Daniel)

Aufruf: python -X utf8 tools/externe_pruefung_prompt_bauen.py
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import zipfile

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(HIER, "docs", "audits", "AUFTRAG_EXTERNE_PRUEFUNG_20261031.md")
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop",
                       "AUFTRAG_EXTERNE_PRUEFUNG_20261031.md")

RAW = "https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/"

# (Pfad im Repo, was darin steht, oeffentlich am 31.10.2026 geprueft)
DATEIEN = [
    ("docs/original/Spielanleitung_2009_Textfassung.txt",
     "**Die Hauptquelle:** Spielanleitung 2009 im Volltext, 1.366 Zeilen mit Seitenmarken. "
     "Zitate im Projekt nennen „Z. 1216“ = Zeile in DIESER Datei.", True),
    ("docs/original/ORIGINAL_Kampf_und_Punkte.md",
     "Auswertung der Handbuchseiten 4/5 und 18–23 (Auftragsarten, Kampf, Punkte, Götterschutz).", True),
    ("docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md",
     "Auswertung: Einheiten, Waren, Rohstoffe, Gebäude, Forschung.", True),
    ("docs/original/ORIGINAL_Werte_Einheiten.md",
     "Einheitenwerte (LE/AT/PA/RS/TP/GS/MU/SK) aus dem Handbuch.", True),
    ("docs/original/Spielanleitung_2005/portal.php.txt",
     "Vorversion 2006: Portal, Limbus, 20 Dimensionen, 20×20, 5.000 Mana, 24 h.", True),
    ("docs/original/Spielanleitung_2005/rohstoffe.php.txt",
     "Vorversion 2006: Rohstofftabelle (weicht teils vom Handbuch ab).", True),
    ("docs/original/Spielanleitung_2005/einheiten.php.txt",
     "Vorversion 2006: Einheiten, Ausbildungsdauer, Herstellerregel.", True),
    ("docs/original/Spielanleitung_2005/punktesystem.php.txt",
     "Vorversion 2006: Punkte je Einheit und Gesamtpunktzahl.", True),
    ("docs/original/Spielanleitung_2005/warentabelle.php.txt",
     "Vorversion 2006: Warenvoraussetzungen (vollständig nur dort).", True),
    ("docs/original/Spielanleitung_2005/forschungstabelle.php.txt",
     "Vorversion 2006: Forschungstabelle.", True),
    ("docs/original/Spielanleitung_2005/siedeln.php.txt",
     "Vorversion 2006: Siedlungen gründen, Siedlergrenze.", True),
    ("docs/AKTUELLER_STAND.md",
     "Selbstauskunft des Projekts: was gebaut ist, was offen ist (Stand 28.–30.10.).", True),
    ("docs/ENTWICKLUNGSPROTOKOLL.md",
     "Entwicklungsprotokoll mit Kennungen, Prüfzahlen und Kosten (das EINE Protokoll).", True),
    ("data/buildings.json",
     "20 Gebäude: Kategorien, Baupreise je Stufe, Voraussetzungen, Erträge, Wallschwellen.", True),
    ("data/units.json",
     "28 Einheiten mit allen Originalwerten, Kriegspunkten, Ladung, Gebäude, Voraussetzung.", True),
    ("data/research.json",
     "21 Forschungen mit Wirkungstext und Kosten (Handbuch 2009, Abweichungen zur Vorversion).", True),
    ("data/resources.json",
     "9 Rohstoffe, Erträge je Stunde, Startwerte, Siedlergrenze.", True),
    ("data/gelaende.json",
     "Geländearten, Bebaubarkeit, Erträge je Gelände.", True),
    ("data/warenrezepte.json",
     "Waren: Kosten, Dauer, Forschungsvoraussetzungen.", True),
    ("data/gebaeude_wirkung.json",
     "Wirkungen der Gebäude (Siedlergrenze, Forschung, Ausbildung, Verteidigung).", True),
    ("data/spielzeit.json",
     "Spieluhr: Faktor 180 (1 echte Sekunde = 180 Spielsekunden).", True),
    ("src/kampf.py",
     "AKTIVES Kampfsystem (neueres Original-Forumssystem, 15 Profile, Wallvorrunde, Sequenzen).", True),
    ("src/kampfbericht.py",
     "Wallvorrunde, Mauerschaden, Beute, Kampfbericht.", True),
    ("src/auftraege.py",
     "Aufträge: Reisezeit, Rückkehr, Ladung, Auftragsarten, offene Lücken.", True),
    ("src/punkte.py",
     "Punkte: Kriegspunkte je Einheit + Wallstufe³, Gesamt = (Krieg+Forschung)/2, Zielzahl 300 (VORSCHLAG).", True),
    ("src/forschung.py",
     "Forschung: Dauer = neue Stufe² in Stunden, Kostenverdopplung, Siedlungssperre.", True),
    ("src/wirtschaft.py",
     "Produktion: Erträge, Forschungsboni, Verbrauch.", True),
    ("src/main.py",
     "Spielschicht und Oberfläche (7.139 Zeilen; für gezielte Fragen, nicht komplett lesen).", True),
    ("docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md",
     "**Original-Hintergrundgeschichte** des Spiels (Website-Archiv 11.09.2007, drei Teile): drei "
     "Drachenbrueder, Erschaffung des Nebelseetals, Salmurs Magie, das Chaos. Grundlage der Legende.", True),
    ("Vorausarbeit gpt chat/Fehlerregister_Nebelseetal.md",
     "Bekannte Fehler und Designprüfungen (u. a. Sieggrenze 300 gegen Originalpunkte).", True),
]

LOKAL_NUR = [
    ("docs/PRUEFREGEL_ORIGINAL.md",
     "**Prüfregister mit 40 belegten Punkten** (Seite/Zeile je Punkt). In diesem Auftrag als "
     "Kurzliste in Abschnitt 5 enthalten, damit nichts doppelt geprüft wird."),
    ("docs/quellen/ABWEICHUNGEN_2006_zu_2009.md",
     "Alle messbaren Abweichungen Vorversion 2006 gegen Handbuch 2009, mit Regel „Balance 2009, "
     "Struktur beide“."),
    ("docs/original/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md",
     "Handbuch S. 9–14: Freischaltung über Forschungsstufen, Dauer Stufe², Kostenverdopplung, Ertragstabelle."),
    ("docs/ENTWURF_WEGZEIT_KAMPF_WELT_20261031.md",
     "Entwurf des starken Modells für Wegzeit, Kampfablauf, Weltlage (195 Zeilen) — VORSCHLAG, teils widerlegt."),
    ("docs/ENTWURF_AUSBILDUNG_HERSTELLER_20261030.md",
     "Entwurf Ausbildung und Hersteller (311 Zeilen) — VORSCHLAG."),
    ("docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md",
     "Prüfbericht dieses Entwurfs gegen Handbuch und Code (6 falsche Aussagen belegt, Entscheidungen E1–E5)."),
    ("docs/audits/BEWEGUNGSSYSTEME_LANDKARTE.md",
     "Landkarte der ZWEI Bewegungssysteme im Code (zwei Formeln, zwei Beuteregeln)."),
]


def lies(pfad: str) -> str:
    with open(os.path.join(HIER, pfad), encoding="utf-8", errors="replace") as f:
        return f.read()


def odt_text(pfad: str) -> str:
    with zipfile.ZipFile(os.path.join(HIER, pfad)) as z:
        x = z.read("content.xml").decode("utf-8")
    x = re.sub(r"</text:p>", "\n", x)
    t = re.sub(r"<[^>]+>", "", x)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def register_kurz() -> str:
    """Die 40 Registerpunkte als Kurzliste: Nummer, Kernaussage, Urteil."""
    with open(os.path.join(HIER, "docs", "PRUEFREGEL_ORIGINAL.md"), encoding="utf-8") as f:
        text = f.read()
    zeilen = []
    for zeile in text.splitlines():
        m = re.match(r"\|\s*(\d{1,2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([\d.]+)\s*\|\s*$",
                     zeile)
        if not m:
            continue
        nr, sache, quelle, urteil, _stand = m.groups()
        sache = re.sub(r"\*\*|~~", "", sache)
        sache = sache.split("|")[0].strip()
        if len(sache) > 190:
            sache = sache[:187] + "…"
        kurz = urteil.replace("**", "").split("—")[0].strip()
        if len(kurz) > 60:
            kurz = kurz[:57] + "…"
        zeilen.append(f"{nr}. {sache} — *{kurz}*")
    return "\n".join(zeilen)


VORSPANN = """# AUFTRAG: Externe Gegenprüfung des „Nebelseetal-Remake"

**Für:** ein externes KI-Modell mit Internetzugriff (ChatGPT), das die Dateien über die unten
stehenden GitHub-Pfade selbst öffnet. Kein lokaler Zugriff nötig, keine Dateien anzuhängen
(außer den zwei Dokumenten, die in Abschnitt 4 im Volltext stehen).
**Von:** Daniel Kössl · **Erstellt:** 31.10.2026 · **Sprache der Antwort:** Deutsch

---

## 0. Worum es geht

Ein deutsches Browsergame von 2005/2009 („Nebelseetal Online") wird als **Einzelspieler-Spiel**
in Python/tkinter neu gebaut, spielbar gegen Bots, mit Spieluhr ×180. Deine Aufgabe ist **nicht**,
Code zu verbessern, sondern **Originaltreue zu prüfen**: Wo weicht das Remake von den
Originalquellen ab, wo wird eine Regel erfunden, wo fehlt eine belegte Mechanik — und wo sind die
belegten Zahlen bei Spieluhr ×180 unspielbar. Du bist die **zweite, unabhängige Meinung**; ein
anderes Modell hat dieselben Quellen schon einmal geprüft, und du sollst nicht abnicken, sondern
widersprechen, wo es etwas zu widersprechen gibt.

## 1. Die Regeln, nach denen das Projekt arbeitet (daran misst du es)

1. **NEUESTE FASSUNG IST DAS ORIGINAL.** Gibt es zu einer Mechanik zwei Fassungen, gilt die neuere.
   **ABER:** Nennt die neuere Fassung nur **Werte** und beschreibt die ältere Fassung die
   **Mechanik**, dann gilt **Mechanik aus der älteren, Zahlen aus der neueren** Fassung. Das ist eine
   begründete Zusammenführung, keine Erfindung — kennzeichne sie als `ZUSAMMENFÜHRUNG` und nenne
   beide Quellen mit Stelle.
2. **Was die Quellen nicht hergeben, ist VORSCHLAG** und muss als VORSCHLAG erkennbar sein. Es wird
   nichts erfunden und nichts „geschätzt, bis es passt".
3. **Daniels eigene frühere Annahmen sind verwerfbar**, wenn die Quellen etwas anderes vorgeben
   (Beispiel: ein Sieg bei 300 Gesamtpunkten ist bereits **verworfen**, weil das Handbuch ausdrücklich
   sagt: „Jeder hat bei Nebelseetal sicher seine eigenen Ziele").
4. **Einzelspieler statt Mehrspieler:** Das Original war ein Browsergame mit vielen Spielern; hier
   spielt **ein Mensch gegen wenige Bots**. Wo eine Regel nur wegen vieler Spieler existiert (z. B.
   20 Dimensionen als Platz für hunderte Welten), darf sie für den Einzelspieler **neu gedeutet**
   werden — aber so, dass sie Sinn ergibt und die Originalmechanik erkennbar bleibt.
5. **Belegpflicht:** jede Behauptung mit Datei **und** Zeile (bzw. Seite). Kannst du etwas nicht
   belegen, schreibst du „nicht belegbar" — das ist ein vollwertiges Ergebnis.
6. **Einmal prüfen, festschreiben:** Abschnitt 5 listet 41 bereits belegte Punkte. Prüfe sie nicht
   erneut, außer du findest einen echten Widerspruch — dann sag es ausdrücklich.

## 1a. Was Daniel am 31.10.2026 bereits entschieden hat (nicht mehr fragen)

| Frage | Entscheidung |
|---|---|
| Reiseformel | **Dauer = 2 × Distanz ÷ GS** (Arbeitsformel, ausdrücklich anpassbar; Grund: bei Spieluhr ×180 wären Wege sonst zu kurz für Vorwarnzeit) |
| Dimensionswechsel | kostet **keine Zeit**, nur Mana — und die 20 Dimensionen werden für den Einzelspieler zu **Ländereien** umgedeutet (hunderte Spieler brauchten Platz, ein Spieler nicht) |
| Beute | **gestaffelt**: erster Angriff (Mauer steht) reißt die Mauer ein und bringt **wenig**; ist die Mauer schon eingerissen, **viel**; ohne Verteidiger darf der Bestand **komplett** mit, begrenzt durch die Karrenladung |
| Sieg | **kein Sieg** wie im Original; stattdessen **Bewertung/Auszeichnungen** (meiste Forschungspunkte, meiste Kriegspunkte, größte Wirtschaftsmacht) und freies Weiterspielen |
| Antrieb ohne Mitspieler | Im Mehrspieler-Spiel ist der Antrieb automatisch da (andere Spieler, Vergleich). Das Einzelspieler-Spiel muss ihn **selbst erzeugen** — gesucht sind Ideen auf **bestehenden** Mechaniken (Bots als Messlatte, Ranglisten, Bestwerte, Auszeichnungen); eine **Legende** ist ein mögliches Mittel, **kein Ersatz** |

**Deine Aufgabe ist, diese Entscheidungen zu prüfen, nicht sie zu wiederholen.** Widerspricht eine
Entscheidung den Quellen, sag es mit Stelle.

## 2. Stand der Veröffentlichung (wichtig für deine Zitate)

* Öffentlich auf GitHub ist ein **Stand, der laufend nachgezogen wird** (zuletzt: die Nacht vom
  30./31.10.2026). Prüfe deshalb **immer den neuesten Commit** im Repo (`main`) und nenne in deiner
  Antwort den Commit-Stand, den du gelesen hast. Alle Pfade in Abschnitt 3 sind am 31.10.2026
  geprüft und abrufbar.
* **Noch nicht veröffentlicht** (liegen nur lokal, Abschnitt 3.2): das Prüfregister, die
  Abweichungsdatei 2006/2009, zwei Entwürfe und zwei Prüfberichte. Das Prüfregister ist in
  Abschnitt 5 als Kurzliste enthalten; die anderen Papiere kannst du nicht lesen — bewerte sie
  nicht, sondern nenne sie „nicht einsehbar", wenn eine Frage dorthin führt.
* Das Projekt selbst hat seit dem 28.10. weitergearbeitet (Menüs, Sperrmeldungen, Punkteleiste).
  Wenn du eine Stelle im Code nicht findest, liegt es daran — nicht an dir.

---

## 3. Die Dateien

### 3.1 Öffentlich (GitHub, Rohdateien)

Alle Adressen haben die Form `""" + RAW + """<pfad>`.
Öffne sie **direkt als Text**, nicht über die GitHub-Oberfläche.

| Datei | Was darin steht |
|---|---|
"""


def main():
    teile = [VORSPANN]
    for pfad, zweck, _ in DATEIEN:
        teile.append(f"| `{pfad}` | {zweck} |")
    teile.append("\n### 3.2 Nur lokal vorhanden (nicht abrufbar — nur zur Kenntnis)\n\n")
    teile.append("| Datei | Was darin steht |\n|---|---|\n")
    for pfad, zweck in LOKAL_NUR:
        teile.append(f"| `{pfad}` | {zweck} |")

    teile.append("""

---

## 4. Drei Originaldokumente im Volltext

Die ersten beiden liegen im Projekt nur als `.odt` vor (ChatGPT kann das Format nicht lesen). Deshalb
stehen sie hier wörtlich. **Sie sind eine Originalquelle und widersprechen dem Handbuch in mehreren
Punkten** — genau das ist eine deiner Fragen (Aufgabe A). Das dritte ist die Original-Geschichte.

### 4.1 „Das Kampfsystem" (neueres Original-Forumssystem, Spielerfund)

```text
""" + odt_text("docs/quellen/Das_Kampfsystem_Neu_Original.odt") + """
```

### 4.2 „Wissenswertes" (Punktesystem, Rohstoffproduktion, Einheitenwerte)

```text
""" + odt_text("docs/quellen/WeitereWerteKampfsystem_Original_28-10-2026.odt") + """
```

### 4.3 Die Original-Hintergrundgeschichte des Spiels (Website, Capture 11.09.2007)

**Das ist die Grundlage für die Legende (Aufgabe D).** Drei Drachenbrüder, die Erschaffung des
Nebelseetals, Salmurs Magiegeschenk und das daraus folgende Chaos. Wörtlich aus dem Website-Archiv.

```text
""" + lies("docs/quellen/ORIGINAL_HINTERGRUNDGESCHICHTE.md") + """
```

---

## 5. Was bereits belegt ist — bitte NICHT erneut prüfen

Diese 45 Punkte sind gegen Handbuch 2009 bzw. die 2006er Seiten geprüft und mit Seite/Zeile
festgeschrieben. Nenne einen Punkt nur dann erneut, wenn du einen **Widerspruch** findest.

""" + register_kurz() + """

---

## 6. Deine vier Aufgaben

Arbeite sie in dieser Reihenfolge. Für jede gilt: **rechnen und entscheiden, nicht beschreiben.**

### Aufgabe A — Kampf: welche Quelle gilt für welchen Schritt, und wie wird die Beute gestaffelt?

Es gibt zwei Originalquellen für den Kampf: das **Handbuch 2009** (LE, AT, PA, MU, RS, TP; Zweikampf
in Kampfrunden; Erschöpfung −1 AT/PA) und das **neuere Forumssystem** aus Abschnitt 4.1
(Konstitution %, Kampfwert-Spanne, Rüstung, Fernkampfwert, Erschöpfungsschaden, Schwelle zur
Kampfunfähigkeit). Das Forumssystem nennt **weder Beute noch Geräteverlust noch Punkte**.

**Verlangt:** eine Tabelle „Kampfschritt | gilt | Quelle (Dokument + Stelle) | Art (belegt /
ZUSAMMENFÜHRUNG / VORSCHLAG)" für Wallvorrunde, Mauerschaden, Fernkampf, Nahkampf/Zweikampf,
Erschöpfung, Flucht, Ausgang, Beute, Geräteverlust, Punkte. Danach höchstens sechs Stellen, an denen
beide Quellen **unvereinbar** sind, je mit der kleineren Änderung. Und die **gestaffelte Beute**
(Daniels Vorgabe): konkrete Prozentwerte für „Mauer steht noch", „Mauer schon eingerissen", „keine
Verteidiger mehr" samt Formel und Eingaben (Wallzustand vor/nach dem Kampf, überlebende Verteidiger,
Karrenladung, Ortslager). Sag ausdrücklich, ob die Staffelung den Originalregeln widerspricht.

### Aufgabe B — Wegzeit, Auftragskosten und Portal: ein Zahlensystem für einen Einzelspieler

Belegt: GS = Reisegeschwindigkeit; Zeitangaben gelten für **eine Strecke**, Rückkehr dauert doppelt;
Geschwindigkeit ist in 10-%-Schritten drosselbar (langsamer = weniger Gold, mehr Nahrung); Aufträge
zu fremden Siedlungen kosten zusätzlich **Mana nach Entfernung**; ein Weltwechsel kostet 5.000 Mana
und ist einmal je 24 h möglich; 20 Dimensionen, je 20×20 Felder. **Keine Quelle nennt eine Formel.**

Entschieden ist die Arbeitsformel `Dauer = 2 × Distanz ÷ GS`. **Verlangt:** diese Formel
nachrechnen (6, 16, 32 Felder × GS 5 und GS 35, Spielstunden **und** Echtzeit bei ×180, Hin- und
Rückweg), eine Kostentabelle (Gold, Nahrung, Mana je Einheit und Strecke) und — weil ein Spieler
keine 20 Dimensionen braucht — **zwei Varianten, wie aus den Dimensionen „Ländereien" werden** (was
das Portal dann ist, welche Mana-Kosten bleiben sinnvoll), mit Empfehlung.

### Aufgabe C — Spielbarkeit bei ×180 und Bewertung statt Sieg

Das Original hat **keine Siegbedingung** (Handbuch S. 3: „Jeder hat bei Nebelseetal sicher seine
eigenen Ziele" — Feldherr, Forscher oder Händler). Ein Ziel bei 300 Gesamtpunkten ist **verworfen**.
**Verlangt:** eine Tabelle „Größe | belegter Wert | Wirkung bei ×180 (gerechnet) | Urteil (spielbar /
zäh / unspielbar)" für Produktion, Siedlerzuwachs, Forschungsdauer, Ausbildungszeiten, Kriegspunkte,
Verteidigungsanlagen (Stufe³) — und danach ein **Auszeichnungssystem mit höchstens sechs
Auszeichnungen**, das die drei genannten Spielziele abbildet (Kennzahl, Rechenweg aus belegten
Punkten, Passung zum Original). Dazu: **wann endet ein Lauf dann?** Zwei Varianten mit Empfehlung.

### Aufgabe D — Antrieb ohne Mitspieler

Daniel: „In einem Mehrspieler-Spiel ist der Antrieb automatisch da: andere Spieler, mit denen man sich
messen kann. Ein Einzelspieler-Spiel muss diesen Antrieb selbst erzeugen." Dazu: „Es soll eine
Lobpreisung an das damalige Browsergame sein und all seiner damaligen Spieler — vielleicht eine kleine
Geschichte, eine Legende über das Spiel." Die Legende ist **ein mögliches Mittel, kein Ersatz**.

**Verlangt:** (1) höchstens sechs Punkte „was erzeugte im Original den Antrieb" mit Mechanik-Bezug
(Ruhmeshalle/Rangfolge, Punkte, Handel, Götterschutz, Diplomatie); (2) **fünf Antriebs-Quellen** für den
Einzelspieler, die auf **bestehenden** Mechaniken aufsetzen (keine neue Mechanik erfinden) — je mit
„wodurch entsteht der Vergleich/Maßstab ohne echte Mitspieler" (Bots als Messlatte, Ranglisten,
Bestwerte, Auszeichnungen) und Aufwand S/M/L; (3) ausdrücklich: **wo der Ersatz nicht trägt**
(höchstens drei Punkte); (3) ein **Legenden-Gerüst in höchstens 250 Wörtern**, ausschließlich aus belegten Originalbausteinen —
**Grundlage ist Material 6: die Original-Hintergrundgeschichte der Website (drei Teile, wörtlich).
Arbeite mit ihren Figuren und Ereignissen (die drei Drachenbrüder Epheus der Weiße, Tardas der Grüne,
Salmur der Rot, die Erschaffung des Nebelseetals, Salmurs Magiegeschenk, das Chaos, die
Landschaftswandlung durch die magischen Ströme) — erfinde keine neuen Götter und keine neue
Vorgeschichte. Trennung: „belegt verwendet" (Zitat/Paraphrase mit Quelle) und „neu erfunden"
(höchstens der Erzählrahmen für den Einzelspieler, klar markiert). Kein Pathos; (5) drei Sätze zu „Dimensionen als
Ländereien" (Anschluss an B); (6) **die eine Frage**, die Daniel zuerst beantworten muss.

---

## 7. Ausgabeformat (halte es genau ein)

1. **Kopf, 3 Sätze:** Was du geprüft hast, wo du Übereinstimmung siehst, was dein wichtigster
   Einwand ist.
2. **Befundtabelle, höchstens 15 Zeilen:**

   | Nr | Bereich | Befund | Beleg im Remake (Datei:Zeile) | Beleg in der Quelle (Dokument + Stelle) | Urteil | Empfehlung | Aufwand |
   |---|---|---|---|---|---|---|---|

   Urteile nur aus: **WIDERSPRUCH · FEHLT · ERFUNDEN · DOPPELT · UNBELEGT · IN ORDNUNG**.
   „ERFUNDEN" heißt: im Remake steht eine Regel oder Zahl, für die es in den Quellen keinen Beleg
   gibt und die nicht als VORSCHLAG gekennzeichnet ist. Höchstens zwei Zeilen „IN ORDNUNG".
3. **Die drei Aufgaben A, B, C** jeweils als eigener Abschnitt mit der verlangten Tabelle/Rechnung.
4. **Was du nicht prüfen konntest:** höchstens 5 Zeilen mit Grund.
5. **Die drei wichtigsten Maßnahmen**, je ein Satz, nach Wirkung sortiert.

Kein Vorwort, kein Lob, keine Zusammenfassung des Projekts, keine Code-Verbesserungsvorschläge
außerhalb der drei Aufgaben.

---

## 8. Was du NICHT tun sollst

* keine Zeilennummern, Seitenzahlen oder Werte erfinden — im Zweifel „nicht belegbar",
* keine Regel aus einem anderen Spiel oder aus Browsergame-Allgemeinwissen ergänzen,
* keine Punkte aus Abschnitt 5 erneut aufrollen,
* keine Dateien bewerten, die du nicht öffnen kannst (Abschnitt 3.2),
* keine Änderungen am Code verlangen, die eine Originalzahl ersetzen — erst Beleg, dann Vorschlag.

---

## 9. Was mit deiner Antwort passiert

Daniel liest sie selbst und gibt sie an die Sitzung zurück, die das Remake baut. Befunde mit
Datei:Zeile werden zu Prüfungen im Projekt (`tests/`), belegte Widersprüche zu Änderungen,
VORSCHLÄGE zu Entscheidungen, die Daniel trifft. Deine Antwort ist damit **Arbeitspapier, keine
Freigabe**: nichts wird gebaut, was nicht durch eine Quelle oder Daniels Entscheidung gedeckt ist.
""")

    text = "\n".join(teile)
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    with open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.makedirs(os.path.dirname(DESKTOP), exist_ok=True)
    shutil.copyfile(ZIEL, DESKTOP)
    print(f"Projekt: {ZIEL}  ({len(text)} Zeichen)")
    print(f"Desktop: {DESKTOP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
