"""Pruefung des Gelaendes und der Siedlungskarte gegen das Handbuch (S. 7-11)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import gelaende as G

abschnitt("Gelände — Bestand nach Handbuch Seite 9-11")
check("sieben Geländearten", len(G.GELAENDEARTEN) == 7, str(G.GELAENDEARTEN))
check("Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf sind dabei",
      set(G.GELAENDEARTEN) == {"grasland", "steppe", "wald", "huegel", "berg", "nebelsee", "sumpf"},
      str(G.GELAENDEARTEN))
check("Sumpf ist nicht bebaubar (Handbuch S. 11)", G.ist_bebaubar("sumpf") is False)
check("die übrigen sechs sind bebaubar",
      all(G.ist_bebaubar(a) for a in G.GELAENDEARTEN if a != "sumpf"))

abschnitt("Gelände — Erträge stimmen mit den Originalzahlen (buildings.json)")
faelle = [
    ("holzfaeller", "wald", 4), ("holzfaeller", "steppe", 2),
    ("steinmetz", "berg", 4), ("steinmetz", "huegel", 2),
    ("erzmine", "berg", 3), ("erzmine", "huegel", 1.5),
    ("goldmine", "berg", 3), ("goldmine", "huegel", 1.5),
    ("farm", "grasland", 4), ("farm", "steppe", 2),
    ("schafszucht", "grasland", 3), ("rinderfarm", "grasland", 3), ("pferdezucht", "grasland", 3),
    ("tempel", "nebelsee", 5),
]
for geb, art, soll in faelle:
    ist = G.ertrag_pro_stunde(geb, art)
    check(f"{geb} auf {art} = {soll}", ist == soll, f"gefunden {ist}")

check("Jäger auf Wald liefert Nahrung 2 und Leder 2",
      G.ertrag_pro_stunde("jaeger", "wald") == {"Nahrung": 2, "Leder": 2},
      str(G.ertrag_pro_stunde("jaeger", "wald")))
check("Jäger auf Steppe liefert Nahrung 1 und Leder 1",
      G.ertrag_pro_stunde("jaeger", "steppe") == {"Nahrung": 1, "Leder": 1})
check("Tempel auf Grasland liefert 1 (Regel 'alle Gelände außer Sumpf')",
      G.ertrag_pro_stunde("tempel", "grasland") == 1,
      str(G.ertrag_pro_stunde("tempel", "grasland")))
check("Tempel liefert auf Sumpf nichts",
      G.ertrag_pro_stunde("tempel", "sumpf") is None)
check("Holzfäller liefert auf Berg nichts",
      G.ertrag_pro_stunde("holzfaeller", "berg") is None)
check("Anzeigename funktioniert wie die Kennung",
      G.ertrag_pro_stunde("holzfaeller", "Wald") == 4)

abschnitt("Gelände — Bauregeln")
ja, warum = G.bau_moeglich("holzfaeller", "wald")
check("Holzfäller darf auf Wald", ja is True, warum)
check("und die Begründung nennt den Ertrag", "4" in warum and "Holz" in warum, warum)

nein, warum = G.bau_moeglich("holzfaeller", "berg")
check("Holzfäller darf NICHT auf Berg", nein is False, warum)
check("Begründung sagt warum", "liefert" in warum, warum)

sumpf_verbote = []
for geb in ("holzfaeller", "steinmetz", "farm", "tempel", "schmiede", "haus", "lager", "bibliothek",
            "jaeger", "goldmine", "kriegerakademie", "diebesgilde", "stellmacher", "bogenbauer"):
    ok, txt = G.bau_moeglich(geb, "sumpf")
    if ok:
        sumpf_verbote.append(geb)
check("kein Gebäude darf auf Sumpf stehen", not sumpf_verbote, ", ".join(sumpf_verbote))

ok, txt = G.bau_moeglich("schmiede", "wald")
check("Schmiede hat einen Geländebezug (Grasland, Steppe, Hügel, Berg)",
      ok is False and "Grasland" in txt, txt)
ok, txt = G.bau_moeglich("schmiede", "huegel")
check("auf dem Hügel steht sie", ok is True, txt)
ok, txt = G.bau_moeglich("haus", "berg")
check("Haus hat einen Geländebezug (nicht auf Fels)", ok is False and "Grasland" in txt, txt)
ok, txt = G.bau_moeglich("haus", "nebelsee")
check("und nicht im Nebelsee (Vorgabe Daniel 05.10.2026)", ok is False, txt)
ok, txt = G.bau_moeglich("haus", "grasland")
check("auf Grasland steht es", ok is True, txt)
# Vorgabe Daniel 05.10.2026: „intelligent angewendet auf ALLE Gebäude" — jedes Gebäude muss
# auf JEDEM Gelände eine klare Antwort geben, und der Nebelsee ist nur Bibliothek und Tempel.
ohne_antwort = [g for g in G.alle_gebaeude()
                if not isinstance(G.bau_moeglich(g, "grasland")[1], str)
                or G.bau_moeglich(g, "grasland")[1].strip() == ""]
check("jedes Gebäude gibt auf jedem Gelände eine Begründung", not ohne_antwort,
      ", ".join(ohne_antwort))
nebelsee_erlaubt = [g for g in G.alle_gebaeude() if G.bau_moeglich(g, "nebelsee")[0]]
check("im Nebelsee dürfen nur Bibliothek und Tempel stehen",
      sorted(nebelsee_erlaubt) == ["bibliothek", "tempel"], ", ".join(sorted(nebelsee_erlaubt)))

nein, warum = G.bau_moeglich("gibtsnicht", "wald")
check("unbekanntes Gebäude wird abgelehnt", nein is False, warum)

abschnitt("Siedlungskarte — Aufbau (8x7 = 56 Felder, davon 40 bebaubar)")
k = G.siedlungskarte_erzeugen(20261004)
check("8 Spalten", k["spalten"] == 8, str(k["spalten"]))
check("7 Zeilen", k["zeilen"] == 7, str(k["zeilen"]))
check("das Raster hat 56 Felder", k["felder"] == 56 and len(k["raster"]) == 56,
      f"felder {k.get('felder')}, raster {len(k['raster'])}")
check("40 Bauplätze (nur die bebaubaren Felder)", k["bauplaetze"] == 40, str(k["bauplaetze"]))
check("genau 16 Felder sind nicht bebaubar",
      sum(1 for a in k["raster"] if not G.ist_bebaubar(a)) == 16,
      str(len([a for a in k["raster"] if not G.ist_bebaubar(a)])) +
      " Felder: " + str(sorted({a for a in k["raster"] if not G.ist_bebaubar(a)})))
check("die 40 Bauplätze sind genau die bebaubaren Felder",
      k["bauplaetze"] == sum(1 for a in k["raster"] if G.ist_bebaubar(a)), str(k["bauplaetze"]))
check("die Zeilenansicht passt zum Raster",
      [f for z in k["zeilen_raster"] for f in z] == k["raster"])
check("die Zeilenansicht hat 7 Zeilen zu je 8 Feldern",
      len(k["zeilen_raster"]) == 7 and all(len(z) == 8 for z in k["zeilen_raster"]))
check("alle Felder sind bekannte Geländearten",
      set(k["raster"]) <= set(G.GELAENDEARTEN), str(sorted(set(k["raster"]) - set(G.GELAENDEARTEN))))

abschnitt("Siedlungskarte — gleiche Saat, gleiche Karte (wichtig für Speichern/Laden)")
a = G.siedlungskarte_erzeugen(4711)["raster"]
b = G.siedlungskarte_erzeugen(4711)["raster"]
c = G.siedlungskarte_erzeugen(4712)["raster"]
check("zweimal Saat 4711 ergibt dieselbe Karte", a == b)
check("Saat 4712 ergibt eine andere Karte", a != c)

abschnitt("Siedlungskarte — jede Siedlung ist spielbar (Mindestbesatz)")
mindest = {"wald": 2, "berg": 2, "grasland": 3, "nebelsee": 1}
fehler = []
for saat in range(300):
    kk = G.siedlungskarte_erzeugen(saat)
    for art, n in mindest.items():
        if kk["zaehlung"][art] < n:
            fehler.append((saat, art, kk["zaehlung"][art]))
    if sum(1 for a in kk["raster"] if not G.ist_bebaubar(a)) != 16 or kk["bauplaetze"] != 40:
        fehler.append((saat, "nicht 40/16", sum(1 for a in kk["raster"] if not G.ist_bebaubar(a)),
                       kk["bauplaetze"]))
check("300 Karten erfüllen alle den Mindestbesatz", not fehler,
      f"{len(fehler)} Verstöße, z. B. {fehler[:3]}")
check("300 Karten haben jede genau 40 bebaubare und 16 gesperrte Felder", not fehler,
      str(fehler[:3]))

abschnitt("Siedlungskarte — Vielfalt")
karten = {tuple(G.siedlungskarte_erzeugen(s)["raster"]) for s in range(50)}
check("50 Saaten ergeben mindestens 45 verschiedene Karten", len(karten) >= 45,
      f"{len(karten)} verschiedene")

abschnitt("Siedlungskarte — Beschreibungen")
txt = G.karte_beschreiben(G.siedlungskarte_erzeugen(1))
check("Textfassung nennt Maße und Saat", "8x7" in txt and "Saat 1" in txt, txt)
check("Textfassung nennt 40 von 56 Feldern bebaubar", "40 von 56" in txt, txt)
bild = G.karte_als_text(G.siedlungskarte_erzeugen(1))
check("Rasterfassung hat 7 Zeilen", len(bild.splitlines()) == 7)
check("und 8 Felder je Zeile", all(len(z.split()) == 8 for z in bild.splitlines()))

abschnitt("Kartentypen — mehrere Karten mit verschiedenen Vorteilen")
check("fünf Kartentypen angelegt", len(G.KARTENTYPEN) == 5, str(sorted(G.KARTENTYPEN)))
check("Waldreich, Steinreich, Weideland, Nebelseeufer, Ausgeglichen sind dabei",
      set(G.KARTENTYPEN) == {"waldreich", "bergreich", "weideland", "nebelseeufer", "gemischt"},
      str(sorted(G.KARTENTYPEN)))
for tid, t in G.KARTENTYPEN.items():
    check(f"{tid} nennt einen Vorteil", bool(t.get("vorteil")), t.get("vorteil", "FEHLT")[:60])
    check(f"{tid} hat Gewichte für alle sieben Geländearten",
          set(t["gewichte"]) == set(G.GELAENDEARTEN), str(sorted(set(G.GELAENDEARTEN) - set(t["gewichte"]))))

vorkommen = {}
for saat in range(400):
    tid = G.siedlungskarte_erzeugen(saat)["typ"]
    vorkommen[tid] = vorkommen.get(tid, 0) + 1
check("über 400 Saaten kommen alle fünf Typen vor", set(vorkommen) == set(G.KARTENTYPEN),
      f"{vorkommen}")
check("die ausgeglichene Karte ist am häufigsten",
      max(vorkommen, key=vorkommen.get) == "gemischt", f"{vorkommen}")
check("das Nebelseeufer ist am seltensten",
      min(vorkommen, key=vorkommen.get) == "nebelseeufer", f"{vorkommen}")

check("gleiche Saat ergibt denselben Kartentyp",
      G.siedlungskarte_erzeugen(999)["typ"] == G.siedlungskarte_erzeugen(999)["typ"]
      and G.siedlungskarte_erzeugen(999)["raster"] == G.siedlungskarte_erzeugen(999)["raster"])
check("Typ lässt sich erzwingen",
      G.siedlungskarte_erzeugen(1, typ_id="bergreich")["typ"] == "bergreich")

abschnitt("Kartentypen — jeder Typ erfüllt die Spielbarkeitsregeln")
verstoesse = []
for tid in G.KARTENTYPEN:
    for saat in range(60):
        kk = G.siedlungskarte_erzeugen(saat, typ_id=tid)
        for art, n in mindest.items():
            if kk["zaehlung"][art] < n:
                verstoesse.append((tid, saat, art, kk["zaehlung"][art]))
        if sum(1 for a in kk["raster"] if not G.ist_bebaubar(a)) != 16 or kk["bauplaetze"] != 40:
            verstoesse.append((tid, saat, "nicht 40/16",
                               sum(1 for a in kk["raster"] if not G.ist_bebaubar(a)), kk["bauplaetze"]))
check("300 Karten aller Typen erfüllen Mindestbesatz und die 40/16-Aufteilung", not verstoesse,
      f"{len(verstoesse)} Verstöße, z. B. {verstoesse[:3]}")

abschnitt("Kartentypen — der Vorteil ist in Zahlen messbar (Mittel über 40 Karten)")


def mittel(tid: str, rohstoff: str) -> float:
    werte = [G.siedlungskarte_erzeugen(s, typ_id=tid)["profil"].get(rohstoff, 0.0) for s in range(40)]
    return round(sum(werte) / len(werte), 1)


def erwartet(tid: str, art: str) -> float:
    """Erwartungswert einer Geländeart aus den Gewichten des Kartentyps.

    56 Felder, davon 16 gesperrt: die bebaubaren Arten teilen sich die 40 freien Felder nach
    ihren Gewichten, die gesperrten Arten die 16 nach ihren eigenen Gewichten (nur Sumpf).
    """
    g = G.KARTENTYPEN[tid]["gewichte"]
    if not G.ist_bebaubar(art):
        summe = sum(v for k, v in g.items() if not G.ist_bebaubar(k))
        return round(16 * g[art] / summe, 1)
    summe = sum(v for k, v in g.items() if G.ist_bebaubar(k))
    return round(40 * g[art] / summe, 1)


for tid in G.KARTENTYPEN:
    if tid == "gemischt":
        continue
    kk = [G.siedlungskarte_erzeugen(s, typ_id=tid) for s in range(40)]
    gewichte = G.KARTENTYPEN[tid]["gewichte"]
    schwerpunkt = max(gewichte, key=gewichte.get)
    ist = round(sum(k["zaehlung"][schwerpunkt] for k in kk) / len(kk), 1)
    check(f"{tid}: Schwerpunkt {schwerpunkt} nahe der Gewichtung",
          abs(ist - erwartet(tid, schwerpunkt)) <= 3.0,
          f"Mittel {ist}, erwartet {erwartet(tid, schwerpunkt)}")
    check(f"{tid}: {schwerpunkt} häufiger als auf ausgeglichener Karte",
          ist > erwartet("gemischt", schwerpunkt),
          f"{ist} gegen {erwartet('gemischt', schwerpunkt)}")

for a, b, roh in [("waldreich", "bergreich", "holz"),
                  ("bergreich", "waldreich", "stein"),
                  ("bergreich", "waldreich", "metall"),
                  ("weideland", "bergreich", "nahrung"),
                  ("weideland", "bergreich", "wolle")]:
    va, vb = mittel(a, roh), mittel(b, roh)
    check(f"{a} liefert mehr {roh} als {b}", va > vb, f"{va} gegen {vb}")

mana = {tid: mittel(tid, "mana") for tid in G.KARTENTYPEN}
uebrige = [v for t, v in mana.items() if t != "nebelseeufer"]
schnitt = sum(uebrige) / len(uebrige)
check("Mana ist am Nebelseeufer am höchsten", max(mana, key=mana.get) == "nebelseeufer", f"{mana}")
check("und deutlich höher als im Schnitt der übrigen Karten",
      mana["nebelseeufer"] >= 1.4 * schnitt,
      f"Nebelseeufer {mana['nebelseeufer']} gegen Schnitt {schnitt:.1f}")

abschnitt("Kartentypen — Profil ist vollständig")
k = G.siedlungskarte_erzeugen(2026)
check("Profil nennt alle neun Rohstoffe", set(k["profil"]) == {
    "holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde"},
    str(sorted(k["profil"])))
check("alle Profilwerte sind positiv", all(v > 0 for v in k["profil"].values()), str(k["profil"]))
check("Beschreibung nennt den Kartentyp", k["typ_name"] in G.karte_beschreiben(k),
      G.karte_beschreiben(k))

sys.exit(bericht())
