import pytest
import numpy as np
import main  # Importiert deine main.py
from main import Zufallsstrategie  # <-- KORREKTUR 1: Fehlender Import hinzugefügt

# --- Konstanten, die wir oft brauchen ---
LEER = "[ ]"
X = "[X]"
O = "[O]"

# --- 1. Tests für Gewinnerkennung ---

def test_gewinn_reihe_0_X_als_Spieler():
    # ARRANGE: Setze das Feld von Hand
    main.Spielfeld = np.array([
        [X, X, X],
        [O, O, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X" # Spieler ist X
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == True

def test_gewinn_reihe_1_O_als_Spieler():
    # ARRANGE
    main.Spielfeld = np.array([
        [X, X, LEER],
        [O, O, O],
        [LEER, LEER, X]
    ])
    main.symbol = "O" # Spieler ist O
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == True

def test_gewinn_spalte_0_X_als_CPU():
    # ARRANGE
    main.Spielfeld = np.array([
        [X, O, O],
        [X, LEER, LEER],
        [X, O, LEER]
    ])
    main.symbol = "O" # Spieler ist O, also ist CPU (X) der Gewinner
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == True

def test_gewinn_diagonale_1_O_als_CPU():
    # ARRANGE
    main.Spielfeld = np.array([
        [O, X, X],
        [LEER, O, X],
        [LEER, LEER, O]
    ])
    main.symbol = "X" # Spieler ist X, also ist CPU (O) der Gewinner
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == True

def test_kein_gewinn_bei_leerem_feld():
    # ARRANGE
    main.Spielfeld = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X"
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == False

def test_kein_gewinn_bei_fast_vollem_feld():
    # ARRANGE
    main.Spielfeld = np.array([
        [X, O, X],
        [O, O, X],
        [O, X, O]
    ])
    main.symbol = "X"
    
    # ACT & ASSERT
    assert main.gewinnPruefung() == False


# --- 2. Tests für ungültige Eingaben ---

def test_gueltiger_zug_mitte():
    assert main.ungültigerZugPruefung("1 1") == True

def test_gueltiger_zug_ecke():
    assert main.ungültigerZugPruefung("0 2") == True

def test_ungueltig_buchstaben():
    assert main.ungültigerZugPruefung("a b") == False

def test_ungueltig_falsche_zahl():
    assert main.ungültigerZugPruefung("9 9") == False

def test_ungueltig_negativ():
    assert main.ungültigerZugPruefung("-1 0") == False
    
def test_ungueltig_falsches_format():
    assert main.ungültigerZugPruefung("1 1 1") == False

def test_ungueltig_nur_eine_zahl():
    assert main.ungültigerZugPruefung("2") == False

def test_ungueltig_leer():
    assert main.ungültigerZugPruefung("") == False


# --- 5. Tests für die Zufallsstrategie ---
# KORREKTUR 2: Diese Funktionen sind jetzt NICHT mehr eingerückt

def test_zufall_waehlt_letztes_freies_feld():
    """
    Test 1: Prüft, ob das *letzte* legale Feld korrekt gewählt wird.
    Hier gibt es keinen Zufall, die KI MUSS (1, 2) wählen.
    """
    # ARRANGE: Erstelle ein Feld, das fast voll ist
    fast_volles_brett = np.array([
        [X, O, X],
        [O, X, LEER], # <--- Einziges freies Feld
        [X, O, O]
    ])
    
    # Setze das globale Feld und das Symbol (Spieler=X, CPU=O)
    main.Spielfeld = fast_volles_brett
    main.symbol = "X"
    
    strategie = Zufallsstrategie()
    
    # ACT: Führe den Zug aus
    strategie.wähle_zug()
    
    # ASSERT:
    # 1. Wurde das *eine* freie Feld (1, 2) mit 'O' gefüllt?
    assert main.Spielfeld[1, 2] == O
    
    # 2. Zähle, ob jetzt wirklich KEINE Felder mehr leer sind
    anzahl_leere_felder = np.count_nonzero(main.Spielfeld == LEER)
    assert anzahl_leere_felder == 0

def test_zufall_mit_seed_waehlt_vorhersehbares_feld():
    """
    Test 2 (Vorschlag 1): 
    Wir setzen einen 'Seed', damit der Zufall reproduzierbar wird.
    """
    # ARRANGE:
    # Setze den Zufalls-Seed. "42" ist eine beliebte Zahl dafür.
    # Das sorgt dafür, dass 'np.random.choice' immer dieselbe "zufällige" Zahl wählt.
    main.np.random.seed(42)
    
    
    

    # Erstelle ein Feld mit 3 freien Feldern: (0,0), (1,1), (2,2)
    brett = np.array([
        [LEER, X, O],
        [X, LEER, O],
        [O, X, LEER]
    ])
    main.Spielfeld = brett
    main.symbol = "X" # Spieler=X, CPU=O

    # Wenn dein Code die freien Felder (0,0), (1,1), (2,2) findet
    # und 'np.random.choice(3)' mit Seed 42 aufruft,
    # wird er (auf den meisten Systemen) Index 0 wählen.
    # Index 0 entspricht dem Feld (0, 0).
    
    strategie = Zufallsstrategie()

    # ACT:
    strategie.wähle_zug()
    
    # ASSERT:
    # Wir wetten darauf, dass der Seed 42 das Feld (0, 0) ausgewählt hat.
    assert main.Spielfeld[2, 2] == O
    
    # Stelle sicher, dass die anderen freien Felder NICHT gefüllt wurden
    assert main.Spielfeld[0, 0] == LEER
    assert main.Spielfeld[1, 1] == LEER

def test_zufall_macht_ueberhaupt_einen_zug():
    """
    Test 3 (Vorschlag 3):
    Wir prüfen nur, ob *irgendein* Feld gesetzt wurde.
    """
    # ARRANGE:
    # Nimm ein leeres Brett (dafür müssen wir es manuell zurücksetzen,
    # da wir keine "Fixtures" verwenden)
    main.Spielfeld = np.array([
        [LEER, LEER, LEER],
        [LEER, LEER, LEER],
        [LEER, LEER, LEER]
    ])
    main.symbol = "X" # CPU ist O
    
    strategie = Zufallsstrategie()

    # ACT:
    strategie.wähle_zug()
    
    # ASSERT:
    # Zähle die 'O'-Symbole. Es muss genau eines sein.
    anzahl_o = np.count_nonzero(main.Spielfeld == O)
    assert anzahl_o == 1
    
    # Zähle die leeren Felder. Es müssen genau 8 sein.
    anzahl_leer = np.count_nonzero(main.Spielfeld == LEER)
    assert anzahl_leer == 8