# Continuous Volume Monitor — Raspberry Pi & Python

This script allows you to **continuously monitor the audio volume** from a USB microphone on your Raspberry Pi. It calculates the RMS (Root Mean Square) value of the audio signal and provides an approximate decibel reading (dBFS) in real time.  
Ideal for projects that require noise level tracking, threshold detection, or integration with IoT systems.

---

## Features

- Real-time measurement of audio volume from any compatible USB microphone.
- Outputs both RMS value and estimated dBFS (decibel Full Scale).
- Configurable sample rate, duration, and device selection.
- Easy to correlate with real-world noise levels using simple calibration.
- Written entirely in Python, suitable for Raspberry Pi OS or any Linux distribution.

---

## Installation

1. **Install dependencies:**
   ```bash
   pip3 install sounddevice numpy
   ```
2. **Connect your USB microphone** and ensure it is recognized by the system.

---

## Usage

1. Save the script as `continuous_volume_monitor.py`.
2. Run the script:
   ```bash
   python3 continuous_volume_monitor.py
   ```
3. The script will print the RMS value and approximate dBFS every half second.

---

## Practical Notes

- **dBFS** is a relative value (decibels referenced to the maximum possible digital audio amplitude).  
  - `0 dBFS` indicates the loudest possible signal (digital clipping).
  - Typical speech is between `-35` and `-15 dBFS`.
- To correlate with real-world decibel SPL, you can calibrate:
  - Measure dBFS in a quiet room and with a known noise source (e.g., use a phone app).
  - Use the difference as an offset for your calibration.
- You can set `DEVICE` in the script to the specific microphone ID, as detected by the included microphone detection scripts.
- Adjust `DURATION` for more or less frequent measurements.

---

## Example Output

```
RMS: 327.4 | Approx. dBFS: -40.0
RMS: 1200.8 | Approx. dBFS: -27.7
RMS: 5400.1 | Approx. dBFS: -15.7
```
## Author

Developed for the "IoT Anti-Colleague Noise Device" project — Raspberry Pi & Python edition.
