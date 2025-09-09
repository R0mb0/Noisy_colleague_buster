# Resources

- **Application/audio_monitor_echo_service.py**  
  The main script performing continuous monitoring of ambient noise via USB microphone on Raspberry Pi.  
  Triggers the echo effect when volume exceeds the configured threshold, manages microphone lockout and echo parameters.  
  Exposes a REST API for remote configuration and logs events to both ThingSpeak (cloud) and local CSV.

- **Application/webapp.py**  
  Flask web application providing a real-time dashboard for system control.  
  Displays live system status, allows changing parameters (threshold, echo, lockout), and manages authentication.  
  Acts as frontend and proxy to the audio backend REST API.

- **Application/static/mixer.js**  
  JavaScript powering the dashboard UI.  
  Handles live controls, displays current noise level, microphone and echo status, and sends parameter changes to the REST API.

- **Application/static/style.css**  
  CSS file for the dashboard web interface, ensuring a modern and responsive look.  
  Controls the style of sliders, status lamps, timers, and overall layout.

- **Application/templates/login.html** & **templates/dashboard.html**  
  HTML template files for Flask.  
  `login.html` displays the authentication form; `dashboard.html` shows the dashboard with all system controls and indicators.

- **Application/threshold_config.json**  
  Configuration file containing runtime system parameters: trigger threshold, microphone lockout, echo parameters (delay, taps, feedback, start/end volume, frame duration).  
  Editable via the dashboard or directly.

- **Application/config.json**  
  Configuration file with the ThingSpeak API keys and channel ID.  
  Used by the Python backend to send data to the cloud.  
  **Note:** This file should not be published in public repositories.

- **Application/event_log.csv**  
  Local log file saving each echo activation event: ISO8601 timestamp and noise level (dBFS).  
  Useful for historical analysis and data backup.

- **Application/audio_monitor_service.py** & **Application/start_audio_monitor.sh**  
  Systemd service file and startup script to run the Python backend as an automatic service on Raspberry Pi boot.

- **Application/password.json**  
  Configuration file storing the dashboard access password.

- **Report/Report/report.tex**  
  The main LaTeX document for the project, including the technical report, results analysis, figures, plots, and detailed implementation description.

- **Report/Report/sample.bib**  
  Example BibTeX file for references in the LaTeX report (if needed).

---

All files are documented and commented within the code and the GitHub repository.  
For questions, feature requests, or bug reports, please refer to the README or open an issue directly on GitHub.
