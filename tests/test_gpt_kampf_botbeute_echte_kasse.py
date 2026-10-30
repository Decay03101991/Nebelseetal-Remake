"""GPT-KA03: echte Gegenbuchung bei Bot-Pluenderung (mit virtueller Anzeige)."""
from __future__ import annotations
import os,sys,tkinter as tk
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt,bericht,check,import_src
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
    bot=main.BotPlayer('Test-Gegner','Test',0.0,0.0,army={},vorraete={'holz':90,'stein':0},wall_stufe=0)
    anfang=float(app.state.resources['holz'].amount)
    erfolg=app._angriff_durchfuehren('Test-Gegner',{},vorrat_ziel=bot, vorraete={'holz':99999})
    delta=float(app.state.resources['holz'].amount)-anfang
    check('Angriff mit Truppen ausgefuehrt',erfolg is True)
    check('Beute aus tatsaechlichem Botlager, nicht aus gefaelschtem Aufrufwert',delta<=90)
    check('Zwei Handkarren maximal 80 Holz',0<=delta<=80)
    check('Beute exakt aus Botlager abgezogen',abs(delta+(float(bot.vorraete['holz'])-90))<1e-6,
          f'Spieler +{delta}, Bot {bot.vorraete["holz"]}')
    check('Botlager darf nicht negativ werden',bot.vorraete['holz']>=0)
    check('Krieger werden nicht grundlos vernichtet',app.state.units['Krieger'].count>=0)
    check('Kampfmeldung wurde geschrieben',app.state.messages[-1]['type']=='kampf')
finally:root.destroy()
sys.exit(bericht())
