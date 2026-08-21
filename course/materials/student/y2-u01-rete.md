# Secondo anno 1. Una rete di nodi

## Obiettivo

In questa unità imparerai a distinguere host, rete e servizio.

## Che cosa sai già

Sai eseguire un programma Python, usare variabili e leggere un semplice diagramma con frecce.

## Modello mentale

Una rete è un insieme di dispositivi che possono scambiarsi dati. Immagina una scuola: l'host è una persona, la rete è il sistema di corridoi e il servizio è lo sportello a cui la persona si rivolge. L'analogia aiuta a separare i ruoli, ma i dati viaggiano in piccoli blocchi e non come persone intere. `127.0.0.1` è il percorso speciale con cui un host parla a sé stesso.

## Esempio minimo commentato

Il primo esperimento non usa Internet: riconosce il percorso locale.

```python
from ipaddress import ip_address

indirizzo = ip_address("127.0.0.1")
print(indirizzo.is_loopback)  # True: il messaggio resta su questo computer
```

Lo scaffold importa `ip_address`: in questa unità non dobbiamo ancora conoscere i socket.

## Prova guidata

1. Disegna due host come rettangoli e una rete come linea fra loro; aggiungi un servizio dentro ogni host.
2. Esegui l'esempio e osserva che il risultato è un valore booleano.
3. Scrivi accanto a ogni elemento del disegno se è host, rete o servizio.
4. Sostituisci l'indirizzo con `192.0.2.10` e prevedi il risultato prima di eseguire.
5. Ripristina il loopback e usa un `assert` prima del messaggio finale.

## Esercizio base

Riconosci `127.0.0.1` come loopback e stampa il risultato soltanto dopo la verifica.

## Esercizio intermedio

Classifica sei esempi dati dal docente come host, collegamento di rete o servizio e motiva due risposte.

## Mini-sfida

Disegna il percorso concettuale computer studente → rete locale → Romeo → servizio di controllo, senza indicare ancora porte.

## Consegna valutata

Completa `is_loopback` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: distinguere host, rete e servizio.

## Errori tipici

- Confondere la rete con Internet: una rete può esistere anche senza accesso esterno.
- Chiamare servizio l'intero Raspberry Pi: il Raspberry Pi è l'host che ospita uno o più servizi.
- Pensare che loopback indichi Romeo: indica sempre il computer che esegue il programma.

## Autoverifica

- So indicare host, rete e servizio in un disegno?
- So spiegare dove resta un messaggio inviato a loopback?
- Il mio programma verifica il dato prima di dichiarare successo?

## Accessibilità

Usa etichette e forme oltre ai colori nel diagramma. È possibile descrivere a voce il percorso come elenco ordinato.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `host` | dispositivo collegato alla rete |
| `servizio` | funzione offerta da un programma |
| `loopback` | percorso con cui un host comunica con sé stesso |
