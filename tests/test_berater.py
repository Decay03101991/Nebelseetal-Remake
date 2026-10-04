"""Pruefung der Auskunft im Spiel (src/berater.py).

Der Berater muss aus den echten Spieldaten antworten und darf nichts erfinden:
jede genannte Zahl muss in data/*.json oder im Handbuch stehen. Wo das Handbuch schweigt,
muss er das sagen.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import berater as B
import gelaende as G
import spieldaten as S

abschnitt("Auskunft — Begrüßung und Beispielfragen")
beg = B.begruessung()
check("die Begrüßung erklärt sich", "Auskunft" in beg and "handbuch" in beg.lower(), beg[:80])
check("und nennt Beispielfragen", beg.count("•") >= 4, str(beg.count("•")))
check("eine leere Frage gibt die Begrüßung", B.antwort("") == beg)

abschnitt("Auskunft — Gebäude werden mit den echten Zahlen erklärt")
t = B.antwort("Was macht der Holzfäller?")
check("nennt den Namen", "Holzfäller" in t, t[:60])
check("nennt Wald 4 pro Stunde", "Wald: 4/h" in t or "Wald: 4" in t, t)
check("nennt Steppe 2 pro Stunde", "Steppe: 2" in t, t)
check("nennt den Baupreis aus der Vorschlagsdatei", "8 Holz" in t and "4 Stein" in t, t)
check("und kennzeichnet den Preis als Vorschlag", "VORSCHLAG" in t, t)

t = B.antwort("Welches Gelände braucht der Steinmetz?")
check("Steinmetz: Berg 4", "Berg: 4" in t, t)
check("Steinmetz: Hügel 2", "Hügel: 2" in t, t)

t = B.antwort("Was ist mit dem Tempel?")
check("Tempel: Nebelsee 5", "Nebelsee: 5" in t, t)
check("Tempel: sonst 1", "1/h" in t or "1 " in t, t[:200])

t = B.antwort("Wie funktioniert der Jäger?")
check("Jäger nennt Nahrung UND Leder", "Nahrung 2" in t and "Leder 2" in t, t)

abschnitt("Auskunft — Gelände und Sumpf")
t = B.antwort("Was ist der Sumpf?")
check("Sumpf wird als nicht bebaubar genannt", "nicht bebaubar" in t, t)
t = B.antwort("Welche Geländearten gibt es?")
for art in ("Grasland", "Steppe", "Wald", "Hügel", "Berg", "Nebelsee", "Sumpf"):
    check(f"Gelände {art} wird genannt", art in t, t[:200] if art not in t else "")

abschnitt("Auskunft — Einheiten nennen die Originalwerte")
t = B.antwort("Was kann der Paladin?")
check("Paladin: Lebensenergie 50", "Lebensenergie 50" in t, t)
check("Paladin: Attacke 85", "Attacke 85" in t, t)
check("Paladin: Treffer 6 bis 20", "Treffer min 6" in t and "Treffer max 20" in t, t)
t = B.antwort("Was ist ein Handkarren?")
check("Handkarren wird erklärt", "Handkarren" in t, t[:80])
check("und die fehlenden Angaben werden benannt", "nicht angegeben" in t, t)

abschnitt("Auskunft — Waren")
t = B.antwort("Wer braucht den Langbogen?")
langbogen = S.waren()["Langbogen"]
check("Langbogen: die Werkstatt aus den Daten wird genannt", langbogen["werkstatt"] in t, t)
bedarf = langbogen.get("benoetigt_von") or []
check("und wer ihn braucht", "Verlangt von" in t and all(x in t for x in bedarf), t)
check("der Langbogen wird nicht mit dem Bogen verwechselt",
      t.strip().startswith("Langbogen"), t[:40])

abschnitt("Auskunft — Regeln (Forschung, Kampf, Punkte, Portal)")
t = B.antwort("Was kostet die Forschung?")
check("Forschung: 50 Holz", "50 Holz" in t, t)
check("Forschung: Stufe im Quadrat", "Stufe × Stufe" in t or "Quadrat" in t or "×" in t, t)
t = B.antwort("Wie läuft ein Kampf ab?")
for stichwort in ("fernk", "wall", "zehn"):
    check(f"Kampf nennt '{stichwort}'", stichwort in t.lower(), t[:160] if stichwort not in t.lower() else "")
t = B.antwort("Wie gibt es Punkte?")
check("Punkte: Stufe hoch drei", "hoch drei" in t or "dreimal" in t, t)
t = B.antwort("Was ist der Limbus?")
check("Portal: 20 Dimensionen", "20 Dimensionen" in t, t)
check("Portal: die sechs Welten", "Valhalla" in t and "Ragnarök" in t, t)

abschnitt("Auskunft — Start und Bedienung")
t = B.antwort("Wie fange ich an?")
check("Start nennt 100 Holz und 100 Stein", "100 Holz" in t and "100 Stein" in t, t)
check("Start nennt die 10 Siedler", "10 Siedlern" in t or "10 Siedler" in t, t)
t = B.antwort("Hilfe zur Steuerung")
check("Bedienung nennt die Siedlungskarte", "Siedlungskarte" in t, t)

abschnitt("Auskunft — Tipp zum Spielstand")
class FalscherZustand:
    pass

ohne = FalscherZustand()
t = B.tipps(ohne)
check("ohne Siedlungen kommt trotzdem ein Tipp", len(t) > 30, t[:80])

class Siedlung:
    def __init__(self):
        self.name = "Testsiedlung"
        self.karte = G.siedlungskarte_erzeugen(5, typ_id="waldreich")
        self.bauten = {}

t = B.tipps(type("Z", (), {"settlements": [Siedlung()]})())
check("Tipp merkt, dass auf Wald kein Holzfäller steht", "Holzfäller" in t, t)
check("Tipp nennt die Sumpffelder als normal", "Sumpffelder" in t, t)

abschnitt("Auskunft — antwortet zu ALLEN Gebaeuden, Einheiten und Waren (kein Absturz)")
fehler = []
for kennung, geb in G.alle_gebaeude().items():
    try:
        a = B.antwort(geb["name"])
        if geb["name"] not in a:
            fehler.append((geb["name"], "Antwort ohne Namen"))
    except Exception as exc:
        fehler.append((geb["name"], f"{type(exc).__name__}: {exc}"))
check(f"alle {len(G.alle_gebaeude())} Gebaeude werden beantwortet", not fehler, str(fehler[:3]))

fehler = []
for name in S.einheiten():
    try:
        a = B.antwort(name)
        if name not in a:
            fehler.append((name, "Antwort ohne Namen"))
    except Exception as exc:
        fehler.append((name, f"{type(exc).__name__}: {exc}"))
check(f"alle {len(S.einheiten())} Einheiten werden beantwortet", not fehler, str(fehler[:3]))

fehler = []
for name in S.waren():
    try:
        a = B.antwort(name)
        if name not in a:
            fehler.append((name, "Antwort ohne Namen"))
    except Exception as exc:
        fehler.append((name, f"{type(exc).__name__}: {exc}"))
check(f"alle {len(S.waren())} Waren werden beantwortet", not fehler, str(fehler[:3]))

abschnitt("Auskunft — jeder Vorschlagsknopf im Spiel wird wirklich beantwortet")
import re
main_quelle = open(os.path.join(ROOT, "src", "main.py"), encoding="utf-8").read()
treffer = re.search(r"vorschlaege = \[(.*?)\]", main_quelle, re.S)
check("die Vorschlagsliste steht im Spiel", treffer is not None)
fragen = re.findall(r'"([^"]+)"', treffer.group(1)) if treffer else []
check("es gibt mindestens fünf Vorschläge", len(fragen) >= 5, str(fragen))
for frage in fragen:
    a = B.antwort(frage)
    check(f"'{frage}' wird beantwortet", "Das weiß ich nicht" not in a, a[:110])

abschnitt("Auskunft — sagt ehrlich, wenn sie etwas nicht weiß")
t = B.antwort("Wie wird das Wetter morgen in Hamburg?")
check("unbekannte Frage wird zugegeben", "Das weiß ich nicht" in t, t[:90])
check("und es werden Beispielfragen angeboten", t.count("•") >= 4, str(t.count("•")))
check("keine erfundene Antwort", "Wetter" not in t.replace("Das weiß ich nicht", ""), t[:140])

abschnitt("Auskunft — arbeitet ohne Netz und ohne Schlüssel")
quelle = open(os.path.join(ROOT, "src", "berater.py"), encoding="utf-8").read()
check("kein Modell fest eingebaut", B.ANTWORT_QUELLE_LLM is None)
for verboten in ("import requests", "import urllib", "api_key", "API_KEY", "sk-"):
    check(f"kein Netzzugriff/Schlüssel im Modul ({verboten})", verboten not in quelle)
check("dafür eine vorbereitete, aber leere Stelle für ein Modell",
      "ANTWORT_QUELLE_LLM" in quelle)

sys.exit(bericht())
