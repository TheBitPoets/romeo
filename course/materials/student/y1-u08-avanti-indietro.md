# 8. Avanti e indietro

## Obiettivo

In questo laboratorio imparerai a comporre due movimenti opposti nel tempo.

## Che cosa sai già

Saper prevedere il movimento da una coppia di velocità.

## Modello mentale

Un comando motore resta attivo finché un altro comando lo cambia. `sleep(1)` non ferma Romeo: lascia trascorrere un secondo con il comando corrente. `backward` imposta entrambe le ruote all'indietro; `stop` le porta infine a zero.

## Esempio minimo commentato

```python
from time import sleep
from romeo.easy import forward, stop

forward(0.2)  # Inizia il movimento.
sleep(1)      # Continua per un secondo.
stop()        # Termina il movimento.
```

## Prova guidata

1. Segna sulla carta tre istanti: inizio, dopo un secondo, fine.
2. Scrivi lo stato delle ruote in ciascun istante dell'esempio.
3. Esegui e osserva come cambia il tempo simulato durante `sleep`.
4. Aggiungi dopo il primo secondo `backward(0.4)` e un secondo `sleep(1)`.
5. Termina con `stop()` e confronta posizione iniziale e finale.

## Esercizio base

Avanza per un secondo, torna indietro per un secondo e fermati.

## Esercizio intermedio

Usa la stessa velocità nei due versi e spiega perché Romeo dovrebbe tornare vicino alla partenza.

## Mini-sfida

Cambia soltanto la durata del ritorno; prevedi da quale lato della partenza finirà.

## Consegna valutata

Avanza per un secondo, torna indietro per un secondo e fermati.

## Errori tipici

- Pensare che `sleep` significhi stop: i motori mantengono l'ultimo comando.
- Usare durate diverse senza aggiornare la previsione della posa finale.
- Mettere `stop()` tra il comando e il relativo `sleep`, annullando il movimento.

## Autoverifica

- So dire quale comando resta attivo durante ogni `sleep`?
- So prevedere il verso del movimento?
- So confrontare posa iniziale e finale usando numeri, non solo l'animazione?

## Accessibilità

Usa una linea del tempo testuale con stato e durata; l'animazione può essere rallentata o sostituita dalla lettura della traiettoria numerica.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `sleep` | attesa durante la quale resta attivo il comando corrente |
| `durata` | tempo per cui continua un movimento |
| `backward` | comando che muove entrambe le ruote all'indietro |
