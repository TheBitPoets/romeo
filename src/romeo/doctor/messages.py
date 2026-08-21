"""Student-facing explanations for Romeo Doctor checks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckHelp:
    label: str
    component: str
    purpose: str
    causes: tuple[str, ...]
    verify: tuple[str, ...]
    avoid: str


CHECK_HELP: dict[str, CheckHelp] = {
    "python": CheckHelp(
        "Python",
        "l'interprete Python che esegue Romeo",
        "Romeo e i suoi driver vengono caricati da Python.",
        ("la versione è troppo vecchia", "è attivo l'ambiente Python sbagliato"),
        ("esegui python3 --version", "attiva l'ambiente virtuale di Romeo"),
        "non installare pacchetti con sudo dentro un ambiente virtuale",
    ),
    "package": CheckHelp(
        "Romeo",
        "il package thebitlab-romeo",
        "contiene API, backend e protezioni usate dal robot.",
        ("il package non è installato", "il comando usa un altro Python"),
        ("esegui python3 -m pip show thebitlab-romeo",),
        "non copiare manualmente file dentro site-packages",
    ),
    "backend": CheckHelp(
        "Backend hardware",
        "la selezione del backend Romeo",
        "sul robot reale i comandi devono raggiungere CRICKIT.",
        ("ROMEO_BACKEND non è impostato su crickit",),
        ("controlla la configurazione persistente del servizio Romeo",),
        "non avviare test motori finché il backend non è quello atteso",
    ),
    "i2c": CheckHelp(
        "I2C",
        "il bus I2C tra Raspberry Pi e CRICKIT",
        "CRICKIT riceve i comandi dal Raspberry Pi attraverso questo bus.",
        ("I2C è disabilitato", "CRICKIT non è alimentato o collegato"),
        ("verifica che /dev/i2c-1 esista", "controlla I2C con raspi-config"),
        "non spostare cablaggi mentre il robot è alimentato",
    ),
    "crickit": CheckHelp(
        "CRICKIT",
        "il controller di motori e servo",
        "trasforma i comandi Romeo in segnali elettrici per gli attuatori.",
        ("driver non installato", "scheda spenta", "errore I2C o alimentazione"),
        ("controlla alimentazione e HAT", "prova di nuovo con le ruote sollevate"),
        "non bypassare il backend Romeo con uno script diretto",
    ),
    "calibration": CheckHelp(
        "Calibrazione",
        "la configurazione del singolo esemplare",
        "limita velocità e servo e registra polarità e trim osservati.",
        ("commissioning mai completato", "file corrotto", "versione package cambiata"),
        ("chiedi al docente di eseguire romeo-doctor --commission",),
        "non copiare la calibrazione di un altro robot",
    ),
    "watchdog": CheckHelp(
        "Watchdog",
        "il timeout automatico dei comandi motore",
        "ferma Romeo quando il controller smette di inviare comandi.",
        ("timeout assente o invalido", "backend safety non attivo"),
        ("controlla watchdog_timeout nella calibrazione",),
        "non aumentare il timeout per nascondere disconnessioni",
    ),
    "speed_limit": CheckHelp(
        "Limite velocità",
        "il limite massimo del singolo esemplare",
        "riduce energia e distanza di arresto durante le attività.",
        ("calibrazione assente", "valore fuori intervallo"),
        ("controlla speed_limit nella calibrazione",),
        "non usare 1.0 durante il collaudo iniziale",
    ),
    "camera": CheckHelp(
        "Camera",
        "Picamera2 e il modulo camera",
        "serve per foto e streaming delle attività visive.",
        ("cavo o connettore non inserito", "Picamera2 non installato", "camera occupata"),
        ("controlla il cavo a robot spento", "prova rpicam-hello"),
        "non mostrare o salvare immagini di persone senza autorizzazione",
    ),
    "network": CheckHelp(
        "Rete",
        "la connessione di rete del Raspberry Pi",
        "consente a controller e servizi didattici di raggiungere Romeo.",
        ("Wi-Fi o Ethernet disconnessi", "indirizzo non assegnato"),
        ("controlla l'icona rete", "esegui hostname -I"),
        "non pubblicare Romeo direttamente su Internet",
    ),
    "server": CheckHelp(
        "Server Romeo",
        "il servizio TCP configurato",
        "riceve comandi soltanto dalla rete didattica prevista.",
        ("servizio spento", "porta diversa", "firewall locale"),
        ("controlla lo stato del servizio Romeo",),
        "non disabilitare il firewall per far passare il test",
    ),
}
