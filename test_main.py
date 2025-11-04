import pytest
import numpy as np
import Aufgabe_1   
import Aufgabe_2 as main
from Aufgabe_2 import Zufallsstrategie  
from Aufgabe_2 import IntelligenteStrategie

# kurz: Symbole, damit ich nicht jedes Mal tippen muss
LEER = "[ ]"
X = "[X]"
O = "[O]"

# check: Reihe 0 sollte X gewinnen
def test_gewinn_reihe_0_X_als_Spieler():
    # bau das Brett so auf, wie ich's will
    main.Spielfeld = np.array([
        [X, X, X],
        [O, O, LEER],
        [LEER, LEER, LEER]
    ])
    # setze den Spieler
    main.symbol = "X"
    # erwartung: Gewinn erkannt
    assert main.gewinnPruefung() == True

# check: Reihe 1 sollte O gewinnen
def test_gewinn_reihe_1_O_als_Spieler():
    # schnelles Setup fürs Brett
    main.Spielfeld = np.array([
        [X, X, LEER],
        [O, O, O],
        [LEER, LEER, X]
    ])
    # O ist am Zug (als Spieler)
    main.symbol = "O"
    # sollte Gewinn melden
    assert main.gewinnPruefung() == True

# check: Spalte 0 -> X gewinnt (CPU)
def test_gewinn_spalte_0_X_als_CPU():
    # Feld so, dass X die Spalte voll macht
    main.Spielfeld = np.array([
        [X, O, O],
        [X, LEER, LEER],
        [X, O, LEER]
    ])
    # Spieler ist O, also CPU (X) gewinnt
    main.symbol = "O"
    assert main.gewinnPruefung() == True

# check: Diagonale (O gewinnt)
def test_gewinn_diagonale_1_O_als_CPU():
    # Diagonale vorbereiten
    main.Spielfeld = np.array([
        [O, X, X],
        [LEER, O, X],
        [LEER, LEER, O]
    ])
    # Spieler X, CPU O gewinnt
    main.symbol = "X"
    assert main.gewinnPruefung() == True

# check: leeres Feld -> kein Gewinn
def test_kein_gewinn_bei_leerem_feld():
    # alles leer
    main.Spielfeld = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X"
    # kein Gewinner
    assert main.gewinnPruefung() == False

# check: volles Feld ohne Gewinner
def test_kein_gewinn_bei_fast_vollem_feld():
    # fast volles Feld (Unentschieden)
    main.Spielfeld = np.array([
        [X, O, X],
        [O, O, X],
        [O, X, O]
    ])
    main.symbol = "X"
    assert main.gewinnPruefung() == False

# Input-Validation Tests
def test_gueltiger_zug_mitte():
    # gültige Koordinaten
    assert main.ungültigerZugPruefung("1 1") == True

def test_gueltiger_zug_ecke():
    # Ecke ist gültig
    assert main.ungültigerZugPruefung("0 2") == True

def test_ungueltig_buchstaben():
    # Buchstaben sind falsch
    assert main.ungültigerZugPruefung("a b") == False

def test_ungueltig_falsche_zahl():
    # außerhalb des Boards
    assert main.ungültigerZugPruefung("9 9") == False

def test_ungueltig_negativ():
    # negative Zahlen sind ungültig
    assert main.ungültigerZugPruefung("-1 0") == False

def test_ungueltig_falsches_format():
    # zu viele Werte
    assert main.ungültigerZugPruefung("1 1 1") == False

def test_ungueltig_nur_eine_zahl():
    # nur eine Zahl -> falsch
    assert main.ungültigerZugPruefung("2") == False

def test_ungueltig_leer():
    # leere Eingabe -> falsch
    assert main.ungültigerZugPruefung("") == False



# Tests für die Zufalls-KI
def test_zufall_waehlt_letztes_freies_feld():
    # mach ein fast volles Brett, nur ein Feld frei
    fast_volles_brett = np.array([
        [X, O, X],
        [O, X, LEER],
        [X, O, O]
    ])
    main.Spielfeld = fast_volles_brett
    main.symbol = "X"
    strategie = Zufallsstrategie()
    # KI zieht
    strategie.wähle_zug()
    # sollte das einzige freie Feld füllen
    assert main.Spielfeld[1, 2] == O
    anzahl_leere_felder = np.count_nonzero(main.Spielfeld == LEER)
    assert anzahl_leere_felder == 0

def test_zufall_mit_seed_waehlt_vorhersehbares_feld():
    # seed setzen, damit's reproduzierbar ist
    main.np.random.seed(42)
    # drei freie Felder
    brett = np.array([
        [LEER, X, O],
        [X, LEER, O],
        [O, X, LEER]
    ])
    main.Spielfeld = brett
    main.symbol = "X"
    strategie = Zufallsstrategie()
    # ziehen lassen
    strategie.wähle_zug()
    # wir erwarten das eine bestimmte freie Ecke gesetzt wird
    assert main.Spielfeld[2, 2] == O
    assert main.Spielfeld[0, 0] == LEER
    assert main.Spielfeld[1, 1] == LEER

