import numpy as np
import random

class Strategie:
     def wähle_zug(self, spielfeld: np.matrix, cpu_symbol: str) -> tuple:
          raise NotImplementedError("Methode muss noch in Unterklasse implementiert werden")
     
class Zufallsstrategie(Strategie):
    def wähle_zug(self, spielfeld: np.matrix, cpu_symbol: str) -> tuple:
         freie_felder_indices = np.where(spielfeld == "[ ]")
         if len(freie_felder_indices[0] == 0):
              return None
         cpu_zug_index = random.choice(range(freie_felder_indices[0]))
         cpu_zug = (freie_felder_indices[0][cpu_zug_index],freie_felder_indices[1][cpu_zug_index])
         return cpu_zug
    
class IntelligenteStrategie(Strategie):
     #Das hier muss noch bearbeitet werden
     def wähle_zug(self, spielfeld, cpu_symbol):
          return super().wähle_zug(spielfeld, cpu_symbol)

def symbolwahl():
        global symbol

        print("Wähle ein Symbol: X oder O")
        symbol = input()
        if symbol == "X" or symbol == "x":
            symbol = "X"
            print("Du hast X gewählt. Du bist Spieler 1.")
            print("Die CPU ist O.")
            print(" ")
        elif symbol == "O" or symbol == "o" or symbol == "0":
            symbol = "O"
            print("Du hast O gewählt. Du bist Spieler 2.")
            print("Die CPU ist X.")
        else:
            print("Ungültige Eingabe.")
            symbolwahl()

def spielzugSpieler():
        global freie_felder
        global zug_index

        freie_felder = np.where((Spielfeld != "X") & (Spielfeld != "O"))
        zug_index = np.where(Spielfeld[zug].split() == "[ ]")
        if symbol == "X":
            Spielfeld[zug_index] = "X"
        else:
            Spielfeld[zug_index] = "O"

def spielzugComputer():
        freie_felder = np.where((Spielfeld != "X") & (Spielfeld != "O"))
        cpu_zug_index = np.random.choice(len(freie_felder[0]))
        cpu_zug = (freie_felder[0][cpu_zug_index], freie_felder[1][cpu_zug_index])
        if symbol == "X":
            Spielfeld[cpu_zug] = "O"
        else:
            Spielfeld[cpu_zug] = "X"
    
def unentschiedenPruefung():
        freie_felder = np.where((Spielfeld != "X") & (Spielfeld != "O"))
        if len(freie_felder[0]) == 0:
            print("Unentschieden! Das Spielfeld ist voll.")
            exit()

def gewinnPruefung():
    kombinationen = [
    
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
    ]

    for kombi in kombinationen:
        a, b, c = kombi
        if Spielfeld[a] == Spielfeld[b] == Spielfeld[c] and Spielfeld[a] != " ":
            gewinner = Spielfeld[a]
            if gewinner == symbol:
                print("Glückwunsch! Du has0t gewonnen!")
            else:
                print("Die CPU hat gewonnen!")
            return True

    return False
       



Spielfeld = np.matrix([["[ ]", "[ ]", "[ ]"],
                        ["[ ]", "[ ]", "[ ]"],
                        ["[ ]", "[ ]", "[ ]"]])


print("Willkommen bei deinem Tic Tac Toe Spiel!")
print("Das Spielfeld ist wie folgt aufgebaut:")
print(Spielfeld)
symbolwahl()
print("Let's Go!")
if symbol == "O":
    print("Die CPU ist am Zug...")
    spielzugComputer()
    print(Spielfeld)
    print(" ")
else:
    print("Du bist am Zug! Wähle ein Feld, indem du die Koordinaten eingibst (z.B. 1 1 für die obere linke Ecke).")
    print(" ")

while True:
    zug = input()
    if zug not in ["0 0", "0 1", "0 2", "1 0", "1 1", "1 2", "2 0", "2 1", "2 2"]:
        print("Ungültige Eingabe. Bitte gib die Koordinaten im Format 'Zeile Spalte' ein (z.B. 1 1).")
        continue
    else:
        spielzugSpieler()
        spielzugComputer()
        print(Spielfeld)
        if gewinnPruefung():
            break
        unentschiedenPruefung()
    print(" ")
exit()
