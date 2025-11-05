import numpy as np
import random

# --- (1) KLASSEN-DEFINITIONEN ---

class Strategie:
     def wähle_zug(self):
         raise NotImplementedError("Methode muss noch in Unterklasse implementiert werden")
     
class Zufallsstrategie(Strategie):
    def wähle_zug(self):
         freie_felder = np.argwhere(Spielfeld == "[ ]")
         if len(freie_felder) > 0:
             cpu_zug = freie_felder[np.random.choice(len(freie_felder))]
             if symbol == "X":
                 Spielfeld[cpu_zug[0], cpu_zug[1]] = "[O]"
             else:
                 Spielfeld[cpu_zug[0], cpu_zug[1]] = "[X]"
     
class IntelligenteStrategie(Strategie):
    def siegesZugPruefung(self, symbol):
        kombinationen = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        for kombi in kombinationen:
            a, b, c = kombi
            if (Spielfeld[a] == Spielfeld[b] and Spielfeld[c] == "[ ]") and Spielfeld[a] == symbol:
                return c

            elif (Spielfeld[a] == Spielfeld[c] and Spielfeld[b] == "[ ]") and Spielfeld[a] == symbol:
                return b

            elif (Spielfeld[b] == Spielfeld[c] and Spielfeld[a] == "[ ]") and Spielfeld[b] == symbol:
                return a
        
        return None

    def wähle_zug(self):
        if symbol == "X":
            cpuSymbol = "[O]"
            spielerSymbol = "[X]"
        else:
            cpuSymbol = "[X]"
            spielerSymbol = "[O]"
    
        #Eigenen Sieg versvollständigen
        zug = self.siegesZugPruefung(cpuSymbol)
        if zug != None:
            Spielfeld[zug[0],zug[1]] = cpuSymbol
            return
    
        #Gegnerischen Sieg blockieren
        zug = self.siegesZugPruefung(spielerSymbol)
        if zug != None:
            Spielfeld[zug[0],zug[1]] = cpuSymbol
            return
    
        #Zug ins Zentrum
        mitte = (1, 1)
        if Spielfeld[mitte] == "[ ]":
            Spielfeld[mitte] = cpuSymbol
            return
    
        #Zufällige Seite auswählen
        seiten = [(0, 1), (1, 0), (2, 1), (1, 2)]
        random.shuffle(seiten)
        for x, y in seiten:
            if Spielfeld[x, y] == "[ ]":
                Spielfeld[x, y] = cpuSymbol
                return
            
        #Zufällige Ecke auswählen
        ecken = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(ecken)
        for x, y in ecken:
            if Spielfeld[x, y] == "[ ]":
                Spielfeld[x, y] = cpuSymbol
                return
            

# --- (2) FUNKTIONS-DEFINITIONEN ---

def symbolwahl():
    global symbol

    print("Wähle ein Symbol: X oder O")
    symbol_input = input().strip().upper()
    if symbol_input == "X" or symbol_input == "x":
        symbol = "X"
        print("Du hast X gewählt. Du bist Spieler 1.")
        print("Die CPU ist O.")
        print(" ")
    elif symbol_input == "O" or symbol_input == "o" or symbol_input == "0":
        symbol = "O"
        print("Du hast O gewählt. Du bist Spieler 2.")
        print("Die CPU ist X.")
    else:
        print("Ungültige Eingabe. Bitte wähle X oder O.")
        symbolwahl()

def ungültigerZugPruefung(zug):
    if len(zug.split()) != 2:
        print("Ungültige Eingabe. Bitte gib die Koordinaten im Format 'Zeile Spalte' ein.")
        return False

    zeile, spalte = zug.split()
    if not zeile.isdigit() or not spalte.isdigit():
        print("Ungültige Eingabe. Die Koordinaten müssen Zahlen sein.")
        return False

    zeile, spalte = int(zeile), int(spalte)
    if 0 <= zeile <= 2 and 0 <= spalte <= 2:
        return True
    else:
        print("Ungültige Eingabe. Die Koordinaten müssen zwischen 0 und 2 liegen.")
        return False