def test_zufall_macht_ueberhaupt_einen_zug():
    # komplett leeres Brett, KI soll ein Feld setzen
    main.Spielfeld = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X"
    strategie = Zufallsstrategie()
    strategie.wähle_zug()
    # genau ein O gesetzt
    anzahl_o = np.count_nonzero(main.Spielfeld == O)
    assert anzahl_o == 1
    anzahl_leer = np.count_nonzero(main.Spielfeld == LEER)
    assert anzahl_leer == 8

# Tests für die clevere KI
def test_intelligenz_prioritaet_1_gewinnt_selbst():
    # CPU kann direkt gewinnen -> soll das machen
    main.Spielfeld = np.array([
        [O, O, LEER],
        [X, X, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X"
    strategie = IntelligenteStrategie()
    strategie.wähle_zug()
    assert main.Spielfeld[0, 2] == O

def test_intelligenz_prioritaet_2_blockiert_gegner():
    # Spieler droht zu gewinnen, CPU soll blocken
    main.Spielfeld = np.array([
        [O, LEER, LEER],
        [X, X, LEER],
        [O, LEER, LEER]
    ])
    main.symbol = "X"
    strategie = IntelligenteStrategie()
    strategie.wähle_zug()
    assert main.Spielfeld[1, 2] == O

def test_intelligenz_prioritaet_3_nimmt_mitte_bei_leerem_feld():
    # Anfang des Spiels -> CPU nimmt Mitte
    main.Spielfeld = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X"
    strategie = IntelligenteStrategie()
    strategie.wähle_zug()
    assert main.Spielfeld[1, 1] == O

def test_intelligenz_prioritaet_4_nimmt_seite_wenn_mitte_belegt():
    # random-seed für deterministische Seitenwahl
    main.random.seed(42)
    # Mitte ist belegt, Seiten sind noch frei
    main.Spielfeld = np.array([
        [X, LEER, LEER],
        [LEER, O, LEER],
        [LEER, LEER, X]
    ])
    main.symbol = "X"
    strategie = IntelligenteStrategie()
    strategie.wähle_zug()
    # erwarte eine Seite (nach Seed) gesetzt
    assert main.Spielfeld[2, 1] == O

def test_intelligenz_prioritaet_5_nimmt_ecke_als_letztes():
    # nochmal Seed setzen, damit Test stabil ist
    main.random.seed(1)
    # nur Ecken sind frei
    main.Spielfeld = np.array([
        [LEER, O, LEER],
        [X, O, X],
        [LEER, X, LEER]
    ])
    main.symbol = "X"
    strategie = IntelligenteStrategie()
    strategie.wähle_zug()
    assert main.Spielfeld[2, 2] == O

# simpler Zufallsspieler für die Simulation
class ZufallsStrategie_AlsSpieler(main.Strategie):
    # spielt zufällig als X
    def wähle_zug(self):
        freie_felder = np.argwhere(main.Spielfeld == LEER)
        if len(freie_felder) > 0:
            cpu_zug = freie_felder[main.np.random.choice(len(freie_felder))]
            if main.symbol == "X":
                main.Spielfeld[cpu_zug[0], cpu_zug[1]] = X
            else:
                main.Spielfeld[cpu_zug[0], cpu_zug[1]] = O

# kurze KI-vs-KI Simulation, damit man sieht, wie oft CPU gewinnt
def test_simulation_ki_vs_ki_statistik(capsys):
    ki_spieler_zufall = ZufallsStrategie_AlsSpieler()
    ki_cpu_intelligenz = IntelligenteStrategie()
    leeres_brett = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    print("\nStarte 50 zufällige Simulations-Spiele...")
    ergebnisse = {"cpu_gewinnt": 0, "unentschieden": 0, "cpu_verliert (Spieler gewinnt)": 0}
    for i in range(50):
        main.Spielfeld = np.copy(leeres_brett)
        main.symbol = "X"
        spiel_ausgabe = ""
        for zug_nummer in range(5):
            ki_spieler_zufall.wähle_zug()
            if main.gewinnPruefung():
                break
            if LEER not in main.Spielfeld:
                break
            ki_cpu_intelligenz.wähle_zug()
            if main.gewinnPruefung():
                break
            if LEER not in main.Spielfeld:
                break
        captured = capsys.readouterr()
        spiel_ausgabe = captured.out
        if "Glückwunsch! Du hast gewonnen!" in spiel_ausgabe:
            ergebnisse["cpu_verliert (Spieler gewinnt)"] += 1
        elif "Die CPU hat gewonnen!" in spiel_ausgabe:
            ergebnisse["cpu_gewinnt"] += 1
        else:
            ergebnisse["unentschieden"] += 1
    print(f"50 Spiele fertig. Statistik: {ergebnisse}")
    assert True