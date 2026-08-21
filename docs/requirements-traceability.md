# Tracciabilità dei requisiti

Matrice aggiornata il 21 agosto 2026. I path indicano l'evidenza autoritativa;
`docs/release/readiness.md` separa i gate automatici dalle verifiche fisiche.

| Requisito | Implementazione | Verifica |
| --- | --- | --- |
| Audit dei quattro repository | `docs/audit.md` con commit fissati e standard riusati | audit read-only e 32 test ABI upstream |
| API studente unica | `romeo.easy`, `Robot`, backend protocol | `test_easy.py`, `test_robot.py`, test runtime con entrambe le API |
| Mock distinto dal simulatore | `MockBackend` registra comandi; `SimulationEngine` calcola fisica | `test_robot.py`, `test_simulation_engine.py` |
| CRICKIT isolato | `CrickitBackend`, wiring motor 2/1 e servo 1/4, import differito | `test_crickit_backend.py`; hardware fisico da collaudare |
| STOP e safety | `SafetyBackend`: limite, watchdog, timeout, lease, disconnect e shutdown | `test_safety.py`, test TCP/WebSocket/gamepad |
| Simulatore 2D headless | posa, ruote, differential drive, clock, collisioni, limiti e camera | `test_simulation_engine.py`, `test_scenario.py` |
| Scenari data-driven | schema `romeo.scenario.v1`, ostacoli e check dichiarativi | parser/validation test e 43 scenari del corso |
| Grading deterministico | posizione, zona, orientamento, collisioni, tempo, checkpoint, eventi/LED | `test_grading.py` e 43 soluzioni docente |
| Viewer separato | protocollo `romeo.simulation.state.v1`, Canvas 2D e WebSocket stato | `test_web_app.py`, asset test e `node --check` |
| TCP didattico | protocollo Romeo/1, whitelist, server/client e ownership | test protocollo, client e server |
| HTTP/REST | FastAPI status, info, state, controllo simulazione e fotografia | OpenAPI automatico e `test_web_app.py` |
| WebSocket realtime | `/ws/control`, `/ws/state`, ack/errori, heartbeat e stop disconnect | test WebSocket e lab secondo anno |
| Camera moderna | `CameraService`, mock, Picamera2/libcamera, foto e MJPEG | `test_camera.py`; una prova Picamera2 marcata hardware |
| Tastiera | mapping W/S/A/D/SPACE portabile e client TCP | `test_text_protocol.py`, `test_tcp_client.py`, unità Y2-13 |
| Gamepad | pygame opzionale, dead-zone e differential mapping | `test_gamepad.py`, unità Y2-19 |
| Plugin TheBitLab | entry point `thebitlab.runtimes`, lifecycle completo, quattro capability | discovery test locale e suite `2cornot2c` upstream |
| Headless Run/artefatti | subprocess, tempo simulato, grading, manifest, trajectory/event/state | `test_thebitlab_runtime.py` |
| Course Bundle | manifest 1.0.0, curriculum, indice e layout standard | validator locale e validator upstream |
| Primo anno | 20 unità Python/robotica con attività, starter, hint, soluzione e materiali | `test_course_bundle.py`, piano `course/docs/first-year-plan.md` |
| Secondo anno | 23 unità rete/telepresenza e check sul comportamento osservabile | plugin completo per ogni soluzione, piano secondo anno |
| Qualità e CI | packaging Hatchling, Ruff, mypy strict, pytest su 3.10/3.12 | `.github/workflows/quality.yml`, wheel build |
| Git e decision log | branch dedicato e commit incrementali; ADR-001–ADR-011 | `git log main..feat/platform-foundation` |
| Evoluzione M12 | confini compatibili con renderer/backend futuri; feature complesse differite | ADR-011, nessuna dipendenza 3D/WebRTC introdotta |

## Limiti dichiarati

- Nessun test automatico sostituisce il collaudo fisico della checklist safety.
- Il browser integrato non era disponibile nell'ambiente di audit; viewer, asset,
  JavaScript, REST e WebSocket sono verificati automaticamente, non tramite una
  sessione visuale manuale.
- Licenza del progetto e provenienza delle immagini iniziali restano la sola
  decisione necessaria prima di push/release, tracciata nell'issue GitHub #1.
