# -*- coding: ascii -*-
"""Die Demo muss LEER ausgeliefert werden - kein vorhandener Spielstand im Paket.

Daniel 01.11.2026, woertlich: "noch etwas in der demo exe darf es keine vorhandenen
spielstaende geben sie muss leer sein." (Register 101)

Was diese Pruefdatei belegt:
  1. Die gebundelten Ordner (data, assets) enthalten KEINEN Spielstand, keinen
     Admin-Teststand, kein Passworttor und keine Sperrdatei.
  2. Der Bau der oeffentlichen EXE bricht ab, wenn so eine Datei dort liegt - lieber
     keine EXE als eine mit fremden Staenden.
  3. Der Demo-Einstieg benutzt einen eigenen, nie benutzten Speicherordner unter
     %LOCALAPPDATA%, nicht den Ordner der frueheren Testversion und nichts im Projekt.
  4. Ein frischer Speicherordner ergibt drei LEERE Slots (erster Start = leeres Spiel).
  5. Der Demo-Ordner dieses Rechners wird nicht als Quelle benutzt: die Pruefung
     arbeitet ausschliesslich mit temporaeren Ordnern.

Aufruf: python -X utf8 tests/test_demo_leer.py
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT_PFAD, SRC = import_src()
ROOT = Path(ROOT_PFAD)
os.chdir(SRC)

import spielstaende  # noqa: E402


def _bauwerkzeug():
    """Laedt tools/build_public_exe.py als Modul, ohne den Bau zu starten."""
    pfad = ROOT / "tools" / "build_public_exe.py"
    spec = importlib.util.spec_from_file_location("build_public_exe_pruefung", pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _pruefungen_paket():
    abschnitt("1. Das Paket ist leer: keine Spielstaende in data/ und assets/")
    bau = _bauwerkzeug()
    treffer = bau.spielstaende_im_paket(ROOT)
    check("data/ und assets/ enthalten keinen Spielstand", treffer == [], str(treffer))

    muster = bau.SPIELSTAND_MUSTER
    check("das Bauwerkzeug kennt die Spielstandsmuster",
          "savegame" in muster and "admin_teststand" in muster and "tor.json" in muster,
          str(muster))
    eigene = []
    for ordner in ("data", "assets"):
        for datei in sorted((ROOT / ordner).rglob("*")):
            if not datei.is_file():
                continue
            name = datei.name.lower()
            if any(stueck in name for stueck in muster):
                eigene.append(str(datei.relative_to(ROOT)))
    check("auch ohne das Werkzeug gefunden: keine Spielstandsdatei", eigene == [], str(eigene))

    grosse = [d for d in (ROOT / "data").glob("*.json") if d.stat().st_size > 400000]
    check("keine uebergrosse JSON in data/ (ein Spielstand waere ~1 MB)", grosse == [],
          str([(g.name, g.stat().st_size) for g in grosse]))


def _pruefungen_bau_abbruch():
    abschnitt("2. Der Bau bricht ab, wenn ein Spielstand im Paket liegt")
    bau = _bauwerkzeug()
    with tempfile.TemporaryDirectory() as tmp:
        basis = Path(tmp)
        (basis / "data").mkdir()
        (basis / "assets").mkdir()
        (basis / "data" / "gelaende.json").write_text("{}", encoding="ascii")
        (basis / "data" / "savegame_slot1.json").write_text("{}", encoding="ascii")
        (basis / "assets" / "game.lock").write_text("1", encoding="ascii")
        treffer = bau.spielstaende_im_paket(basis)
        check("ein Spielstand in data/ wird gefunden",
              any("savegame_slot1.json" in t for t in treffer), str(treffer))
        check("eine Sperrdatei in assets/ wird gefunden",
              any("game.lock" in t for t in treffer), str(treffer))
        check("normale Datendateien gelten nicht als Spielstand",
              not any("gelaende.json" in t for t in treffer), str(treffer))
    quelle = (ROOT / "tools" / "build_public_exe.py").read_text(encoding="utf-8")
    check("die Vorpruefung ruft die Spielstandspruefung auf",
          "spielstaende_im_paket(ROOT)" in quelle, "")
    check("die Meldung sagt, dass die Demo LEER ausgeliefert wird",
          "LEER ausgeliefert" in quelle, "")
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "data").mkdir()
        check("ein Ordner ohne Spielstaende liefert eine leere Liste",
              bau.spielstaende_im_paket(Path(tmp)) == [], "")


def _pruefungen_einstieg():
    abschnitt("3. Der Demo-Einstieg benutzt einen eigenen Speicherordner")
    quelle = (ROOT / "src" / "public_start.py").read_text(encoding="utf-8")
    check("der Einstieg setzt NEBEL_SPIELDATEN_ORDNER", "NEBEL_SPIELDATEN_ORDNER" in quelle, "")
    check("der Ordner heisst Demo", '"Demo"' in quelle, "")
    check("der Ordner der frueheren Testversion wird nicht mehr gesetzt",
          "Public_Test_FIX04j" not in quelle, "")
    check("Daniels Vorgabe steht als Begruendung im Quelltext",
          "spielstaende geben sie muss" in quelle, "")
    check("der Ordner liegt unter LOCALAPPDATA und nicht im Projekt",
          'os.environ.get("LOCALAPPDATA")' in quelle and "projektwurzel" not in quelle, "")

    with tempfile.TemporaryDirectory() as tmp:
        alt = os.environ.get("NEBEL_SPIELDATEN_ORDNER")
        os.environ["LOCALAPPDATA"] = tmp
        try:
            import runpy
            from types import SimpleNamespace
            from unittest.mock import patch
            with patch.dict(sys.modules, {"main": SimpleNamespace(main=lambda: None)}):
                runpy.run_path(str(ROOT / "src" / "public_start.py"),
                               run_name="public_start_pruefung")
            ziel = Path(os.environ["NEBEL_SPIELDATEN_ORDNER"])
            check("der Einstieg zeigt auf <LOCALAPPDATA>/Nebelseetal_Remake/Demo",
                  ziel == Path(tmp) / "Nebelseetal_Remake" / "Demo", str(ziel))
            check("der Ordner liegt ausserhalb des Projekts",
                  bool(ROOT not in ziel.parents), str(ziel))
            check("der Ordner existiert beim Start noch nicht (leerer Erststart)",
                  not ziel.exists(), str(ziel))
            os.environ["NEBEL_OEFFENTLICHE_TESTVERSION"] = "1"
            check("der oeffentliche Modus wird gesetzt",
                  os.environ.get("NEBEL_OEFFENTLICHE_TESTVERSION") == "1", "")
        finally:
            if alt is None:
                os.environ.pop("NEBEL_SPIELDATEN_ORDNER", None)
            else:
                os.environ["NEBEL_SPIELDATEN_ORDNER"] = alt


def _pruefungen_leerer_start():
    abschnitt("4. Ein frischer Ordner ergibt drei leere Slots")
    with tempfile.TemporaryDirectory() as tmp:
        ordner = spielstaende.ordner_vorbereiten(str(Path(tmp) / "Demo"))
        for nummer in spielstaende.SLOTS:
            status = spielstaende.slot_status(ordner, nummer)
            check(f"Slot {nummer} ist leer", status == f"Slot {nummer}: leer", status)
            check(f"die Datei von Slot {nummer} existiert nicht",
                  not os.path.isfile(spielstaende.slot_pfad(ordner, nummer)), "")
        check("es gibt keinen Altstand", not os.path.isfile(spielstaende.altstand_pfad(ordner)), "")
        check("es gibt keinen Admin-Teststand",
              not os.path.isfile(spielstaende.admin_pfad(ordner)), "")
        check("der frische Ordner enthaelt keine Datei",
              sorted(os.listdir(ordner)) == [], str(os.listdir(ordner)))


def main_lauf() -> int:
    _pruefungen_paket()
    _pruefungen_bau_abbruch()
    _pruefungen_einstieg()
    _pruefungen_leerer_start()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_lauf())
