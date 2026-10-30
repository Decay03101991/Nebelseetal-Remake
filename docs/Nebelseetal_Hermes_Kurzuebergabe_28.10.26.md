# Hermes — KURZKONTEXT (nur diese Datei zuerst lesen)

**Rolle:** Externer GPT-6-Zuarbeitsagent von Daniel; **Hermes bleibt alleiniger Hauptkoordinator**. Ich habe ausschließlich eine isolierte ZIP-Kopie bearbeitet, **keine führende Datei**, keinen Commit, keinen Skill und keine Roadmap geändert. Dieses Paket enthält neue Tests/Diagnose und externe Protokolle; **Integration ausschließlich durch Hermes**.

**Basis:** gelieferter Source-Stand `1c4dffa3cf1c47c9c4963e9782b34272fcca29d1` (06.10.2026), ältere EXE SHA256 `c1523670aa307077fd8be3c0858d52a44a1a20a40c024f1d2275658c4276ac75`. Quellcode ruft `tick_bis` bereits auf (Schritt 10/Teil 2); altes `KONTEXT_PAKET.md` nicht blind als neuesten Schritt ausführen. In **deiner** Roadmap weiterarbeiten.

**Daniel legt fest:** Exakte Original-Handbuchwerte für Gebäudestundenraten je Gelände, 28 Einheiten mit Werten/Kosten/Voraussetzungen, 17 Waren und Forschung. **8×7 Felder = 56, davon 40 baubar** ist Daniels zusätzliche Remake-Entscheidung, nicht Handbuchwert. Echte örtliche Lager, sinnvolle Waren- und Truppenketten, Karrentransporte, Kämpfe; keine kostenlosen Transfers und keine Wirtschafts-Sackgassen. Keine erfundenen Produktionswerte; fehlende Baupreise/Zeitwerte bleiben als Vorschlag markiert.

**Bestätigt, Fixplan in `04_DETAIL/FEHLERREGISTER_UND_FIXWEGE.md`:** F01 doppelte Reichs-/Ortskasse (auch Siedler), F02 fremde Ortlager indirekt ohne Karren bezahlen, F03 Farm ohne Baukunst baubar, F04 Mehrtages-Tick zählt nur einen Tag. F01/F02 haben gemeinsame Ursache, **nicht zwei unabhängig zu patchende Module**. F05 alter EXE-Build ist ein Freigabe-/Abnahmethema. Weitere Risiken/Balancing ausdrücklich von belegten Bugs getrennt.

**Geliefert:** Fünf neue Tests + reine Versorgungsdiagnose in `01_TESTS/`, Einzelprotokolle `02_PROTOKOLLE/`, Testlogs `03_BELEGE/`, Fixwege, Modellaufträge und Skill-Vorschläge `04_DETAIL/`, zuvor erstelltes GPT-001-Paket `05_VORARBEIT_001/`. Keine bestehende Spielquelldatei ersetzt.

**Aktuelle neue Prüfergebnisse:** Originaltreue **77/0/0**, Waren/Einheiten **171/0/0**, Diagnose **15/0/0**, Integrationsrisiken **4/0/3 Befunde**, Doppelbuchung **4/0/5 Befunde**. GPT-001 Tageswechsel **13/0/8 Befunde**. Die Befunde werden mit `--strict` erwartungsgemäß rot. **Nicht** als grünen Gesamttest interpretieren. Frühere 21 Basistests: 18 Exit 0, 3 umgebungsbedingt nicht vollständig; Windows-Sammellauf/EXE nicht abgenommen.

**Deine nächste Handlung:** Den eigenen Schritt prüfen; Details nur nach Bedarf lesen. Neue Tests isoliert einführen, Fehler nach deines Plans Priorität beheben, strict grün, den Windows-Gesamtlauf+Save/Load+EXE-Start prüfen, dann erst deine Protokollzeile und Commit. DeepSeek Flash für *eine Funktion plus Test*, tiefe Gutachten/Astra nur nach DEINEN Skill-/Budgetregeln und mit kurzem Belegkontext.

**Externer Abschluss:** Ich bin nicht Hermes, habe keine Integrationsentscheidung getroffen und keine laufende Sitzung auf deinem Rechner gesteuert. Übernommene Änderungen sind erst nach deiner unabhängigen Prüfung Projektbestandteil.
