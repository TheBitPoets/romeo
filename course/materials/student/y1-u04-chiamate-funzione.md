# 4. Chiama una funzione

## Obiettivo

In questo laboratorio imparerai a riconoscere nome, parentesi e argomento.

## Che cosa sai già

Saper provare una riga nel REPL e riconoscere un `NameError`.

## Modello mentale

Una funzione è un comando con un nome. Le parentesi chiedono a Python di eseguirlo; il valore dentro le parentesi è un argomento che precisa come eseguirlo. `forward(0.3)` significa quindi: esegui `forward` usando velocità 0.3.

## Esempio minimo commentato

```python
from romeo.easy import forward, stop

# Nome: forward; parentesi: esegui; argomento: 0.3.
forward(0.3)
stop()
```

## Prova guidata

1. Sottolinea il nome `forward` nell'esempio.
2. Cerchia le parentesi e racchiudi in un quadrato l'argomento `0.3`.
3. Prevedi quale evento motore apparirà per primo.
4. Esegui il programma e confronta il valore mostrato con `0.3`.
5. Cambia soltanto l'argomento in `0.2`, ripeti e poi ripristina la consegna.

## Esercizio base

Scrivi la chiamata richiesta `forward(0.3)` e termina con `stop()`.

## Esercizio intermedio

Confronta gli eventi prodotti da `forward()` e `forward(0.3)` senza cambiare altre righe.

## Mini-sfida

Trova e correggi tre chiamate errate: `Forward(0.3)`, `forward 0.3`, `forward("0.3")`.

## Consegna valutata

Chiama forward con velocità 0.3, quindi stop.

## Errori tipici

- Omettere le parentesi e quindi non eseguire la funzione.
- Usare la virgola al posto del punto in `0.3`.
- Mettere il numero tra virgolette e trasformarlo in testo.

## Autoverifica

- So indicare nome, parentesi e argomento in una chiamata?
- So spiegare che cosa cambia modificando soltanto l'argomento?
- So riconoscere un numero e una stringa?

## Accessibilità

Usa marcatori diversi anche nel testo — «nome», «parentesi», «argomento» — senza affidare le tre parti soltanto a colori.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `funzione` | un comando Python che può essere eseguito |
| `chiamata` | il nome della funzione seguito dalle parentesi |
| `argomento` | un valore fornito alla funzione |
