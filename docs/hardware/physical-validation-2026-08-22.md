# Validazione fisica Romeo — 2026-08-22

Stato: **in corso; alimentazioni separate stabili a riposo, prove attive
bloccate dal mancato avvio autonomo del controller Seesaw dopo power-cycle**.

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

La correzione minima è stata applicata sul branch dedicato nel commit
`faf9eda88a83fe5955c88bf2b00e75ff0605b531`: oltre alla risoluzione del nome,
il Doctor usa una route lookup UDP senza invio di pacchetti per ricavare
l'indirizzo dell'interfaccia. Il test di regressione riproduce hostname risolto
solo in `127.0.1.1` e route locale `192.168.1.61`. Verifiche locali: 21 test del
modulo Doctor PASS; suite completa 426 PASS e 3 skip attesi; Ruff PASS. Il
checkout editable della Pi è stato portato allo stesso commit e il probe ha
restituito `['192.168.1.61']`. La ripetizione di `romeo-doctor --json` ha quindi
riportato rete `passed`, `address_count: 1`; lo stato complessivo è rimasto
correttamente `preflight_failed` per calibrazione, identità e backend ancora
mancanti.

Il preflight è stato quindi ripetuto passivamente con backend selezionato per
la sola invocazione (`ROMEO_BACKEND=crickit`). Backend CRICKIT e `/dev/i2c-1`
sono stati riconosciuti, ma il check CRICKIT è fallito con `ValueError`. Una
riproduzione tramite la factory Romeo, senza accesso applicativo diretto ad
`adafruit_crickit`, ha mostrato due timeout I2C e l'errore finale
`No I2C device at address: 0x49` durante il probe del controller Seesaw.
Configurazione Pi verificata passivamente: I2C abilitato (`raspi-config nonint
get_i2c` = 0), `dtparam=i2c_arm=on`, moduli `i2c_dev`, `i2c_bcm2835` e relativi
driver caricati. `i2cdetect` non è installato e non è stata eseguita alcuna
scansione del bus. Esito: **FAIL CRICKIT/I2C A 0x49**; commissioning motori
bloccato in attesa di ispezione fisica ad alimentazioni scollegate.

L'ispezione fotografica attuale ha identificato un CRICKIT HAT per Raspberry
Pi, con header GPIO apparentemente parallelo e senza offset o pin piegati
visibili; il selettore fisico è stato confermato dall'operatore su `On`. Dopo
shutdown completo è stata ripetuta la sequenza Pi USB-C prima, pacco CRICKIT
dopo: Pi `throttled=0x0`, LED OK CRICKIT verde, warning inizialmente spento,
NeoPixel verde, nessun movimento, rumore, warning Pi, odore o calore. Il probe
Romeo ha tuttavia confermato il FAIL a `0x49`.

Seguendo il troubleshooting ufficiale Adafruit è stata quindi eseguita una
sola pressione breve di `Seesaw Reset`. L'operatore ha osservato LED OK verde,
un LED giallo lampeggiante e NeoPixel rosso; ruote e servo fermi e nessun
rumore. Il rosso è rimasto presente anche dopo aver scollegato il pacco CRICKIT,
finché il Pi è rimasto alimentato via GPIO; dopo shutdown pulito e rimozione
dell'USB-C tutti i LED si sono spenti, senza movimento o rumore. Stato:
**FAIL CRICKIT/SEESAW NON RISOLTO**. La sequenza LED non viene interpretata come
una diagnosi certa senza misura elettrica o identificazione firmware; nessun
aggiornamento firmware è stato ancora eseguito.

La diagnosi è proseguita con pacco CRICKIT scollegato e controller Seesaw
alimentato dalla propria micro-USB dati collegata al Pi. Prima del bootloader il
kernel ha rilevato il dispositivo full-speed ma non è riuscito a enumerarlo
(`error -32`, `error -71`). Un doppio reset supervisionato, attuatori fermi, ha
prodotto LED giallo pulsante e NeoPixel verde: il Pi ha quindi enumerato
`239a:002d Adafruit crickit`, `ttyACM0` e volume `CRICKITBOOT`. Il file
`INFO_UF2.TXT` identifica `UF2 Bootloader
v2.0.0-adafruit.0-14-g39b76ca`, modello `crickit`, Board-ID
`SAMD21G18A-crickit-v0`; il seriale non è riportato nell'evidenza. Le stringhe
di `CURRENT.UF2` identificano `Crickit Hat` ma non una versione applicativa
affidabile. Nessun file è stato scritto e nessun firmware è stato aggiornato.

