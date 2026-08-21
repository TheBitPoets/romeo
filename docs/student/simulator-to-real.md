# Dal simulatore al robot reale

Il robot fisico è una fase successiva del laboratorio, non il primo posto in cui provare codice incompleto.

## Gate prima della prova fisica

Il passaggio consigliato è:

```text
scrivi main.py
   -> simulatore
   -> test/grading
   -> correggi
   -> programma pronto
   -> preflight hardware
   -> autorizzazione docente
   -> robot reale
```

Il preflight hardware potrà essere eseguito tramite lo strumento diagnostico Romeo quando disponibile nell'installazione; finché il commissioning automatico non è stato validato, il docente usa la checklist hardware autorevole.

## Lo stesso programma

L'obiettivo architetturale di Romeo è mantenere invariato il codice didattico. Un programma basato sull'API pubblica, per esempio:

```python
from romeo.easy import forward, stop

forward(0.3)
stop()
```

non dovrebbe essere riscritto per "diventare hardware". È il backend, configurato dall'ambiente, a cambiare target.

## Cosa può cambiare nel mondo reale

Una traiettoria perfetta nel simulatore può diventare leggermente curva sul pavimento. Non significa automaticamente che il programma sia sbagliato. Le cause fisiche possono includere:

- ruote con attrito diverso;
- motori non perfettamente identici;
- livello della batteria;
- superficie;
- distribuzione del peso;
- inerzia;
- calibrazione del singolo esemplare.

## Durante la prova

Usa velocità conservative e tieni libera l'area. Se il comportamento non è quello atteso, ferma Romeo e confronta la **sequenza di comandi** con quella osservata nel simulatore prima di cambiare il codice.

## Dopo la prova

Distingui sempre due domande:

1. il programma esprime correttamente la strategia?
2. il robot fisico necessita di calibrazione?

Questa distinzione è una delle idee più importanti del corso: un modello software e un sistema fisico non sono la stessa cosa, ma possono condividere la stessa interfaccia e la stessa logica.
