# 20. Capstone: consegna robotica

## Obiettivo

In questo laboratorio imparerai a progettare, testare e spiegare una missione completa.

## Che cosa sai già

Aver completato U01–U19 e saper usare funzioni, condizioni, cicli, coordinate, grading e stop sicuro.

## Modello mentale

Il capstone è un piccolo progetto, non un unico tentativo. Prima definiamo criteri di successo, poi dividiamo la missione in funzioni, proviamo segmenti, leggiamo le evidenze e documentiamo una correzione. Il grader misura il comportamento; la spiegazione mostra il metodo.

## Esempio minimo commentato

```python
from romeo.easy import stop

def parcheggia():
    # Aggiungi qui soltanto i passi del parcheggio finale.
    stop()

# Le altre funzioni della missione verranno chiamate prima.
parcheggia()
```

L'esempio mostra la struttura, non rivela il percorso o i valori della soluzione.

## Prova guidata

1. Trascrivi i criteri: checkpoint, collisioni, parcheggio, orientamento, tempo e stop presenti nello scenario.
2. Disegna il percorso e assegna un nome a ogni segmento o fase.
3. Implementa funzioni piccole e verifica ciascuna fase con una posa attesa.
4. Usa una condizione o un ciclo soltanto dove rende il piano più chiaro, poi prova entrambi i casi necessari.
5. Esegui il grader completo e correggi un check alla volta.
6. Consegna codice, previsione, una correzione documentata e una breve spiegazione della safety.

## Esercizio base

Completa la missione con funzioni nominate e stop finale, superando tutti i check comportamentali.

## Esercizio intermedio

Riduci una ripetizione con un ciclo già conosciuto e dimostra che la traiettoria resta corretta.

## Mini-sfida

Trova una seconda strategia valida e confrontala con la prima per chiarezza, tempo simulato e margine dagli ostacoli.

## Consegna valutata

Raggiungi i checkpoint, evita collisioni, fermati nel parcheggio e consegna una breve spiegazione.

## Errori tipici

- Scrivere l'intera missione come una lunga sequenza prima di provare i segmenti.
- Aggiungere funzioni o cicli decorativi che non rendono il piano più chiaro.
- Considerare sufficiente il punteggio automatico senza consegnare spiegazione ed evidenze di debug.

## Autoverifica

- Ogni funzione ha un nome che descrive una fase della missione?
- Posso mostrare un'evidenza per ogni criterio della rubrica?
- Romeo resta fermo anche alla conclusione dell'ultima fase?

## Accessibilità

La consegna e la rubrica devono essere disponibili come checklist testuale; coordinate, eventi e risultati accompagnano sempre la mappa visiva.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `capstone` | progetto finale che combina le competenze del corso |
| `rubrica` | criteri trasparenti usati per valutare il lavoro |
| `evidenza` | dato, evento o spiegazione che dimostra un risultato |
