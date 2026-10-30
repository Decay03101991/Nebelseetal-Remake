# Testspielstaende fuer NEUEN Quellcode – kein fertiges Release

- `savegame_slot1.json`: frische regulaere Partie, 100 Holz/100 Stein/10 Siedler, Originalkarte Nr. 36 „Das Z“ mit 10×10 Feldern, kein Sieg, keine Gratisbauten. Entspricht Slot 1.
- `admin_teststand.json`: Admin-Testteil mit sechs unterschiedlichen Originalkarten im 10×10-Format, Ortslagern, Werkstaetten, Einheiten und Produktion. Nur mit Adminfreigabe ladbar. Normalerweise separat von Slot 1–3.
- Beide Dateien wurden durch `GameState.save()` erzeugt und `GameState.load()` getestet.
- **Nicht** in die alte EXE vom 06.10. laden. Erst Hermes' neue Windows-Buildversion fuer diese Quelldaten testen.
- Kein Passwort/Tor enthalten. Die im Chat hochgeladene `tor.json` gehoert NICHT in den Paketordner.
- Vor einem eventuellen Kopieren in `%USERPROFILE%\\.nebelseetal` eigene Dateien sichern; niemals unbesehen vorhandene Slots ueberschreiben.
