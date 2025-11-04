import numpy as np

def symbolwahl():
    global symbol

    print("Wähle ein Symbol: X oder O")
    symbol = input().strip().upper()
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

def spielzugComputer():
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
                exit()
            else:
                print("Die CPU hat gewonnen!")
                ergebnisSpeichern("CPU")
                exit()
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


Spielfeld = np.array([["[ ]", "[ ]", "[ ]"],
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
    spielzugComputer()
    print(Spielfeld)
    if gewinnPruefung():
        break
    unentschiedenPruefung()
    print(" ")
exit()
