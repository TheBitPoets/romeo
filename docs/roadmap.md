# Roadmap

Ogni milestone termina con test automatici e documentazione aggiornati. Le prove
hardware non bloccano lo sviluppo delle parti verificabili in CI.

| Milestone | Stato | Risultato verificabile |
| --- | --- | --- |
| M0 — Baseline | Completata | Audit, package, test baseline, CI, architettura e decision log. |
| M1 — Romeo API | Completata | `romeo.easy`, `Robot`, contratto backend, mock e CRICKIT isolato. |
| M2 — Safety | Completata | Stop, limiti, timeout, watchdog e shutdown fail-safe con test. |
| M3 — Simulator core | Completata | Differential drive 2D, mondo, collisioni, scenari, clock e grading deterministici. |
| M4 — Simulator web | Completata | Viewer 2D, protocollo stato/eventi, start/reset e traiettoria. |
| M5 — TCP | Completata | Protocollo testuale, server/client e tastiera leggibile. |
| M6 — HTTP/REST/WebSocket | Completata | FastAPI, status, controllo e telemetria real-time. |
| M7 — Camera | Completata | CameraService, Picamera2, foto, pan/tilt e MJPEG. |
| M8 — Gamepad | Completata | Client pygame, mapping configurabile e stop su disconnessione. |
| M9 — Runtime TheBitLab | Completata | Plugin `romeo-sim`, lifecycle ABI, run headless, grading e artefatti. |
| M10 — Bundle primo anno | Completata | 20 attività Python/robotica, materiali studente/docente, handout e capstone verificati. |
| M11 — Bundle secondo anno | Pianificata | Socket, REST, WebSocket, camera, gamepad e telepresenza. |
| M12 — Evoluzione opzionale | Pianificata | Solo dopo validazione: 3D, sensori, visione e navigazione. |

## Gate trasversali

- Una submission produce lo stesso comportamento osservabile con backend reale e
  simulato, entro le differenze fisiche documentate.
- Tutti i test CI girano senza Raspberry Pi.
- Ogni trasporto di rete applica ownership del controller e stop alla perdita di
  connessione.
- Ogni attività usa il formato Course Bundle e il runtime ABI esistenti.
- M12 non inizia finché il percorso 2D e il grading non sono stabili.