Dopo una singola pressione per uscire dal bootloader, il NeoPixel ha
lampeggiato rosso con la sola alimentazione USB del controller e pacco
principale assente. In questa condizione il preflight Romeo ha raggiunto `0x49`
e marcato CRICKIT PASS, dimostrando che controller, firmware applicativo e
percorso I2C attraverso l'HAT erano funzionali. È stato poi collegato il pacco
CRICKIT mantenendo temporaneamente la micro-USB: operatore ha osservato OK
verde, warning spento, NeoPixel verde, attuatori fermi e Pi senza low-voltage;
Doctor CRICKIT PASS e `throttled=0x0`. Infine la micro-USB è stata rimossa,
lasciando la configurazione normale Pi USB-C + pacco CRICKIT: nessun cambiamento
fisico osservato, `throttled=0x0`, nessun evento voltage/brownout e CRICKIT PASS.
Dodici campioni a circa cinque secondi hanno mantenuto `0x0`, temperatura
57.4–58.9 °C; un ulteriore `romeo-doctor --json` ha riconfermato backend, I2C,
CRICKIT e rete PASS. Esito aggiornato: **PASS PREFLIGHT HARDWARE PASSIVO DOPO
RIPRISTINO SEESAW**, mentre commissioning, watchdog e speed limit restano
correttamente non eseguiti/saltati. La causa radice del mancato avvio Seesaw
iniziale non è provata e resta follow-up; non è stato necessario scrivere
firmware.

Dopo una successiva perdita totale di alimentazione e riavvio completo, il
CRICKIT è tornato non raggiungibile a `0x49`, pur con LED OK verde, warning
spento, NeoPixel verde, attuatori fermi e Pi `throttled=0x0`. Questo dimostra
che il ripristino Seesaw non sopravvive in modo affidabile al power-cycle e
invalida il precedente PASS come condizione persistente. Stato aggiornato:
**FAIL INTERMITTENTE/RIPRODUCIBILE ALL'AVVIO SEESAW**; commissioning ancora
bloccato.

È stato preparato, ma non installato, il firmware ufficiale Adafruit seesaw
release 1.1.6 per HAT: `seesaw-crickitHat.uf2`, 53760 byte, SHA-256
`52AC44CF1E7E7FE5DC12DB3A97831C80D3B55C755446D39BF987FDA42EDB7DC8`.
Con pacco CRICKIT scollegato, il bootloader era nuovamente entrato nello stato
atteso (giallo pulsante, NeoPixel verde), ma durante la sola verifica read-only
del volume la Pi e tutti i LED si sono spenti. L'operatore ritiene scarico il
powerbank. Il trasferimento del file non era iniziato: **NESSUN FIRMWARE
SCRITTO**. Micro-USB Seesaw, USB-C Pi e pacco CRICKIT sono stati scollegati;
operatore ha confermato tutto spento. Non verrà usata una porta USB-A del PC per
alimentare il Pi durante l'aggiornamento, a causa del rischio di corrente
insufficiente/undervoltage. Ripresa bloccata fino a sorgente Pi ricaricata e
stabile.

#### Aggiornamento firmware e nuovo test a freddo — 2026-08-29 pomeriggio

Dopo la ricarica completa del powerbank, il Pi è stato avviato da solo con
pacco CRICKIT e micro-USB Seesaw scollegati. L'operatore ha osservato soltanto
i LED Pi, attuatori fermi e nessun rumore, odore o calore; il probe passivo ha
restituito `throttled=0x0`, boot time `2026-08-29 17:11:58` e nessun evento
kernel voltage/brownout.

Con pacco CRICKIT ancora scollegato è stata collegata la micro-USB Seesaw.
L'operatore ha osservato NeoPixel verde fisso, ruote e servo fermi e nessuna
anomalia. Il doppio reset supervisionato ha prodotto lo stato bootloader
atteso: LED giallo pulsante lento, NeoPixel verde, attuatori fermi. Il Pi ha
enumerato `239a:002d Adafruit crickit`, `/dev/ttyACM0` e il volume
`/media/acari/CRICKITBOOT`.

Il firmware ufficiale Adafruit `seesaw-crickitHat.uf2` della release 1.1.6 è
stato trasferito nella directory temporanea del Pi e ricontrollato prima della
scrittura: 53760 byte, SHA-256
`52AC44CF1E7E7FE5DC12DB3A97831C80D3B55C755446D39BF987FDA42EDB7DC8`.
Un primo comando di copia non è arrivato alla scrittura a causa di quoting
PowerShell ed è terminato con exit code 1. Il secondo comando ha verificato
l'hash (`OK`), copiato il file sul volume e completato `sync` con exit code 0.
L'operatore ha osservato spegnimento del LED giallo, NeoPixel rosso
lampeggiante, un riavvio, attuatori fermi e nessuna anomalia. Il bootloader è
scomparso e il dispositivo applicativo è stato enumerato come
`239a:002e Adafruit Crickit Hat`. Con micro-USB presente Romeo Doctor ha
raggiunto il CRICKIT e la Pi è rimasta `throttled=0x0`.

