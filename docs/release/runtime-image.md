# Runtime image deployment gate

Il grading autorevole di Romeo è abilitabile soltanto dopo la pubblicazione del
runner OCI e la configurazione del suo riferimento immutabile.

## Gate di pubblicazione

La pipeline `.github/workflows/runtime-image.yml` deve completare con successo:

- wheelhouse ricostruita da `requirements.lock` con verifica SHA-256;
- build `linux/amd64` da base Python pin-nata per digest;
- push su `ghcr.io/thebitpoets/romeo-runtime`;
- provenance e SBOM OCI;
- estrazione del digest della manifest pubblicata;
- smoke `command-trace` sul digest;
- smoke `behavioral-tests` sul digest.

L'artifact `runtime-image.env` contiene il valore da distribuire:

```text
ROMEO_SANDBOX_IMAGE=ghcr.io/thebitpoets/romeo-runtime@sha256:<digest>
```

## Gate di attivazione TheBitLab

Prima di abilitare il backend Docker per gli studenti:

1. installare il package Romeo compatibile con il runtime `romeo-sim`;
2. configurare `ROMEO_SANDBOX_IMAGE` con il riferimento esatto prodotto dal
   workflow, mai con un tag mobile;
3. verificare che `probe()` riporti `sandbox_broker_available=true`;
4. eseguire una Activity geometrica attraverso il broker e verificare la
   finalizzazione trusted della command trace;
5. eseguire una Activity di secondo anno con behavioral test;
6. verificare nel report `authoritative=true` e isolamento `docker` /
   `thebitlab-sandbox` secondo il livello che produce il report.

La mancata configurazione del digest deve lasciare il percorso autorevole in
fail-closed. Il percorso locale `run()` resta utile per sviluppo ma non deve
essere presentato come grading sicuro di codice non fidato.

## Gate indipendenti

La pubblicazione dell'immagine non sostituisce:

- il collaudo del robot fisico in `docs/hardware/pre-merge-checklist.md`;
- la chiusura dell'issue #1 relativa alla provenienza/licenza delle immagini
  prima della loro distribuzione.
