import sounddevice as sd

print("Available audio devices:")
devices = sd.query_devices()
for idx, device in enumerate(devices):
    print(f"ID: {idx} - Name: {device['name']} - Inputs: {device['max_input_channels']}")