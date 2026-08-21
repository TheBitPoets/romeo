# Secondo anno 20. Telemetria versionata

## Obiettivo

In questa unità imparerai a leggere stato senza dipendere dal renderer.

## Che cosa sai già

Conosci JSON, schema, coordinate del simulatore e WebSocket.

## Modello mentale

La telemetria è una fotografia strutturata dello stato inviata nel tempo. `schema_version` dice al client come leggere i campi; pose, motori, camera e tempo hanno nomi e unità documentati. Il renderer è soltanto un consumatore: il test può leggere gli stessi dati senza browser.

## Esempio minimo commentato

```python
state = engine.state()
assert state["schema_version"] == "romeo.simulation.state.v1"
pose = state["pose"]
print(pose["x"], pose["y"], state["time"])
```

Prima si controlla la versione, poi i campi; lo scaffold fornisce scenario ed engine.

## Prova guidata

1. Annota versione, pose, motori, camera e tempo in uno snapshot.
2. Controlla schema_version prima degli altri campi.
3. Leggi pose e unità documentate.
4. Confronta due snapshot dopo un passo simulato.
5. Simula una versione sconosciuta e rifiutala con un errore chiaro.

## Esercizio base

Valida versione e campi principali di uno snapshot.

## Esercizio intermedio

Calcola se Romeo è in movimento usando le due velocità motore dello snapshot.

## Mini-sfida

Scrivi un consumer che ignora campi aggiuntivi ma rifiuta versioni incompatibili e campi obbligatori mancanti.

## Consegna valutata

Genera uno snapshot simulato e verifica schema e campi.

## Errori tipici

- Leggere campi prima di controllare la versione.
- Confondere tempo simulato e ora del computer.
- Dipendere da coordinate o elementi HTML del viewer.

## Autoverifica

- So spiegare perché lo schema è versionato?
- Conosco unità e significato dei campi usati?
- Il mio consumer funziona senza renderer?

## Accessibilità

Presenta la telemetria come tabella e JSON copiabile; non affidarti soltanto all'animazione del viewer.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `telemetria` | stato misurato e comunicato nel tempo |
| `pose` | posizione e orientamento |
| `schema_version` | versione del contratto dei dati |
