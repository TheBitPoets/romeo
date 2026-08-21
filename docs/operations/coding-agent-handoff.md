# Handoff al coding agent: installazione, collaudo e Romeo Doctor

Questo documento definisce il lavoro che richiede accesso a una macchina TheBitLab reale e/o al robot Romeo fisico. Non è sostituibile dalla CI e deve essere sufficiente anche senza recuperare una vecchia conversazione.

## Obiettivi

Il coding agent deve completare tre risultati collegati:

1. installare e verificare `thebitlab-romeo` nell'ambiente reale TheBitLab;
2. collaudare e calibrare un esemplare fisico secondo la procedura hardware;
3. trasformare i controlli ripetibili in uno strumento diagnostico `romeo-doctor`, con preflight studente passivo e commissioning docente supervisionato.

## Prima regola: non copiare un digest da questa pagina

La release runtime approvata cambia quando la pipeline pubblica e ricertifica un'immagine. Leggi sempre:

[`docs/release/runtime-image-current.env`](../release/runtime-image-current.env)

Il record contiene:

- `ROMEO_SANDBOX_IMAGE` con digest OCI immutabile;
- SHA sorgente Romeo;
- workflow run;
- SHA broker TheBitLab usato nello smoke.

Installazione e audit devono usare il record corrente, non un digest incollato in un prompt precedente.

## 1. Inventario del deployment reale

Prima di installare package, ricostruisci la topologia osservata seguendo [Inventario del deployment](deployment-inventory.md): Python effettivo del servizio, venv, utente, supervisor, Docker daemon, configurazione persistente e nodi di runtime/grading.

Non assumere che il Python della shell amministrativa coincida con quello di TheBitLab.

## 2. Installazione plugin

Installa Romeo nello stesso ambiente Python che effettua la discovery di `thebitlab.runtimes`. Preferisci un wheel o un checkout fissato a SHA; usa editable install solo se l'ambiente è esplicitamente di sviluppo/collaudo.

Configura persistentemente il valore `ROMEO_SANDBOX_IMAGE` letto dal record di release. Un semplice `export` nella shell non è sufficiente per un servizio avviato da systemd/container/supervisor.

Poi verifica:

```console
python scripts/thebitlab_runtime_cli.py list --json
python scripts/thebitlab_runtime_cli.py probe romeo-sim --json
```

