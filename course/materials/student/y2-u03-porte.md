# Secondo anno 3. Porte e servizi

## Obiettivo

In questa unità imparerai a associare una porta libera a un socket.

## Che cosa sai già

Sai cos'è un host e sai usare tuple e `with` in Python.

## Modello mentale

L'indirizzo porta il messaggio all'host; la porta lo consegna al servizio corretto. Un endpoint è quindi la coppia `(indirizzo, porta)`. La porta `0` non è la porta del servizio: durante `bind` chiede al sistema di scegliere temporaneamente una porta disponibile.

## Esempio minimo commentato

Lo scaffold crea e chiude il socket; osserviamo solo l'assegnazione della porta.

```python
import socket

with socket.socket() as listener:
    listener.bind(("127.0.0.1", 0))
    endpoint = listener.getsockname()
    print(endpoint)  # per esempio ('127.0.0.1', 53124)
```

Il socket è una risorsa del sistema: `with` lo chiude anche in caso di errore.

## Prova guidata

1. Cerchia separatamente indirizzo e porta nell'endpoint dell'esempio.
2. Prevedi quale parte resta stabile e quale può cambiare fra due esecuzioni.
3. Esegui due volte e registra le porte scelte.
4. Estrai la porta con `listener.getsockname()[1]`.
5. Verifica che sia compresa fra 1 e 65535 prima di stampare il marker.

## Esercizio base

Chiedi una porta effimera al sistema e verifica che sia positiva.

## Esercizio intermedio

Crea due listener contemporanei sulla porta `0` e verifica che abbiano endpoint diversi.

## Mini-sfida

Spiega perché salvare una porta trovata chiudendo subito il socket non garantisce che resti libera.

## Consegna valutata

Completa `choose_free_port` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: associare una porta libera a un socket.

## Errori tipici

- Usare soltanto la porta e dimenticare l'indirizzo.
- Pensare che `0` sia la porta finale assegnata.
- Dimenticare di chiudere il socket dopo l'esperimento.

## Autoverifica

- So costruire un endpoint?
- So spiegare che cosa fa `bind`?
- So trovare la porta realmente assegnata?

## Accessibilità

Rappresenta l'endpoint sia come coppia scritta sia come diagramma. Pronuncia separatamente indirizzo e porta.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `porta` | numero che seleziona un servizio su un host |
| `endpoint` | coppia indirizzo e porta |
| `bind` | associazione di un socket a un endpoint locale |
