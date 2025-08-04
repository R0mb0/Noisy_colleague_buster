import pyaudio

p = pyaudio.PyAudio()

print("Dispositivi audio disponibili:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"ID: {i} - Nome: {info['name']} - Ingressi: {info['maxInputChannels']}")

p.terminate()