---
marp: true
paginate: true
size: 16:9
title: 05 — Romeo Y2: networking e protocolli
---

# 05 — Networking e protocolli

Unità Y2 1–7

---

# Richiamo

Nel primo anno il programma controllava Romeo localmente.

Nel secondo anno separiamo:

```text
controller / client
        ↕ rete
Romeo / server
```

Ora gli errori possono avvenire anche **tra** i componenti.

---

# Obiettivi

- distinguere host, rete, servizio e porta;
- riconoscere indirizzi IPv4;
- spiegare client/server;
- aprire un socket TCP sul loopback;
- definire un protocollo testuale semplice;
- validare messaggi con whitelist;
- serializzare dati JSON senza fidarsi dell'input.

---

# Host, porta, servizio

Un indirizzo identifica un host/interfaccia di rete; una porta identifica il servizio nel contesto del trasporto.

```text
127.0.0.1 : 9000
   host       porta
```

Il numero di porta non è il “numero del computer”.

---

# Client / server

```text
client                    server
connect ────────────────→ listen/accept
send    ────────────────→ recv
recv    ←──────────────── send
close   ────────────────→ close
```

Il protocollo decide **che cosa significano i byte**.

---

# TCP

TCP fornisce uno stream ordinato e affidabile, non messaggi applicativi già separati.

Quindi il protocollo deve decidere framing/delimitazione.

```text
MOVE 0.5 0.5\n
STOP\n
```

---

# Protocollo Romeo/1

Un protocollo semplice è una buona palestra per imparare:

- grammatica;
- whitelist di comandi;
- parsing;
- errori;
- risposta;
- versione del protocollo.

Non eseguire input di rete come codice arbitrario.

---

# JSON

JSON permette di rappresentare dati strutturati:

```json
{"type":"move","left":0.5,"right":0.5}
```

Ma “JSON valido” non significa “comando valido”.

Serve validazione semantica di tipo, range e campi ammessi.

---

# Boundary di fiducia

```text
rete / input esterno
       ↓
parse
       ↓
validate
       ↓
comando interno
```

Ogni messaggio remoto è `untrusted` finché non attraversa i controlli previsti.

---

# Errore tipico

> Assumere che un singolo `recv()` restituisca sempre esattamente un messaggio completo.

TCP è uno stream. Il framing appartiene al protocollo applicativo.

---

# Checkpoint

Spiega la differenza tra:

1. host;
2. porta;
3. socket;
4. protocollo;
5. payload JSON.

Poi indica quale livello decide se `left=3.7` è accettabile per Romeo.

---

# Lab

Usa il server/client Romeo sul loopback prima della rete fisica:

```text
stesso PC
→ protocollo osservabile
→ errori riproducibili
→ poi rete reale
```

Conserva request/response e caso di input rifiutato.

---

# Recap

- rete e servizio sono livelli diversi;
- TCP trasporta stream;
- il protocollo assegna significato;
- JSON rappresenta dati ma non sostituisce la validazione;
- input remoto attraversa un trust boundary.

---

# Prossimo blocco

Portiamo lo stesso modello sul Web:

**HTTP, REST, FastAPI e WebSocket realtime**.