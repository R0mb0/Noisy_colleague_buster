import json
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

# --- Configuration ---
API_URL = "http://127.0.0.1:8080"  # REST API of audio_monitor_echo_service
PASSWORD_PATH = os.path.join(os.path.dirname(__file__), "password.json")
SECRET_KEY = "change_this_for_real_deploy"  # Change this for deployment

INSULTS = [
    "Wrong password, dork.",
    "Nope. Did you smash your keyboard?",
    "Try again, genius.",
    "Denied. You're not as clever as you think.",
    "Do you even know what you're doing?",
    "Access denied, rookie.",
    "Nice try, clown.",
    "Seriously? That's your password?",
    "Dream on, hacker.",
    "Not even close, pal.",
    "Better luck next time, loser.",
    "Nope, that's not it, champ.",
    "Are you even trying?",
    "Come on, my grandma does better.",
    "Password fail. Again.",
    "Have you considered reading the manual?",
    "404: Brain not found.",
    "Nice guess, but no.",
    "Keep guessing, Sherlock.",
    "Wrong again. Go have a coffee."
]

app = Flask(__name__)
app.secret_key = "0e9d82151d5b86b40c00b1a257f20093b93b5f705f9fd90cd3c878962209ca6c"

def get_password():
    with open(PASSWORD_PATH) as f:
        data = json.load(f)
    return data["password"]

def insult():
    return random.choice(INSULTS)

def is_logged_in():
    return session.get("logged_in", False)

# --- ROUTES ---

@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    color = "red"
    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == get_password():
            session["logged_in"] = True
            msg = "Access granted"
            color = "green"
            return redirect(url_for("dashboard"))
        else:
            msg = insult()
    return render_template("login.html", msg=msg, color=color)

@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- API PROXIES (between frontend and backend REST API) ---

@app.route("/api/status")
def api_status():
    try:
        r = requests.get(f"{API_URL}/status", timeout=2)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 503

@app.route("/api/volume")
def api_volume():
    try:
        r = requests.get(f"{API_URL}/volume", timeout=2)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 503

@app.route("/api/threshold", methods=["GET", "POST"])
def api_threshold():
    if request.method == "POST":
        data = request.json
        try:
            r = requests.post(f"{API_URL}/threshold", json=data, timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503
    else:
        try:
            r = requests.get(f"{API_URL}/threshold", timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503

@app.route("/api/echo_params", methods=["GET", "POST"])
def api_echo_params():
    if request.method == "POST":
        data = request.json
        try:
            r = requests.post(f"{API_URL}/echo_params", json=data, timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503
    else:
        try:
            r = requests.get(f"{API_URL}/echo_params", timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503

@app.route("/api/lockout", methods=["GET", "POST"])
def api_lockout():
    if request.method == "POST":
        data = request.json
        try:
            r = requests.post(f"{API_URL}/lockout", json=data, timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503
    else:
        try:
            r = requests.get(f"{API_URL}/lockout", timeout=2)
            return jsonify(r.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 503

@app.route("/api/start_echo", methods=["POST"])
def api_start_echo():
    try:
        r = requests.post(f"{API_URL}/start_echo", timeout=2)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
