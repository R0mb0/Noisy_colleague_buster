import sounddevice as sd
from scipy.io.wavfile import write, read

# --- Settings ---
DURATION = 60        # seconds
SAMPLE_RATE = 48000  # Hz (PS3 Eye and most USB mics)
CHANNELS = 1         # mono
DEVICE = None        # None = default input/output device

print(f"Recording for {DURATION} seconds...")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', device=DEVICE)
sd.wait()
write('test_record.wav', SAMPLE_RATE, audio)
print("Recording complete! Saved as test_record.wav")

# Playback
print("Playing back the recorded audio...")
fs, data = read('test_record.wav')
sd.play(data, fs, device=DEVICE)
sd.wait()
print("Playback finished.")