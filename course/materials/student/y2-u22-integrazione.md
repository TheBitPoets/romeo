# Secondo anno 22. Integra controllo e stato

## Obiettivo

In questa unità imparerai a collegare comando realtime e telemetria.

## Che cosa sai già

Hai completato WebSocket control, telemetria versionata e safety con disconnect.

## Modello mentale

L'integrazione collega due flussi senza confonderli: `/ws/control` riceve intenzioni e restituisce ack; `/ws/state` pubblica telemetria. Entrambi usano la stessa API Robot e lo stesso safety boundary. Lo scaffold fornisce app e connessioni; lo studente completa la sequenza e le verifiche end-to-end.

## Esempio minimo commentato

```text
controller → /ws/control → ack
                         ↓
                     Robot API
                         ↓
viewer     ← /ws/state ← state versionato
```

Il diagramma mostra dipendenze, non ordine temporale; la prova guidata aggiunge la timeline.

## Prova guidata

1. Etichetta control, ack, Robot API e state.
2. Apri i due canali scaffolded e verifica i messaggi ready.
3. Invia FORWARD e attendi ack.
4. Leggi uno state e verifica movimento e versione.
5. Chiudi il controller e verifica uno state successivo con motori a zero.

## Esercizio base

Collega un comando a un aggiornamento di stato osservabile.

## Esercizio intermedio

Verifica che payload invalido produca errore e non modifichi lo stato.

## Mini-sfida

Interrompi il canale control senza STOP esplicito e dimostra il fail-safe tramite il canale state.

## Consegna valutata

Completa `control_and_read` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: collegare comando realtime e telemetria.

## Errori tipici

- Usare REST polling e chiamarlo telemetria realtime.
- Considerare l'ack prova sufficiente del movimento.
- Chiudere il viewer ma lasciare vivo il controller senza timeout.

## Autoverifica

- So distinguere i due canali?
- Verifico sia ack sia stato?
- La perdita del control porta a motori zero?

## Accessibilità

Ack e telemetria sono disponibili come log testuale; il controller include pulsanti oltre a tastiera e gamepad.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `integrazione` | verifica congiunta di componenti già testati separatamente |
| `end-to-end` | prova dal comando fino allo stato osservato |
| `canale` | connessione con una responsabilità definita |
