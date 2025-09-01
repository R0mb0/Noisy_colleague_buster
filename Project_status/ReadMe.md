# Roadmap Dettagliata — Dispositivo IoT Anti Collega Fastidioso (Raspberry Pi + Python + ThingSpeak)

Questa guida elenca in ordine tutti i sottoproblemi e obiettivi da raggiungere per completare il progetto.  
Ogni punto corrisponde a una fase concreta dello sviluppo, dalla configurazione hardware alla visualizzazione dei dati sul cloud.

---

## 1. Preparazione Hardware

- [X] **Procurare e assemblare i componenti:**
  - Raspberry Pi 3B+ con alimentazione
  - Microfono USB compatibile
  - Altoparlante (jack 3.5mm o USB)
- [X] **Collegare il microfono USB e verificare che venga riconosciuto dal sistema**
- [X] **Collegare l’altoparlante e verificarne il funzionamento audio**

---

## 2. Configurazione di Sistema

- [X] **Installare Raspberry Pi OS (Legacy) with Desktop**
- [X] **Aggiornare il sistema operativo e i pacchetti**
- [X] **Abilitare e testare la connessione di rete (LAN/WiFi)**
- [X] **Configurare accesso SSH e SFTP per gestione remota**
- [X] **Installare Python 3 e pip**
- [X] **Installare librerie audio Python (PyAudio, SoX, ALSA, ecc.)**

---

## 3. Acquisizione Audio

- [X] **Scrivere uno script Python per rilevare il microfono collegato**
- [X] **Testare la registrazione di audio dal microfono**
- [X] **Implementare la lettura continua del livello di volume (RMS o altro)**
- [X] **Gestire errori di acquisizione o assenza microfono**

---

## 4. Gestione Soglia di Rumore

- [X] **Definire una soglia di intervento modificabile (da file di configurazione)**
- [X] **Implementare la logica di confronto tra volume rilevato e soglia**
- [X] **Permettere la modifica della soglia senza riavviare il sistema**

---

## 5. Attivazione Eco/Disturbo

- [ ] **Implementare funzione di eco/disturbo audio**
  - Semplice delay audio (loopback con ritardo)
  - Alternativamente, riproduzione di un suono pre-registrato
- [ ] **Testare la riproduzione audio sull’altoparlante**
- [ ] **Attivare l’effetto solo quando il volume supera la soglia**

---

## 6. Registrazione degli Eventi

- [ ] **Salvare timestamp e livello rumore ogni volta che si attiva il disturbo**
- [ ] **Archiviare gli eventi in locale (file CSV o database leggero)**
- [ ] **Gestire rotazione/backup dei dati locali**

---

## 7. Invio Dati a ThingSpeak

- [X] **Registrare un account ThingSpeak e creare un canale**
- [ ] **Configurare API KEY e parametri di accesso**
- [ ] **Implementare invio dati (timestamp, livello rumore) via HTTP REST API**
- [ ] **Gestire errori di invio e ritentativi**

---

## 8. Visualizzazione e Analisi Cloud

- [ ] **Verificare la ricezione e visualizzazione degli eventi su ThingSpeak**
- [ ] **Configurare dashboard e grafici per analisi temporale e statistica**
- [ ] **Testare la visualizzazione dei dati da vari dispositivi/remotamente**
- [ ] **Documentare il processo di visualizzazione**

---

## 9. Ottimizzazione e Manutenzione

- [ ] **Documentare il codice e scrivere README**
- [ ] **Automatizzare avvio script Python all’accensione del Raspberry Pi**
- [ ] **Gestire aggiornamenti software e sicurezza**
- [ ] **Prevedere notifiche/alert (opzionale)**
- [ ] **Testare e validare tutto il sistema in condizioni reali**

---

## 10. Estensioni Future (Facoltative)

- [X] **Interfaccia Web locale su Raspberry Pi per gestione/configurazione**
- [ ] **Aggiunta di altre metriche (temperatura, presenza, ecc.)**
- [ ] **Supporto multi-device e aggregazione dati da più stanze**
- [ ] **Integrazione con altri servizi cloud o bot Telegram per notifiche**

---

**Seguendo questa roadmap, puoi affrontare il progetto in modo strutturato e risolvere ogni sottoproblema passo passo fino al completamento del dispositivo IoT!**
