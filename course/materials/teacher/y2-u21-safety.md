# Guida docente — secondo anno 21. Safety di rete

Durata: 75 minuti. Difficoltà: C. Obiettivo osservabile: lo studente sa
applicare ownership, timeout e stop e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci controllo remoto, timeout, mock backend e test deterministici.

Il controllo è un permesso temporaneo: un solo controller possiede il lease. Ogni comando valido rinnova il tempo; il watchdog ferma i motori quando scade. Release, disconnect, eccezione e shutdown devono tutti portare allo stesso stato sicuro: velocità zero. Il test usa clock e watchdog controllati dallo scaffold.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–75 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Disattivare il watchdog proprio nel test che dovrebbe verificarlo.
- Fermare solo un motore.
- Affidarsi allo STOP manuale come unico percorso sicuro.

## Inclusione ed evidenze

La timeline è anche un elenco numerato; stato owner, tempo residuo e motori sono disponibili come testo.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