Segui [Verificare l'installazione](verify-installation.md) e [Aggiornamento e rollback](upgrade-rollback.md).

## 3. End-to-end del vero percorso studente

Non limitarti al worker o al plugin chiamato direttamente. Prova:

```text
assignment studente
 -> student runtime/dispatcher
 -> trusted Romeo plugin
 -> prepare_sandbox
 -> broker Docker TheBitLab
 -> worker Romeo
 -> sandbox result
 -> trusted finalize
 -> report studente
```

Per un runtime sandbox-capable deve risultare il comportamento previsto dalla policy TheBitLab: richiesta storica/default locale, backend effettivo Docker, risultato autorevole e nessun fallback process-only se la sandbox fallisce.

Esegui almeno una Activity Y1 command-trace/trusted replay e una Y2 behavioral.

## 4. Fail-closed

In modo controllato e reversibile verifica digest mancante/non valido e, se possibile senza interrompere altri servizi, sandbox/Docker indisponibile. Il risultato deve essere un fallimento stabile del grading autorevole, mai l'esecuzione automatica di `plugin.run()` sull'host.

Ripristina subito la configurazione approvata.

## 5. Commissioning fisico

Prima di muovere il robot leggi:

- [Safety hardware](../hardware/safety.md);
- [Commissioning](../hardware/commissioning.md);
- [Checklist hardware](../hardware/pre-merge-checklist.md);
- issue Romeo #6.

Identifica Raspberry Pi, CRICKIT, motori, servo, camera e alimentazione. Inizia con ruote sollevate o robot assicurato, velocità conservative e possibilità immediata di togliere alimentazione.

Verifica almeno:

- motore sinistro e destro separatamente;
- polarità/verso con conferma umana se non esiste feedback sensoriale sufficiente;
- forward/backward/left/right/stop;
- stop su eccezione e shutdown;
- watchdog con latenza **misurata**;
- perdita controller, TCP e WebSocket;
- pan/tilt e limiti conservativi senza battuta meccanica;
- Picamera2, still e streaming;
- motori + camera/servo sotto carico e segnali di brownout/reset;
- differenza fra ruote e necessità di inversione/trim/speed limit.

Mantieni la calibrazione del singolo esemplare separata dai default del modello/simulatore.

## 6. Stesso programma simulatore → robot

Scegli una missione semplice e usa lo stesso `main.py` prima in TheBitLab e poi sul robot. Confronta sequenza, tempi, direzioni, distanza/rotazione indicative e deviazioni.

Non aspettarti identità perfetta: documenta l'effetto di attrito, batteria, superficie, tolleranze dei motori e calibrazione.

## 7. `romeo-doctor`

Il collaudo non deve rimanere solo una checklist manuale. Riusa le abstraction Romeo esistenti per costruire, se il codice corrente non lo contiene già, uno strumento diagnostico coerente.

### Preflight studente

Il normale `romeo-doctor` deve essere rapido, leggibile e prevalentemente passivo. Può controllare package/versione, backend, I2C/CRICKIT, calibrazione, limiti, camera, rete/servizi richiesti e stato safety/watchdog senza muovere automaticamente il robot a ogni run.

Output umano indicativo:

```text
[OK] CRICKIT
[OK] calibrazione motori
[OK] watchdog
[OK] camera
[OK] rete
Romeo è pronto.
```

Gli errori devono spiegare cosa è stato controllato, perché serve, una possibile causa e una verifica semplice. Lo stack trace non è l'interfaccia primaria per uno studente.

### Commissioning docente

Una modalità esplicita, per esempio `romeo-doctor --commission`, può eseguire test attivi supervisionati. Ogni movimento deve avere velocità/durata limitate, conferma umana e STOP garantito anche su eccezione, timeout o `KeyboardInterrupt`.

### Output machine-readable

Se implementato, `romeo-doctor --json` deve usare uno schema versionato e riportare check `passed/failed/skipped/warning`, misure, stato readiness e calibrazione non sensibile. Definisci exit code stabili.

### Test

Quasi tutta la logica diagnostica deve essere provabile con fake/mock: device mancanti, calibrazione invalida, camera assente, watchdog, output JSON, exit code e soprattutto STOP su errore/timeout/Ctrl-C. Le prove fisiche restano marcate `hardware`.

## 8. Integrazione futura del preflight con TheBitLab

L'obiettivo UX futuro è:

```text
simulatore + grading
 -> Run on real Romeo
 -> preflight
 -> OK: esecuzione
 -> FAIL: blocco + spiegazione
```

Non hardcodare Romeo nel core TheBitLab. Se serve cambiare il contratto generico o introdurre una capability comune per health/preflight, trattala come decisione architetturale e fermati prima di modificare l'ABI. Se il controllo può restare interno al plugin Romeo senza cambiare contratti comuni, procedi autonomamente.

## 9. Evidenze

Crea `docs/hardware/physical-validation-YYYY-MM-DD.md` con ambiente, hardware, SHA/versioni, digest, probe, Y1/Y2, fail-closed, misure watchdog, motori, servo, camera, alimentazione, calibrazione, prova simulator→real e stato di `romeo-doctor`.

Non inserire segreti.

Aggiorna issue #6 spuntando soltanto controlli osservati realmente. Chiudila solo quando Romeo fisico è davvero pronto per la classe.

## Criterio di completamento

Non dichiarare completato nulla che non sia stato osservato direttamente. Nel report finale separa sempre:

- completato;
- misure ottenute;
- fix/PR creati;
- non verificato;
- blocker;
- eventuale decisione architetturale richiesta.
