# Checklist di collaudo fisico

Registrare modello Raspberry Pi, revisione CRICKIT, alimentazione, data, tester e
commit. Per ogni riga segnare PASS/FAIL e una nota breve.

1. Robot sollevato: avvio e shutdown lasciano entrambi i motori a zero.
2. Verificare separatamente verso e polarità di ruota sinistra e destra al 20%.
3. Provare `forward`, `backward`, `left`, `right`, `stop` con limite velocità.
4. Interrompere client TCP e WebSocket in movimento: misurare il tempo allo STOP.
5. Lasciare scadere watchdog e command timeout; verificare STOP senza riavvio.
6. Provocare un errore controllato del backend; verificare motori a zero.
7. Misurare limiti meccanici pan/tilt senza forzare i servo.
8. Acquisire foto e MJPEG con Picamera2; annotare orientamento, latenza e temperatura.
9. Provare alimentazione peggiore prevista e controllare brownout/riavvii.
10. Ripetere shutdown e perdita alimentazione; ispezionare lo stato finale.
