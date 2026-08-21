# Changelog

Le modifiche rilevanti del progetto sono registrate qui.

## Unreleased

### Added

- Licenze esplicite: Apache-2.0 per il software e CC BY-SA 4.0 per Course Bundle
  e immagini originali, con avvisi, inventario asset e validazione del manifest.
- API studente `romeo.easy` e classe `Robot`, con backend mock e adapter CRICKIT.
- Safety backend con limite velocità, watchdog, timeout, controller esclusivo e
  stop fail-safe.
- Simulatore 2D deterministico headless con differential drive, collisioni,
  scenari JSON, traiettoria, event log e grading data-driven.
- Viewer Canvas 2D con protocollo stato WebSocket, telemetria e controlli di
  avvio, stop e reset.
- Protocollo TCP testuale, server con controller esclusivo, client sincrono e
  controllo tastiera W/S/A/D portabile.
- API FastAPI con status/info OpenAPI, telemetria WebSocket e controllo realtime
  browser con heartbeat, ownership esclusiva e stop alla disconnessione.
- `CameraService`, mock CI e adapter Picamera2/libcamera per foto, preview MJPEG e
  pan/tilt tramite il backend Romeo.
- Client gamepad pygame opzionale con mapping analogico, dead-zone, heartbeat e
  STOP garantito alla disconnessione.
- Plugin TheBitLab `romeo-sim` con lifecycle ABI, launch interattivo, worker
  headless deterministico, grading e manifest artifact.
- Course Bundle del primo anno con 20 attività, scenari, starter, hint, soluzioni,
  materiali studente/docente, handout, rubriche e validazione CI.
- Estensione del bundle con 23 unità del secondo anno: socket, protocollo,
  JSON, HTTP/REST, FastAPI, WebSocket, camera, gamepad, telemetria, safety e
  capstone telepresenza.
- Grading runtime dichiarativo dell'output per laboratori di rete deterministici.
- Primitive didattiche LED e ruote indipendenti, con check di grading dedicati.
- Test unitari, simulation/safety/protocol test, lint, typing e CI Python 3.10/3.12.
- Audit iniziale dei repository Romeo, `marwano/robo`, `2cornot2c` e
  `thebitlab-hardware`, con riferimenti riproducibili e rischi aperti.
- Architettura target basata su API studente unica, backend sostituibili,
  simulatore 2D headless e integrazione TheBitLab tramite ABI ufficiale.
- Roadmap M0-M12 con gate di qualità, safety e compatibilità.
- Decision log iniziale per backend, simulazione, mock, safety, networking,
  dipendenze opzionali e provenienza del codice.