Il pacco CRICKIT è stato quindi collegato sotto supervisione: LED principale
verde fisso, giallo spento, NeoPixel verde fisso, ruote e servo fermi, nessun
low-voltage o altra anomalia. Otto campioni hanno restituito `throttled=0x0`,
senza eventi kernel voltage/brownout/I2C. Rimuovendo la micro-USB non è cambiato
nulla fisicamente e Romeo Doctor ha continuato a raggiungere il CRICKIT via
HAT/I2C. Questo è un **PASS TRANSITORIO DEL PREFLIGHT PASSIVO**, non un PASS di
commissioning o degli attuatori.

È stato poi eseguito un vero ciclo a freddo: CRICKIT portato su `OFF`, shutdown
ordinato Pi, rimozione USB-C e conferma di tutti i LED spenti e attuatori fermi.
Il Pi è ripartito con CRICKIT `OFF` alle `2026-08-29 17:35:56`, con
`throttled=0x0` e nessun evento kernel pertinente. Portando poi CRICKIT su `ON`,
l'operatore ha osservato LED principale verde, giallo spento, NeoPixel verde,
attuatori fermi e nessuna anomalia. Tuttavia `romeo-doctor`,
`romeo-doctor --student` e `romeo-doctor --json`, tutti con
`ROMEO_BACKEND=crickit`, hanno riprodotto `CRICKIT non raggiungibile`
(`ValueError`) in tre invocazioni consecutive. Otto campioni di alimentazione
erano tutti `throttled=0x0` e i log non contenevano undervoltage, brownout o
timeout I2C.

La singola pressione di `Seesaw Reset` prescritta dal troubleshooting Adafruit
non ha risolto il problema: LED rimasti nello stato apparentemente corretto,
attuatori fermi, ma Doctor ancora in FAIL. Collegando poi la sola micro-USB
Seesaw, senza Reset, non è cambiato nulla visivamente; il Pi ha però enumerato
subito `239a:002e Adafruit Crickit Hat` e Romeo Doctor ha nuovamente raggiunto
il CRICKIT, con `throttled=0x0`. Esito: **FAIL RIPRODUCIBILE DELL'AVVIO
AUTONOMO/ALIMENTAZIONE-COMUNE DEL SEESAW**. La micro-USB è un'evidenza
diagnostica e non viene accettata come soluzione o come autorizzazione al
commissioning. Nessun motore, servo o fotogramma camera è stato comandato.

## Inventario hardware e software

