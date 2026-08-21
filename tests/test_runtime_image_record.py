import re
from pathlib import Path

import pytest

from romeo.integrations.thebitlab.runtime_record import (
    RuntimeImageRecordError,
    load_runtime_image_record,
    validate_digest_pinned_image,
)

IMAGE = "ghcr.io/thebitpoets/romeo-runtime@sha256:" + "a" * 64
SOURCE_SHA = "b" * 40
BROKER_SHA = "c" * 40


def write_record(path: Path, *, image: str = IMAGE) -> None:
    path.write_text(
        "\n".join(
            (
                "# generated",
                f"ROMEO_SANDBOX_IMAGE={image}",
                f"ROMEO_RUNTIME_SOURCE_SHA={SOURCE_SHA}",
                "ROMEO_RUNTIME_WORKFLOW_RUN=123",
                f"ROMEO_THEBITLAB_BROKER_SHA={BROKER_SHA}",
            )
        ),
        encoding="utf-8",
    )


def test_valid_runtime_record_binds_image_source_and_broker(tmp_path: Path) -> None:
    path = tmp_path / "runtime-image-current.env"
    write_record(path)

    record = load_runtime_image_record(path)

    assert record.sandbox_image == IMAGE
    assert record.runtime_source_sha == SOURCE_SHA
    assert record.thebitlab_broker_sha == BROKER_SHA


def test_missing_runtime_record_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeImageRecordError, match="unavailable"):
        load_runtime_image_record(tmp_path / "missing.env")


@pytest.mark.parametrize(
    "image",
    [
        "ghcr.io/thebitpoets/romeo-runtime:latest",
        "ghcr.io/thebitpoets/romeo-runtime@sha256:not-a-digest",
        "ghcr.io/thebitpoets/romeo-runtime@sha512:" + "a" * 128,
    ],
    ids=["mobile-tag", "invalid-sha256", "not-sha256"],
)
def test_runtime_record_rejects_non_digest_pinned_images(
    tmp_path: Path, image: str
) -> None:
    path = tmp_path / "runtime-image-current.env"
    write_record(path, image=image)

    with pytest.raises(RuntimeImageRecordError, match="sha256"):
        load_runtime_image_record(path)


def test_image_override_validator_rejects_mobile_tag() -> None:
    with pytest.raises(RuntimeImageRecordError, match="sha256"):
        validate_digest_pinned_image("ghcr.io/thebitpoets/romeo-runtime:latest")


def test_operational_smoke_and_deployment_guide_do_not_embed_a_digest() -> None:
    smoke = Path("scripts/smoke_thebitlab_fail_closed.py").read_text(encoding="utf-8")
    guide = Path("docs/integrations/thebitlab-deployment.md").read_text(encoding="utf-8")
    embedded_digest = re.compile(r"ghcr\.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}")

    assert embedded_digest.search(smoke) is None
    assert embedded_digest.search(guide) is None
