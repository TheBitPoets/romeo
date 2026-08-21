# 16. Controlla un ciclo while

## Obiettivo

In questo laboratorio imparerai a usare una condizione e assicurare la terminazione.

## Che cosa sai già

Saper leggere `if`, un confronto semplice e un blocco ripetuto con `for`.

## Modello mentale

`while` ripete il corpo finché la sua domanda resta vera. Servono un contatore iniziale, un limite e un aggiornamento: senza aggiornamento la domanda non cambia e il ciclo può non finire. Prima del run simuliamo ogni giro in una tabella.

## Esempio minimo commentato

```python
contatore = 0
while contatore < 3:
    # Il contatore deve cambiare a ogni giro.
    contatore = contatore + 1
```

La tabella dei valori è 0 → 1 → 2 → 3; quando vale 3, `3 < 3` è falso e il ciclo termina.

## Prova guidata

1. Crea una tabella con colonne `contatore` e `contatore < 3`.
2. Compila a mano le righe per 0, 1, 2 e 3.
3. Individua nel codice l'istruzione che avvicina il ciclo alla fine.
4. Aggiungi `forward(0.2)` nel corpo e prevedi tre eventi motore.
5. Esegui nel simulatore, verifica tre eventi e lascia `stop()` fuori dal ciclo.

## Esercizio base

Usa `while` e un contatore per inviare tre comandi, poi fermati.

## Esercizio intermedio

Modifica il limite a 2 e poi a 4, compilando prima la tabella di previsione.

## Mini-sfida

Trova il difetto in una copia senza incremento, senza eseguirla; spiega come interrompere una prova che non termina.

## Consegna valutata

Invia tre comandi con while e termina con stop.

## Errori tipici

- Dimenticare l'incremento e creare un ciclo che non termina.
- Rientrare `stop()` nel corpo quando deve essere eseguito una volta sola.
- Confondere `< 3` con `<= 3` e ottenere un giro in più.

## Autoverifica

- So elencare i valori del contatore a ogni giro?
- So indicare perché la condizione diventa falsa?
- So riconoscere un ciclo potenzialmente infinito prima di eseguirlo?

## Accessibilità

La tabella testuale rende espliciti i cambiamenti del contatore; fornisci una procedura scritta e raggiungibile da tastiera per interrompere l'esecuzione.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `while` | ciclo che continua mentre una condizione è vera |
| `contatore` | numero aggiornato a ogni iterazione |
| `terminazione` | momento in cui la condizione diventa falsa e il ciclo finisce |
