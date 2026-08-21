# Guida docente — secondo anno 14. Camera come servizio

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
usare una camera sostituibile e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai usare oggetti, chiamare metodi e chiudere risorse con `try/finally`.

CameraService è una presa comune: il codice chiede una foto senza sapere se dietro c'è Picamera2 o un mock. Il mock restituisce dati prevedibili in classe e CI. La camera reale richiede hardware, permesso e segnalazione chiara; questi dettagli restano nell'implementazione del servizio.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Importare direttamente Picamera2 nel programma applicativo.
- Stampare migliaia di byte della foto.
- Dimenticare privacy e chiusura della camera su errore.

## Inclusione ed evidenze

Descrivi testualmente stato camera e risultato; prevedi attività completa col mock per chi non può usare o essere ripreso dalla camera.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
