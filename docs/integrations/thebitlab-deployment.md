# Installazione amministrativa Romeo in TheBitLab

Questa procedura non introduce un nuovo deployment system: usa wheel Python,
entry point standard e il meccanismo di servizio già scelto dall'installazione
TheBitLab reale.

## Ricognizione obbligatoria

Prima di installare registra, senza segreti: host/OS/CPU, utente del servizio,
SHA TheBitLab, interprete e venv effettivi, modalità di avvio, nodo del broker,
Docker/permessi, file persistente delle environment variable, aggiornamento e
rollback. Non assumere che una shell amministrativa sia l'ambiente del servizio.

## Artefatto certificato

Per la release runtime certificata:

```text
Romeo source SHA: b6bb70fef89fcf539fbf087cd26ca80f203fc7cb
package: thebitlab-romeo 0.1.0
image: ghcr.io/thebitpoets/romeo-runtime@sha256:3d854fb99d2d1f4b7264c87fcce550dd5e3e739de055c73325609893a088d997
TheBitLab broker SHA: ec60eaca11da481a8510ec67255abaf76ac5b23e
```

Costruisci da un worktree detached dello SHA, non da un checkout successivo:

```text
python -m venv .venv-build
.venv-build/bin/python -m pip install build
.venv-build/bin/python -m build --wheel
sha256sum dist/thebitlab_romeo-0.1.0-py3-none-any.whl
```

Conserva wheel, SHA-256, source SHA e digest OCI nello stesso registro di
rilascio. Non usare editable install fuori dallo sviluppo.

## Installazione e rollback

Usa esattamente il Python che avvia TheBitLab:

```text
/path/to/thebitlab-venv/bin/python -m pip install --no-deps \
  /path/to/thebitlab_romeo-0.1.0-py3-none-any.whl
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

Il valore deve contenere il digest completo sopra. Un semplice `export` o
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
