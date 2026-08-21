# Iniziare con Romeo

## Che cosa serve davvero

Per imparare a programmare Romeo non serve avere subito il robot sul banco. La configurazione consigliata è:

1. Python 3.10 o successivo;
2. TheBitLab per consegne, workspace, tentativi e report;
3. il package Romeo installato nell'ambiente gestito dal laboratorio;
4. Docker disponibile sul nodo che esegue il grading autorevole;
5. il robot fisico solo per le prove autorizzate dal docente.

Il codice studente usa una API semplice e non dipende direttamente da CRICKIT:

```python
from time import sleep

from romeo.easy import forward, left, stop

forward()
sleep(1)
left()
sleep(0.5)
stop()
```

Lo stesso modello di programma può essere provato nel simulatore e, quando il docente lo autorizza, sul robot reale. La separazione fra API e backend serve proprio a evitare che ogni esercizio debba essere riscritto per l'hardware.

## Due modalità da non confondere

### Simulatore

È il percorso standard per scrivere, provare, sbagliare e correggere. Le Activity Romeo integrate con TheBitLab possono essere eseguite in una sandbox Docker e finalizzate dal plugin trusted. Il report deve indicare un'esecuzione autorevole e isolamento Docker.

### Robot fisico

È una fase controllata. Prima dell'uso reale devono essere verificati polarità dei motori, stop, watchdog, perdita del controller, servo, camera e alimentazione. La procedura è nella [checklist hardware](hardware/pre-merge-checklist.md).

## Quale guida leggere

- Se sei uno studente: [Guida studente](student/index.md).
- Se sei un docente: [Guida docente](teacher/index.md).
- Se devi installare il runtime: [Installazione e verifica](operations/install-thebitlab-plugin.md).
- Se sviluppi Romeo: [Ambiente di sviluppo](development/environment.md).
