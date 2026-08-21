# Romeo

Romeo è una piattaforma didattica di Python e robotica per il primo biennio delle
scuole secondarie di secondo grado. Lo stesso programma usa un backend simulato,
mock o CRICKIT senza esporre agli studenti i dettagli dell'hardware.

```python
from time import sleep

from romeo.easy import forward, left, stop

forward()
sleep(2)
left()
sleep(0.6)
stop()
```

## Avvio rapido

Richiede Python 3.10 o successivo.

```console
python -m pip install -e ".[dev]"
python -m pytest
```

Il backend predefinito è il mock, quindi il primo programma è sicuro su un PC.
Per il simulatore interattivo:

```console
python -m pip install -e ".[web]"
python -m uvicorn romeo.web.app:create_app --factory --host 127.0.0.1 --port 8000
```

Apri quindi `http://127.0.0.1:8000/`. Per il laboratorio TCP separato usa
`romeo-tcp-server --backend sim` e collega `romeo-keyboard 127.0.0.1`.

Il plugin TheBitLab è scoperto come runtime `romeo-sim`. Le attività in
[`course/`](course/) possono essere lanciate o corrette headless e producono
risultato, traiettoria, event log e stato finale.

## Mappa del progetto

- `src/romeo/easy.py`: API a funzioni per il primo approccio;
- `src/romeo/robot.py`: API a oggetti e controllo diretto delle ruote;
- `src/romeo/simulation/`: motore 2D deterministico e grading;
- `src/romeo/web/`: REST, WebSocket e viewer Canvas;
- `src/romeo/network/`: protocollo TCP, server, client e tastiera;
- `src/romeo/camera/`: servizio camera, mock e adapter Picamera2;
- `course/`: Course Bundle TheBitLab con 20 unità del primo anno e 23 del secondo;
- `docs/`: audit, architettura, decisioni e guide tecniche.

L'accesso CRICKIT è isolato nell'extra `hardware`; i test CI non richiedono un
Raspberry Pi. Prima di usare il robot fisico leggere la
[checklist safety](docs/hardware/safety.md) e calibrare polarità, velocità e servo
su un'area libera.

---

## Guida di assemblaggio storica

<h2>Documentazione</h2>

<ul>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Crickit">Libreria python per Crickit-Hat</a> e <a href="https://docs.circuitpython.org/projects/crickit/en/latest/">Documentazione completa</a></li>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Crickit/blob/main/examples/crickit_dc_motor_simpletest.py">Esempio movimento motore ruota</a></li>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Crickit/blob/main/examples/crickit_servo_simpletest.py">Esempio movimento motore telecamera</a></li>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Crickit/blob/main/examples/crickit_neopixel_simpletest.py">Esempio uso LED</a></li>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Crickit/blob/main/examples/crickit_touch_simpletest.py">Esempio uso tasti</a></li>
</ul>

<h2>Installare Raspberry Pi OS e configurare il sistema</h2>

