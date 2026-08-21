# Installare Romeo come plugin TheBitLab

## Modello di deployment

Il package `thebitlab-romeo` registra l'entry point `romeo-sim`. Deve essere installato **nello stesso ambiente Python del processo TheBitLab che scopre/esegue i runtime**.

La sandbox autorevole usa invece l'immagine OCI pubblicata separatamente. Package Python e immagine Docker sono due artefatti diversi e devono essere verificati entrambi.

## 1. Virtual environment gestito

Esempio Linux:

```console
python3 -m venv /opt/thebitlab/venv
source /opt/thebitlab/venv/bin/activate
python -m pip install --upgrade pip
```

In sviluppo si può installare Romeo da checkout:

```console
python -m pip install --no-deps --no-build-isolation /path/to/romeo
```

In produzione è preferibile installare un artefatto/versione revisionata e riproducibile anziché un checkout modificabile.

## 2. Configurare il digest approvato

Il riferimento corrente viene scritto automaticamente in:

```text
docs/release/runtime-image-current.env
```

Copiare **esattamente** il valore `ROMEO_SANDBOX_IMAGE=ghcr.io/...@sha256:...` nell'ambiente del servizio TheBitLab. Non usare `latest` o altri tag mobili.

Se TheBitLab è avviato da systemd/container/servizio, rendere la variabile persistente nella configurazione di quel servizio e riavviare il processo.

## 3. Verificare la discovery

Dal repository TheBitLab, usando lo stesso interprete/virtual environment del servizio:

```console
python scripts/thebitlab_runtime_cli.py list --json
python scripts/thebitlab_runtime_cli.py probe romeo-sim --json
```

Il runtime deve risultare installato e disponibile. Il probe Romeo deve inoltre confermare che la configurazione per il broker sandbox è presente.

## 4. Verificare il percorso studente reale

Non basta chiamare direttamente il worker Docker. La verifica deve attraversare il normale dispatcher studente TheBitLab e dimostrare che una richiesta storicamente `local` viene promossa al backend effettivo Docker per un runtime che supporta `sandbox-plan.v1`.

Eseguire almeno:

- una Activity con command trace e finalizzazione trusted;
- una Activity con behavioral test;
- un caso con Docker/digest assente per confermare il fail-closed.

## 5. Evidenza da conservare

Registrare:

- SHA/versione TheBitLab;
- SHA/versione package Romeo;
- digest `ROMEO_SANDBOX_IMAGE`;
- versione Docker/host;
- output `probe`;
- Activity usate nello smoke;
- esito e data;
- eventuale configurazione del servizio, senza segreti.

Vedi anche [Runtime image deployment gate](../release/runtime-image.md).
