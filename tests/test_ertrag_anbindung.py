"""
Anbindung der Kartenertraege an die Rohstoffproduktion (W4b-4, 04.10.2026).

Beweist, dass die Rohstoffe aus den BEBauten FELDERN der Siedlungskarten kommen — im Zeitlauf,
in der Anzeige und mit Forschungsfaktor — und dass KEIN Gebaeude mehr von sich aus Rohstoffe
erzeugt (sonst gaebe es denselben Rohstoff zweimal).

Sollwerte aus dem Originalhandbuch: Holzfaeller auf Wald 4 Holz/Stunde, auf Steppe 2 Holz/Stunde.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende as G
import main as M
import wirtschaft as W


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def karte_und_felder(art, anzahl=1,
                     typen=("waldreich", "gemischt", "bergreich", "weideland", "nebelseeufer"),
                     saaten=range(500)):
    """Eine Siedlungskarte mit mindestens ``anzahl`` Feldern der Geländeart — samt Feldindizes."""
    for typ in typen:
        for s in saaten:
            karte = G.siedlungskarte_erzeugen(s, typ_id=typ)
            felder = [i for i, a in enumerate(karte["raster"]) if a == art]
            if len(felder) >= anzahl:
                return karte, felder
    return None, []


def neue_siedlung(karte, name="Testsiedlung"):
    return M.Settlement(name=name, map_id="test", karte=karte, bauten={})


class _Forschungsstand:
    """Nur zum Setzen eines Forschungsstands — das Spiel liest bloss ``.level``."""
    def __init__(self, level):
        self.level = level


# --------------------------------------------------------------------------
# 1. Ohne Siedlungskarte wird nichts erzeugt
# --------------------------------------------------------------------------

abschnitt("Ohne bebaute Karte wird nichts erzeugt")

st = M.GameState()
check("ein frisches Spiel hat keine Siedlung", st.settlements == [], str(st.settlements))
check("der Stundenerertrag ist leer", st.stundenertrag() == {}, str(st.stundenertrag()))

vorher = st.resources["holz"].amount
st.tick(3600)
check("nach einer Stunde ist kein Holz dazugekommen",
      st.resources["holz"].amount == vorher,
      f"{vorher:.2f} -> {st.resources['holz'].amount:.2f}")
check("kein Gebaeude erzeugt mehr von sich aus Rohstoffe",
      all(not getattr(b, "production", {}) for b in st.buildings.values()),
      str({k: b.production for k, b in st.buildings.items() if b.production}))
check("die rohstofferzeugenden Gebaeude sind aus der Gebaeudeliste entfernt",
      not ({"holzfäller", "steinmetz", "jäger", "schmiede", "markt"} & set(M.BUILDINGS)),
      str(sorted(M.BUILDINGS)))


# --------------------------------------------------------------------------
# 2. Ein Holzfäller auf Wald liefert 4 Holz je Stunde
# --------------------------------------------------------------------------

abschnitt("Holzfäller auf Wald liefert 4 Holz je Stunde (Handbuch)")

karte, wald_felder = karte_und_felder("wald")
check("eine Waldkarte ist zu finden", karte is not None and bool(wald_felder))

siedlung = neue_siedlung(karte)
st.settlements.append(siedlung)
ok, meldung = M.bauen_auf_karte(siedlung, "holzfaeller", wald_felder[0])
check("der Holzfäller lässt sich auf dem Waldfeld bauen", ok, meldung)

ertrag = st.stundenertrag()
check("der Stundenerertrag nennt Holz", "holz" in ertrag, str(ertrag))
check("er beträgt genau 4 Holz je Stunde (Handbuchwert)", ertrag.get("holz") == 4.0, str(ertrag))

holz_vorher = st.resources["holz"].amount
st.tick(3600)
check("nach einer Stunde sind 4 Holz dazugekommen",
      round(st.resources["holz"].amount - holz_vorher, 2) == 4.0,
      f"{holz_vorher:.2f} -> {st.resources['holz'].amount:.2f}")
st.tick(1800)
check("nach einer weiteren halben Stunde 2 Holz mehr",
      round(st.resources["holz"].amount - holz_vorher, 2) == 6.0,
      f"{st.resources['holz'].amount:.2f}")
st.tick(60)
check("eine Minute bringt 4/60 = 0,07 Holz (auf zwei Stellen gerundet)",
      round(st.resources["holz"].amount - holz_vorher, 2) == 6.07,
      f"{st.resources['holz'].amount:.2f}")


# --------------------------------------------------------------------------
# 3. Zwei Felder erzeugen doppelt so viel
# --------------------------------------------------------------------------

abschnitt("Zwei bebaute Felder erzeugen doppelt so viel")

karte2, zwei_wald = karte_und_felder("wald", anzahl=2)
zwei = neue_siedlung(karte2, name="Zweisiedlung")
st2 = M.GameState()
st2.settlements.append(zwei)
M.bauen_auf_karte(zwei, "holzfaeller", zwei_wald[0])
M.bauen_auf_karte(zwei, "holzfaeller", zwei_wald[1])
check("zwei Holzfäller auf Wald ergeben 8 Holz je Stunde",
      st2.stundenertrag().get("holz") == 8.0, str(st2.stundenertrag()))

# Steppe liefert die Haelfte (Handbuch): 4 auf Wald, 2 auf Steppe
karte3, steppe_felder = karte_und_felder("steppe")
dritte = neue_siedlung(karte3, name="Steppensiedlung")
st3 = M.GameState()
st3.settlements.append(dritte)
M.bauen_auf_karte(dritte, "holzfaeller", steppe_felder[0])
check("ein Holzfäller auf Steppe liefert 2 Holz je Stunde",
      st3.stundenertrag().get("holz") == 2.0, str(st3.stundenertrag()))

# Zwei Siedlungen werden summiert
st3.settlements.append(neue_siedlung(karte2, name="Zweite Siedlung"))
M.bauen_auf_karte(st3.settlements[1], "holzfaeller", zwei_wald[0])
check("zwei Siedlungen werden summiert (2 + 4 = 6)",
      st3.stundenertrag().get("holz") == 6.0, str(st3.stundenertrag()))


# --------------------------------------------------------------------------
# 4. Forschung wirkt auf den Kartenertrag
# --------------------------------------------------------------------------

abschnitt("Forschung wirkt auf den Ertrag der Karte")

st.research["bergbau"] = _Forschungsstand(2)      # +10 % Holz je Stufe
erwartet = round(4.0 * 1.2, 2)
check(f"Bergbau Stufe 2 hebt Waldholz von 4 auf {erwartet} je Stunde",
      st.stundenertrag().get("holz") == erwartet, str(st.stundenertrag()))

laufend = st.resources["holz"].amount
st.tick(3600)
check(f"und der Zeitlauf liefert ebenfalls {erwartet} Holz",
      round(st.resources["holz"].amount - laufend, 2) == erwartet,
      f"{laufend:.2f} -> {st.resources['holz'].amount:.2f}")

st.research["bergbau"] = _Forschungsstand(0)
check("ohne Forschung sind es wieder 4 Holz je Stunde",
      st.stundenertrag().get("holz") == 4.0, str(st.stundenertrag()))


# --------------------------------------------------------------------------
# 5. Rechnung und Anzeige kommen aus derselben Quelle
# --------------------------------------------------------------------------

abschnitt("Rechnung und Anzeige haben EINE Quelle")

st.research["bergbau"] = _Forschungsstand(3)
stufen = {k: v.level for k, v in st.research.items()}
aus_modul = {k.lower(): v for k, v in W.ertrag_gesamt(st.settlements, stufen).items()}
check("der Spielstand liefert genau das, was das Wirtschaftsmodul rechnet",
      st.stundenertrag() == aus_modul, f"{st.stundenertrag()} gegen {aus_modul}")
check("das Wirtschaftsmodul ist im Spiel eingebunden", M.wirtschaft is W)

check("der Ertrag ist ein Wörterbuch aus Rohstoff zu Menge",
      isinstance(st.stundenertrag(), dict)
      and all(isinstance(k, str) and isinstance(v, (int, float))
              for k, v in st.stundenertrag().items()),
      str(st.stundenertrag()))

sys.exit(bericht())
