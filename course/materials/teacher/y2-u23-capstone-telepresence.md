# Guida docente — secondo anno 23. Capstone telepresenza

Durata: 120 minuti. Difficoltà: C. Obiettivo osservabile: lo studente sa
integrare video, controllo, telemetria e safety e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Hai completato foto/video, controller, telemetria, safety e integrazione e sai documentare test e failure.

La telepresenza è un sistema a strati: input → controllo sicuro → Robot API → backend, mentre camera e telemetria riportano ciò che accade. Il capstone non richiede di riscrivere server o framework: lo scaffold fornisce infrastruttura, e il gruppo integra, verifica e spiega i confini. Ogni incremento deve lasciare Romeo fermo.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–120 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Assemblare componenti senza verificare ogni incremento.
- Mostrare movimento e video ma non i failure mode.
- Usare il robot reale prima di superare mock, simulazione e checklist safety.

## Inclusione ed evidenze

La demo offre pulsanti, tastiera rimappabile e log testuale; video e colore non sono l'unica evidenza. Definire ruoli di gruppo ruotabili e consenso camera.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
