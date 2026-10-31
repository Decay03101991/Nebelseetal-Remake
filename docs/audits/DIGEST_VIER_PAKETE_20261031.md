# Digest der vier großen Modell-Antworten — 31.10.2026

**Wozu:** Eine Seite statt vier Dateien. Was `deepseek-v4-pro` je Paket gesagt hat, was davon schon
gebaut ist, und was nur eine Entscheidung von Daniel braucht. Die Volltexte liegen daneben:
`BEFUND_A2_WEGZEIT`, `BEFUND_A1_KAMPFMODELL`, `BEFUND_A3_SPIELBARKEIT`, `BEFUND_A4_EINZELSPIELER`
(alle `_20261031.md`).

**Kosten, gemessen:** 0,0362 + 0,0539 + 0,0569 + 0,0325 = **0,1795 USD** für alle vier.

---

## A2 — Wegzeit, Kosten, Portal

| | |
|---|---|
| **Kernaussage** | Faktor 2 (`Dauer = 2·d/GS`) ist bei ×180 richtig: 32 Felder mit GS 5 → 256 s je Strecke, 512 s hin und zurück. „Das gibt dem Verteidiger ausreichend Vorwarnzeit und ist für den Einzelspieler erträglich." |
| **Kosten** | Gold 0,1 je Feld und GS-Punkt · Nahrung 0,1 je Feld geteilt durch GS · Mana 5 + 0,5 je Feld + 20 je Dimensionsstufe (nur fremdes Ziel). **Alle Höhen sind VORSCHLAG** — die Quellen nennen nur die Richtung. |
| **Drosselung** | 10 % langsamer → Dauer +11,1 %, Gold −10 %, Nahrung +11,1 % (nachgerechnet, stimmt) |
| **Dimensionen** | 20 als Kulisse behalten, **5–7 aktiv**, Rest „versiegelt"; Portal = Tor zwischen Ländereien, Handel und Kopfgeld laufen darüber |
| **Schon gebaut** | Reisekosten-Funktion + Buchung (`auftraege.kosten_der_mission`) |
| **Offen** | Dimensionen als Ländereien (Datenmodell `data/welten.json`) — Frage 7 |

## A1 — Kampfmodell und Beute

| | |
|---|---|
| **Kernaussage** | Der Wall entscheidet über den Angriff, nicht über die Beute. Zitate: „der Mauerzustand ist im Original kein Faktor für die Beute"; belegt ist **100 % des Ortslagers, begrenzt durch die Karrenladung** |
| **Widersprüche** | Fünf: Fernkampf (Handbuch „in jeder Sequenz" gegen Forum „nur Vorrunden"), Zweikampf (LE/AT/PA gegen Kampfwert-Wurf), Erschöpfung, Flucht, „Fußtruppen" gegen „Nahkampfeinheiten" |
| **Empfehlung** | Forum-Kampf + ältere Nebenregeln (Beute, Geräteverlust, Punkte), saubere Trennung dokumentieren |
| **Prüfung durch uns** | Die Staffel (10/30/60/100) **widerspricht** dem Original — bleibt aber als Daniels E4 bewusst drin und ist **wirksam**: gemessen 1 von 10 Verteidigern übrig → 10 % = 240 statt 400 |
| **Schon gebaut** | Beute einheitlich + Abbuchung beim Ziel (`beute_am_ziel`), Doku der erfundenen Kampfwerte (`kampf.vorschlaege`) |
| **Offen** | Frage 4 (Staffel behalten?) |

## A3 — Spielbarkeit bei ×180 und Bewertung statt Sieg

