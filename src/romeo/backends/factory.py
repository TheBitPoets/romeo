"""Backend selection without leaking infrastructure into student programs."""

import os

from romeo.backends.base import Backend
from romeo.backends.mock import MockBackend
from romeo.safety import SafetyBackend


def create_backend(name: str | None = None, *, safety: bool = True) -> Backend:
    """Create a backend selected explicitly or through ``ROMEO_BACKEND``.

    ``mock`` is the safe default on development machines. The simulation backend is
    added by the simulator milestone and uses the same selection mechanism.
    """

    selected_name = name if name is not None else os.environ.get("ROMEO_BACKEND", "mock")
    backend_name = selected_name.strip().lower()
    if backend_name == "mock":
        backend: Backend = MockBackend()
    elif backend_name == "crickit":
        from romeo.backends.crickit import CrickitBackend

        backend = CrickitBackend()
    else:
        raise ValueError(f"unknown Romeo backend: {backend_name!r}")
    if not safety:
        return backend
    max_speed = float(os.environ.get("ROMEO_MAX_SPEED", "0.7"))
    command_timeout = float(os.environ.get("ROMEO_COMMAND_TIMEOUT", "1.0"))
    return SafetyBackend(backend, max_speed=max_speed, command_timeout=command_timeout)
