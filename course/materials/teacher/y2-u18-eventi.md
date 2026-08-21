# Guida docente — secondo anno 18. Programmazione a eventi

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
reagire a eventi senza polling fragile e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai definire funzioni, usare condizioni, liste e cicli brevi.

Un evento descrive qualcosa che è accaduto; un handler è una funzione che decide come reagire. Il dispatcher consegna ogni evento all'handler. Lo scaffold contiene il ciclo della coda: oggi scriviamo reazioni semplici, non callback, async o event loop complessi. Questa unità va studiata prima dei controller interattivi.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Mettere tutta la logica nel ciclo invece che nell'handler testabile.
- Eseguire movimento per eventi sconosciuti.
- Confondere ordine della coda e priorità degli eventi.

## Inclusione ed evidenze

Gli eventi possono provenire da pulsante, tastiera o dati simulati; mostra sempre una traccia testuale ordinata.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
