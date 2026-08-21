# Installazione amministrativa Romeo in TheBitLab

Questa procedura non introduce un nuovo deployment system: usa wheel Python,
entry point standard e il meccanismo di servizio già scelto dall'installazione
TheBitLab reale.

## Ricognizione obbligatoria

Prima di installare registra, senza segreti: host/OS/CPU, utente del servizio,
SHA TheBitLab, interprete e venv effettivi, modalità di avvio, nodo del broker,
Docker/permessi, file persistente delle environment variable, aggiornamento e
rollback. Non assumere che una shell amministrativa sia l'ambiente del servizio.

## Record autorevole della release

Non copiare un digest da questa guida. Leggi sempre
[`docs/release/runtime-image-current.env`](../release/runtime-image-current.env),
record generato dopo publish GHCR, smoke diretto e smoke attraverso il broker.
Contiene insieme:

- `ROMEO_SANDBOX_IMAGE`, riferimento GHCR immutabile `@sha256:`;
- `ROMEO_RUNTIME_SOURCE_SHA`, sorgente del worker pubblicato;
- `ROMEO_THEBITLAB_BROKER_SHA`, broker usato per la certificazione.

Prima dell'installazione verifica che il riferimento corrisponda esattamente a
`ghcr.io/...@sha256:<64 cifre esadecimali>`. Tag come `latest` non sono validi.

Costruisci da un worktree detached dello SHA letto dal record, non da un
checkout successivo:

```text
python -m venv .venv-build
.venv-build/bin/python -m pip install build
.venv-build/bin/python -m build --wheel
sha256sum dist/thebitlab_romeo-*.whl
```

Conserva wheel, SHA-256, source SHA e digest OCI nello stesso registro di
rilascio. Non usare editable install fuori dallo sviluppo.

## Installazione e rollback

Usa esattamente il Python che avvia TheBitLab:

```text
/path/to/thebitlab-venv/bin/python -m pip install --no-deps \
  /path/to/thebitlab_romeo-<version>-py3-none-any.whl
```

Per aggiornare, conserva prima la wheel precedente e il suo hash. Per rollback,
reinstalla esplicitamente quella wheel con `--force-reinstall --no-deps`,
ripristina il precedente digest immutabile e riavvia soltanto il componente che
scopre i runtime.

## Environment persistente

Configura `ROMEO_SANDBOX_IMAGE` nel vero ambiente del processo. Esempi, da
adattare alla topologia osservata:

- systemd: `EnvironmentFile=` posseduto da root e `systemctl daemon-reload`;
- container: environment del manifest/Compose e ricreazione del solo servizio;
- servizio Windows: environment del service wrapper, non della shell corrente;
- launcher shell: file environment letto dal launcher amministrativo.

Il valore deve essere copiato dal record autorevole. Un semplice `export` o
`$env:` in una console di collaudo non configura un servizio separato.

## Probe e percorso studente

Dal medesimo Python e dal root TheBitLab:

```text
python scripts/thebitlab_runtime_cli.py list --json
python scripts/thebitlab_runtime_cli.py probe romeo-sim --json
```

Il probe diretto descrive il fallback interno del plugin come `process-only` e
`untrusted_submissions_supported=false`: è intenzionale. L'autorità si dimostra
solo attraverso il normale `student_runtime`, dove una richiesta storica
`local` per la capability `sandbox-plan.v1` deve diventare `docker`, con
`authoritative=true` e `execution_isolation=docker`.

Usa `scripts/smoke_thebitlab_published_runtime.py` per Y1/Y2 e
`scripts/smoke_thebitlab_fail_closed.py` per immagine assente, invalida e broker
irraggiungibile. Il secondo instrumenta `plugin.run()` e fallisce se viene usato
come fallback.
