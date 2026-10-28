"""Nur die Bedienoberflaeche fuer Admin-Testwerkzeuge.

Sicherheitsgrenze: Diese Datei authentifiziert NICHT. Der Hauptdialog muss
vor dem Aufruf das separate Admin-Passwort geprueft haben. Jede Mutation im
Kernmodul ``admin_werkzeuge`` prueft zusaetzlich Testmodus und Freigabe.

Keine Spielregeln, Werte oder Datenquellen werden hier dupliziert.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

import admin_werkzeuge


def oeffnen(parent, state, weltgebiete, *, speichern, aktualisieren):
    """Oeffnet die Admin-Konsole fuer einen bereits autorisierten Teststand.

    ``speichern`` sichert ausschliesslich nach dem Admin-Teststand-Pfad.
    ``aktualisieren`` zeichnet die Spieloberflaeche nach Aenderungen neu.
    """
    if not getattr(state, "admin_teststand", False) or not getattr(state, "oekonomie_aktiv", False):
        raise PermissionError("Admin-Werkzeuge nur im aktiven Admin-Teststand.")

    fenster = tk.Toplevel(parent)
    fenster.title("Nebelseetal - Admin-Testwerkzeuge")
    fenster.geometry("760x500")
    fenster.transient(parent)
    fenster.grab_set()
    body = ttk.Frame(fenster, padding=14)
    body.pack(fill="both", expand=True)
    ttk.Label(body, text="Admin-Testmodus: Testdaten, nicht fuer normale Spielstaende",
              font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 8))

    siedlungen = {f"{s.name} [{s.id}]": s.id for s in state.settlements}
    if not siedlungen:
        fenster.destroy()
        raise ValueError("Der Teststand hat keine Siedlung.")
    ort_text = tk.StringVar(value=next(iter(siedlungen)))
    ort_box = ttk.Frame(body)
    ort_box.pack(fill="x", pady=(0, 12))
    ttk.Label(ort_box, text="Siedlung:").pack(side="left")
    ttk.Combobox(ort_box, textvariable=ort_text, values=list(siedlungen),
                 state="readonly", width=55).pack(side="left", padx=10)

    def ort_id():
        return siedlungen[ort_text.get()]

    tabs = ttk.Notebook(body)
    tabs.pack(fill="both", expand=True)

    # Bestandsvergabe: Originalnamen kommen aus dem Regelmodul.
    lager = ttk.Frame(tabs, padding=12)
    tabs.add(lager, text="Rohstoffe / Waren / Einheiten")
    kategorie = tk.StringVar(value="Rohstoff")
    posten = tk.StringVar()
    menge = tk.StringVar(value="100")
    ttk.Label(lager, text="Kategorie").grid(row=0, column=0, sticky="w", pady=6)
    cb_art = ttk.Combobox(lager, state="readonly", textvariable=kategorie,
                          values=("Rohstoff", "Ware", "Einheit"), width=22)
    cb_art.grid(row=0, column=1, sticky="w", pady=6)
    ttk.Label(lager, text="Originalposten").grid(row=1, column=0, sticky="w", pady=6)
    cb_posten = ttk.Combobox(lager, state="readonly", textvariable=posten, width=34)
    cb_posten.grid(row=1, column=1, sticky="w", pady=6)
    ttk.Label(lager, text="Menge (1 - 1.000.000)").grid(row=2, column=0, sticky="w", pady=6)
    ttk.Entry(lager, textvariable=menge, width=17).grid(row=2, column=1, sticky="w", pady=6)

    def posten_auffuellen(*_):
        werte = admin_werkzeuge.verfuegbare_posten(kategorie.get())
        cb_posten.configure(values=werte)
        posten.set(werte[0] if werte else "")

    kategorie.trace_add("write", posten_auffuellen)
    posten_auffuellen()

    def anwenden(aktion, erfolg):
        try:
            aktion()
        except (ValueError, PermissionError, TypeError, KeyError) as exc:
            messagebox.showerror("Admin-Aktion abgelehnt", str(exc), parent=fenster)
            return
        # Die eigentliche Speicherung ist absichtlich manuell, damit Admins
        # mehrere Experimente ausfuehren und bei Bedarf verwerfen koennen.
        status.set(erfolg + " (noch nicht gespeichert)")
        aktualisieren()

    def geben():
        def aktion():
            admin_werkzeuge.geben(state, ort_id(), kategorie.get(), posten.get(),
                                  int(menge.get()), freigabe=True)
        anwenden(aktion, "Bestand im lokalen Lager zugeteilt")

    ttk.Button(lager, text="In dieses Dorflager geben", command=geben).grid(
        row=3, column=0, columnspan=2, sticky="w", pady=14)

    # Kartenwechsel mit Erhalt aller Bauten nur bei regelkonformer Neupositionierung.
    karten = ttk.Frame(tabs, padding=12)
    tabs.add(karten, text="Siedlungskarte")
    karte = tk.StringVar()
    ttk.Label(karten, text="Kartentyp").grid(row=0, column=0, sticky="w", pady=8)
    cb_karte = ttk.Combobox(karten, textvariable=karte, state="readonly", width=32)
    cb_karte.grid(row=0, column=1, sticky="w", pady=8)

    def karten_auffuellen(*_):
        werte = admin_werkzeuge.freie_karten(state, ort_id())
        cb_karte.configure(values=werte)
        karte.set(werte[0] if werte else "")

    ort_text.trace_add("write", karten_auffuellen)
    karten_auffuellen()

    def karte_setzen():
        def aktion():
            admin_werkzeuge.karte_waehlen(state, ort_id(), karte.get(), freigabe=True)
        anwenden(aktion, "Karte zugewiesen")
        karten_auffuellen()

    ttk.Button(karten, text="Karte zuweisen (Bauten erhalten)", command=karte_setzen).grid(
        row=1, column=0, columnspan=2, sticky="w", pady=8)
    ttk.Label(karten, text="Bereits anderen Doerfern zugewiesene Karten sind gesperrt.").grid(
        row=2, column=0, columnspan=2, sticky="w", pady=4)

    # Weltpositionen sind 0-basiert, Grenzen stehen in der Gebiets-Konfiguration.
    position = ttk.Frame(tabs, padding=12)
    tabs.add(position, text="Weltposition")
    gebiet = tk.StringVar(value=state.current_map)
    x = tk.StringVar(value="0")
    y = tk.StringVar(value="0")
    ttk.Label(position, text="Weltgebiet").grid(row=0, column=0, sticky="w", pady=6)
    ttk.Combobox(position, state="readonly", textvariable=gebiet,
                 values=[g["id"] for g in weltgebiete], width=28).grid(
                     row=0, column=1, sticky="w", pady=6)
    for row, name, variable in [(1, "X (ab 0)", x), (2, "Y (ab 0)", y)]:
        ttk.Label(position, text=name).grid(row=row, column=0, sticky="w", pady=6)
        ttk.Entry(position, textvariable=variable, width=12).grid(row=row, column=1, sticky="w", pady=6)

    def bewegen():
        def aktion():
            admin_werkzeuge.positionieren(state, ort_id(), gebiet.get(),
                                          int(x.get()), int(y.get()), weltgebiete,
                                          freigabe=True)
        anwenden(aktion, "Siedlung auf neues Weltfeld versetzt")

    ttk.Button(position, text="Siedlung positionieren", command=bewegen).grid(
        row=3, column=0, columnspan=2, sticky="w", pady=12)
    ttk.Label(position, text="Nur freie Landfelder; kein Entfernen fremder Siedlungen oder Bots.").grid(
        row=4, column=0, columnspan=2, sticky="w", pady=6)

    # FIX04d – Anzeigeoption im eigenen Teststand, kein Eingriff in Schutzfristen.
    anzeige = ttk.Frame(tabs, padding=12)
    tabs.add(anzeige, text="Spielerhilfe / Anzeige")
    ttk.Label(anzeige, text="Automatische Einstiegshilfe im Admin-Teststand",
              font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 8))
    hilfe_modus = tk.StringVar(value=getattr(state, "admin_hilfe_modus", "auto"))
    for wert, titel in (("auto", "Automatisch (wie beim normalen Spieler)"),
                        ("anzeigen", "Immer anzeigen – auch nach Götterschutz"),
                        ("ausblenden", "Ausblenden – auch während Götterschutz")):
        ttk.Radiobutton(anzeige, text=titel, variable=hilfe_modus,
                        value=wert).pack(anchor="w", pady=4)
    ttk.Label(anzeige, text="Nur die Anzeige wird geändert, nicht Götterschutz, Angriffsschutz oder Spielwerte.",
              wraplength=600).pack(anchor="w", pady=(8, 4))

    def hilfe_anwenden():
        anwenden(lambda: admin_werkzeuge.spielerhilfe_modus_setzen(
            state, hilfe_modus.get(), freigabe=True), "Admin-Spielerhilfe geändert")

    ttk.Button(anzeige, text="Anzeige-Einstellung übernehmen",
               command=hilfe_anwenden).pack(anchor="w", pady=(8, 0))

    fuss = ttk.Frame(body)
    fuss.pack(fill="x", pady=(12, 0))
    status = tk.StringVar(value="Aenderungen gelten nur fuer diesen Admin-Teststand.")
    ttk.Label(fuss, textvariable=status, wraplength=470).pack(side="left", fill="x", expand=True)

    def admin_sichern():
        try:
            ok = speichern()
        except Exception as exc:
            messagebox.showerror("Admin-Sicherung", str(exc), parent=fenster)
            return
        if ok:
            status.set("Admin-Teststand gespeichert (separate Datei).")
        else:
            messagebox.showerror("Admin-Sicherung", "Admin-Teststand konnte nicht gesichert werden.",
                                 parent=fenster)

    ttk.Button(fuss, text="Adminstand sichern", command=admin_sichern).pack(side="right", padx=3)
    ttk.Button(fuss, text="Schliessen", command=fenster.destroy).pack(side="right", padx=3)
    return fenster
