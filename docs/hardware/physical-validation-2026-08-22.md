# Validazione fisica Romeo — 2026-08-22

Stato: **in corso; inventario passivo ripreso il 2026-08-25, prove attive
bloccate da nuovi eventi di undervoltage**.

Questo documento registra esclusivamente valori misurati e osservazioni riferite
dall'operatore presente davanti al robot. Il documento del 2026-08-21 è evidenza
storica e non fornisce alcun PASS hardware per questa sessione.

## Identificazione della sessione

| Campo | Valore | Metodo / evidenza |
|---|---|---|
| Data | 2026-08-22 | Data della sessione, fuso Europe/Rome |
| Tester / operatore | Da confermare | Non ancora comunicato |
| Repository | `TheBitPoets/romeo` | Remoto Git `origin` |
| Branch | `hardware/physical-validation-2026-08-22` | `git branch --show-current` |
| Commit di partenza | `45e5f7e131802fccc89358a23a25dbed1884bbfa` | `git rev-parse HEAD` e `git rev-parse origin/main`, dopo `git fetch origin main --prune` |
| Stato iniziale | Pulito | `git status --short --branch` prima della creazione del branch |
| Baseline `images/` | tree `4bd50b952ae4e63fc1e2e1df10b6e330929903ab` | `git rev-parse HEAD:images`; nessuna immagine deve essere modificata |
| Host della sessione Codex | PC Windows, non identificato come Raspberry Pi | `Get-ComputerInfo`; non usare le sue versioni come inventario del robot |

## Procedura e gate

La procedura autorevole è
[`pre-merge-checklist.md`](pre-merge-checklist.md). Prima delle prove sono stati
letti, nell'ordine richiesto: `safety.md`, `commissioning.md`, `doctor.md`, la
checklist autorevole, l'evidenza storica del 2026-08-21, le due guide studente e
l'issue #6 con i commenti correnti.

Nessun comando attivo viene eseguito senza briefing di sicurezza e conferma
intermedia dell'operatore.

### Ripresa della sessione — 2026-08-25

Il branch locale e `origin/main` coincidono ancora al commit
`45e5f7e131802fccc89358a23a25dbed1884bbfa`. La sessione SSH passiva è stata
ripresa sul nodo `romeo` come utente `acari`; l'orologio del Raspberry indicava
`2026-08-25T10:17:01+02:00`.

I probe passivi hanno riconfermato Raspberry Pi 4 Model B Rev 1.5, Debian 13.2,
kernel `6.12.47+rpt-rpi-v8`, Python 3.13.5, `thebitlab-romeo` 0.2.0 editable dal
checkout pulito `/home/acari/romeo-src` allo stesso SHA di partenza, nodi I2C
presenti e Picamera2 0.3.33. `rpicam-hello --list-cameras`, senza acquisire
fotogrammi, ha enumerato il sensore `imx708` a 4608×2592.

Non esiste ancora `/home/acari/.config/romeo/hardware.json`: il singolo
esemplare non ha una calibrazione/commissioning persistente. Il nuovo avvio,
iniziato alle `2026-08-25 10:10:58`, ha restituito `throttled=0x50000`; il kernel
ha registrato undervoltage a 11.327185 s, 466.961791 s e 505.272535 s, oltre a
normalizzazioni a 45.599078 s e 470.994071 s. Pertanto l'alimentazione non è
considerata verificata e nessuna prova attiva è autorizzata sulla base di questo
avvio.

Il monitoraggio passivo successivo ha rilevato complessivamente sei intervalli
di undervoltage a riposo: 11.327185–45.599078 s, 466.961791–470.994071 s,
505.272535–515.349266 s, 626.225917–632.273907 s,
795.574233–799.606365 s e 906.459774–910.491907 s dall'avvio. Una finestra di
campionamento da `2026-08-25T10:26:17+02:00` a
`2026-08-25T10:27:18+02:00` ha mostrato sempre `throttled=0x50000` senza flag
correnti, ma l'ultimo intervallo era terminato appena circa nove secondi prima.
Esito: **FAIL alimentazione a riposo / instabilità intermittente**; la finestra
pulita di un minuto non costituisce stabilizzazione e non autorizza carichi
attivi.

### Ripresa della sessione — 2026-08-29

Il repository locale sul branch `hardware/physical-validation-2026-08-22`, il
checkout installato sul Raspberry Pi e il `main` remoto coincidono al commit
`45e5f7e131802fccc89358a23a25dbed1884bbfa`. L'issue #6 è ancora aperta.

