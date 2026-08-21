"""Non-sensitive identity binding for one physical Raspberry Pi unit."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Sequence
from pathlib import Path

FINGERPRINT_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")
_DEVICE_TREE_SERIAL_PATHS = (
    Path("/sys/firmware/devicetree/base/serial-number"),
    Path("/proc/device-tree/serial-number"),
)
_CPUINFO_SERIAL_PATTERN = re.compile(r"^Serial\s*:\s*(\S+)\s*$", re.IGNORECASE)
_FINGERPRINT_DOMAIN = b"romeo-unit-identity-v1\0"

UnitIdentifierProvider = Callable[[], str]


class UnitIdentityError(RuntimeError):
    """Raised when a stable physical-unit identity cannot be obtained safely."""


def read_raspberry_unit_identifier(
    *,
    device_tree_paths: Sequence[Path] = _DEVICE_TREE_SERIAL_PATHS,
    cpuinfo_path: Path = Path("/proc/cpuinfo"),
) -> str:
    """Read a stable Raspberry identifier without returning it to diagnostics.

    Device-tree serial is authoritative. ``/proc/cpuinfo`` is retained only as
    the Raspberry-compatible fallback used by older kernels.
    """

    for path in device_tree_paths:
        try:
            raw = path.read_bytes().rstrip(b"\x00\r\n\t ")
        except (FileNotFoundError, PermissionError, OSError):
            continue
        if raw:
            try:
                return raw.decode("ascii")
            except UnicodeDecodeError as error:
                raise UnitIdentityError("Raspberry unit identifier is not ASCII") from error

    try:
        cpuinfo = cpuinfo_path.read_text(encoding="ascii", errors="strict")
    except (FileNotFoundError, PermissionError, OSError, UnicodeError) as error:
        raise UnitIdentityError("Raspberry unit identifier is unavailable") from error
    if "Raspberry Pi" not in cpuinfo:
        raise UnitIdentityError("Raspberry unit identifier is unavailable")
    for line in cpuinfo.splitlines():
        match = _CPUINFO_SERIAL_PATTERN.fullmatch(line)
        if match:
            return match.group(1)
    raise UnitIdentityError("Raspberry unit identifier is unavailable")


def fingerprint_unit_identifier(identifier: str) -> str:
    """Hash one raw identifier with a domain separator; never persist the input."""

    if not isinstance(identifier, str) or not identifier.strip():
        raise UnitIdentityError("Raspberry unit identifier is unavailable")
    normalized = identifier.strip().encode("utf-8")
    return "sha256:" + hashlib.sha256(_FINGERPRINT_DOMAIN + normalized).hexdigest()


def is_unit_fingerprint(value: object) -> bool:
    """Return whether a value is a canonical non-sensitive unit fingerprint."""

    return isinstance(value, str) and FINGERPRINT_PATTERN.fullmatch(value) is not None
