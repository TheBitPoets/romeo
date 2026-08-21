# Preflight prima di una sessione reale

Il preflight risponde a una domanda più piccola del commissioning: **questo Romeo, già collaudato, è pronto adesso per eseguire un programma studente?**

## Caratteristiche desiderate

Il preflight deve essere:

- rapido;
- ripetibile;
- comprensibile allo studente;
- prevalentemente passivo;
- fail-safe;
- capace di produrre anche un risultato machine-readable.

## Check tipici

Dove l'hardware e il software lo permettono, controlla:

- package/versione Romeo;
- backend hardware;
- I2C/CRICKIT;
- configurazione motori;
- calibrazione presente e valida;
- limiti servo;
- camera;
- rete/servizi richiesti;
- watchdog/safety configurati;
- stato noto del commissioning.

## Test attivi

Non è necessario far girare motori e servo a ogni `Run on real Romeo`. I test che muovono l'hardware appartengono al commissioning o a una modalità attiva supervisionata.

## Stato

Il sistema dovrebbe poter distinguere almeno:

- non collaudato;
- commissioning valido;
- preflight pronto;
- preflight fallito.

Un fallimento deve indicare cosa è stato controllato, perché serve e quale verifica semplice può fare lo studente/docente.

## Romeo Doctor

Il coding agent è incaricato di trasformare le parti automatizzabili del collaudo in uno strumento diagnostico riutilizzabile. Quando `romeo-doctor` sarà disponibile e collaudato, questa pagina verrà aggiornata con i comandi e lo schema JSON effettivi. Fino ad allora non assumere che il comando esista nell'installazione.
