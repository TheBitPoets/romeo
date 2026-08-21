# Secondo anno 15. Pan e tilt

## Obiettivo

In questa unità imparerai a orientare la camera attraverso Robot.

## Che cosa sai già

Conosci la API Robot, i numeri decimali e il CameraService.

## Modello mentale

Pan ruota lo sguardo a sinistra/destra; tilt lo inclina su/giù. Gli angoli sono gradi entro limiti sicuri. Robot inoltra la richiesta al backend: il mock registra gli angoli, mentre il backend reale muove i servo.

## Esempio minimo commentato

```python
backend = MockBackend()
robot = Robot(backend)
try:
    robot.look(pan=60, tilt=120)
    print(backend.pan_angle, backend.tilt_angle)
finally:
    robot.close()
```

Lo scaffold mostra gli assi con etichette e fornisce limiti sicuri; non forzare manualmente i servo.

## Prova guidata

1. Indica pan e tilt su un disegno etichettato.
2. Porta prima la camera nella posizione centrale fornita.
3. Cambia un asse alla volta e prevedi il risultato.
4. Verifica i valori registrati dal mock.
5. Prova un valore fuori limite senza collegare hardware reale.

## Esercizio base

Imposta pan 60 e tilt 120 sul backend mock.

## Esercizio intermedio

Scrivi `centra_camera(robot)` usando gli angoli centrali documentati.

## Mini-sfida

Limita in modo esplicito due valori ricevuti prima di passarli a `look` e spiega la scelta.

## Consegna valutata

Porta la camera a pan 60 e tilt 120 con il backend mock.

## Errori tipici

- Scambiare pan e tilt.
- Assumere che qualsiasi angolo sia fisicamente sicuro.
- Dimenticare `close` quando un assert fallisce.

## Autoverifica

- So indicare i due assi?
- Conosco unità e limiti?
- Il test usa il mock prima dell'hardware?

## Accessibilità

Accompagna le frecce con parole sinistra/destra/su/giù e valori numerici; consenti controllo tramite pulsanti grandi oltre agli assi analogici.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `pan` | rotazione orizzontale della camera |
| `tilt` | inclinazione verticale della camera |
| `servo` | motore comandato verso una posizione angolare |
