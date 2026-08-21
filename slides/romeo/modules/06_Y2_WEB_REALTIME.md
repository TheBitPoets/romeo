---
marp: true
paginate: true
size: 16:9
title: 06 — Romeo Y2: Web e realtime
---

# 06 — HTTP, REST, FastAPI e realtime

Unità Y2 8–13

---

# Richiamo

Abbiamo già separato:

```text
trasporto → protocollo → payload → validazione
```

HTTP aggiunge un protocollo applicativo standard con metodo, URL, status, header e body.

---

# Obiettivi

- leggere request/response HTTP;
- distinguere stato e comando in una API REST;
- creare endpoint FastAPI tipizzati;
- capire perché WebSocket serve al realtime bidirezionale;
- tradurre input UI/tastiera in messaggi validi;
- preservare lo stop finale e la safety anche da remoto.

---

# HTTP

```text
GET /state HTTP/1.1
        ↓
200 OK
Content-Type: application/json
...
```

Non guardare solo il JSON: metodo e status fanno parte del contratto.

---

# REST: leggere lo stato

Una risorsa di stato permette a un client di chiedere una fotografia autorevole:

```text
GET /api/state
```

Il renderer/UI non deve diventare la fonte di verità.

---

# FastAPI

Un endpoint tipizzato rende espliciti boundary e validazione:

```python
@app.get('/state')
def state() -> StateResponse:
    ...
```

Il tipo documenta e aiuta a verificare il contratto, ma non sostituisce la logica di dominio.

---

# Command path vs state path

Modello utile:

```text
client → comando validato → Romeo
client ← stato/telemetria ← Romeo
```

Separare comando e osservazione riduce accoppiamento e rende più facile il debug.

---

# WebSocket

HTTP request/response è ottimo per molte operazioni.

Per controllo realtime bidirezionale può servire una connessione persistente:

```text
browser ⇄ WebSocket ⇄ controller
```

Persistente non significa “senza regole”: servono ownership, validazione e timeout.

---

# Controller web

La UI produce intenzioni:

```text
pulsante avanti
→ evento UI
→ messaggio validato
→ comando Romeo
```

Non lasciare che dettagli del DOM entrino direttamente nel backend/hardware layer.

---

# Tastiera remota

Separare:

```text
mappa tasti
trasporto
comando interno
```

La tastiera è soltanto una sorgente di input sostituibile.

La sessione deve garantire stop alla chiusura/perdita del controllo prevista dal protocollo.

---

# Errore tipico

> Tenere l'ultimo comando di movimento indefinitamente se il client scompare.

Nel controllo fisico la perdita di connessione è un evento da gestire, non una condizione neutra.

---

# Checkpoint

Scegli HTTP o WebSocket e motiva:

1. leggere una fotografia JPEG;
2. recuperare lo stato corrente;
3. inviare aggiornamenti continui di un joystick;
4. leggere un catalogo di missioni;
5. notificare eventi realtime al controller.

---

# Lab

Lavora prima con backend simulato:

```text
client web/tastiera
→ API/WebSocket
→ simulatore
→ stato/event log
```

Solo dopo verifica che lo stesso contratto possa collegarsi al backend autorizzato.

---

# Recap

- HTTP rende espliciti request/response;
- REST espone risorse/stato;
- FastAPI formalizza endpoint e tipi;
- WebSocket abilita canale persistente;
- UI e trasporto devono restare separati;
- perdita controller deve avere una policy di safety.

---

# Prossimo blocco

Aggiungiamo percezione e osservabilità:

**camera, pan/tilt, eventi, gamepad e telemetria**.