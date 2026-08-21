# Guida docente — secondo anno 20. Telemetria versionata

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
leggere stato senza dipendere dal renderer e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci JSON, schema, coordinate del simulatore e WebSocket.

La telemetria è una fotografia strutturata dello stato inviata nel tempo. `schema_version` dice al client come leggere i campi; pose, motori, camera e tempo hanno nomi e unità documentati. Il renderer è soltanto un consumatore: il test può leggere gli stessi dati senza browser.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Leggere campi prima di controllare la versione.
- Confondere tempo simulato e ora del computer.
- Dipendere da coordinate o elementi HTML del viewer.

## Inclusione ed evidenze

Presenta la telemetria come tabella e JSON copiabile; non affidarti soltanto all'animazione del viewer.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
