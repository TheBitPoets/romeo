# Scrivere e provare il codice in TheBitLab

Questa è la sequenza operativa consigliata per una Activity Romeo.

## 1. Apri la consegna

Dalla TUI o dall'interfaccia TheBitLab scegli l'Activity assegnata dal docente. Controlla consegna, scadenza, stato del workspace e criteri visibili di valutazione.

Nella TUI attuale sono disponibili, tra gli altri, i comandi per:

- aprire il workspace;
- aprire l'editor;
- aprire un terminale;
- eseguire i test;
- vedere lo storico dei tentativi;
- selezionare il tentativo finale;
- chiedere aiuto secondo la policy della consegna.

## 2. Modifica solo gli artifact della submission

Per le prime Activity Romeo il file principale è normalmente `main.py`. Parti dallo starter fornito e lavora nel workspace della consegna. Non modificare scenario, configurazioni di grading o file docente.

Esempio:

```python
from time import sleep

from romeo.easy import forward, right, stop

forward(0.5)
sleep(1)
right(0.4)
sleep(0.5)
stop()
```

## 3. Esegui i test nel simulatore

Usa **Esegui test**. Per un runtime Romeo configurato correttamente, TheBitLab riconosce `romeo-sim` e usa automaticamente il percorso sandbox autorevole. Lo studente non deve scegliere manualmente l'immagine Docker.

Il flusso è:

```text
workspace studente
  -> TheBitLab
  -> plugin Romeo trusted
  -> worker Docker senza rete
  -> risultato tecnico
  -> finalizzazione trusted
  -> report studente
```

## 4. Leggi il report, non limitarti a "verde/rosso"

Controlla:

- quanti test sono passati;
- quale comportamento non corrisponde alla consegna;
- eventuali messaggi pubblici;
- traiettoria/stato finale quando mostrati;
- errori di sintassi o runtime.

I dettagli riservati dei test non devono essere esposti allo studente.

## 5. Correggi e ripeti

Modifica il programma, riesegui il test e confronta i risultati. Ogni esecuzione può diventare un tentativo distinto: lo storico serve a vedere il percorso, non solo l'ultimo risultato.

## 6. Seleziona il tentativo finale

Quando sei soddisfatto, seleziona il tentativo che vuoi consegnare come definitivo secondo il flusso previsto dalla classe. Non dare per scontato che "ultimo" significhi automaticamente "finale".

## 7. Passaggio al robot fisico

Il passaggio dal simulatore al robot non è automatico. Avviene solo quando il docente lo autorizza e il robot è stato collaudato. Prima della prova reale:

- area libera;
- velocità iniziale conservativa;
- stop raggiungibile immediatamente;
- nessuna persona o oggetto nella traiettoria;
- docente presente per le prime prove.

Il programma deve essere già stato verificato nel simulatore.
