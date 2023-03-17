import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack
import wave

# Ouvrir le fichier audio
audio_file = wave.open("out.wav", "r")

# Extraire les échantillons audio
signal_frames = audio_file.readframes(-1)
signal_frames = np.frombuffer(signal_frames, dtype=np.int16)

# Obtenir la fréquence d'échantillonnage
sampling_freq = audio_file.getframerate()

# Appliquer une fenêtre de Hamming au signal
signal_frames = signal_frames * np.hamming(len(signal_frames))

# Calculer la Transformée de Fourier Rapide (FFT)
fft = fftpack.fft(signal_frames)

# Extraire les fréquences et les amplitudes
freqs = fftpack.fftfreq(len(signal_frames)) * sampling_freq
power_spectrum = np.abs(fft)

# Rechercher l'indice de la fréquence maximale dans la plage de fréquences de la voix
min_freq = 43
max_freq = 10000
freq_idx = np.where((freqs >= min_freq) & (freqs <= max_freq))
fundamental_freq = freqs[freq_idx][np.argmax(power_spectrum[freq_idx])]

print("La fréquence fondamentale est : {:.2f} Hz".format(fundamental_freq))
