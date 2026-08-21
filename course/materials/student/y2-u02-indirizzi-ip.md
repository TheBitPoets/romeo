# Secondo anno 2. Indirizzi IP

## Obiettivo

In questa unità imparerai a risolvere un nome e riconoscere IPv4.

## Che cosa sai già

Sai distinguere host, rete e servizio e sai usare stringhe e confronti in Python.

## Modello mentale

Un indirizzo IP identifica un'interfaccia di rete, come un numero civico identifica una destinazione. Un nome come `localhost` è più facile da ricordare e viene risolto in un indirizzo. Il paragone postale non è perfetto: un host può avere più indirizzi e un indirizzo può cambiare.

## Esempio minimo commentato

Risolviamo un nome e poi controlliamo il risultato.

```python
import socket
from ipaddress import ip_address

testo = socket.gethostbyname("localhost")  # nome → testo IPv4
indirizzo = ip_address(testo)              # testo → oggetto verificabile
print(testo, indirizzo.version)
```

`gethostbyname` è fornita da Python: in questa lezione osserviamo la risoluzione, non la implementiamo.

## Prova guidata

1. Prevedi se `localhost` è un nome o un indirizzo.
2. Esegui l'esempio e annota il testo restituito.
3. Stampa `type(testo)` e `type(indirizzo)` per distinguere rappresentazione e oggetto.
4. Verifica che la versione sia 4 e che `indirizzo.is_loopback` sia vero.
5. Simula un errore passando a `ip_address` un testo non valido e leggi il messaggio senza nasconderlo.

## Esercizio base

Risolvi `localhost` e verifica che produca un IPv4 di loopback.

## Esercizio intermedio

Confronta `127.0.0.1` e il risultato della risoluzione spiegando perché rappresentano lo stesso percorso locale.

## Mini-sfida

Scrivi una funzione `descrivi(indirizzo)` che restituisce `locale` oppure `non locale` usando `is_loopback`.

## Consegna valutata

Completa `resolve_ipv4` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: risolvere un nome e riconoscere IPv4.

## Errori tipici

- Confondere il nome `localhost` con il suo indirizzo numerico.
- Controllare soltanto che il testo contenga punti invece di validarlo.
- Usare l'indirizzo locale pensando di raggiungere il Raspberry Pi remoto.

## Autoverifica

- So descrivere il passaggio nome → indirizzo?
- So distinguere stringa e oggetto `IPv4Address`?
- So verificare che un indirizzo sia loopback?

## Accessibilità

Leggi gli indirizzi anche cifra per cifra; non affidarti alla sola posizione in un diagramma e lascia il risultato testuale copiabile.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `indirizzo IP` | identificatore numerico di un'interfaccia di rete |
| `DNS` | sistema che risolve nomi in indirizzi |
| `IPv4` | formato di indirizzo composto da quattro numeri |
