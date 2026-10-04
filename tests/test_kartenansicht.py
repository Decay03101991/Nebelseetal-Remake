"""Pruefung der Siedlungskarte im Fenster (Tkinter), ohne Hauptschleife.

Geprueft wird das, was Daniel sehen wird: Ansicht oeffnen, Feld waehlen, Eignung lesen,
bauen (mit Kostenabzug), Sumpf gesperrt, abreissen, und die Schaltflaechen der Uebersicht.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import tkinter as tk
import gelaende as G
import main as M


def neuen_app():
    """Fenster aufbauen, aber nicht anzeigen (kein mainloop)."""
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    # Die Ladepage wartet auf after()-Rueckrufe; ohne mainloop feuern die nie.
    app._build_main_ui()
    return root, app


try:
    root, app = neuen_app()
except Exception as fehler:                     # kein Bildschirm vorhanden
    print(f"ACHTUNG: kein Fenster moeglich ({type(fehler).__name__}: {fehler}) —")
    print("diese Pruefung braucht einen angemeldeten Windows-Desktop.")
    sys.exit(1)


def sammle_knoepfe(widget):
    """Alle Schaltflaechen unterhalb eines Elements (rekursiv)."""
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Button):
            treffer.append(kind)
        treffer += sammle_knoepfe(kind)
    return treffer


def sammle_texte(widget):
    """Alle Beschriftungen unterhalb eines Elements (rekursiv)."""
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            treffer.append(str(kind.cget("text")))
        treffer += sammle_texte(kind)
    return treffer

abschnitt("Siedlungskarte im Fenster — Ansicht oeffnen")
siedlung = M.Settlement(name="Probesiedlung", map_id=app.state.current_map,
                        karte=G.siedlungskarte_erzeugen(31, typ_id="weideland"))
app.state.settlements.append(siedlung)

app._oeffne_siedlungskarte(siedlung)
check("Ansicht heisst 'Siedlungskarte'", app.current_view == "Siedlungskarte", app.current_view)
kinder = app.content.winfo_children()
check("die Ansicht hat Inhalte aufgebaut", len(kinder) > 3, f"{len(kinder)} Elemente")
check("die gewaehlte Siedlung ist gesetzt", app.karten_siedlung is siedlung)

# Das Raster muss 40 anklickbare Felder haben
rasters = [w for w in kinder if isinstance(w, tk.Frame)]
kacheln = []
for rahmen in rasters:
    kacheln += [w for w in rahmen.winfo_children() if isinstance(w, tk.Button)]
check("40 anklickbare Felder im Raster", len(kacheln) == 40, f"{len(kacheln)} Kacheln")
farben = {k.cget("bg") for k in kacheln}
check("die Kacheln tragen die Gelaendefarben", len(farben) >= 4, f"{len(farben)} Farben")

abschnitt("Siedlungskarte im Fenster — Feld waehlen und Eignung lesen")
raster = siedlung.karte["raster"]
wald = raster.index("wald")
app._karten_feld_waehlen(wald)
check("das gewaehlte Feld ist gemerkt", app.karten_feld == wald, str(app.karten_feld))
namen = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("auf Wald wird der Holzfäller angeboten",
      any("Holzfäller" in n for n in namen), str(namen[:6]))
check("und der Steinmetz NICHT (liefert auf Wald nichts)",
      not any("Steinmetz" in n for n in namen), str(namen[:6]))
check("die Kosten stehen an der Schaltfläche",
      any("Holz" in n and "Stein" in n for n in namen),
      str([n for n in namen if "Holzfäller" in n]))
check("auch die Ausbildungsstätten werden angeboten (kein Geländebezug)",
      any("Kriegerakademie" in n for n in namen), str([n for n in namen if "akademie" in n.lower()]))

abschnitt("Siedlungskarte im Fenster — Sumpf ist gesperrt")
sumpf = raster.index("sumpf")
app._karten_feld_waehlen(sumpf)
namen = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("auf Sumpf wird kein Bauvorschlag gemacht",
      not any("(" in n for n in namen), str(namen[:6]))
check("die Meldung nennt das Feld als Sumpf",
      any("Sumpf" in t for t in sammle_texte(app.content)), str(sammle_texte(app.content)[:6]))

abschnitt("Siedlungskarte im Fenster — Bauen kostet Rohstoffe und belegt das Feld")
app.state.resources["holz"].amount = 500
app.state.resources["stein"].amount = 500
vorher_holz = app.state.resources["holz"].amount
vorher_stein = app.state.resources["stein"].amount
vorher_siedler = app.state.population
kosten = M.baukosten("holzfaeller")
check("Holzfäller-Preis ist der belegte Originalpreis (10 Holz, 5 Stein, 1 Siedler)",
      kosten == {"holz": 10, "stein": 5, "siedler": 1}, str(kosten))
check("Haus kostet 80 Holz und 50 Stein und KEINEN Siedler (es beherbergt welche)",
      M.baukosten("haus") == {"holz": 80, "stein": 50}, str(M.baukosten("haus")))
check("der Siedler erscheint lesbar in der Kostenzeile",
      "Siedler" in M.kosten_text(kosten), M.kosten_text(kosten))

app._karten_feld_waehlen(wald)
app._karten_bauen("holzfaeller")
check("das Feld ist belegt", siedlung.bauten.get(str(wald)) == "holzfaeller", str(siedlung.bauten))
check(f"Holz wurde abgezogen ({kosten['holz']})",
      app.state.resources["holz"].amount == vorher_holz - kosten["holz"],
      f"{vorher_holz} -> {app.state.resources['holz'].amount}")
check(f"Stein wurde abgezogen ({kosten['stein']})",
      app.state.resources["stein"].amount == vorher_stein - kosten["stein"],
      f"{vorher_stein} -> {app.state.resources['stein'].amount}")
check("ein Siedler arbeitet jetzt im Gebäude (Bevölkerung sinkt)",
      app.state.population == vorher_siedler - 1,
      f"{vorher_siedler} -> {app.state.population}")
check("das Feld ist danach abgewählt", app.karten_feld is None)

abschnitt("Siedlungskarte im Fenster — zu wenig Rohstoffe wird gemeldet")
app.state.resources["holz"].amount = 1
app.state.resources["stein"].amount = 1
freies_waldfeld = [i for i, a in enumerate(raster) if a == "wald" and str(i) not in siedlung.bauten][0]
app._karten_feld_waehlen(freies_waldfeld)
app._karten_bauen("holzfaeller")
check("ohne Rohstoffe wird nicht gebaut", str(freies_waldfeld) not in siedlung.bauten,
      str(siedlung.bauten))
check("und der Grund steht im Spielprotokoll",
      any("Nicht genug Rohstoffe" in z for z in app.state.log[-3:]), str(app.state.log[-2:]))

abschnitt("Siedlungskarte im Fenster — abreissen (Handbuch S. 292)")
app._karten_feld_waehlen(wald)
app._karten_abreissen()
check("das Feld ist wieder frei", str(wald) not in siedlung.bauten, str(siedlung.bauten))
check("das Abreissen steht im Protokoll",
      any("abgerissen" in z for z in app.state.log[-3:]), str(app.state.log[-2:]))

abschnitt("Siedlungskarte im Fenster — Uebersicht zeigt den Weg zur Karte")
app._switch_view("Dorfzentrum")
uebersicht_texte = sammle_texte(app.content)
knopf_texte = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("die Siedlung nennt ihren Kartentyp",
      any("Weideland" in str(t) for t in uebersicht_texte), str(uebersicht_texte[:4]))
check("und hat eine Schaltfläche 'Karte öffnen'",
      any("Karte öffnen" == str(t) for t in knopf_texte), str(knopf_texte[:4]))

abschnitt("Auskunft im Spiel — der Reiter Chat")
app._switch_view("Chat")
check("die Ansicht heißt Chat", app.current_view == "Chat", app.current_view)
texte = sammle_texte(app.content)
check("die Begrüßung steht da", any("Auskunft" in t for t in texte),
      str(texte[:3]))
check("das Eingabefeld ist da", hasattr(app, "chat_eingabe")
      and app.chat_eingabe.winfo_exists())
knopf_texte = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("es gibt Vorschlagsfragen zum Antippen", any("Holzfäller" in t for t in knopf_texte),
      str(knopf_texte[:4]))

vorher = len(getattr(app, "chat_verlauf", []))
app._chat_fragen("Was macht der Holzfäller?")
check("die Frage und die Antwort landen im Verlauf", len(app.chat_verlauf) == vorher + 2,
      str(len(app.chat_verlauf)))
letzte_frage, letzte_antwort = app.chat_verlauf[-2], app.chat_verlauf[-1]
check("die Frage ist gespeichert", letzte_frage == ("du", "Was macht der Holzfäller?"),
      str(letzte_frage))
check("die Antwort nennt den Wald und 4 pro Stunde",
      "Wald" in letzte_antwort[1] and "4" in letzte_antwort[1], letzte_antwort[1][:120])
check("und wieder ist die Ansicht aufgebaut", len(app.content.winfo_children()) > 3)

app._chat_fragen("Wie wird das Wetter?")
check("unbekannte Frage wird ehrlich verneint", "Das weiß ich nicht" in app.chat_verlauf[-1][1],
      app.chat_verlauf[-1][1][:90])

app._chat_fragen("Paladin")
check("Einzelfrage nach einer Einheit funktioniert", "Paladin" in app.chat_verlauf[-1][1],
      app.chat_verlauf[-1][1][:80])

app._chat_fragen("")
check("eine leere Frage ändert nichts", len(app.chat_verlauf) == vorher + 6,
      str(len(app.chat_verlauf)))

abschnitt("Siedlungskarte im Fenster — Siedlung ohne Karte (alter Spielstand)")
alt = M.Settlement(name="Alte Siedlung", map_id=app.state.current_map)
app.state.settlements.append(alt)
app._oeffne_siedlungskarte(alt)
check("ohne Karte zeigt die Ansicht keinen Bauplan", app.karten_feld is None)
app._karten_zuwaeisen(alt)
check("der alten Siedlung wurde eine Karte zugewiesen",
      alt.karte is not None and bool(alt.karte["typ_name"]), str(alt.karte and alt.karte["typ_name"]))
check("und sie ist nicht dieselbe wie die der anderen Siedlung",
      M.karten_signatur(alt.karte) != M.karten_signatur(siedlung.karte))

root.destroy()
sys.exit(bericht())
