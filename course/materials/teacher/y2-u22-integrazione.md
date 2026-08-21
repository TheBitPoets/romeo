# Guida docente — secondo anno 22. Integra controllo e stato

Durata: 90 minuti. Difficoltà: C. Obiettivo osservabile: lo studente sa
collegare comando realtime e telemetria e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Hai completato WebSocket control, telemetria versionata e safety con disconnect.

L'integrazione collega due flussi senza confonderli: `/ws/control` riceve intenzioni e restituisce ack; `/ws/state` pubblica telemetria. Entrambi usano la stessa API Robot e lo stesso safety boundary. Lo scaffold fornisce app e connessioni; lo studente completa la sequenza e le verifiche end-to-end.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–90 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo e non è prova sommativa. Il risultato è
autorevole solo quando il runtime usa il sandbox broker TheBitLab e un'immagine Romeo identificata
da digest; il run locale resta esplicitamente diagnostico.

## Misconcezioni e safety

- Usare REST polling e chiamarlo telemetria realtime.
- Considerare l'ack prova sufficiente del movimento.
- Chiudere il viewer ma lasciare vivo il controller senza timeout.

## Inclusione ed evidenze

Ack e telemetria sono disponibili come log testuale; il controller include pulsanti oltre a tastiera e gamepad.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
