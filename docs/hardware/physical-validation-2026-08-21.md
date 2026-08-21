# Validazione operativa Romeo — 2026-08-21

Stato: **parziale; software certificato verificato, robot fisico non raggiungibile**.
Nessuna voce hardware è considerata completata senza osservazione diretta.

## Ambiente osservato

- Host: `LAPTOP-NMCGI8PV`.
- OS: Microsoft Windows 10.0.26200, x64.
- Utente di collaudo: account Windows interattivo; nessun servizio TheBitLab
  reale identificato.
- Python host: 3.10.7 predefinito; Python 3.12.10 usato per build e venv test.
- TheBitLab test venv:
  `F:\dev\romeo\.worktrees\2cornot2c-ec60\.venv`, Python 3.12.
- TheBitLab SHA testato: `ec60eaca11da481a8510ec67255abaf76ac5b23e`.
- Romeo source SHA della wheel: `b6bb70fef89fcf539fbf087cd26ca80f203fc7cb`.
- Package: `thebitlab-romeo 0.1.0`.
- Wheel SHA-256:
  `511c63f3538d7df05ecd15e8ef19d74bb3af124e87453f5d2371b8d80c950356`.
- Docker client/server: 28.3.2; Docker Desktop 4.44.0; daemon Linux amd64.
- OCI runtime:
  `ghcr.io/thebitpoets/romeo-runtime@sha256:3d854fb99d2d1f4b7264c87fcce550dd5e3e739de055c73325609893a088d997`.

Il checkout classroom moderno presente sull'host è incompleto: non esistono una
box Vagrant `2cornot2c/*` né `.classroom-box`. Una VM Vagrant legacy registrata
era spenta, usa un fork 2024 privo del runtime broker ed è stata esclusa. Non è
stata inventata una topologia UI/grading/broker e non è stata modificata la VM.

## Package e probe plugin

La wheel è stata costruita da un worktree detached dello SHA certificato,
installata con `--no-index` e `--no-deps` nella stessa venv usata per i probe.
Entry point osservato:

```text
thebitlab.runtimes / romeo-sim = romeo.integrations.thebitlab:create_plugin
```

`list --json` e `probe romeo-sim --json` hanno restituito: installed/available
true, runtime id `romeo-sim`, plugin/runtime 0.1.0, API `runtime_plugin.v1`,
capability `sandbox-plan.v1`, `sandbox_broker_available=true`.

La variabile OCI è stata impostata soltanto nel processo di collaudo. Non è
registrata come persistente perché non esiste un vero servizio TheBitLab
identificato su questo host.

## Authoritative end-to-end

Percorso esercitato: assignment → `student_runtime` → plugin trusted →
`prepare_sandbox` → Docker broker → worker OCI → finalize trusted → report.
Il backend non è stato forzato.

| Activity | Assignment | Esito | Score | Summary | Requested | Effective | Authoritative | Isolation |
|---|---|---:|---:|---|---|---|---:|---|
| `romeo-y1-u08-avanti-indietro` | `runtime-smoke-y1-u08-avanti-indietro` | pass | 10.0 | 2/2 | local | docker | true | docker |
| `romeo-y2-u07-json` | `runtime-smoke-y2-u07-json` | pass | 10.0 | 2/2 | local | docker | true | docker |

Entrambe hanno riportato runtime id `romeo-sim`, plugin 0.1.0 e hanno usato il
digest OCI immutabile indicato sopra. Y1 ha prodotto result, trajectory, events,
final-state e manifest; Y2 ha eseguito i behavioral tests e prodotto result.

## Fail-closed

Tre processi isolati hanno provato:

- `ROMEO_SANDBOX_IMAGE` assente;
- valore mobile/invalido `romeo-runtime:latest`;
- digest corretto con `DOCKER_HOST=tcp://127.0.0.1:1` solo nel processo.

