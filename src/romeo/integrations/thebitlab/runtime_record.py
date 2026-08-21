"""Parse the generated record that binds source, broker, and immutable OCI image."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_IMAGE_PATTERN = re.compile(
    r"ghcr\.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}\Z"
)
_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}\Z")


class RuntimeImageRecordError(ValueError):
    """Raised when the generated runtime-image record is absent or invalid."""


@dataclass(frozen=True, slots=True)
class RuntimeImageRecord:
    sandbox_image: str
    runtime_source_sha: str
    thebitlab_broker_sha: str


def validate_digest_pinned_image(image: str) -> str:
    """Require an immutable lower-case GHCR reference pinned by sha256 digest."""

    if not isinstance(image, str) or _IMAGE_PATTERN.fullmatch(image) is None:
        raise RuntimeImageRecordError(
            "runtime image must match ghcr.io/...@sha256:<64 lowercase hex>"
        )
    return image


def load_runtime_image_record(path: str | Path) -> RuntimeImageRecord:
    """Load the three authoritative values from ``runtime-image-current.env``."""

    record_path = Path(path)
    try:
        lines = record_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise RuntimeImageRecordError(f"runtime image record unavailable: {record_path}") from error

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise RuntimeImageRecordError(f"invalid record line {line_number}")
        name, value = line.split("=", 1)
        if not name or not value or name in values:
            raise RuntimeImageRecordError(f"invalid record line {line_number}")
        values[name] = value

    required = {
        "ROMEO_SANDBOX_IMAGE",
        "ROMEO_RUNTIME_SOURCE_SHA",
        "ROMEO_THEBITLAB_BROKER_SHA",
    }
    missing = required - values.keys()
    if missing:
        raise RuntimeImageRecordError(
            "runtime image record missing: " + ", ".join(sorted(missing))
        )
    source_sha = values["ROMEO_RUNTIME_SOURCE_SHA"]
    broker_sha = values["ROMEO_THEBITLAB_BROKER_SHA"]
    if _COMMIT_PATTERN.fullmatch(source_sha) is None:
        raise RuntimeImageRecordError("ROMEO_RUNTIME_SOURCE_SHA must be a 40-hex commit")
    if _COMMIT_PATTERN.fullmatch(broker_sha) is None:
        raise RuntimeImageRecordError("ROMEO_THEBITLAB_BROKER_SHA must be a 40-hex commit")
    return RuntimeImageRecord(
        sandbox_image=validate_digest_pinned_image(values["ROMEO_SANDBOX_IMAGE"]),
        runtime_source_sha=source_sha,
        thebitlab_broker_sha=broker_sha,
    )
