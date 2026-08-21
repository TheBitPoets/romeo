# Secondo anno 13. Tastiera remota sicura

## Obiettivo

In questa unità imparerai a separare la mappa dei tasti dal trasporto e garantire lo stop finale.

## Che cosa sai già

Sai gestire un evento con una funzione e conosci il protocollo testuale e lo STOP WebSocket.

## Modello mentale

La tastiera produce tasti, ma il robot accetta comandi. Una funzione pura converte W/A/S/D/SPACE; un client separato trasporta il comando. Lo scaffold gestisce le differenze del terminale e la connessione: lo studente non deve leggere direttamente caratteri grezzi dal sistema operativo.

## Esempio minimo commentato

```python
from romeo.network.keyboard import command_for_key

comando = command_for_key("w")
print(comando.name)  # FORWARD
```

Lo STOP va inviato anche in `finally`, perché un errore o la chiusura non devono lasciare Romeo in movimento.

## Prova guidata

1. Compila la tabella W/A/S/D/SPACE.
2. Prova ogni tasto con la funzione pura.
3. Verifica maiuscole, minuscole e tasto sconosciuto.
4. Collega il mapping al client fornito.
5. Simula un errore e osserva lo STOP nel blocco `finally`.

## Esercizio base

Trasforma W e SPACE in FORWARD e STOP.

## Esercizio intermedio

Gestisci tutti i tasti previsti e ignora in modo esplicito quelli sconosciuti.

## Mini-sfida

Crea una sequenza controllata che invia STOP dopo un periodo senza nuovi tasti.

## Consegna valutata

Trasforma W e spazio nei comandi remoti FORWARD e STOP.

## Errori tipici

- Inviare il tasto grezzo invece del comando di protocollo.
- Dimenticare SPACE o lo STOP finale.
- Dipendere da una API terminal-specific non presente sul computer dello studente.

## Autoverifica

- So separare mapping e trasporto?
- Ogni uscita dal programma invia STOP?
- Esiste un'alternativa ai tasti per chi non può usarli?

## Accessibilità

Mantieni anche pulsanti cliccabili e rimappabili; stampa il comando riconosciuto e non richiedere pressioni simultanee.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `mapping` | corrispondenza fra tasto e comando |
| `timeout` | tempo massimo senza un nuovo evento |
| `finally` | blocco eseguito anche quando avviene un errore |
