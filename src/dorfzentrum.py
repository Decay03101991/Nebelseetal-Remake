"""Die Masse und die Texte des Dorfzentrums - an EINER Stelle (Nr. 16, Teil A).

Daniels Entscheidungen F-56, F-58, F-59, F-65 und F-66 (Register 550/568) legen das Dorfzentrum
in Zahlen fest. Bis V_0.0.4 standen diese Zahlen verstreut in `main.py` (Kachelmasse, Spalten,
Blattbreiten) - hier stehen sie EINMAL, damit Ansicht und Pruefdatei dieselbe Quelle lesen
(F-04: eine Rechenstelle, keine zweite Handliste).

Was hier NICHT steht: kein Tk, kein Zeichnen, keine Kenntnis des Spielstands. Nur Rechnung und
Formatierung. Die Ansicht ruft diese Funktionen und setzt die Zahlen um; die Wache
`tests/test_dorfzentrum_masse.py` rechnet dieselben Zahlen ohne Fenster nach.

Kennzeichnung wie in den Antworten: [g] gemessen, [r] gerechnet, Startwert = gekennzeichnet,
ersetzt durch eine Messung im Prozess.

**Quellen der Zahlen** (alle nachgerechnet, `docs/eingaenge/CLAUDE_20261112_ENTSCHEIDUNGEN_NR16/
NACHRECHNUNG_NR16.md`):
  * `ANTWORT_NR16.md`, Teil A1: die vollstaendige Masstabelle in beiden Faellen
    (1037 x 589, k = 1) und (1127 x 764, k = 1,2512).
  * `ANTWORT_NR14_DORFZENTRUM.md`: die Absicht hinter den Bloecken und Reitern (drei Reiter
    Lager / Werkstaetten / Einheiten, Auswahl je Reiter, Hinweis darunter).

**Befund B1 aus der Nachrechnung:** `tkopf` (Hoehe der Tabellenkopfzeile) ist NICHT zuverlaessig
gerechnet - seine Formel `ls(Fließtext fett) + round(9k)` ergibt im Fall 2 **33** statt der
angenommenen 30, weil Tk Pixel auf ganze Punkte rundet. Darum ist `tkopf` hier ein PARAMETER:
fehlt er, gilt der gekennzeichnete Startwert (und `tkopf_gemessen` ist False). Die Ansicht misst
die Kopfzeile und gibt sie mit.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------------------------
# Die Grundwerte (F-56 und Nr. 16, Abschnitt 0)
# ---------------------------------------------------------------------------------------------
KLEINTEXT_PX = 15           # F-56: Kleintext ist ABSOLUT 15 px - nicht `schrift(15)` (das waeren 19)
# Quelle der drei Faktoren: Antwort Nr. 16, Teil A1 (Register 555 nachgerechnet) - belegt, keine
# ANNAHME. Sie sind der Anteil, der mit k waechst (Nr. 14, R1).
P_FAKTOR = 8                # p = round(8k): Innenabstand und Luecke; belegt (Nr. 16, A1)
G_FAKTOR = 6                # g = round(6k): Abstand Symbol - Text; belegt (Nr. 14, R1)
S_MIN_FAKTOR = 316          # S_min = round(316k): Wunschbreite; belegt (Nr. 14, R2)
FELD_MAX = 64               # groesser wird ein Kartenfeld nie (Originalmass)
LEISTE = 18                 # Koordinatenleiste der Karte
LS_KLEIN, LS_ZW, LS_TITEL = 15, 18, 24   # Grundzeilenhoehen (mal k) aus Nr. 14, Abschnitt 0
KACHEL_SYMBOL = (64, 56)    # Bild, waechst NICHT mit k (Nr. 14, R1)
KACHEL_INNEN = 16           # 8 links + 8 rechts je Kachel (Nr. 16, A1)
LAGER_SPALTEN = 3           # fest: 17 Waren in 3 Spalten, 6 Reihen, letzte Reihe mit 2 Kacheln
EINHEITEN_JE_HAELFTE = 14   # 28 Arten in 2 x 14 (alle bleiben stehen, auch mit Bestand 0)
REITER_ANZAHL = 3           # Lager, Werkstaetten, Einheiten (Nr. 14, Abschnitt B)
REITER = ("Lager", "Werkstätten", "Einheiten")   # Reihenfolge = Nr. 14, Abschnitt B

# Startwerte der Knopfhoehen (Fall 2 gemessen, Fall 1 UNBEKANNT - Nr. 16, A1)
KNOEPFE_START = {"h_b": 35, "h_b1": 37}


def _rund(wert: float) -> int:
    """Kaufmaennisch runden, nie unter 1 (eine Breite von 0 waere unsichtbar)."""
    return max(1, int(round(float(wert))))


def _p(k: float) -> int:
    """Der Innenabstand p = round(8k) - EINE Stelle fuer alle Bloecke, Kacheln und Spalten."""
    return _rund(P_FAKTOR * k)


def _g(k: float) -> int:
    """Der Abstand zwischen Symbol und Text g = round(6k) - EINE Stelle (Nr. 14, R1)."""
    return _rund(G_FAKTOR * k)


def ls_start(k: float = 1.0) -> Dict[str, int]:
    """Zeilenhoehen (linespace) als gekennzeichneter STARTWERT: text / zw / zahl / titel.

    Die Zeilenhoehe ist KEINE gerade Funktion von k - sie kommt aus der Schrift, die Tk wirklich
    benutzt, und Tk rundet Pixel auf ganze Punkte. Gemessen sind es im Fall 2 **19 / 22 / 30**
    (Nr. 16, A1); `round(18 x 1,2512)` ergaebe 23 und damit 13 px zu hohe Tabellen. Darum ist
    `ls` in allen Funktionen ein PARAMETER: die Ansicht misst mit `font.metrics("linespace")` und
    gibt die echten Werte mit. Diese Funktion liefert nur den Startwert, wenn nicht gemessen wird.
    """
    return {"text": _rund(LS_KLEIN * k), "zw": _rund(LS_ZW * k), "zahl": _rund(LS_ZW * k),
            "titel": _rund(LS_TITEL * k)}


def _ls_wert(ls: Optional[Dict[str, Any]], k: float) -> Dict[str, int]:
    """Die uebergebenen Zeilenhoehen, aufgefuellt um fehlende Rollen aus dem Startwert."""
    roh = ls_start(k)
    if not ls:
        return roh
    for rolle in ("text", "zw", "zahl", "titel"):
        if rolle in ls:
            roh[rolle] = max(1, int(ls[rolle]))
    if "zahl" not in ls and "zw" in ls:            # Zahl und Zwischentitel sind gleich hoch
        roh["zahl"] = roh["zw"]
    return roh


def masse(breite: int, hoehe: int, k: float = 1.0, rollbalken: int = 17,
          tkopf: Optional[int] = None, ls: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Alle Masse des Dorfzentrums aus der GEMESSENEN Flaeche (Nr. 16, Teil A).

    Die Formeln sind die aus Nr. 14, Abschnitt R2 und Nr. 16, Abschnitt A1:

        p    = round(8k)          S_min = round(316k)      S = W - rb - R
        f    = min(64, (H-18)//10, (W - rb - S_min - 18) // 10)
        R    = 10f + 18

    Damit gilt bei (1127, 764, k = 1,2512, rb = 21): f = 64, R = **658**, S = **448** - dieselbe
    Spalte wie die Siedlungsansicht (F-57), also zwei Ansichten mit einer Spaltenbreite.

    `kopf` (74 / 59), `reiterleiste` (42 / 34) und `innenhoehe` (702 / 539) sind die drei
    Senkrechtmasse; `bloecke()` verteilt die Spalte darauf.

    Rueckgabe (Woerterbuch, alle Werte in px)::

        p, g, s_min, feld, karte, spalte, rollbalken, textbreite,
        ls_text, ls_zw, ls_zahl, ls_titel, kopf, reiterleiste, innenhoehe, reiterbreite,
        tkopf, tkopf_gemessen, lager{}, einheiten{}, werkstaetten{}, bloecke{}
    """
    breite = max(1, int(breite))
    hoehe = max(1, int(hoehe))
    rb = max(0, int(rollbalken))
    p = _p(k)
    g = _g(k)
    s_min = _rund(S_MIN_FAKTOR * k)
    feld = min(FELD_MAX, (hoehe - LEISTE) // 10, (breite - rb - s_min - LEISTE) // 10)
    feld = max(1, int(feld))
    karte = 10 * feld + LEISTE
    spalte = max(0, breite - rb - karte)
    hoehen = _ls_wert(ls, k)
    ls_text = hoehen["text"]
    ls_zw = hoehen["zw"]
    ls_zahl = hoehen["zahl"]
    ls_titel = hoehen["titel"]
    kopf = 2 * p + ls_titel + _rund(4 * k) + ls_text
    reiterleiste = ls_zw + 2 * p
    innenhoehe = hoehe - reiterleiste - 2 * p
    reiterbreite = max(1, (karte - 2 * p) // REITER_ANZAHL)
    textbreite = max(1, spalte - 2 * p)
    if tkopf is None:                                  # Startwert (Befund B1: ungenau, bitte messen)
        kopfzeile = ls_text + _rund(9 * k)
        gemessen = False
    else:
        kopfzeile = max(1, int(tkopf))
        gemessen = True
    ergebnis = {
        "breite": breite, "hoehe": hoehe, "k": float(k), "rollbalken": rb,
        "p": p, "g": g, "s_min": s_min, "feld": feld, "karte": karte, "spalte": spalte,
        "textbreite": textbreite,
        "ls_text": ls_text, "ls_zw": ls_zw, "ls_zahl": ls_zahl, "ls_titel": ls_titel,
        "kopf": kopf, "reiterleiste": reiterleiste, "innenhoehe": innenhoehe,
        "reiterbreite": reiterbreite, "tkopf": kopfzeile, "tkopf_gemessen": gemessen,
        "uebereinander": spalte < 2 * p + 100,          # zu schmal: Karte nimmt die volle Breite
    }
    ergebnis["lager"] = lager_masse(karte, k, hoehen)
    ergebnis["einheiten"] = einheiten_masse(karte, k, kopfzeile, hoehen)
    ergebnis["werkstaetten"] = werkstaetten_masse(karte, k, kopfzeile, hoehen)
    ergebnis["bloecke"] = bloecke(hoehe, k, ls_text=ls_text, tkopf=kopfzeile, ls_titel=ls_titel)
    return ergebnis


def bloecke(hoehe: int, k: float = 1.0, ls_text: Optional[int] = None, h_b: Optional[int] = None,
            h_b1: Optional[int] = None, tkopf: Optional[int] = None,
            ls_titel: Optional[int] = None, technik: bool = False) -> Dict[str, int]:
    """Die sieben Bloecke der Spalte (F-59, Nr. 16 A1) - Hoehen in px, von oben nach unten.

    | # | Block            | Formel                      | Fall 2 |
    |---|------------------|-----------------------------|--------|
    | 1 | Kopf             | wie `masse()["kopf"]`       |     74 |
    | 2 | Naechster Schritt| 2p + h_b1                   |     57 |
    | 3 | Ort              | 2p + h_b                    |     55 |
    | 4 | Aktionen         | 2p + 2 h_b + p              |    100 |
    | 5 | Auswahl je Reiter| **Rest**                    |    370 |
    | 6 | Hinweis          | 2p + 2 ls_text              |     58 |
    | 7 | Technik          | 2p + h_b (nur Entwickler)   |     55 |

    Block 5 bekommt den REST, nicht eine eigene Zahl: nur so fuellt die Spalte die Hoehe genau,
    und der Reiterwechsel aendert die Hoehe der uebrigen Bloecke nicht. Summe der Bloecke 1 bis 4
    und 6 = 344 im Fall 2, dazu fuenf Luecken a p = 10 -> 394; 764 - 394 = **370**.

    `technik` nimmt Block 7 mit und verkleinert Block 5 um dessen Hoehe plus eine Luecke
    (Entwicklerbetrieb; im Spielerbetrieb bleibt der Block weg).
    """
    p = _p(k)
    n = ls_text if ls_text is not None else _rund(LS_KLEIN * k)
    titel = int(ls_titel) if ls_titel is not None else _rund(LS_TITEL * k)
    kopf = 2 * p + titel + _rund(4 * k) + n
    h_b = int(h_b if h_b is not None else KNOEPFE_START["h_b"])
    h_b1 = int(h_b1 if h_b1 is not None else KNOEPFE_START["h_b1"])
    seite = {"kopf": kopf, "naechster": 2 * p + h_b1, "ort": 2 * p + h_b,
             "aktionen": 2 * p + 2 * h_b + p, "hinweis": 2 * p + 2 * n}
    technikblock = (2 * p + h_b) if technik else 0
    luecken = 5 * p if not technik else 6 * p       # fuenf feste Luecken, mit Technik sechs
    rest = int(hoehe) - sum(seite.values()) - luecken - technikblock
    seite["auswahl"] = max(120, rest)
    seite["technik"] = technikblock
    seite["tkopf"] = int(tkopf) if tkopf is not None else 0     # nur zur Nachvollziehbarkeit
    return seite


def lager_masse(karte: int, k: float = 1.0, ls: Optional[Dict[str, Any]] = None,
                waren: int = 17) -> Dict[str, int]:
    """Reiter **Lager**: 17 Waren als Kacheln, 3 Spalten, 6 Reihen (Nr. 16, A1).

        T_w = (R - 4p) // 3                 Kachelbreite          206
        Text = T_w - 16 - 64 - g            Textbreite in der K.  118
        Block = 2 ls_text + round(2k) + ls_zahl                   63
        T_h = 2p + max(56, Block)           Kachelhoehe            83
        6 Reihen = 6 T_h + 5 p                                    548 <= 702

    `waren` ist die Anzahl der Waren (aus `data/items.json` gelesen, hier nur als Startwert 17):
    die Reihenzahl ergibt sich als `ceil(waren / 3)`, damit eine neue Ware die Tabelle vergroessert
    statt still aus dem Bild zu fallen.
    """
    reihen = max(1, -(-int(waren) // LAGER_SPALTEN))
    p = _p(k)
    g = _g(k)
    hoehen = _ls_wert(ls, k)
    ls_text = hoehen["text"]
    ls_zahl = hoehen["zahl"]
    breite = max(1, (int(karte) - 4 * p) // LAGER_SPALTEN)
    textblock = 2 * ls_text + _rund(2 * k) + ls_zahl
    hoehe = 2 * p + max(KACHEL_SYMBOL[1], textblock)
    return {"spalten": LAGER_SPALTEN, "kachel_breite": breite, "kachel_hoehe": hoehe,
            "textbreite": max(1, breite - KACHEL_INNEN - KACHEL_SYMBOL[0] - g),
            "textblock": textblock, "symbol_breite": KACHEL_SYMBOL[0],
            "symbol_hoehe": KACHEL_SYMBOL[1], "reihen": reihen,
            "hoehe": reihen * hoehe + (reihen - 1) * p, "luecke": p}


def einheiten_masse(karte: int, k: float = 1.0, tkopf: Optional[int] = None,
                    ls: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
    """Reiter **Einheiten**: 28 Arten in zwei Haelften zu je 14, OHNE Spalte Verwundete (F-65).

        z      = ls_zahl + p                       Zeilenhoehe            32
        Haelften = (R - 3p) // 2                   halbe Breite          314
        Zahl   = round(48k)                        Zahlspalte             60
        Name   = Haelften - Zahl - p               Namensspalte          244
        Hoehe  = tkopf + 14 z                                            478 (tkopf 30)

    F-65 (Daniel 12.11.2026): keine Spalte "Verwundete". Damit braucht keine Einheit Kleintext;
    Heilpreis und Heildauer bleiben in `verwundete.py` und werden hier NICHT angezeigt.
    """
    p = _p(k)
    hoehen = _ls_wert(ls, k)
    z = hoehen["zahl"] + p
    halbe = max(1, (int(karte) - 3 * p) // 2)
    zahl = _rund(48 * k)
    kopf = int(tkopf) if tkopf is not None else hoehen["text"] + _rund(9 * k)
    return {"zeile": z, "kopfzeile": kopf, "haelfte": halbe, "zahlspalte": zahl,
            "namensspalte": max(1, halbe - zahl - p), "je_haelfte": EINHEITEN_JE_HAELFTE,
            "hoehe": kopf + EINHEITEN_JE_HAELFTE * z}


def werkstaetten_masse(karte: int, k: float = 1.0, tkopf: Optional[int] = None,
                       ls: Optional[Dict[str, Any]] = None,
                       zeilen: int = 17) -> Dict[str, int]:
    """Reiter **Werkstaetten**: 17 Rezepte, vier Spalten mit Zutat-Spalte (F-58, Nr. 16 A1).

        Werkstatt = round(100k)   Zutat = round(120k)   Zustand = round(84k)
        Name      = R - 2p - 3p - (Werkstatt + Zutat + Zustand)      228
        Hoehe     = tkopf + 17 z                                     574 (tkopf 30)

    Die Zutat-Spalte traegt "[Zutat] [vorhanden] / [noetig] ✓/✕" - die Ware selbst hat genau EINE
    Zutat (Faktenblatt: 17 Rezepte mit hoechstens einer Zutat), darum passt sie in 150 px.
    `zeilen` ist die Anzahl der Rezepte (aus `data/warenrezepte.json`, hier Startwert 17).
    """
    p = _p(k)
    hoehen = _ls_wert(ls, k)
    z = hoehen["zahl"] + p
    werkstatt = _rund(100 * k)
    zutat = _rund(120 * k)
    zustand = _rund(84 * k)
    kopf = int(tkopf) if tkopf is not None else hoehen["text"] + _rund(9 * k)
    return {"zeile": z, "kopfzeile": kopf, "werkstatt": werkstatt, "zutat": zutat,
            "zustand": zustand, "zeilen": max(1, int(zeilen)),
            "name": max(1, int(karte) - 2 * p - 3 * p - (werkstatt + zutat + zustand)),
            "hoehe": kopf + max(1, int(zeilen)) * z}


# ---------------------------------------------------------------------------------------------
# Texte - die Ansicht FORMATIERT nur (F-66, F-58, F-65)
# ---------------------------------------------------------------------------------------------
HAKEN = "\u2713"            # ✓
KREUZ = "\u2715"            # ✕
TRENNER = " \u00b7 "        # ·


def kennzahlen_text(kennzahlen: Dict[str, Any]) -> str:
    """Der Kopf des Dorfzentrums in Worten (F-66): "x von 17 vorrätig · y von 17 herstellbar".

    Gezaehlt wird in `spieloekonomie.dorfzentrum_kennzahlen` (F-60); hier wird nur formatiert -
    keine Zahl der Ansicht stammt aus einer eigenen Rechnung (`test_quelle_ast`).
    Fehlt ein Schluessel, bleibt sein Teil weg (kein erfundenes "0 von 0").
    """
    daten = kennzahlen or {}
    teile: List[str] = []
    if "vorraetig" in daten and "waren_gesamt" in daten:
        teile.append("%s von %s vorr\u00e4tig" % (daten["vorraetig"], daten["waren_gesamt"]))
    if "herstellbar" in daten and "waren_gesamt" in daten:
        teile.append("%s von %s herstellbar" % (daten["herstellbar"], daten["waren_gesamt"]))
    return TRENNER.join(teile)


def zutat_text(name: str, vorhanden: Any, noetig: Any) -> str:
    """Die Zutat einer Ware in der Werkstatt-Tabelle: "Metall 12 / 4 ✓" (Nr. 16, A1).

    Reihenfolge ist **vorhanden / noetig** - der Spieler liest links seinen Bestand, rechts den
    Bedarf. Das Zeichen sagt dasselbe wie die Zahlen; es ersetzt sie nicht.
    """
    try:
        genug = float(vorhanden) >= float(noetig)
    except (TypeError, ValueError):
        genug = False
    return "%s %s / %s %s" % (str(name), zahl_text(vorhanden), zahl_text(noetig),
                              HAKEN if genug else KREUZ)


def zustand_text(herstellbar: bool) -> str:
    """Der Zustand einer Ware in der Werkstatt-Tabelle: "✓ herstellbar" oder "✕ fehlt"."""
    return ("%s herstellbar" % HAKEN) if herstellbar else ("%s fehlt" % KREUZ)


def zahl_text(wert: Any) -> str:
    """Eine Zahl fuer die Anzeige: ganzzahlig ohne Komma, grosse Zahlen mit Punkt.

    Dieselbe Regel wie `main._lager_zahl` (T08 C2): 0 bleibt "0", 1334.0 wird "1334",
    12345 wird "12.345", eine echte Nachkommastelle bleibt stehen.
    """
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return str(wert)
    if abs(zahl - int(zahl)) < 1e-9:
        ganz = int(zahl)
        if abs(ganz) >= 10000:
            return "{:,}".format(ganz).replace(",", ".")
        return str(ganz)
    return "%g" % zahl


def kleintext_zu_breit(text: str, breite: int, messen) -> bool:
    """F-56: Kleintext ist absolut 15 px - passt er nicht, meldet diese Stelle es.

    `messen(text, 15)` liefert die Textbreite in px bei ABSOLUTEN 15 px (die Ansicht gibt
    `font.measure` weiter). Die Regel aus Nr. 16, A1 lautet: passt `messwert > breite - 4`, wird
    gekuerzt - bei Mengen zuerst die Zahl, nie der Name.

    Ohne Messfunktion (reine Rechnung) kommt False zurueck: dann ist die Frage nicht beantwortet,
    nicht etwa "passt".
    """
    if messen is None:
        return False
    try:
        return float(messen(str(text), KLEINTEXT_PX)) > float(breite) - 4.0
    except Exception:                                          # noqa: BLE001 - Messung nicht moeglich
        return False


def reiter_treffer(x: int, reiterbreite: int, p: int, anzahl: int = REITER_ANZAHL) -> int:
    """Welcher Reiter wurde bei x angeklickt? -1 heisst: keiner (Nr. 14, B1: nur anklicken).

    Die Reiterleiste beginnt bei p; jeder Reiter ist `reiterbreite` breit. Ein Klick ausserhalb
    der Leiste waehlt NICHTS - vorher haette er still den letzten Reiter genommen.
    """
    try:
        x = int(x)
    except (TypeError, ValueError):
        return -1
    if x < p:
        return -1
    stelle = (x - p) // max(1, int(reiterbreite))
    if 0 <= stelle < int(anzahl):
        return int(stelle)
    return -1


def warentext(wert: Any) -> str:
    """Ein Warenbestand als Text - eine Stelle fuer alle Reiter (Nulllage bleibt "0")."""
    return zahl_text(wert)
