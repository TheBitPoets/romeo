"""Importable student contracts and hidden behavioural checks for year two."""

# ruff: noqa: E501 -- embedded teaching and grading programs remain readable strings.

from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class Y2Contract:
    """Generated code and the public callable names assessed by TheBitLab."""

    entrypoints: tuple[str, ...]
    starter: str
    solution: str
    hidden_tests: str


def _code(value: str) -> str:
    return dedent(value).lstrip()


def _contract(
    entrypoints: str | tuple[str, ...], starter: str, solution: str, tests: str
) -> Y2Contract:
    names = (entrypoints,) if isinstance(entrypoints, str) else entrypoints
    return Y2Contract(names, _code(starter), _code(solution), _code(tests))


CONTRACTS_Y2: dict[str, Y2Contract] = {
    "rete": _contract(
        "is_loopback",
        '''
        from ipaddress import ip_address

        def is_loopback(address):
            """Restituisce True se address indica questo stesso computer."""
            # TODO: converti address con ip_address e controlla is_loopback.
            pass
        ''',
        '''
        from ipaddress import ip_address

        def is_loopback(address):
            """Restituisce True se address indica questo stesso computer."""
            return ip_address(address).is_loopback
        ''',
        '''
        import pytest
        from main import is_loopback

        def test_classifica_indirizzi_diversi():
            assert is_loopback("127.0.0.1") is True
            assert is_loopback("127.2.3.4") is True
            assert is_loopback("192.0.2.4") is False

        def test_rifiuta_testo_non_ip():
            with pytest.raises(ValueError):
                is_loopback("romeo.local")
        ''',
    ),
    "indirizzi-ip": _contract(
        "resolve_ipv4",
        '''
        import socket
        from ipaddress import ip_address

        def resolve_ipv4(hostname):
            """Risolve hostname e restituisce un indirizzo IPv4 valido."""
            # TODO: usa socket.gethostbyname e valida il risultato.
            pass
        ''',
        '''
        import socket
        from ipaddress import ip_address

        def resolve_ipv4(hostname):
            """Risolve hostname e restituisce un indirizzo IPv4 valido."""
            address = socket.gethostbyname(hostname)
            if ip_address(address).version != 4:
                raise ValueError("il resolver non ha restituito IPv4")
            return address
        ''',
        '''
        import main

        def test_usa_il_nome_ricevuto_e_non_hardcode(monkeypatch):
            calls = []
            def resolve(name):
                calls.append(name)
                return "192.0.2.81"
            monkeypatch.setattr(main.socket, "gethostbyname", resolve)
            assert main.resolve_ipv4("robot.example") == "192.0.2.81"
            assert calls == ["robot.example"]
        ''',
    ),
    "porte": _contract(
        "choose_free_port",
        '''
        import socket

        def choose_free_port():
            """Chiede al sistema una porta libera sul loopback."""
            # TODO: usa bind(("127.0.0.1", 0)) e restituisci la porta.
            pass
        ''',
        '''
        import socket

        def choose_free_port():
            """Chiede al sistema una porta libera sul loopback."""
            with socket.socket() as listener:
                listener.bind(("127.0.0.1", 0))
                return listener.getsockname()[1]
        ''',
        '''
        from main import choose_free_port

        def test_restituisce_una_porta_effimera_valida():
            port = choose_free_port()
            assert isinstance(port, int)
            assert 0 < port < 65536
        ''',
    ),
    "client-server": _contract(
        "exchange_ping_pong",
        '''
        def exchange_ping_pong(client, server):
            """Scambia PING e PONG sui due socket già collegati."""
            # TODO: usa sendall e recv e restituisci i due messaggi ricevuti.
            pass
        ''',
        '''
        def exchange_ping_pong(client, server):
            """Scambia PING e PONG sui due socket già collegati."""
            client.sendall(b"PING\\n")
            request = server.recv(16)
            server.sendall(b"PONG\\n")
            response = client.recv(16)
            return request, response
        ''',
        '''
        from main import exchange_ping_pong

        class Endpoint:
            def __init__(self, incoming):
                self.incoming = incoming
                self.sent = []
            def sendall(self, data):
                self.sent.append(data)
            def recv(self, size):
                assert size > 0
                return self.incoming

        def test_scambia_byte_nei_due_sensi():
            client = Endpoint(b"PONG\\n")
            server = Endpoint(b"PING\\n")
            assert exchange_ping_pong(client, server) == (b"PING\\n", b"PONG\\n")
            assert client.sent == [b"PING\\n"]
            assert server.sent == [b"PONG\\n"]
        ''',
    ),
    "socket": _contract(
        "tcp_request",
        '''
        import socket

        def tcp_request(host, port, message=b"HELLO\\n"):
            """Invia message a un server TCP e restituisce la risposta."""
            # TODO: apri la connessione con un context manager.
            pass
        ''',
        '''
        import socket

        def tcp_request(host, port, message=b"HELLO\\n"):
            """Invia message a un server TCP e restituisce la risposta."""
            with socket.create_connection((host, port), timeout=2.0) as client:
                client.sendall(message)
                return client.recv(1024)
        ''',
        '''
        import main

        class Connection:
            def __init__(self):
                self.sent = []
                self.closed = False
            def __enter__(self): return self
            def __exit__(self, *args): self.closed = True
            def sendall(self, data): self.sent.append(data)
            def recv(self, size): return b"WELCOME\\n"

        def test_connette_invia_riceve_e_chiude(monkeypatch):
            connection = Connection()
            calls = []
            monkeypatch.setattr(main.socket, "create_connection", lambda endpoint, timeout: calls.append((endpoint, timeout)) or connection)
            assert main.tcp_request("127.0.0.1", 4321, b"CIAO\\n") == b"WELCOME\\n"
            assert calls == [(("127.0.0.1", 4321), 2.0)]
            assert connection.sent == [b"CIAO\\n"] and connection.closed
        ''',
    ),
    "protocollo-testuale": _contract(
        "parse_command_line",
        '''
        from romeo.network.protocol import parse_command

        def parse_command_line(line):
            """Valida una riga Romeo/1 e restituisce nome e argomenti."""
            # TODO: usa parse_command e restituisci una tupla semplice.
            pass
        ''',
        '''
        from romeo.network.protocol import parse_command

        def parse_command_line(line):
            """Valida una riga Romeo/1 e restituisce nome e argomenti."""
            command = parse_command(line)
            return command.name, command.arguments
        ''',
        '''
        import pytest
        from main import parse_command_line

        def test_accetta_comandi_validi():
            assert parse_command_line("FORWARD 0.4") == ("FORWARD", (0.4,))
            assert parse_command_line("STOP") == ("STOP", ())

        @pytest.mark.parametrize("line", ["DANCE", "STOP 1", "FORWARD 0.2 0.3", "FORWARD nan"])
        def test_rifiuta_comandi_non_validi(line):
            with pytest.raises(ValueError):
                parse_command_line(line)
        ''',
    ),
    "json": _contract(
        ("encode_state", "decode_state"),
        '''
        import json

        def encode_state(state):
            """Codifica uno stato come testo JSON."""
            pass

        def decode_state(text):
            """Decodifica e valida type, motors e moving."""
            pass
        ''',
        '''
        import json

        def encode_state(state):
            """Codifica uno stato come testo JSON."""
            return json.dumps(state)

        def decode_state(text):
            """Decodifica e valida type, motors e moving."""
            state = json.loads(text)
            if state.get("type") != "state":
                raise ValueError("type deve essere state")
            if not isinstance(state.get("motors"), list) or len(state["motors"]) != 2:
                raise ValueError("motors deve contenere due valori")
            if not isinstance(state.get("moving"), bool):
                raise ValueError("moving deve essere booleano")
            return state
        ''',
        '''
        import json
        import pytest
        from main import decode_state, encode_state

        def test_round_trip_non_hardcoded():
            state = {"type": "state", "motors": [-0.2, 0.7], "moving": True}
            wire = encode_state(state)
            assert isinstance(wire, str) and json.loads(wire) == state
            assert decode_state(wire) == state

        @pytest.mark.parametrize("bad", [{"type":"other","motors":[0,0],"moving":False}, {"type":"state","motors":0,"moving":False}, {"type":"state","motors":[0,0],"moving":1}])
        def test_valida_i_tipi(bad):
            with pytest.raises(ValueError): decode_state(json.dumps(bad))
        ''',
    ),
    "http": _contract(
        "fetch_status",
        '''
        import json
        import urllib.request

        def fetch_status(url):
            """Esegue GET e restituisce il body JSON di una risposta 200."""
            # TODO: usa urlopen come context manager e controlla status.
            pass
        ''',
        '''
        import json
        import urllib.request

        def fetch_status(url):
            """Esegue GET e restituisce il body JSON di una risposta 200."""
            with urllib.request.urlopen(url, timeout=2.0) as response:
                if response.status != 200:
                    raise ValueError("status HTTP inatteso")
                return json.load(response)
        ''',
        '''
        import io
        import main
        import pytest

        class Response(io.BytesIO):
            def __init__(self, body, status=200): super().__init__(body); self.status=status; self.closed_by_context=False
            def __enter__(self): return self
            def __exit__(self, *args): self.closed_by_context=True; self.close()

        def test_get_json_e_cleanup(monkeypatch):
            response = Response(b'{"status":"ready"}')
            monkeypatch.setattr(main.urllib.request, "urlopen", lambda url, timeout: response)
            assert main.fetch_status("http://127.0.0.1/status") == {"status":"ready"}
            assert response.closed_by_context

        def test_rifiuta_status_non_200(monkeypatch):
            monkeypatch.setattr(main.urllib.request, "urlopen", lambda url, timeout: Response(b'{}', 503))
            with pytest.raises(ValueError): main.fetch_status("http://local/status")
        ''',
    ),
    "rest": _contract(
        "read_robot_status",
        '''
        def read_robot_status(client):
            """Legge e valida la risorsa REST /api/status."""
            pass
        ''',
        '''
        def read_robot_status(client):
            """Legge e valida la risorsa REST /api/status."""
            response = client.get("/api/status")
            if response.status_code != 200:
                raise ValueError("status REST inatteso")
            data = response.json()
            if "status" not in data or "moving" not in data:
                raise ValueError("risposta incompleta")
            return data
        ''',
        '''
        import pytest
        from main import read_robot_status

        class Response:
            status_code=200
            def json(self): return {"status":"ok", "moving":True, "nonce":17}
        class Client:
            def __init__(self): self.paths=[]
            def get(self, path): self.paths.append(path); return Response()

        def test_legge_la_risorsa_senza_hardcode():
            client=Client()
            assert read_robot_status(client)["nonce"] == 17
            assert client.paths == ["/api/status"]
        ''',
    ),
    "fastapi": _contract(
        "create_status_app",
        '''
        from fastapi import FastAPI

        def create_status_app():
            """Crea un'app FastAPI con GET /status."""
            app = FastAPI()
            # TODO: aggiungi la route e restituisci app.
            return app
        ''',
        '''
        from fastapi import FastAPI

        def create_status_app():
            """Crea un'app FastAPI con GET /status."""
            app = FastAPI()
            @app.get("/status")
            def status():
                return {"robot": "romeo", "ready": True}
            return app
        ''',
        '''
        from fastapi.testclient import TestClient
        from main import create_status_app

        def test_contratto_http_della_app():
            client=TestClient(create_status_app())
            assert client.get("/status").json() == {"robot":"romeo", "ready":True}
            assert client.post("/status").status_code == 405
        ''',
    ),
    "websocket": _contract(
        "request_stop",
        '''
        def request_stop(client):
            """Apre /ws/control, invia STOP e restituisce l'ack."""
            pass
        ''',
        '''
        def request_stop(client):
            """Apre /ws/control, invia STOP e restituisce l'ack."""
            with client.websocket_connect("/ws/control") as websocket:
                ready = websocket.receive_json()
                if ready.get("type") != "ready":
                    raise ValueError("WebSocket non pronto")
                websocket.send_json({"command": "STOP"})
                ack = websocket.receive_json()
                if ack.get("type") != "ack":
                    raise ValueError("ack mancante")
                return ack
        ''',
        '''
        from main import request_stop

        class Socket:
            def __init__(self): self.received=iter([{"type":"ready"},{"type":"ack","command":"stop"}]); self.sent=[]; self.closed=False
            def __enter__(self): return self
            def __exit__(self,*args): self.closed=True
            def receive_json(self): return next(self.received)
            def send_json(self,data): self.sent.append(data)
        class Client:
            def __init__(self): self.socket=Socket(); self.path=None
            def websocket_connect(self,path): self.path=path; return self.socket

        def test_handshake_stop_ack_e_close():
            client=Client()
            assert request_stop(client)["command"] == "stop"
            assert client.path == "/ws/control"
            assert client.socket.sent == [{"command":"STOP"}] and client.socket.closed
        ''',
    ),
    "web-controller": _contract(
        "drive_then_stop",
        '''
        def drive_then_stop(client, speed):
            """Invia FORWARD e garantisce STOP prima di chiudere."""
            pass
        ''',
        '''
        def drive_then_stop(client, speed):
            """Invia FORWARD e garantisce STOP prima di chiudere."""
            with client.websocket_connect("/ws/control") as websocket:
                websocket.receive_json()
                forward_ack = None
                try:
                    websocket.send_json({"command": "FORWARD", "speed": speed})
                    forward_ack = websocket.receive_json()
                finally:
                    websocket.send_json({"command": "STOP"})
                    stop_ack = websocket.receive_json()
                return forward_ack, stop_ack
        ''',
        '''
        import pytest
        from main import drive_then_stop

        class Socket:
            def __init__(self, fail=False): self.sent=[]; self.count=0; self.fail=fail
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def send_json(self,data): self.sent.append(data)
            def receive_json(self):
                self.count += 1
                if self.fail and self.count == 2: raise RuntimeError("lost ack")
                return {"type":"ready"} if self.count==1 else {"type":"ack"}
        class Client:
            def __init__(self,socket): self.socket=socket
            def websocket_connect(self,path): assert path=="/ws/control"; return self.socket

        def test_velocita_variabile_e_stop():
            socket=Socket(); drive_then_stop(Client(socket), 0.37)
            assert socket.sent == [{"command":"FORWARD","speed":0.37},{"command":"STOP"}]

        def test_stop_anche_se_ack_fallisce():
            socket=Socket(True)
            with pytest.raises(RuntimeError): drive_then_stop(Client(socket), 0.2)
            assert socket.sent[-1] == {"command":"STOP"}
        ''',
    ),
    "tastiera-remota": _contract(
        "commands_for_keys",
        '''
        from romeo.network.keyboard import command_for_key

        def commands_for_keys(keys):
            """Traduce i tasti e termina sempre la sequenza con STOP."""
            pass
        ''',
        '''
        from romeo.network.keyboard import command_for_key

        def commands_for_keys(keys):
            """Traduce i tasti e termina sempre la sequenza con STOP."""
            commands = []
            for key in keys:
                try:
                    command = command_for_key(key.lower())
                except ValueError:
                    continue
                if command is not None:
                    commands.append(command.name)
            if not commands or commands[-1] != "STOP":
                commands.append("STOP")
            return commands
        ''',
        '''
        from main import commands_for_keys

        def test_mappa_tasti_e_stop_finale():
            assert commands_for_keys(["W", "x", "a"]) == ["FORWARD", "LEFT", "STOP"]
            assert commands_for_keys([]) == ["STOP"]
            assert commands_for_keys([" "]) == ["STOP"]
        ''',
    ),
    "camera": _contract(
        "capture_photo",
        '''
        def capture_photo(camera):
            """Acquisisce una foto usando il servizio ricevuto."""
            pass
        ''',
        '''
        def capture_photo(camera):
            """Acquisisce una foto usando il servizio ricevuto."""
            photo = camera.capture_photo()
            if not isinstance(photo, bytes):
                raise ValueError("la foto deve essere bytes")
            return photo
        ''',
        '''
        import pytest
        from main import capture_photo

        class Camera:
            def __init__(self, photo): self.photo=photo; self.calls=0
            def capture_photo(self): self.calls+=1; return self.photo

        def test_usa_il_servizio_iniettato_una_volta():
            camera=Camera(b"photo-17")
            assert capture_photo(camera) == b"photo-17" and camera.calls == 1

        def test_rifiuta_un_risultato_non_bytes():
            with pytest.raises(ValueError): capture_photo(Camera("photo"))
        ''',
    ),
    "pan-tilt": _contract(
        "point_camera",
        '''
        def point_camera(robot, pan, tilt):
            """Orienta la camera attraverso la API Robot."""
            # TODO: chiama robot.look con gli angoli ricevuti.
            pass
        ''',
        '''
        def point_camera(robot, pan, tilt):
            """Orienta la camera attraverso la API Robot."""
            robot.look(pan, tilt)
        ''',
        '''
        from main import point_camera

        class Robot:
            def __init__(self): self.calls=[]
            def look(self, pan, tilt): self.calls.append((pan,tilt))

        def test_inoltra_angoli_diversi():
            robot=Robot(); point_camera(robot, 31, 149); point_camera(robot, 90, 45)
            assert robot.calls == [(31,149),(90,45)]
        ''',
    ),
    "fotografia": _contract(
        "download_photo",
        '''
        def download_photo(client):
            """Scarica e valida una foto JPEG dalla REST API."""
            pass
        ''',
        '''
        def download_photo(client):
            """Scarica e valida una foto JPEG dalla REST API."""
            response = client.get("/api/camera/photo")
            if response.status_code != 200:
                raise ValueError("foto non disponibile")
            if not response.headers.get("content-type", "").startswith("image/jpeg"):
                raise ValueError("media type inatteso")
            return response.content
        ''',
        '''
        import pytest
        from main import download_photo

        class Response:
            status_code=200; headers={"content-type":"image/jpeg"}; content=b"jpeg-variable"
        class Client:
            def __init__(self): self.paths=[]
            def get(self,path): self.paths.append(path); return Response()

        def test_path_media_type_e_contenuto():
            client=Client(); assert download_photo(client) == b"jpeg-variable"
            assert client.paths == ["/api/camera/photo"]
        ''',
    ),
    "video": _contract(
        "first_video_frame",
        '''
        def first_video_frame(camera, fps=10):
            """Legge e valida il primo frame JPEG dello stream."""
            pass
        ''',
        '''
        def first_video_frame(camera, fps=10):
            """Legge e valida il primo frame JPEG dello stream."""
            frame = next(camera.frames(frames_per_second=fps))
            if not frame.startswith(b"\\xff\\xd8") or not frame.endswith(b"\\xff\\xd9"):
                raise ValueError("frame JPEG non valido")
            return frame
        ''',
        '''
        import pytest
        from main import first_video_frame

        class Camera:
            def __init__(self, frame): self.frame=frame; self.fps=[]
            def frames(self, frames_per_second): self.fps.append(frames_per_second); yield self.frame; raise AssertionError("consumato più di un frame")

        def test_un_solo_frame_e_fps_inoltrato():
            camera=Camera(b"\\xff\\xd8body\\xff\\xd9")
            assert first_video_frame(camera, 7) == b"\\xff\\xd8body\\xff\\xd9"
            assert camera.fps == [7]

        def test_rifiuta_frame_non_jpeg():
            with pytest.raises(ValueError): first_video_frame(Camera(b"png"))
        ''',
    ),
    "eventi": _contract(
        "dispatch_events",
        '''
        def dispatch_events(events, handler):
            """Consegna ogni evento al callback nello stesso ordine."""
            pass
        ''',
        '''
        def dispatch_events(events, handler):
            """Consegna ogni evento al callback nello stesso ordine."""
            for event in events:
                handler(event)
        ''',
        '''
        import pytest
        from main import dispatch_events

        def test_dispatch_fifo():
            events=[{"type":"key","value":"w"},{"type":"key","value":"space"}]
            handled=[]; dispatch_events(events, handled.append)
            assert handled == events

        def test_si_ferma_se_handler_fallisce():
            handled=[]
            def handler(event):
                handled.append(event)
                if event == 2: raise RuntimeError("stop")
            with pytest.raises(RuntimeError): dispatch_events([1,2,3], handler)
            assert handled == [1,2]
        ''',
    ),
    "gamepad": _contract(
        "stick_to_wheels",
        '''
        from romeo.gamepad import GamepadMapping, wheel_speeds

        def stick_to_wheels(x, y, max_speed=0.6):
            """Converte gli assi dello stick in velocità delle ruote."""
            pass
        ''',
        '''
        from romeo.gamepad import GamepadMapping, wheel_speeds

        def stick_to_wheels(x, y, max_speed=0.6):
            """Converte gli assi dello stick in velocità delle ruote."""
            return wheel_speeds(x, y, GamepadMapping(max_speed=max_speed))
        ''',
        '''
        import pytest
        from main import stick_to_wheels

        @pytest.mark.parametrize("x,y,expected", [(0,-1,(0.6,0.6)),(0,1,(-0.6,-0.6)),(0.02,0.02,(0,0))])
        def test_direzioni_dead_zone_e_limiti(x,y,expected):
            assert stick_to_wheels(x,y) == pytest.approx(expected)

        def test_max_speed_non_hardcoded():
            assert stick_to_wheels(0,-1,0.35) == pytest.approx((0.35,0.35))
        ''',
    ),
    "telemetria": _contract(
        "read_telemetry",
        '''
        def read_telemetry(engine):
            """Legge e valida uno snapshot dal simulation engine."""
            pass
        ''',
        '''
        def read_telemetry(engine):
            """Legge e valida uno snapshot dal simulation engine."""
            state = engine.state()
            if state.get("schema_version") != "romeo.simulation.state.v1":
                raise ValueError("schema telemetria inatteso")
            required = {"pose", "motors", "camera", "time"}
            if not required <= state.keys():
                raise ValueError("telemetria incompleta")
            return state
        ''',
        '''
        from main import read_telemetry

        class Engine:
            def state(self): return {"schema_version":"romeo.simulation.state.v1","pose":{"x":17},"motors":{},"camera":{},"time":3.5}

        def test_restituisce_lo_snapshot_del_engine():
            state=read_telemetry(Engine())
            assert state["pose"]["x"] == 17 and state["time"] == 3.5
        ''',
    ),
    "safety": _contract(
        "drive_safely",
        '''
        def drive_safely(safety, controller_id, speed):
            """Acquisisce il controllo, muove e rilascia sempre la lease."""
            pass
        ''',
        '''
        def drive_safely(safety, controller_id, speed):
            """Acquisisce il controllo, muove e rilascia sempre la lease."""
            safety.claim_controller(controller_id)
            try:
                safety.set_motor_speeds_for(controller_id, speed, speed)
            finally:
                safety.release_controller(controller_id)
        ''',
        '''
        import pytest
        from main import drive_safely

        class Safety:
            def __init__(self,fail=False): self.calls=[]; self.fail=fail
            def claim_controller(self,c): self.calls.append(("claim",c))
            def set_motor_speeds_for(self,c,l,r): self.calls.append(("move",c,l,r));\
                (_ for _ in ()).throw(RuntimeError("motor")) if self.fail else None
            def release_controller(self,c): self.calls.append(("release",c))

        def test_ownership_velocita_e_release():
            safety=Safety(); drive_safely(safety,"student-7",0.34)
            assert safety.calls == [("claim","student-7"),("move","student-7",0.34,0.34),("release","student-7")]

        def test_release_anche_su_errore():
            safety=Safety(True)
            with pytest.raises(RuntimeError): drive_safely(safety,"student",0.2)
            assert safety.calls[-1] == ("release","student")
        ''',
    ),
    "integrazione": _contract(
        "control_and_read",
        '''
        def control_and_read(client, speed):
            """Muove via WebSocket, garantisce STOP e legge lo stato REST."""
            pass
        ''',
        '''
        def control_and_read(client, speed):
            """Muove via WebSocket, garantisce STOP e legge lo stato REST."""
            with client.websocket_connect("/ws/control") as control:
                control.receive_json()
                try:
                    control.send_json({"command":"FORWARD", "speed":speed})
                    control.receive_json()
                finally:
                    control.send_json({"command":"STOP"})
                    control.receive_json()
            state = client.get("/api/status").json()
            if state.get("moving") is not False:
                raise ValueError("Romeo non è fermo")
            return state
        ''',
        '''
        from main import control_and_read

        class Socket:
            def __init__(self): self.sent=[]; self.responses=iter([{"type":"ready"},{"type":"ack"},{"type":"ack"}])
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def send_json(self,data): self.sent.append(data)
            def receive_json(self): return next(self.responses)
        class Response:
            def json(self): return {"moving":False,"nonce":29}
        class Client:
            def __init__(self): self.socket=Socket(); self.paths=[]
            def websocket_connect(self,path): assert path=="/ws/control"; return self.socket
            def get(self,path): self.paths.append(path); return Response()

        def test_controllo_stop_e_stato_non_hardcoded():
            client=Client(); state=control_and_read(client,0.41)
            assert client.socket.sent == [{"command":"FORWARD","speed":0.41},{"command":"STOP"}]
            assert client.paths == ["/api/status"] and state["nonce"] == 29
        ''',
    ),
    "capstone-telepresence": _contract(
        "run_telepresence_session",
        '''
        def run_telepresence_session(client, speed=0.2):
            """Integra foto, stato, controllo realtime e STOP fail-safe."""
            pass
        ''',
        '''
        def run_telepresence_session(client, speed=0.2):
            """Integra foto, stato, controllo realtime e STOP fail-safe."""
            photo_response = client.get("/api/camera/photo")
            if photo_response.status_code != 200:
                raise ValueError("foto non disponibile")
            before = client.get("/api/status").json()
            with client.websocket_connect("/ws/control") as control:
                control.receive_json()
                try:
                    control.send_json({"command":"FORWARD", "speed":speed})
                    forward_ack = control.receive_json()
                finally:
                    control.send_json({"command":"STOP"})
                    stop_ack = control.receive_json()
            after = client.get("/api/status").json()
            if after.get("moving") is not False:
                raise ValueError("STOP non confermato")
            return {"photo":photo_response.content, "before":before, "after":after, "acks":[forward_ack,stop_ack]}
        ''',
        '''
        from main import run_telepresence_session

        class Response:
            def __init__(self,content=b"",data=None): self.status_code=200; self.content=content; self._data=data
            def json(self): return self._data
        class Socket:
            def __init__(self): self.sent=[]; self.responses=iter([{"type":"ready"},{"type":"ack","n":1},{"type":"ack","n":2}])
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def send_json(self,data): self.sent.append(data)
            def receive_json(self): return next(self.responses)
        class Client:
            def __init__(self): self.socket=Socket(); self.statuses=iter([{"moving":False,"n":1},{"moving":False,"n":2}])
            def get(self,path):
                return Response(b"jpeg-53") if path.endswith("photo") else Response(data=next(self.statuses))
            def websocket_connect(self,path): assert path=="/ws/control"; return self.socket

        def test_integra_e_non_hardcode_dati_o_velocita():
            client=Client(); result=run_telepresence_session(client,0.43)
            assert result["photo"] == b"jpeg-53" and result["after"]["n"] == 2
            assert client.socket.sent == [{"command":"FORWARD","speed":0.43},{"command":"STOP"}]
        ''',
    ),
}
