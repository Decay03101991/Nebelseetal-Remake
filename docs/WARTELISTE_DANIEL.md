# Warteliste Daniel — was nur deine Hand kann

> Angelegt 05.11.2026 (Sitzung ab 03:34). Diese Liste wächst und wird am Ende **einmal**
> vorgelegt. Nichts davon blockiert die Arbeit am Spiel.

## 1. Gmail wieder verbinden (das Wichtigste, ca. 2 Minuten)

**Befund (gemessen, nicht vermutet):** Der Refresh-Token in
`C:\Users\saras\AppData\Local\hermes\google_token.json` ist **tot** — der Austausch gegen ein neues
Access-Token antwortet `HTTP 400 invalid_grant`. Kein `himalaya`, kein `gws`-CLI, die `EMAIL_*`-Zeilen
in `.env` sind auskommentiert. Damit ist kein Abruf und keine Ablage von Anhängen möglich.

**Was du tun musst:**
1. Cloud Console → *APIs & Services* → *OAuth consent screen* → Publishing-Status auf
   **In Produktion** (Branding ausfüllen). Ohne diesen Schritt hält jede Neu-Autorisierung nur
   ~7 Tage.
2. Danach einmal neu autorisieren — Link und Befehl liegen bereit, du musst nur die
   Rücksprung-Adresse (`http://localhost/?code=…`) zurückgeben. Die Seite selbst zeigt „nicht
   erreichbar" — das ist der Erfolgsfall.

**Was in der Zwischenzeit weiterläuft:** die ganze Spielarbeit. Sobald der Token lebt, hole ich die
1.250 Mails in „Allgemein" (552 ungelesen) nach, lege die Anhänge in die Akten (Biografie, Medizin,
Amt/Wohnen, Finanzen, Dokumentenübersicht) und trage offene Fristen zusammen.

## 2. Gmail-Fenster in Chrome

Ich habe Gmail zweimal in Chrome geöffnet, bevor du es gemeldet hast. Danach keine Tabs mehr, kein
Nachladen. Der Tab `Posteingang (552)` steht noch offen — ich lasse ihn, wie er ist.

## 3. WhatsApp-Kanal (für die To-do-Zusammenfassung)

Die App läuft nicht (`list_apps`: `WhatsApp … running: false`). Für Punkt 6 aus Block A
(offene To-dos aus den Mails in den Self-Chat) muss der Kanal erst verbunden werden. Ich habe
**nichts behauptet und nichts gesendet**.

## 4. Ein Entwurf liegt in Gmail

„Entwürfe 1" ist ungelesen markiert. Nicht angefasst — das ist deine Sache.

## 5. Entscheidungen, die dir gehören

Siehe `docs/FRAGEN_AN_DANIEL_20261105.md` — sieben Fragen, jede mit Messlage, Möglichkeiten und
Empfehlung zuerst. Sie werden am Ende der Sitzung in **einer** Runde vorgelegt.
