# Changelog

Le modifiche rilevanti del progetto sono registrate qui.

## Unreleased

### Added

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
- Test unitari, simulation/safety/protocol test, lint, typing e CI Python 3.10/3.12.
- Audit iniziale dei repository Romeo, `marwano/robo`, `2cornot2c` e
  `thebitlab-hardware`, con riferimenti riproducibili e rischi aperti.
- Architettura target basata su API studente unica, backend sostituibili,
  simulatore 2D headless e integrazione TheBitLab tramite ABI ufficiale.
- Roadmap M0-M12 con gate di qualità, safety e compatibilità.
- Decision log iniziale per backend, simulazione, mock, safety, networking,
  dipendenze opzionali e provenienza del codice.
