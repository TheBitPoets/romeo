# Architettura target

## Obiettivo

Lo stesso programma usa la stessa API Romeo nel simulatore e sul robot reale. Il
codice dello studente non conosce CRICKIT, server web, viewer o TheBitLab.

```text
programma studente
        |
        v
romeo.easy / Robot
        |
        v
controller e safety
        |
        +----------------------+----------------------+
        v                      v                      v
backend CRICKIT          backend simulato       backend mock
                               |
                        simulation engine
                               |
                      protocollo stato/eventi
                               |
                         viewer web 2D
```

## Confini

- **API pubblica:** funzioni elementari in `romeo.easy`, seguite dalla classe
  `Robot`. Niente pattern avanzati nel materiale introduttivo.
- **Backend:** contratto piccolo per motori e pan/tilt. Il backend reale è l'unico
  punto che importa librerie Raspberry Pi; il mock registra comandi; il simulatore
  traduce i comandi in dinamica differenziale.
- **Safety:** limite velocità, stop idempotente, command timeout, watchdog e stop
  durante errori/shutdown avvolgono il backend reale.
- **Simulazione:** stato 2D, clock discreto iniettato, scenari dati, collisioni e
  grading headless. Nessuna dipendenza dal browser.
- **Presentazione:** snapshot ed eventi versionati alimentano Canvas/SVG oggi e
  consentono un renderer futuro senza cambiare il motore.
- **Rete:** protocollo testuale TCP, REST e WebSocket sono adapter distinti verso
  la stessa API. La perdita del controller provoca stop.
- **Camera:** servizio sostituibile; Picamera2 è opzionale e caricata solo sul Pi.
- **TheBitLab:** activity extension `extensions.thebitlab.runtime`, entry point
  `thebitlab.runtimes`, runtime id `romeo-sim`, lifecycle ufficiale e soli
  dati/artefatti al confine.

## Flusso headless di grading

1. Il runtime valida attività, scenario e submission.
2. Crea un engine con seed, passo e clock dichiarati.
3. Esegue il programma entro limiti di tempo e risorse.
4. Valuta checkpoint, posa, collisioni e tempo simulato.
5. Restituisce risultato e artefatti: sorgente, trajectory JSON, event log,
   metriche e, quando disponibile, immagine finale.

## Dipendenze

Il nucleo rimane Python puro. FastAPI, Picamera2 e pygame sono extra opzionali per
non rendere l'esperienza headless dipendente da hardware o interfacce grafiche.
