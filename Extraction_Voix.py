import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Charger le fichier audio
audio_file = 'audio.wav'
with wave.open(audio_file, 'r') as wave_file:
    # Obtenir les paramètres audio
    nchannels, sampwidth, framerate, nframes, comptype, compname = wave_file.getparams()
    # Lire les données audio
    audio_data = wave_file.readframes(nframes)
    # Convertir les données audio en tableau numpy
    audio_data = np.frombuffer(audio_data, dtype=np.int16)

# Normaliser les données audio
audio_data = audio_data / np.max(np.abs(audio_data))

# Extraire la fréquence fondamentale
f0 = np.zeros_like(audio_data)
for i in range(len(audio_data)):
    # Calculer l'autocorrélation
    corr = np.correlate(audio_data[i:i+framerate], audio_data[i:i+framerate], mode='full')
    # Trouver le premier pic après le décalage de la fréquence d'échantillonnage
    peaks, _ = find_peaks(corr[framerate:], height=0)
    if len(peaks) > 0:
        f0[i] = framerate / peaks[0]

# Extraire les formants
formants = np.zeros((len(audio_data), 4))
for i in range(len(audio_data)):
    # Calculer le spectrogramme
    f, t, Sxx = plt.specgram(audio_data[i:i+framerate], Fs=framerate)
    # Trouver les quatre premiers formants
    peaks, _ = find_peaks(np.mean(Sxx, axis=1), height=0)
    if len(peaks) >= 4:
        formants[i] = f[peaks[:4]]

# Extraire l'énergie spectrale
spectral_flux = np.zeros_like(audio_data)
for i in range(len(audio_data)):
    if i == 0:
        spectral_flux[i] = 0
    else:
        # Calculer la différence spectrale entre les trames successives
        diff = np.abs(np.fft.rfft(audio_data[i:i+framerate])) - np.abs(np.fft.rfft(audio_data[i-1:i-1+framerate]))
        spectral_flux[i] = np.sum(np.maximum(diff, 0))

# Extraire la durée
duration = len(audio_data) / framerate

# Extraire l'intensité
intensity = np.zeros_like(audio_data)
for i in range(len(audio_data)):
    intensity[i] = 20 * np.log10(np.abs(audio_data[i]))

# Imprimer les résultats
print('Fréquence fondamentale :', f0)
print('Formants :', formants)
print('Énergie spectrale :', spectral_flux)
print('Durée :', duration)
print('Intensité :', intensity)
