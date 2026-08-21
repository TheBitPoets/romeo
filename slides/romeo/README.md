# Slide docente — Romeo Python & Robotics

Deck Markdown/Marp per la conduzione del corso. Le 43 unità canoniche restano in `course/curriculum.json` e nelle Activity; queste slide raggruppano le unità in **macro-blocchi narrativi** per evitare duplicazione.

| Deck | Copertura | Focus |
|---:|---|---|
| 00 | corso completo | [Architettura didattica e workflow](modules/00_COURSE_MAP.md) |
| 01 | Y1 unità 1–5 | [Fondamenti: primo programma, API, REPL, LED](modules/01_Y1_FONDAMENTI.md) |
| 02 | Y1 unità 6–11 | [Movimento, ruote, stop e safety](modules/02_Y1_MOVIMENTO_SAFETY.md) |
| 03 | Y1 unità 12–16 | [Funzioni, sequenze e controllo del flusso](modules/03_Y1_CONTROL_FLOW.md) |
| 04 | Y1 unità 17–20 | [Simulatore, coordinate, missioni e capstone](modules/04_Y1_SIMULATORE_MISSIONI.md) |
| 05 | Y2 unità 1–7 | [Networking, TCP, protocollo Romeo/1 e JSON](modules/05_Y2_NETWORK_PROTOCOLS.md) |
| 06 | Y2 unità 8–13 | [HTTP, REST, FastAPI, WebSocket e controller](modules/06_Y2_WEB_REALTIME.md) |
| 07 | Y2 unità 14–20 | [Camera, eventi, gamepad e telemetria](modules/07_Y2_TELEPRESENCE.md) |
| 08 | Y2 unità 21–23 | [Safety di rete, integrazione e capstone](modules/08_Y2_SAFETY_CAPSTONE.md) |
| 09 | trasversale | [Dal simulatore al robot reale](modules/09_SIM_TO_REAL.md) |

## Contratto del deck

Ogni macro-deck usa, quando applicabile:

`richiamo → obiettivi → modello mentale → demo → errore tipico → checkpoint → Activity/simulatore → evidenza → prossimo passo`.

Il deck 09 è operativo: distingue esplicitamente commissioning, preflight e il futuro `romeo-doctor` senza dichiarare disponibile un comando non ancora implementato.