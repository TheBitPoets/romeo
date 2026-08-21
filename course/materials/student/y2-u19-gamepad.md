# Secondo anno 19. Controller analogico

## Obiettivo

In questa unità imparerai a convertire assi in velocità ruote.

## Che cosa sai già

Conosci eventi, velocità delle due ruote, funzioni e numeri fra -1 e 1.

## Modello mentale

Lo stick produce due assi. Prima applichiamo una dead-zone per ignorare piccoli tremolii, poi mescoliamo avanti e sterzo nelle velocità sinistra/destra e infine limitiamo il risultato. pygame e il dispositivo sono nello scaffold: la funzione matematica resta testabile con numeri simulati.

## Esempio minimo commentato

```python
mapping = GamepadMapping(max_speed=0.6)
sinistra, destra = wheel_speeds(0.0, -1.0, mapping)
print(sinistra, destra)  # 0.6 0.6: stick avanti
```

Molti controller riportano avanti come Y negativo; il mapping isola questa convenzione.

## Prova guidata

1. Segna centro e direzioni sugli assi etichettati.
2. Prevedi le ruote per centro, avanti e destra.
3. Verifica le previsioni con input simulati.
4. Prova valori dentro e fuori la dead-zone.
5. Collega infine la funzione agli eventi pygame forniti.

## Esercizio base

Calcola le ruote per centro e avanti rispettando velocità massima.

## Esercizio intermedio

Verifica una curva a destra e una a sinistra con proprietà simmetriche.

## Mini-sfida

Crea una configurazione con dead-zone e max speed diverse senza modificare la funzione di mapping.

## Consegna valutata

Calcola le ruote per stick avanti e verifica direzione e limite.

## Errori tipici

- Dimenticare che l'asse Y può essere invertito.
- Inviare il rumore vicino allo zero ai motori.
- Mescolare lettura pygame e matematica rendendo impossibili i test senza gamepad.

## Autoverifica

- So spiegare la dead-zone?
- Le velocità rispettano sempre i limiti?
- Posso testare tutto senza controller fisico?

## Accessibilità

Offri tastiera e pulsanti come input equivalenti; mostra numericamente assi e ruote e consenti rimappatura.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `asse` | valore continuo prodotto dallo stick |
| `dead-zone` | zona vicino allo zero trattata come ferma |
| `differential drive` | movimento ottenuto combinando due velocità ruota |
