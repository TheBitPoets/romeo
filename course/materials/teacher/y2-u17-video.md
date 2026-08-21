# Guida docente — secondo anno 17. Stream MJPEG

Durata: 70 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
riconoscere frame e boundary e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai leggere byte JPEG e una response HTTP; conosci iteratori e `next` grazie a uno scaffold guidato.

MJPEG invia una sequenza di immagini JPEG dentro una response HTTP multipart. Un boundary separa i frame, come un divisore etichettato. Lo scaffold costruisce server e generatore: lo studente osserva due parti e verifica la struttura, senza implementare streaming o concorrenza da zero.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–70 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Chiamare MJPEG un singolo byte array JPEG.
- Confondere boundary e marker interni JPEG.
- Creare un ciclo infinito senza condizione di arresto o cleanup.

## Inclusione ed evidenze

Fornisci frame campione e struttura testuale; il risultato può essere verificato con contatori e status senza dover vedere il video.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
