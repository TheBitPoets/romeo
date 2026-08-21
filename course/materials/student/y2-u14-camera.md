# Secondo anno 14. Camera come servizio

## Obiettivo

In questa unità imparerai a usare una camera sostituibile.

## Che cosa sai già

Sai usare oggetti, chiamare metodi e chiudere risorse con `try/finally`.

## Modello mentale

CameraService è una presa comune: il codice chiede una foto senza sapere se dietro c'è Picamera2 o un mock. Il mock restituisce dati prevedibili in classe e CI. La camera reale richiede hardware, permesso e segnalazione chiara; questi dettagli restano nell'implementazione del servizio.

## Esempio minimo commentato

```python
camera = MockCameraService()
try:
    foto = camera.capture_photo()
    assert foto.startswith(b"\xff\xd8")
finally:
    camera.close()
```

I byte non vengono visualizzati: controlliamo soltanto il contratto minimo del servizio.

## Prova guidata

1. Individua chiamante, interfaccia e implementazione nel diagramma.
2. Cattura una foto dal mock.
3. Osserva tipo e lunghezza senza stampare tutti i byte.
4. Sposta `close` in `finally`.
5. Simula camera non disponibile e produci un messaggio comprensibile.

## Esercizio base

Acquisisci e valida una foto dal mock senza importare Picamera2.

## Esercizio intermedio

Scrivi una funzione che riceve un CameraService come parametro e restituisce la dimensione della foto.

## Mini-sfida

Gestisci `available == False` senza tentare la cattura e garantendo cleanup.

## Consegna valutata

Acquisisci una foto dal mock senza importare Picamera2.

## Errori tipici

- Importare direttamente Picamera2 nel programma applicativo.
- Stampare migliaia di byte della foto.
- Dimenticare privacy e chiusura della camera su errore.

## Autoverifica

- Il mio codice funziona con un mock?
- La camera viene sempre chiusa?
- So spiegare perché l'hardware è isolato?

## Accessibilità

Descrivi testualmente stato camera e risultato; prevedi attività completa col mock per chi non può usare o essere ripreso dalla camera.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `CameraService` | contratto comune per le operazioni della camera |
| `mock` | sostituto prevedibile usato nei test |
| `JPEG` | formato compresso dei byte della foto |
