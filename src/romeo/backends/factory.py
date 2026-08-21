"""Backend selection without leaking infrastructure into student programs."""

import os

from romeo.backends.base import Backend
from romeo.backends.mock import MockBackend


def create_backend(name: str | None = None) -> Backend:
    """Create a backend selected explicitly or through ``ROMEO_BACKEND``.

    ``mock`` is the safe default on development machines. The simulation backend is
    added by the simulator milestone and uses the same selection mechanism.
    """

    selected_name = name if name is not None else os.environ.get("ROMEO_BACKEND", "mock")
    backend_name = selected_name.strip().lower()
    if backend_name == "mock":
        return MockBackend()
    if backend_name == "crickit":
        from romeo.backends.crickit import CrickitBackend

        return CrickitBackend()
    raise ValueError(f"unknown Romeo backend: {backend_name!r}")
