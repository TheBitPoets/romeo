# Secondo anno 23. Capstone telepresenza

## Obiettivo

In questa unità imparerai a integrare video, controllo, telemetria e safety.

## Che cosa sai già

Hai completato foto/video, controller, telemetria, safety e integrazione e sai documentare test e failure.

## Modello mentale

La telepresenza è un sistema a strati: input → controllo sicuro → Robot API → backend, mentre camera e telemetria riportano ciò che accade. Il capstone non richiede di riscrivere server o framework: lo scaffold fornisce infrastruttura, e il gruppo integra, verifica e spiega i confini. Ogni incremento deve lasciare Romeo fermo.

## Esempio minimo commentato

```text
1. status e foto funzionano con mock
2. controllo produce ack e stato coerente
3. stream può essere aperto e chiuso
4. timeout/disconnect producono STOP
5. demo ripetibile e log registrato
```

Questo è un piano di verifica, non codice da copiare: ogni riga diventa un checkpoint osservabile.

## Prova guidata

1. Disegna l'architettura con API, protocolli e backend separati.
2. Completa checkpoint status+camera con mock.
3. Aggiungi controllo e telemetria senza hardware.
4. Inietta payload invalido, timeout e disconnect e registra l'esito.
5. Esegui la demo completa due volte lasciando motori a zero.
6. Solo dopo la checklist docente, ripeti una prova breve sull'hardware reale.

## Esercizio base

Integra foto, un comando WebSocket, ack, stato versionato e STOP finale nel simulatore.

## Esercizio intermedio

Aggiungi stream e input accessibile, mantenendo separati UI, trasporto e Robot API.

## Mini-sfida

Dimostra con log automatico che disconnect, timeout e camera indisponibile degradano in modo sicuro e comprensibile.

## Consegna valutata

Completa `run_telepresence_session` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: integrare video, controllo, telemetria e safety.

## Errori tipici

- Assemblare componenti senza verificare ogni incremento.
- Mostrare movimento e video ma non i failure mode.
- Usare il robot reale prima di superare mock, simulazione e checklist safety.

## Autoverifica

- Ogni requisito ha un'evidenza osservabile?
- La stessa logica funziona con simulatore e backend reale?
- Ogni uscita o errore lascia i motori a zero e chiude camera/connessioni?

## Accessibilità

La demo offre pulsanti, tastiera rimappabile e log testuale; video e colore non sono l'unica evidenza. Definire ruoli di gruppo ruotabili e consenso camera.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `telepresenza` | controllo remoto accompagnato da percezione e stato |
| `fail-safe` | comportamento che porta a uno stato sicuro in caso di guasto |
| `checkpoint` | risultato intermedio verificabile |
