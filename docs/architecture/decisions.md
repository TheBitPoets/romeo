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

## ADR-009 — Un bundle progressivo e generabile

- **Stato:** accettata, 2026-08-21.
- **Problema:** attività, materiali e indici devono restare coerenti mentre il
  corso cresce da primo a secondo anno.
- **Decisione:** un solo Course Bundle TheBitLab contiene entrambe le annualità;
  script deterministici generano i file ripetitivi e un validatore offline
  controlla manifest, Activity, runtime, asset, scenari e indice.
- **Motivazione:** evita due cataloghi divergenti e rende le modifiche ripetibili.
- **Alternative:** bundle separati per anno o file mantenuti soltanto a mano.
- **Conseguenze:** i generatori sono sorgenti autoritative e ogni soluzione
  docente viene eseguita nel simulatore in CI.

## ADR-010 — Grading di rete per comportamento osservabile

- **Stato:** accettata, 2026-08-21.
- **Problema:** un check spaziale non dimostra che un programma abbia compreso
  socket, JSON o status HTTP.
- **Decisione:** la configurazione runtime può aggiungere `stdout_checks`
  pesati; le soluzioni stampano i marker soltanto dopo assert sul comportamento.
- **Motivazione:** mantiene il protocollo runtime ufficiale e rende i lab
  trasparenti e deterministici senza introdurre un secondo runner.
- **Alternative:** grading geometrico fittizio o un runtime distinto per rete.
- **Conseguenze:** i marker offrono solo feedback formativo. Verifiche ad alto
  impatto restano bloccate finché il runtime non entra nel boundary ufficiale
  TheBitLab con grader fidato separato.

## ADR-011 — M12 resta opzionale e non altera il percorso 2D

- **Stato:** accettata, 2026-08-21.
- **Decisione:** non introdurre ora 3D, WebRTC, computer vision, nuovi sensori o
  Webots. Il protocollo stato/eventi consente renderer futuri senza cambiare API.
- **Motivazione:** il criterio di successo è già soddisfatto dal simulatore 2D
  deterministico; le alternative aumentano hardware, privacy e dipendenze.
- **Conseguenze:** ogni estensione M12 richiederà un caso didattico verificato e,
  se cambia hardware/licenza/distribuzione, una decisione di prodotto esplicita.

## ADR-012 — Licenze separate e immagini in quarantena

- **Stato:** accettata, 2026-08-21.
- **Problema:** codice, materiali didattici e fotografie richiedono permessi e
  obblighi adatti alla loro natura; il repository iniziale non li dichiarava.
- **Decisione:** software Apache-2.0 e Course Bundle CC BY-SA 4.0. Le 53 immagini
  sono escluse dalla distribuzione finché l'autore non registra provenienza e
  licenza nel repository; nomi e loghi restano fuori dalle concessioni.
- **Motivazione:** Apache-2.0 mantiene il runtime permissivo con una concessione
  esplicita sui brevetti; CC BY-SA consente riuso e adattamento del corso facendo
  restare condivisibili gli adattamenti.
- **Alternative:** MIT con CC BY (massima permissività, senza reciprocità sui
  materiali) e corso proprietario (maggiore controllo, minore collaborazione).
- **Conseguenze:** issue #1 resta aperta; manifest, avvisi e inventario devono
  impedire che assenza di evidenza venga scambiata per originalità.

## ADR-013 — Broker sandbox TheBitLab e grading trusted separato

- **Stato:** accettata dal product owner, 2026-08-21.
- **Problema:** subprocess, `python -I` e timeout non confinano codice studente
  non affidabile e il worker locale condivide interprete con simulatore/grader.
- **Decisione:** estendere l'ABI v1 con `prepare_sandbox()` e
  `finalize_sandbox()`. TheBitLab esegue il piano nel proprio profilo Docker;
  il container riceve solo gli artifact dichiarati e produce una command trace
  non fidata. Scenario, replay, grading e artifact finali restano sull'host.
- **Motivazione:** riusa un unico boundary ufficiale e una trace falsificata può
  al massimo esprimere comandi che lo studente avrebbe potuto impartire.
- **Alternative:** sandbox autonoma per plugin; runtime solo formativo locale.
- **Conseguenze:** immagini OCI solo per digest; `run()` resta fallback
  formativo non autorevole; senza Docker o digest configurato si fallisce chiuso.

## ADR-014 — Contratti funzionali nominati per il secondo anno

- **Stato:** accettata dal product owner, 2026-08-21.
- **Problema:** codice top-level e marker stdout non offrono un punto osservabile
  per testare socket, HTTP, WebSocket, camera, controller e safety.
- **Decisione:** ogni unità Y2 espone una piccola funzione nominata, importabile
  senza side effect. Starter, soluzione, consegna e behavioural test condividono
  la stessa firma; rete, camera e controller sono iniettati quando possibile.
- **Motivazione:** mantiene il codice leggibile e permette test di valori,
  ordine, cleanup ed errori senza affidarsi a stringhe stampate.
- **Alternative:** harness black-box di processi/porte; sola rubrica docente.
- **Conseguenze:** i marker restano feedback; il voto deriva dai behavioural
  test eseguiti nel sandbox e validati dal finalize trusted.
