# Guida docente — secondo anno 9. REST: leggere lo stato

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
consumare una risorsa JSON e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai leggere request e response HTTP e decodificare JSON.

REST tratta gli elementi del sistema come risorse con indirizzi stabili. `GET /api/status` chiede una rappresentazione dello stato; non significa 'esegui una funzione chiamata status'. TestClient sostituisce la rete esterna ma conserva metodo, path, status e body. FastAPI è nascosto nello scaffold fino alla prossima unità.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Chiamare REST qualsiasi risposta JSON.
- Inserire verbi come `getStatus` nel path senza ragionare sulla risorsa.
- Fidarsi del JSON senza controllare lo status.

## Inclusione ed evidenze

Scrivi sempre metodo e path insieme (`GET /api/status`) e accompagna ogni icona con un'etichetta testuale.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
