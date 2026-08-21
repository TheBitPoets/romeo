# Guida studente

Questa sezione descrive il flusso normale di lavoro con Romeo dentro TheBitLab. L'obiettivo è concentrarsi sul programma, sugli esperimenti e sul comportamento del robot senza dover conoscere subito tutta l'infrastruttura.

```{toctree}
:maxdepth: 2

setup
first-program
workflow-thebitlab
simulator
report-and-attempts
simulator-to-real
troubleshooting
```

## Il percorso in una frase

**Scrivi → simula → osserva → leggi il report → correggi → riprova → passa al robot soltanto quando il sistema è pronto.**

## Principio fondamentale

**Prima simulatore, poi robot fisico.** Un programma che non ha un comportamento corretto e ripetibile nel simulatore non deve essere usato per comandare l'hardware reale.

## Non devi conoscere tutto subito

Nel primo anno userai soprattutto l'API semplice `romeo.easy`. Nel secondo anno vedrai progressivamente rete, socket, HTTP, REST, WebSocket, camera e controller. Le pagine tecniche e la reference API sono disponibili quando vuoi capire cosa succede sotto il livello didattico.
