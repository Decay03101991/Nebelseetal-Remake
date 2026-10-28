"""GPT-B01: konservative Bot-Zielwahl nach den Wallregeln der Originalanleitung.

Keine eigenen Kampfwerte, keine Magieressourcen, keine Mutation. Der Bot greift nur
Orte an, deren belegte Wall-SK-Schwelle er aktuell erreichen kann. Er darf trotzdem
im eigentlichen Kampf verlieren: die Vorpruefung garantiert KEINEN Sieg.

Entwurfsregel (nicht Original): unter geeigneten Orten wird derjenige mit dem
niedrigsten Wall, dann den wenigsten stationierten Verteidigern, dann dem Namen
gewaehlt. Hermes kann diese Gewichtung spaeter ersetzen.
"""
from __future__ import annotations

import einheiten
import gebaeude_wirkung


def _anzahl(x):
    try:
        return max(0, int(x))
    except (ValueError, TypeError, OverflowError):
        return 0


def _stufe(x):
    try:
        return max(0, min(10, int(x)))
    except (TypeError, ValueError, OverflowError):
        return 0


def _zustand(x):
    try:
        return max(0.0, min(100.0, float(x)))
    except (TypeError, ValueError, OverflowError):
        return 100.0


def schlagkraft(truppen, geraete=None):
    """Summiert nur die Rollen, die das Original in der Vorrunde vorsieht.

    Fusstruppen = Nah- und Fernkampf (entspricht `kampf.FUSSTRUPPEN`).
    Belagerungs-SK nur von echten Belagerungswaffen, nicht von Karren.
    """
    fuss = 0
    bel = 0
    for inventar in (truppen or {}, geraete or {}):
        for name, menge in inventar.items():
            eintrag = einheiten.alle().get(name)
            if not eintrag:
                continue
            anzahl = _anzahl(menge)
            if eintrag['kategorie'] in ('Nahkampf', 'Fernkampf'):
                fuss += einheiten.schlagkraft(name) * anzahl
            elif eintrag['rolle'] == 'belagerung':
                bel += einheiten.schlagkraft(name) * anzahl
    return {'fusstruppen': fuss, 'belagerungswaffen': bel}


def pruefe_vorrunde(truppen, geraete, stufe, zustand=100.0):
    """Beurteilung der Wall-Vorrunde mit den ORIGINAL-Schwellen aus den Daten.

    Ausgabe 'moeglich' bezieht sich ausschliesslich auf die Vorrunde, nicht
    Kampf-/Siegwahrscheinlichkeit. Abgewehrte und wehrlose Truppen erhalten keine
    Gratisbeute und keinen Kassenabzug.
    """
    sk = schlagkraft(truppen, geraete)
    stufe = _stufe(stufe)
    faktor = _zustand(zustand) / 100.0
    schwelle = gebaeude_wirkung.wall_schwelle(stufe)
    fuss_noetig = float(schwelle['fusstruppen'] or 0) * faktor
    bel_noetig = (float(schwelle['belagerungswaffen']) * faktor
                  if schwelle['belagerungswaffen'] is not None else 0.0)
    gruende = []
    if not any(einheiten.alle().get(n, {}).get('kategorie') in ('Nahkampf', 'Fernkampf') and _anzahl(v) > 0
               for n, v in (truppen or {}).items()):
        gruende.append('Keine Fusskampftruppen vorhanden.')
    if sk['fusstruppen'] < fuss_noetig:
        gruende.append('Schlagkraft der Fusstruppen reicht fuer den Wall nicht.')
    if sk['belagerungswaffen'] < bel_noetig:
        gruende.append('Belagerungswaffen reichen fuer diese Wallstufe nicht.')
    return {'moeglich': not gruende, 'grund': ' '.join(gruende),
            'sk': sk, 'schwelle': {'fusstruppen': fuss_noetig,
                                'belagerungswaffen': bel_noetig}}


def waehle_ziel(orte, truppen, geraete, wallzustand):
    """Rueckgabe (Ort|None, Diagnose). `wallzustand(ort)` -> (Stufe, Zustand).

    Nicht geeignete Orte werden NICHT angegriffen. Strategische Auswahl unter
    moeglichen Zielen ist Vorschlag, Originalhandbuch hat keine Bot-Zielwahl.
    """
    machbare = []
    gesperrt = []
    for ort in (orte or []):
        stufe, zustand = wallzustand(ort)
        pruefung = pruefe_vorrunde(truppen, geraete, stufe, zustand)
        if pruefung['moeglich']:
            verteidiger = sum(_anzahl(v) for v in (getattr(ort, 'einheiten', {}) or {}).values())
            machbare.append((_stufe(stufe), verteidiger, str(getattr(ort, 'name', '')), ort))
        else:
            gesperrt.append((str(getattr(ort, 'name', '')), pruefung['grund']))
    if not machbare:
        return None, {'moeglich': False, 'gesperrt': gesperrt,
                      'grund': 'Kein mit der aktuellen Armee ueberwindbarer Dorfwall.'}
    machbare.sort(key=lambda entry: entry[:3])
    return machbare[0][3], {'moeglich': True, 'gesperrt': gesperrt,
                            'grund': 'Vorrunde erreichbar, Kampfausgang offen.'}