def spielzugSpieler():
    global Spielfeld
    while True:
        zug = input("Wähle ein Feld (z.B. 1 1 für die Mitte): ")
        if not ungültigerZugPruefung(zug):
            continue
        zeile, spalte = map(int, zug.split())
        if Spielfeld[zeile, spalte] == "[ ]":
            Spielfeld[zeile, spalte] = f"[{symbol}]"
            break
        else:
            print("Das Feld ist bereits belegt. Wähle ein anderes Feld.")

def spielzugComputerZufall():
    freie_felder = np.argwhere(Spielfeld == "[ ]")
    if len(freie_felder) > 0:
        cpu_zug = freie_felder[np.random.choice(len(freie_felder))]
        if symbol == "X":
            Spielfeld[cpu_zug[0], cpu_zug[1]] = "[O]"
        else:
            Spielfeld[cpu_zug[0], cpu_zug[1]] = "[X]"


def unentschiedenPruefung():
    if "[ ]" not in Spielfeld:
        print("Unentschieden! Das Spielfeld ist voll.")
        ergebnisSpeichern("Unentschieden")
        exit()

def gewinnPruefung():
    kombinationen = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for kombi in kombinationen:
        a, b, c = kombi
        if Spielfeld[a] == Spielfeld[b] == Spielfeld[c] and Spielfeld[a] != "[ ]":
            gewinner = Spielfeld[a]
            if gewinner == f"[{symbol}]":
                print("Glückwunsch! Du hast gewonnen!")
                ergebnisSpeichern("Spieler")
            else:
                print("Die CPU hat gewonnen!")
                ergebnisSpeichern("CPU")
            return True

    return False

def ergebnisSpeichern(gewinner):
    dateiname = "Ergebnisse.txt"
    ergebnisse = {"Spieler": 0, "CPU": 0, "Unentschieden": 0, "Gesamtspiele": 0}

    try:
        with open(dateiname, "r") as datei:
            for zeile in datei:
                name, wert = zeile.strip().split(": ")
                ergebnisse[name] = int(wert)
    except FileNotFoundError:
        pass  

    if gewinner == "Spieler":
        ergebnisse["Spieler"] += 1
    elif gewinner == "CPU":
        ergebnisse["CPU"] += 1
    elif gewinner == "Unentschieden":
        ergebnisse["Unentschieden"] += 1

    ergebnisse["Gesamtspiele"] += 1

    with open(dateiname, "w") as datei:
        for name, wert in ergebnisse.items():
            datei.write(f"{name}: {wert}\n")

# --- (3) GLOBALE VARIABLEN ---
# Diese müssen hier definiert werden, damit Tests sie importieren können
Spielfeld = np.array([["[ ]", "[ ]", "[ ]"],
                      ["[ ]", "[ ]", "[ ]"],
                      ["[ ]", "[ ]", "[ ]"]])
symbol = "" # Wird von symbolwahl() gesetzt


# --- (4) SPIELSTART-LOGIK ---
# Dieser Teil wird nur ausgeführt, wenn du 'python main.py' startest,
# nicht, wenn 'unittest' oder 'pytest' die Datei importiert.

if __name__ == "__main__":
    
    print("Willkommen bei deinem Tic Tac Toe Spiel!")
    print("Das Spielfeld ist wie folgt aufgebaut:")
    print(Spielfeld)
    
    symbolwahl() # Setzt das globale 'symbol'
    
    print("Let's Go!")

    strategie = IntelligenteStrategie()

    if symbol == "O":
        print("Die CPU ist am Zug...")
        strategie.wähle_zug()
        print(Spielfeld)
        print(" ")
    else:
        print("Du bist am Zug! Wähle ein Feld, indem du die Koordinaten eingibst.")
        print(Spielfeld)
        print(" ")

    while True:
        spielzugSpieler()
        print(Spielfeld)
        if gewinnPruefung():
            break
        unentschiedenPruefung()
        
        print("Die CPU ist am Zug...")
        strategie.wähle_zug()
        print(Spielfeld)
        if gewinnPruefung():
            break
        unentschiedenPruefung()
        print(" ")
        
    exit()
