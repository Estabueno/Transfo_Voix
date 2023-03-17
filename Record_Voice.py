import pyaudio
import wave

# Définir les paramètres de l'enregistrement audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialiser l'objet PyAudio
audio = pyaudio.PyAudio()

# Ouvrir le flux audio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Enregistrement en cours...")

# Enregistrer les données audio
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Enregistrement terminé.")

# Arrêter le flux audio
stream.stop_stream()
stream.close()
audio.terminate()

# Enregistrer les données audio dans un fichier WAV
wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wave_file.setnchannels(CHANNELS)
wave_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_file.setframerate(RATE)
wave_file.writeframes(b''.join(frames))
wave_file.close()
