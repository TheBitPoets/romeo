# Secondo anno 5. Un vero socket TCP

## Obiettivo

In questa unità imparerai a aprire server e client sul loopback.

## Che cosa sai già

Sai scambiare byte su una coppia locale e conosci indirizzo, porta, client e server.

## Modello mentale

Un server TCP prepara un punto di ascolto con `bind` e `listen`; `accept` crea un nuovo socket dedicato a un client. Il client usa `connect`. Per far avanzare server e client nello stesso programma lo scaffold avvia il server in un thread: la concorrenza è fornita, non è l'obiettivo da implementare oggi.

## Esempio minimo commentato

Lo scaffold contiene `serve_once` e il thread. Tu completi il client.

```python
with socket.create_connection(("127.0.0.1", porta), timeout=2) as client:
    client.sendall(b"HELLO\n")
    risposta = client.recv(32)
    assert risposta == b"WELCOME\n"
```

Il timeout impedisce un'attesa infinita; non garantisce che la rete risponda in tempo.

## Prova guidata

1. Ordina le tessere bind, listen, connect, accept, send, recv.
2. Segui nel diagramma il socket di ascolto e il nuovo socket restituito da `accept`.
3. Avvia lo scaffold e completa soltanto il blocco client.
4. Aggiungi timeout e verifica la risposta prima del marker.
5. Esegui due volte e controlla che thread e socket vengano sempre chiusi.

## Esercizio base

Completa il client che saluta il server fornito e valida `WELCOME`.

## Esercizio intermedio

Completa il corpo di `serve_once` nello scaffold, mantenendo timeout e context manager.

## Mini-sfida

Gestisci un saluto errato restituendo `ERROR` senza lasciare thread o socket aperti.

## Consegna valutata

Avvia un piccolo server in thread, collega il client e verifica la risposta.

## Errori tipici

- Chiamare `connect` prima che il listener sia pronto.
- Confondere il socket listener con quello della connessione accettata.
- Usare `recv` senza timeout durante il debug.

## Autoverifica

- So raccontare l'ordine di apertura della connessione?
- So indicare i due socket lato server?
- Il programma termina anche con input errato?

## Accessibilità

Fornisci anche una sequenza numerata testuale del diagramma temporale. Lo scaffold evita che difficoltà con i thread oscurino il concetto di TCP.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `listen` | mette il socket in attesa di connessioni |
| `accept` | accetta un client e restituisce il socket della connessione |
| `thread` | flusso concorrente fornito qui dallo scaffold |
