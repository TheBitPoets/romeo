# Romeo Doctor

`romeo-doctor` controlla il robot prima delle attività e conserva la calibrazione
del singolo esemplare. Il comando predefinito è passivo: non muove motori o servo
e non acquisisce fotografie.

## Preflight studente

Nel vero ambiente Python di Romeo:

```text
romeo-doctor
romeo-doctor --student
romeo-doctor --json
```

Il preflight controlla Python, package, backend `crickit`, calibrazione, I2C,
CRICKIT con `SafetyBackend`, watchdog, limite velocità, Picamera2, rete e
l'eventuale server configurato. Il probe passivo costruisce il servizio
Picamera2 senza configurare lo stream né acquisire immagini; apertura completa e
JPEG vengono verificati soltanto nel commissioning supervisionato. Un check
`warning` non blocca; un check bloccante
`failed` produce `ready=false`.

Exit code:

- `0`: pronto;
- `1`: preflight completato ma Romeo non è pronto;
- `2`: commissioning annullato;
- `3`: errore di configurazione o commissioning.

L'output JSON usa `romeo.hardware_diagnostic.v1`. Ogni check contiene `id`,
`status` (`passed`, `failed`, `skipped`, `warning`), `detail` e `measured`.
Non contiene password, token, cookie, MAC address o seriali hardware.

## Commissioning docente

Prima di eseguire:

- solleva Romeo affinché le ruote non tocchino il pavimento;
- libera l'area e non lasciare persone davanti al robot;
- prepara un modo immediato per togliere alimentazione;
- controlla tensione, polarità, massa comune e cablaggi;
- usa esclusivamente una sessione locale supervisionata.

Avvio:

```text
romeo-doctor --commission
```

Il docente deve scrivere `SICURO`. Ogni motore riceve al massimo throttle `0.15`
per `0.4 s`; il codice rifiuta valori superiori a `0.2` o `0.5 s`. Un timer
indipendente e un blocco `finally` chiamano `stop()` anche con eccezione,
timeout o Ctrl-C. Il docente conferma la direzione osservata: il Doctor propone
l'inversione ma non salva nulla fino alla conferma finale `SALVA`.

Il watchdog viene provato tre volte con throttle `0.10`. Il Doctor registra
latenze minima, massima e media soltanto dopo che `SafetyBackend` ha completato
lo stop. Un timer indipendente ferma comunque i motori se il watchdog non
conferma l'intervento.

I limiti pan/tilt vengono inseriti come valori conservativi e poi provati dal
centro verso i limiti dichiarati. Il Doctor non cerca automaticamente la battuta.
Rifiuta il limite se compaiono buzzing, resistenza o cavi in tensione. La foto
JPEG di commissioning è acquisita soltanto dopo conferma esplicita; un errore
camera lascia comunque i motori fermi.
Il servo torna al centro sicuro dopo ogni posizione, anche su rifiuto o Ctrl-C.

## Configurazione persistente

Percorso Linux predefinito:

```text
~/.config/romeo/hardware.json
```

`ROMEO_DOCTOR_CONFIG` seleziona un percorso amministrativo esplicito;
`XDG_CONFIG_HOME` è rispettato. Lo schema è
`romeo.hardware_calibration.v1` e separa:

- `model_defaults`: valori generali del modello;
- `unit_calibration`: inversioni, trim, speed limit, limiti servo e watchdog del
  singolo robot;
- `commissioning`: stato, timestamp, versione package e fingerprint per-unità
  SHA-256 specifico del singolo Raspberry ma privo del seriale grezzo, più le
  misure watchdog in millisecondi.

Il fingerprint deriva prima dal seriale device-tree del Raspberry e usa il
campo `Serial` di `/proc/cpuinfo` soltanto come fallback per kernel Raspberry
meno recenti. Il seriale originale non viene salvato né mostrato. Il preflight
ricalcola il fingerprint: una calibrazione copiata su un altro Romeo, un record
legacy senza fingerprint valido o una identità non leggibile bloccano `ready`.
La forma JSON resta `romeo.hardware_calibration.v1`: il campo
`hardware_fingerprint` esisteva già, quindi cambia soltanto la sua semantica
fail-closed e non serve una v2.

Il file è validato in modo stretto e salvato atomicamente. Campi sconosciuti
sono rifiutati, anche per evitare che credenziali vengano inserite per errore.
Lo schema JSON documenta anche i vincoli incrociati `pan_min < pan_max` e
`tilt_min < tilt_max`, applicati dal validatore Romeo perché JSON Schema
standard non confronta direttamente proprietà sorelle.
Il backend `crickit` consuma la calibrazione; `mock` e simulatore restano
invariati. `ROMEO_MAX_SPEED` e `ROMEO_COMMAND_TIMEOUT`, se impostate
esplicitamente dal servizio, hanno precedenza.

Stati:

- `not_commissioned`: nessun collaudo registrato;
- `commissioned`: commissioning salvato;
- `preflight_failed`: almeno un controllo bloccante fallisce;
- `ready`: commissioning coerente con la versione installata e preflight OK.

Una variazione della versione package invalida la readiness finché il docente
non ricontrolla il robot. Non è una firma crittografica e non sostituisce la
supervisione.

## Test senza hardware e opt-in fisico

La logica usa backend/camera fake in CI. Il probe fisico passivo è separato:

```text
ROMEO_BACKEND=crickit ROMEO_HARDWARE_TEST=1 python -m pytest \
  -m hardware tests/test_doctor_hardware.py
```

Non automatizzare i test attivi in una CI non presidiata.
