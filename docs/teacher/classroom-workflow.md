# Workflow di classe per il docente

## Prima della lezione

Verificare una volta per postazione/nodo di grading:

1. TheBitLab è operativo;
2. il plugin `romeo-sim` è installato e rilevabile;
3. il digest `ROMEO_SANDBOX_IMAGE` è quello approvato dalla release Romeo;
4. Docker è disponibile sul nodo di esecuzione;
5. una Activity Romeo di primo anno produce un report autorevole;
6. una Activity con behavioral test produce anch'essa un report autorevole;
7. il percorso fallisce chiuso se Docker o il digest mancano.

## Durante la lezione

Il ciclo consigliato è:

```text
spiegazione breve
  -> consegna TheBitLab
  -> lavoro nel workspace
  -> simulazione/test
  -> feedback e correzione
  -> nuovo tentativo
  -> scelta del tentativo finale
```

Il docente dovrebbe distinguere sempre:

- **feedback formativo**, utile durante lo sviluppo;
- **grading autorevole**, ottenuto attraverso il runtime sandbox configurato;
- **prova sul robot fisico**, che verifica anche aspetti reali non presenti nel modello simulato.

## Lettura del report

Per una Activity runtime Romeo il report autorevole deve indicare il backend effettivo Docker e metadati coerenti con `authoritative=true`. Se il runtime non è disponibile, la consegna non deve essere degradata silenziosamente a esecuzione process-only.

## Quando usare il robot fisico

Il robot fisico è utile per mostrare la differenza fra modello e realtà: attrito, batteria, differenze tra motori, inerzia, rete, camera e latenza. Va però introdotto dopo che il comportamento logico è già corretto nel simulatore.

Prima dell'uso con la classe seguire [Safety hardware](../hardware/safety.md) e [Checklist di collaudo](../hardware/pre-merge-checklist.md). I risultati del collaudo devono essere registrati, non affidati alla memoria del docente.

## Gestione dei problemi

Se una consegna Romeo non parte:

1. verificare prima il runtime con gli strumenti di inventory/probe di TheBitLab;
2. controllare che il plugin sia installato nello stesso ambiente Python che esegue TheBitLab;
3. verificare il digest OCI configurato;
4. verificare Docker;
5. solo dopo esaminare l'Activity e il codice studente.

Non risolvere un problema infrastrutturale facendo eseguire codice studente non fidato direttamente sul processo host.