| Elemento | Modello / valore | Metodo | Stato / note |
|---|---|---|---|
| Raspberry Pi modello/revisione | Raspberry Pi 4 Model B Rev 1.5 | `tr -d '\0' </sys/firmware/devicetree/base/model; echo`, output riferito dall'operatore | VERIFICATO VIA DEVICE TREE |
| Raspberry Pi OS | Raspberry Pi reference `2025-12-04`, generato con `pi-gen` commit `4997bf4e4e49bc3305eb182a4a08bd023529da04`, stage4; userspace Debian GNU/Linux 13.2 (trixie) | `cat /etc/rpi-issue`; `cat /etc/os-release`, output riferito dall'operatore | VERIFICATO |
| Kernel | Linux `6.12.47+rpt-rpi-v8`, build `Debian 1:6.12.47-1+rpt1 (2025-09-16)`, aarch64 | `uname -a`, output riferito dall'operatore | VERIFICATO |
| CRICKIT HAT modello/revisione | Adafruit CRICKIT HAT per Raspberry Pi; bootloader Board-ID `SAMD21G18A-crickit-v0` | Ispezione fotografica, `INFO_UF2.TXT`, enumerazione USB | MODELLO VERIFICATO; revisione PCB non leggibile |
| Firmware CRICKIT | Immagine ufficiale Adafruit seesaw 1.1.6 per Crickit HAT, hash documentato | Artefatto verificato e copia UF2 completata; enumerazione applicativa `239a:002e` | INSTALLATO; versione runtime non esposta da un probe affidabile |
| Motore sinistro | Da determinare | Ispezione etichetta | NON VERIFICATO |
| Motore destro | Da determinare | Ispezione etichetta | NON VERIFICATO |
| Collegamento motori | Sinistro Motor 2, destro Motor 1 | Ispezione fisica riferita dall'operatore | VERIFICATO CABLAGGIO; verso non ancora provato |
| Servo pan | Da determinare | Ispezione etichetta e cablaggio | NON VERIFICATO |
| Canale pan | Servo 1 | Connettori scambiati ad alimentazioni rimosse e ricontrollati dall'operatore | VERIFICATO CABLAGGIO; movimento non provato |
| Servo tilt | Da determinare | Ispezione etichetta e cablaggio | NON VERIFICATO |
| Canale tilt | Servo 4 | Connettori scambiati ad alimentazioni rimosse e ricontrollati dall'operatore | VERIFICATO CABLAGGIO; movimento non provato |
| Camera | Raspberry Pi Camera Module con sensore `imx708`, 4608×2592 enumerato | `rpicam-hello --list-cameras`, senza acquisizione | SENSORE VERIFICATO; immagine non acquisita |
| Alimentazione Raspberry Pi | Powerbank SBS 10000 mAh / 37 Wh, uscita USB-C 5 V 3 A nominali, collegata direttamente all'ingresso USB-C Pi | Etichetta fotografata, osservazione operatore, `vcgencmd` e log | PASS A RIPOSO nei boot controllati; carico combinato non ancora provato |
| Alimentazione CRICKIT/motori | Pacco separato 4× AA Panasonic/eneloop NiMH, 1.2 V e min 2500 mAh per cella, jack DC | Etichetta celle e ispezione operatore; polarità riferita come verificata dal tecnico | MODELLO/CABLAGGIO VERIFICATI; tensione reale non misurata per assenza multimetro |
| Tensioni nominali | SBS: USB 1/2 output `5 V 3 A / 9 V 2 A / 10 V 2.25 A / 12 V 1.5 A`; USB-C output `5 V 3 A / 9 V 2.22 A / 12 V 1.67 A`; total output `22.5 W max`; batteria `10000 mAh (3.7 V, 37 Wh)` | Fotografie odierne della confezione fornite dall'operatore | VERIFICATO DA ETICHETTA; SKU coperto/non leggibile |
| Python sul Pi | 3.13.5 nella shell corrente | `python3 --version` | VERIFICATO PER L'INTERPRETE DI SISTEMA |
| `thebitlab-romeo` installato | 0.2.0 in `/home/acari/romeo-venv`, editable da `/home/acari/romeo-src`; `romeo-doctor` presente | `pip show`; `romeo-doctor --help` | PASS INSTALLAZIONE; nessun PASS hardware |
| Source/commit installato | `45e5f7e131802fccc89358a23a25dbed1884bbfa` | Clone pulito di `refs/heads/main`; `git rev-parse HEAD`, `git status` | VERIFICATO |
| I2C | `/dev/i2c-1` disponibile; CRICKIT `0x49` raggiungibile solo dopo alimentazione micro-USB Seesaw, non dopo avvio normale a freddo | Romeo Doctor tramite backend/safety; nessun bypass diretto | FAIL RIPRODUCIBILE ALL'AVVIO NORMALE |
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
| `ROMEO_BACKEND=crickit romeo-doctor` | 1 nelle invocazioni senza wrapper | FAIL-CLOSED | Dopo avvio normale a freddo: Python/package/backend/I2C/rete disponibili, CRICKIT non raggiungibile; calibrazione e identità assenti |
| `ROMEO_BACKEND=crickit romeo-doctor --student` | 1 nelle invocazioni senza wrapper | FAIL-CLOSED | Stesso FAIL CRICKIT a freddo; nessuna autorizzazione studente |
| `ROMEO_BACKEND=crickit romeo-doctor --json` | 1 nelle invocazioni senza wrapper | `preflight_failed`, `ready=false` | `crickit: failed`, `measured: ValueError`; con micro-USB Seesaw collegata lo stesso check passa, ma il workaround non è accettato come stato normale |

## Commissioning e safety reale

| Test | Risultato | Comando | Misura | Osservazione fisica operatore | Note |
|---|---|---|---|---|---|
| Avvio/shutdown con ruote sollevate | ESEGUITO, NESSUN MOVIMENTO INVOLONTARIO | `sudo shutdown -h now`, rimozione/riapplicazione supervisionata delle due alimentazioni | Power-cycle completo; `throttled=0x0` dopo riavvio | Tutti i LED spenti a sorgenti rimosse; ruote e servo sempre fermi; nessuna anomalia | Il power-cycle riproduce il FAIL Seesaw/I2C e quindi non autorizza commissioning |
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
