# 13. Progetta una sequenza

## Obiettivo

In questo laboratorio imparerai a ordinare azioni e durate per una missione.

## Che cosa sai già

Saper costruire movimenti temporizzati e racchiudere una piccola ricetta in una funzione.

## Modello mentale

Una sequenza è un algoritmo espresso come passi ordinati. Ogni movimento ha tre parti: avvio, durata, cambiamento successivo. Prima di scrivere Python possiamo disegnare frecce e numerare i segmenti; poi traduciamo un segmento alla volta.

## Esempio minimo commentato

```python
from time import sleep
from romeo.easy import forward, left, stop

forward(0.4)  # Segmento 1: avanza.
sleep(1)
left(0.5)     # Segmento 2: cambia orientamento.
sleep(0.5)
stop()
```

## Prova guidata

1. Disegna la missione con tre frecce numerate: avanti, sinistra, avanti.
2. Per ogni freccia scrivi comando e durata previsti.
3. Implementa ed esegui soltanto il primo segmento, terminando temporaneamente con stop.
4. Aggiungi la rotazione e confronta posa prevista e osservata.
5. Aggiungi l'ultimo avanzamento e lascia un solo stop finale.

## Esercizio base

Esegui avanti, rotazione a sinistra, avanti e stop nell'ordine richiesto.

## Esercizio intermedio

Racchiudi il tratto rettilineo in una funzione già nota e usala due volte.

## Mini-sfida

Inverti l'ordine dei primi due segmenti, prevedi la posa diversa e poi verifica.

## Consegna valutata

Avanza, ruota a sinistra, avanza ancora e fermati.

## Errori tipici

- Scrivere tutti i comandi prima di aggiungere le durate.
- Correggere più segmenti insieme e non sapere quale modifica ha funzionato.
- Confondere ordine del disegno e ordine delle righe Python.

## Autoverifica

- So numerare e descrivere i segmenti prima di programmare?
- So collegare ogni `sleep` al comando che resta attivo?
- So testare un segmento alla volta?

## Accessibilità

Offri sia una mappa a frecce sia una lista numerata equivalente; la missione deve essere comprensibile senza interpretare solo il disegno.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `algoritmo` | serie ordinata di passi per ottenere un risultato |
| `segmento` | una parte della missione verificabile da sola |
| `sequenza` | azioni eseguite in un ordine preciso |
