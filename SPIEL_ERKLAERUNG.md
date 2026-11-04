# Die offizielle Erklärung: was Nebelseetal Remake ist

**Nebelseetal Remake** ist ein Einzelspieler-Aufbaustrategiespiel für Windows. Es ist ein Remake des
historischen Browserspiels *Nebelseetal* und übernimmt dessen Welt, dessen Regeln und dessen Zahlen —
aber es läuft allein auf einem Rechner, ohne Anmeldung, ohne Server, ohne Internet.

## Für wen

Für Leute, die Aufbauspiele mit Tiefe mögen: Rohstoffe, Warenketten, Forschungen, Bauten, Kriege und
Diplomatie. Für Leute, die das alte Browserspiel kennen und es noch einmal spielen wollen. Und für
Leute, die neugierig sind, was ein einzelner Entwickler mit einem Agenten-System auf die Beine stellt.

## Was man tut

Man ist ein Herrscher. Man kommt mit zehn Siedlern, zwei Werkzeugkisten und einem Feld an und baut
daraus ein Reich.

| Schritt | Was man tut | Was es kostet |
|---|---|---|
| **Gründen** | eine Siedlung auf ein Feld setzen | Rohstoffe, Siedler |
| **Produzieren** | Holzfäller, Steinmetz, Farm, Mine auf passendes Gelände bauen | Baukosten, Bauzeit |
| **Verarbeiten** | Werkstätten und Warenketten: aus Rohstoffen werden 17 Waren | Rohstoffe, Ausrüstung |
| **Forschen** | Bibliothek bauen, dann 21 Forschungen von Baukunst bis Wagenbau | Zeit, Voraussetzungen |
| **Ausbilden** | Einheiten in der Kaserne, Waffen aus der Schmiede | Gold, Nahrung, Ausrüstung |
| **Bewegen** | Aufträge, Transporte, Handelsfahrten, Angriffe — mit Wegzeit | Gold, Nahrung, Mana |
| **Kämpfen** | Wall, Schlacht in Sequenzen, Beute, Kriegspunkte | Einheiten, Material |
| **Reisen** | Portale in andere Welten, Mana je Entfernung | Mana |

Dazwischen: fünf Nachbarn, die dasselbe tun — nur gegen dich.

## Was dieses Spiel besonders macht

**Es gibt keinen Sieg.** Das ist keine Lücke, sondern die Regel des Originals: Jeder Herrscher hat seine
eigenen Ziele, belohnt wird über Punkte. Das Remake führt das als **vier Auszeichnungen**: Feldherr
(Krieg), Forscher (Wissen), Händler (Handel), Gesamtherrscher (alles zusammen). Eine Niederlage gibt es
nur, wenn wirklich nichts mehr übrig ist.

**Die Zahlen sind belegt, nicht erfunden.** Baupreise, Einheitenwerte, Forschungskosten, Siedlergrenzen,
Götterschutz und Punkteformeln stammen aus der Originalanleitung und der Vorversion. Wo die Quellen
schweigen, steht der Wert als *Vorschlag* in den Datendateien — nicht als Regel getarnt.

**Alles Spielbare steht in Daten, nicht im Code.** Einheiten, Waren, Gebäude, Forschungen, Welten,
Fraktionen und alle Texte liegen als JSON in `data/`. Wer etwas ändern will, ändert eine Datei.

**Die Welt hat eine Geschichte.** Eine Chronik der Welt erzählt Schöpfung, Bruch und Gegenwart; ein
Intro, sieben Chronikkapitel und die Stimmen der Nachbarn tragen sie ins Spiel. Zu lesen in
[CHRONIK_DER_WELT.md](CHRONIK_DER_WELT.md) und als gestaltetes Buch in
[CHRONIK_DER_WELT.pdf](CHRONIK_DER_WELT.pdf).

## Was es nicht ist

- **Kein Browserspiel.** Kein Server, kein Konto, kein Netzwerk, keine anderen Menschen.
- **Kein fertiges Spiel.** Diese Fassung ist eine Vorabversion zum Testen.
- **Kein Nachbau der Originalgrafik.** Die Bilder stammen aus eigenen Lieferungen und eigenen
  Generierungen; die historische Oberfläche dient als Vorbild, nicht als Kopiervorlage.
- **Kein Free-to-play.** Nichts kostet Geld, nichts wird nachgeladen, es gibt keine Werbung.

## Technisch, in einem Satz

Python mit tkinter, portabel als einzelne `.exe`, Spielstände als JSON im Benutzerprofil, keine
Installation, kein Python auf dem Zielrechner nötig.
