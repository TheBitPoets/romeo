# Secondo anno 11. WebSocket bidirezionale

## Obiettivo

In questa unità imparerai a mantenere una connessione per comandi realtime.

## Che cosa sai già

Conosci HTTP, JSON e FastAPI; sai usare un context manager.

## Modello mentale

HTTP normale apre uno scambio request/response; WebSocket mantiene un canale aperto in cui entrambe le parti possono inviare messaggi. Lo scaffold fornisce server e gestione asincrona: il client didattico usa TestClient sincrono, così il nuovo concetto è soltanto la conversazione persistente.

## Esempio minimo commentato

```python
with client.websocket_connect("/ws/control") as ws:
    pronto = ws.receive_json()
    ws.send_json({"command": "STOP"})
    risposta = ws.receive_json()
```

```text
server → ready
client → STOP
server → ack
```

L'ordine fa parte del protocollo; la chiusura del `with` termina la connessione.

## Prova guidata

1. Confronta una timeline HTTP con quella WebSocket.
2. Numera ready, comando e ack.
3. Collegati al server fornito e verifica `ready`.
4. Invia STOP e valida l'ack completo.
5. Chiudi senza inviare altri dati e verifica che il robot resti fermo.

## Esercizio base

Completa la conversazione ready→STOP→ack.

## Esercizio intermedio

Invia un comando invalido e verifica una risposta error senza perdere la connessione.

## Mini-sfida

Disegna come heartbeat o timeout rileverebbero un client scomparso, senza implementarli qui.

## Consegna valutata

Completa `request_stop` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: mantenere una connessione per comandi realtime.

## Errori tipici

- Inviare prima di leggere il messaggio ready previsto.
- Confondere WebSocket con una serie di GET HTTP.
- Uscire senza verificare lo STOP alla disconnessione.

## Autoverifica

- So spiegare perché la connessione resta aperta?
- So indicare chi invia ogni messaggio?
- So descrivere cosa deve accadere alla chiusura?

## Accessibilità

La sequenza dei messaggi è disponibile come elenco testuale oltre alle frecce; gli ack sono leggibili e non dipendono da animazioni.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `WebSocket` | canale persistente e bidirezionale |
| `frame` | unità trasmessa sul WebSocket |
| `ack` | risposta che conferma la gestione del messaggio |
