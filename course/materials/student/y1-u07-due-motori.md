# 7. Coordina due ruote

## Obiettivo

In questo laboratorio imparerai a confrontare velocità delle due ruote.

## Che cosa sai già

Saper leggere i due argomenti di `robot.drive(sinistra, destra)`.

## Modello mentale

Romeo usa una guida differenziale: decide il movimento confrontando le due ruote. Due valori positivi uguali lo fanno avanzare diritto; un valore zero fa perno su una ruota; valori diversi producono una curva.

## Esempio minimo commentato

```python
from romeo import Robot

robot = Robot()
robot.drive(0.3, 0.3)  # Stessa velocità: direzione diritta.
robot.stop()
```

## Prova guidata

1. Disegna due ruote e scrivi 0.3 accanto a entrambe.
2. Prevedi se il robot va diritto o gira.
3. Esegui l'esempio e controlla che lo stesso evento contenga entrambi i valori 0.3.
4. Prova temporaneamente `drive(0.2, 0.4)` e descrivi la curva senza misurarla.
5. Ripristina due valori 0.3 e termina con lo stop richiesto.

## Esercizio base

Imposta entrambe le ruote a 0.3 e termina in sicurezza.

## Esercizio intermedio

Compila una tabella di previsione per `(0.3, 0.3)`, `(0.0, 0.3)` e `(0.2, 0.4)`.

## Mini-sfida

Trova due coppie diverse che facciano curvare Romeo in direzioni opposte.

## Consegna valutata

Imposta entrambe le ruote a 0.3 e termina in sicurezza.

## Errori tipici

- Credere che due numeri uguali facciano girare il robot.
- Confondere la coppia di velocità con due comandi eseguiti in tempi diversi.
- Controllare soltanto una ruota nel feedback.

## Autoverifica

- So prevedere l'effetto di due valori uguali?
- So distinguere una curva da un movimento diritto usando i numeri?
- So verificare che entrambe le ruote siano state comandate nello stesso evento?

## Accessibilità

Rappresenta ogni coppia sia con frecce sia con una tabella testuale sinistra/destra; le frecce da sole non sono necessarie per capire.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `guida differenziale` | movimento ottenuto confrontando le velocità delle due ruote |
| `coppia` | i due valori sinistra e destra considerati insieme |
| `curva` | movimento con velocità delle ruote diverse |