L'operatore ha dichiarato un nuovo schema di alimentazione separato: Raspberry
Pi alimentato dal powerbank tramite il proprio ingresso USB-C e CRICKIT
alimentato separatamente mediante quattro batterie AA NiMH. La presenza, la
polarità e la tensione del pacco CRICKIT non sono ancora state misurate in
questa ripresa e pertanto non costituiscono un PASS.

Il Pi si è avviato alle `2026-08-29 09:17:33+02:00`. Il primo probe alle
`09:27:31+02:00` ha restituito `throttled=0x50000`: nessun undervoltage attivo,
ma eventi storici di undervoltage e throttling dall'avvio. Il kernel ha
registrato undervoltage a 9.407099 s e 19.486993 s, con normalizzazione
rispettivamente a 15.454979 s e 29.566977 s.

L'operatore ha successivamente chiarito la sequenza fisica osservata: ha
collegato e acceso prima il pacco batterie del CRICKIT e soltanto dopo, trascorso
il tempo necessario a trovare il cavo, ha collegato il powerbank direttamente
all'ingresso USB-C del Pi. Poiché il CRICKIT HAT alimenta anche il Pi attraverso
il connettore GPIO, questa sequenza spiega tecnicamente l'avvio iniziale dal
pacco NiMH e i due eventi prima dell'arrivo dell'alimentazione USB-C. È una
motivazione verificabile della fase transitoria, ma per eliminare l'ambiguità è
richiesto un nuovo avvio controllato Pi-only con CRICKIT spento.

È stata quindi osservata una finestra passiva a riposo dal
`2026-08-29T09:27:51+02:00` al `2026-08-29T09:31:04+02:00`, con 36 campioni a
intervalli di circa cinque secondi. Tutti i campioni hanno mantenuto
`throttled=0x50000`, senza comparsa di flag correnti o nuovi eventi kernel. La
temperatura osservata è rimasta tra 45.764 °C e 50.634 °C. Esito:
**STABILE A RIPOSO DOPO IL BOOT, MA NON PASS**; i due cali durante l'avvio
restano da diagnosticare e il carico combinato non è stato provato.

Inventario software riconfermato passivamente: Raspberry Pi 4 Model B Rev 1.5,
kernel `6.12.47+rpt-rpi-v8`, Python 3.13.5, `thebitlab-romeo` 0.2.0 editable da
`/home/acari/romeo-src`, Picamera2 0.3.33 e nodi I2C 0, 1, 10, 20, 21 e 22
presenti. Nessun backend hardware, motore, servo o acquisizione camera è stato
attivato.

È stato poi eseguito uno shutdown pulito con il pacco CRICKIT scollegato. Dopo
lo shutdown i LED di Pi e CRICKIT sono rimasti alimentati dall'USB-C; rimosso
l'USB-C, tutti i LED si sono spenti e l'operatore non ha riferito movimenti.
Il successivo avvio controllato Pi-only, con pacco CRICKIT fisicamente
scollegato, ha prodotto il boot ID
`7df3979a-7389-49d0-8cf9-01f8c3f78f61` e boot time corretto dalla
sincronizzazione dell'orologio `2026-08-29 09:51:36+02:00`. Il primo probe ha
restituito `throttled=0x0`, temperatura 48.7 °C e nessuna riga kernel relativa
a undervoltage, voltage o brownout. Dodici campioni passivi a circa cinque
secondi hanno mantenuto `throttled=0x0`; temperatura minima 46.2 °C, massima
48.7 °C. Il boot ID è rimasto invariato e il controllo finale era ancora
`throttled=0x0`, senza eventi kernel. Esito software del test Pi-only:
**PASS PI-ONLY A RIPOSO**. L'operatore ha confermato che durante l'avvio non ha
osservato warning low-voltage, rumori, movimenti o LED CRICKIT accesi. Questo
risultato non qualifica il CRICKIT né il carico combinato.

La misura a vuoto della tensione e della polarità del pacco batterie CRICKIT
non è stata eseguita perché l'operatore non dispone di un multimetro. Stato:
**NON ESEGUITA / EVIDENZA MANCANTE**, non PASS e non N/A. L'eventuale prova di
alimentazione successiva deve quindi partire da ispezione visiva del pacco e
collegamento supervisionato, senza assumere tensione o polarità misurate.
L'operatore ha identificato quattro celle Panasonic/eneloop AA, 1.2 V e
capacità minima dichiarata 2500 mAh, orientate correttamente; ha osservato fili
integri e spinotto saldato. La polarità è stata verificata dal tecnico che ha
costruito il portabatterie, ma non rimisurata in questa sessione.

