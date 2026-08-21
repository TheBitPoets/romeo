# Struttura del progetto e invarianti

Romeo separa API didattica, dominio robot, backend, simulazione, rete, web e integrazione TheBitLab. Prima di modificare un modulo, identifica il livello a cui appartiene la responsabilità.

## Mappa

```text
src/romeo/
├── easy.py                 API a funzioni per i primi passi
├── robot.py                API a oggetti e semantica del robot
├── safety.py               limiti, watchdog e stop
├── backends/               adattatori real/mock/sim
├── simulation/             modello 2D, scenario, grading
├── network/                TCP, protocollo e tastiera
├── web/                    REST, WebSocket e viewer
├── camera/                 camera service e adapter
└── integrations/thebitlab/ runtime plugin e sandbox contract
```

## Invariante 1 — il codice studente non conosce il backend

Il programma didattico deve restare centrato su `romeo.easy` o `Robot`. Non introdurre import CRICKIT, Docker o simulation engine negli esercizi introduttivi per risolvere un problema interno.

## Invariante 2 — stesso comportamento pubblico, target diversi

Quando aggiungi una funzione pubblica valuta almeno:

- backend simulato;
- backend reale;
- fake/mock per test;
- safety;
- documentazione;
- eventuale supporto runtime TheBitLab.

Una feature che esiste soltanto sul robot reale senza una semantica simulabile deve essere dichiarata esplicitamente, non nascosta dietro un comportamento incompatibile.

## Invariante 3 — safety sopra l'attuatore

STOP, limiti di velocità e watchdog non devono dipendere dalla buona volontà del programma studente. Mantieni il confine safety in un livello condiviso e testabile.

## Invariante 4 — grading autorevole fuori dal processo studente

Il worker sandbox produce dati tecnici non trusted. Il voto/test finale viene ricostruito dal plugin trusted. Non trasformare un payload prodotto dalla submission in una decisione autorevole senza validazione/finalizzazione.

## Invariante 5 — il corso è un consumer dell'API

Le 43 Activity devono usare l'API pubblica come farebbe uno studente. Se una lezione richiede accesso a un interno solo per essere possibile, chiediti prima se l'API pubblica è incompleta o se l'obiettivo didattico appartiene a un livello avanzato.
