import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 48000    # Hz
CHANNELS = 1           # Mono
DEVICE = None          # Default input device, set ID if needed
DURATION = 0.5         # Window in seconds (how often to refresh)
REF = 32768            # Reference for dB calculation (int16 max amplitude)

def rms_to_dbfs(rms, ref=REF):
    """Convert RMS to dBFS (decibels relative to full scale)"""
    if rms > 0:
        dbfs = 20 * np.log10(rms / ref)
    else:
        dbfs = -float('inf')
    return dbfs

print("Starting continuous volume monitoring (Ctrl+C to stop)...")
try:
    while True:
        audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', device=DEVICE)
        sd.wait()
        rms = np.sqrt(np.mean(audio.astype(np.float64)**2))
        dbfs = rms_to_dbfs(rms)
        print(f"RMS: {rms:.1f} | Approx. dBFS: {dbfs:.1f}")
        time.sleep(0.05)  # Small pause between measurements
except KeyboardInterrupt:
    print("Monitoring stopped.")