Con il robot sollevato, ruote libere, area sgombra e arresto ottenibile
scollegando il jack, l'operatore ha collegato il pacco al CRICKIT mentre il Pi
era già stabile via USB-C. Ha osservato LED CRICKIT verde fisso, entrambe le
ruote ferme, servo fermi, nessun buzzing, Pi acceso senza warning low-voltage e
nessun odore o calore anomalo. Dodici campioni passivi a riposo hanno restituito
`throttled=0x0`, con temperatura minima 53.0 °C e massima 54.5 °C. Il boot ID è
rimasto `7df3979a-7389-49d0-8cf9-01f8c3f78f61`; il controllo finale era
`throttled=0x0` e il filtro del kernel non ha trovato eventi voltage, brownout o
errori I2C. Esito: **PASS ACCENSIONE E RIPOSO PI+CRICKIT**, senza carichi; non è
ancora un PASS di motori, servo, camera o carico combinato.

Il preflight passivo è stato eseguito nelle tre forme `romeo-doctor`,
`romeo-doctor --student` e `romeo-doctor --json`. Tutte hanno terminato con
exit code 1 e stato fail-closed: Python 3.13.5 e package 0.2.0 PASS; calibrazione
e identità per-unità assenti; backend selezionato `mock`; I2C, CRICKIT,
watchdog e limite velocità saltati; Picamera2 soltanto inizializzato, senza
apertura o foto; server saltato. Il JSON riporta schema
`romeo.hardware_diagnostic.v1`, `ready=false` e `status=preflight_failed`.
Esito: **FAIL ATTESO / COMMISSIONING NON ANCORA ESEGUITO**; il fail-closed non è
stato aggirato.

È stato inoltre riprodotto un bug del controllo rete: il Doctor riporta
`Nessun indirizzo di rete disponibile` e `address_count: 0`, benché la sessione
SSH sia attiva su `192.168.1.61` e `hostname -I` restituisca lo stesso indirizzo.
La causa verificata è che `socket.getaddrinfo(socket.gethostname(), None)`
risolve `romeo` soltanto in `127.0.1.1`, che il Doctor scarta correttamente come
loopback senza però enumerare l'indirizzo dell'interfaccia. Stato controllo
rete: **FAIL SOFTWARE RIPRODOTTO**, non FAIL della connettività e non PASS.

## Inventario hardware e software

