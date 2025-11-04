import numpy as np
import Aufgabe_2 as main



# --- Hilfsklassen für Spieler-Start und CPU-Start ---

class IntelligenteStrategie_AlsSpieler(main.IntelligenteStrategie):
    """Intelligente KI spielt als Spieler (X)."""
    def wähle_zug(self):
        main.symbol = "X"  # Spieler ist X
        super().wähle_zug()

class ZufallsStrategie_AlsSpieler(main.Zufallsstrategie):
    """Zufallsstrategie spielt als Spieler (X)."""
    def wähle_zug(self):
        main.symbol = "X"
        super().wähle_zug()


# --- Testsimulation ---

def test_simulation_ki_vs_ki_statistik(capsys):
    """
    Simulation von 100 Spielen zwischen Intelligenz und Zufallsstrategie.
    Das Startrecht (X) wechselt bei jedem Spiel.
    """
    LEER = "[ ]"
    anzahl_spiele = 50

    leeres_brett = np.array([[LEER, LEER, LEER],
                             [LEER, LEER, LEER],
                             [LEER, LEER, LEER]])

    ergebnisse = {"intelligenz": 0, "zufall": 0, "unentschieden": 0}
    details = []

    with capsys.disabled():
        print(f"\nStarte {anzahl_spiele} Spiele mit abwechselndem Startrecht...\n")

    for i in range(anzahl_spiele):
        main.Spielfeld = np.copy(leeres_brett)
        gewinner = None

        # --- Startrecht wechseln ---
        if i % 2 == 0:
            # Intelligente KI startet
            starter = IntelligenteStrategie_AlsSpieler()
            gegner = main.Zufallsstrategie()
            starter_name = "Intelligenz (X)"
            gegner_name = "Zufall (O)"
        else:
            # Zufallsstrategie startet
            starter = ZufallsStrategie_AlsSpieler()
            gegner = main.IntelligenteStrategie()
            starter_name = "Zufall (X)"
            gegner_name = "Intelligenz (O)"

        with capsys.disabled():
            print(f"Spiel {i+1:03d}: Starter = {starter_name}")

        # --- Spielablauf ---
        for _ in range(5):  # maximal 5 Spielrunden
            # Spieler (X)
            main.symbol = "X"
            starter.wähle_zug()
            if main.gewinnPruefung():
                gewinner = starter_name
                break
            if LEER not in main.Spielfeld:
                break

            # CPU (O)
            main.symbol = "O"
            gegner.wähle_zug()
            if main.gewinnPruefung():
                gewinner = gegner_name
                break
            if LEER not in main.Spielfeld:
                break

        # --- Ergebnis ---
        if gewinner:
            if "Intelligenz" in gewinner:
                ergebnisse["intelligenz"] += 1
                details.append(f"Spiel {i+1:03d}: Intelligenz gewinnt ({gewinner})")
            else:
                ergebnisse["zufall"] += 1
                details.append(f"Spiel {i+1:03d}: Zufall gewinnt ({gewinner})")
        else:
            ergebnisse["unentschieden"] += 1
            details.append(f"Spiel {i+1:03d}: Unentschieden")

    # --- Statistik ausgeben ---
    gesamt = sum(ergebnisse.values())
    with capsys.disabled():
        print("\n--- Detaillierte Ergebnisse ---")
        for e in details:
            print(e)

        print("\n--- Gesamtstatistik ---")
        print(f"Intelligente Strategie gewinnt: {ergebnisse['intelligenz']} ({ergebnisse['intelligenz']/gesamt*100:.1f}%)")
        print(f"Zufallsstrategie gewinnt:      {ergebnisse['zufall']} ({ergebnisse['zufall']/gesamt*100:.1f}%)")
        print(f"Unentschieden:                 {ergebnisse['unentschieden']} ({ergebnisse['unentschieden']/gesamt*100:.1f}%)")

    # Test soll nie fehlschlagen
    assert True