Tutti hanno restituito `passed=false`, `status=runtime-unavailable`, nessun
grading autorevole. `RomeoRuntimePlugin.run()` è stato instrumentato: chiamate
osservate come fallback process-only = **0**. La configurazione corretta del
daemon non è stata modificata.

## Hardware identificato

Non verificato. Nel workspace non sono presenti hostname/IP/inventory del
Raspberry, sessione SSH, modello/revisione, OS/kernel, CRICKIT, firmware,
motori, servo, camera o dati di alimentazione dell'esemplare.

## Motori, polarità e safety

Non verificati fisicamente: motore sinistro/destro, forward/backward/left/right,
rumore, vibrazioni, STOP, eccezione, shutdown, perdita controller/TCP/WebSocket.
Le primitive software e Doctor sono coperte con fake, ma non sostituiscono
l'osservazione del robot.

## Watchdog

Non misurato fisicamente. Nessun minimo/massimo/media è disponibile.

## Servo

Pan, tilt, centro e limiti conservativi non verificati sull'esemplare.

## Camera

Picamera2, foto, endpoint, streaming, pan/tilt e riapertura non verificati sul
Raspberry.

## Alimentazione

Motori/camera/servo combinati, undervoltage, brownout, reset, I2C e CRICKIT non
verificati fisicamente.

## Calibrazione e simulatore → robot

Nessuna calibrazione del singolo esemplare e nessuna missione identica
simulatore→robot sono state eseguite. Il simulatore Y1 ha prodotto command trace,
trajectory e stato finale, ma manca il confronto fisico.

## Romeo Doctor

Implementato su branch `feat/romeo-doctor`: preflight passivo, commissioning
supervisionato, schema `romeo.hardware_calibration.v1`, report
`romeo.hardware_diagnostic.v1`, output didattico/JSON, exit code, persistenza
atomica, invalidazione su version mismatch e uso della calibrazione nel backend
CRICKIT. La release proposta è 0.2.0 e mantiene runtime ABI v1; non sostituisce
la wheel certificata 0.1.0 usata nelle prove sopra. I test fake coprono stop su
eccezione, timeout, Ctrl-C ed errore camera, misura watchdog ripetuta e ritorno
servo al centro sicuro.
Il test fisico è separato con marker `hardware` e opt-in esplicito.

La wheel candidata `thebitlab-romeo 0.2.0` è stata inoltre installata nella
stessa venv TheBitLab. Hash SHA-256 dell'artefatto di verifica:
`f9325a2699defcdfcf3cd604f24ac99f1778e4020717ea7842ddc994f8d4c873`.
Il probe ha osservato plugin/runtime `0.2.0`, capability `sandbox-plan.v1` e
broker disponibile. Le due Activity Y1/Y2 sono state ripetute con esito positivo
sullo stesso digest OCI e sullo stesso broker SHA, mantenendo requested `local`,
effective `docker`, `authoritative=true` ed execution isolation `docker`.

Gate automatici sul candidato: **402 passed, 3 skipped**; gli skip sono la
camera Raspberry, il preflight hardware opt-in e un test symlink non disponibile
su Windows. Ruff, mypy e `git diff --check` sono verdi. Il comando installato
`romeo-doctor --json` ha restituito schema v1, `ready=false` ed exit code 1
sull'host senza robot/calibrazione, quindi non ha prodotto un falso positivo.

## Problemi, limiti e follow-up

1. Identificare il vero nodo classroom e il suo service manager; installare lì
   la wheel e rendere persistente il digest prima di dichiarare il deployment.
2. Ottenere accesso al Raspberry e presenza umana; eseguire integralmente safety
   e checklist con ruote sollevate.
3. Misurare watchdog più volte e registrare minimo/massimo/media.
4. Verificare camera, power matrix, brownout, calibrazione e missione sim→real.
5. Il WebSocket corrente è simulator-only: una futura integrazione hardware
   richiede valutazione separata, senza modificare ora l'ABI TheBitLab.
6. Issue #6 resta aperta e nessuna casella hardware va spuntata in questa fase.
