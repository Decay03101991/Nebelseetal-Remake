"""FIX04c – Spielerhilfe während des Götterschutzes, jederzeit aufrufbar.

Nur Präsentation/Orientierung, KEINE Spielmechanik. Der einzige maßgebliche
Schutzstatus ist GameState.noob_protection. Daten zu Baueignung/-ertrag kommen
weiterhin aus gelaende/baumenue_info, Fragen aus dem bestehenden berater.
"""
from __future__ import annotations

import berater
import wirtschaft

# Bewusst nur Themen, die das gegenwärtige Spiel tatsächlich anbietet.
# Nicht fertig entwickelte Funktionen nicht als abgeschlossen versprechen.
FRAGEN = (
    "Wie fange ich an?",
    "Wie baue ich ressourcenschonend?",
    "Warum kann ich hier nicht bauen?",
    "Wofür brauche ich eine Bibliothek?",
    "Wie funktioniert Forschung?",
    "Was bedeutet Götterschutz?",
    "Wie funktionieren Ortslager?",
    "Wie bilde ich Einheiten aus?",
    "Wie speichere und lade ich?",
    "Wie läuft ein Kampf ab?",
)


def schutz_aktiv(zustand) -> bool:
    """Ausschließlich das bestehende, gespeicherte Schutzmerkmal verwenden.

    Der Regelkern beendet den Schutz nach sieben Spieltagen oder durch einen
    ersten Kriegspunkt; weder GUI noch Hilfe rechnen eine zweite Frist aus.
    """
    return bool(getattr(zustand, "noob_protection", False))


# FIX04d: Nur der authentifizierte Admin-Teststand darf die Anzeige übersteuern.
# Die Einstellung veraendert weder Schutzfristen noch Kampfregeln.
ADMIN_HILFE_MODI = ("auto", "anzeigen", "ausblenden")


def hilfe_sichtbar(zustand, *, admin_freigabe=False) -> bool:
    """Sichtbarkeit der begleitenden Hilfe, niemals Wirkung des Götterschutzes."""
    if admin_freigabe and getattr(zustand, "admin_teststand", False):
        modus = getattr(zustand, "admin_hilfe_modus", "auto")
        if modus == "anzeigen":
            return True
        if modus == "ausblenden":
            return False
    return schutz_aktiv(zustand)


def grundproduktion_erste_siedlung(zustand) -> dict:
    """Gebaeudeertrag der ersten Siedlung, OHNE passives Grundeinkommen.

    Eine blosse Startgutschrift oder die automatische Grundrate von 1 Holz/Stein/h
    ist kein aufgebauter Rohstoffbetrieb. Entsprechend dem bestehenden
    Wirtschaftsregelkern wird nur tatsaechlicher Ertrag von bebauten Kartenfeldern
    betrachtet. Keine Mutation am Spielstand; auch nach Laden neu berechenbar.
    """
    orte = getattr(zustand, "settlements", None) or ()
    if not orte:
        return {r: 0.0 for r in ("holz", "stein", "nahrung")}
    produktion = wirtschaft.siedlung_ertrag(orte[0])
    normiert = {str(k).lower(): float(v) for k, v in produktion.items()
                if isinstance(v, (int, float))}
    return {r: normiert.get(r, 0.0) for r in ("holz", "stein", "nahrung")}


def startaufgabe_pflicht(zustand) -> bool:
    """Onboarding zwingend bis ERSTE Siedlung und alle drei Produzenten laufen.

    Beabsichtigt unabhaengig von Götterschutz und Admin-Anzeigemodus.
    Die rechte allgemeine Einstiegshilfe bleibt separat schaltbar.
    """
    if not (getattr(zustand, "settlements", None) or ()):
        return True
    return any(rate <= 0 for rate in grundproduktion_erste_siedlung(zustand).values())


def admin_hilfe_modus_text(zustand, *, admin_freigabe=False) -> str:
    """Sichtbar machen, ob die Admin-Anzeige von der Spielregel abweicht."""
    if not (admin_freigabe and getattr(zustand, "admin_teststand", False)):
        return ""
    modus = getattr(zustand, "admin_hilfe_modus", "auto")
    return {"anzeigen": "Admin-Test: Einstiegshilfe erzwungen eingeblendet.",
            "ausblenden": "Admin-Test: Einstiegshilfe manuell ausgeblendet.",
            "auto": "Admin-Test: Einstiegshilfe folgt dem Götterschutz."}.get(modus, "")


def naechster_schritt(zustand) -> str:
    """Kurzer, nicht-mutierender Einstieg, passend zum tatsächlichen Spielstand."""
    orte = getattr(zustand, "settlements", ()) or ()
    if not orte:
        return "Gründe im Dorfzentrum deine erste Siedlung und öffne ihre Originalkarte."
    for ort in orte:
        karte = getattr(ort, "karte", None) or {}
        raster = karte.get("raster") or []
        gebaut = set((getattr(ort, "bauten", None) or {}).values())
        if not raster:
            return "Wähle für deine Siedlung eine Originalkarte aus."
        for kennung, gelaendeart, hinweis in (
            ("holzfaeller", "wald", "Baue einen Holzfäller auf Wald für Holzproduktion."),
            ("steinmetz", "berg", "Baue einen Steinmetz auf Berg für Steinproduktion."),
            ("farm", "grasland", "Baue eine Farm auf Grasland für Nahrung."),
        ):
            if kennung not in gebaut and gelaendeart in raster:
                return hinweis + " Prüfe zuerst den Ortslagerbestand."
    return ("Sichere die Grundversorgung. Danach helfen Bibliothek/Forschung, "
            "Haus und Werkstätten beim Ausbau.")


