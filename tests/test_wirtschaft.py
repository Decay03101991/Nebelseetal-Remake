"""
Pruefung der Wirtschaft — stuendlicher Rohstoffertrag aus den Siedlungskarten.

Alle Sollwerte stammen aus dem Handbuch 2009 (data/buildings.json / data/resources.json),
nachgerechnet ueber echte Siedlungskarten aus gelaende.siedlungskarte_erzeugen.
"""
from __future__ import annotations

import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import gelaende as G
import wirtschaft as W


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def siedlung(karte=None, bauten=None):
    """Eine Siedlung wie im Spiel: Felder .karte und .bauten (beide duerfen fehlen/None sein)."""
    return types.SimpleNamespace(karte=karte, bauten=bauten)


def felder_von(karte, art):
    return [i for i, a in enumerate(karte["raster"]) if a == art]


def karte_mit(art, typen=("gemischt", "bergreich", "waldreich", "weideland", "nebelseeufer"),
              saaten=range(300)):
    """Sucht eine Karte, die die Gelaendeart enthaelt, samt erstem Feldindex."""
    for typ in typen:
        for s in saaten:
            k = G.siedlungskarte_erzeugen(s, typ_id=typ)
            i = felder_von(k, art)
            if i:
                return k, i[0]
    raise RuntimeError(f"kein Feld der Art '{art}' gefunden")


def roh(ertrag):
    """Ertrag ohne die Uebersprungenen-Liste."""
    return {k: v for k, v in ertrag.items() if k != W.UEBERSPRUNGEN}


# Feste Testkarten
KW = G.siedlungskarte_erzeugen(101, typ_id="waldreich")
wald = felder_von(KW, "wald")
berg = felder_von(KW, "berg")
gras = felder_von(KW, "grasland")
nebel = felder_von(KW, "nebelsee")

KH, huegel_feld = karte_mit("huegel")
KS, sumpf_feld = karte_mit("sumpf")


abschnitt("Holzfäller — Handbuch: Wald 4/h, Steppe 2/h")
e = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "holzfaeller"}))
check("ein Holzfäller auf einem Waldfeld = 4 Holz/Stunde", roh(e).get("Holz") == 4, str(roh(e)))
check("genau der Rohstoff Holz wird geführt", set(roh(e)) == {"Holz"}, str(roh(e)))
check("nichts wird übersprungen", W.uebersprungen_von(e) == [], str(W.uebersprungen_von(e)))

e2 = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "holzfaeller", str(wald[1]): "holzfaeller"}))
check("zwei Holzfäller auf zwei Waldfeldern = 8 Holz/Stunde", roh(e2).get("Holz") == 8, str(roh(e2)))
check("Ertragstext nennt 'Holz 8/h'", W.ertrag_text(e2) == "Holz 8/h", W.ertrag_text(e2))


abschnitt("Jäger — Handbuch: Wald 2 Nahrung + 2 Leder/h")
e = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "jaeger"}))
check("ein Jäger auf Wald = 2 Nahrung/Stunde", roh(e).get("Nahrung") == 2, str(roh(e)))
check("und zugleich 2 Leder/Stunde", roh(e).get("Leder") == 2, str(roh(e)))
check("sonst kein weiterer Rohstoff", set(roh(e)) == {"Nahrung", "Leder"}, str(roh(e)))
check("Ertragstext nennt beide Rohstoffe",
      "Nahrung 2/h" in W.ertrag_text(e) and "Leder 2/h" in W.ertrag_text(e), W.ertrag_text(e))


abschnitt("Tempel — Handbuch: Nebelsee 5/h, sonst 1/h")
e = W.siedlung_ertrag(siedlung(KW, {str(nebel[0]): "tempel"}))
check("Tempel auf Nebelsee = 5 Mana/Stunde", roh(e).get("Mana") == 5, str(roh(e)))
e = W.siedlung_ertrag(siedlung(KW, {str(gras[0]): "tempel"}))
check("Tempel auf Grasland = 1 Mana/Stunde", roh(e).get("Mana") == 1, str(roh(e)))
e = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "tempel"}))
check("Tempel auf Wald = 1 Mana/Stunde (Regel 'alle Gelände außer Sumpf')",
      roh(e).get("Mana") == 1, str(roh(e)))


