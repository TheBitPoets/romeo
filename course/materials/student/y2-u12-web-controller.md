# Secondo anno 12. Controller web

## Obiettivo

In questa unità imparerai a tradurre input UI in messaggi validi.

## Che cosa sai già

Conosci eventi semplici, payload JSON e conversazione WebSocket ready/comando/ack.

## Modello mentale

Il controller web ha due responsabilità separate: un evento dell'interfaccia sceglie un comando; il trasporto lo invia. Lo scaffold fornisce pagina, connessione e listener del browser. Tu completi una funzione pura che traduce azione in payload, così puoi testarla senza clic reali.

## Esempio minimo commentato

```javascript
function payloadFor(action) {
  if (action === "forward") {
    return {command: "FORWARD", speed: 0.25};
  }
  return {command: "STOP"};
}
```

Il pulsante e la tastiera possono chiamare la stessa funzione; il feedback mostra l'ultimo ack anche come testo.

## Prova guidata

1. Associa ogni pulsante a un'azione scritta.
2. Prevedi il payload di avanti e stop.
3. Completa la funzione di traduzione nello scaffold.
4. Verifica i payload senza rete.
5. Collega la funzione al WebSocket fornito e osserva ack ed errore.

## Esercizio base

Traduci pulsanti avanti e stop in payload validi.

## Esercizio intermedio

Aggiungi indietro, sinistra e destra mantenendo una sola funzione di mapping.

## Mini-sfida

Disabilita i comandi di movimento quando la connessione non è pronta e lascia STOP sempre disponibile.

## Consegna valutata

Invia FORWARD via WebSocket, controlla ack, quindi STOP.

## Errori tipici

- Mescolare selezione del comando e dettagli del WebSocket in ogni pulsante.
- Inviare stringhe diverse dal protocollo documentato.
- Mostrare stato soltanto tramite colore senza testo.

## Autoverifica

- So testare il mapping senza browser?
- Tutti i controlli producono payload validi?
- L'interfaccia mostra connessione e ack in testo?

## Accessibilità

Ogni pulsante ha etichetta, focus da tastiera e stato testuale; non usare soltanto colore, hover o posizione per comunicare il comando.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `evento UI` | azione prodotta da pulsante o tastiera |
| `payload` | dati contenuti nel messaggio |
| `feedback` | informazione visibile sul risultato del comando |
