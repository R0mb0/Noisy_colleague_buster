"""
Audio Monitor & Echo Service with Robust State Handling

Reads configuration from threshold_config.json at startup.
API modifications persist to the same file.
Adds robust state management: mic_enabled and echo_active always reset even in case of errors.
"""

import sounddevice as sd
import numpy as np
import threading
import time
import json
import os
from flask import Flask, jsonify, request

# --- Config file path ---
CONFIG_PATH = "/home/rombo/00_APPLICATION/threshold_config.json"

# --- Defaults (used if JSON missing fields) ---
DEFAULT_CONFIG = {
    "THRESHOLD_DBFS": -25.0,
    "LOCKOUT_SEC": 2.0,
    "ECHO_DELAY_SEC": 0.25,
    "ECHO_TAPS": 3,
    "ECHO_FEEDBACK": 0.5,
    "ECHO_START_VOL": 1.0,
    "ECHO_END_VOL": 0.3,
    "FRAME_DURATION": 1.5
}

# --- Load/save config ---
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    # Fill any missing fields with defaults
    out = DEFAULT_CONFIG.copy()
    out.update(data)
    return out

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

# --- Global (dynamic) state from config ---
config = load_config()
THRESHOLD_DBFS = config["THRESHOLD_DBFS"]
LOCKOUT_SEC = config["LOCKOUT_SEC"]
ECHO_DELAY_SEC = config["ECHO_DELAY_SEC"]
ECHO_TAPS = config["ECHO_TAPS"]
ECHO_FEEDBACK = config["ECHO_FEEDBACK"]
ECHO_START_VOL = config["ECHO_START_VOL"]
ECHO_END_VOL = config["ECHO_END_VOL"]
FRAME_DURATION = config.get("FRAME_DURATION", 1.5)

SAMPLE_RATE = 16000
CHANNELS = 1
DEVICE = None

current_volume = {
    "rms": 0.0,
    "dbfs": -float('inf'),
    "updated": time.time()
}
lock = threading.Lock()

mic_enabled = True
echo_active = False
echo_level = 0.0
echo_level_lock = threading.Lock()

api_app = Flask(__name__)

def rms_to_dbfs(rms, ref=32768.0):
    if rms > 0:
        return 20 * np.log10(rms / ref)
    return -float('inf')

def get_echo_envelope(taps, start_vol, end_vol):
    if taps <= 1:
        return [start_vol]
    return np.linspace(start_vol, end_vol, taps)

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def create_echo_buffer(audio, taps, delay_sec, feedback, start_vol, end_vol):
    n_samples = len(audio)
    delay_samples = int(delay_sec * SAMPLE_RATE)
    envelope = get_echo_envelope(taps, start_vol, end_vol)
    out = np.zeros(n_samples + delay_samples * taps, dtype=np.float32)
    out[:n_samples] += audio.flatten()
    for i in range(taps):
        start = delay_samples * (i + 1)
        end = start + n_samples
        if end > len(out):
            break
        echo = audio.flatten() * envelope[i]
        if feedback > 0 and i > 0:
            echo += out[start-delay_samples:end-delay_samples] * feedback
        out[start:end] += echo
    return out, envelope

def monitor_thread():
    global current_volume, mic_enabled
    while True:
        if mic_enabled:
            try:
                audio = sd.rec(int(FRAME_DURATION * SAMPLE_RATE),
                               samplerate=SAMPLE_RATE,
                               channels=CHANNELS, dtype='int16', device=DEVICE)
                sd.wait()
                arr = audio.astype(np.float32)
                rms = np.sqrt(np.mean(arr**2))
                dbfs = rms_to_dbfs(rms)
                with lock:
                    current_volume = {
                        "rms": float(rms),
                        "dbfs": float(dbfs),
                        "updated": time.time()
                    }
                if dbfs > THRESHOLD_DBFS:
                    log(f"Threshold exceeded! dbfs={dbfs:.1f}. Triggering echo...")
                    trigger_echo(arr.flatten())
            except Exception as e:
                log(f"Audio monitor error: {e}")
                time.sleep(1)
        else:
            time.sleep(0.05)

def trigger_echo(audio_frame):
    global mic_enabled, echo_active, echo_level
    echo_audio, envelope = create_echo_buffer(
        audio_frame,
        ECHO_TAPS,
        ECHO_DELAY_SEC,
        ECHO_FEEDBACK,
        ECHO_START_VOL,
        ECHO_END_VOL
    )
    echo_audio = np.clip(echo_audio, -32768, 32767).astype(np.int16)
    mic_enabled = False
    echo_active = True

    def playback_with_animation():
        global echo_level, echo_active, mic_enabled
        try:
            sd.play(echo_audio, samplerate=SAMPLE_RATE, device=DEVICE)
            # Animate echo_level for UI: step through each tap
            for i, tap_env in enumerate(envelope):
                with echo_level_lock:
                    echo_level = float(tap_env)
                if i == 0:
                    time.sleep(FRAME_DURATION)
                else:
                    time.sleep(ECHO_DELAY_SEC)
            with echo_level_lock:
                echo_level = float(ECHO_END_VOL)
            # Added timeout to avoid infinite blocking
            sd.wait(timeout=int(FRAME_DURATION + ECHO_DELAY_SEC * len(envelope) + 2))
            log("Echo playback finished.")
        except Exception as e:
            log(f"Echo playback error: {e}")
        finally:
            echo_active = False
            mic_enabled = True
            log("Mic re-enabled after lockout (finally block).")

    # Run echo playback and animation in a separate thread
    thread = threading.Thread(target=playback_with_animation)
    thread.start()
    # Lockout delay is now handled in the finally block, not here