abschnitt("Steinmetz — Handbuch: Berg 4/h, Hügel 2/h")
e = W.siedlung_ertrag(siedlung(KW, {str(berg[0]): "steinmetz"}))
check("Steinmetz auf Berg = 4 Stein/Stunde", roh(e).get("Stein") == 4, str(roh(e)))
e = W.siedlung_ertrag(siedlung(KH, {str(huegel_feld): "steinmetz"}))
check("Steinmetz auf Hügel = 2 Stein/Stunde", roh(e).get("Stein") == 2, str(roh(e)))


abschnitt("Sumpf trägt nichts bei")
e = W.siedlung_ertrag(siedlung(KS, {str(sumpf_feld): "holzfaeller"}))
check("Gebäude auf einem Sumpffeld liefert keinen Ertrag", roh(e) == {}, str(roh(e)))
check("die Überspringung wird begründet und nennt den Sumpf",
      any("Sumpf" in g for g in W.uebersprungen_von(e)), str(W.uebersprungen_von(e)))
check("und das Feld erhöht den Ertrag nicht", roh(e).get("Holz", 0) == 0, str(roh(e)))


abschnitt("Siedlung ohne Karte (alter Spielstand)")
e = W.siedlung_ertrag(siedlung(None, {"0": "holzfaeller"}))
check("ohne Karte gibt es keinen einzigen Rohstoff", roh(e) == {}, str(roh(e)))
check("und die Überspringung wird gemeldet (Karte)",
      any("Karte" in g for g in W.uebersprungen_von(e)), str(W.uebersprungen_von(e)))

e = W.siedlung_ertrag(siedlung(KW, None))
check("ohne gespeicherte Bauten ebenfalls kein Rohstoff und eine Begründung",
      roh(e) == {} and W.uebersprungen_von(e) != [], str(W.uebersprungen_von(e)))


abschnitt("Unbekanntes Gebäude und Feld ohne Ertrag")
e = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "zauberhuette"}))
check("ein unbekanntes Gebäude liefert nichts", roh(e) == {}, str(roh(e)))
check("und wird begründet übersprungen",
      any("unbekanntes" in g.lower() for g in W.uebersprungen_von(e)), str(W.uebersprungen_von(e)))

e = W.siedlung_ertrag(siedlung(KW, {str(berg[0]): "holzfaeller"}))
check("Holzfäller auf Berg liefert nichts (kein Ertrag dort)", roh(e) == {}, str(roh(e)))
check("und der Grund nennt das Gebäude bzw. Gelände",
      any("liefert" in g for g in W.uebersprungen_von(e)), str(W.uebersprungen_von(e)))


abschnitt("Mehrere Siedlungen addieren sich")
s1 = siedlung(KW, {str(wald[0]): "holzfaeller"})
s2 = siedlung(KW, {str(wald[1]): "holzfaeller"})
ges = W.ertrag_gesamt([s1, s2])
check("zwei Siedlungen mit je einem Holzfäller = 8 Holz/Stunde", ges.get("Holz") == 8, str(ges))

s2b = siedlung(KW, {str(wald[1]): "jaeger"})
ges = W.ertrag_gesamt([s1, s2b])
check("Holzfäller + Jäger ergeben Holz 4, Nahrung 2, Leder 2",
      ges == {"Holz": 4, "Nahrung": 2, "Leder": 2}, str(ges))

ges = W.ertrag_gesamt([])
check("ohne Siedlungen ist der Gesamtertrag leer", ges == {}, str(ges))


abschnitt("Forschungsfaktor (bonus_system)")
s = siedlung(KW, {str(wald[0]): "holzfaeller"})
check("ohne Forschung bleibt Holz bei 4/Stunde", W.ertrag_gesamt([s]).get("Holz") == 4,
      str(W.ertrag_gesamt([s])))
