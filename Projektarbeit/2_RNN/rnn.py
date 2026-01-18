# %% [markdown]
# Aufgabe 2

# %% [markdown]
# Laden der Daten

# %%
import os
import pandas as pd 
import matplotlib.pyplot as plt 

ordnerName = 'Datensätze'
dateiNamen = [
    'mpi_roof_2014a.csv',
    'mpi_roof_2014b.csv',
    'mpi_roof_2015a.csv',
    'mpi_roof_2015b.csv',
    'mpi_roof_2016a.csv',
    'mpi_roof_2016b.csv'
]

datensatzArray = []

for datensatzName in dateiNamen:
    pfadName = os.path.join(ordnerName, datensatzName)
    print(f"Lade Datei: {pfadName}")
    datensatzArray.append(pd.read_csv(pfadName, encoding='ISO-8859-1'))
    
datensatz = pd.concat(datensatzArray, ignore_index = True)
print("Datensätze erfolgreich zusammengefügt")
display(datensatz)

# %% [markdown]
# Reduktion der Messfrequenz

# %%
datensatz['Date Time'] = pd.to_datetime(datensatz['Date Time'], format='%d.%m.%Y %H:%M:%S')

datensatz.set_index('Date Time', inplace = True)

datensatzStündlich = datensatz.resample('h').mean()

display(datensatzStündlich)

import matplotlib.pyplot as plt

# 1. Korrelation berechnen
korrelation = datensatzStündlich.corr()

# 2. Plot mit Matplotlib erstellen
plt.figure(figsize=(12, 10))
plt.matshow(korrelation, fignum=1, cmap='coolwarm')
plt.colorbar()

# Beschriftungen hinzufügen
plt.xticks(range(len(korrelation.columns)), korrelation.columns, rotation=90)
plt.yticks(range(len(korrelation.columns)), korrelation.columns)

plt.title("Korrelation der Features", y=1.2) # Titel etwas höher schieben
plt.show()

# %% [markdown]
# Daten visualisieren

# %%
plt.figure(figsize = (15, 6))

plt.plot(datensatzStündlich.index, datensatzStündlich['T (degC)'])

plt.title("Temperaturverlauf Jena (2014-2016) - Stündliche Mittelwerte")
plt.xlabel("Datum")
plt.ylabel("Temperatur in °C")
plt.grid(True)

plt.show()

# %% [markdown]
# Feature Engineering

# %%
import numpy as np

# Flüssigen Übergang in Windrichtung machen

windrichtung_rad = datensatzStündlich['wd (deg)'] * np.pi / 180

datensatzStündlich['Wx'] = np.sin(windrichtung_rad)
datensatzStündlich['Wy'] = np.cos(windrichtung_rad)

datensatzStündlich = datensatzStündlich.drop(columns=['wd (deg)'])


# weitere redundante features löschen

spalten_zum_loeschen = [
    'Tpot (K)',          
    'rho (g/m**3)',      
    'H2OC (mmol/mol)',   
    'Tdew (degC)',       
    'VPmax (mbar)',      
    'VPdef (mbar)'       
]

datensatzStündlich = datensatzStündlich.drop(columns=spalten_zum_loeschen)



# %% [markdown]
# Aufteilung der Daten (70% Training, 20% Validierung, 10% Test)

# %%
n = len(datensatzStündlich)

trainingsEndeIndex = int(n * 0.7)
validierungsEndeIndex = int(n * 0.9)

trainingsDatensatz = datensatzStündlich.iloc[:trainingsEndeIndex]
validierungsDatensatz = datensatzStündlich.iloc[trainingsEndeIndex:validierungsEndeIndex]
testDatensatz = datensatzStündlich.iloc[validierungsEndeIndex:]

display(trainingsDatensatz)
display(validierungsDatensatz)
display(testDatensatz)

# %% [markdown]
# Alle Datensets plotten

# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 6))

plt.plot(trainingsDatensatz.index, trainingsDatensatz['T (degC)'], label='Training')
plt.plot(validierungsDatensatz.index, validierungsDatensatz['T (degC)'], label='Validierung')
plt.plot(testDatensatz.index, testDatensatz['T (degC)'], label='Test')

plt.title("Datenaufteilung: Training, Validierung und Test")
plt.xlabel("Datum")
plt.ylabel("Temperatur (°C)")
plt.legend() 
plt.grid(True)
plt.show()

# %% [markdown]
# Normalisieren

