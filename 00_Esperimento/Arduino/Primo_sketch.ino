#include <SPI.h>
#include <WiFi.h> // Libreria per la shield WiFi ufficiale

// --- Impostazioni WiFi ---
// Sostituisci queste stringhe con il nome e la password della tua rete WiFi
const char* ssid     = "NOME_TUA_RETE";
const char* password = "PASSWORD_WIFI";

// Crea un server TCP sulla porta 8080
WiFiServer server(8080);

// Pin su cui è collegato il LED (pin 13 = LED integrato su Arduino Uno)
const int ledPin = 13;

void setup() {
  // Imposta il pin del LED come uscita
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // All'avvio il LED è spento

  Serial.begin(9600); // Per eventuali messaggi di debug su Seriale

  Serial.println("Connessione al WiFi...");
  // Avvia la connessione alla rete WiFi
  WiFi.begin(ssid, password);

  // Attendi finché la connessione non è stabilita
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connesso!");

  // Avvia il server TCP sulla porta specificata
  server.begin();
}

void loop() {
  // Verifica se ci sono client collegati (es. PC o web app)
  WiFiClient client = server.available();

  if (client) {
    // Leggi la stringa inviata dal client fino a newline ('\n')
    String command = client.readStringUntil('\n');
    command.trim(); // Rimuove eventuali spazi o caratteri di invio

    // Gestione dei comandi
    if (command == "LED_ON") {
      digitalWrite(ledPin, HIGH); // Accende il LED
      client.println("LED_ON_OK"); // Risposta di conferma al client
    } else if (command == "LED_OFF") {
      digitalWrite(ledPin, LOW);  // Spegne il LED
      client.println("LED_OFF_OK"); // Risposta di conferma al client
    } else {
      client.println("UNKNOWN_CMD"); // Comando non riconosciuto
    }
    client.stop(); // Chiudi la connessione con il client
  }
}