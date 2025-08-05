Urbino`s University - Computing and digital innovation - Programmazione per l'internet of things

# IoT Anti-Colleague Noise Device
*Raspberry Pi + Python + ThingSpeak Edition*

<div align="center">
<img height="60%" width="60%" src="https://github.com/R0mb0/Noisy_colleague_buster/blob/main/Images/Logo.png" alt="Logo" />
</div>

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1bb60833b43e4ff1b3ff6dc529737e05)](https://app.codacy.com/gh/R0mb0/Noisy_colleague_buster/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/R0mb0/Noisy_colleague_buster)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/R0mb0/Noisy_colleague_buster)
[![MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)
[![Donate](https://img.shields.io/badge/PayPal-Donate%20to%20Author-blue.svg)](http://paypal.me/R0mb0)

## What is this?

Ever dreamed of sweet, peaceful silence in your office?  
Tired of that one colleague who thinks "speaking up" means "shouting across the room"?  
Meet the **IoT Anti-Colleague Noise Device**: a Raspberry Pi-powered gadget that keeps your workspace civil, and your eardrums intact!

---

## Project Overview

This device is a DIY IoT system built with a Raspberry Pi, a USB microphone, and a speaker.  
Its mission: **detect excessive noise, gently "punish" the offender, and keep a cloud-based log of every incident.**

### How does it work?

1. **Continuous Noise Monitoring:**  
   The Pi listens to the room using a USB microphone, measuring the volume in real time.
2. **Threshold Detection:**  
   Too loud? The device knows. You can set the sensitivity via a config file.
3. **"Reprimand" via Speaker:**  
   If the noise crosses the limit, the speaker plays back an echo or a funny sound.  
   (Think of it as a gentle, geeky way to say "shhh!")
4. **Cloud Logging (ThingSpeak):**  
   Every incident is recorded (timestamp, volume) and sent to ThingSpeak for analysis and beautiful graphs.

---

## Hardware Required

- **Raspberry Pi 3B+** (or newer)
- **USB Microphone** (e.g., PS3 Eye Camera for extra nerd points)
- **Speaker** (3.5mm jack or USB)
- **Power Supply** (USB)

---

## Software Features

- Real-time audio monitoring using Python (`sounddevice` or `PyAudio`)
- Noise threshold configurable on the fly (no need to restart)
- Echo/disturbance playback when someone gets too loud
- Local event logging (CSV or lightweight DB)
- Push events to ThingSpeak via REST API for cloud visualization
- Fully open source and hackable

---

## Cloud Integration

Data is sent to **ThingSpeak**, a free IoT analytics platform.  
You get:
- Online dashboard with incident graphs
- Aggregated stats (who's the loudest, when, etc.)
- Access from anywhere

---

## Why would I want this?

- **Fun:** Tech-powered office pranks!
- **Peace:** Bring order to chaotic open spaces.
- **Metrics:** Finally, proof that Sbregò is too loud.
- **Hackability:** Extend it, automate alerts, add sensors, whatever you want.
