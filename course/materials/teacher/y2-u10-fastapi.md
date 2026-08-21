# Guida docente — secondo anno 10. Costruisci una API FastAPI

Durata: 75 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
definire un endpoint tipizzato e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai definire funzioni Python e conosci route REST, status e JSON.

FastAPI collega una coppia metodo+path a una normale funzione Python. Il decorator `@app.get` registra la route: non cambia il ragionamento dentro la funzione. TestClient avvia l'app in memoria; nasconde socket e thread per farci concentrare sulla route.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–75 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Dimenticare `@` davanti al decorator.
- Restituire testo che sembra JSON invece di un dizionario Python.
- Confondere il path della route con il nome della funzione.

## Inclusione ed evidenze

Mostra il codice con annotazioni testuali, non solo evidenziazione sintattica; fornisci una tabella route→funzione.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
