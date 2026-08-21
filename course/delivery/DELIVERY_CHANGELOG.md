# Romeo — Delivery Change Log

Questo file traccia le revisioni di **delivery** del corso: slide, navigazione, spiegazioni, setup, troubleshooting e fix operativi che non cambiano automaticamente il contratto delle 43 unità o il comportamento del runtime/hardware.

## Tipi

- `errata` — correzione senza cambio di obiettivo;
- `clarification` — spiegazione/esempio equivalente;
- `slides` — modifica ai deck docente;
- `lab-fix` — correzione operativa che preserva l'Activity contract;
- `setup` — installazione/esecuzione/troubleshooting;
- `hardware-doc` — chiarimento operativo/safety senza cambio di hardware behavior;
- `curriculum-change` — modifica alle unità/obiettivi/grading da sottoporre a review;
- `runtime-change` — modifica al comportamento software o hardware, fuori dal solo delivery layer.

## Registro

| Data | Area | Tipo | Modifica | Motivo | Contratto curricolare/runtime invariato? |
|---|---|---|---|---|---|
| 2026-08-21 | delivery layer | clarification | Aggiunti dashboard e indice slide sopra Course Bundle e portale Sphinx esistenti | Rendere navigabile il percorso senza duplicare i 43 contenuti | Sì |

## Regola per il robot reale

Un cambiamento a `commissioning`, `preflight` o safety può essere classificato come semplice documentazione solo se descrive meglio la procedura esistente. Se cambia limiti, comandi, watchdog, backend hardware, movimento o autorizzazione della sessione reale, è una modifica runtime/hardware e richiede il relativo collaudo.

`romeo-doctor` non deve essere documentato come comando disponibile finché non è implementato e validato nello SHA effettivamente installato.