| Elemento | Modello / valore | Metodo | Stato / note |
|---|---|---|---|
| Raspberry Pi modello/revisione | Raspberry Pi 4 Model B Rev 1.5 | `tr -d '\0' </sys/firmware/devicetree/base/model; echo`, output riferito dall'operatore | VERIFICATO VIA DEVICE TREE |
| Raspberry Pi OS | Raspberry Pi reference `2025-12-04`, generato con `pi-gen` commit `4997bf4e4e49bc3305eb182a4a08bd023529da04`, stage4; userspace Debian GNU/Linux 13.2 (trixie) | `cat /etc/rpi-issue`; `cat /etc/os-release`, output riferito dall'operatore | VERIFICATO |
| Kernel | Linux `6.12.47+rpt-rpi-v8`, build `Debian 1:6.12.47-1+rpt1 (2025-09-16)`, aarch64 | `uname -a`, output riferito dall'operatore | VERIFICATO |
| CRICKIT HAT modello/revisione | Da determinare | Ispezione etichetta/scheda | NON VERIFICATO |
| Firmware CRICKIT | Da determinare se rilevabile | Probe passivo supportato | NON VERIFICATO |
| Motore sinistro | Da determinare | Ispezione etichetta | NON VERIFICATO |
| Motore destro | Da determinare | Ispezione etichetta | NON VERIFICATO |
| Collegamento motori | Atteso da documentazione: sinistro Motor 2, destro Motor 1 | Da confermare con ispezione cablaggio | NON VERIFICATO; il valore atteso non è evidenza fisica |
| Servo pan | Da determinare | Ispezione etichetta e cablaggio | NON VERIFICATO |
| Canale pan | Atteso dal backend: servo 1 | Da confermare con ispezione cablaggio | NON VERIFICATO |
| Servo tilt | Da determinare | Ispezione etichetta e cablaggio | NON VERIFICATO |
| Canale tilt | Atteso dal backend: servo 4 | Da confermare con ispezione cablaggio | NON VERIFICATO |
| Camera | Da determinare | Probe passivo + ispezione | NON VERIFICATO |
| Alimentazione Raspberry Pi | Unica sorgente dichiarata: powerbank SBS PD 20 W, 10000 mAh; non collegato all'ingresso USB-C del Pi; percorso elettrico esatto ancora da confermare | Dichiarazione e osservazione dell'operatore | FAIL/BLOCCANTE: il Raspberry Pi mostra `low voltage warning, please check your power supply` |
| Alimentazione CRICKIT/motori | Stessa unica sorgente, collegata al connettore di alimentazione cilindrico riferito dall'operatore; cavo/adattatore e scheda destinataria da confermare | Dichiarazione e osservazione dell'operatore | PARZIALE; valori d'uscita effettivi non ancora letti |
| Tensioni nominali | SBS: USB 1/2 output `5 V 3 A / 9 V 2 A / 10 V 2.25 A / 12 V 1.5 A`; USB-C output `5 V 3 A / 9 V 2.22 A / 12 V 1.67 A`; total output `22.5 W max`; batteria `10000 mAh (3.7 V, 37 Wh)` | Fotografie odierne della confezione fornite dall'operatore | VERIFICATO DA ETICHETTA; SKU coperto/non leggibile |
| Python sul Pi | 3.13.5 nella shell corrente | `python3 --version` | VERIFICATO PER L'INTERPRETE DI SISTEMA |
| `thebitlab-romeo` installato | 0.2.0 in `/home/acari/romeo-venv`, editable da `/home/acari/romeo-src`; `romeo-doctor` presente | `pip show`; `romeo-doctor --help` | PASS INSTALLAZIONE; nessun PASS hardware |
| Source/commit installato | `45e5f7e131802fccc89358a23a25dbed1884bbfa` | Clone pulito di `refs/heads/main`; `git rev-parse HEAD`, `git status` | VERIFICATO |
| I2C | Device presenti: `/dev/i2c-0`, `1`, `10`, `20`, `21`, `22`; CRICKIT spento e non sondato | `ls -l /dev/i2c-*` | PARZIALE; presenza bus, non raggiungibilità periferica |
| Picamera2 | 0.3.33 da `/usr/lib/python3/dist-packages`, visibile nel venv dedicato | `pip show picamera2` con `/home/acari/romeo-venv/bin/python` | PASS DISPONIBILITÀ MODULO; camera non aperta/acquisita |

Account operativo osservato: `acari`, uid/gid 1000, appartenente tra gli altri
ai gruppi `sudo`, `video`, `gpio`, `i2c`, `spi`, `render` e `input`. Package
Raspberry `raspberrypi-sys-mods` versione `1:20251028+1`; `raspberrypi-ui-mods`
non ha prodotto una versione. Individuato `/home/acari/pyenv/pyvenv.cfg`;
nessun servizio systemd con nome contenente `romeo` è stato elencato.

Il virtualenv `/home/acari/pyenv` usa Python 3.13.5 e
`include-system-site-packages = false`. `import romeo`, `pip show
thebitlab-romeo` e la verifica di `bin/romeo-doctor` hanno confermato l'assenza
del package. Un tentativo separato di lettura metadata ha prodotto un
`SyntaxError` perché il terminale ha inserito un ritorno a capo nel nome del
package; non è usato come evidenza dell'assenza.

Pre-installazione: Git 2.47.3; filesystem root `/dev/sda2` 28 GiB, 7.0 GiB
usati e 20 GiB disponibili (27%); risoluzione `github.com` funzionante;
`git ls-remote` ha osservato `refs/heads/main` allo SHA
`45e5f7e131802fccc89358a23a25dbed1884bbfa`, uguale alla baseline della
sessione. Il probe Pi-only è rimasto `throttled=0x0`.

Installazione sul Pi: creati `/home/acari/romeo-src` e
`/home/acari/romeo-venv`; il nuovo venv usa Python 3.13.5 con
`include-system-site-packages = true`. Installazione editable
`/home/acari/romeo-src[hardware]` completata con exit code 0. Versioni osservate:
`thebitlab-romeo 0.2.0`, `adafruit-circuitpython-crickit 2.3.24`, Picamera2
0.3.33 dal package Raspberry Pi OS. `romeo-doctor --help` ha confermato entry
point e modalità passive/commissioning senza costruire il backend. Subito dopo
l'installazione `vcgencmd get_throttled` era ancora `0x0`.

## Preflight passivo

