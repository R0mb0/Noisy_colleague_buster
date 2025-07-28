const express = require('express');
const net = require('net');
const path = require('path');

const ARDUINO_IP = '192.168.1.123'; // Sostituisci con l'IP del tuo Arduino
const ARDUINO_PORT = 8080;

const app = express();
const PORT = 3000;

// Serve file statici (la GUI)
app.use(express.static(path.join(__dirname, 'public')));

// Funzione per inviare comando ad Arduino via TCP
function sendCommandToArduino(command) {
    return new Promise((resolve, reject) => {
        const client = new net.Socket();
        let dataReceived = '';

        client.connect(ARDUINO_PORT, ARDUINO_IP, function() {
            client.write(command + '\n');
        });

        client.on('data', function(data) {
            dataReceived += data.toString();
        });

        client.on('end', function() {
            resolve(dataReceived.trim());
        });

        client.on('error', function(err) {
            reject(err);
        });

        client.on('close', function() {});
    });
}

// API REST per accensione/spegnimento LED (usate dalla GUI)
app.post('/api/led/:action', express.json(), async (req, res) => {
    const action = req.params.action;
    let command = '';
    if (action === 'on') command = 'LED_ON';
    else if (action === 'off') command = 'LED_OFF';
    else {
        return res.status(400).json({error: 'Comando non valido'});
    }
    try {
        const result = await sendCommandToArduino(command);
        res.json({result});
    } catch (err) {
        res.status(500).json({error: 'Errore comunicazione: ' + err.message});
    }
});

// Pagina principale (serve la GUI)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Web-app disponibile su http://localhost:${PORT}`);
    console.log(`Invierà i comandi a Arduino su ${ARDUINO_IP}:${ARDUINO_PORT}`);
});