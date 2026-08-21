---
marp: true
paginate: true
size: 16:9
title: 07 — Romeo Y2: camera, eventi e telemetria
---

# 07 — Camera, eventi e telemetria

Unità Y2 14–20

---

# Richiamo

Un controller remoto non ha bisogno soltanto di inviare comandi.

Deve anche **osservare** ciò che il sistema sta facendo.

```text
comando → Romeo
stato/video ← Romeo
```

---

# Obiettivi

- trattare la camera come servizio sostituibile;
- controllare pan/tilt attraverso l'API del robot;
- distinguere foto e stream;
- capire eventi vs polling fragile;
- mappare assi analogici in comandi ruote;
- usare telemetria versionata indipendente dal renderer.

---

# Camera come adapter

```text
app
 ↓
Camera interface
 ↓
mock | Picamera2
```

Come per i motori, il codice superiore non dovrebbe dipendere dai dettagli hardware quando non è necessario.

---

# Pan / tilt

Un servo fisico ha limiti reali.

Il contratto software deve rispettare range conservativi e configurazione dell'esemplare.

Nel simulatore possiamo testare intenzione e protocollo; nel commissioning si verificano limiti fisici sicuri.

---

# Foto vs stream

**Fotografia REST**:

```text
request → JPEG singolo → response finita
```

**MJPEG stream**:

```text
connessione lunga → frame/boundary → frame/boundary → ...
```

Sono contratti diversi.

---

# Media type e framing

Un client deve sapere che cosa sta ricevendo.

Headers/boundary non sono dettagli estetici: permettono al ricevente di interpretare correttamente i byte.

---

# Event-driven

Polling fragile:

```text
while True:
    chiedi_stato()
    sleep(...)
```

Eventi:

```text
quando succede X → reagisci
```

L'event-driven riduce lavoro inutile, ma richiede lifecycle e gestione degli handler.

---

# Gamepad analogico

Gli assi del controller diventano intenzioni di movimento.

Esempio concettuale differential drive:

```text
forward + turn → left/right wheel speeds
```

Serve normalizzazione, dead-zone e limiti, non passaggio cieco dei valori hardware.

---

# Telemetria

La telemetria deve essere leggibile senza dipendere dal renderer specifico.

```json
{"version":1,"motion":"stopped","controller":"web"}
```

La versione rende possibile evolvere il formato in modo controllato.

---

# Errore tipico

> Usare il video come unica fonte di stato del sistema.

Il video aiuta l'operatore, ma stato strutturato e telemetria sono più adatti a test, automazione e debug.

---

# Checkpoint

Quale canale useresti per:

1. un JPEG singolo;
2. un flusso continuo di immagini;
3. velocità ruote correnti;
4. evento “controller perso”;
5. input analogico del gamepad.

Indica anche il boundary di validazione.

---

# Lab

Componi una sessione simulata con:

```text
controller
+ stato/telemetria
+ evento
+ camera mock
```

Verifica che la logica non richieda una camera fisica per essere testata.

---

# Recap

- camera e gamepad sono adapter sostituibili;
- foto e stream hanno contratti diversi;
- eventi ≠ polling continuo;
- telemetria strutturata è una API;
- limiti fisici appartengono al boundary hardware/safety.

---

# Prossimo blocco

Integrare tutto significa affrontare il problema più importante:

**chi controlla il robot, per quanto tempo e che cosa succede quando qualcosa si interrompe?**