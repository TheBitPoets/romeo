# 9. Curve e rotazioni

## Obiettivo

In questo laboratorio imparerai a distinguere curva e rotazione sul posto.

## Che cosa sai già

Saper usare una durata e conoscere l'effetto di velocità uguali o diverse.

## Modello mentale

In una curva il centro di Romeo cambia posizione; in una rotazione sul posto le ruote vanno in versi opposti e il centro resta quasi fermo. L'angolo ottenuto dipende da velocità, durata e distanza tra le ruote: perciò si calibra una durata con prove piccole.

## Esempio minimo commentato

```python
from time import sleep
from romeo.easy import left, stop

left(0.5)       # Le ruote girano in versi opposti.
sleep(0.5)      # Una prima prova breve, non ancora "90 gradi".
stop()
```

## Prova guidata

1. Disegna la posa iniziale con una freccia orientata verso destra.
2. Esegui una prova breve di 0.5 s e leggi l'orientamento finale.
3. Confronta l'angolo osservato con 90 gradi e calcola soltanto se serve più o meno tempo.
4. Modifica la durata di un piccolo passo e ripeti, senza cambiare anche la velocità.
5. Quando sei nella tolleranza, termina con `stop()` e annota la durata calibrata.

## Esercizio base

Ruota a sinistra fino a circa 90 gradi e fermati.

## Esercizio intermedio

Confronta una curva ottenuta con ruote diverse e una rotazione sul posto, descrivendo posizione e orientamento.

## Mini-sfida

Trova una durata per circa 45 gradi mantenendo la stessa velocità e spiega la tua previsione.

## Consegna valutata

Ruota Romeo di circa 90 gradi a sinistra e fermalo.

## Errori tipici

- Copiare una durata precisa senza verificarla nel proprio scenario.
- Cambiare velocità e durata insieme, rendendo difficile capire quale modifica ha avuto effetto.
- Confondere coordinate finali e orientamento finale.

## Autoverifica

- So distinguere curva e rotazione usando il movimento del centro?
- So leggere l'errore di orientamento in gradi?
- So descrivere una calibrazione cambiando una variabile alla volta?

## Accessibilità

Fornisci orientamento iniziale/finale e errore in gradi come testo; non richiedere di stimare l'angolo soltanto dalla figura.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `orientamento` | direzione verso cui punta Romeo |
| `grado` | unità usata per misurare un angolo |
| `calibrazione` | serie di piccole prove per trovare un valore adatto |
