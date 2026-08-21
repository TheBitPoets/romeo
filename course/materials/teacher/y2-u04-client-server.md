# Guida docente — secondo anno 4. Client e server

Durata: 60 minuti. Difficoltà: B. Obiettivo osservabile: lo studente sa
scambiare byte tra due endpoint e giustifica protocollo, validazione e cleanup.

## Prerequisiti e modello mentale

Sai distinguere host e servizio, conosci gli endpoint e sai usare byte letterali come `b"PING"`.

Il client avvia una richiesta; il server attende e risponde. In questa prima prova `socketpair` crea due estremità locali già collegate: nasconde indirizzi, porte e apertura della connessione per farci osservare soltanto lo scambio di byte. Non è ancora un server TCP reale.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–60 min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output offre soltanto feedback formativo ed è banalmente riproducibile. Non usarlo
come prova sommativa. Finché il runtime non viene eseguito dentro il boundary ufficiale TheBitLab,
anche gli assert e i check comportamentali presuppongono una submission collaborativa.

## Misconcezioni e safety

- Inviare una stringa invece di byte.
- Leggere prima che l'altra estremità abbia inviato.
- Credere che `recv(16)` restituisca sempre esattamente 16 byte.

## Inclusione ed evidenze

Affianca alle frecce parole `invia` e `riceve`; recita la sequenza in ordine per chi non usa il diagramma.

Le evidenze sono sorgente, comportamento osservato, gestione degli errori, cleanup e spiegazione
orale. Il marker, da solo, non dimostra la competenza.
