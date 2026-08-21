# Decision log

## ADR-001 — Una API, backend sostituibili

- **Stato:** accettata, 2026-08-21.
- **Problema:** simulatore e hardware non devono dividere il percorso didattico.
- **Decisione:** `romeo.easy` e `Robot` delegano a un backend sostituibile.
- **Motivazione:** conserva lo stesso programma e permette test senza Pi.
- **Alternative:** API separate o rilevamento hardware nel codice studente.
- **Conseguenze:** il contratto backend deve restare piccolo e stabile.

## ADR-002 — Simulazione 2D deterministica e headless

- **Stato:** accettata, 2026-08-21.
- **Problema:** grading ripetibile con un solo robot fisico disponibile.
- **Decisione:** motore Python 2D a passo discreto, indipendente dal viewer.
- **Motivazione:** è semplice da spiegare, veloce in CI e verificabile.
- **Alternative:** 3D/WebGL come motore o simulazione legata al tempo reale.
- **Conseguenze:** il viewer consuma snapshot/eventi e non decide la fisica.

## ADR-003 — Mock e simulatore sono componenti distinti

- **Stato:** accettata, 2026-08-21.
- **Problema:** verificare chiamate hardware e missioni spaziali sono esigenze
  differenti.
- **Decisione:** il mock registra throttle/servo/chiamate; il simulatore calcola
  posa, traiettoria e collisioni.
- **Conseguenze:** test più chiari, a costo di due implementazioni del backend.

## ADR-004 — Integrazione TheBitLab solo tramite ABI ufficiale

- **Stato:** accettata, 2026-08-21.
- **Decisione:** activity extension `extensions.thebitlab.runtime`, entry point
  `thebitlab.runtimes`, id `romeo-sim` e lifecycle
  `describe/probe/launch/run/close`, senza import interni TheBitLab.
- **Alternative:** adapter incorporato nell'app TheBitLab.
- **Conseguenze:** versione del protocollo e conformance test sono obbligatori.

## ADR-005 — Dipendenze hardware e UI opzionali

- **Stato:** accettata, 2026-08-21.
- **Decisione:** core Python puro; CRICKIT/Picamera2, FastAPI e pygame in extra
  dedicati con import differito.
- **Motivazione:** installazione e CI devono funzionare su macchine comuni.
- **Conseguenze:** errori di capability devono essere espliciti e didattici.

## ADR-006 — Safety davanti al backend reale

- **Stato:** accettata, 2026-08-21.
- **Decisione:** limite velocità, command timeout, watchdog, controller singolo e
  stop su errore/disconnessione/shutdown sono invarianti, non opzioni del client.
- **Motivazione:** nessun client deve poter lasciare i motori attivi senza lease.
- **Conseguenze:** timeout e limiti sono configurabili ma con default conservativi;
  i valori finali richiedono prova fisica.

## ADR-007 — Progressione di rete a adapter separati

- **Stato:** accettata, 2026-08-21.
- **Decisione:** TCP testuale, REST e WebSocket sono livelli didattici distinti che
  comandano lo stesso controller.
- **Alternative:** un solo protocollo universale.
- **Conseguenze:** più adapter, ma concetti introdotti uno alla volta e protocollo
  separato dal dominio.

## ADR-008 — Provenienza e licenze

- **Stato:** accettata, 2026-08-21.
- **Decisione:** materiali del corso originali; adattamenti sostanziali dal
  repository MIT `marwano/robo` conservano attribuzione e licenza; dipendenze e
  asset hanno inventario prima della distribuzione.
- **Conseguenze:** non si copia testo Manning e la provenienza è verificabile.

## Decisioni ancora da prendere

Nessuna blocca M0-M3. Una decisione di prodotto sarà richiesta solo se una futura
necessità impone di cambiare significativamente l'API studente, abbandonare la
roadmap 2D o modificare hardware/licenza/distribuzione.
