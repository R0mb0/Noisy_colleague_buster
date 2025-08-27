// Runs after DOMContentLoaded
document.addEventListener("DOMContentLoaded", async function() {
    // --- Default "center" values (hardcoded, do not change unless you want to shift the reference) ---
    const paramCenters = {
        "THRESHOLD_DBFS": -25.0,
        "LOCKOUT_SEC": 2.0,
        "ECHO_DELAY_SEC": 0.25,
        "ECHO_TAPS": 3,
        "ECHO_FEEDBACK": 0.5,
        "ECHO_START_VOL": 1.0,
        "ECHO_END_VOL": 0.3
    };

    const colDefs = [
        // label, type, param, min, max, step, format, extra
        { label: "VOLUME", type: "vmeter" },
        { label: "THRESHOLD", type: "slider", param: "THRESHOLD_DBFS", min: -50, max: 0, step: 0.5, format: v => v.toFixed(1) + " dBFS" },
        { label: "MIC STATUS", type: "lamp", state: "mic_enabled", on: true, on_label: "ON", off_label: "OFF" },
        { label: "LOCKOUT", type: "slider", param: "LOCKOUT_SEC", min: 0, max: 10, step: 0.1, format: v => v.toFixed(1) + " s" },
        { label: "ECHO STATUS", type: "lamp", state: "echo_active", on: true, on_label: "ON", off_label: "OFF" },
        { label: "ECHO DELAY", type: "slider", param: "ECHO_DELAY_SEC", min: 0, max: 1.0, step: 0.01, format: v => v.toFixed(2) + " s" },
        { label: "ECHO TAPS", type: "slider", param: "ECHO_TAPS", min: 1, max: 8, step: 1, format: v => v },
        { label: "ECHO FEEDBACK", type: "slider", param: "ECHO_FEEDBACK", min: 0, max: 1.0, step: 0.01, format: v => Math.round(v*100) + "%" },
        { label: "ECHO VOLUME", type: "timer" },
        { label: "START VOL", type: "slider", param: "ECHO_START_VOL", min: 0, max: 1.5, step: 0.01, format: v => v.toFixed(2) },
        { label: "END VOL", type: "slider", param: "ECHO_END_VOL", min: 0, max: 1.5, step: 0.01, format: v => v.toFixed(2) }
    ];

    const paramMap = {
        "THRESHOLD_DBFS": { api: "/api/threshold", key: "threshold_dbfs" },
        "LOCKOUT_SEC": { api: "/api/lockout", key: "lockout_sec" },
        "ECHO_DELAY_SEC": { api: "/api/echo_params", key: "delay_sec" },
        "ECHO_TAPS": { api: "/api/echo_params", key: "taps" },
        "ECHO_FEEDBACK": { api: "/api/echo_params", key: "feedback" },
        "ECHO_START_VOL": { api: "/api/echo_params", key: "start_vol" },
        "ECHO_END_VOL": { api: "/api/echo_params", key: "end_vol" }
    };

    let current = {}; // Holds latest status

    // --- Fetch initial values from backend before rendering UI ---
    let initialValues = {};
    try {
        const resp = await fetch("/api/status");
        if (resp.ok) {
            const data = await resp.json();
            initialValues = {
                "THRESHOLD_DBFS": data.threshold_dbfs,
                "LOCKOUT_SEC": data.lockout_sec,
            };
            if (data.echo_params) {
                initialValues["ECHO_DELAY_SEC"] = data.echo_params.delay_sec;
                initialValues["ECHO_TAPS"] = data.echo_params.taps;
                initialValues["ECHO_FEEDBACK"] = data.echo_params.feedback;
                initialValues["ECHO_START_VOL"] = data.echo_params.start_vol;
                initialValues["ECHO_END_VOL"] = data.echo_params.end_vol;
            }
        }
    } catch (e) {
        // If cannot fetch, fallback to centers
        initialValues = {...paramCenters};
    }

    function createCol(def, idx) {
        const col = document.createElement("div");
        col.className = "mixer-col";
        const label = document.createElement("div");
        label.className = "mixer-label";
        label.textContent = def.label;
        col.appendChild(label);

        // Column content
        if (def.type === "vmeter") {
            const vmeter = document.createElement("div");
            vmeter.className = "vmeter";
            vmeter.style.position = "relative";
            const bar = document.createElement("div");
            bar.className = "vmeter-bar";
            bar.style.height = "10%";
            bar.style.background = "#ffe06655";
            vmeter.appendChild(bar);

            // Scale
            const scale = document.createElement("div");
            scale.className = "vmeter-scale";
            scale.innerHTML = "<span>0</span><span>-10</span><span>-20</span><span>-30</span><span>-40</span><span>-50</span>";
            vmeter.appendChild(scale);

            col.appendChild(vmeter);

            // dBFS value
            const value = document.createElement("div");
            value.className = "slider-value";
            value.id = "vmeter-value";
            value.textContent = "-∞ dBFS";
            col.appendChild(value);

            col.vmeterBar = bar;
            col.vmeterValue = value;
        }
        else if (def.type === "lamp") {
            const lamp = document.createElement("div");
            lamp.className = "lamp red";
            lamp.innerHTML = "&nbsp;";
            const stateLabel = document.createElement("div");
            stateLabel.style.marginTop = "10px";
            stateLabel.style.fontSize = "0.95em";
            stateLabel.textContent = def.off_label;
            col.appendChild(lamp);
            col.appendChild(stateLabel);
            col.lamp = lamp;
            col.lampLabel = stateLabel;
            col.lampState = def.state;
            col.lampOn = def.on;
            col.lampOnLabel = def.on_label;
            col.lampOffLabel = def.off_label;
        }
        else if (def.type === "slider") {
            const slider = document.createElement("input");
            slider.type = "range";
            slider.className = "slider-vert";
            slider.min = def.min;
            slider.max = def.max;
            slider.step = def.step;

            // --- Set initial value from backend/status ---
            let initial = initialValues[def.param];
            if (initial === undefined || initial === null) initial = paramCenters[def.param];
            slider.value = initial;

            slider.paramDef = def;

            // --- Add marker for "center" reference value ---
            const marker = document.createElement("div");
            marker.className = "slider-center-marker";
            let centerVal = paramCenters[def.param];
            let percent = (centerVal - def.min) / (def.max - def.min);
            marker.style.top = (100 - percent * 100) + "%";
            col.appendChild(marker);

            // Value display
            const value = document.createElement("div");
            value.className = "slider-value";
            value.id = `sliderval-${def.param}`;
            value.textContent = def.format(Number(slider.value));

            slider.addEventListener("input", function(e) {
                value.textContent = def.format(Number(slider.value));
            });

            slider.addEventListener("change", function(e) {
                // Send updated value to backend
                const param = paramMap[def.param];
                const val = Number(slider.value);
                value.textContent = def.format(val);
                let payload = {};
                payload[param.key] = val;
                fetch(param.api, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
            });

            col.appendChild(slider);
            col.appendChild(value);
            col.slider = slider;
            col.sliderValue = value;
        }
        else if (def.type === "timer") {
            const timer = document.createElement("div");
            timer.className = "timer-col";
            const tlabel = document.createElement("div");
            tlabel.textContent = "Echo Level";
            tlabel.className = "mixer-label";
            timer.appendChild(tlabel);

            const tval = document.createElement("div");
            tval.className = "timer-value";
            tval.textContent = "0.00";
            timer.appendChild(tval);

            col.appendChild(timer);
            col.timerValue = tval;
        }
        return col;
    }

    // --- Render all columns ---
    const mixer = document.getElementById("mixer-columns");
    const colObjs = [];
    for (let i = 0; i < colDefs.length; i++) {
        const col = createCol(colDefs[i], i);
        mixer.appendChild(col);
        colObjs.push(col);
    }

    // --- Poll status and update UI ---
    async function pollStatus() {
        try {
            const resp = await fetch("/api/status");
            const data = await resp.json();
            current = data;

            // Update Vmeter
            if (colObjs[0].vmeterBar && data.last_dbfs !== undefined) {
                let dbfs = data.last_dbfs;
                let pct = Math.max(0, Math.min(1, (dbfs + 50) / 50));
                colObjs[0].vmeterBar.style.height = (pct*100) + "%";
                colObjs[0].vmeterValue.textContent = dbfs === -Infinity ? "-∞ dBFS" : dbfs.toFixed(1) + " dBFS";
            }

            // Update sliders
            for (let c of colObjs) {
                if (c.slider) {
                    let p = c.slider.paramDef.param;
                    let v = null;
                    if (p === "THRESHOLD_DBFS") v = data.threshold_dbfs;
                    else if (p === "LOCKOUT_SEC") v = data.lockout_sec;
                    else if (data.echo_params && p.startsWith("ECHO_")) {
                        if (p === "ECHO_DELAY_SEC") v = data.echo_params.delay_sec;
                        if (p === "ECHO_TAPS") v = data.echo_params.taps;
                        if (p === "ECHO_FEEDBACK") v = data.echo_params.feedback;
                        if (p === "ECHO_START_VOL") v = data.echo_params.start_vol;
                        if (p === "ECHO_END_VOL") v = data.echo_params.end_vol;
                    }
                    if (v !== null && v !== undefined && c.slider.value != v) {
                        c.slider.value = v;
                        c.sliderValue.textContent = c.slider.paramDef.format(v);
                    }
                }
                if (c.lamp) {
                    let state = false;
                    if (c.lampState === "mic_enabled") state = !!data.mic_enabled;
                    if (c.lampState === "echo_active") state = !!(data.echo_params && (data.echo_params.active || data.echo_params.last_triggered));
                    c.lamp.className = "lamp " + (state ? "green" : "red");
                    c.lampLabel.textContent = state ? c.lampOnLabel : c.lampOffLabel;
                }
                if (c.timerValue && data.echo_params) {
                    let start = data.echo_params.start_vol, end = data.echo_params.end_vol;
                    c.timerValue.textContent = (data.echo_params.active ? start : end).toFixed(2);
                }
            }
        } catch (e) {
            // Connection error, set all lamps to red
            for (let c of colObjs) {
                if (c.lamp) {
                    c.lamp.className = "lamp red";
                    c.lampLabel.textContent = c.lampOffLabel;
                }
            }
        }
    }

    setInterval(pollStatus, 600); // Poll every 0.6s
    pollStatus();
});