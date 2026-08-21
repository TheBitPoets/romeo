# Guida docente — secondo anno 3. Porte e servizi

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
associare una porta libera a un socket e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai cos'è un host e sai usare tuple e `with` in Python.

L'indirizzo porta il messaggio all'host; la porta lo consegna al servizio corretto. Un endpoint è quindi la coppia `(indirizzo, porta)`. La porta `0` non è la porta del servizio: durante `bind` chiede al sistema di scegliere temporaneamente una porta disponibile.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Usare soltanto la porta e dimenticare l'indirizzo.
- Pensare che `0` sia la porta finale assegnata.
- Dimenticare di chiudere il socket dopo l'esperimento.

## Inclusione ed evidenze

Rappresenta l'endpoint sia come coppia scritta sia come diagramma. Pronuncia separatamente indirizzo e porta.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
