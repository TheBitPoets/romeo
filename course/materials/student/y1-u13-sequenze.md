# 13. Progetta una sequenza

## Obiettivo

In questo laboratorio imparerai a ordinare azioni e durate per una missione. Le parole chiave sono: algoritmo, ordine, stato.
Lavora prima nel simulatore: puoi ripetere la prova senza rischiare il robot fisico e il clock
simulato rende ogni esecuzione confrontabile con la precedente.

## Procedura

1. Apri `starter.py` e individua import, istruzioni già presenti e commenti.
2. Prevedi su carta cosa dovrebbe accadere, compreso lo stato finale dei motori.
3. Modifica poche righe alla volta e premi Run in TheBitLab.
4. Leggi il feedback di ogni controllo; usa traiettoria ed event log se il risultato sorprende.
5. Termina sempre esplicitamente con `stop()` quando hai mosso Romeo.

## Consegna

Avanza, ruota a sinistra, avanza ancora e fermati.

Le velocità sono numeri normalizzati: `0` significa fermo e `1` è il massimo consentito.
Valori negativi in `Robot.drive(sinistra, destra)` fanno girare una ruota all'indietro.
`sleep(secondi)` fa avanzare il tempo simulato; sul robot reale rappresenta tempo reale.

## Errori utili

- `NameError`: controlla di avere importato e scritto correttamente il nome.
- `TypeError`: verifica parentesi e tipo dell'argomento.
- Romeo non si ferma: aggiungi `stop()` e controlla il flusso del programma.
- La missione fallisce di poco: non cambiare tutto; osserva posa finale, tempo e tolleranza.

## Mini-sfida e autoverifica

Prima di eseguire, cambia un solo valore e annota la tua previsione. Poi ripristina la soluzione
della consegna. Sai spiegare quale backend riceve il comando? Sai indicare lo stato finale delle
ruote? Sapresti raccontare a un compagno perché la stessa API funziona nel simulatore e sul robot?
