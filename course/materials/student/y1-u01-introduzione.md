# 1. Conosci Romeo

## Obiettivo

In questo laboratorio imparerai a eseguire il primo programma e fermare il robot.

## Che cosa sai già

Nessuna esperienza di programmazione. È sufficiente saper usare mouse e tastiera.

## Modello mentale

Un programma è una lista di istruzioni che Romeo esegue dall'alto verso il basso. Il pulsante Run avvia la lista; `stop()` lascia le ruote ferme alla fine. Oggi non serve capire ogni simbolo: prima osserviamo che una riga di codice produce un effetto.

## Esempio minimo commentato

```python
# Questa riga rende disponibile il comando stop.
from romeo.easy import stop

# Questa istruzione ferma entrambe le ruote.
stop()
```

Premendo Run, la riga con `stop()` viene eseguita e lo stato finale mostra entrambe le ruote ferme.

## Prova guidata

1. Apri lo starter e individua le righe che iniziano con `from` e quelle che terminano con le parentesi `()`.
2. Indica con il dito la prima istruzione che Romeo eseguirà e poi la seconda.
3. Prima di premere Run, scrivi: «alla fine le ruote saranno ferme».
4. Premi Run e cerca nel feedback lo stato finale dei motori.
5. Aggiungi i comandi richiesti dalla consegna, uno per riga, mantenendo `stop()` come ultima azione.

## Esercizio base

Esegui un programma che accende il LED blu e termina con `stop()`.

## Esercizio intermedio

Inserisci un breve comando `forward(0.2)` prima di `stop()` e prevedi l'ordine degli eventi mostrati dal simulatore.

## Mini-sfida

Scambia due istruzioni, prevedi cosa cambia e poi verifica. Ripristina `stop()` come ultima azione.

## Consegna valutata

Accendi il LED blu, invia un breve comando avanti e termina con stop.

## Errori tipici

- Scrivere `stop` senza parentesi: il comando viene nominato ma non eseguito.
- Scrivere `Stop()` con la maiuscola: Python distingue maiuscole e minuscole.
- Eliminare `stop()` finale: lo stato sicuro non è più espresso chiaramente dal programma.

## Autoverifica

- So indicare l'ordine in cui vengono eseguite tre istruzioni?
- So trovare nel feedback se le ruote sono ferme?
- So spiegare perché `stop()` deve restare alla fine?

## Accessibilità

Leggi ad alta voce l'ordine delle istruzioni e usa anche lo stato testuale dei motori: il colore e il movimento sullo schermo non sono le sole evidenze.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `programma` | una lista ordinata di istruzioni |
| `istruzione` | un'azione scritta su una riga |
| `Run` | il comando che avvia il programma |
