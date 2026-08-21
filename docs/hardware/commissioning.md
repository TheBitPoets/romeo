# Commissioning del robot fisico

Il commissioning è la procedura completa con cui un docente/tecnico stabilisce che un esemplare Romeo è sicuro e calibrato. Non va confuso con il preflight quotidiano dello studente.

## Prima di iniziare

Leggi [Safety hardware](safety.md) e la [checklist di collaudo](pre-merge-checklist.md). Prepara area libera, possibilità di togliere alimentazione e una posizione in cui le ruote possano essere testate senza spostare il robot.

## Ordine consigliato

1. inventario hardware e alimentazione;
2. Raspberry Pi / I2C / CRICKIT;
3. motore sinistro a velocità minima;
4. motore destro;
5. verifica polarità con conferma umana;
6. STOP;
7. watchdog e perdita controller;
8. forward/backward/turn a terra in area libera;
9. servo pan/tilt con limiti conservativi;
10. Picamera2 e streaming;
11. prova combinata sotto carico e controllo brownout;
12. calibrazione sinistra/destra;
13. stessa missione simulatore → robot.

## Feedback fisico

Se l'esemplare non possiede encoder/IMU sufficienti, il software non può sapere autonomamente se una ruota comandata con throttle positivo gira nel verso meccanico corretto. Il commissioning deve quindi chiedere conferma all'operatore invece di inventare una misura.

## Misure da conservare

Registra valori osservati, non solo checkbox:

- watchdog configurato e latenza misurata;
- limiti pan/tilt sicuri;
- eventuale inversione motori;
- trim sinistra/destra;
- speed limit;
- problemi di alimentazione;
- camera/FPS o limitazioni rilevanti.

## Commissioning vs preflight

Il commissioning può includere movimenti attivi e deve essere supervisionato. Il preflight quotidiano deve invece essere rapido e prevalentemente passivo, verificando configurazione/device/stato prima di autorizzare una sessione reale.

Il progetto prevede uno strumento diagnostico riutilizzabile (`romeo-doctor`) come evoluzione del collaudo. Finché tale comando non è presente e validato nello SHA installato, questa procedura e la checklist restano l'autorità operativa.

## Evidenza

Il collaudo reale deve produrre un documento `physical-validation-YYYY-MM-DD.md` con hardware, versioni, misure, test eseguiti e problemi rimasti aperti. Non inserire credenziali o dati sensibili.
