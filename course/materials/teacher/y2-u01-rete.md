# Guida docente — secondo anno 1. Una rete di nodi

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
distinguere host, rete e servizio e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai eseguire un programma Python, usare variabili e leggere un semplice diagramma con frecce.

Una rete è un insieme di dispositivi che possono scambiarsi dati. Immagina una scuola: l'host è una persona, la rete è il sistema di corridoi e il servizio è lo sportello a cui la persona si rivolge. L'analogia aiuta a separare i ruoli, ma i dati viaggiano in piccoli blocchi e non come persone intere. `127.0.0.1` è il percorso speciale con cui un host parla a sé stesso.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Confondere la rete con Internet: una rete può esistere anche senza accesso esterno.
- Chiamare servizio l'intero Raspberry Pi: il Raspberry Pi è l'host che ospita uno o più servizi.
- Pensare che loopback indichi Romeo: indica sempre il computer che esegue il programma.

## Inclusione ed evidenze

Usa etichette e forme oltre ai colori nel diagramma. È possibile descrivere a voce il percorso come elenco ordinato.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
