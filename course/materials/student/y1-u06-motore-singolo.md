# 6. Controlla una ruota

## Obiettivo

In questo laboratorio imparerai a comandare separatamente la ruota sinistra.

## Che cosa sai già

Saper chiamare funzioni con argomenti numerici e leggere lo stato di un'uscita.

## Modello mentale

`robot` è il nome della plancia di comando di Romeo. Il punto in `robot.drive(...)` sceglie il comando `drive` di quella plancia. I due numeri indicano nell'ordine ruota sinistra e ruota destra; zero significa ruota ferma. Non occorre ancora studiare le classi.

## Esempio minimo commentato

```python
from romeo import Robot

robot = Robot()          # Prepariamo la plancia di comando.
robot.drive(0.3, 0.0)    # Sinistra attiva, destra ferma.
robot.stop()             # Entrambe ferme alla fine.
```

## Prova guidata

1. Scrivi sopra i due argomenti le etichette «sinistra» e «destra».
2. Prevedi la coppia di valori mostrata dopo `drive(0.3, 0.0)`.
3. Esegui e cerca l'evento con sinistra 0.3 e destra 0.0.
4. Scambia i due valori e osserva quale ruota cambia, poi annulla la modifica.
5. Completa la consegna e controlla l'evento di stop finale.

## Esercizio base

Attiva soltanto la ruota sinistra a 0.35 e poi ferma Romeo.

## Esercizio intermedio

Esegui due prove separate: solo sinistra e solo destra; confronta gli eventi.

## Mini-sfida

Prevedi il verso di rotazione del robot quando soltanto la ruota sinistra avanza.

## Consegna valutata

Con Robot.drive fai girare solo la ruota sinistra, poi ferma Romeo.

## Errori tipici

- Invertire l'ordine sinistra/destra degli argomenti.
- Scrivere `Robot.drive(...)` invece di usare il nome `robot` preparato.
- Dimenticare `robot.stop()` perché l'animazione sembra già terminata.

## Autoverifica

- So indicare quale argomento comanda ciascuna ruota?
- So spiegare il significato di zero?
- So verificare negli eventi che una sola ruota sia stata attivata?

## Accessibilità

Affianca ai valori le parole sinistra/destra e usa lo stato numerico; non richiedere di dedurre la ruota attiva soltanto dall'animazione.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `robot` | il nome scelto per la plancia di comando |
| `drive` | il comando che imposta insieme le due ruote |
| `velocità con segno` | numero positivo per avanti, negativo per indietro |
