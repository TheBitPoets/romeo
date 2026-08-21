# 14. Decidi con if

## Obiettivo

In questo laboratorio imparerai a scegliere un comportamento in base a un dato.

## Che cosa sai già

Saper chiamare una funzione e comprendere un nome che riceve un valore, come un parametro.

## Modello mentale

Una condizione è una domanda con risposta `True` o `False`. `if` esegue il blocco rientrato soltanto quando la risposta è `True`; `else` descrive l'altra strada. Seguiamo una strada per volta con il dito prima di eseguire.

## Esempio minimo commentato

```python
from romeo.easy import forward

modalita_sicura = True
if modalita_sicura:
    forward(0.3)  # Eseguita perché la condizione è True.
```

## Prova guidata

1. Leggi la condizione come domanda: «modalità sicura è attiva?».
2. Segna quale riga rientrata verrà eseguita con `True`.
3. Esegui e controlla la velocità 0.3 nell'evento motore.
4. Aggiungi un ramo `else` con velocità 0.5 e ripeti temporaneamente con `False`.
5. Ripristina `True`, usa la durata adatta al target e termina con stop fuori dai due rami.

## Esercizio base

Con `modalita_sicura = True`, scegli velocità 0.3 e fermati sul target.

## Esercizio intermedio

Completa anche `else` e verifica separatamente sia `True` sia `False`.

## Mini-sfida

Scrivi una funzione `scegli_velocita(modalita_sicura)` che esegua una delle due velocità e provala con entrambi i valori.

## Consegna valutata

Se modalita_sicura è True usa velocità 0.3; raggiungi il target e fermati.

## Errori tipici

- Dimenticare i due punti dopo `if` o `else`.
- Allineare il corpo con `if` invece di rientrarlo.
- Provare soltanto il caso `True` e credere che anche l'altra strada funzioni.

## Autoverifica

- So dire quale blocco viene eseguito con `True` e con `False`?
- So spiegare perché lo stop comune può stare dopo i due rami?
- Ho verificato entrambe le strade cambiando un solo valore?

## Accessibilità

Rappresenta i due rami con le etichette testuali VERO/FALSO oltre alle frecce; leggi l'indentazione come «dentro if» o «dentro else».

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `booleano` | valore che può essere soltanto `True` o `False` |
| `if` | esegue un blocco quando la condizione è vera |
| `else` | esegue il blocco alternativo quando la condizione è falsa |
