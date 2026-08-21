# Roadmap

Ogni milestone termina con test automatici e documentazione aggiornati. Le prove
hardware non bloccano lo sviluppo delle parti verificabili in CI.

| Milestone | Risultato verificabile |
| --- | --- |
| M0 — Baseline | Audit, package, test baseline, CI, architettura e decision log. |
| M1 — Romeo API | `romeo.easy`, `Robot`, contratto backend, mock e CRICKIT isolato. |
| M2 — Safety | Stop, limiti, timeout, watchdog e shutdown fail-safe con test. |
| M3 — Simulator core | Differential drive 2D, mondo, collisioni, scenari, clock e grading deterministici. |
| M4 — Simulator web | Viewer 2D, protocollo stato/eventi, start/reset e traiettoria. |
| M5 — TCP | Protocollo testuale, server/client e tastiera leggibile. |
| M6 — HTTP/REST/WebSocket | FastAPI, status, controllo e telemetria real-time. |
| M7 — Camera | CameraService, Picamera2, foto, pan/tilt e MJPEG. |
| M8 — Gamepad | Client pygame, mapping configurabile e stop su disconnessione. |
| M9 — Runtime TheBitLab | Plugin `romeo-sim`, lifecycle ABI, run headless, grading e artefatti. |
| M10 — Bundle primo anno | Attività Python/robotica, materiali studente/docente e capstone. |
| M11 — Bundle secondo anno | Socket, REST, WebSocket, camera, gamepad e telepresenza. |
| M12 — Evoluzione opzionale | Solo dopo validazione: 3D, sensori, visione e navigazione. |

## Gate trasversali

- Una submission produce lo stesso comportamento osservabile con backend reale e
  simulato, entro le differenze fisiche documentate.
- Tutti i test CI girano senza Raspberry Pi.
- Ogni trasporto di rete applica ownership del controller e stop alla perdita di
  connessione.
- Ogni attività usa il formato Course Bundle e il runtime ABI esistenti.
- M12 non inizia finché il percorso 2D e il grading non sono stabili.
