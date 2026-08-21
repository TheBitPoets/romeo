# Usare il simulatore

Il simulatore è il posto normale in cui scrivere, provare e correggere un programma Romeo.

Non è soltanto un'animazione: applica un modello deterministico del robot e produce stato, traiettoria ed eventi che il grader può verificare.

## Il ciclo di lavoro

1. Apri la consegna in TheBitLab.
2. Apri il workspace.
3. Modifica `main.py`.
4. Salva.
5. Esegui la prova.
6. Guarda il movimento simulato e il report.
7. Correggi una cosa alla volta.
8. Ripeti finché il comportamento è quello richiesto.

## Che cosa osservare

Durante una prova non guardare solo se Romeo "arriva". Controlla anche:

- posizione iniziale e finale;
- orientamento;
- percorso seguito;
- collisioni;
- checkpoint;
- tempo simulato;
- presenza di uno `stop()` finale quando richiesto.

## Simulatore e robot reale

Il simulatore rappresenta un modello ideale. Il robot fisico aggiunge attrito, batteria, tolleranze dei motori, superficie e inerzia. Per questo il simulatore serve a verificare soprattutto **logica e sequenza dei comandi**; il passaggio al robot serve poi a osservare e calibrare il mondo reale.

```text
main.py
  -> Romeo API
  -> romeo-sim
  -> simulation engine
  -> trajectory/events
  -> grader
  -> report
```

## Reset e ripetibilità

Quando ripeti la stessa Activity con lo stesso programma e lo stesso scenario, il grading deve essere riproducibile. Se cambi una sola riga puoi quindi confrontare l'effetto della modifica senza confonderlo con variazioni casuali del mondo fisico.

## Prima del robot reale

Passa al robot solo quando:

- il programma è sintatticamente corretto;
- la missione simulata è coerente;
- hai letto il report;
- gli eventuali test richiesti passano;
- il docente ha autorizzato la prova fisica;
- il preflight hardware è valido.