| Comando | Exit code | Risultato | Evidenza |
|---|---:|---|---|
| `romeo-doctor` | — | NON ESEGUITO | In attesa di accesso al vero ambiente Python del Pi |
| `romeo-doctor --student` | — | NON ESEGUITO | In attesa di accesso al vero ambiente Python del Pi |
| `romeo-doctor --json` | — | NON ESEGUITO | In attesa di accesso al vero ambiente Python del Pi |

## Commissioning e safety reale

| Test | Risultato | Comando | Misura | Osservazione fisica operatore | Note |
|---|---|---|---|---|---|
| Avvio/shutdown con ruote sollevate | NON ESEGUITO | — | — | — | — |
| Motore sinistro, verso/polarità | NON ESEGUITO | — | — | — | — |
| Motore destro, verso/polarità | NON ESEGUITO | — | — | — | — |
| STOP | NON ESEGUITO | — | — | — | — |
| Watchdog | NON ESEGUITO | — | min/max/media: — | — | Configurazione: — |
| Command timeout | NON ESEGUITO | — | — | — | — |
| Ctrl+C / eccezione | NON ESEGUITO | — | — | — | — |
| Perdita controller | NON ESEGUITO | — | — | — | — |
| Disconnessione TCP | NON ESEGUITO | — | — | — | — |
| Disconnessione WebSocket | NON ESEGUITO | — | — | — | Valutare applicabilità sull'architettura reale |

## Movimento a terra

| Test | Risultato | Comando | Valore osservato | Osservazione fisica operatore |
|---|---|---|---|---|
| Forward | NON ESEGUITO | — | — | — |
| Backward | NON ESEGUITO | — | — | — |
| Left | NON ESEGUITO | — | — | — |
| Right | NON ESEGUITO | — | — | — |
| Stop a terra | NON ESEGUITO | — | — | — |

Deriva, differenza ruote, vibrazioni/rumori e trim: **non ancora osservati**.

## Pan/tilt

| Parametro / test | Risultato o valore | Osservazione fisica operatore |
|---|---|---|
| Centro sicuro | NON DETERMINATO | — |
| `pan_min` | NON DETERMINATO | — |
| `pan_max` | NON DETERMINATO | — |
| `tilt_min` | NON DETERMINATO | — |
| `tilt_max` | NON DETERMINATO | — |

## Camera

Picamera2, acquisizione JPEG, orientamento, MJPEG, FPS/latenza, errori e
temperatura: **NON ESEGUITI / NON MISURATI**.

## Alimentazione e brownout

Prima di applicare carichi è stato osservato dal vivo un warning di bassa
tensione del Raspberry Pi: `low voltage warning, please check your power
supply`. L'operatore riferisce che il Pi non è alimentato tramite il proprio
ingresso USB-C. Percorso di alimentazione, tensione nominale, corrente nominale,
connettori e massa non sono ancora stati identificati. Esito: **FAIL/BLOCCANTE**;
nessuna prova attiva deve iniziare prima della diagnosi e della correzione.

Probe passivi riferiti dall'operatore:

- `vcgencmd get_throttled` → `throttled=0x50000`: nessun flag corrente nei bit
  bassi al momento del probe; eventi storici di undervoltage e throttling
  registrati dall'avvio;
- `dmesg` → undervoltage rilevato a 12.639221 s, tensione normalizzata a
  20.703204 s, nuovo undervoltage a 24.736351 s e tensione normalizzata a
  40.863219 s;
- modello via device tree → `Raspberry Pi 4 Model B Rev 1.5`.