| | |
|---|---|
| **Kernaussage** | Produktion und Forschung sind bei ×180 spielbar, hohe Forschungsstufen „zäh"; Ausbildungszeiten sind **nicht belegbar** |
| **Auszeichnungen** | Feldherr (Kriegspunkte) · Forscher (Forschungspunkte) · Händler (Handelspunkte, **nur 2006 belegt**) · Gesamtherrscher (Gesamtpunkte) |
| **Laufende** | Empfehlung: Zeitlimit 120 Echtminuten = 15 Spieltage, danach Bewertung, danach freiwillig weiter |
| **Stellschrauben** | Zeitfaktor (180 lassen), Startbedingungen (5×5-Karte mit Bibliotheksplatz), Kartengröße (1 Dimension, 6 Welten) |
| **Schon gebaut** | `punkte.auszeichnungen` + `punkte.handelspunkte` (21 Prüfungen), Bot-Punkte aus der Originalformel |
| **Offen** | Fragen 5 und 6 (Sandbox/Kampagne, Zeitlimit) |

## A4 — Antrieb ohne Mitspieler und die Legende

| | |
|---|---|
| **Kernaussage** | Sechs Antriebsquellen im Original (Ruhmeshalle, Punkte, Handel, Götterschutz, Diplomatie, Gildenhalle); ohne Menschen tragen davon fünf als Ersatz, **ehrlich benannt**: Bots ersetzen keine Aushandlung, keine Dynamik, keine Bindung |
| **Fünf Ersatzantriebe** | Bot-Ruhmeshalle · persönliche Bestwerte · Handel mit Bot-Händlern · Götterschutz-Meilensteine · Bot-Gilden |
| **Legende** | Epheus, Tardas, Salmur → Nebelseetal, Magiegeschenk, Zersplitterung in 20 Dimensionen, Nebelsee aus Epheus' Tränen. **Belegt** aus der Original-Geschichte; nur die Verbindung „Götter gewähren Schutz, Ruhmeshalle als ewiges Verzeichnis" ist neu erfunden und so gekennzeichnet |
| **Die eine Frage** | Endloses Highscore-Spiel oder Kampagne mit festem Ziel? |
| **Schon gebaut** | nichts aus A4 (reine Gestaltung) |
| **Offen** | Frage 5 und die Legende als Textbaustein (kann jederzeit ins Spiel, der Text steht) |

---

## Wo sich die beiden großen Modelle widersprechen (und wer recht hat)

| Streitpunkt | GPT (extern) | DeepSeek (A1/A2) | Unsere Prüfung |
|---|---|---|---|
| Reiseformel | schlägt `4·d/GS` vor | bestätigt **Faktor 2** mit Rechnung | Faktor 2 bleibt (GPT kannte unsere Entscheidung nicht — der Prompt war blind) |
| Beute | Staffel ist „bewusster Widerspruch zum Original" | Original = 100 % bei Sieg | beide haben recht: Original sagt 100 %, E4 ist Hausregel — bleibt, klar gekennzeichnet |
| Kampfwerte | Spannen „UNBELEGT" | Spannen sind die jüngere Tabelle | Registerpunkt 40 gilt: jüngere Tabelle gewinnt |
| Wallprüfung | **AT statt SK = Fehler** | — | GPT hatte recht, **war noch im Code** → behoben (`_schlagkraft_fussttruppen`) |
| Spionage | fehlt | — | fehlt tatsächlich → Frage 1 |

## Querschnitt: drei Fehler, die nur durch Nachrechnen sichtbar wurden

1. **Wallprüfung rechnete mit AT** (Kämpfer 40 statt 2) — die Vorprüfung bestand fast immer.
2. **Beute wurde gutgeschrieben, aber beim Ziel nicht abgezogen** — Güter aus dem Nichts.
3. **Beute-Verteilung frass den ersten Rohstoff** (Holz 80 / Stein 0 statt 50 / 30), weil gegen die
   ideale statt gegen die mitnehmbare Menge gerechnet wurde.

Alle drei sind behoben und mit Prüfdatei belegt (`test_auftraege` 129/0/1, `test_beute_am_ziel`
24/0/0, `test_kampf_einhaengung` 42/0/0).
