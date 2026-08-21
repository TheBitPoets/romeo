# Guida docente — secondo anno 7. Dati JSON

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
serializzare e validare un messaggio e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai usare dizionari, liste, stringhe, numeri e booleani Python.

JSON è testo con una struttura condivisa. `json.dumps` trasforma un oggetto Python in testo da inviare; `json.loads` ricostruisce dati Python dal testo. JSON non apre connessioni e non esegue comandi.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Confondere un dizionario con il testo JSON che lo rappresenta.
- Scrivere `True` a mano nel JSON, dove il valore è `true`.
- Usare campi ricevuti senza verificarne presenza e tipo.

## Inclusione ed evidenze

Mostra dict e JSON su righe separate con etichette; non segnalare le differenze solo con colori.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
