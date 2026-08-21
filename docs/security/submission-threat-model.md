# Threat model delle submission TheBitLab

Audit eseguito il 21 agosto 2026 contro `2cornot2c` commit
`5472eef86568a4e7ce59ad34ba937220df27efd7`.

## Confine di fiducia osservato

Il plugin `romeo-sim` avvia un processo Python con `-I`, directory di lavoro
dedicata e timeout. Queste misure isolano import e ciclo di vita del processo;
**non costituiscono una sandbox**. Il processo conserva i diritti dell'utente
host. Può leggere o modificare file accessibili, aprire rete e subprocess,
osservare parte dell'ambiente e consumare CPU, memoria, disco e processi. Un
timeout non limita da solo i processi figli. Se le submission condividono utente
o directory, può inoltre tentare l'accesso ai lavori altrui.

Il worker esegue submission, simulatore e grader nello stesso interprete. Codice
ostile può quindi manomettere oggetti Python o artefatti prima del grading. Il
risultato è deterministico per codice collaborativo, ma non è una prova
valutativa resistente alla manomissione.

| Minaccia | Controllo attuale | Residuo |
| --- | --- | --- |
| Lettura/scrittura file host | containment dei path dichiarati | accesso host ancora possibile dal codice Python |
| Rete | nessuno nel processo locale | rete host disponibile |
| Subprocess | timeout del worker diretto | figli e process tree non confinati |
| Environment/segreti | ambiente figlio ridotto a una allowlist | altri canali host restano accessibili |
| CPU/memoria/disco/PID/output | timeout e limiti di input/storia | nessun limite kernel completo |
| Altre submission | directory artefatti verificata, symlink rifiutati | dipende dai permessi e mount dell'host |
| Integrità del grader | snapshot prima del cleanup | stesso interprete della submission |

## Boundary TheBitLab esistente

Il backend generico TheBitLab dispone già di un profilo Docker: utente non
root, root filesystem read-only, rete disabilitata, capability rimosse,
`no-new-privileges`, limiti PID/memoria/CPU, sorgente read-only e tmpfs. Il
contratto runtime plugin, però, delega al plugin l'esecuzione e attualmente il
dispatcher invoca Romeo localmente: quel profilo non avvolge automaticamente
`run()`.

Non viene introdotta qui una seconda sandbox. Tutte le 43 activity dichiarano
pertanto `sandbox: false`; probe e documentazione espongono
`execution_isolation=process-only` e `untrusted_submissions_supported=false`.

## Decisione architetturale aperta

La scelta raccomandata è estendere il broker sandbox ufficiale TheBitLab alle
activity runtime e tenere simulatore/grader fidati fuori dal processo studente.
Le alternative sono descritte nel report pre-merge. Fino alla decisione il
runtime è adatto a esercizi formativi locali con codice collaborativo, non a
grading sommativo di codice non affidabile.
