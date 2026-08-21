# Guida docente — secondo anno 11. WebSocket bidirezionale

Durata: 75 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
mantenere una connessione per comandi realtime e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci HTTP, JSON e FastAPI; sai usare un context manager.

HTTP normale apre uno scambio request/response; WebSocket mantiene un canale aperto in cui entrambe le parti possono inviare messaggi. Lo scaffold fornisce server e gestione asincrona: il client didattico usa TestClient sincrono, così il nuovo concetto è soltanto la conversazione persistente.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–75 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Inviare prima di leggere il messaggio ready previsto.
- Confondere WebSocket con una serie di GET HTTP.
- Uscire senza verificare lo STOP alla disconnessione.

## Inclusione ed evidenze

La sequenza dei messaggi è disponibile come elenco testuale oltre alle frecce; gli ack sono leggibili e non dipendono da animazioni.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
