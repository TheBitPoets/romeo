# Guida docente — secondo anno 6. Il protocollo Romeo/1

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
analizzare comandi testuali con una whitelist e giustifica protocollo, validazione e cleanup.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output viene valutato soltanto se il programma arriva alla relativa stampa; chiedere
agli studenti di mantenerlo dopo gli assert, mai prima. Per valutazioni sommative aggiungere test
riservati nel sandbox TheBitLab: i check dichiarativi sono feedback trasparente, non una barriera
anti-manomissione.

## Misconcezioni e safety

`localhost` non è il Raspberry Pi remoto; una porta non identifica da sola un protocollo; JSON non
è una connessione; REST e WebSocket non sono sinonimi. Una UI chiusa deve causare STOP, e il
watchdog resta obbligatorio. Evitare rete pubblica e camera reale senza autorizzazioni e informativa.

## Inclusione ed evidenze

Fornire diagrammi con colori per endpoint e frecce. Permettere prima una simulazione con coppie di
socket o TestClient. Estensione: introdurre un payload non valido e progettare l'errore. Evidenze:
sorgente, marker, gestione errori, chiusura risorse e spiegazione orale. Collegare il debrief alla
prossima unità senza anticipare più di un nuovo livello di protocollo.
