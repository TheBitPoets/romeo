# Secondo anno 4. Client e server

## Obiettivo

In questa unità imparerai a scambiare byte tra due endpoint.

## Che cosa sai già

Sai distinguere host e servizio, conosci gli endpoint e sai usare byte letterali come `b"PING"`.

## Modello mentale

Il client avvia una richiesta; il server attende e risponde. In questa prima prova `socketpair` crea due estremità locali già collegate: nasconde indirizzi, porte e apertura della connessione per farci osservare soltanto lo scambio di byte. Non è ancora un server TCP reale.

## Esempio minimo commentato

```python
import socket

client, server = socket.socketpair()  # coppia locale già collegata
with client, server:
    client.sendall(b"PING\n")
    ricevuto = server.recv(16)
    print(ricevuto)                    # b'PING\n'
```

`recv(16)` può ricevere fino a 16 byte; una rete reale non promette un messaggio intero per ogni `recv`.

## Prova guidata

1. Disegna due estremità e una freccia PING dal client al server.
2. Esegui l'esempio e osserva la `b` davanti al dato stampato.
3. Aggiungi la risposta `PONG` nella direzione opposta.
4. Verifica entrambi i byte ricevuti con `assert`.
5. Rimuovi temporaneamente l'invio di PONG e prevedi perché il client rimarrebbe in attesa.

## Esercizio base

Completa uno scambio PING/PONG sulla coppia locale.

## Esercizio intermedio

Invia due parole in un unico blocco e separale usando il carattere di fine riga.

## Mini-sfida

Disegna che cosa dovrà essere aggiunto per trasformare la coppia locale in client e server TCP su loopback.

## Consegna valutata

Completa `exchange_ping_pong` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: scambiare byte tra due endpoint.

## Errori tipici

- Inviare una stringa invece di byte.
- Leggere prima che l'altra estremità abbia inviato.
- Credere che `recv(16)` restituisca sempre esattamente 16 byte.

## Autoverifica

- So indicare chi avvia ogni messaggio?
- So distinguere stringhe e byte?
- So chiudere entrambe le estremità?

## Accessibilità

Affianca alle frecce parole `invia` e `riceve`; recita la sequenza in ordine per chi non usa il diagramma.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `client` | programma che avvia una richiesta |
| `server` | programma che attende e risponde |
| `byte` | unità di dati trasmessa dal socket |
