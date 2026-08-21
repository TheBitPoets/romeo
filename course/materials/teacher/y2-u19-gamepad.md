# Guida docente — secondo anno 19. Controller analogico

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
convertire assi in velocità ruote e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci eventi, velocità delle due ruote, funzioni e numeri fra -1 e 1.

Lo stick produce due assi. Prima applichiamo una dead-zone per ignorare piccoli tremolii, poi mescoliamo avanti e sterzo nelle velocità sinistra/destra e infine limitiamo il risultato. pygame e il dispositivo sono nello scaffold: la funzione matematica resta testabile con numeri simulati.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Dimenticare che l'asse Y può essere invertito.
- Inviare il rumore vicino allo zero ai motori.
- Mescolare lettura pygame e matematica rendendo impossibili i test senza gamepad.

## Inclusione ed evidenze

Offri tastiera e pulsanti come input equivalenti; mostra numericamente assi e ruote e consenti rimappatura.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
