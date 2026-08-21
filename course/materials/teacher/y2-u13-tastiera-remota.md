# Guida docente — secondo anno 13. Tastiera remota sicura

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
separare la mappa dei tasti dal trasporto e garantire lo stop finale e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai trasformare un valore con una funzione e conosci il protocollo testuale e lo STOP WebSocket.

La tastiera produce tasti, ma il robot accetta comandi. Una funzione pura converte W/A/S/D/SPACE; un client separato trasporta il comando. Lo scaffold gestisce le differenze del terminale e la connessione: lo studente non deve leggere direttamente caratteri grezzi dal sistema operativo.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Inviare il tasto grezzo invece del comando di protocollo.
- Dimenticare SPACE o lo STOP finale.
- Dipendere da una API terminal-specific non presente sul computer dello studente.

## Inclusione ed evidenze

Mantieni anche pulsanti cliccabili e rimappabili; stampa il comando riconosciuto e non richiedere pressioni simultanee.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
