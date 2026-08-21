# Guida docente — secondo anno 8. Una richiesta HTTP

Durata: 75 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
riconoscere metodo, status e body e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Conosci client/server, endpoint, protocollo testuale e JSON.

HTTP organizza uno scambio in request e response. La request contiene metodo e risorsa; la response contiene status, header e body. Il server e il thread sono già nello scaffold: oggi leggiamo il protocollo, non implementiamo ancora un server web.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–75 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Guardare soltanto il body e ignorare lo status.
- Confondere metodo HTTP e nome della funzione Python.
- Costruire subito server, thread e handler senza isolare il concetto HTTP.

## Inclusione ed evidenze

Presenta request e response come testo copiabile oltre al diagramma; pronuncia i codici cifra per cifra e spiegane il significato.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
