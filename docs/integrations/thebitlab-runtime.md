# Runtime TheBitLab `romeo-sim`

Romeo si registra nel gruppo entry point `thebitlab.runtimes` e implementa il
protocollo duck-typed `runtime_plugin.v1`. Non importa moduli interni di
TheBitLab.

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
  finale sotto il workspace.

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

`-I`, containment e subprocess limitano accoppiamento e failure, ma non sono una
sandbox di sistema: una submission Python rimane codice non fidato. In produzione
il processo runtime deve essere eseguito nel sandbox imposto dall'host TheBitLab
con limiti di filesystem, rete, memoria e CPU. Questa responsabilità non viene
nascosta dietro una falsa garanzia del plugin.

## Conformance verificata

Il 21 agosto 2026 discovery, inventory e probe sono stati provati contro
`TheBitPoets/2cornot2c` al commit
`5472eef86568a4e7ce59ad34ba937220df27efd7`. La suite mirata upstream ha prodotto
32 test passati. Il package usa Hatchling affinché un editable install esponga un
solo entry point, come richiesto dal registry.

