# Guida docente — secondo anno 12. Controller web

Durata: 80 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
tradurre input UI in messaggi validi e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai associare un'azione a un valore, costruire payload JSON e seguire una conversazione WebSocket ready/comando/ack.

Il controller web ha due responsabilità separate: un'azione su un pulsante sceglie un comando; il trasporto lo invia. Lo scaffold fornisce pagina, connessione e listener del browser. Tu completi una funzione pura che traduce azione in payload, così puoi testarla senza clic reali.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–80 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Mescolare selezione del comando e dettagli del WebSocket in ogni pulsante.
- Inviare stringhe diverse dal protocollo documentato.
- Mostrare stato soltanto tramite colore senza testo.

## Inclusione ed evidenze

Ogni pulsante ha etichetta, focus da tastiera e stato testuale; non usare soltanto colore, hover o posizione per comunicare il comando.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