# --- REST API (Flask) ---
@api_app.route('/volume', methods=['GET'])
def api_get_volume():
    with lock:
        return jsonify(current_volume)

@api_app.route('/threshold', methods=['GET', 'POST'])
def api_threshold():
    global THRESHOLD_DBFS, config
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "threshold_dbfs" in data:
            try:
                val = float(data["threshold_dbfs"])
                THRESHOLD_DBFS = val
                config["THRESHOLD_DBFS"] = val
                save_config(config)
                log(f"Threshold updated via API: {val:.1f} dBFS")
                return jsonify({"status": "ok", "threshold_dbfs": THRESHOLD_DBFS})
            except Exception:
                return jsonify({"status": "error", "message": "Invalid value"}), 400
        return jsonify({"status": "error", "message": "Missing field"}), 400
    else:
        return jsonify({"threshold_dbfs": THRESHOLD_DBFS})

@api_app.route('/echo_params', methods=['GET', 'POST'])
def api_echo_params():
    global ECHO_DELAY_SEC, ECHO_TAPS, ECHO_FEEDBACK, ECHO_START_VOL, ECHO_END_VOL, FRAME_DURATION, config
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            if "delay_sec" in data:
                ECHO_DELAY_SEC = float(data["delay_sec"])
                config["ECHO_DELAY_SEC"] = ECHO_DELAY_SEC
            if "taps" in data:
                ECHO_TAPS = int(data["taps"])
                config["ECHO_TAPS"] = ECHO_TAPS
            if "feedback" in data:
                ECHO_FEEDBACK = float(data["feedback"])
                config["ECHO_FEEDBACK"] = ECHO_FEEDBACK
            if "start_vol" in data:
                ECHO_START_VOL = float(data["start_vol"])
                config["ECHO_START_VOL"] = ECHO_START_VOL
            if "end_vol" in data:
                ECHO_END_VOL = float(data["end_vol"])
                config["ECHO_END_VOL"] = ECHO_END_VOL
            if "frame_duration" in data:
                FRAME_DURATION = float(data["frame_duration"])
                config["FRAME_DURATION"] = FRAME_DURATION
            save_config(config)
            log(f"Echo params updated via API.")
            return jsonify({
                "status": "ok",
                "delay_sec": ECHO_DELAY_SEC,
                "taps": ECHO_TAPS,
                "feedback": ECHO_FEEDBACK,
                "start_vol": ECHO_START_VOL,
                "end_vol": ECHO_END_VOL,
                "frame_duration": FRAME_DURATION
            })
        except Exception:
            return jsonify({"status": "error", "message": "Invalid value"}), 400
    else:
        return jsonify({
            "delay_sec": ECHO_DELAY_SEC,
            "taps": ECHO_TAPS,
            "feedback": ECHO_FEEDBACK,
            "start_vol": ECHO_START_VOL,
            "end_vol": ECHO_END_VOL,
            "frame_duration": FRAME_DURATION
        })

@api_app.route('/lockout', methods=['GET', 'POST'])
def api_lockout():
    global LOCKOUT_SEC, config
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "lockout_sec" in data:
            try:
                val = float(data["lockout_sec"])
                LOCKOUT_SEC = val
                config["LOCKOUT_SEC"] = val
                save_config(config)
                log(f"Lockout updated via API: {val:.1f} sec")
                return jsonify({"status": "ok", "lockout_sec": LOCKOUT_SEC})
            except Exception:
                return jsonify({"status": "error", "message": "Invalid value"}), 400
        return jsonify({"status": "error", "message": "Missing field"}), 400
    else:
        return jsonify({"lockout_sec": LOCKOUT_SEC})

@api_app.route('/start_echo', methods=['POST'])
def api_start_echo():
    if not mic_enabled:
        return jsonify({"status": "error", "message": "Mic is locked out"}), 403
    try:
        audio = sd.rec(int(FRAME_DURATION * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE,
                       channels=CHANNELS, dtype='int16', device=DEVICE)
        sd.wait()
        arr = audio.astype(np.float32)
        threading.Thread(target=trigger_echo, args=(arr.flatten(),), daemon=True).start()
        log("Manual echo triggered via API.")
        return jsonify({"status": "ok", "message": "Echo triggered"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_app.route('/status', methods=['GET'])
def api_status():
    with lock:
        v = dict(current_volume)
    with echo_level_lock:
        level = float(echo_level)
    status = {
        "mic_enabled": mic_enabled,
        "last_rms": v["rms"],
        "last_dbfs": v["dbfs"],
        "updated": v["updated"],
        "threshold_dbfs": THRESHOLD_DBFS,
        "echo_params": {
            "delay_sec": ECHO_DELAY_SEC,
            "taps": ECHO_TAPS,
            "feedback": ECHO_FEEDBACK,
            "start_vol": ECHO_START_VOL,
            "end_vol": ECHO_END_VOL,
            "frame_duration": FRAME_DURATION,
            "active": echo_active,
            "level": level
        },
        "lockout_sec": LOCKOUT_SEC
    }
    return jsonify(status)

if __name__ == '__main__':
    log("Starting Audio Monitor + Echo + API Service...")
    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    api_app.run(host='127.0.0.1', port=8080, threaded=True)