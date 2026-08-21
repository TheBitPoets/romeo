# 15. Ripeti con for

## Obiettivo

In questo laboratorio imparerai a ripetere un numero noto di azioni.

## Che cosa sai già

Saper riconoscere un blocco rientrato e chiamare più volte la stessa funzione.

## Modello mentale

Un ciclo `for` ripete un blocco un numero già noto di volte. `range(4)` fornisce quattro giri; a ogni giro il nome `passo` riceve il numero corrente. Le righe fuori dal rientro, come lo stop finale, vengono eseguite una sola volta.

## Esempio minimo commentato

```python
from romeo.easy import forward, stop

for passo in range(4):
    forward(0.2)  # Questa riga viene chiamata quattro volte.

stop()            # Questa riga viene chiamata una volta.
```

## Prova guidata

1. Scrivi su carta i quattro valori prodotti da `range(4)`: 0, 1, 2, 3.
2. Evidenzia la sola riga che appartiene al corpo del ciclo.
3. Prevedi il numero di eventi motore prima del run.
4. Esegui e conta gli eventi, non la distanza percorsa: senza `sleep` i comandi sono immediati.
5. Cambia temporaneamente `range(2)`, verifica due eventi e ripristina quattro.

## Esercizio base

Usa `for` e `range(4)` per inviare quattro comandi, poi fermati.

## Esercizio intermedio

Aggiungi una breve durata nel corpo per rendere osservabile ogni ripetizione e prevedi il tempo totale.

## Mini-sfida

Definisci una funzione con parametro `ripetizioni` e usa `range(ripetizioni)`; provala con 2 e 4.

## Consegna valutata

Usa un ciclo for per inviare quattro comandi di movimento, poi stop.

## Errori tipici

- Credere che `range(4)` produca cinque valori da 0 a 4.
- Non rientrare il comando da ripetere.
- Rientrare anche `stop()` e fermare Romeo a ogni giro senza averlo previsto.

## Autoverifica

- So prevedere quanti giri produce `range(4)`?
- So indicare quali righe sono dentro e fuori dal ciclo?
- So verificare il numero di ripetizioni negli eventi?

## Accessibilità

Accompagna il blocco rientrato con una lista dei quattro giri; usa il nome esplicito `passo` invece di simboli convenzionali non spiegati.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `for` | ciclo che visita una sequenza di valori |
| `range` | funzione che produce un numero stabilito di valori interi |
| `iterazione` | un singolo giro del ciclo |
