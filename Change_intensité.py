import wave
import numpy as np

# Ouvrir le fichier audio
audio_file = wave.open("voice.wav", "r")

# Extraire les échantillons audio
signal_frames = audio_file.readframes(-1)
signal_frames = np.frombuffer(signal_frames, dtype=np.int16)

# Normaliser les échantillons audio
signal_frames_norm = signal_frames / (2 ** 15)

# Modifier la puissance sonore
power = 4  # facteur de puissance
signal_frames_powered = np.sign(signal_frames_norm) * (np.abs(signal_frames_norm) ** power)

# Convertir les échantillons audio en un format compatible avec le fichier audio
signal_frames_powered *= 2 ** 15 - 1
signal_frames_powered = signal_frames_powered.astype(np.int16)

# Sauvegarder le fichier audio modifié
audio_file_powered = wave.open("voice.wav", "w")
audio_file_powered.setnchannels(audio_file.getnchannels())
audio_file_powered.setsampwidth(audio_file.getsampwidth())
audio_file_powered.setframerate(audio_file.getframerate())
audio_file_powered.writeframes(signal_frames_powered.tobytes())
audio_file_powered.close()
