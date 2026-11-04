# Wie dieses Spiel entstanden ist

Für Besucher, die wissen wollen, was hier eigentlich passiert — grob, ohne Entwicklerdetails.

## Das Original

Nebelseetal war ein deutsches Browserspiel: ein Aufbauspiel im Fantasy-Gewand, in dem man ein Reich
führte, Siedlungen gründete, forschte, handelte und gegen andere Herrscher Krieg führte. Die Welt lag
im „Limbus", einem magischen Raum aus 20 Dimensionen; Portale verbanden die Welten, und Reisen kostete
Mana — je weiter das Ziel, desto teurer. Rund um das Spiel lagen eine Anleitung, eine Vorversion mit
eigenen Regeln und eine kleine Gemeinde. Irgendwann wurde der Betrieb eingestellt.

## Warum ein Remake

Weil das Spielprinzip gut gealtert ist und weil es zu diesem Spiel keine spielbare Fassung mehr gibt.
Ein Browserspiel braucht einen Server; ein Einzelspieler-Remake braucht nur einen Rechner. Also:
dieselben Ideen — Siedler, Rohstoffe, Waren, Forschungen, Kriege, Portale — aber lokal, offline und
ohne Anmeldung.

Wichtig dabei: **Die Originalregeln sind die Richtschnur.** Wo die Quellen — die Anleitung von 2009 und
die Vorversion von 2006 — Zahlen nennen, gelten diese Zahlen. Wo sie schweigen, wird nichts erfunden,
sondern als Vorschlag gekennzeichnet und nachgefragt. Wo beide Fassungen voneinander abweichen, steht
das angeschrieben, statt stillschweigend angeglichen zu werden.

## Wie gearbeitet wird

Der Entwickler, **Daniel Kössl**, hat sich dafür ein Agenten-System gebaut: einen Hermes-Agenten mit
Coding-Subagenten. Der Agent heißt **Weltenfresser**. Er schreibt Code, legt Prüfungen an, rechnet
Zahlen nach, führt Prüfläufe aus und dokumentiert jeden Schritt; die Entscheidungen über Inhalt, Ton,
Regeln und Gestaltung trifft der Entwickler.

Über weite Strecken arbeitet dabei ein schnelles, günstiges Modell (`deepseek-v4-flash`). Für Entwürfe,
die wirklich nachdenken müssen — Regelsysteme, Konzepte, die Geschichte der Welt — werden einzelne,
kontrollierte Aufträge an ein großes Modell gegeben. Dazu kommen einzelne Bilddeutungen und
Textarbeiten aus anderen Modellen. Die Zuordnung, welche KI was gemacht hat, steht im
[README](README.md#herkunft-und-transparenz).

## Was in den ersten Wochen entstanden ist

Die Entwicklung begann im September 2026 und lief in Etappen:

1. **Das Gerüst.** Karte, Siedlungen, Rohstoffproduktion, Spielstand, Speichern und Laden.
2. **Die Wirtschaft.** Gebäude mit Preisen und Wirkungen, Waren aus Rohstoffen, Forschungen mit
   Voraussetzungen, Werkstätten, Handelsaufträge.
3. **Der Kampf.** Einheiten mit Werten, Wälle, Schlachten in Sequenzen, Beute, Punkte.
4. **Die Nachbarn.** Fünf Bots, die eine eigene Wirtschaft führen, forschen, bauen, gründen, rauben —
   und ihre Taktik je nach Lage wechseln.
5. **Die Welt.** Sechs belegte Welten im Limbus, Portale mit Manakosten, Reisen mit Wegzeit, 127
   historische Siedlungskarten als Gelände.
6. **Die Oberfläche.** Vom ersten Fenster über Icons und Rahmen bis zu Menüs im Stil der alten Vorlage.
7. **Die Geschichte.** Ein Intro, eine Chronik, die mit dem Fortschritt wächst, sprechende Nachbarn —
   und eine Chronik der Welt, die man als Buch lesen kann.

Was das im Einzelnen beweist, prüfen **164 Prüfdateien mit rund 6.700 Einzelprüfungen**. Jede neue
Regel bekommt eine Prüfung; jede Prüfung wird gegengeprüft, indem die Regel absichtlich abgeschaltet
wird — fällt dann nichts aus, prüft sie nichts. Dieses Vorgehen ist der Grund, warum das Spiel in
diesem Tempo überhaupt wachsen kann.

## Wer dahinter steht

Daniel Kössl ist angehender Fachinformatiker für Systemintegration — und, wenn man ihn beim Arbeiten
erlebt, ein **anstrengender, aber kluger Jungentwickler**. Anstrengend im besten Sinn: Er gibt sich mit
einem „läuft doch" nicht zufrieden, fragt bei Zahlen nach, statt sie zu glauben, und lässt sich Fehler
lieber zeigen als wegdiskutieren. Klug darin, wie er ein großes Vorhaben zerlegt: in prüfbare Schritte,
mit klaren Grenzen, und mit der Geduld, einen Schritt lieber zweimal zu prüfen als einmal zu raten.
Wenn eine Regel keinen Beleg hat, bleibt sie ein Vorschlag — dieser Satz stammt von ihm, und das ganze
System hält sich daran.

Dass ein einzelner Mensch mit einem Agenten-System ein Spiel dieser Größe baut, liegt genau daran:
nicht an einem Trick, sondern an Disziplin im Kleinen — jede Entscheidung aufgeschrieben, jede Änderung
nachvollziehbar, jeder Zweifel festgehalten.

## Sicherheit und Kontrolle zuerst

Auf Daniels Vorgabe steht Sicherheit im ganzen System an erster Stelle — und das Entwicklungssystem ist
keine Ausnahme. Die Agenten arbeiten **hierarchisch nach Regeln und Skills**: eine übergeordnete
Arbeitsregel schlägt jede Fachanweisung, eine Sicherheitsgrenze schlägt alles. Die Rechte sind geteilt —
es gibt Rollen, die **nur lesen** dürfen, und Rollen, die **schreiben** dürfen; was eine Rolle nicht
darf, kann sie auch nicht versehentlich tun. Jede Änderung an einer Regel oder einem Skill wird
protokolliert, mit Grund, Freigabe und Rückrollweg.

Das ist der Grund, warum dieses Projekt in dieser Größe überhaupt verantwortbar ist: nicht weil ein
Agent viel kann, sondern weil klar ist, was er nicht darf.

## Was als Nächstes kommt

- Die Welt auf **sechs Welten** umstellen (bisher liegen noch 20 Limbus-Dimensionen im Code).
- Drei offene **Kampfregeln** ergänzen: Flucht, Beutereihenfolge, Mauerreparatur mit Bauzeit.
- Die **Oberfläche flüssiger** machen: Ansichten sollen sich aktualisieren, statt neu zu bauen.
- **Ton und Musik**, die heute noch fehlen.

Diese Vorabversion ist der erste öffentliche Stand. Wer mitspielt und Fehler meldet, hilft genau dabei.