def kurzinfo(zustand, *, admin_freigabe=False) -> str:
    """Text der Seitenleiste; Admin-Darstellung nie als echten Schutz ausgeben."""
    tag = getattr(zustand, "day", "?")
    schutz = schutz_aktiv(zustand)
    kopf = (f"Götterschutz aktiv · Tag {tag}\n" if schutz else
            f"Götterschutz beendet · Tag {tag}\n")
    zusatz = ("Admin-Testanzeige: unabhängig vom Schutzstatus.\n" if
              admin_freigabe and getattr(zustand, "admin_teststand", False) and
              getattr(zustand, "admin_hilfe_modus", "auto") == "anzeigen" else "")
    return (kopf + zusatz + "Der Schutz endet nach sieben Spieltagen oder früher mit dem "
            "ersten Kriegspunkt.\n\n"
            f"Nächster Schritt: {naechster_schritt(zustand)}\n\n"
            "Bautipp: Rohstoffgebäude auf ertragreiche Felder setzen; "
            "Bibliothek und andere Funktionsgebäude nach Möglichkeit "
            "auf freie Steppe. Sümpfe sind nicht bebaubar.")


def antwort(frage: str, zustand=None) -> str:
    """Kurze Antworten auf die vorgefertigten Fragen; Detailauskunft bleibt bei berater."""
    if frage == "Wie baue ich ressourcenschonend?":
        return ("Nutze die Ertragsangabe im Baumenü für das angeklickte Originalfeld. "
                "Holzfäller liefern auf Wald besonders viel Holz, Steinmetze auf Berg "
                "besonders viel Stein und Farmen auf Grasland besonders viel Nahrung. "
                "Funktionsgebäude (etwa Bibliotheken) nach Möglichkeit auf freie Steppe "
                "setzen, damit ertragreiche Flächen verfügbar bleiben. "
                "Die Steppe kann selbst Rohstoffe liefern; prüfe daher die konkrete Karte. "
                "Sumpf bleibt unbebaubar.")
    if frage == "Warum kann ich hier nicht bauen?":
        return ("Wähle ein Feld auf der Originalkarte. Das Baumenü zeigt die passenden "
                "Gebäude nach Kategorie, fehlende Rohstoffe aus dem Ortslager "
                "und noch nicht erforschte Voraussetzungen. Ein belegtes Feld "
                "ist nicht erneut bebaubar; Sümpfe sind unbebaubar. "
                "Dorfwälle belegen kein Kartenfeld.")
    if frage == "Was bedeutet Götterschutz?":
        status = ("Aktuell aktiv." if zustand is not None and schutz_aktiv(zustand)
                  else "Aktuell nicht aktiv oder ohne Spielstand nicht bestimmbar.")
        return ("Der Götterschutz schützt neue Spieler vor Angriffen. "
                "Im Regelkern endet er nach sieben Spieltagen oder früher durch den "
                "ersten Kriegspunkt. Die begleitende Seitenhilfe verschwindet "
                "dann automatisch; über 'Spielerhilfe' bleibt diese Auskunft erhalten. "
                "Im getrennten Admin-Teststand darf nur die Anzeige übersteuert werden, "
                "nicht der tatsächliche Schutz. "
                + status)
    if frage == "Wie funktionieren Ortslager?":
        return ("Jede Siedlung hat ein eigenes Ortslager. Gebäude bezahlen ihre Kosten "
                "aus dem Ortslager der ausgewählten Siedlung; die Rohstoffleiste "
                "oben zeigt nur die Summe des Reichs. Für Transporte und Handel "
                "die jeweils betroffenen Orte beachten.")
    if frage == "Wie bilde ich Einheiten aus?":
        return ("Baue zuerst die erforderlichen Gebäude und schalte notwendige "
                "Forschungen frei. Die Ausbildung benötigt Siedler, Rohstoffe, "
                "gegebenenfalls Ausrüstung und Spielzeit. "
                "Beispiel: Die Kriegerakademie erfordert Baukunst Stufe 1. "
                "Prüfe die angegebenen Voraussetzungen im Bau- und Kasernenmenü.")
    if frage == "Wie speichere und lade ich?":
        return ("Oben im Spiel auf 'Speichern' oder 'Laden' klicken. "
                "Im normalen Spiel stehen drei Spielerslots bereit. "
                "Im Menü 'Spielstände' kannst du Slots verwalten: "
                "Löschen verschiebt sie datiert ins private Archiv, "
                "Wiederherstellen holt Archivstände zurück. "
                "Bewusstes Überschreiben ersetzt den gewählten Slot; "
                "der Admin-Teststand bleibt getrennt.")
    return berater.antwort(frage, zustand)