mit_forschung = W.ertrag_gesamt([s], {"Forstwirtschaft": 1})
ohne_forschung = W.ertrag_gesamt([s], None)
check("Forschung Forstwirtschaft 1 erhöht Holz von 4 auf 4.4", mit_forschung.get("Holz") == 4.4,
      str(mit_forschung))
check("der Forschungsfaktor erhöht die Rate wirklich", mit_forschung.get("Holz") > ohne_forschung.get("Holz"),
      f"{mit_forschung} gegen {ohne_forschung}")

sj = siedlung(KW, {str(wald[0]): "jaeger"})
kj = W.ertrag_gesamt([sj], {"Felderwirtschaft": 2})
check("Felderwirtschaft 2 erhöht Nahrung auf 2.4 (Handbuch: +10 % je Stufe)",
      kj.get("Nahrung") == 2.4, str(kj))
check("Leder bleibt ohne Forschungsfaktor bei 2", kj.get("Leder") == 2, str(kj))


abschnitt("ertrag_text — lesbare Fassung")
e = W.siedlung_ertrag(siedlung(KW, {str(wald[0]): "holzfaeller", str(wald[1]): "jaeger"}))
txt = W.ertrag_text(e)
check("die Reihenfolge folgt den Feldern und nennt alle drei Rohstoffe",
      txt == "Holz 4/h, Nahrung 2/h, Leder 2/h", txt)
check("eine leere Fassung ohne Rohstoffe ist ein leerer Text",
      W.ertrag_text({W.UEBERSPRUNGEN: ["x"]}) == "", W.ertrag_text({W.UEBERSPRUNGEN: ["x"]}))


abschnitt("Kapazität — theoretischer Höchstertrag der Karte")
kap = W.kapazitaet(siedlung(KW))
erw_holz = 4 * KW["zaehlung"]["wald"] + 2 * KW["zaehlung"]["steppe"]
check("Holz-Kapazität = 4*Waldfelder + 2*Steppefelder (Holzfäller)",
      kap.get("Holz") == erw_holz, f"{kap.get('Holz')} gegen {erw_holz}")
erw_stein = 4 * KW["zaehlung"]["berg"] + 2 * KW["zaehlung"]["huegel"]
check("Stein-Kapazität = 4*Berg + 2*Hügel (Steinmetz)",
      kap.get("Stein") == erw_stein, f"{kap.get('Stein')} gegen {erw_stein}")
erw_mana = 5 * KW["zaehlung"]["nebelsee"] + (
    KW["bauplaetze"] - KW["zaehlung"]["nebelsee"])
check("Mana-Kapazität = 5*Nebelsee + 1*alle übrigen bebaubaren Felder (Tempel)",
      kap.get("Mana") == erw_mana, f"{kap.get('Mana')} gegen {erw_mana}")

check("eine Karte ohne Karte hat keine Kapazität", W.kapazitaet(siedlung(None)) == {},
      str(W.kapazitaet(siedlung(None))))


def kap_summe(typ, rohstoff, n=15):
    return round(sum(W.kapazitaet(siedlung(G.siedlungskarte_erzeugen(s, typ_id=typ))).get(rohstoff, 0)
                     for s in range(n)), 2)


for typ_hoch, typ_niedrig, rohstoff in [("waldreich", "bergreich", "Holz"),
                                        ("bergreich", "waldreich", "Stein"),
                                        ("bergreich", "waldreich", "Metall")]:
    vh, vn = kap_summe(typ_hoch, rohstoff), kap_summe(typ_niedrig, rohstoff)
    check(f"{typ_hoch} hat mehr {rohstoff}-Kapazität als {typ_niedrig}",
          vh > vn, f"{vh} gegen {vn}")

check("die Waldkarte hat überhaupt Holz-Kapazität", kap_summe("waldreich", "Holz") > 0,
      str(kap_summe("waldreich", "Holz")))

sys.exit(bericht())
