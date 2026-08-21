# Threat model delle submission TheBitLab

Audit aggiornato il 21 agosto 2026 contro `2cornot2c` commit
`5472eef86568a4e7ce59ad34ba937220df27efd7` e l'estensione broker proposta nel
branch `feat/runtime-sandbox-broker`.

## Due percorsi, due garanzie

`run()` avvia `python -I` in subprocess con ambiente ridotto e timeout. È utile
per sviluppo locale, ma offre soltanto **process isolation**: il codice conserva
i permessi dell'utente host. Il risultato dichiara quindi
`authoritative=false`, `execution_isolation=process-only` e non va usato per
codice non affidabile.

Il percorso autorevole usa invece l'estensione ABI `sandbox-plan.v1`:

1. `prepare_sandbox()` dichiara immagine OCI per digest, submission e fixture
   docente strettamente necessarie;
2. il broker TheBitLab valida il piano e copia solo input confinati;
3. Docker impone rete `none`, filesystem root read-only, utente non root,
   capability drop, `no-new-privileges`, limiti PID/memoria/CPU/output e tmpfs;
4. `finalize_sandbox()` ricostruisce il risultato sul lato host trusted.

Scenario, rubrica e grader geometrico non entrano nel container. Per il
simulatore, il container produce soltanto una command trace che l'host valida e
riproduce su un engine nuovo. Per Y2, i test comportamentali sono activity input
docente e il finalizzatore confronta nomi e cardinalità con il manifest trusted.

## Minacce e controlli

| Minaccia | Percorso locale | Broker autorevole | Residuo |
| --- | --- | --- | --- |
| File host/altre submission | permessi host | mount temporaneo read-only con soli input dichiarati | sicurezza del daemon e del kernel host |
| Rete | disponibile | `--network none` | nessuna rete, incluso loopback tra processi esterni |
| Subprocess/PID | timeout processo padre | cgroup, PID limit e rimozione container | denial of service entro i limiti assegnati |
| Environment/segreti | allowlist ridotta | solo `TMPDIR`, nessun env scelto dal plugin | non inserire segreti nelle fixture |
| CPU/memoria/disco/output | timeout parziale | CPU, memoria, PID, tmpfs e output limitati | quote dipendono dalla configurazione Docker |
| Integrità grading simulatore | stesso host process | trace non privilegiata, replay e grading host | validare sempre schema e limiti della trace |
| Integrità test Y2 | non autorevole | runner trusted nel container e manifest host | la fixture è leggibile dalla submission e non è un segreto |

`python -I` non blocca file, rete, subprocess o risorse; resta una misura di
igiene degli import anche dentro il container, non il boundary di sicurezza.

## Fail closed e prerequisiti di deploy

Il plugin accetta solo `ROMEO_SANDBOX_IMAGE` nel formato
`repository@sha256:<digest>`. Senza digest, o senza capability broker, il grading
autorevole non parte. La pipeline immagine deve usare una base Python 3.12 slim
per digest, wheelhouse con hash, SBOM e scansione. I test nascosti non devono
contenere credenziali o expected outcome sensibili: sono nascosti prima del
tentativo, ma visibili al programma nello stesso container.