<p align="justify">
  La pagina della documentazione ufficiale di Raspberry Pi ( https://raspberrypi.com/documentation/ ) è un'ottima fonte per chi lavora con il Raspberry Pi.
</p>

<p align="justify">
  Per installare Raspberry Pi OS, procedere come segue:
</p>

<ol>
  <li>
    <p align="justify">Visita https://www.raspberrypi.com/software/operating-systems/</p>
  </li>
  <li>
    <p align="justify">
      Clicca sul link Raspberry Pi OS e scarica l'immagine "Raspberry Pi OS (64 bit)". Verrà scaricata l'ultima versione. L'immagine desktop include un ambiente desktop, che sarà utile quando creeremo applicazioni grafiche per i progetti robotici.
    </p>
    <div align="center">
      <img width="70%" src="https://github.com/TheBitPoets/romeo/blob/main/images/1_os_installation.png">
    </div>
  </li>
  <li>
    <p>
      Fare clic sul collegamento <a href="https://www.raspberrypi.com/software/">"Raspberry Pi Imager"</a> e seguire le istruzioni per scaricare e installare il software Imager
    </p>
    <div align="center">
      <img width="70%" src="https://github.com/TheBitPoets/romeo/blob/main/images/2_raspberry_pi_imager.png">
    </div>
  </li>
  <li>
    <p align="justify">
      Il Raspberry Pi 4 può essere installato e avviato sia da una scheda microSD che da una chiavetta USB. Le chiavette USB offrono prestazioni migliori e sono l'opzione consigliata.
    </p>
  </li>
  <li>
    <p align="justify">
      Utilizzare il software Imager per preparare il supporto di installazione con l'immagine scaricata (scheda microSD/unità flash USB).
    </p>
   <div>
    <div align="center">
      <img width="40%" src="https://github.com/TheBitPoets/romeo/blob/main/images/3_raspberry_pi_imager.png">
    </div>
    <div align="center">
      <img width="40%" src="https://github.com/TheBitPoets/romeo/blob/main/images/4_raspberry_pi_imager.png">
      <p align="justify">Nella schermata di sopra <b>fai attenzione ad accettare i termini della licenza</b> altrimenti il processo d'installazione non può proseguire</p>
    </div>
    <div align="center">
      <img width="40%" src="https://github.com/TheBitPoets/romeo/blob/main/images/5_raspberry_pi_imager.png">
    </div>
    <div align="center">
      <img width="40%" src="https://github.com/TheBitPoets/romeo/blob/main/images/6_raspberry_pi_imager.png">
      <p align="justify">Al termine del processo d'installazione <b>clicca su Fine</b></p>
    </div>
  </div>
  </li>
  <li>
    <p align="justify">
      Una volta avviato il Raspberry Pi con il programma di installazione, selezionare il modello della tua raspberry (nel nostro caso <b>Raspberry Pi 4</b>) e fare clic su Avanti nella schermata di benvenuto.
    </p>
     <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/7_raspberry_pi_imager.png">
    </div>
  </li>
  <li>
    <p align="justify">
      Scegli il sistema operativo da installare
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/8_raspberry_pi_imager.png">
    </div>
    <p align="justify">
      Seleziona il dispositivo rimovibile su cui installare il sistema operativo (nel nostro caso una penna usb che devi aver precedentemente collegato al PC)
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/9_raspberry_pi_imager.png">
    </div>
    <p align="justify">
      Continua la configurazione scegliendo hostname, nome utente e password etc. I passi principali sono mostrati nelle immagini di sotto
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/10_raspberry_pi_imager.png">
       <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/11_raspberry_pi_imager.png">
       <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/13_raspberry_pi_imager.png">
       <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/14_raspberry_pi_imager.png">
    </div>
    <p align="justify">
      Al termine del processo clicca su Scrivi per scrivere l'immagine del sistema operativo sulla penna USB. Non scollegare la penna prima che il processo sia terminato.
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/15_raspberry_pi_imager.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/16_raspberry_pi_imager.png">
    </div>
  </li>
  <li>
    <p align="justify">
     Alimenta la Rasperry, noi useremo un powerbank per ragione di mobilità (per fare questo hai bisogno di un cavo Type-C)
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/17_romeo_installation.png">
    </div>
       <p align="justify">
    Avrai bisogno anche di un adattatore HDMI <-> Micro HDMI ed ovviamente di un cavo HDMI per collegare uno schermo alla Rasperri Pi 4
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/18_romeo_installation.png">
    </div>
    <p align="justify">
    Guarda l'immagine di sotto per controllare i tuoi collegamenti. (Ovviamente devi collegare alla Rasperry Pi 4 anche un muose ed una tastiera attraverso le porte USB)
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/19_romeo_installation.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/19_romeo_installation2.png">
    </div>
  </li>
  <li>
    <p align="justify">
        Utilizziamo lo strumento di configurazione per abilitare le interfacce SSH, VNC e I2C. La Figura B.2 mostra come apparirà la schermata delle interfacce una volta abilitate
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/20_romeo_installation.png">
    </div>
  </li>
  <li>
    <p align="justify">
      Ora riavvia il Pi affinché le modifiche abbiano effetto
    </p>
  </li>
  <li>
    <p align="justify">
        Ottieni l'indirizzo IP della macchina eseguendo <code>ip a s</code> nel terminale
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/21_romeo_installation.png">
    </div>
  </li>
  <li>
    <p align="justify">
      Da un altro computer in rete, verifica di poter accedere tramite SSH al Raspberry Pi utilizzando il suo indirizzo IP. Su windows puoi usare <a href="https://putty.org/index.html">Putty</a> come client ssh. Ora puoi usare SSH per eseguire comandi ed eseguire script Python sul Pi da qualsiasi computer in rete
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/22_romeo_installation.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/23_romeo_installation.png">
    </div>
  </li>
  <li>
    La configurazione del Pi è terminata Possiamo passare alla configurazione dell'Adafruit CRICKIT HAT
  </li>
</ol>

<h2>Configurazione dell'Adafruit CRICKIT HAT</h2>

<p align="justify">
  Per completare la configurazione hardware e software dell'Adafruit CRICKIT HAT, seguire questi passaggi:
</p>

<div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/24_crickit_installation.png">
</div>

<ol>
  <li>
    <p align="justify">
      Sul sito web di Adafruit è disponibile una guida molto completa per configurare il CRICKIT HAT e risolvere eventuali problemi. Faremo riferimento a sezioni specifiche nei passaggi successivi ( https://learn.adafruit.com/adafruit-crickit-hat-for-raspberry-pi-linux-computers ).
    </p>
  </li>
  <li>
    <p align="justify">
      Prima di utilizzare il CRICKIT HAT per la prima volta, è consigliabile aggiornarne il firmware. Nella guida di apprendimento di Adafruit, seguire i passaggi nella sezione "Aggiorna il tuo CRICKIT" ( https://learn.adafruit.com/adafruit-crickit-hat-for-raspberry-pi-linux-computers/update-your-crickit )
    </p>
  </li>
  <li>
    <p align="justify">
      Spegnere il Raspberry Pi. Per collegare il CRICKIT HAT al Raspberry Pi, collegare prima il distanziatore fornito con il CRICKIT al connettore GPIO del Raspberry Pi. Quindi collegare il CRICKIT HAT
    </p>
  </li>
  <li>
    <p align="justify">
      Collegare il cavo di alimentazione al jack CC del CRICKIT e accendere l'interruttore di alimentazione del CRICKIT. Verificare che il LED del CRICKIT sia verde, a indicare che l'alimentazione è funzionante
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/26_crickit_installation.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/27_crickit_installation.png">
    </div>
  </li>
  <li>
    <p align="justify">
      Accendi il Raspberry Pi e apri un terminale o una connessione SSH.
    </p>
  </li>
  <li>
    <p align="justify">
      Esegui il comando <code>i2cdetect</code> e verifica che l'indirizzo I2C <code>0x49</code> appaia nell'output. L'indirizzo apparirà come testo, 49 come mostrato di seguito:
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/25_crickit_installation.png">
    </div>
  </li>
  <li>
    <p align="justify">
Eseguire i seguenti comandi per aggiornare i pacchetti software
    </p>
    <pre><code>
sudo apt update
sudo apt upgrade
sudo apt autoremove
    </code>
    </pre>
  </li>
  <li>
    <p align="justify">
Eseguire il seguente comando per riavviare la macchina
    </p>
    <pre><code>sudo reboot</code></pre>
  </li>
  <li>
    <p align="justify">
Dopo il riavvio, riconnettetevi alla macchina ed eseguite le seguenti righe per creare un ambiente virtuale Python e installare la libreria Adafruit CRICKIT in tale ambiente virtuale:
    </p>
    <pre><code>python3 -m venv ~/pyenv</code></pre>
    <pre><code>~/pyenv/bin/pip install adafruit-circuitpython-crickit</code></pre>
  </li>
  <li>
    <p align="justify">
Esegui la riga successiva per aggiungere l'alias bash <code>activate</code> che può essere utilizzato per attivare l'ambiente virtuale Python ogni volta che è necessario. Dopo aver eseguito il comando, apri un nuovo terminale affinché il nuovo alias abbia effetto:
    </p>
    <pre><code>echo "alias activate='source ~/pyenv/bin/activate'" >> ~/.bashrc</code></pre>
  </li>
  <li>
  <p align="justify">
Il comando successivo avvierà una sessione di ciclo di lettura-valutazione-stampa (REPL) Python nell'ambiente virtuale:    </p>
    <pre><code>~/pyenv/bin/python</code></pre>
  </li>
  <li>
    <p align="justify">
Eseguire il seguente codice Python nel REPL e verificare che il Neopixel integrato diventi rosso per configurare l'Adafruit CRICKIT HAT:    </p>
    <pre><code>
from adafruit_crickit import crickit
crickit.onboard_pixel.fill(0xFF0000)
    </code></pre>
     <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/28_crickit_installation.png">
    </div>
  </li>
</ol>

<h4>Costruzione robot mobile</h4>

<ol>
  <li>
    <p align="justify">
Il sito web di Adafruit offre un'eccellente guida sul CRICKIT HAT ( https://learn.adafruit.com/adafruit-crickit-hat-for-raspberry-pi-linux-computers ). Seguite le istruzioni nella guida per collegare il CRICKIT HAT al Raspberry Pi.
    <p>
  </li>
  <li>
    <p align="justify">
Quindi segui la guida Pibow ( https://learn.pimoroni.com/article/building-your-pibow ) per assemblare e posizionare il Raspberry Pi 4 nel case Pibow    
    <p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/29_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/30_build_robot.png">
    </div>
  </li>
   <li>
    <p align="justify">
Collegare il crickit-hat al pi e successivamente collegare anche i cavi di prolunga ai collegamenti del motore 1 e 2.  
    </p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/31_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/32_build_robot.png">
    </div>
   </li>
  <li>
    <p align="justify">
Ora possiamo assemblare il telaio del robot e collegare il power bank
    <p>
    <div align="center">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/33_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/34_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/36_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/37_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/38_build_robot.png">
      <p align="justify">
Prendiamo uno degli strati neri del telaio. Tutti e tre gli strati sono identici. Allinealo sul tavolo come mostrato nella figura di sopra. Nota che il pannello non è simmetrico : guarda a sinistra per vedere il rettangolo ritagliato. Assicurati che sia allineato come vedi qui! Fissare due dei distanziatori in ottone allo strato nero del telaio. I distanziatori devono essere avvitati nel secondo set di fori dal bordo esterno, ovvero nei due fori interni.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/39_build_robot.png">
      <p align="justify">
Girare il piatto. Fissare la ruota libera bianca nei fori esterni più vicini all'apertura rettangolare. La ruota libera bianca dovrebbe trovarsi sul lato opposto del telaio del distanziale.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/40_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/41_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/42_build_robot.png">
      <p align="justify">
Girare di nuovo il piatto. Prendi le ruote assemblate e inseriscile nello strato del telaio. Ci sono 2 slot sui pannelli neri che hai attaccato al motore che dovrebbero adattarsi perfettamente allo strato del telaio. La parte anteriore metallica del motore sarà rivolta verso il lato del telaio in cui hai posizionato la ruota libera bianca. Posiziona il livello successivo del telaio sopra i motori. Le due fessure sui pannelli neri che hai attaccato ai motori dovrebbero adattarsi perfettamente al livello successivo del telaio. Questo mantiene i motori in posizione in modo che non possano scivolare. Avvitare lo strato del telaio fissandolo ai distanziatori in ottone. Avvitare i restanti 2 o 4 distanziatori nel secondo strato del telaio. Puoi posizionarli praticamente ovunque, purché siano entrambi i lati.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/43_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/44_build_robot.png">
      <p align="justify">
Avvitare l'ultimo strato del telaio. CE L'HAI FATTA! Ora è il momento di aggiungere la Pi con il crickit-hat sopra l'ultimo strato.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/45_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/46_build_robot.png">
      <p align="justify">
Fissare il Raspberry Pi con il suo case allo strato superiore del telaio. Le porte USB del Raspberry Pi devono essere rivolte verso il retro del robot. In questo modo, i connettori di alimentazione del CRICKIT HAT e del Raspberry Pi rimangono più vicini ai cavi di alimentazione del power bank.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/47_build_robot.png">
      <p align="justify">
Inserite il powerbank nel ripiano intermedio e collegate i fili di collegamento ai motori CC. Assicuratevi di collegare il motore CC destro al connettore 1 e il motore CC sinistro al connettore 2.
      </p>
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/48_build_robot.png">
      <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/49_build_robot.png">
    </div>
  </li>
</ol>

<h4>Aggiunta telecamera anteriore servoassistita</h4>

<p align="justify">
  La configurazione del robot con telecamera servoassistita prevede un robot con una telecamera collegata a due servomotori. Un servomotore ci permetterà di muovere la telecamera in orizzontale, mentre l'altro applicherà un movimento di inclinazione. Seguite questi passaggi per costruire il robot:
</p>

<ul>
  <li>
  <p align="justify">
Il kit Adafruit Mini Pan-Tilt viene fornito completamente assemblato. Il kit supporta il montaggio di moduli telecamera di diverse dimensioni e stili. Questa guida all'assemblaggio del robot Adafruit ( https://learn.adafruit.com/pixy-pet-robot-color-vision-follower-using-pixycam?embeds=allow ) utilizza il kit Pan-Tilt e fornisce una spiegazione esaustiva su come rimuovere le linguette laterali necessarie per il passaggio successivo.
  </p>
  </li>
  <li>
  <p align="justify">
Il kit è dotato di due linguette laterali in nylon morbido che possono essere rimosse. È possibile rimuovere una delle linguette laterali ruotandola o utilizzando un tronchese. Ne basta una sola per tenerla in posizione.
  </p>
  </li>
  <li>
  <p align="justify">
Il passaggio successivo consiste nel collegare il Pan-Tilt Kit al Raspberry Pi. Consulta la <a href="https://www.raspberrypi.com/documentation/computers/camera_software.html">documentazione ufficiale Raspberry Pi sulla camera</a> per il collegamento e l'uso con libcamera/Picamera2.
  </p>
  </li>
    <li>
  <p align="justify">
Il CRICKIT HAT ha un'apertura per il cavo della fotocamera. Fai passare il cavo della fotocamera attraverso il CRICKIT HAT e collegalo al Raspberry Pi. Quindi collega il CRICKIT HAT al Raspberry Pi
  </p>
  <div align="center">
    <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/50_build_robot.png">
    <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/51_build_robot.png">
  </div>
  </li>
    <li>
  <p align="justify">
La guida Adafruit sul CRICKIT HAT, a cui si fa riferimento nella sezione precedente, è un'ottima risorsa per il collegamento del kit Pan-Tilt al CRICKIT HAT. In particolare, la sezione "Servocomandi" di CircuitPython fornisce dettagli approfonditi su come collegare i servomotori del kit Pan-Tilt al CRICKIT HAT.
La guida spiega l'orientamento in cui collegare i connettori del servo al CRICKIT HAT.
  </p>
  </li>
    <li>
  <p align="justify">
Collegare il connettore del servo inferiore alla connessione del servo 1 e il connettore del servo superiore alla connessione del servo 4.
  </p>
  </li>
      <li>
  <p align="justify">
Ora collega i cavi di alimentazione del CRICKIT HAT e del Raspberry Pi come abbiamo fatto nella sezione precedente.  </p>
  </li>
      <li>
  <p align="justify">
La Figura di sotto mostra l'aspetto del robot completamente assemblato. Questo robot può muovere la telecamera collegata sia in orizzontale che in verticale utilizzando i servomotori
  </p>
  <div align="center">
    <img width="60%" src="https://github.com/TheBitPoets/romeo/blob/main/images/52_build_robot.png">
  </div>
  </li>
</ul>
