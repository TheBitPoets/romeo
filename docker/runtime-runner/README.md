# Romeo runtime runner image

Questa immagine contiene soltanto API Romeo e `TraceBackend`: scenario, grader,
rubrica e artifact output restano sull'host trusted. La build richiede
esplicitamente `PYTHON_BASE_IMAGE` con digest OCI di una Python 3.12 slim
basata su Debian; non esiste un default mobile. Anche le dipendenze usate dai
test comportamentali sono bloccate in `requirements.lock`.

```text
docker build --build-arg PYTHON_BASE_IMAGE=<repository>@sha256:<digest> ...
```

Dopo pubblicazione, l'amministratore configura
`ROMEO_SANDBOX_IMAGE=<repository>@sha256:<digest>`. Tag senza digest vengono
rifiutati. TheBitLab impone rete disabilitata, root filesystem read-only,
utente non privilegiato, capability drop e limiti PID/CPU/memoria; il Dockerfile
non può modificare tali opzioni.

La pipeline di pubblicazione deve installare il lock da una wheelhouse interna
con hash verificati e registrare SBOM e digest finale. Fino alla pubblicazione
del digest, il probe segnala `sandbox_broker_available=false` e il percorso
autorevole fallisce chiuso.
