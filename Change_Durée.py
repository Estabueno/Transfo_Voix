import wave
import numpy as np

# Ouvrir le fichier audio
audio_file = wave.open("voice.wav", "r")

# Extraire les échantillons audio
signal_frames = audio_file.readframes(-1)
signal_frames = np.frombuffer(signal_frames, dtype=np.int16)

# Obtenir la fréquence d'échantillonnage
sampling_freq = audio_file.getframerate()

# Calculer le facteur d'échelle
rate = 0.1  # facteur d'échelle
new_len = int(len(signal_frames) / rate)

# Appliquer une interpolation linéaire pour modifier la longueur temporelle
time_old = np.linspace(0, len(signal_frames) / sampling_freq, num=len(signal_frames))
time_new = np.linspace(0, len(signal_frames) / sampling_freq, num=new_len)
signal_frames_stretched = np.interp(time_new, time_old, signal_frames)

# Convertir les échantillons audio en un format compatible avec le fichier audio
signal_frames_stretched = signal_frames_stretched.astype(np.int16)

# Sauvegarder le fichier audio modifié
audio_file_stretched = wave.open("voice.wav", "w")
audio_file_stretched.setnchannels(audio_file.getnchannels())
audio_file_stretched.setsampwidth(audio_file.getsampwidth())
audio_file_stretched.setframerate(sampling_freq)
audio_file_stretched.writeframes(signal_frames_stretched.tobytes())
audio_file_stretched.close()
