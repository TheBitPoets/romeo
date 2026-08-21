# Installazione amministrativa Romeo in TheBitLab

Questa procedura non introduce un nuovo deployment system: usa wheel Python,
entry point standard e il meccanismo di servizio già scelto dall'installazione
TheBitLab reale.

## Ricognizione obbligatoria

Prima di installare registra, senza segreti: host/OS/CPU, utente del servizio,
SHA TheBitLab, interprete e venv effettivi, modalità di avvio, nodo del broker,
Docker/permessi, file persistente delle environment variable, aggiornamento e
rollback. Non assumere che una shell amministrativa sia l'ambiente del servizio.

## Fonte autorevole della release installabile

Non copiare digest OCI, source SHA o versione package da una guida statica. Il
record autorevole è `docs/release/runtime-image-current.env` su `main`: viene
riscritto dalla pipeline `Publish runtime runner` **solo dopo** push su GHCR,
smoke diretto del digest e smoke end-to-end attraverso il broker TheBitLab.

Il record contiene:

```text
ROMEO_SANDBOX_IMAGE=ghcr.io/thebitpoets/romeo-runtime@sha256:<digest>
ROMEO_RUNTIME_SOURCE_SHA=<sha Romeo verificato>
ROMEO_RUNTIME_WORKFLOW_RUN=<run id>
ROMEO_THEBITLAB_BROKER_SHA=<sha broker verificato>
```

Prima di un nuovo deployment:

1. leggi quel file dalla `main` aggiornata;
2. verifica che il workflow indicato abbia conclusione `success`;
3. usa **esattamente** `ROMEO_SANDBOX_IMAGE`, senza sostituirlo con un tag mobile;
4. costruisci la wheel Romeo dal commit `ROMEO_RUNTIME_SOURCE_SHA` e registra
   versione, nome file e SHA-256 della wheel realmente installata;
5. usa il broker allo SHA `ROMEO_THEBITLAB_BROKER_SHA` o una revisione successiva
   che abbia superato nuovamente gli stessi gate.

Esempio di build da source SHA registrato:

```text
git worktree add --detach ../romeo-release <ROMEO_RUNTIME_SOURCE_SHA>
cd ../romeo-release
python -m venv .venv-build
.venv-build/bin/python -m pip install build
.venv-build/bin/python -m build --wheel
sha256sum dist/thebitlab_romeo-*.whl
```

Conserva wheel, SHA-256, source SHA, digest OCI e workflow run nello stesso
registro di rilascio. Non usare editable install fuori dallo sviluppo.

`docs/hardware/physical-validation-2026-08-21.md` conserva prove storiche su
artefatti precedenti e sul candidato Romeo Doctor. È evidenza di collaudo, non
una fonte da cui copiare i valori per un deployment futuro.

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

Configura `ROMEO_SANDBOX_IMAGE` nel vero ambiente del processo con il valore del
record autorevole. Esempi, da adattare alla topologia osservata:

- systemd: `EnvironmentFile=` posseduto da root e `systemctl daemon-reload`;
- container: environment del manifest/Compose e ricreazione del solo servizio;
- servizio Windows: environment del service wrapper, non della shell corrente;
- launcher shell: file environment letto dal launcher amministrativo.

Un semplice `export` o `$env:` in una console di collaudo non configura un
servizio separato.

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
