# Runtime TheBitLab `romeo-sim`

Romeo si registra nel gruppo entry point `thebitlab.runtimes` e implementa il
protocollo duck-typed `runtime_plugin.v1`. Non importa moduli interni di
TheBitLab.

Il contratto generico autorevole appartiene alla piattaforma TheBitLab:

- [runtime plugin contract](https://github.com/TheBitPoets/2cornot2c/blob/main/doc/architecture/runtime-plugin-contract.md);
- [sandbox per il grading](https://github.com/TheBitPoets/2cornot2c/blob/main/doc/ASSIGNMENT_SANDBOX.md).

Questa pagina documenta invece l'implementazione Romeo di quei contratti.

```toml
[project.entry-points."thebitlab.runtimes"]
romeo-sim = "romeo.integrations.thebitlab:create_plugin"
```

## Descriptor

Il runtime dichiara le capability:

- `interactive-launch`: avvia viewer e simulatore locale, restituendo endpoint e
  session id;
- `headless-run`: esegue la submission in un processo Python isolato;
- `deterministic-grade`: sostituisce `time.sleep` nel worker con avanzamento del
  clock simulato;
- `artifact-collect`: salva manifest, risultato, traiettoria, eventi e stato
  finale sotto il workspace;
- `sandbox-plan.v1`: delega l'esecuzione non fidata al broker ufficiale
  TheBitLab tramite `prepare_sandbox()` e `finalize_sandbox()`.

`probe()` resta disponibile per il percorso headless anche se l'extra `web` non è
installato; `metadata.interactive_available` segnala separatamente il viewer.

## Config activity

Il file indicato da `extensions.thebitlab.runtime.config` usa:

```json
{
  "schema_version": "romeo.thebitlab.v1",
  "scenario": "scenario.json",
  "submission_artifact_id": "main",
  "max_simulation_seconds": 60
}
```

Scenario e submission sono risolti con containment check. La submission è
limitata a 1 MB; timeout wall-clock e limite di tempo simulato sono indipendenti.

I laboratori possono dichiarare `stdout_checks`, una lista di controlli
con `name`, `contains` e `points`. Il runtime li combina con i check spaziali:
sono utili per verificare marcatori emessi dopo una risposta socket, JSON o HTTP.
Non sostituiscono il sandbox né test comportamentali. Y2 usa invece
`behavioral_tests` con path ed entrypoint nominati.

## Esecuzione

Il worker viene avviato con `python -I`, collega un singolo
`SimulationEngine` sia a `romeo.easy` sia ai normali `Robot()`, intercetta
`time.sleep`, acquisisce stdout/stderr e restituisce un risultato versionato. Un
ciclo che non usa `sleep` viene terminato dal timeout del processo; sleep eccessivi
falliscono sul limite simulato.

Gli output sono riportati in `runtime_execution.v1.metadata.artifacts`, perché la
v1 TheBitLab non definisce ancora un campo o collector standard per artifact
prodotti dal runtime. Non viene aggiunto alcun campo top-level fuori ABI.

## Sicurezza

`run()` con `-I`, containment e subprocess non è una sandbox e restituisce
`authoritative=false`. Il percorso autorevole richiede il broker TheBitLab e
un'immagine configurata per digest. Nel caso geometrico la submission produce
una trace e scenario/grader restano sull'host; nel caso Y2 il container esegue
la fixture e il finalizzatore ricostruisce il risultato autorevole lato trusted.

Nel normale percorso studente un runtime sandbox-capable viene promosso dal
requested backend storico `local` al backend effettivo `docker`; un errore del
boundary non deve provocare fallback automatico al percorso process-only.

## Conformance e release corrente

La conformance non è attestata da una frase mantenuta a mano. Il file generato
[`docs/release/runtime-image-current.env`](../release/runtime-image-current.env)
registra la combinazione effettivamente verificata di:

- SHA sorgente Romeo;
- digest OCI immutabile;
- workflow run di pubblicazione;
- SHA del broker TheBitLab.

Quel record viene aggiornato solo dopo build/push dell'immagine, smoke del suo
ENTRYPOINT e smoke attraverso il broker TheBitLab. Per installazione o audit usa
sempre il record corrente invece di copiare un digest da una guida narrativa.
