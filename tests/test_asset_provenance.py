from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"


def _historical_image_names() -> set[str]:
    names = {"1_os_installation.png"}
    names.update(f"{index}_raspberry_pi_imager.png" for index in range(2, 17))
    names.update(f"{index}_romeo_installation.png" for index in range(17, 24))
    names.add("19_romeo_installation2.png")
    names.update(f"{index}_crickit_installation.png" for index in range(24, 29))
    names.update(f"{index}_build_robot.png" for index in range(29, 53))
    return names


def test_historical_assembly_images_are_preserved() -> None:
    expected = _historical_image_names()
    present = {path.name for path in IMAGES.glob("*.png")}

    assert len(expected) == 53
    assert expected <= present


def test_historical_assembly_guide_still_uses_repository_images() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "## Guida di assemblaggio storica" in readme
    assert "images/1_os_installation.png" in readme
    assert "images/52_build_robot.png" in readme


def test_image_rights_are_separate_from_course_license() -> None:
    license_notice = (IMAGES / "LICENSE.md").read_text(encoding="utf-8")
    provenance = (IMAGES / "PROVENANCE.md").read_text(encoding="utf-8")

    assert "non sono comprese" in license_notice
    assert "Apache-2.0" in license_notice
    assert "CC BY-SA 4.0" in license_notice
    assert "53 immagini PNG" in provenance
    assert "non deve essere rimossa" in provenance
