# Verificare l'installazione Romeo

Dopo l'installazione non fermarti a `pip show`: verifica discovery, sandbox e normale percorso studente.

## 1. Discovery

Dallo stesso ambiente Python di TheBitLab:

```console
python scripts/thebitlab_runtime_cli.py list --json
python scripts/thebitlab_runtime_cli.py probe romeo-sim --json
```

Controlla runtime id, versione plugin, capability e disponibilità. Un runtime sandbox-capable deve dichiarare `sandbox-plan.v1`.

## 2. Digest

Verifica che il processo reale riceva un riferimento del tipo:

```text
ROMEO_SANDBOX_IMAGE=ghcr.io/thebitpoets/romeo-runtime@sha256:<digest>
```

Non considerare valido un tag senza digest.

## 3. Percorso studente

La prova significativa parte dal dispatcher usato dalla TUI/servizio studente, non dal worker invocato direttamente.

Per un'Activity Romeo sandbox-capable devono risultare:

- requested backend storico/default: `local`;
- backend effettivo: `docker`;
- `authoritative=true`;
- isolamento Docker dichiarato nei metadata attesi.

Esegui almeno una missione Y1 command-trace e una Y2 behavioral.

## 4. Fail-closed

In una finestra controllata verifica che digest mancante/non valido o sandbox indisponibile non producano fallback a `plugin.run()` locale. Ripristina immediatamente la configurazione corretta.

## 5. Salva l'evidenza

Registra data, versioni, SHA, digest e Activity usate. Il report deve permettere a un altro amministratore di capire esattamente che cosa era in esecuzione senza accedere a segreti.
