# Romeo — Course Delivery Dashboard

Questo indice collega il Course Bundle Romeo ai manuali Sphinx, alle slide docente e al passaggio controllato simulatore → robot reale. Non duplica le 43 unità: `course/curriculum.json`, le Activity e le pagine generate restano la fonte didattica puntuale.

## Stato e fonti autorevoli

- Curriculum: [`course/curriculum.json`](../curriculum.json) — 20 unità del primo anno + 23 del secondo.
- Activity: [`course/activities/`](../activities/).
- Catalogo pubblico: generato dal Course Bundle nel portale Sphinx.
- Manuale studente: [`docs/student/index.md`](../../docs/student/index.md).
- Manuale docente: [`docs/teacher/index.md`](../../docs/teacher/index.md).
- Operations: [`docs/operations/`](../../docs/operations/).
- Hardware safety: [`docs/hardware/safety.md`](../../docs/hardware/safety.md).
- Commissioning fisico: [`docs/hardware/commissioning.md`](../../docs/hardware/commissioning.md).
- Preflight studente: [`docs/hardware/preflight.md`](../../docs/hardware/preflight.md).
- Slide: [`slides/romeo/README.md`](../../slides/romeo/README.md).
- Revisioni in-year: [`course/delivery/DELIVERY_CHANGELOG.md`](DELIVERY_CHANGELOG.md).

## Mappa del corso

Prima di entrare nei due anni usa [00 — Architettura didattica e workflow](../../slides/romeo/modules/00_COURSE_MAP.md) per presentare il modello backend-sostituibile, il flusso TheBitLab/simulatore e il ruolo distinto del robot reale.

## Regola fondamentale: stesso programma, backend diverso

Il flusso didattico normale è:

```text
scrivi codice
→ esegui con mock/simulatore
→ osserva traiettoria/event log/report
→ correggi
→ supera i gate dell'Activity
→ preflight del robot già commissionato
→ stessa missione sul robot reale, se autorizzata
```

Il robot fisico **non è il debugger primario**. Il simulatore è il luogo normale in cui gli studenti provano, sbagliano, ripetono e raccolgono evidenze.

## Primo anno — Python e robotica 2D

| Blocco | Unità | Focus | Slide docente | Manuali/lab |
|---|---|---|---|---|
| Y1-A | 1–5 | primo programma, componenti, REPL, chiamate, LED | [01 — Fondamenti](../../slides/romeo/modules/01_Y1_FONDAMENTI.md) | [first program](../../docs/student/first-program.md), Activity del bundle |
| Y1-B | 6–11 | ruote, movimento, curve, stop/safety, velocità | [02 — Movimento e safety](../../slides/romeo/modules/02_Y1_MOVIMENTO_SAFETY.md) | simulatore + event log |
| Y1-C | 12–16 | funzioni, sequenze, if, for, while | [03 — Astrazione e controllo](../../slides/romeo/modules/03_Y1_CONTROL_FLOW.md) | Activity del bundle |
| Y1-D | 17–20 | simulazione, coordinate, missioni, capstone | [04 — Simulatore e missioni](../../slides/romeo/modules/04_Y1_SIMULATORE_MISSIONI.md) | [simulator](../../docs/student/simulator.md), report/attempts |

## Secondo anno — rete, servizi e telepresenza

| Blocco | Unità | Focus | Slide docente | Manuali/lab |
|---|---|---|---|---|
| Y2-A | 1–7 | rete, IP, porte, client/server, TCP, Romeo/1, JSON | [05 — Networking e protocolli](../../slides/romeo/modules/05_Y2_NETWORK_PROTOCOLS.md) | TCP lab + Activity del bundle |
| Y2-B | 8–13 | HTTP, REST, FastAPI, WebSocket, controller web/tastiera | [06 — Web e realtime](../../slides/romeo/modules/06_Y2_WEB_REALTIME.md) | web simulator + Activity del bundle |
| Y2-C | 14–20 | camera, pan/tilt, foto/video, eventi, gamepad, telemetria | [07 — Telepresenza e telemetria](../../slides/romeo/modules/07_Y2_TELEPRESENCE.md) | camera mock/reale sostituibile |
| Y2-D | 21–23 | safety di rete, integrazione, capstone telepresenza | [08 — Safety e capstone](../../slides/romeo/modules/08_Y2_SAFETY_CAPSTONE.md) | grading comportamentale + report |

## Passaggio simulatore → robot reale

La transizione fisica ha un deck operativo separato: [09 — Dal simulatore al robot reale](../../slides/romeo/modules/09_SIM_TO_REAL.md).

Distinguere sempre:

- **commissioning**: collaudo completo del singolo esemplare, supervisionato, con movimenti attivi e misure;
- **preflight**: controllo rapido prima di una sessione studente su un robot già commissionato, prevalentemente passivo;
- **`romeo-doctor`**: capability diagnostica opzionale la cui disponibilità dipende dallo **SHA/versione realmente installato**. Se il comando è presente e validato in quella versione, può automatizzare i check passivi previsti dal preflight; se non è presente, le checklist hardware restano il fallback autorevole.

Il doctor non sostituisce il commissioning: verso meccanico delle ruote, movimento reale, calibrazione fisica e altre osservazioni che richiedono feedback umano restano supervisionate e documentate.

## Conduzione di una lezione

Sequenza consigliata:

```text
richiamo
→ obiettivo osservabile
→ modello mentale
→ demo minima
→ checkpoint
→ Activity/simulatore
→ report/evidenza
→ eventuale estensione
```

Per le lezioni con robot fisico aggiungere prima il gate di preflight e mantenere una procedura di STOP/alimentazione immediatamente disponibile.

## Modifiche durante l'anno

Correzioni a slide, spiegazioni, setup, troubleshooting o equivalenti lab-fix possono evolvere senza riscrivere il Course Bundle, purché preservino il contratto didattico. Registrarle nel Delivery Change Log.

Una modifica a unità, obiettivi, grading contract o hardware behavior non è una semplice patch di delivery e richiede review specifica.