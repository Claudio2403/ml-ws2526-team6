import pytest
from main import gewinnPruefung
import numpy as np
import main

LEER = "[ ]"
SPIELER_X = "[X]"
SPIELER_O = "[O]"
CPU_O = "[O]"
CPU_X = "[X]"

main.symbol = "X"
main.Spielfeld = np.array([[LEER, LEER, LEER],
                           [SPIELER_X, SPIELER_X, SPIELER_X],
                            [LEER, LEER, LEER]])
ergebnis = gewinnPruefung()

assert ergebnis == True