Etichetta powerbank fotografata dall'operatore: ingressi micro-USB `5 V 2 A /
9 V 2 A / 12 V 1.5 A` e USB-C `5 V 2.4 A / 9 V 2 A / 12 V 1.5 A (18
W)`; uscite USB 1/2 e USB-C come riportato nell'inventario. Il massimo dichiarato
a 5 V è 3 A; il profilo esatto usato dal cavo USB→jack e la caduta sotto carico
non sono ancora misurati.

Test diagnostico Pi-only supervisionato: jack CRICKIT scollegato, CRICKIT
riferito su OFF e Raspberry Pi alimentato direttamente alla propria USB-C dal
powerbank. Il Pi si è avviato; l'operatore non ha visto warning ma ha aperto il
monitor in ritardo, ha riferito LED CRICKIT apparentemente spenti e nessun
movimento o rumore di motori/servo. Boot osservato: `2026-08-22 07:32:47`.
`vcgencmd get_throttled` ha restituito `throttled=0x0` e il filtro `dmesg` per
undervoltage/voltage/brownout non ha restituito righe. Risultato: **PASS
DIAGNOSTICO PI-ONLY A RIPOSO**; non costituisce PASS dell'alimentazione
combinata. Il confronto circoscrive il problema al percorso USB→jack/CRICKIT o
al budget combinato, ma non ne distingue ancora la causa.

Carico combinato, reset, brownout, errori I2C, riavvii, instabilità camera e
comportamento motori: **NON ESEGUITI / NON OSSERVATI**.

Shutdown diagnostico supervisionato: dopo briefing e conferma `PRONTO ALLO
SHUTDOWN`, l'operatore ha eseguito `sudo shutdown -h now`, quindi ha osservato
LED spenti e nessun movimento dei motori. La sorgente era un powerbank SBS PD
20 W, 10000 mAh, collegato tramite USB verso il connettore cilindrico di
alimentazione riferito dall'operatore. Questa osservazione documenta lo stato
finale dello shutdown, ma non sostituisce le prove attive di stop/fail-safe.

Secondo shutdown, dalla configurazione Pi-only: dopo lo spegnimento del sistema
ma con cavo USB-C ancora collegato, l'operatore ha osservato accendersi una luce
verde sul CRICKIT nonostante il jack cilindrico fosse scollegato. L'operatore
ritiene fosse acceso soltanto il verde ma non ne è certo. Dopo la rimozione del
cavo USB-C la luce CRICKIT si è spenta; nessun movimento o rumore. Questo prova
che l'alimentazione USB-C del Pi energizza almeno parte/indicazione del CRICKIT
attraverso l'HAT, ma non determina quali rail fossero attive né autorizza
l'alimentazione di motori/servo da quel percorso. Risultato: **OSSERVAZIONE
SAFETY, NON PASS**.

## Calibrazione

Nessun coefficiente è stato determinato. Non è stato scritto alcun file
`romeo.hardware_calibration.v1` durante questa sessione.

## Missione simulatore → robot e audit documentazione studente

NON ESEGUITA. L'Activity e il `main.py` invariato verranno registrati dopo il
commissioning e i gate safety. Ambiguità, passaggi mancanti, comandi obsoleti e
procedure di recupero mancanti saranno annotati qui senza usare conoscenze
implicite.

Finding preliminare di documentazione: le fotografie storiche del README
mostrano Raspberry Pi 4/Pibow, CRICKIT HAT, motori gialli tipo TT, powerbank e
pan/tilt. Le righe 386 e 442 parlano dei collegamenti di alimentazione sia del
CRICKIT sia del Raspberry Pi, mentre l'esemplare odierno è stato riferito come
alimentato soltanto dal jack cilindrico del CRICKIT, con USB-C del Pi non
collegato. Il README non specifica sorgente, profili V/A, cavo/adattatore,
polarità o budget di corrente combinato. Le immagini storiche descrivono il
montaggio previsto ma non costituiscono evidenza del cablaggio fisico odierno.

Finding documentale riprodotto sul Pi: `docs/hardware/camera.md` prescrive
l'installazione apt di `python3-picamera2`, mentre README e guide ambiente creano
venv isolati senza documentare `--system-site-packages`. Nel venv reale
`/home/acari/pyenv` (`include-system-site-packages = false`) Picamera2 non è
importabile, pur essendo disponibile nell'interprete di sistema da
`/usr/lib/python3/dist-packages/picamera2`. La procedura hardware deve spiegare
come rendere coerenti venv e package Raspberry Pi OS senza ricorrere a
conoscenza implicita.

## Problemi e follow-up

1. Determinare accesso al terminale del Raspberry Pi reale senza registrare
   credenziali nel repository.
2. Completare l'inventario passivo e fisico prima di qualsiasi movimento.
3. Identificare e correggere l'alimentazione del Raspberry Pi che ha prodotto il
   warning low voltage; ripetere poi i controlli passivi di undervoltage.
4. L'operatore riferisce di non avere disponibile durante la sessione un'altra
   sorgente oltre al powerbank SBS. Il commissioning combinato resta bloccato
   finché non è disponibile e verificata un'alimentazione adeguata; un eventuale
   test Pi-only non costituirà PASS di CRICKIT, motori, servo, camera o brownout.

## Stato issue #6

Issue aperta. Nessuna casella hardware è completata e nessuna dichiarazione
«Romeo fisico pronto per la classe» è autorizzata.
