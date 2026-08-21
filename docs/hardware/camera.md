# Telecamera Romeo

Romeo usa Picamera2, l'API basata su libcamera per Raspberry Pi OS moderno. Il
codice applicativo accede solo al contratto `CameraService`: import e lifecycle
Picamera2 restano nell'adapter hardware.

## Installazione sul Raspberry Pi

Il progetto Picamera2 raccomanda i pacchetti Raspberry Pi OS, perché mantengono
allineate le versioni di Picamera2 e libcamera:

```bash
sudo apt update
sudo apt install python3-picamera2
```

Su Raspberry Pi OS Lite è disponibile anche l'installazione ridotta:

```bash
sudo apt install python3-picamera2 --no-install-recommends
```

Verificare prima la camera con gli strumenti `rpicam-*` del sistema. L'API legacy
`picamera` non viene usata.

## API e stream

- `CameraService.capture_photo()` restituisce JPEG bytes;
- `CameraService.frames()` produce frame JPEG per MJPEG;
- `GET /api/camera/photo` acquisisce una fotografia;
- `GET /api/camera/stream` espone
  `multipart/x-mixed-replace; boundary=FRAME`;
- il comando `LOOK pan tilt` o il messaggio WebSocket `look` muove i servo tramite
  il backend Romeo, non tramite il servizio camera.

La prima implementazione privilegia chiarezza e portabilità: acquisisce JPEG con
`Picamera2.capture_file()` in un buffer e compone MJPEG nel server. Una futura
ottimizzazione può usare `MJPEGEncoder`/`FileOutput` mantenendo invariato
`CameraService`.

## Riferimento verificato

Implementazione confrontata il 21 agosto 2026 con il repository ufficiale
`raspberrypi/picamera2` al commit
`4509d7cd7fba79962f86da02fd3f2522d2e6db29`, in particolare gli esempi
`capture_to_buffer.py` e `mjpeg_server.py`.

## Verifica fisica ancora necessaria

La CI usa `MockCameraService`. Sul robot vanno ancora verificati risoluzione,
frame rate sostenibile, latenza, temperatura, orientamento dell'immagine e
interferenze tra movimento servo e cavo flat. Il test fisico resta marcato
`hardware` e skipped nelle macchine comuni.

