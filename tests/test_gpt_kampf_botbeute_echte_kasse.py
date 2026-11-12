"""GPT-KA03: echte Gegenbuchung bei Bot-Pluenderung (mit virtueller Anzeige)."""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['kampf', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import os,sys,tkinter as tk
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt,angriff_mit_marsch,bericht,check,import_src
import_src()
import main

abschnitt('Bot-Lager gegen Spieler-Gutschrift: keine Rohstoffe aus dem Nichts')
root = tk.Tk();root.withdraw()
try:
    app=main.NebelseetalApp(root)
    app._build_main_ui()
    for u in app.state.units.values(): u.count=0
    app.state.units['Krieger'].count=100
    app.state.units['Handkarren'].count=2
    bot=main.BotPlayer('Test-Gegner','Test',0.0,0.0,wall_stufe=0)   # S-5b: kein army-Feld mehr
    # B-3 (02.11.2026): die Kasse eines Bots liegt in seinen DOERFERN; `bot.vorraete` ist die
    # Summe (Eigenschaft). Gesetzt wird sie hier ueber dieselbe Eigenschaft - kein Sonderweg.
    bot.vorraete={'holz':90,'stein':0}
    # ENTSCHEIDUNG 1 (01.11.2026): der Kampf faellt erst am Ziel an, und dort wird der Bot
    # ueber seinen Namen in state.bots gesucht. Ein nicht eingetragener Bot haette ein
    # Kopielager - die Beute kaeme aus dem Nichts. Deshalb steht er hier wie im Spiel drin.
    app.state.bots.append(bot)
    anfang=float(app.state.resources['holz'].amount)
    erfolg=angriff_mit_marsch(app,'Test-Gegner',{},vorrat_ziel=bot, vorraete={'holz':99999})
    delta=float(app.state.resources['holz'].amount)-anfang
    check('Angriff mit Truppen ausgefuehrt',erfolg is True)
    check('Beute aus tatsaechlichem Botlager, nicht aus gefaelschtem Aufrufwert',delta<=90)
    check('Zwei Handkarren maximal 80 Holz',0<=delta<=80)
    check('Beute exakt aus Botlager abgezogen',abs(delta+(float(bot.vorraete['holz'])-90))<1e-6,
          f'Spieler +{delta}, Bot {bot.vorraete["holz"]}')
    check('Botlager darf nicht negativ werden',bot.vorraete['holz']>=0)
    check('Krieger werden nicht grundlos vernichtet',app.state.units['Krieger'].count>=0)
    check('Kampfmeldung wurde geschrieben',any(m.get('type')=='kampf' for m in app.state.messages))
finally:root.destroy()
sys.exit(bericht())
