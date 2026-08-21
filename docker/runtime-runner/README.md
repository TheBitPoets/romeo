# Romeo runtime runner image

Questa immagine contiene soltanto API Romeo e `TraceBackend`: scenario, grader,
rubrica e artifact output restano sull'host trusted. La build richiede
esplicitamente `PYTHON_BASE_IMAGE` con digest OCI di una Python 3.12 slim
basata su Debian; non esiste un default mobile. Anche le dipendenze usate dai
test comportamentali sono bloccate e verificate con `pip --require-hashes` in
`requirements.lock`.

## Wheelhouse verificata

La build non scarica pacchetti Python dalla rete. Prima di invocare Docker, CI e
release materializzano una wheelhouse a partire dal lock hashato:

```text
rm -rf docker/runtime-runner/wheelhouse
mkdir -p docker/runtime-runner/wheelhouse
python -m pip download \
  --require-hashes \
  --only-binary=:all: \
  --dest docker/runtime-runner/wheelhouse \
  -r docker/runtime-runner/requirements.lock
```

Il Dockerfile installa poi esclusivamente da quella directory con `--no-index`.
La wheelhouse è un artefatto effimero e non viene versionata nel repository.

## Build locale

Dopo avere preparato la wheelhouse:

```text
docker build \
  --build-arg PYTHON_BASE_IMAGE=<repository>@sha256:<digest> \
  --tag romeo-runtime-runner:local \
  --file docker/runtime-runner/Dockerfile \
  .
```

La CI usa una base Python 3.12.11 slim-bookworm fissata al digest dell'indice
OCI.

## Pubblicazione

`.github/workflows/runtime-image.yml` pubblica il runner su:

```text
ghcr.io/thebitpoets/romeo-runtime
```

La pipeline:

1. ricostruisce la wheelhouse dal lock hashato;
2. costruisce soltanto `linux/amd64` da una base pin-nata per digest;
3. pubblica l'immagine su GHCR;
4. registra provenance e SBOM OCI tramite Buildx;
5. legge il digest della manifest effettivamente pubblicata;
6. esegue gli smoke `command-trace` e `behavioral-tests` usando direttamente
   `<repository>@sha256:<digest>`;
7. salva `runtime-image.env` e i metadata Buildx come artifact del workflow.

Il riferimento operativo risultante ha quindi sempre la forma:

```text
ROMEO_SANDBOX_IMAGE=ghcr.io/thebitpoets/romeo-runtime@sha256:<digest>
```

Un tag può essere usato come indice umano nel registry, ma non è mai accettato
come configurazione autorevole. `RomeoRuntimePlugin` rifiuta immagini prive di
digest.

## Boundary TheBitLab

Dopo pubblicazione, l'amministratore configura
`ROMEO_SANDBOX_IMAGE=<repository>@sha256:<digest>`. TheBitLab impone rete
disabilitata, root filesystem read-only, utente non privilegiato, capability
drop e limiti PID/CPU/memoria; il Dockerfile non può modificare tali opzioni.

Fino alla pubblicazione/configurazione del digest, il probe segnala
`sandbox_broker_available=false` e il percorso autorevole fallisce chiuso.
