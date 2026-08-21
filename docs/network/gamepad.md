# Controllo con gamepad

Il client gamepad usa pygame per nascondere le differenze tra Windows, macOS e
Linux. La lettura diretta di `/dev/input/js0` resta un approfondimento avanzato,
non è richiesta nei primi laboratori.

## Installazione e avvio

```bash
python -m pip install ".[gamepad]"
romeo-gamepad 192.168.1.42
```

Il server Romeo deve essere già in esecuzione:

```bash
romeo-tcp-server --backend crickit
```

L'asse verticale controlla avanti/indietro e quello orizzontale la rotazione. Il
pulsante principale esegue STOP. Dead-zone e velocità massima sono applicate da
funzioni pure prima di inviare il comando `DRIVE left right`.

Il client:

- invia heartbeat mentre gli assi restano fermi in posizione non neutra;
- invia STOP quando il controller viene scollegato, la finestra termina o si
  verifica un errore;
- usa lo stesso lease esclusivo del client tastiera e del browser;
- non importa pygame finché il gamepad non viene realmente avviato.

La safety del server rimane l'ultima barriera: anche se il client scompare senza
poter inviare STOP, watchdog e command timeout azzerano i motori.

