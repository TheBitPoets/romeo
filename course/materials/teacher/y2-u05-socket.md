# Guida docente — secondo anno 5. Un vero socket TCP

Durata: 70 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
aprire server e client sul loopback e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai scambiare byte su una coppia locale e conosci indirizzo, porta, client e server.

Un server TCP prepara un punto di ascolto con `bind` e `listen`; `accept` crea un nuovo socket dedicato a un client. Il client usa `connect`. Per far avanzare server e client nello stesso programma lo scaffold avvia il server in un thread: la concorrenza è fornita, non è l'obiettivo da implementare oggi.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–70 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Chiamare `connect` prima che il listener sia pronto.
- Confondere il socket listener con quello della connessione accettata.
- Usare `recv` senza timeout durante il debug.

## Inclusione ed evidenze

Fornisci anche una sequenza numerata testuale del diagramma temporale. Lo scaffold evita che difficoltà con i thread oscurino il concetto di TCP.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
