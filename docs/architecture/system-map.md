# Mappa del sistema Romeo

Questa pagina collega i nomi che compaiono nelle guide senza richiedere subito di conoscere l'implementazione.

## Vista studente

```text
main.py
  -> Romeo API
  -> simulatore
  -> risultato/report
```

Quando il docente autorizza una prova fisica, lo stesso programma usa il target reale invece del modello simulato.

## Vista docente

```text
Course Bundle / Activity
       -> workspace studente
       -> romeo-sim
       -> scenario + grading
       -> report / tentativi
       -> eventuale coda robot reale
```

Il robot fisico non è necessario perché tutti lavorino contemporaneamente.

## Vista amministratore

```text
TheBitLab process
  -> Python entry point: romeo-sim
  -> trusted Romeo plugin
  -> sandbox plan
  -> Docker broker
  -> pinned Romeo OCI worker
  -> sandbox result (untrusted)
  -> trusted finalize
  -> authoritative report
```

Package Python e immagine OCI sono artefatti distinti. Il processo deve conoscere il digest immutabile approvato.

## Vista sviluppatore

```text
romeo.easy / Robot
        |
      safety
        |
   backend interface
     /       \
 mock/sim   CRICKIT
    |          |
simulation   hardware
    |
TheBitLab runtime integration
```

## Trusted e untrusted

Nel grading sandbox il codice studente e il payload del worker sono non trusted. Lo scenario/rubrica/decisione finale restano dove possibile nel lato trusted e la finalizzazione valida il risultato tecnico prima di produrre il report autorevole.

## Una sola API didattica

La separazione dei backend serve a mantenere stabile il modello mentale dello studente. Non dovrebbe essere necessario imparare un set di comandi per il simulatore e un altro per il robot fisico.
