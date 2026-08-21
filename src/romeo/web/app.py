"""FastAPI host for the renderer-neutral Romeo simulation protocol."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from romeo.network.control import execute_command
from romeo.network.protocol import Command, ProtocolError, parse_command
from romeo.safety import ControllerAccessError, ControllerBusyError, SafetyBackend
from romeo.simulation.engine import SimulationEngine
from romeo.simulation.scenario import SCENARIO_SCHEMA, Scenario

STATIC_DIRECTORY = Path(__file__).parent / "static"


class SimulationSession:
    """Advance an engine for an interactive viewer without changing headless semantics."""

    def __init__(self, engine: SimulationEngine, *, tick_seconds: float = 0.02) -> None:
        self.engine = engine
        self.tick_seconds = tick_seconds
        self._task: asyncio.Task[None] | None = None

    @property
    def running(self) -> bool:
        return self._task is not None and not self._task.done()

    async def start(self) -> bool:
        if self.running:
            return False
        self._task = asyncio.create_task(self._run(), name="romeo-simulation-session")
        return True

    async def pause(self, *, stop_motors: bool = True) -> bool:
        task = self._task
        if task is None:
            if stop_motors:
                self.engine.stop()
            return False
        self._task = None
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        if stop_motors:
            self.engine.stop()
        return True

    async def reset(self) -> None:
        await self.pause(stop_motors=False)
        self.engine.reset()

    async def _run(self) -> None:
        while True:
            await asyncio.sleep(self.tick_seconds)
            self.engine.step(self.tick_seconds)


def create_app(engine: SimulationEngine | None = None) -> FastAPI:
    """Create an isolated viewer app around one simulation engine."""

    active_engine = engine or _default_engine()
    session = SimulationSession(active_engine)
    control = SafetyBackend(active_engine, max_speed=1.0, command_timeout=0.75)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        del app
        yield
        await session.pause()
        control.close()

    app = FastAPI(
        title="Romeo Simulator",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.simulation = session
    app.state.control = control

    @app.get("/", include_in_schema=False)
    async def viewer() -> FileResponse:
        return FileResponse(STATIC_DIRECTORY / "index.html")

    @app.get("/static/{asset_name}", include_in_schema=False)
    async def asset(asset_name: str) -> FileResponse:
        if asset_name not in {"viewer.js", "styles.css"}:
            return FileResponse(STATIC_DIRECTORY / "index.html", status_code=404)
        return FileResponse(STATIC_DIRECTORY / asset_name)

    @app.get("/api/state")
    async def state() -> dict[str, Any]:
        return _session_state(session)

    @app.get("/api/status")
    async def status() -> dict[str, Any]:
        return {
            "status": "ok",
            "simulation_running": session.running,
            "moving": not active_engine.stopped,
            "controller_active": control.active_controller is not None,
            "time": active_engine.time,
            "collisions": active_engine.collisions,
        }

    @app.get("/api/info")
    async def info() -> dict[str, Any]:
        return {
            "name": "Romeo",
            "version": "0.1.0",
            "backend": "simulation",
            "state_schema": SimulationEngine.STATE_SCHEMA,
            "commands": ["forward", "backward", "left", "right", "stop", "look"],
        }

    @app.post("/api/simulation/start")
    async def start() -> dict[str, Any]:
        changed = await session.start()
        return {
            "status": "started" if changed else "already_running",
            "state": _session_state(session),
        }

    @app.post("/api/simulation/stop")
    async def stop() -> dict[str, Any]:
        changed = await session.pause()
        return {
            "status": "stopped" if changed else "already_stopped",
            "state": _session_state(session),
        }

    @app.post("/api/simulation/reset")
    async def reset() -> dict[str, Any]:
        await session.reset()
        return {"status": "reset", "state": _session_state(session)}

    @app.websocket("/ws/state")
    async def websocket_state(websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            while True:
                await websocket.send_json(_session_state(session))
                await asyncio.sleep(0.05)
        except (WebSocketDisconnect, RuntimeError):
            return

    @app.websocket("/ws/control")
    async def websocket_control(websocket: WebSocket) -> None:
        await websocket.accept()
        controller_id = f"web-{uuid4().hex}"
        try:
            control.claim_controller(controller_id)
        except ControllerBusyError:
            await websocket.send_json(
                {"type": "error", "code": "controller_busy", "detail": "Romeo è già controllato"}
            )
            await websocket.close(code=1013)
            return
        try:
            await websocket.send_json({"type": "ready", "controller_id": controller_id})
            while True:
                try:
                    payload = await websocket.receive_json()
                    command = _command_from_payload(payload)
                    execute_command(control, controller_id, command)
                    if command.name in {"FORWARD", "BACKWARD", "LEFT", "RIGHT"}:
                        await session.start()
                    await websocket.send_json(
                        {
                            "type": "ack",
                            "command": command.name.lower(),
                            "state": _session_state(session),
                        }
                    )
                except (ProtocolError, TypeError, ValueError) as error:
                    await websocket.send_json(
                        {"type": "error", "code": "invalid_command", "detail": str(error)}
                    )
        except (WebSocketDisconnect, RuntimeError):
            return
        finally:
            with suppress(ControllerAccessError):
                control.release_controller(controller_id)

    return app


def _session_state(session: SimulationSession) -> dict[str, Any]:
    state = session.engine.state()
    state["session_running"] = session.running
    state["events"] = session.engine.event_log()[-20:]
    return state


def _command_from_payload(payload: object) -> Command:
    if not isinstance(payload, dict):
        raise TypeError("control message must be an object")
    raw_name = payload.get("command")
    if not isinstance(raw_name, str):
        raise TypeError("command must be a string")
    name = raw_name.strip().upper()
    if name in {"FORWARD", "BACKWARD", "LEFT", "RIGHT"}:
        speed = payload.get("speed", 0.5)
        if isinstance(speed, bool) or not isinstance(speed, (int, float)):
            raise TypeError("speed must be a number")
        return parse_command(f"{name} {speed}")
    if name == "LOOK":
        pan = payload.get("pan")
        tilt = payload.get("tilt")
        if (
            isinstance(pan, bool)
            or not isinstance(pan, (int, float))
            or isinstance(tilt, bool)
            or not isinstance(tilt, (int, float))
        ):
            raise TypeError("look requires numeric pan and tilt")
        return parse_command(f"LOOK {pan} {tilt}")
    return parse_command(name)


def _default_engine() -> SimulationEngine:
    scenario = Scenario.from_mapping(
        {"schema_version": SCENARIO_SCHEMA, "id": "viewer-default-arena"}
    )
    return SimulationEngine(scenario)
