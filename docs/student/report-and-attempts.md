# Capire il report e i tentativi

Dopo l'esecuzione TheBitLab produce un report. Non leggerlo soltanto come "verde" o "rosso": usalo come strumento di debug.

## Quattro domande

Quando un test fallisce chiediti, nell'ordine:

1. **Il programma è partito?** Se no, guarda prima errori di sintassi/import.
2. **Ha fatto la sequenza giusta?** Confronta comandi ed eventi.
3. **Ha raggiunto il comportamento richiesto?** Controlla traiettoria, checkpoint, stato finale o test comportamentali.
4. **È terminato in sicurezza?** Verifica stop, timeout e stato dei motori quando l'Activity lo richiede.

## Test pubblici e controlli riservati

Alcune verifiche possono essere spiegate in dettaglio allo studente. Altre sono comportamentali e non mostrano ogni dato interno: servono a valutare ciò che il programma *fa*, non a suggerire una stringa da stampare.

Il report studente deve comunque dire abbastanza per correggere il lavoro senza esporre soluzioni o expected outcome riservati.

## Un tentativo non è un voto definitivo

Nel normale workflow puoi eseguire più prove. Usa i tentativi intermedi per imparare e correggere; seleziona come definitivo solo quello che rappresenta il lavoro che vuoi consegnare.

## Metodo di debug consigliato

Cambia una cosa alla volta. Se modifichi contemporaneamente velocità, durata, direzione e struttura del programma, non saprai quale modifica ha corretto o peggiorato il comportamento.

Annota mentalmente o sul quaderno:

- cosa pensavo sarebbe successo;
- cosa è successo;
- quale evidenza lo mostra;
- quale singola modifica provo adesso.

Questo stesso metodo sarà ancora più importante sul robot reale, dove entrano in gioco anche fattori fisici.
