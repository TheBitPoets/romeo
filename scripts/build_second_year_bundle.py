"""Generate the networking-focused second-year extension of the Romeo bundle."""

# ruff: noqa: E501 -- executable lesson programs are intentionally complete strings.

from __future__ import annotations

import json
from dataclasses import dataclass
from textwrap import dedent

from build_first_year_bundle import COURSE, UNITS, dump, write
from build_first_year_bundle import build as build_first_year


@dataclass(frozen=True)
class NetworkUnit:
    slug: str
    title: str
    objective: str
    concepts: str
    task: str
    solution: str
    markers: tuple[str, ...]
    minutes: int = 60
    difficulty: str = "B"


def code(value: str) -> str:
    return dedent(value).lstrip()


UNITS_Y2 = (
    NetworkUnit(
        "rete",
        "Una rete di nodi",
        "distinguere host, rete e servizio",
        "host, loopback, indirizzo",
        "Valida l'indirizzo di loopback e stampa il marker solo dopo l'assert.",
        code("""
        from ipaddress import ip_address

        loopback = ip_address("127.0.0.1")
        assert loopback.is_loopback
        print("RETE OK")
    """),
        ("RETE OK",),
    ),
    NetworkUnit(
        "indirizzi-ip",
        "Indirizzi IP",
        "risolvere un nome e riconoscere IPv4",
        "DNS, localhost, IPv4",
        "Risolvi localhost, valida l'indirizzo e stampa IP OK.",
        code("""
        import socket
        from ipaddress import ip_address

        address = socket.gethostbyname("localhost")
        assert ip_address(address).version == 4
        print("IP OK", address)
    """),
        ("IP OK",),
    ),
    NetworkUnit(
        "porte",
        "Porte e servizi",
        "associare una porta libera a un socket",
        "porta, bind, endpoint",
        "Chiedi al sistema una porta effimera e verifica che sia positiva.",
        code("""
        import socket

        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            assert 0 < port < 65536
        print("PORTA OK")
    """),
        ("PORTA OK",),
    ),
    NetworkUnit(
        "client-server",
        "Client e server",
        "scambiare byte tra due endpoint",
        "client, server, send, recv",
        "Invia PING su una coppia di socket e rispondi PONG.",
        code("""
        import socket

        client, server = socket.socketpair()
        with client, server:
            client.sendall(b"PING\\n")
            assert server.recv(16) == b"PING\\n"
            server.sendall(b"PONG\\n")
            assert client.recv(16) == b"PONG\\n"
        print("CLIENT SERVER OK")
    """),
        ("CLIENT SERVER OK",),
    ),
    NetworkUnit(
        "socket",
        "Un vero socket TCP",
        "aprire server e client sul loopback",
        "listen, accept, connect",
        "Avvia un piccolo server in thread, collega il client e verifica la risposta.",
        code("""
        import socket
        import threading

        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]

        def serve():
            connection, _ = listener.accept()
            with connection:
                assert connection.recv(16) == b"HELLO\\n"
                connection.sendall(b"WELCOME\\n")

        thread = threading.Thread(target=serve)
        thread.start()
        with socket.create_connection(("127.0.0.1", port)) as client:
            client.sendall(b"HELLO\\n")
            assert client.recv(16) == b"WELCOME\\n"
        thread.join()
        listener.close()
        print("SOCKET OK")
    """),
        ("SOCKET OK",),
        70,
    ),
    NetworkUnit(
        "protocollo-testuale",
        "Il protocollo Romeo/1",
        "analizzare comandi testuali con una whitelist",
        "riga, comando, validazione",
        "Analizza FORWARD e STOP e controlla nome e argomenti.",
        code("""
        from romeo.network.protocol import parse_command

        forward = parse_command("FORWARD 0.4")
        stop = parse_command("STOP")
        assert forward.name == "FORWARD" and forward.arguments == (0.4,)
        assert stop.name == "STOP"
        print("PROTOCOLLO OK")
    """),
        ("PROTOCOLLO OK",),
    ),
    NetworkUnit(
        "json",
        "Dati JSON",
        "serializzare e validare un messaggio",
        "oggetto, array, serializzazione",
        "Codifica uno stato Romeo, decodificalo e verifica i tipi.",
        code("""
        import json

        message = {"type": "state", "motors": [0.3, 0.3], "moving": True}
        wire = json.dumps(message)
        decoded = json.loads(wire)
        assert decoded["type"] == "state" and decoded["moving"] is True
        print("JSON OK")
    """),
        ("JSON OK",),
    ),
    NetworkUnit(
        "http",
        "Una richiesta HTTP",
        "riconoscere metodo, status e body",
        "GET, status code, header",
        "Servi JSON su loopback, esegui GET e verifica status 200.",
        code("""
        import json
        import threading
        import urllib.request
        from http.server import BaseHTTPRequestHandler, HTTPServer

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                body = json.dumps({"status": "ok"}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.handle_request)
        thread.start()
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/status") as response:
            assert response.status == 200
            assert json.load(response)["status"] == "ok"
        thread.join()
        server.server_close()
        print("HTTP 200 OK")
    """),
        ("HTTP 200 OK",),
        75,
    ),
    NetworkUnit(
        "rest",
        "REST: leggere lo stato",
        "consumare una risorsa JSON",
        "risorsa, endpoint, response",
        "Interroga /api/status con TestClient e verifica il contratto.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.web import create_app

        with TestClient(create_app()) as client:
            response = client.get("/api/status")
            data = response.json()
            assert response.status_code == 200 and data["status"] == "ok"
        print("REST STATUS OK")
    """),
        ("REST STATUS OK",),
    ),
    NetworkUnit(
        "fastapi",
        "Costruisci una API FastAPI",
        "definire un endpoint tipizzato",
        "decorator, route, OpenAPI",
        "Crea /status, chiamalo senza rete esterna e verifica il JSON.",
        code("""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        app = FastAPI()

        @app.get("/status")
        def status():
            return {"robot": "romeo", "ready": True}

        response = TestClient(app).get("/status")
        assert response.status_code == 200 and response.json()["ready"] is True
        print("FASTAPI OK")
    """),
        ("FASTAPI OK",),
        75,
    ),
    NetworkUnit(
        "websocket",
        "WebSocket bidirezionale",
        "mantenere una connessione per comandi realtime",
        "upgrade, frame, ack",
        "Collegati a /ws/control, invia STOP e verifica l'ack.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.web import create_app

        with TestClient(create_app()) as client:
            with client.websocket_connect("/ws/control") as websocket:
                ready = websocket.receive_json()
                websocket.send_json({"command": "STOP"})
                ack = websocket.receive_json()
                assert ready["type"] == "ready" and ack["type"] == "ack"
        print("WEBSOCKET ACK OK")
    """),
        ("WEBSOCKET ACK OK",),
        75,
    ),
    NetworkUnit(
        "web-controller",
        "Controller web",
        "tradurre input UI in messaggi validi",
        "evento, payload, feedback",
        "Invia FORWARD via WebSocket, controlla ack, quindi STOP.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.web import create_app

        with TestClient(create_app()) as client:
            with client.websocket_connect("/ws/control") as websocket:
                websocket.receive_json()
                websocket.send_json({"command": "FORWARD", "speed": 0.25})
                assert websocket.receive_json()["command"] == "forward"
                websocket.send_json({"command": "STOP"})
                assert websocket.receive_json()["command"] == "stop"
        print("WEB CONTROL OK")
    """),
        ("WEB CONTROL OK",),
        80,
    ),
    NetworkUnit(
        "tastiera-remota",
        "Tastiera remota sicura",
        "separare la mappa dei tasti dal trasporto e garantire lo stop finale",
        "WASD, client, timeout, stop",
        "Trasforma W e spazio nei comandi remoti FORWARD e STOP.",
        code("""
        from romeo.network.keyboard import command_for_key

        sequence = [command_for_key(key) for key in ("w", " ")]
        assert [command.name for command in sequence] == ["FORWARD", "STOP"]
        print("CONTROLLO REMOTO OK")
    """),
        ("CONTROLLO REMOTO OK",),
    ),
    NetworkUnit(
        "camera",
        "Camera come servizio",
        "usare una camera sostituibile",
        "CameraService, mock, isolamento",
        "Acquisisci una foto dal mock senza importare Picamera2.",
        code("""
        from romeo.camera.mock import MINIMAL_JPEG, MockCameraService

        camera = MockCameraService()
        assert camera.available and camera.capture_photo() == MINIMAL_JPEG
        camera.close()
        print("CAMERA SERVICE OK")
    """),
        ("CAMERA SERVICE OK",),
    ),
    NetworkUnit(
        "pan-tilt",
        "Pan e tilt",
        "orientare la camera attraverso Robot",
        "servo, angolo, limite",
        "Porta la camera a pan 60 e tilt 120 con il backend mock.",
        code("""
        from romeo import Robot
        from romeo.backends.mock import MockBackend

        backend = MockBackend()
        robot = Robot(backend)
        robot.look(60, 120)
        assert (backend.pan_angle, backend.tilt_angle) == (60.0, 120.0)
        robot.close()
        print("PAN TILT OK")
    """),
        ("PAN TILT OK",),
    ),
    NetworkUnit(
        "fotografia",
        "Fotografia REST",
        "ricevere JPEG con media type corretto",
        "JPEG, Content-Type, endpoint",
        "Inietta MockCameraService e verifica /api/camera/photo.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.camera.mock import MINIMAL_JPEG, MockCameraService
        from romeo.web import create_app

        with TestClient(create_app(camera=MockCameraService())) as client:
            response = client.get("/api/camera/photo")
            assert response.status_code == 200
            assert response.headers["content-type"] == "image/jpeg"
            assert response.content == MINIMAL_JPEG
        print("FOTO JPEG OK")
    """),
        ("FOTO JPEG OK",),
        70,
    ),
    NetworkUnit(
        "video",
        "Stream MJPEG",
        "riconoscere frame e boundary",
        "frame, multipart, MJPEG",
        "Leggi il primo frame del mock e verifica i marker JPEG.",
        code("""
        from romeo.camera.mock import MockCameraService

        camera = MockCameraService()
        frame = next(camera.frames(frames_per_second=10))
        camera.close()
        assert frame.startswith(b"\\xff\\xd8") and frame.endswith(b"\\xff\\xd9")
        print("MJPEG FRAME OK")
    """),
        ("MJPEG FRAME OK",),
        70,
    ),
    NetworkUnit(
        "eventi",
        "Programmazione a eventi",
        "reagire a eventi senza polling fragile",
        "queue, evento, handler",
        "Inserisci due eventi in una coda e gestiscili nell'ordine.",
        code("""
        from collections import deque

        events = deque([{"type": "key", "value": "w"}, {"type": "key", "value": "space"}])
        handled = []
        while events:
            handled.append(events.popleft()["value"])
        assert handled == ["w", "space"]
        print("EVENTI OK")
    """),
        ("EVENTI OK",),
    ),
    NetworkUnit(
        "gamepad",
        "Controller analogico",
        "convertire assi in velocità ruote",
        "asse, dead-zone, differential drive",
        "Calcola le ruote per stick avanti e verifica direzione e limite.",
        code("""
        from romeo.gamepad import GamepadMapping, wheel_speeds

        left, right = wheel_speeds(0.0, -1.0, GamepadMapping(max_speed=0.6))
        assert left == 0.6 and right == 0.6
        assert wheel_speeds(0.02, 0.02) == (0.0, 0.0)
        print("GAMEPAD OK")
    """),
        ("GAMEPAD OK",),
    ),
    NetworkUnit(
        "telemetria",
        "Telemetria versionata",
        "leggere stato senza dipendere dal renderer",
        "schema, pose, motors, clock",
        "Genera uno snapshot simulato e verifica schema e campi.",
        code("""
        from romeo.simulation import Scenario, SimulationEngine

        scenario = Scenario.from_mapping({"schema_version": "romeo.scenario.v1", "id": "telemetry"})
        state = SimulationEngine(scenario).state()
        assert state["schema_version"] == "romeo.simulation.state.v1"
        assert {"pose", "motors", "camera", "time"} <= state.keys()
        print("TELEMETRIA OK")
    """),
        ("TELEMETRIA OK",),
    ),
    NetworkUnit(
        "safety",
        "Safety di rete",
        "applicare ownership, timeout e stop",
        "lease, watchdog, disconnect",
        "Prendi il controllo, muovi, rilascia e verifica motori a zero.",
        code("""
        from romeo.backends.mock import MockBackend
        from romeo.safety import SafetyBackend

        backend = MockBackend()
        safety = SafetyBackend(backend, background_watchdog=False)
        safety.claim_controller("student-client")
        safety.set_motor_speeds_for("student-client", 0.4, 0.4)
        safety.release_controller("student-client")
        assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
        safety.close()
        print("SAFETY STOP OK")
    """),
        ("SAFETY STOP OK",),
        75,
        "C",
    ),
    NetworkUnit(
        "integrazione",
        "Integra controllo e stato",
        "collegare comando realtime e telemetria",
        "WebSocket, stato, stop",
        "Invia un comando, leggi lo stato e chiudi lasciando Romeo fermo.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.web import create_app

        with TestClient(create_app()) as client:
            with client.websocket_connect("/ws/control") as control:
                control.receive_json()
                control.send_json({"command": "FORWARD", "speed": 0.2})
                assert control.receive_json()["type"] == "ack"
                control.send_json({"command": "STOP"})
                assert control.receive_json()["type"] == "ack"
            assert client.get("/api/status").json()["moving"] is False
        print("INTEGRAZIONE OK")
    """),
        ("INTEGRAZIONE OK",),
        90,
        "C",
    ),
    NetworkUnit(
        "capstone-telepresence",
        "Capstone telepresenza",
        "integrare video, controllo, telemetria e safety",
        "architettura, camera, realtime, fail-safe",
        "Verifica foto, stato, controllo WebSocket e stop alla fine della sessione.",
        code("""
        from fastapi.testclient import TestClient
        from romeo.camera.mock import MockCameraService
        from romeo.web import create_app

        with TestClient(create_app(camera=MockCameraService())) as client:
            assert client.get("/api/camera/photo").status_code == 200
            assert client.get("/api/status").json()["status"] == "ok"
            with client.websocket_connect("/ws/control") as control:
                control.receive_json()
                control.send_json({"command": "FORWARD", "speed": 0.2})
                assert control.receive_json()["command"] == "forward"
                control.send_json({"command": "STOP"})
                assert control.receive_json()["command"] == "stop"
            assert client.get("/api/status").json()["moving"] is False
        print("FOTO OK")
        print("CONTROLLO WS OK")
        print("TELEMETRIA STOP OK")
    """),
        ("FOTO OK", "CONTROLLO WS OK", "TELEMETRIA STOP OK"),
        120,
        "C",
    ),
)


def activity(index: int, unit: NetworkUnit) -> dict[str, object]:
    identifier = f"romeo-y2-u{index:02d}-{unit.slug}"
    previous = (
        f"romeo-y1-u20-{UNITS[-1].slug}"
        if index == 1
        else f"romeo-y2-u{index - 1:02d}-{UNITS_Y2[index - 2].slug}"
    )
    return {
        "schema_version": "1.0",
        "id": identifier,
        "title": unit.title,
        "titolo": unit.title,
        "kind": "laboratorio",
        "tipo": "laboratorio",
        "language": "python",
        "linguaggio": "python",
        "difficulty": unit.difficulty,
        "difficolta": unit.difficulty,
        "topics": [part.strip() for part in unit.concepts.split(",")],
        "argomenti": [part.strip() for part in unit.concepts.split(",")],
        "objective": unit.objective,
        "prerequisites": [previous],
        "instructions": unit.task,
        "consegna": unit.task,
        "student_support_mode": "hint-progressivi",
        "grading_policy": {"compila": True, "test": True, "sandbox": True, "ai_feedback": False},
        "correzione": {"compila": True, "test": True, "sandbox": True, "ai_feedback": False},
        "metriche": {
            "tempo_stimato_minuti": unit.minutes,
            "traccia_tempo_dichiarato": True,
            "traccia_sessioni_thebitlab": True,
            "traccia_eventi_didattici": True,
            "traccia_errori_compilazione": True,
        },
        "rubrica": [
            {"criterio": "Comportamento di rete verificato", "punti": 5},
            {"criterio": "Protocollo e validazione", "punti": 2},
            {"criterio": "Cleanup e safety", "punti": 2},
            {"criterio": "Spiegazione", "punti": 1},
        ],
        "assets": [
            {
                "type": "starter",
                "path": "starter.py",
                "target_path": "main.py",
                "visibility": "student",
                "description": "Codice iniziale",
            },
            {
                "type": "fixture",
                "path": "scenario.json",
                "visibility": "grading",
                "description": "Scenario headless",
            },
            {
                "type": "fixture",
                "path": "runtime-config.json",
                "visibility": "grading",
                "description": "Check deterministici",
            },
            {
                "type": "teacher_only",
                "path": "solution.py",
                "visibility": "teacher",
                "description": "Soluzione verificata",
            },
            {
                "type": "example",
                "path": "hints.md",
                "visibility": "student",
                "description": "Hint progressivi",
            },
        ],
        "extensions": {
            "thebitlab.runtime": {
                "schema_version": "runtime_activity.v1",
                "runtime_id": "romeo-sim",
                "config": {"path": "runtime-config.json", "media_type": "application/json"},
                "required_capabilities": [
                    "headless-run",
                    "deterministic-grade",
                    "artifact-collect",
                ],
                "submission": {
                    "artifacts": [
                        {
                            "id": "main",
                            "path": "main.py",
                            "media_type": "text/x-python",
                            "required": True,
                        }
                    ]
                },
            }
        },
    }


def student_material(index: int, unit: NetworkUnit) -> str:
    return f"""# Secondo anno {index}. {unit.title}

## Obiettivo e modello mentale

In questa unità imparerai a {unit.objective}. Userai {unit.concepts}. Separa sempre tre domande:
chi comunica, quale messaggio attraversa il confine e quale risposta prova che l'operazione è
riuscita. Il robot non deve conoscere i dettagli del trasporto: socket, REST e WebSocket arrivano
alla stessa API Romeo attraverso adapter distinti.

## Laboratorio

{unit.task}

1. Disegna endpoint e direzione dei messaggi.
2. Completa `starter.py` con la minima operazione osservabile.
3. Verifica dati e status prima di stampare il marker richiesto dal grader.
4. Chiudi socket, camera o sessioni anche in caso di errore.
5. Esegui due volte: un risultato deterministico deve essere ripetibile.

## Debug guidato

Un timeout suggerisce spesso che un endpoint attende dati o una chiusura. Una risposta ricevuta non
è automaticamente valida: controlla tipo, schema, status e valori. Per JSON distingui testo e
oggetto Python; per HTTP distingui trasporto, metodo e risorsa; per WebSocket considera la durata
della connessione e lo STOP alla disconnessione. Non esporre il server della classe su Internet.
Usa loopback durante gli esperimenti e non inserire segreti nel sorgente.

## Autoverifica

Sai spiegare perché questa tecnologia è adatta al compito? Quale failure hai gestito? Dove avviene
la validazione? Quale istruzione libera la risorsa? Mostra un'evidenza concreta: risposta, marker,
stato motori o test. Poi descrivi come cambierebbe solo l'adapter passando dal simulatore al Romeo
fisico.
"""


def teacher_material(index: int, unit: NetworkUnit) -> str:
    return f"""# Guida docente — secondo anno {index}. {unit.title}

Durata: {unit.minutes} minuti. Difficoltà: {unit.difficulty}. Obiettivo osservabile: lo studente sa
{unit.objective} e giustifica protocollo, validazione e cleanup.

## Conduzione

- 0–10 min: mappa alla lavagna di client, server, request e response.
- 10–25 min: dimostrazione su loopback, prima con previsione e poi con trace.
- 25–50 min: pair programming; un ruolo cura il protocollo, l'altro failure e risorse.
- 50–{unit.minutes} min: run TheBitLab, revisione dell'evidenza ed exit ticket.

Il marker di output viene valutato soltanto se il programma arriva alla relativa stampa; chiedere
agli studenti di mantenerlo dopo gli assert, mai prima. Per valutazioni sommative aggiungere test
riservati nel sandbox TheBitLab: i check dichiarativi sono feedback trasparente, non una barriera
anti-manomissione.

## Misconcezioni e safety

`localhost` non è il Raspberry Pi remoto; una porta non identifica da sola un protocollo; JSON non
è una connessione; REST e WebSocket non sono sinonimi. Una UI chiusa deve causare STOP, e il
watchdog resta obbligatorio. Evitare rete pubblica e camera reale senza autorizzazioni e informativa.

## Inclusione ed evidenze

Fornire diagrammi con colori per endpoint e frecce. Permettere prima una simulazione con coppie di
socket o TestClient. Estensione: introdurre un payload non valido e progettare l'errore. Evidenze:
sorgente, marker, gestione errori, chiusura risorse e spiegazione orale. Collegare il debrief alla
prossima unità senza anticipare più di un nuovo livello di protocollo.
"""


def build() -> None:
    build_first_year()
    bundle = json.loads((COURSE / "bundle.json").read_text(encoding="utf-8"))
    curriculum = json.loads((COURSE / "curriculum.json").read_text(encoding="utf-8"))
    for index, unit in enumerate(UNITS_Y2, start=1):
        unit_id = f"y2-u{index:02d}-{unit.slug}"
        base = COURSE / "activities" / unit_id
        dump(base / "activity.json", activity(index, unit))
        dump(
            base / "scenario.json",
            {"schema_version": "romeo.scenario.v1", "id": unit_id, "checks": []},
        )
        dump(
            base / "runtime-config.json",
            {
                "schema_version": "romeo.thebitlab.v1",
                "scenario": "scenario.json",
                "submission_artifact_id": "main",
                "max_simulation_seconds": 20,
                "stdout_checks": [
                    {"name": marker, "contains": marker, "points": 1} for marker in unit.markers
                ],
            },
        )
        write(
            base / "starter.py",
            f'"""{unit.task}\n\nTODO: completa il laboratorio e stampa il marker solo dopo le verifiche.\n"""\n',
        )
        write(base / "solution.py", unit.solution)
        write(
            base / "hints.md",
            f"# Hint progressivi\n\n1. Disegna prima gli endpoint e la direzione del messaggio.\n2. Verifica {unit.concepts} e chiudi ogni risorsa.\n3. Confronta la tua struttura con le API già importate negli esempi del corso, senza copiare il marker prima degli assert.\n",
        )
        student = f"materials/student/{unit_id}.md"
        teacher = f"materials/teacher/{unit_id}.md"
        worksheet = f"handouts/{unit_id}-worksheet.md"
        assessment = f"handouts/{unit_id}-assessment.md"
        handouts = [worksheet, assessment]
        if index == len(UNITS_Y2):
            handouts.append("handouts/y2-u23-capstone-rubric.md")
        write(COURSE / student, student_material(index, unit))
        write(COURSE / teacher, teacher_material(index, unit))
        write(
            COURSE / worksheet,
            f"# Traccia di rete — {unit.title}\n\nEndpoint A: __________ Endpoint B: __________\n\nMessaggio/request: __________\n\nRisposta attesa e validazione: __________\n\nErrore simulato: __________ Cleanup/STOP: __________\n",
        )
        write(
            COURSE / assessment,
            f"# Exit ticket — {unit.title}\n\n1. Motiva la tecnologia scelta.\n2. Scrivi un'invariante del protocollo.\n3. Indica come hai verificato errore, cleanup e safety.\n4. Allega il marker e una seconda evidenza osservabile.\n",
        )
        bundle["content"]["units"].append(
            {
                "id": unit_id,
                "title": unit.title,
                "order": 20 + index,
                "activities": [f"activities/{unit_id}/activity.json"],
                "materials": [student, teacher],
                "handouts": handouts,
            }
        )
    curriculum["years"].append(
        {
            "year": 2,
            "focus": "Networking, servizi web, controllo realtime e telepresenza",
            "units": [
                {
                    "id": f"y2-u{index:02d}-{unit.slug}",
                    "year": 2,
                    "order": index,
                    "title": unit.title,
                    "objective": unit.objective,
                    "estimated_minutes": unit.minutes,
                    "difficulty": unit.difficulty,
                    "activity": f"activities/y2-u{index:02d}-{unit.slug}/activity.json",
                }
                for index, unit in enumerate(UNITS_Y2, start=1)
            ],
        }
    )
    bundle["version"] = "0.2.0"
    dump(COURSE / "bundle.json", bundle)
    dump(COURSE / "curriculum.json", curriculum)
    index_units = []
    for unit in bundle["content"]["units"]:
        items = [
            {"type": item_type, "path": path}
            for field, item_type in (
                ("activities", "activity"),
                ("materials", "material"),
                ("handouts", "handout"),
            )
            for path in unit.get(field, [])
        ]
        index_units.append(
            {
                "id": unit["id"],
                "title": unit["title"],
                "order": unit["order"],
                "items": items,
            }
        )
    dump(COURSE / "index.json", {"units": index_units})
    write(
        COURSE / "handouts" / "y2-u23-capstone-rubric.md",
        """# Rubrica capstone telepresenza\n\n| Criterio | 0 | 1 | 2 |\n| --- | --- | --- | --- |\n| Controllo | Assente | Parziale | WebSocket validato e STOP finale |\n| Telemetria | Assente | Dato singolo | Stato versionato e interpretato |\n| Camera | Assente | Foto senza controlli | JPEG verificato e servizio isolato |\n| Safety | Movimento persistente | Stop manuale | Lease, timeout e disconnect spiegati |\n| Architettura | Accoppiata | Confini parziali | API, protocollo e backend separati |\n\nLa demo fisica richiede checklist docente, area libera e consenso per la camera.\n""",
    )
    write(
        COURSE / "docs" / "second-year-plan.md",
        """# Piano del secondo anno\n\nVentitré unità introducono rete, socket e protocollo testuale prima di JSON, HTTP, REST e WebSocket. Camera, input event-driven, gamepad, telemetria e safety convergono nel capstone telepresenza. I laboratori usano loopback, test double e TestClient; la rete esterna e la camera reale non sono prerequisiti.\n\nCon un solo robot, i gruppi ruotano tra client, server, osservabilità e verifica safety. La prova fisica avviene soltanto dopo il superamento deterministico e usa un controller attivo alla volta.\n""",
    )
    write(
        COURSE / "README.md",
        "# Course Bundle Romeo\n\nCourse Bundle TheBitLab originale per il primo e secondo anno. Contiene attività, scenari, starter, hint, soluzioni verificate, materiali studente/docente e handout. Rigenera tutto con `python scripts/build_second_year_bundle.py`; valida con `python scripts/validate_course.py`.\n",
    )


if __name__ == "__main__":
    build()
