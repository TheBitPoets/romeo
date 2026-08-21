# Troubleshooting docente

Diagnostica per livelli: **codice → Activity → runtime → sandbox → hardware**. Evita di saltare direttamente all'hardware quando l'errore è già visibile nel simulatore.

## Il programma non parte

Controlla prima il report Python e lo starter. Se il problema si ripete su più studenti con lo stesso file, verifica l'Activity; se riguarda un solo workspace, confronta il sorgente dello studente.

## `romeo-sim` non disponibile

Esegui il probe amministrativo. Verifica package installato, entry point e ambiente Python effettivamente usato da TheBitLab. Il runtime non deve essere "riparato" chiedendo agli studenti di installare dipendenze nel proprio workspace gestito.

## Il grading runtime fallisce per infrastruttura

Controlla il boundary Docker e la configurazione del digest OCI. Il comportamento corretto è fail-closed; non passare a `plugin.run()` locale per ottenere un voto.

## Simulatore corretto, robot reale sbagliato

Classifica prima il sintomo:

- verso invertito → polarità/configurazione;
- deviazione progressiva → trim, attrito, ruote, batteria;
- scatti/reset → alimentazione/brownout;
- stop tardivo → watchdog/trasporto;
- camera assente → device/Picamera2/cablaggio;
- servo rumoroso → possibile limite meccanico.

In questi casi ferma l'attività fisica e usa il commissioning/preflight, non una modifica casuale del programma studente.

## WebSocket/TCP si disconnette

La priorità è verificare che la disconnessione porti i motori a zero. Solo dopo analizza la causa di rete. Una sessione che perde il controller ma mantiene il movimento è un problema safety, non un semplice problema UX.

## Come raccogliere evidenze

Per un bug riproducibile conserva:

- Activity e unità;
- SHA/versione Romeo;
- report o messaggio preciso;
- backend effettivo;
- se riguarda simulatore o robot;
- passi minimi per riprodurlo;
- cosa ti aspettavi;
- cosa hai osservato.

Apri una issue tecnica separata quando il problema non è specifico della singola lezione.
