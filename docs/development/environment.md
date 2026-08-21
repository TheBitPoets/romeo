# Ambiente di sviluppo

## Virtual environment

Dalla root del repository:

```console
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```console
source .venv/bin/activate
```

Installazione completa per sviluppo, web simulator e documentazione:

```console
python -m pip install --upgrade pip
python -m pip install -e ".[dev,web,docs]"
```

Aggiungere `gamepad` o `hardware` solo quando servono davvero:

```console
python -m pip install -e ".[gamepad]"
python -m pip install -e ".[hardware]"
```

L'extra `hardware` va usato su un ambiente compatibile con CRICKIT/Raspberry Pi; non è necessario per simulatore e CI ordinaria.

## Loop di sviluppo

Prima di aprire una PR:

```console
python -m ruff check .
python -m mypy src
python scripts/validate_course.py
python -m pytest
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Per il simulatore web:

```console
python -m uvicorn romeo.web.app:create_app --factory --host 127.0.0.1 --port 8000
```

## Docker e runtime TheBitLab

Docker serve quando si modifica il percorso autorevole o il runtime runner. Il normale sviluppo delle API pure può essere fatto senza Docker, ma qualsiasi modifica a `prepare_sandbox`, worker, trace o finalizzazione deve passare anche gli smoke del runtime container.

Il confine da preservare è:

```text
trusted plugin -> untrusted Docker worker -> trusted finalize
```

Non introdurre fallback automatici dal grading sandbox al processo locale.
