# Guida docente — secondo anno 2. Indirizzi IP

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
risolvere un nome e riconoscere IPv4 e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai distinguere host, rete e servizio e sai usare stringhe e confronti in Python.

Un indirizzo IP identifica un'interfaccia di rete, come un numero civico identifica una destinazione. Un nome come `localhost` è più facile da ricordare e viene risolto in un indirizzo. Il paragone postale non è perfetto: un host può avere più indirizzi e un indirizzo può cambiare.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Confondere il nome `localhost` con il suo indirizzo numerico.
- Controllare soltanto che il testo contenga punti invece di validarlo.
- Usare l'indirizzo locale pensando di raggiungere il Raspberry Pi remoto.

## Inclusione ed evidenze

Leggi gli indirizzi anche cifra per cifra; non affidarti alla sola posizione in un diagramma e lascia il risultato testuale copiabile.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
