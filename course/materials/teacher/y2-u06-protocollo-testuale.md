# Guida docente — secondo anno 6. Il protocollo Romeo/1

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
analizzare comandi testuali con una whitelist e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai scambiare righe di byte e usare `split`, condizioni e conversioni numeriche.

Un protocollo è un accordo preciso sul significato dei messaggi. Romeo/1 usa una riga per comando: prima una parola ammessa, poi gli eventuali argomenti. Una whitelist elenca ciò che è valido; tutto il resto viene rifiutato senza eseguire azioni.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Accettare qualsiasi parola e passarla direttamente al robot.
- Dimenticare di convertire e limitare la velocità.
- Ignorare il fine riga e unire due comandi ricevuti insieme.

## Inclusione ed evidenze

La tabella del protocollo usa testo e non colori. Leggi gli errori con una motivazione breve e stabile.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
