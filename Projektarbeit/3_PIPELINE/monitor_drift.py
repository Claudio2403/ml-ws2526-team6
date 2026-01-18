import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import sys
import os

skript_ordner = os.path.dirname(os.path.abspath(__file__))

csv_pfad = os.path.join(skript_ordner, 'vehicle_emissions.csv')

referenz_daten = pd.read_csv(csv_pfad)

aktuelle_daten = referenz_daten.sample(frac=0.2, random_state=42).copy()

# -----------------------------------------------------
aktuelle_daten['Fuel_Consumption_comb(L/100km)'] *= 0.8
# -----------------------------------------------------

def pruefe_daten_veraenderung(referenz, aktuell, merkmal_name, grenzwert=0.05):

    referenz_werte = referenz[merkmal_name].dropna()
    aktuell_werte = aktuell[merkmal_name].dropna()

    abstand, p_wert = ks_2samp(referenz_werte, aktuell_werte)
    
    print(f"Prüfe Merkmal: {merkmal_name}")
    print(f"  Abstandswert: {abstand:.4f}, Wahrscheinlichkeit (P-Wert): {p_wert:.4f}")

    if p_wert < grenzwert:
        print(f"WARNUNG: Signifikanter Data Drift bei {merkmal_name} erkannt")
        return True
    else:
        print(f"  [OK] Keine nennenswerte Änderung.")
        return False

merkmale_zur_ueberwachung = ["Engine_Size", "Fuel_Consumption_comb(L/100km)"]

drift_gefunden = False

for merkmal in merkmale_zur_ueberwachung:
    if pruefe_daten_veraenderung(referenz_daten, aktuelle_daten, merkmal):
        drift_gefunden = True

if drift_gefunden:
    print("\nERGEBNIS: Die Datenwelt hat sich verändert. Modell neu trainieren!")
else:
    print("\nERGEBNIS: Alles stabil. Das Modell kann weiter genutzt werden.")