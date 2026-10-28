"""Pruefung der Siedlungskarte im Spiel: Zuweisung, Einzigartigkeit, Bauen, Speichern/Laden.

Belegte Regeln (Handbuch 2009, S. 259/283/313):
  * eine Siedlung zeigt eine Karte ihrer Gebaeude
  * beim Bauen wird die Eignung des Gelaendes angezeigt
  * 'Einer neuen Siedlung wird per Zufall eine Karte zugewiesen. Es werden niemals zwei
    Deiner Siedlungen die gleiche Karte bekommen.'
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import main as M
import gelaende as G

abschnitt("Siedlungskarte — Spielregeln aus dem Handbuch")
check("höchstens sechs Siedlungen (SIEDLUNGEN_MAXIMUM)", M.SIEDLUNGEN_MAXIMUM == 6,
      str(M.SIEDLUNGEN_MAXIMUM))
check("Settlement trägt ein Feld 'karte'", "karte" in M.Settlement.__dataclass_fields__)
check("Settlement trägt ein Feld 'bauten'", "bauten" in M.Settlement.__dataclass_fields__)
neu = M.Settlement(name="Probe", map_id="x")
check("eine Siedlung ohne Karte ist zulässig (alte Spielstände laden weiter)", neu.karte is None)

abschnitt("Siedlungskarte — keine zwei eigenen Siedlungen bekommen dieselbe Karte")
karten = []
for _ in range(30):
    karten.append(M.neue_siedlungskarte(karten))
signaturen = [M.karten_signatur(k) for k in karten]
check("30 nacheinander gegründete Siedlungen haben 30 verschiedene Karten",
      len(set(signaturen)) == 30, f"{len(set(signaturen))} verschiedene")
check("jede Karte erfüllt den Mindestbesatz (spielbar)",
      all(k["zaehlung"]["wald"] >= 2 and k["zaehlung"]["berg"] >= 2
          and k["zaehlung"]["grasland"] >= 3 and k["zaehlung"]["nebelsee"] >= 1 for k in karten))
check("jede Karte hat einen Kartentyp und einen Vorteil",
      all(k.get("typ_name") and k.get("vorteil") for k in karten))

abschnitt("Siedlungskarte — Bauen mit Eignungsprüfung (Handbuch S. 7/8)")
s = M.Settlement(name="Bauprobe", map_id="x", karte=G.siedlungskarte_erzeugen(7, typ_id="waldreich"))
raster = s.karte["raster"]
wald_feld = raster.index("wald")
sumpf_feld = raster.index("sumpf")
berg_feld = raster.index("berg")

ok, meldung = M.bauen_auf_karte(s, "holzfäller", wald_feld)
check("Holzfäller lässt sich auf ein Waldfeld setzen", ok is True, meldung)
check("und die Meldung nennt den Ertrag", "Holz" in meldung and "/Stunde" in meldung, meldung)
check("das Gebäude steht danach auf dem Feld", s.bauten.get(str(wald_feld)) == "holzfäller",
      str(s.bauten))

ok, meldung = M.bauen_auf_karte(s, "holzfäller", sumpf_feld)
check("auf Sumpf wird nicht gebaut", ok is False, meldung)
check("und die Meldung sagt, warum", "Sumpf" in meldung, meldung)
check("das Sumpffeld bleibt frei", str(sumpf_feld) not in s.bauten)

ok, meldung = M.bauen_auf_karte(s, "holzfäller", berg_feld)
check("Holzfäller wird auf Berg abgelehnt", ok is False, meldung)

ok, meldung = M.bauen_auf_karte(s, "holzfaeller", wald_feld)
check("ein belegtes Feld wird abgelehnt", ok is False, meldung)
check("die Meldung nennt das belegende Gebäude", "holzfäller" in meldung or "belegt" in meldung,
      meldung)

# Wichtig: ein FREIES Waldfeld nehmen, sonst schlägt die Prüfung wegen der Belegung an
# und nicht wegen des Geländes — der grüne Haken wäre dann wertlos.
freier_wald = [i for i, a in enumerate(raster) if a == "wald" and str(i) not in s.bauten][0]
ok, meldung = M.bauen_auf_karte(s, "steinmetz", freier_wald)
check("Steinmetz wird auf freiem Wald abgelehnt (liefert dort nichts)",
      ok is False and "liefert" in meldung, meldung)
check("und das Waldfeld bleibt danach frei", str(freier_wald) not in s.bauten)
ok, meldung = M.bauen_auf_karte(s, "steinmetz", -1)
check("ein Feld außerhalb der Karte wird abgelehnt", ok is False, meldung)
ok, meldung = M.bauen_auf_karte(s, "steinmetz", 9999)
check("auch ein zu großes Feld", ok is False, meldung)

ok, meldung = M.bauen_auf_karte(s, "schmiede", wald_feld)
check("Schmiede braucht kein bestimmtes Gelände", ok is False,   # Feld ist belegt
      meldung)
frei = [i for i, a in enumerate(raster) if a != "sumpf" and str(i) not in s.bauten][0]
ok, meldung = M.bauen_auf_karte(s, "schmiede", frei)
check("Schmiede lässt sich auf freiem Gelände setzen", ok is True, meldung)

ohne = M.Settlement(name="Ohne", map_id="x")
ok, meldung = M.bauen_auf_karte(ohne, "holzfäller", 0)
check("ohne Karte wird nicht gebaut", ok is False and "Karte" in meldung, meldung)

abschnitt("Siedlungskarte — Speichern und Laden")
zustand = M.GameState()
karte = G.siedlungskarte_erzeugen(4242, typ_id="nebelseeufer")
siedlung = M.Settlement(name="Speicherprobe", map_id=zustand.current_map, x=1, y=2, karte=karte)
zustand.settlements.append(siedlung)
feld = karte["raster"].index("nebelsee")
ok, meldung = M.bauen_auf_karte(siedlung, "tempel", feld)
check("Tempel auf Nebelsee gebaut", ok is True, meldung)

pfad = os.path.join(tempfile.gettempdir(), "nebel_spielstand_probe.json")
zustand.save(pfad)
check("Spielstand geschrieben", os.path.exists(pfad), pfad)

geladen = M.GameState()
geladen.load(pfad)
check("eine Siedlung geladen", len(geladen.settlements) == 1, str(len(geladen.settlements)))
g = geladen.settlements[0]
check("die Karte ist vollständig erhalten", g.karte is not None and g.karte["raster"] == karte["raster"])
check("der Kartentyp bleibt gleich", g.karte["typ_name"] == karte["typ_name"],
      f"{g.karte.get('typ_name')} gegen {karte['typ_name']}")
check("das Vorteilsprofil bleibt gleich", g.karte["profil"] == karte["profil"])
check("das Gebäude bleibt auf seinem Feld", g.bauten.get(str(feld)) == "tempel", str(g.bauten))

ok, meldung = M.bauen_auf_karte(g, "tempel", feld)
check("nach dem Laden ist das Feld weiterhin belegt", ok is False, meldung)
check("die Saat der Karte ist unverändert", g.karte["seed"] == 4242, str(g.karte["seed"]))

try:
    os.remove(pfad)
except OSError:
    pass

abschnitt("Siedlungskarte — Bot-Siedlungen bleiben unberührt")
check("BotPlayer speichert Siedlungen als Namen (keine Karten nötig)",
      all(isinstance(n, str) for n in M.BotPlayer("Test", "neutral", 0.5, 0.5).settlements))

sys.exit(bericht())
