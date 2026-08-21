# 5. Comunica con il LED

## Obiettivo

In questo laboratorio imparerai a usare un output immediato per mostrare lo stato.

## Che cosa sai già

Saper chiamare una funzione con un argomento e distinguere numero e testo.

## Modello mentale

Il LED è un'uscita immediata: `led(...)` cambia il suo stato ma non muove le ruote. Il nome del colore è testo, quindi va scritto tra virgolette. Il pannello di stato riporta anche il nome o i valori del colore per non dipendere soltanto dalla vista.

## Esempio minimo commentato

```python
from romeo.easy import led

# Le virgolette indicano che blue è testo.
led("blue")
```

## Prova guidata

1. Individua le due virgolette che racchiudono `blue`.
2. Prevedi il nome del colore che apparirà nello stato.
3. Esegui una volta con `red` e leggi il feedback testuale.
4. Modifica soltanto la stringa in `blue` per la consegna.
5. Controlla che nessun evento motore sia necessario per cambiare il LED.

## Esercizio base

Imposta il LED blu e verifica il valore testuale o RGB finale.

## Esercizio intermedio

Mostra in ordine `red`, `green`, `blue`; annota quale colore resta alla fine.

## Mini-sfida

Prevedi e verifica che cosa accade con `led("off")` dopo un colore acceso.

## Consegna valutata

Imposta il LED su blu; il grader controllerà il colore finale.

## Errori tipici

- Scrivere `led(blue)` senza virgolette e ricevere `NameError`.
- Usare un nome non previsto, per esempio `azzurro`, invece dei valori documentati.
- Pensare che il primo colore resti quello finale dopo una seconda chiamata.

## Autoverifica

- So spiegare perché il colore è tra virgolette?
- So trovare lo stato del LED anche senza distinguere il colore nell'immagine?
- So prevedere quale di più chiamate determina il colore finale?

## Accessibilità

Nomina sempre il colore nel testo e leggi i valori di stato; non usare rosso/verde come unico modo per comunicare errore o successo.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `stringa` | testo racchiuso tra virgolette |
| `RGB` | tre quantità che descrivono rosso, verde e blu |
| `stato finale` | il valore rimasto dopo l'ultima istruzione |