# %%
trainingsDatensatzDurchschnitt = trainingsDatensatz.mean()
trainingsDatensatzStandardabweichung = trainingsDatensatz.std()

trainingsDatensatz = (trainingsDatensatz - trainingsDatensatzDurchschnitt) / trainingsDatensatzStandardabweichung
validierungsDatensatz = (validierungsDatensatz - trainingsDatensatzDurchschnitt) / trainingsDatensatzStandardabweichung
testDatensatz = (testDatensatz - trainingsDatensatzDurchschnitt) / trainingsDatensatzStandardabweichung

trainingsDatensatz = trainingsDatensatz.fillna(0)
validierungsDatensatz = validierungsDatensatz.fillna(0)
testDatensatz = testDatensatz.fillna(0)

print("Neuer Durchschnitt (Training):")
print(trainingsDatensatz['T (degC)'].mean())

display(trainingsDatensatz)

# %% [markdown]
# Windowing

# %%
import numpy as np 
from tensorflow.keras.utils import timeseries_dataset_from_array

FENSTER_GROESSE = 24
VORHERSAGE_GROESSE = 1
BATCH_GROESSE = 32

zielSpaltenIndex = list(trainingsDatensatz.columns).index('T (degC)')

def erstelleDatensatz(daten, zielIndex, fenster, batchSize, zufaelligkeit):
    eingabewerte = daten.to_numpy()[:-fenster]
    zielwerte = daten.iloc[fenster:, zielIndex].to_numpy()
    
    datensatz = timeseries_dataset_from_array(
        data = eingabewerte,
        targets = zielwerte,
        sequence_length = fenster,
        batch_size = batchSize,
        shuffle = zufaelligkeit,
    )
    return datensatz

trainingsDatensatzFenster = erstelleDatensatz(trainingsDatensatz, zielSpaltenIndex, FENSTER_GROESSE, BATCH_GROESSE, True)
validierungsDatensatzFenster = erstelleDatensatz(validierungsDatensatz, zielSpaltenIndex, FENSTER_GROESSE, BATCH_GROESSE, False)
testDatensatzFenster = erstelleDatensatz(testDatensatz, zielSpaltenIndex, FENSTER_GROESSE, BATCH_GROESSE, False)



# %% [markdown]
# Aufgabe 3

# %%
import tensorflow as tf 
from tensorflow.keras import layers

modell = tf.keras.Sequential()

anzahlSpalten = trainingsDatensatz.shape[1]

# Schicht 1
modell.add(layers.LSTM(units = 32, input_shape = (FENSTER_GROESSE, anzahlSpalten)))

# Schicht 2
modell.add(layers.Dropout(0.2))

# Schicht 3
modell.add(layers.Dense(units = 1))

# Hyperparameter festlegen
modell.compile(
    loss = 'mae',       # mae = mean absolute error
    optimizer = 'adam',
    metrics = ['mae'],
)

modell.summary()

print("Training starten ...")

verlauf = modell.fit(
    trainingsDatensatzFenster,
    epochs = 10,
    validation_data = validierungsDatensatzFenster,
)



# %%
loss = verlauf.history['loss']
val_loss = verlauf.history['val_loss']

plt.figure(figsize=(10, 6))
plt.plot(loss, label='Training (mit Dropout)')
plt.plot(val_loss, label='Validierung (ohne Dropout)')
plt.title('Lernkurve mit Dropout')
plt.xlabel('Epochen')
plt.ylabel('Fehler (MAE)')
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# Aufgabe 4

# %%
testergebnis = modell.evaluate(testDatensatzFenster)

print(f"Test Loss (Fehler): {testergebnis[0]}")
print(f"Test MAE (Genauigkeit): {testergebnis[1]}")

# %% [markdown]
# visualisieren

# %%
input_batch, echte_temperatur = next(iter(testDatensatzFenster))

vorhersage = modell.predict(input_batch)

plt.figure(figsize=(12, 6))

plt.plot(echte_temperatur, label = 'Echte Temperatur (Messung)', color = 'blue', marker = '.')

plt.plot(vorhersage, label = 'Vorhersage (KI)', color = 'red', marker = 'x')

plt.title('Realität vs. Vorhersage (Ausschnitt von 32 Stunden)')
plt.ylabel('Temperatur (normalisiert)')
plt.xlabel('Zeit (Stunden im Batch)')
plt.legend()
plt.grid(True)

plt.show()


