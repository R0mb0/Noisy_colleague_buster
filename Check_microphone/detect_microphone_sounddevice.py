import sounddevice as sd

print("Dispositivi audio disponibili:")
devices = sd.query_devices()
for idx, device in enumerate(devices):
    print(f"ID: {idx} - Nome: {device['name']} - Ingressi: {device['max_input_channels']}")